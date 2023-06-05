import os, sys
import json, csv
import requests
import concurrent.futures
from jinja2 import Environment, FileSystemLoader, select_autoescape
from errgen import ErrorGenerator

class RefGen:

    def __init__(self, specifications, category, parents):
        self.specifications = specifications
        self.category = category
        self.parents = parents

    def refgen(self):
        env = Environment(
            loader=FileSystemLoader('templates'),
            autoescape=select_autoescape(['html', 'xml'])
        )

        env.filters['res_format'] = self.res_format
        env.filters['req_format'] = self.req_format
        env.filters['list_error'] = self.list_error
        env.filters['get_example'] = self.get_example

        template = env.get_template('reference.md')

        for url in self.specifications['paths']:
            for method in self.specifications['paths'][url]:
                query_params = []
                path_params = []
                req_bodies = []
                res_body = {}

                page_title = self.specifications['paths'][url][method]['summary'] 
                page_excerpt = self.specifications['paths'][url][method]['description']
                page_parent = [ x['id'] for x in self.parents if x['title'] == self.specifications['paths'][url][method]['tags'][0] ][0]
                siblings = [ x for x in self.parents if x['id'] == page_parent ][0]['pages']
                page_slug = [ x for x in siblings if x['title'] == page_title ][0]['slug']
                page_url = [ x for x in siblings if x['title'] == page_title ][0]['url']
                page_method = [ x for x in siblings if x['title'] == page_title ][0]['method']
                server = self.specifications['servers'][0]['url'].replace('{cloud-region}', 'aws-us-west-2')
                
                
                if 'parameters' in self.specifications['paths'][url][method]:
                    for param in self.specifications['paths'][url][method]['parameters']:
                        if param['in'] == 'query':
                            query_params.append(param)
                        elif param['in'] == 'path':
                            path_params.append(param)

                if 'requestBody' in self.specifications['paths'][url][method]:
                    schema = self.specifications['paths'][url][method]['requestBody']['content']['application/json']['schema']
                    if 'oneOf' in schema:
                        for req_body in schema['oneOf']:
                            req_bodies.append(req_body)
                    else:
                        req_bodies.append(schema)
                
                if 'responses' in self.specifications['paths'][url][method]:
                    print(page_title)
                    res_des = self.specifications['paths'][url][method]['responses']['200']['description']
                    if 'oneOf' in self.specifications['paths'][url][method]['responses']['200']['content']['application/json']['schema']:
                        schemas = self.specifications['paths'][url][method]['responses']['200']['content']['application/json']['schema']['oneOf']
                        res_body = [ x for x in schemas if 'data' in x['properties'] ][0]
                    else:
                        res_body = self.specifications['paths'][url][method]['responses']['200']['content']['application/json']['schema']

                t = template.render({
                    'page_title': page_title,
                    'page_excerpt': page_excerpt,
                    'page_slug': page_slug,
                    'category_id': self.category,
                    'parent_id': page_parent,
                    'page_url': page_url,
                    'server': server,
                    'page_method': page_method,
                    'query_params': query_params,
                    'path_params': path_params,
                    'req_bodies': req_bodies,
                    'res_des': res_des,
                    'res_body': res_body
                })

                file_name = page_title.replace(' ', '_').lower()

                with open('restref/{}.md'.format(file_name), 'w') as f:
                    f.write(t)

    def groupgen(self):
        env = Environment(
            loader=FileSystemLoader('templates'),
            autoescape=select_autoescape(['html', 'xml'])
        )

        env.filters['get_slug'] = self.get_slug

        template = env.get_template('group.md')

        for group in self.parents:
            t = template.render({
                'group_title': group['title'],
                'group_slug': group['slug'],
                'category_id': self.category,
                'pages': group['pages']
            })

            file_name = group['title'].replace(' ', '_').lower()

            with open('restref/{}.md'.format(file_name), 'w') as f:
                f.write(t)

    def get_example(self, title):
        with open('apis/examples.md', 'r') as f:
            lines = f.readlines()
            start_poses = [ i for i, x in enumerate(lines) if x.startswith('## ') ]
            example_titles = [ x.strip()[3:] for x in lines if x.startswith('## ')]    

            for i, example_title in enumerate(example_titles):
                if example_title == title:
                    end_pos = start_poses[i+1] if i+1 < len(start_poses) else len(lines)
                    start_pos = start_poses[i] + 1
                    return ''.join(lines[start_pos:end_pos])    

    def get_slug(self, docs, title):
        for doc in docs:
            if doc['title'] == title:
                return doc['slug']
            elif 'children' in doc:
                for child in doc['children']:
                    if child['title'] == title:
                        return child['slug']
                    
    def req_format(self, req_body):
        b = None
        if 'properties' in req_body:
            properties = req_body['properties']

            b = {}
            for k,v in properties.items():
                if v['type'] == 'object':
                    b1 = {}
                    for k1,v1 in v['properties'].items():
                        b1[k1] = v1['type']
                        b[k] = b1
                elif v['type'] == 'array':
                    b2 = [{}]
                    if 'properties' in v['items']:
                        for k2,v2 in v['items']['properties'].items():
                            b2[0][k2] = v2['type']

                    b[k] = b2 if b2[0] else []
                else:
                    b[k] = v['type']
        elif 'items' in req_body:
            items = req_body['items']
            if 'properties' in items:
                properties = items['properties']
                b = [{}]
                for k,v in properties.items():
                    b[0][k] = v['type']
                
                b = b if b[0] else []

        return json.dumps(b, indent=4, sort_keys=True)
        
    def res_format(self, res_body):
        b = None
        if 'properties' in res_body['properties']['data']:
            properties = res_body['properties']['data']['properties']
        
            b = {}
            for k,v in properties.items():
                if v['type'] == 'object':
                    b1 = {}
                    for k1,v1 in v['properties'].items():
                        b1[k1] = v1['type']
                        b[k] = b1
                elif v['type'] == 'array':
                    b2 = [{}]
                    if 'properties' in v['items']:
                        for k2,v2 in v['items']['properties'].items():
                            b2[0][k2] = v2['type']
                        b[k] = b2 if b2[0] else []
                else:
                    b[k] = v['type']
        elif 'items' in res_body['properties']['data']:
            items = res_body['properties']['data']['items']
            if 'properties' in items:
                properties = items['properties']
                b = [{}]
                for k,v in properties.items():
                    b[0][k] = v['type']

                b = b if b[0] else []

        if b:
            return json.dumps({
                    "code": 200,
                    "data": b
                }, indent=4, sort_keys=True)
        else: 
            return json.dumps({
                    "code": 200,
                    "data": {}
                }, indent=4, sort_keys=True)
        
    def list_error(self, page_title):
        errgen = ErrorGenerator()
        if ''.join(page_title.split(' ')) in errgen.groups:
            group = errgen.groups[''.join(page_title.split(' '))]
            group.sort()
            return ''.join([ f'| {x} | {errgen.get_errorcode_desc(x)} |\n' for x in group])
        else:
            return '|  | (to be added) |\n'

