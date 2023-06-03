import os
import re
import time
import boto3
import json
import asyncio
import requests as req
import concurrent.futures
from urllib import parse
from io import BytesIO
from dotenv import load_dotenv
from asyncclient import AsyncClient
from docwriter import DocWriter

async def get_children(blocks):
    start = time.perf_counter()
    b = []
    for group in blocks:
        if group:
            for block in group:
                if block['has_children']:
                    block[block['type']]['children'] = f"/v1/blocks/{block['id']}/children"

            children = [ await notion_client.get(block[block['type']]['children']) if block['has_children'] else None for block in group ]
            children = [ json.loads(x)['results'] if x else x for x in children ]

            children = await upload_images(children)
            children = await get_video_meta(children)
            children = await get_synced_blocks(children)
            children = await get_children(children)

            for block, child in zip(group, children):
                if block['has_children']:
                    block[block['type']]['children'] = child

        b.append(group)

    end = time.perf_counter()

    print(f"Time elapsed for retrieving children recursively: {end - start:0.4f} seconds")
    return b

async def get_synced_blocks(blocks):
    start = time.perf_counter()
    b = []
    for group in blocks:
        if group and 'results' in group:
            for block in group:
                if block['type'] == 'synced_block':
                    if block['synced_block']['synced_from']:
                        sid = block['synced_block']['synced_from']
                    else:
                        sid = block['id']

                    block['synced_block']['children'] = f"/v1/blocks/{sid}/children"

            children = [ await notion_client.get(block['synced_block']['children']) if block['type'] == 'synced_block' else None for block in group ]
            children = [ json.loads(x)['results'] if x else x for x in children ]

            for block, child in zip(group, children):
                if block['type'] == 'synced_block':
                    block['synced_block']['children'] = child

        b.append(group)
    
    end = time.perf_counter()

    print(f"Time elapsed for retrieving synced blocks: {end - start:0.4f} seconds")
    return b

async def get_video_meta(blocks):
    b = []
    for group in blocks:
        if group:
            for block in group:
                if block['type'] == 'video' and 'external' in block['video']:
                    block['video']['external']['meta'] = f"https://youtube.com/watch?v={block['video']['external']['url'].split('/')[-1]}"

            youtube_client = AsyncClient()

            children = [ await youtube_client.get("https://www.youtube.com/oembed?url=" + block['video']['external']['meta']  + "&format=json") if block['type'] == 'video' else None for block in group ]
            children = [ json.loads(x) if x else x for x in children ]

            for block, child in zip(group, children):
                if block['type'] == 'video':
                    block['video']['external']['meta'] = child

        b.append(group)
    
    return b

