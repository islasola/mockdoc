import asyncio
import requests
import boto3
import json
import re
import os

import time

from urllib import parse
from io import BytesIO
from asyncclient import AsyncClient
from docwriter import DocWriter

def canonical_id(p):
    return p["id"] if 'Reuse' not in [ t['name'] for t in p['properties']['Tags']['multi_select'] ] else p['properties']['Title']['title'][0]['mention']['page']['id']         
    
def search_zdoc_by_url(zdoc, search_term):  
    for c in zdoc:
        for b in c['books']:
            for p in b['pages']:
                if search_term in p['url']:
                    return p['slug']
                    
def search_zdoc_by_id(zdoc, page_id):
    print(page_id)
    for c in zdoc:
        for b in c['books']:
            for p in b['pages']:
                if p['id'] == page_id:
                    return p['title'], p['slug']
                
async def thru_blocks(client, blocks):
    blocks_has_children = [ x for x in blocks if x['has_children'] ]

    children = await asyncio.gather(*[client.get(f'/v1/blocks/{x["id"]}/children') for x in blocks_has_children])
    children = [ json.loads(x)['results'] for x in children ]

    for i, x in enumerate(blocks_has_children):
        x['children'] = children[i]

    for b in blocks:
        for x in blocks_has_children:
            if x['id'] == b['id']:
                b['children'] = await thru_blocks(client, x['children'])
                break

    return blocks

async def get_child_blocks(root_block, has_children, block_type):
    if block_type == page:
        blocks = await asyncio.gather(*[client.get(f"/v1/blocks/{root_block['id']}/children")])
        root_block['blocks'] = json.load(blocks)['results']
        root_block['blocks'] = [ await get_child_blocks(x, x['has_children'], x['type']) for x in root_block['blocks'] ]   
    else:
        if has_children:
            children = await asyncio.gather(*[client.get(f"/v1/blocks/{root_block['id']}/children")])
            root_block[block_type]['children'] = json.load(blocks)['results']
            root_block[block_type]['children'] = [ await get_child_blocks(x, x['has_children'], x['type']) for x in root_block['blocks'] ]  
    
    return root_block
       
async def get_child_blocks(root_block, has_children, block_type):
    if root_block['has_children']:
        children = await asyncio.gather(*[client.get(f"/v1/blocks/{root_block['id']}/children")])
        root_block['children'] = json.loads(children)['results']
        root_block['children'] = [ await get_child_blocks(x) for x in root_block['children'] ]
        
    return root_block
    
