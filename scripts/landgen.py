import os, sys, json, re
import asyncio
import requests as req
import copy
import concurrent.futures
from jinja2 import Environment, FileSystemLoader, select_autoescape
from asyncclient import AsyncClient
from dotenv import load_dotenv

class LandingPageGen:

    def __init__(self, guides):
        self.categories = guides
        self.landing_categories = ['Zilliz Cloud 101', 'AI Model Integrations', 'Advanced User Guides', 'Migration from Milvus']

    def generate(self):
        categories = [ dict(x, block_id=self.landing_categories.index(x['title'])) for x in self.categories if x['title'] in self.landing_categories ]

        for category in categories:
            for book in category['books']:
                book['max'] = self.__max_length(book['pages'])
                book['counts'] = len(book['pages'])  

        env = Environment(
            loader=FileSystemLoader('landing')
        )

        env.filters['max'] = max

        template = env.get_template('landing_temp.html')

        t = (template.render(dict(categories=categories)))

        with open('landing/index.html', 'w') as f:
            f.write(t)      


    def __max_length(self, pages):
        if pages:
            return max([ len(x['title']) for x in pages ])
        else:
            return 0
        

async def main():
    categories = req.post(f"https://api.notion.com/v1/databases/{ROOT_DATABASE_ID}/query", headers=notion_headers, json=payload)
    categories = categories.json()['results']

    remote_categories = req.get("https://dash.readme.com/api/v1/categories?perPage=20", headers=rdme_headers).json()

    for c in categories:
        for r in remote_categories:
            if c['properties']['Title']['title'][0]['plain_text'] == r['title']:
                c['rid'] = r['_id']
                c['slug'] = r['slug']
                c['title'] = r['title'] 

    categories = [ dict(
        id=x['id'],
        rid=x['rid'],
        title=x['title'], 
        slug=x['slug'],
        books=f"/v1/blocks/{x['id']}/children"
    ) for x in categories ]

    books = [ await notion_client.get(x['books']) for x in categories ]
    books = [ json.loads(x)['results'] for x in books ]
    
    categories = [ dict(
        id=x['id'],
        rid=x['rid'],
        title=x['title'], 
        slug=x['slug'],
        books=[z for z in y if z['type']=='child_database']
    ) for x, y in zip(categories, books) ]

    remote_books = [ await rdme_client.get(f"/api/v1/categories/{x['slug']}/docs") for x in categories ]
    remote_books = [ json.loads(x) for x in remote_books ]

    for i, c in enumerate(categories):
        if c['title'] == 'FAQs':
            break;
        
        docs_to_create = []
        for book in c['books']:
            book['id'] = book['id']
            book['title'] = book['child_database']['title'][3:]
            book['seq'] = int(book['child_database']['title'][:2])
            book['pages']=f"/v1/databases/{book['id']}/query"
            book['description']=f"/v1/databases/{book['id']}"
            if book['title'] not in [x['title'] for x in remote_books[i]]:
                docs_to_create.append({"title": book['title'], "order": book['seq'], "category": c['rid']})

        # get remote books
        remote_books[i] = req.get(f"https://dash.readme.com/api/v1/categories/{c['slug']}/docs", headers=rdme_headers).json()

        for x in c['books']:
            for y in remote_books[i]:
                if x['title'] == y['title']:
                    x['rid'] = y['_id']
                    x['slug'] = y['slug']
                    x['pages'] = y['children']

    with open('categories.json', "w") as f:
        json.dump(categories, f, indent=4)

    LandingPageGen(categories).generate()

if __name__ == '__main__':
    load_dotenv()

    README_API_KEY = os.environ.get('README_API_KEY')
    NOTION_API_KEY = os.environ.get('NOTION_API_KEY')
    NOTION_VERSION = os.environ.get('NOTION_VERSION')
    ROOT_DATABASE_ID = os.environ.get('ROOT_DATABASE_ID')   

    notion_headers = {
        "Authorization": f"Bearer {NOTION_API_KEY}",
        "NOTION-VERSION": NOTION_VERSION
    }

    rdme_headers = {
       "accept": "application/json",
       "content-type": "application/json",
       "authorization": f"Basic {README_API_KEY}"
    }

    notion_client = AsyncClient("https://api.notion.com", notion_headers)
    rdme_client = AsyncClient("https://dash.readme.com", rdme_headers)

    payload = {
        "filter": {
            "and": [
                {
                    "property": "Title",
                    "rich_text": {
                        "does_not_equal": "API Reference"
                    }
                },
                {
                    "or": [
                        {
                            "property": "Progress",
                            "select": {
                                "equals": "Drafted"
                            }
                        },
                        {
                            "property": "Progress",
                            "select": {
                                "equals": "Reviewed"
                            }
                        },                        
                    ]
                }
            ]
        },
        "sorts": [
            {
                "property": "Seq. ID",
                "direction": "ascending"
            }
        ]
    }  
    
    asyncio.run(main())  # LandingPageGen(guides).generate()
