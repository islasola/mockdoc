import os, sys, json, re
import requests
import copy
import concurrent.futures
from jinja2 import Environment, FileSystemLoader, select_autoescape


def max_length(pages):
    if pages:
        return max([ len(x['title']) for x in pages ])
    else:
        return 0

def my_copy(obj):
    return copy.deepcopy(obj)


if __name__ == "__main__":
    
    api_key = sys.argv[1]

    headers = {
        'Authorization': 'Basic {}'.format(api_key),
    }
    
    url = 'https://dash.readme.com/api/v1/categories?perPage=50'

    r = requests.get(url, headers=headers)

    if r.status_code != 200:
        print('Error fetching categories')
        sys.exit(1)

    categories = r.json()  
    landing_categories = ['Zilliz Cloud 101', 'AI Model Integrations', 'Advanced User Guides', 'Migration from Milvus'] 

    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        children = [ executor.submit(requests.get, 'https://dash.readme.com/api/v1/categories/{}/docs'.format(x['slug']), headers=headers) for x in categories ]
        children = [ x.result() for x in children ]

        for category, child in zip(categories, children):
            category['books'] = child.json()

    
    categories = [ dict(x, block_id=landing_categories.index(x['title'])) for x in categories if x['title'] in landing_categories ]

    for category in categories:
        for book in category['books']:
            book['max'] = max_length(book['children'])
            book['counts'] = len(book['children'])

    print(categories[0]['books'][0]['title'])

    
    env = Environment(
        loader=FileSystemLoader('landing')
    )

    env.filters['max'] = max

    template = env.get_template('landing_temp.html')

    t = (template.render(dict(categories=categories)))

    with open('landing/index.html', 'w') as f:
        f.write(t)