async def upload_images(blocks):
    start = time.perf_counter()
    b = []
    s3 = boto3.resource('s3')
    bucket = s3.Bucket("assets.zilliz.com")

    for group in blocks:
        if group:
            for block in group:
                if block['type'] == 'image':
                    if 'file' in block['image']:
                        block['image']['file'] = {
                            "id": block['id'],
                            "url": block['image']['file']['url'],
                            "title": f"{block['image']['caption'][0]['plain_text'] if len(block['image']['caption']) > 0 else block['id']}.png"
                        }

                if block['type'] == 'link_preview':
                    if 'url' in block['link_preview']:
                        block['link_preview']['key'] = parse.urlsplit(block['link_preview']['url']).path.split('/')[2]
                        block['link_preview']['node'] = ":".join(parse.parse_qs(block['link_preview']['url'])['node-id'][0].split("-"))

            images = [ dict(block, title=block['image']['file']['title'], content=req.get(block['image']['file']['url']).content) for block in group if block['type'] == 'image' and 'file' in block['image'] ]

            link_previews = [ dict(
                key=block['link_preview']['key'],
                node=block['link_preview']['node'],
                content=await figma_client.get(f"/v1/images/{block['link_preview']['key']}?ids={block['link_preview']['node']}&format=png&scale=1"),
                title=await figma_client.get(f"/v1/files/{block['link_preview']['key']}/nodes?ids={block['link_preview']['node']}")) 
            for block in group if block['type'] == 'link_preview' ]

            link_previews = [ dict(
                key=x['key'],
                node=x['node'],
                content=BytesIO(req.get(json.loads(x['content'])['images'][x['node']], headers=figma_headers).content),
                title=json.loads(x['title'])['nodes'][x['node']]['document']['name'] + '.png')
            for x in link_previews]

            with concurrent.futures.ThreadPoolExecutor() as executor:
                [ executor.submit(bucket.put_object, Key=f"zdoc/{image['title']}", Body=image['content'], ACL='public-read') for image in images ]
                [ executor.submit(bucket.put_object, Key=f"zdoc/{link_preview['title']}", Body=link_preview['content'], ACL='public-read') for link_preview in link_previews ]

            for block in group:
                if block['type'] == 'image' and 'file' in block['image']:
                    block['image']['file']['url'] = f"https://assets.zilliz.com/zdoc/{block['image']['file']['title']}"

                if block['type'] == 'link_preview':
                    block['link_preview']['title'] = [ x for x in link_previews if x['key'] == block['link_preview']['key'] and x['node'] == block['link_preview']['node'] ][0]['title']
                    block['link_preview']['url'] = f"https://assets.zilliz.com/zdoc/{block['link_preview']['title']}"  

        b.append(group)

    end = time.perf_counter()

    print(f"Time elapsed for uploading images: {end - start:0.4f} seconds")
    return b

async def faqs(category):
    query = {
        "filter": {
            "property": "Added to FAQ?",
            "checkbox": {
                "equals": True
            }
        }
    }

    print(category['id'])

    faqs = await notion_client.post(f"/v1/databases/{FAQS_DATABASE_ID}/query", json=query)
    faqs = json.loads(faqs)

    faqs_categories = list(set([ x['properties']['Category']['multi_select'][0]['name'] for x in faqs['results'] ]))
    faqs_questions = [ dict(category=x['properties']['Category']['multi_select'][0]['name'], question=x['properties']['Question']['title'][0]['plain_text']) for x in faqs['results'] ]
    faqs_answers = [ json.loads(await notion_client.get(f"/v1/blocks/{x['id']}/children"))['results'] for x in faqs['results'] ]
    faqs_answers = await upload_images(faqs_answers)
    faqs_answers = await get_video_meta(faqs_answers)
    faqs_answers = await get_synced_blocks(faqs_answers)
    faqs_answers = await get_children(faqs_answers)
    
    faqs_questions = [ dict(category=question['category'], question=question['question'], answer=answer) for question, answer in zip(faqs_questions, faqs_answers) ]

    for i, faqs_category in enumerate(faqs_categories):
        questions = []
        for faqs_question in faqs_questions:
            if faqs_question['category'] == faqs_category:
                questions.append(faqs_question)

        faqs_categories[i] = dict(category=faqs_category, questions=questions)

    remotes = json.loads(await rdme_client.get(f"/api/v1/categories/{category['slug']}/docs"))

    faqs_categories_to_add = []
    
    for faqs_category in faqs_categories:
        for remote in remotes:
            if faqs_category['category'] == remote['title'].split(": ")[1]:
                faqs_category['rid'] = remote['_id']
                faqs_category['slug'] = remote['slug']
                break
            else:
                faqs_categories_to_add.append(faqs_category['category'])

    faqs_categories_to_add = list(set(faqs_categories_to_add))
    print(faqs_categories_to_add)

    if faqs_categories_to_add:
        [ await rdme_client.post('/api/v1/docs', json={"title": f"FAQs: {x}", "category": category['rid']}) for x in faqs_categories_to_add ]

    remote = json.loads(await rdme_client.get(f"/api/v1/categories/{category['slug']}/docs"))

    for faqs_category in faqs_categories:
        if 'rid' not in faqs_category:
            faqs_category['rid'] = [ x['_id'] for x in remote if x['title'].split(": ")[1] == faqs_category['category'] ][0]

    with open('faqs.json', 'w') as f:
        json.dump(faqs_categories, f, indent=4)

    ## Generate doc pages
    DocWriter(faqs_categories, type="faqs").write_faqs(category['id'])

