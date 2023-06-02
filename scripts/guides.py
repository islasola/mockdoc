import os
import time
import boto3
import json
import requests as req
import concurrent.futures
from urllib import parse
from io import BytesIO
from dotenv import load_dotenv
from docwriter import DocWriter

def get_children(blocks):
    start = time.perf_counter()
    b = []
    for group in blocks:
        if group:
            for block in group:
                if block['has_children']:
                    block[block['type']]['children'] = f"https://api.notion.com/v1/blocks/{block['id']}/children"

            with concurrent.futures.ThreadPoolExecutor() as executor:
                children = [ executor.submit(req.get, block[block['type']]['children'], headers=notion_headers) if block['has_children'] else None for block in group ]
                children = [ x.result().json()['results'] if x else x for x in children ]

            children = get_children(children)
            for block, child in zip(group, children):
                if block['has_children']:
                    block[block['type']]['children'] = child

        b.append(group)

    end = time.perf_counter()

    print(f"Time elapsed for retrieving children recursively: {end - start:0.4f} seconds")
    return b

def get_synced_blocks(blocks):
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

                    block['synced_block']['children'] = f"https://api.notion.com/v1/blocks/{sid}/children"
            
            with concurrent.futures.ThreadPoolExecutor() as executor:
                children = [ executor.submit(req.get, block['synced_block']['children'], headers=notion_headers) if block['type'] == 'synced_block' else None for block in group ]
                children = [ x.result().json()['results'] if x else x for x in children ]

            children = get_synced_blocks(children)
            for block, child in zip(group, children):
                if block['type'] == 'synced_block':
                    block['synced_block']['children'] = child

        b.append(group)
    
    end = time.perf_counter()

    print(f"Time elapsed for retrieving synced blocks: {end - start:0.4f} seconds")
    return b

def get_video_meta(blocks):
    b = []
    v = []
    for group in blocks:
        if group:
            for block in group:
                if block['type'] == 'video':
                    v.append(f"https://youtube.com/watch?v={block['video']['external']['url'].split('/')[-1]}")
    
            with concurrent.futures.ThreadPoolExecutor() as executor:
                meta = [ executor.submit(req.get, f"https://www.youtube.com/oembed?url={url}&format=json") for url in v ]
                meta = [ x.result().json() for x in meta ]

            for block, m in zip(group, meta):
                if block['type'] == 'video':
                    block['video']['external']['meta'] = m

        b.append(group)
    
    return b

def upload_images(blocks):
    start = time.perf_counter()
    b = []
    i = []
    l = []

    s3 = boto3.resource('s3')
    bucket = s3.Bucket("assets.zilliz.com")

    for group in blocks:
        if group:
            for block in group:
                if block['type'] == 'image':
                    if 'file' in block['image']:
                        i.append({
                            "id": block['id'],
                            "url": block['image']['file']['url'],
                            "title": block['image']['caption'][0]['plain_text'] if len(block['image']['caption']) > 0 else block['id']
                        })

            with concurrent.futures.ThreadPoolExecutor() as executor:
                images = [ executor.submit(req.get, x['url']) for x in i ]
                images = [ x.result().content for x in images ]


            with concurrent.futures.ThreadPoolExecutor() as executor:
                for itm, image in zip(i, images):
                    executor.submit(bucket.put_object, Key=f"zdoc/{itm['title']}", Body=image, ACL='public-read')

            for block in group:
                for itm, image in zip(i, images):
                    if block['type'] == 'image':
                        block['image']['file']['url'] = f"https://assets.zilliz.com/zdoc/{itm['title']}"
                        block['image']['file']['title'] = itm['title']

            for block in group:
                if block['type'] == 'link_preview':
                    url = block['link_preview']['url']
                    key = parse.urlsplit(url).path.split('/')[2]
                    node = ':'.join(parse.parse_qs(url)['node-id'][0].split('-'))
                    l.append(
                        (
                            key,
                            node,
                            f"https://api.figma.com/v1/images/{key}?ids={node}&scale=2&format=png",
                            f"https://api.figma.com/v1/files/{key}/nodes?ids={node}"
                        )
                    )

            with concurrent.futures.ThreadPoolExecutor() as executor:
                previews = [ executor.submit(req.get, x[2], headers=figma_headers) for x in l ]
                previews = [ executor.submit(req.get, x.result().json()['images'][itm[1]]) for x, itm in zip(previews, l) ]
                previews = [ BytesIO(x.result().content) for x in previews ]
                captions = [ executor.submit(req.get, x[3], headers=figma_headers) for x in l ]
                captions = [ x.result().json()['nodes'][itm[1]]['document']['name'] for x, itm in zip(captions, l) ]

            with concurrent.futures.ThreadPoolExecutor() as executor:
                for itm, preview, caption in zip(l, previews, captions):
                    executor.submit(bucket.put_object, Key=f"zdoc/{itm[0]}/{itm[1]}", Body=preview.getvalue(), ACL='public-read')

            for block in group:
                for itm, preview, caption in zip(l, previews, captions):
                    if block['type'] == 'link_preview':
                        block['link_preview']['url'] = f"https://assets.zilliz.com/zdoc/{itm[0]}/{itm[1]}"
                        block['link_preview']['caption'] = caption

        b.append(group)

    end = time.perf_counter()

    print(f"Time elapsed for uploading images: {end - start:0.4f} seconds")
    return b

def get_mention_page(page_meta):
    id = page_meta['id']

    if page_meta['properties']['Title']['title'][0]['type'] == 'mention':
        id = page_meta['properties']['Title']['title'][0]['mention']['page']['id']

    return id