async def main():
    notion_headers = {
        "Authorization": f"Bearer {NOTION_API_KEY}",
        "NOTION-VERSION": NOTION_VERSION
    }
    start = time.time()
    client = AsyncClient("https://api.notion.com", headers=notion_headers)
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

    # 01 Read the root database
    start = time.time()
    response = requests.post(f"https://api.notion.com/v1/databases/{ROOT_DATABASE_ID}/query", headers=notion_headers, json=payload)
    results = response.json()['results']
    end = time.time()
    print(f"Took {end-start} seconds to pull {len(results)} pages")

    # 02 Read child databases
    start = time.time()
    page_metas = await asyncio.gather(*[client.get(f'/v1/pages/{x["id"]}') for x in results])
    page_titles = [json.loads(x)['properties']['Title']['title'][0]['plain_text'] for x in page_metas ]
    pages = await asyncio.gather(*[client.get(f'/v1/blocks/{x["id"]}/children') for x in results])
    blocks = [json.loads(x)['results'] for x in pages]
    child_databases = [list(filter(lambda x: x['type'] == 'child_database', x)) for x in blocks ]
    child_database_descriptions = [[await asyncio.gather(*[client.get(f"/v1/databases/{d['id']}")]) for d in x] for x in child_databases]
    end = time.time()
    print(f"Took {end-start} seconds to find some child databases")

    # 03 Read child pages
    start= time.time()
    child_pages = [[await asyncio.gather(*[client.post(f"/v1/databases/{d['id']}/query", json=payload)]) for d in x] for x in child_databases]
    end = time.time()
    print(f"Took {end-start} seconds to pull several child pages")

    # 04 Read abundant blocks
    start = time.time()
    child_databases = [[{
        "id": d["id"],
        "title": d["child_database"]["title"],
        "description": json.loads(child_database_descriptions[j][i][0])['description'],
        "pages": [{
            "id": canonical_id(p)
        } for p in json.loads(child_pages[j][i][0])['results']]
    } for i, d in enumerate(x)] for j, x in enumerate(child_databases)]

    page_blocks = [[[ await get_child_blocks(b，True, 'page') for b in d['pages']] for d in x] for x in child_databases]

    end = time.time()
    print(f"Took {end-start} seconds to pull abundant blocks")

    # 05 Contatenate everything to form zdoc
    child_databases = [[{
        "id": d["id"],
        "title": d["title"],
        "description": d["description"],
        "pages": [{
            "id": canonical_id(p),
            "title": p["properties"]["Title"]["title"][0]["plain_text"],
            "url": p["url"],
            "created_time": p["created_time"],
            "last_edited_time": p["last_edited_time"],
            "seq": p['properties']['Seq. ID']['number'],
            "progress": p['properties']['Progress']['select']['name'],
            "version": p['properties']['Version']['rich_text'][0]['plain_text'],
            "tags": [ t['name'] for t in p['properties']['Tags']['multi_select'] ],
            "blocks": json.loads(page_blocks[j][i][k][0])['results'], 
        } for k, p in enumerate(json.loads(child_pages[j][i][0])['results'])]
    } for i, d in enumerate(x)] for j, x in enumerate(child_databases)]
    
    zdoc = [ {
        "title": x,
        "books": child_databases[i]
    } for i, x in enumerate(page_titles)]

    # 06 Added empty pages to readme
    rdme_headers = {
            "accept": "application/json",
            "content-type": "application/json",
            "authorization": f"Basic {README_API_KEY}"
        }
    rdme_client = AsyncClient("https://dash.readme.com", headers=rdme_headers) 

    # 06-1 Upsert categories
    start = time.time()
    categories = [ x['title'] for x in json.loads(await rdme_client.get("/api/v1/categories"))]
    [ await asyncio.gather(*[rdme_client.post("/api/v1/categories", json={"title": x['title']})]) for x in zdoc if x['title'] not in categories ]
    categories = [ x for x in json.loads(await rdme_client.get("/api/v1/categories"))]
    for z in zdoc:
        t = [x for x in categories if x['title'] == z['title']]
        if t:
            z['slug'] = t[0]['slug']
            z['rid'] = t[0]['_id']

    print([x['slug'] for x in zdoc])
    end = time.time()

    print(f"Took {end-start} seconds to upsert categories")

    # 06-2 Upsert books
    start = time.time()
    # retrieve direct pages of all categories and compare the titles with those in zdoc to find the ones that need to be created
    for z in zdoc:
        pages = json.loads(await rdme_client.get(f"/api/v1/categories/{z['slug']}/docs"))
        titles = [x['title'] for x in pages]
        for b in z['books']:
            title = b['title'][3:]
            order = int(b['title'][:2])
            if title not in titles:
                await rdme_client.post(f"/api/v1/docs", json={"title": title, "order": order, "category": z['rid']})

        pages = json.loads(await rdme_client.get(f"/api/v1/categories/{z['slug']}/docs"))
        for b in z['books']:
            title = b['title'][3:]
            t = [x for x in pages if x['title'] == title]
            if t:
                b['slug'] = t[0]['slug']
                b['rid'] = t[0]['_id']

    print([[y['slug'] for y in x['books']] for x in zdoc])        
    end = time.time()

    print(f"Took {end-start} seconds to upsert books")

    # 06-3 Upsert pages
    start = time.time()
    for z in zdoc:
        pages = json.loads(await rdme_client.get(f"/api/v1/categories/{z['slug']}/docs"))
        for b in z['books']:
            book_title = b['title'][3:]
            child_pages = [ x for x in pages if x['title'] == book_title ][0]['children']
            titles = [x['title'] for x in child_pages]
            for p in b['pages']:
                if p['title'] not in titles:
                    await rdme_client.post(f"/api/v1/docs", json={"title": p['title'], "order": p['seq'], "category": z['rid'], "parentDoc": b['rid']})

        pages = json.loads(await rdme_client.get(f"/api/v1/categories/{z['slug']}/docs"))
        for b in z['books']:
            book_title = b['title'][3:]
            child_pages = [ x for x in pages if x['title'] == book_title ][0]['children']
            for p in b['pages']:
                t = [x for x in child_pages if x['title'] == p['title']]
                if t:
                    p['slug'] = t[0]['slug']
                    p['rid'] = t[0]['_id']
    
    print([[[z['slug'] for z in y['pages']] for y in x['books']] for x in zdoc])
    end = time.time()

    print(f"Took {end-start} seconds to upsert pages")

    # 06-4 Replace internal links
    text = json.dumps(zdoc, indent=4)
    internal_links = list(set(re.findall(r'/[a-z0-9]{32}', text)))
    for page_link in internal_links:
        slug = search_zdoc_by_url(zdoc, page_link[1:])

        if not slug:
            slug = 'doc: 404'
        else:
            slug = 'doc:' + slug
            
        text = re.sub(page_link, slug, text)

    zdoc = json.loads(text)

    # 06-5 Replace link previews
    link_previews = []
    for c in zdoc:
        for bk in c['books']:
            for p in bk['pages']:
                for bl in p['blocks']:
                    if bl['type'] == 'link_preview':
                        link_previews.append(bl['link_preview']['url'])
                        
    link_previews = [ {
        "raw": x,
        "key": parse.urlsplit(x).path.split('/')[2],
        "node": ":".join(parse.parse_qs(x)['node-id'][0].split("-")),
        
    } for x in list(set(link_previews)) ]

    figma_headers = {
        'Accept': 'application/json',
        'X-Figma-Token': FIGMA_API_KEY
    } 

    figma_client = AsyncClient("https://api.figma.com", headers=figma_headers)

    # 06-5-1 Retrieve image content
    start = time.time()
    image_contents = await asyncio.gather(*[figma_client.get(f"/v1/images/{x['key']}?ids={x['node']}&scale=2&format=png") for x in link_previews])
    end = time.time()
    print(f"Took {end-start} seconds to retrieve image content")

    # 06-5-2 Retrieve image title
    start = time.time()
    image_titles = await asyncio.gather(*[figma_client.get(f"/v1/files/{x['key']}/nodes?ids={x['node']}") for x in link_previews])
    end = time.time()
    print(f"Took {end-start} seconds to retrieve image title")

    s3 = boto3.resource('s3')
    bucket = "assets.zilliz.com"

    start = time.time()
    for i, x in enumerate(link_previews):
        x['title'] = json.loads(image_titles[i])['nodes'][x['node']]['document']['name']
        x['content'] = json.loads(image_contents[i])['images'][x['node']]
        
        image = BytesIO(requests.get(x['content'], headers=figma_headers).content)

        try:
            s3.Bucket(bucket).put_object(Key=f'zdoc/{x["title"]}.png', Body=image, ACL='public-read')
        except Exception as e:
            raise Exception(f'Failed to upload to s3: {e}')
        
        x['content'] = f'https://assets.zilliz.com/zdoc/{x["title"]}.png'
    end = time.time()

    print(f"Took {end-start} seconds to upload to s3")

    print(link_previews)

    for c in zdoc:
        for bk in c['books']:
            for p in bk['pages']:
                for bl in p['blocks']:
                    if bl['type'] == 'link_preview':
                        for x in link_previews:
                            if x['raw'] == bl['link_preview']['url']:
                                bl['link_preview']['url'] = x['content']
                                bl['link_preview']['title'] = x['title']
                                break

    # zdoc = json.loads(text)

    ## 06-6 Retrieve synced blocks
    start = time.time()
    synced_blocks = []
    for c in zdoc:
        for bk in c['books']:
            for p in bk['pages']:
                for bl in p['blocks']:
                    if bl['type'] == 'synced_block':
                        if bl['synced_block']['synced_from']:
                            sid = bl['synced_block']['synced_from']['block_id']
                        else:
                            sid = bl['id']

                        synced_blocks.append({
                            "id": sid,
                            "uri": f'/v1/blocks/{sid}/children'
                        })

    children = await asyncio.gather(*[client.get(x['uri']) for x in synced_blocks])
    
    for i, x in enumerate(synced_blocks):
        x['children'] = json.loads(children[i])['results']

    for c in zdoc:
        for bk in c['books']:
            for p in bk['pages']:
                for bl in p['blocks']:
                    if bl['type'] == 'synced_block':
                        for x in synced_blocks:
                            if bl['synced_block']['synced_from']:
                                if bl['synced_block']['synced_from']['block_id'] == x['id']:
                                    bl['synced_block']['children'] = x['children']
                                    break
                            else:
                                if bl['id'] == x['id']:
                                    bl['synced_block']['children'] = x['children']
                                    break

    end = time.time()
    print(f"Took {end-start} seconds to retrieve synced blocks")

    # 06-7 Retrieve table children
    start = time.time()
    table_blocks = []
    for c in zdoc:
        for bk in c['books']:
            for p in bk['pages']:
                for bl in p['blocks']:
                    if bl['type'] == 'table':
                        table_blocks.append({
                            "id": bl['id'],
                            "uri": f'/v1/blocks/{bl["id"]}/children'
                        })

    children = await asyncio.gather(*[client.get(x['uri']) for x in table_blocks])

    for i, x in enumerate(table_blocks):
        x['children'] = json.loads(children[i])['results']

    for c in zdoc:
        for bk in c['books']:
            for p in bk['pages']:
                for bl in p['blocks']:
                    if bl['type'] == 'table':
                        for x in table_blocks:
                            if x['id'] == bl['id']:
                                bl['table']['children'] = x['children']
                                break
    end = time.time()
    print(f"Took {end-start} seconds to retrieve table children")

    # 07 Retrieve links to pages
    text = json.dumps(zdoc, indent=4)

    start = time.time()
    link_to_pages = []
    for c in zdoc:
        for bk in c['books']:
            for p in bk['pages']:
                for bl in p['blocks']:
                    if bl['type'] == 'link_to_page':
                        lid = bl['link_to_page']['page_id']
                        link_to_pages.append(lid)
                            
    
    link_to_pages = list(set(link_to_pages))
    link_to_pages = [ {
        "id": x,
        "title_slug": search_zdoc_by_id(zdoc, x),
    } for x in link_to_pages ]

    for c in zdoc:
        for bk in c['books']:
            for p in bk['pages']:
                for bl in p['blocks']:
                    if bl['type'] == 'link_to_page':
                        for x in link_to_pages:
                            if x['id'] == bl['link_to_page']['page_id']:
                                if x['title_slug']:
                                    bl['link_to_page']['title'] = x['title_slug'][0]
                                    bl['link_to_page']['slug'] = x['title_slug'][1]
                                else:
                                    bl['link_to_page']['title'] = '404'
                                    bl['link_to_page']['slug'] = '404'
                                break

    end = time.time()
    print(f"Took {end-start} seconds to retrieve links to pages")

    # 08 Retrieve images
    start = time.time()
    image_blocks = []
    for c in zdoc:
        for bk in c['books']:
            for p in bk['pages']:
                for bl in p['blocks']:
                    if bl['type'] == 'image':
                        if 'file' in bl['image']:
                            image_blocks.append({
                                "id": bl['id'],
                                "url": bl['image']['file']['url'],
                                "title": bl['image']['caption'] if len(bl['image']['caption']) > 0 else bl['id']
                            })

    s3 = boto3.resource('s3')
    bucket = "assets.zilliz.com"

    start = time.time()
    for i, x in enumerate(image_blocks):
        image = requests.get(x['url']).content

        try:
            s3.Bucket(bucket).put_object(Key=f'zdoc/{x["title"]}.png', Body=image, ACL='public-read')
        except Exception as e:
            raise Exception(f'Failed to upload to s3: {e}')
        
        x['content'] = f'https://assets.zilliz.com/zdoc/{x["title"]}.png'

    
    for c in zdoc:
        for bk in c['books']:
            for p in bk['pages']:
                for bl in p['blocks']:
                    if bl['type'] == 'image':
                        for x in image_blocks:
                            if x['id'] == bl['id']:
                                bl['image']['file']['url'] = x['content']
                                bl['image']['file']['title'] = x['title']
                                break
    end = time.time()

    print(f"Took {end-start} seconds to upload images to s3")

    # 09 Retrieve video embeds
    start = time.time()
    video_blocks = []
    for c in zdoc:
        for bk in c['books']:
            for p in bk['pages']:
                for bl in p['blocks']:
                    if bl['type'] == 'video':
                        if bl['video']['type'] == 'external':
                            video_blocks.append({
                                "id": bl['id'],
                                "uri": f"https://youtube.com/watch?v={bl['video']['external']['url'].split('/')[-1]}"
                            })
    youtube_client = AsyncClient()
    video_metas = await asyncio.gather(*[youtube_client.get("https://www.youtube.com/oembed?url=" + x['uri']  + "&format=json") for x in video_blocks])

    for c in zdoc:
        for bk in c['books']:
            for p in bk['pages']:
                for bl in p['blocks']:
                    if bl['type'] == 'video':
                        for i, x in enumerate(video_blocks):
                            if x['id'] == bl['id']:
                                bl['video']['external']['meta'] = json.loads(video_metas[i])
                                break

    with open("zdoc.json", "w") as f:
        json.dump(zdoc, f, indent=4)

    with open("zdoc.json", "r") as f:
        zdoc = json.loads(f.read())

    # 09 Retrieve list items
    start = time.time()
    list_items = []
    for c in zdoc:
        for bk in c['books']:
            for p in bk['pages']:
                for bl in p['blocks']:
                    if bl['has_children']:
                        if 'bulleted_list_item' in bl or 'numbered_list_item' in bl:
                            list_items.append({
                                "id": bl['id']
                            })

    children = await asyncio.gather(*[client.get(f'/v1/blocks/{x["id"]}/children') for x in list_items])

    for i, x in enumerate(list_items):
        x['children'] = await thru_blocks(client, json.loads(children[i])['results'])

    for c in zdoc:
        for bk in c['books']:
            for p in bk['pages']:
                for bl in p['blocks']:
                    for x in list_items:
                        if x['id'] == bl['id']:
                            bl['children'] = x['children']
                            break

    end = time.time()
    print(f"Took {end-start} seconds to retrieve list items")
                       
    # 10 Generate Docs
    start = time.time()
    DocWriter(zdoc).write_docs()
    end = time.time()

    print(f"Took {end-start} seconds to generate docs")

if __name__ == "__main__":

    README_API_KEY = os.environ.get('README_API_KEY')
    FIGMA_API_KEY = os.environ.get('FIGMA_API_KEY')
    NOTION_API_KEY = os.environ.get('NOTION_API_KEY')
    NOTION_VERSION = os.environ.get('NOTION_VERSION')
    AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
    AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')
    ROOT_DATABASE_ID = os.environ.get('ROOT_DATABASE_ID')

    asyncio.run(main())
