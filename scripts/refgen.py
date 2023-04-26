import os, sys
import json
import requests
from jinja2 import Environment, FileSystemLoader, select_autoescape

def get_slug(docs, title):
    result = None
    for doc in docs:
        if doc['title'] == title:
            result = doc['slug']
        elif 'children' in doc:
            for child in doc['children']:
                if child['title'] == title:
                    return child['slug']
                
def req_format(req_body):
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
                b[k] = b2
            else:
                b[k] = v['type']
    elif 'items' in req_body:
        items = req_body['items']
        if 'properties' in items:
            properties = items['properties']
            b = [{}]
            for k,v in properties.items():
                b[0][k] = v['type']

    return json.dumps(b, indent=4, sort_keys=True)
      
def res_format(res_body):
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
                    b[k] = b2
            else:
                b[k] = v['type']
    elif 'items' in res_body['properties']['data']:
        items = res_body['properties']['data']['items']
        if 'properties' in items:
            properties = items['properties']
            b = [{}]
            for k,v in properties.items():
                b[0][k] = v['type']

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

if __name__ == '__main__':
    api_key = sys.argv[1]
    
    url = 'https://dash.readme.com/api/v1/categories'
    headers = {
        'Authorization': 'Basic {}'.format(api_key),
    }
    r = requests.get(url, headers=headers)

    if r.status_code != 200:
        print('Error fetching categories')
        sys.exit(1)

    category_id = [x for x in r.json() if x['slug'] == 'api-reference'][0]['id']

    url = "https://dash.readme.com/api/v1/categories/api-reference/docs"
    headers = {
        'Authorization': 'Basic {}'.format(api_key),
    }
    r = requests.get(url, headers=headers)

    if r.status_code != 200:
        print('Error fetching docs')
        sys.exit(1)
    
    docs = r.json()

    env = Environment(
        loader=FileSystemLoader('templates'),
        autoescape=select_autoescape(['html', 'xml'])
    )

    env.filters['res_format'] = res_format
    env.filters['req_format'] = req_format

    template = env.get_template('reference.md')

    with open('apis/clean.json') as f:
        specifications = json.load(f)

        for url in specifications['paths']:
            for method in specifications['paths'][url]:
                query_params = []
                path_params = []
                req_bodies = []
                res_body = {}

                page_title = specifications['paths'][url][method]['summary'] 
                page_excerpt = specifications['paths'][url][method]['description']
                title_slug = get_slug(docs, page_title)

                if 'parameters' in specifications['paths'][url][method]:
                    for param in specifications['paths'][url][method]['parameters']:
                        if param['in'] == 'query':
                            query_params.append(param)
                        elif param['in'] == 'path':
                            path_params.append(param)

                if 'requestBody' in specifications['paths'][url][method]:
                    schema = specifications['paths'][url][method]['requestBody']['content']['application/json']['schema']
                    if 'oneOf' in schema:
                        for req_body in schema['oneOf']:
                            req_bodies.append(req_body)
                    else:
                        req_bodies.append(schema)
                
                if 'responses' in specifications['paths'][url][method]:
                    print(page_title)
                    res_des = specifications['paths'][url][method]['responses']['200']['description']
                    if 'oneOf' in specifications['paths'][url][method]['responses']['200']['content']['application/json']['schema']:
                        schemas = specifications['paths'][url][method]['responses']['200']['content']['application/json']['schema']['oneOf']
                        res_body = [ x for x in schemas if 'data' in x['properties'] ][0]
                    else:
                        res_body = specifications['paths'][url][method]['responses']['200']['content']['application/json']['schema']

                t = template.render({
                    'page_title': page_title,
                    'page_excerpt': page_excerpt,
                    'category_id': category_id,
                    'title_slug': title_slug,
                    'query_params': query_params,
                    'path_params': path_params,
                    'req_bodies': req_bodies,
                    'res_des': res_des,
                    'res_body': res_body
                })

                file_name = page_title.replace(' ', '_').lower()

                with open('restref/{}.md'.format(file_name), 'w') as f:
                    f.write(t)
    

                
                    