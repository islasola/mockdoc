import json

if __name__ == '__main__':

    with open('apis/openapi.json', 'r') as f:
        specifications = json.load(f)
        
        for url in specifications['paths']:
            for method in specifications['paths'][url]:
                
                if 'parameters' in specifications['paths'][url][method]:
                    for param in specifications['paths'][url][method]['parameters']:
                        if 'example' in param:
                            del param['example']

        with open('apis/clean.json', 'w') as f:
            json.dump(specifications, f, indent=4)