if __name__ == '__main__':
    load_dotenv()

    README_API_KEY = os.environ.get('README_API_KEY')
    FIGMA_API_KEY = os.environ.get('FIGMA_API_KEY')
    NOTION_API_KEY = os.environ.get('NOTION_API_KEY')
    NOTION_VERSION = os.environ.get('NOTION_VERSION')
    AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
    AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')
    ROOT_DATABASE_ID = os.environ.get('ROOT_DATABASE_ID')    

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

    payload = {
        "filter": {
            "and": [
                {
                    "property": "Title",
                    "rich_text": {
                        "does_not_equal": "FAQs"
                    }
                },
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

    # retrieve categories
    start = time.perf_counter()

    categories = req.post(f"https://api.notion.com/v1/databases/{ROOT_DATABASE_ID}/query", headers=notion_headers, json=payload)
    categories = categories.json()['results']

    remote_categories = req.get("https://dash.readme.com/api/v1/categories", headers=rdme_headers).json()
    remote_category_titles = [ x['title'] for x in remote_categories ]
    category_titles = [ x['properties']['Title']['title'][0]['plain_text'] for x in categories ]

    # upsert categories
    with concurrent.futures.ThreadPoolExecutor() as executor:
        for x in category_titles:
            if x not in remote_category_titles:
                executor.submit(req.put, f"https://dash.readme.com/api/v1/categories", headers=rdme_headers, json=dict(title=x))

    remote_categories = req.get("https://dash.readme.com/api/v1/categories", headers=rdme_headers).json()

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
        books=f"https://api.notion.com/v1/blocks/{x['id']}/children"
    ) for x in categories ]

    with concurrent.futures.ThreadPoolExecutor() as executor:
        books = [ executor.submit(req.get, x['books'], headers=notion_headers) for x in categories ]
    
    categories = [ dict(
        id=x['id'],
        rid=x['rid'],
        title=x['title'], 
        slug=x['slug'],
        books=[z for z in y.result().json()['results'] if z['type']=='child_database']
    ) for x, y in zip(categories, books) ]

    with concurrent.futures.ThreadPoolExecutor() as executor:
        # get remote books
        remote_books = [ executor.submit(req.get, f"https://dash.readme.com/api/v1/categories/{x['slug']}/docs", headers=rdme_headers) for x in categories ]
        remote_books = [ x.result().json() for x in remote_books ]

    for i, c in enumerate(categories):
        c['books'] = [ dict(
            id=x['id'],
            rid=y['_id'],
            title=x['child_database']['title'][3:],
            seq=int(x['child_database']['title'][:2]),
            slug=y['slug'],
            pages=f"https://api.notion.com/v1/databases/{x['id']}/query",
            description=f"https://api.notion.com/v1/databases/{x['id']}"
        ) if x['child_database']['title'][3:] == y['title'] else dict(
            id=x['id'],
            title=x['child_database']['title'][3:],
            seq=int(x['child_database']['title'][:2]),
            pages=f"https://api.notion.com/v1/databases/{x['id']}/query",
            description=f"https://api.notion.com/v1/databases/{x['id']}"
        ) for x, y in zip(c['books'], remote_books[i]) ]

        # add books
        with concurrent.futures.ThreadPoolExecutor() as executor:
            for x in c['books']:
                if 'rid' not in x:
                    executor.submit(req.post, f"https://dash.readme.com/api/v1/categories/{c['slug']}/docs", headers=rdme_headers, json=dict(title=x['title']))

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

        with concurrent.futures.ThreadPoolExecutor() as executor:
            pages = [ executor.submit(req.post, bk['pages'], headers=notion_headers, json=payload) for bk in c['books'] ]
            pages = [ x.result().json()['results'] for x in pages ]
            description = [ executor.submit(req.get, bk['description'], headers=notion_headers) for bk in c['books'] ]
            description = [ x.result().json() for x in description ]

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

            with concurrent.futures.ThreadPoolExecutor() as executor:
                for pg in bk['pages']:
                    if pg['title'] not in remote_page_titles:
                        executor.submit(req.post, f"https://dash.readme.com/api/v1/docs", headers=rdme_headers, json=dict(title=pg['title'], order=pg['seq'], category=c['rid'], parentDoc=bk['rid']))

            remote_pages = req.get(f"https://dash.readme.com/api/v1/categories/{c['slug']}/docs", headers=rdme_headers).json()
            remote_pages = list(filter(lambda x: x['title'] == bk['title'], remote_pages))[0]['children']

            for pg in bk['pages']:
                for r in remote_pages:
                    if pg['title'] == r['title']:
                        pg['rid'] = r['_id']
                        pg['slug'] = r['slug']

            # retrieve blocks
            for pg in bk['pages']:
                pg['blocks'] = f"https://api.notion.com/v1/blocks/{pg['id']}/children"

            end = time.perf_counter()

            print(f"Time elapsed for retrieving pages in book {bk['title']}: {end - start:0.4f} seconds")

            # retrieve blocks
            start = time.perf_counter()

            with concurrent.futures.ThreadPoolExecutor() as executor:
                blocks = [ executor.submit(req.get, pg['blocks'], headers=notion_headers) for pg in bk['pages'] ]
                blocks = [ x.result().json()['results'] for x in blocks ]

            blocks = get_children(blocks)
            blocks = get_synced_blocks(blocks)
            blocks = upload_images(blocks)
            blocks = get_video_meta(blocks)

            for pg in bk['pages']:
                pg['blocks'] = [ y for x in blocks for y in x if y['parent']['page_id'] == pg['id'] ] 

            end = time.perf_counter()

            print(f"Time elapsed for retrieving blocks: {end - start:0.4f} seconds")

        with open(f"books/{c['title']}.json", 'w') as f:
            json.dump(c, f, indent=4)