def get_mention_page(page_meta):
    id = page_meta['id']

    if page_meta['properties']['Title']['title'][0]['type'] == 'mention':
        id = page_meta['properties']['Title']['title'][0]['mention']['page']['id']

    return id

def replace_links(pages, flat_pages, work_type='blocks'):
    for page in pages:
            for block in page[work_type]:
                type = block['type']
                if 'rich_text' in block[type]:
                    for segment in block[block['type']]['rich_text']:
                        type = segment['type']
                        if 'link' in segment[type]:
                            if segment[type]['link']:
                                m = re.search(r'([a-z0-9]{32})$', segment[type]['link']['url'])
                                if m:
                                    slug = [p['slug'] for p in flat_pages if ''.join(p['id'].split('-')) == m.group(1)]
                                    if slug:
                                        segment[type]['link']['url'] = f"doc:{slug[0]}"
                                        print(f"Page found: {m.group(1)}. Changed to \"doc:{slug[0]}\"")
                                    else:
                                        print(f"Page not found: {m.group(1)}")

            if block['has_children']:
                if 'children' in block:
                    replace_links(block['children'], flat_pages, work_type='children')
                else:
                    print(f"Block has children but no children: {block['id']}") 

async def main():
    # retrieve categories
    start = time.perf_counter()

    categories = req.post(f"https://api.notion.com/v1/databases/{ROOT_DATABASE_ID}/query", headers=notion_headers, json=payload)
    categories = categories.json()['results']
    category_titles = [ x['properties']['Title']['title'][0]['plain_text'] for x in categories ]

    remote_categories = req.get("https://dash.readme.com/api/v1/categories?perPage=20", headers=rdme_headers).json()
    remote_category_titles = [ x['title'] for x in remote_categories ]

    [ await rdme_client.post('/api/v1/categories', json={"title": x}) if x not in remote_category_titles else x for x in category_titles ]

    remote_categories = req.get("https://dash.readme.com/api/v1/categories?perPage=20", headers=rdme_headers).json()

    for c in categories:
        for r in remote_categories:
            if c['properties']['Title']['title'][0]['plain_text'] == r['title']:
                c['rid'] = r['_id']
                c['slug'] = r['slug']
                c['title'] = r['title'] 

    end = time.perf_counter()

    print(f"Time elapsed for retrieving categories: {end - start:0.4f} seconds")     

    # retrieve books
    start = time.perf_counter()

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

        [ await rdme_client.post('/api/v1/docs', json=x) for x in docs_to_create ]

        # get remote books
        remote_books[i] = req.get(f"https://dash.readme.com/api/v1/categories/{c['slug']}/docs", headers=rdme_headers).json()

        for x in c['books']:
            for y in remote_books[i]:
                if x['title'] == y['title']:
                    x['rid'] = y['_id']
                    x['slug'] = y['slug']

        end = time.perf_counter()

        print(f"Time elapsed for retrieving books in category {c['title']}: {end - start:0.4f} seconds")

        # retrieve pages
        start = time.perf_counter()

        pages = [ await notion_client.post(bk['pages'], json=payload) for bk in c['books'] ]
        pages = [ json.loads(x)['results'] for x in pages]
        description = [ await notion_client.get(bk['description']) for bk in c['books']]
        description = [ json.loads(x) for x in description ]

        for bk in c['books']:
            bk['description'] = [ x for x in description if x['id'] == bk['id'] ][0]['description']

            bk['pages'] = [ dict(
                id=get_mention_page(y),
                title=y['properties']['Title']['title'][0]['plain_text'],
                url=y['url'],
                created_time=y['created_time'],
                last_edited_time=y['last_edited_time'],
                seq=y['properties']['Seq. ID']['number'],
                progress=y['properties']['Progress']['select']['name'],
                version=y['properties']['Version']['rich_text'][0]['plain_text'],
                tags=[ t['name'] for t in y['properties']['Tags']['multi_select'] ],
                blocks=[],
            ) for x in pages for y in x if y['parent']['database_id'] == bk['id'] ]


            remote_pages = req.get(f"https://dash.readme.com/api/v1/categories/{c['slug']}/docs", headers=rdme_headers).json()
            remote_pages = list(filter(lambda x: x['title'] == bk['title'], remote_pages))[0]['children']
            remote_page_titles = [ x['title'] for x in remote_pages ]

            [ await rdme_client.post('/api/v1/docs', json=dict(title=x['title'], order=x['seq'], category=c['rid'], parentDoc=bk['rid'])) for x in bk['pages'] if x['title'] not in remote_page_titles ]

            remote_pages = req.get(f"https://dash.readme.com/api/v1/categories/{c['slug']}/docs", headers=rdme_headers).json()
            remote_pages = list(filter(lambda x: x['title'] == bk['title'], remote_pages))[0]['children']

            for pg in bk['pages']:
                for r in remote_pages:
                    if pg['title'] == r['title']:
                        pg['rid'] = r['_id']
                        pg['slug'] = r['slug']

            # retrieve blocks
            for pg in bk['pages']:
                pg['blocks'] = f"/v1/blocks/{pg['id']}/children"

            end = time.perf_counter()

            print(f"Time elapsed for retrieving pages in book {bk['title']}: {end - start:0.4f} seconds")

            # retrieve blocks
            start = time.perf_counter()

            blocks = [ await notion_client.get(pg['blocks']) for pg in bk['pages'] ]
            blocks = [ json.loads(x)['results'] for x in blocks ]

            blocks = await upload_images(blocks)
            blocks = await get_video_meta(blocks)
            blocks = await get_synced_blocks(blocks)
            blocks = await get_children(blocks)

            for pg in bk['pages']:
                pg['blocks'] = [ y for x in blocks for y in x if y['parent']['page_id'] == pg['id'] ] 

                end = time.perf_counter()

                print(f"Time elapsed for retrieving blocks on page {pg['title']}: {end - start:0.4f} seconds")

    flat_pages = [ dict(
        id=p['id'],
        title=p['title'],
        rid=p['rid'],
        slug=p['slug'],
        blocks=p['blocks'],
    ) for c in categories if c['title'] != 'FAQs' for b in c['books'] for p in b['pages']]

    for c in categories:
        if c['title'] == 'FAQs':
            break;

        for b in c['books']:
            b['pages'] = replace_links(b['pages'], flat_pages)

    guides = [ c for c in categories if c['title'] != 'FAQs' ]

    DocWriter(guides).write_docs()

    faqs = [ c for c in categories if c['title'] == 'FAQs' ][0]

    await faqs(c)

if __name__ == '__main__':
    load_dotenv()

    README_API_KEY = os.environ.get('README_API_KEY')
    FIGMA_API_KEY = os.environ.get('FIGMA_API_KEY')
    NOTION_API_KEY = os.environ.get('NOTION_API_KEY')
    NOTION_VERSION = os.environ.get('NOTION_VERSION')
    AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
    AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')
    ROOT_DATABASE_ID = os.environ.get('ROOT_DATABASE_ID')   
    FAQS_DATABASE_ID = os.environ.get('FAQS_DATABASE_ID') 

    notion_headers = {
        "Authorization": f"Bearer {NOTION_API_KEY}",
        "NOTION-VERSION": NOTION_VERSION
    }

    figma_headers = {
        'Accept': 'application/json',
        'X-Figma-Token': FIGMA_API_KEY
    } 

    rdme_headers = {
       "accept": "application/json",
       "content-type": "application/json",
       "authorization": f"Basic {README_API_KEY}"
    }

    notion_client = AsyncClient("https://api.notion.com", notion_headers)
    figma_client = AsyncClient("https://api.figma.com", figma_headers)
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

    asyncio.run(main())
