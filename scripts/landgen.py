import os, sys, json, re
import requests
import copy
import concurrent.futures
from jinja2 import Environment, FileSystemLoader, select_autoescape

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
        
if __name__ == '__main__':
    with open('guides.json', 'r') as f:
        guides = json.load(f)
        LandingPageGen(guides).generate()
