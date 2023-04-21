import os
import json
from jinja2 import Environment, FileSystemLoader, select_autoescape

if __name__ == '__main__':
    env = Environment(
        loader=FileSystemLoader('templates'),
        autoescape=select_autoescape(['html', 'xml'])
    )

    template = env.get_template('reference.md')

    with open('apis/openapi.json') as f:
        specifications = json.load(f)

        for url in specifications['paths']:
            for method in specifications['paths'][url]:
                query_params = []
                path_params = []
                req_bodies = []
                res_body = {}

                page_title = specifications['paths'][url][method]['summary'] 
                page_excerpt = specifications['paths'][url][method]['description']

                if 'parameter' in specifications['paths'][url][method]:
                    for param in specifications['paths'][url][method]['parameters']:
                        if param['in'] == 'query':
                            query_params.append(param)
                        elif param['in'] == 'path':
                            path_params.append(param)
                            
                if 'requestBody' in specifications['paths'][url][method]:
                    request_body = specifications['paths'][url][method]['requestBody']['content']['application/json']['schema']
                    
                    if 'oneOf' in request_body:
                        for idx, oneOf in enumerate(request_body['oneOf']):
                            properties = request_body['oneOf'][idx]['properties']
                            # form a new dictionary of properties with name as the key and type as the value
                            req_bodies.append({"body": json.dumps(
                                {k: v['type'] for k, v in properties.items()},
                                sort_keys=True,
                                indent=4,
                                separators=(',', ': ')
                                ),
                                "properties": properties})
                            
                    else: 
                        properties = request_body['properties']
                        req_bodies.append({"body": json.dumps(
                            {k: v['type'] for k, v in properties.items()},
                            sort_keys=True,
                            indent=4,
                            separators=(',', ': ')
                            ),
                            "properties": properties})
                        
                if 'responses' in specifications['paths'][url][method]:
                    response_description = specifications['paths'][url][method]['responses']["200"]["description"]
                    response_body = specifications['paths'][url][method]['responses']["200"]["content"]["application/json"]["schema"]
                    response_body = [ x for x in response_body["oneOf"] if 'message' not in x['properties'] ]

                    if response_body:
                        properties = response_body[0]['properties']
                        if properties['data']
                        res_body["body"] = json.dumps(
                            {k: v['type'] for k, v in properties.items()},
                            sort_keys=True,
                            indent=4,
                            separators=(',', ': ')
                            )
                        res_body["properties"] = properties
                    
                t = template.render({
                    'page_title': page_title,
                    'page_excerpt': page_excerpt,
                    'query_params': query_params,
                    'path_params': path_params,
                    'req_bodies': req_bodies,
                    'response_description': response_description,
                    'res_body': res_body
                })

                file_name = page_title.replace(' ', '_').lower()

                with open('references/{}.md'.format(file_name), 'w') as f:
                    f.write(t)
    

                
                    