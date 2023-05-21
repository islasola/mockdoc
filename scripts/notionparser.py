import requests
import boto3
import re
import logging
from urllib import parse
from sys import stdout
from io import BytesIO
import json
import os

class NotionPageParser:

    def __init__(self, page_id):
        self.notion_headers = {
            'Accept': 'application/json',
            'Authorization': f'Bearer {os.environ["notion_api"]}',
            'Notion-Version': os.environ["notion_version"]
        }
        self.figma_headers = {
            'Accept': 'application/json',
            'X-Figma-Token': os.environ["figma_api"]
        }
        self.page_id = page_id
        self.page = self.__retrieve_page()
        self.page_title = self.__page_title(self.page)
        self.page_slug = self.__page_slug(self.page_title)
        self.blocks = self.__retrieve_page_children()['results']
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)
        self.logger.addHandler(logging.StreamHandler(stdout))

    def markdown(self, blocks=None):
        blocks = self.blocks if blocks is None else blocks
        return self.__markdown(blocks)
    
    def synced_block(self, block):
        return self.__synced_block(block)
    
    def quote(self, block):
        return self.__quote(block)

    def __markdown(self, blocks=None):
        prev_block_type = None
        markdown = []
        for block in blocks:
            if prev_block_type == 'quote' and block['type'] != 'quote':
                markdown.append('\n')
            if prev_block_type == 'bulleted_list_item' and block['type'] != 'bulleted_list_item':
                markdown.append('\n')
            if prev_block_type == 'numbered_list_item' and block['type'] != 'numbered_list_item':
                markdown.append('\n')
            if block['type'].startswith('heading'):
                markdown.append(self.__header(block))
                prev_block_type = block['type']
            if block['type'] == 'paragraph':
                markdown.append(self.__paragraph(block))
                prev_block_type = block['type']
            if block['type'] == 'quote':
                markdown.append(self.__quote(block))
                prev_block_type = block['type']
            if block['type'] == 'bulleted_list_item':
                markdown.append(self.__bullet_list_item(block))
            if block['type'] == 'numbered_list_item':
                markdown.append(self.__numbered_list_item(block))
                prev_block_type = block['type']
            if block['type'] == 'link_preview':
                markdown.append(self.__link_preview(block))
                prev_block_type = block['type']
            if block['type'] == 'link_to_page':
                markdown.append(self.__link_to_page(block))
                prev_block_type = block['type']
            if block['type'] == 'table':
                markdown.append(self.__table(block))
                prev_block_type = block['type']
            if block['type'] == 'code':
                markdown.append(self.__code(block))
                prev_block_type = block['type']
            if block['type'] == 'synced_block':
                markdown.append(self.__synced_block(block))
                prev_block_type = block['type']
            if block['type'] == 'image':
                markdown.append(self.__image(block))
                prev_block_type = block['type']

        return ''.join(markdown)
        
    def __retrieve_page(self, page_id=None):
        if page_id is None:
            page_id = self.page_id

        url = f'https://api.notion.com/v1/pages/{page_id}'
        r = requests.get(url, headers=self.notion_headers)

        if r.status_code != 200:
            message = r.json()['message']
            raise Exception(f'Failed to retrieve page children: {r.status_code} {message}')
        
        return r.json()
    
    def __retrieve_page_children(self):
        url = f'https://api.notion.com/v1/blocks/{self.page_id}/children'
        r = requests.get(url, headers=self.notion_headers)
        
        if r.status_code != 200:
            message = r.json()['message']
            raise Exception(f'Failed to retrieve page children: {r.status_code} {message}')
        
        return r.json()
    
    def __header(self, block):
        if block['type'] == 'heading_1' or block['type'] == 'heading_2':
            type = block['type']
            return f"## {block[type]['rich_text'][0]['plain_text']}\n\n"
        if block['type'] == 'heading_3':
            return f"### {block['heading_3']['rich_text'][0]['plain_text']}\n\n"
        
    def __code(self, block, tabSize=4):
        caption = block['code']['caption']

        if len(caption):
            caption = f" {caption[0]['plain_text']}"
        else:
            caption = ''
        
        code = block['code']['rich_text']

        if len(code):
            code = code[0]['plain_text'].replace('\t', ' ' * tabSize)
        else:
            code = ''

        lang = block['code']['language']

        return f"```{lang}{caption}\n{code}\n```\n\n" 

    def __synced_block(self, block):
        print(block['synced_block']['synced_from'])
        if not block['synced_block']['synced_from']:
            url = f'https://api.notion.com/v1/blocks/{block["id"]}/children'
        else:
            url = f'https://api.notion.com/v1/blocks/{block["synced_block"]["synced_from"]["block_id"]}/children'
        r = requests.get(url, headers=self.notion_headers)
        
        if r.status_code != 200:
            message = r.json()['message']
            raise Exception(f'Failed to retrieve page children: {r.status_code} {message}')
        
        children = r.json()['results']

        return self.__markdown(blocks=children)

    def __image(self, block):
        if 'file' in block['image']:
            file = block['image']['file']['url']
            image_content = requests.get(file).content
            caption = block['image']['caption']

            if len(caption) == 0:
                caption = block['id']

            try:
                self.__upload_to_s3(caption, image_content)
            except Exception as e:
                print(e)
                
            return f"![{caption}](https://assets.zilliz.com/zdoc/{caption}.png)\n\n"
        
        if 'external' in block['image']:
            caption = block['image']['caption']

            if len(caption) == 0:
                caption = block['id']

            return f"![{caption}]({block['image']['external']['url']})\n\n"
            

    def __quote(self, block):
        plain_text = block['quote']['rich_text'][0]['plain_text']
        if plain_text.endswith('Notes') or plain_text.endswith('Warning'):
            return f"> {block['quote']['rich_text'][0]['plain_text']}\n> "
        else:
            segments = block['quote']['rich_text']
            return f"> {self.__paragraph(segments=segments)[:-2]}"
        
    def __bullet_list_item(self, block):
        segments = block['bulleted_list_item']['rich_text']
        return f"* {self.__paragraph(segments=segments)}"

    def __numbered_list_item(self, block):
        segments = block['numbered_list_item']['rich_text']
        return f"1. {self.__paragraph(segments=segments)}"
    
    def __link_preview(self, block):
        url = block['link_preview']['url']
        if url.startswith('https://www.figma.com/file/'):
            url = parse.urlsplit(url)
            key = url.path.split('/')[2]
            query = parse.parse_qs(url.query)
            node = query['node-id'][0]

            title = self.__figma_retrieve_image_title(key, node)
            content = self.__figma_retrieve_image_content(key, node)

            try:
                self.__upload_to_s3(title, content)
            except Exception as e:
                print(e)
            
            return f"![{title}](https://assets.zilliz.com/zdoc/{title}.png)\n\n"
    
    def __link_to_page(self, block):
        page_id = block['link_to_page']['page_id']
        title = self.__retrieve_page(page_id)['properties']['Title']['title'][0]['text']['content']
        slug = self.__page_slug(title)

        return f"- [{title}](docs:{slug})\n"
    
    def __table(self, block):
        id = block['id']
        # table_width = block['table']['table_width']
        # has_column_header = block['table']['has_column_header']
        # has_row_header = block['table']['has_row_header']

        url = f'https://api.notion.com/v1/blocks/{id}/children'
        r = requests.get(url, headers=self.notion_headers)
        
        if r.status_code != 200:
            message = r.json()['message']
            raise Exception(f'Failed to retrieve page children: {r.status_code} {message}')
        
        rows = r.json()['results']
        rows_length_matrix = map(self.__table_row_cell_lengths, rows)
        rows_template = list(map(max, zip(*rows_length_matrix)))
        table_header_divider = list(map(lambda x: '-' * x, rows_template))
        rows = list(map(self.__table_row_cells, rows))
        rows.insert(1, table_header_divider)
        rows = '\n'.join([ self.__format_table_row(x, rows_template) for x in rows ])

        return f"{rows}\n\n"

    def __table_row_cells(self, block):
        cells = block['table_row']['cells']
        cells = map(lambda x:  self.__paragraph(segments=x)[:-2] if len(x) > 0 else '   ', cells)
        
        return list(cells)
    
    def __format_table_row(self, row, temp):
        for i in range(len(temp)):
            if len(row[i]) < temp[i]:
                row[i] = row[i] + (temp[i] - len(row[i])) * ' '

        return '| ' + ' | '.join(row) + ' |'
    
    def __table_row_cell_lengths(self, block):
        cells = block['table_row']['cells']
        cells = map(lambda x: len(self.__paragraph(segments=x)[:-2]) if len(x) > 0 else 3, cells)
        
        return list(cells)        

    def __paragraph(self, block=None, **kwargs):
        if 'segments' in kwargs:
            segments = kwargs['segments']
        else:
            segments = block['paragraph']['rich_text']

        segments = map(self.__parse_text, segments)

        return ''.join(segments) + "\n\n"

    def __parse_text(self, segment):
        if segment['type'] == 'text':
            if segment['text']['link']:
                url = segment['text']['link']['url']
                if re.match('/[a-z0-9]', url):
                    url = self.__retrieve_page(page_id=url[1:])
                    url = url['properties']['Title']['title'][0]['text']['content']
                    url = f"docs:{self.__page_slug(url)}"
                return f"[{segment['plain_text']}]({url})"
            elif segment['annotations']['bold']:
                return f"**{segment['plain_text']}**"
            elif segment['annotations']['italic']:
                return f"*{segment['plain_text']}*"
            elif segment['annotations']['strikethrough']:
                return f"~~{segment['plain_text']}~~"
            elif segment['annotations']['underline']:
                return f"<u>{segment['plain_text']}</u>"
            else:
                return segment['plain_text']
        else:
            return ''
            
    def __figma_retrieve_image_content(self, key, node):
        url = f'https://api.figma.com/v1/images/{key}?ids={node}&scale=2&format=png'
        r = requests.get(url, headers=self.figma_headers)

        if r.json()['err']:
            raise Exception(f'Failed to retrieve figma nodes: {r.status_code} {r.json()["err"]}')
        
        node_key = ":".join(node.split('-'))
        image = requests.get(r.json()['images'][node_key])
        
        return BytesIO(image.content)
    
    def __figma_retrieve_image_title(self, key, node):
        url = f'https://api.figma.com/v1/files/{key}/nodes?ids={node}'
        r = requests.get(url, headers=self.figma_headers)

        if r.status_code != 200:
            raise Exception(f'Failed to retrieve figma nodes: {r.status_code} {r.json()["err"]}')
        
        node_key = ":".join(node.split('-'))
        title = r.json()['nodes'][node_key]['document']['name']
        
        return title
        
    def __upload_to_s3(self, img_title, img_content):
        s3 = boto3.resource('s3')
        bucket = "assets.zilliz.com"

        try:
            response = s3.Bucket(bucket).put_object(Key=f'zdoc/{img_title}.png', Body=img_content, ACL='public-read')
        except Exception as e:
            raise Exception(f'Failed to upload to s3: {e}')
        
        return response
    
    def __page_title(self, page):
        if 'Title' in page['properties']:
            if len(page['properties']['Title']['title']) > 0:
                if 'mention' in page['properties']['Title']['title'][0]:
                    return page['properties']['Title']['title'][0]['plain_text']
            
                return page['properties']['Title']['title'][0]['text']['content']
        elif 'Question' in page['properties']:
            return page['properties']['Question']['title'][0]['text']['content']
        else:
            return ''
    
    def __page_slug(self, title):
        return '-'.join([ x.lower() for x in title.split(' ') if re.match(r'[a-zA-Z0-9]', x) ]) \
            .replace('/', '-') \
            .replace(',', '') \
            .replace('.', '_')