if __name__ == '__main__':
    api_key = sys.argv[1]

    headers = {
        'Authorization': 'Basic {}'.format(api_key),
    }
    
    url = 'https://dash.readme.com/api/v1/categories'

    r = requests.get(url, headers=headers)

    if r.status_code != 200:
        print('Error fetching categories')
        sys.exit(1)

    category_id = [x for x in r.json() if x['slug'] == 'api-reference'][0]['id']
    category_slug = [x for x in r.json() if x['slug'] == 'api-reference'][0]['slug']

    url = "https://dash.readme.com/api/v1/categories/api-reference/docs"

    r = requests.get(url, headers=headers)

    if r.status_code != 200:
        print('Error fetching docs')
        sys.exit(1)
    
    docs = r.json()

    with open('apis/clean.json') as f:
        specifications = json.load(f)

    groups = [ dict(title=x['name']) for x in specifications['tags'] ]

    for group in groups:
        for doc in docs:
            if doc['title'] == group['title']:
                group['id'] = doc['_id']
                group['slug'] = doc['slug']
                break
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        groups = [ executor.submit(
            requests.post, 
            'https://dash.readme.com/api/v1/docs', 
            headers=headers, 
            json={"title": x["title"], "category": category_id, "hidden": False}
        ) if 'slug' not in x else x for x in groups ]

        groups = [ dict(
            id=x.result().json()['id'],
            title=x.result().json()['title'],
            slug=x.result().json()['slug'],
        ) if isinstance(x, concurrent.futures.Future) else x for x in groups ]

    remote_pages = requests.get('https://dash.readme.com/api/v1/categories/api-reference/docs', headers=headers).json()

    pages = [ dict(
        title=specifications['paths'][url][method]['summary'],
        description=specifications['paths'][url][method]['description'],
        url=url,
        method=method,
        group=specifications['paths'][url][method]['tags'][0],
    )  for url in specifications['paths'] for method in specifications['paths'][url] ]

    for group in groups:
        group['pages'] = []
        remotes = []
        for remote_page in remote_pages:
            if remote_page['title'] == group['title']:
                remotes= remote_page['children']
        for page in pages:
            for remote in remotes:
                if page['title'] == remote['title']:
                    page['id'] = remote['_id']
                    page['slug'] = remote['slug']

            if page['group'] == group['title']:
                group['pages'].append(page)

    for group in groups:
        with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
            remote_pages = [ executor.submit(
                requests.post, 
                'https://dash.readme.com/api/v1/docs', 
                headers=headers, 
                json={"title": x["title"], "category": category_id, "parentDoc": group['id'], "hidden": False}
            ) if 'slug' not in x else x for x in group['pages'] ]

            remote_pages = [ dict(
                id=x.result().json()['id'],
                title=x.result().json()['title'],
                slug=x.result().json()['slug'],
            ) if isinstance(x, concurrent.futures.Future) else x for x in remote_pages ]

        for page in group['pages']:
            for remote_page in remote_pages:
                if page['title'] == remote_page['title']:
                    page['id'] = remote_page['id']
                    page['slug'] = remote_page['slug']

    refgen = RefGen(specifications, category_id, groups)
    refgen.refgen()
    refgen.groupgen()