class NotionDatabaseParser:

    def __init__(self):
        self.headers = {
            'Accept': 'application/json',
            'Authorization': f'Bearer {os.environ["notion_api"]}',
            'Notion-Version': os.environ['notion_version']
        }

    def retrieve(self, id, query=None):
        url = f'https://api.notion.com/v1/databases/{id}/query'

        if query:
            r = requests.post(url, headers=self.headers, json=query)
        else:
            r = requests.post(url, headers=self.headers)

        if r.status_code != 200:
            message = r.json()['message']
            raise Exception(f'Failed to retrieve database: {r.status_code} {message}')

        return self.__map(r.json()['results'])  
        
    def book_title(self, id):
        url = f'https://api.notion.com/v1/databases/{id}'

        r = requests.get(url, headers=self.headers)

        return re.sub("[0-9]+ ", "", r.json()['title'][0]['text']['content'])

    def __map(self, results):  
        r = []
        for item in results:
            page_id = item['id']
            page_title = re.sub('[0-9]*\s$', '', item['properties']['Title']['title'][0]['plain_text'])
            page_slug = self.__title_slug(page_title)
            page_tags = [x['name'] for x in item['properties']['Tags']['multi_select']]
            page_progress = item['properties']['Progress']['select']['name']
            page_version = item['properties']['Version']['rich_text'][0]['plain_text']
            if 'Reuse' in page_tags:
                page_id = item['properties']['Title']['title'][0]['mention']['page']['id']

            children = self.__child_page(page_id)

            r.append({
                'page_id': page_id,
                'page_title': page_title,
                'page_slug': page_slug,
                'page_tags': page_tags,
                'page_progress': page_progress,
                'page_version': page_version,
                'children': children
            })

        return r
    
    def __child_page(self, page_id):
        page = NotionPageParser(page_id)
        print(f"Retrieving page: {page.page_title}")
        return page

    def __title_slug(self, title):
        if title:
            # write a slug converter that ignores non-alphanumeric characters
            return '-'.join([ x.lower() for x in title.split(' ') if re.match(r'[a-zA-Z0-9]', x) ]) \
                .replace('/', '-') \
                .replace(',', '') \
                .replace('.', '_')
        
    def overview(self, pages):
        excerpts = []
        for page in pages:
            page = page['children']
            page_title = page.page_title
            page_slug = page.page_slug
            blocks = page.blocks
            if len(blocks) == 0:
                excerpts.append("- *[{page_title}](doc:{page_slug})*\n\n    No short description available")
            elif blocks[0]['type'] == 'synced_block':
                children = page.synced_block(blocks[0])
                children = children.split('\n')[0]
                excerpts.append(f"- *[{page_title}](doc:{page_slug})*\n\n    {children}")
            else:
                excerpts.append(f"- *[{page_title}](doc:{page_slug})*\n\n    {page.markdown([page.blocks[0]])}")
                    
        return '\n'.join(excerpts)

class ReadmeOperator:

    def __init__(self):
        self.headers = {
            "accept": "application/json",
            "content-type": "application/json",
            "authorization": f"Basic {os.environ["readme_api"]}"
        } 
        self.cat_url = "https://dash.readme.com/api/v1/categories"
        self.doc_url = "https://dash.readme.com/api/v1/docs"

    def retrieve_categories(self):
        r = requests.get(self.cat_url, headers=self.headers)
        categories = r.json()
        return categories
    
    def retrieve_docs_in_category(self, category_slug):
        r = requests.get(f"{self.cat_url}/{category_slug}/docs", headers=self.headers)
        docs = r.json()
        return docs
    
    def retrieve_sub_pages_in_doc(self, category_slug, doc_id):
        r = requests.get(f"{self.cat_url}/{category_slug}/docs", headers=self.headers)
        sub_pages = list(filter(lambda x: x['_id'] == doc_id , r.json()))[0]['children']
        return sub_pages
    
    def add_category(self, title, type='guide'):
        r = requests.post(self.cat_url, headers=self.headers, json={"title": title, "type": type})
        return r.json()
    
    def add_page(self, title, body=None, category=None, parent=None):
        payload = {
            "title": title,
            "category": category
        }

        if body:
            payload['body'] = body
        
        if parent:
            payload['parentDoc'] = parent

        r = requests.post(self.doc_url, headers=self.headers, data=json.dumps(payload))

        return r.json()
    
    def update_page(self, page_slug, body=None):
        r = requests.put(
            f"{self.doc_url}/{page_slug}", 
            headers=self.headers, 
            data=json.dumps({"body": body})
        )
        return r.json()
