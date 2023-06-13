import os
from io import BytesIO
import json
import boto3
import requests as req
import concurrent.futures
from urllib import parse
from dotenv import load_dotenv

def find_media(block):
    images = []
    link_previews = []
    videos = []
    if block['type'] == 'image':
        images.append(block)

    if block['type'] == 'link_preview':
        link_previews.append(block)

    if block['type'] == 'video':
        videos.append(block)

    if block['has_children']:
        for child in block[block['type']]['children']:
            media = find_media(child)
            images += media[0]
            link_previews += media[1]
            videos += media[2]

    return images, link_previews, videos

def replace_link_preview_url(block, link_preview_blocks, link_preview_titles):
    print(block['type'])
    if block['type'] == 'link_preview':
        for i, link_preview_block in enumerate(link_preview_blocks):
            if link_preview_block['link_preview']['node'] == block['link_preview']['node']:
                block['link_preview']['url'] = link_preview_block['link_preview']['url']
                block['link_preview']['title'] = link_preview_titles[i]

    if block['has_children']:
        for child in block[block['type']]['children']:
            child = replace_link_preview_url(child, link_preview_blocks, link_preview_titles)

    return block  

def replace_image_url(block):
    if block['type'] == 'image':
        if block['image']['type'] == 'file':
            block['image']['file']['url'] = f"https://assets.zilliz.com/zdoc/{block['id']}.png"
            block['image']['file']['title'] = f"{block['image']['caption'][0]['plain_text'] if len(block['image']['caption']) > 0 else block['id']}.png"

    if block['has_children']:
        for child in block[block['type']]['children']:
            child = replace_image_url(child)

    return block  

def replace_video_meta(block, video_blocks):
    for video_block in video_blocks:
        if video_block['id'] == block['id']:
            block['video']['external']['meta'] = video_block['video']['external']['meta']

    if block['has_children']:
        for child in block[block['type']]['children']:
            child = replace_video_meta(child, video_blocks)

    return block


if __name__ == '__main__':

    load_dotenv()

    FIGMA_API_KEY = os.environ.get('FIGMA_API_KEY')
    AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
    AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')

    figma_headers = {
        'Accept': 'application/json',
        'X-Figma-Token': FIGMA_API_KEY
    } 

    s3 = boto3.resource('s3')
    bucket = s3.Bucket("assets.zilliz.com")
    
    with open('guides.json', "r") as f:
        categories = json.load(f)

    with open('faqs.json', "r") as f:
        faqs = json.load(f)

    # find all images
    image_blocks = []
    link_preview_blocks = []
    video_blocks = []
    for category in categories:
        for book in category['books']:
            for page in book['pages']:
                for block in page['blocks']:
                    media = find_media(block)
                    image_blocks += media[0]
                    link_preview_blocks += media[1]
                    video_blocks += media[2]

    for faq in faqs:
        for q in faq["questions"]:
            for block in q['answer']:
                media = find_media(block)
                image_blocks += media[0]
                link_preview_blocks += media[1]
                video_blocks += media[2]

    image_blocks = [ x for x in image_blocks if x['image']['type'] == 'file' ]
    
    for block in link_preview_blocks:
        block['link_preview']['key'] = parse.urlsplit(block['link_preview']['url']).path.split('/')[2]
        block['link_preview']['node'] = ":".join(parse.parse_qs(block['link_preview']['url'])['node-id'][0].split("-"))
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        print(f"Getting {len(image_blocks)} images...")
        files = [ executor.submit(req.get, x['image']['file']['url']) for x in image_blocks ]
        files = [ x.result() for x in files ]
        files = [ BytesIO(x.content) for x in files ]
        print(f"Got {len(files)} images!")
        files = [ executor.submit(bucket.put_object, Key=f"zdoc/{x['id']}.png", Body=y, ACL='public-read') for x, y in zip(image_blocks, files)]
        files = [ x.result() for x in files ]
        print(f"Uploaded {len(files)} images!")

        for x in image_blocks:
            x['image']['file']['url'] = f"https://assets.zilliz.com/zdoc/{x['id']}.png"

        print(f"Getting {len(link_preview_blocks)} link previews...")
        link_previews = [ executor.submit(req.get, f"https://api.figma.com/v1/images/{x['link_preview']['key']}?ids={x['link_preview']['node']}&format=png&scale=3", headers=figma_headers) for x in link_preview_blocks ]
        link_previews = [ x.result() for x in link_previews ]
        link_previews = [ x.json()['images'][y['link_preview']['node']] for x, y in zip(link_previews, link_preview_blocks) ]
        link_previews = [ executor.submit(req.get, x) for x in link_previews ]
        link_previews = [ x.result() for x in link_previews ]
        link_preview_contents = [ BytesIO(x.content) for x in link_previews ]
        print(f"Got {len(link_previews)} link previews!")
        link_previews = [ executor.submit(req.get, f"https://api.figma.com/v1/files/{block['link_preview']['key']}/nodes?ids={block['link_preview']['node']}", headers=figma_headers) for block in link_preview_blocks ]
        link_previews = [ x.result() for x in link_previews ]
        link_preview_titles = [ x.json()['nodes'][y['link_preview']['node']]['document']['name'] for x, y in zip(link_previews, link_preview_blocks) ]
        print(f"Got {len(link_previews)} link preview titles!")
        link_previews = [ executor.submit(bucket.put_object, Key=f"zdoc/{y}.png", Body=z, ACL='public-read') for y, z in zip(link_preview_titles, link_preview_contents)]
        link_previews = [ x.result() for x in link_previews ]
        print(f"Uploaded {len(link_previews)} link previews!")

        for x, y in zip(link_preview_blocks, link_preview_titles):
            x['link_preview']['url'] = f"https://assets.zilliz.com/zdoc/{y}.png"

        print(f"Getting {len(video_blocks)} videos...")
        videos = [ executor.submit(req.get, "https://www.youtube.com/oembed?url=" + f"https://youtube.com/watch?v={x['video']['external']['url'].split('/')[-1]}" + "&format=json") for x in video_blocks ]
        videos = [ x.result() for x in videos ]
        print(f"Got {len(videos)} videos!")

        for x, y in zip(video_blocks, videos):
            x['video']['external']['meta'] = y.json()

    for category in categories:
        for book in category['books']:
            for page in book['pages']:
                for block in page['blocks']:
                    if block['type'] == 'image':
                        block = replace_image_url(block)
                    
                    if block['type'] == 'link_preview':
                        block = replace_link_preview_url(block, link_preview_blocks, link_preview_titles)

                    if block['type'] == 'video':
                        block = replace_video_meta(block, video_blocks)

                    if block['has_children']:
                        for child in block[block['type']]['children']:
                            if child['type'] == 'image':
                                child = replace_image_url(child)
                            
                            if child['type'] == 'link_preview':
                                child = replace_link_preview_url(child, link_preview_blocks, link_preview_titles)

                            if child['type'] == 'video':
                                child = replace_video_meta(child, video_blocks)

    with open('guides.json', "w") as f:
        json.dump(categories, f, indent=4)

    for faq in faqs:
        for q in faq["questions"]:
            for block in q['answer']:
                if block['type'] == 'image':
                    block = replace_image_url(block)
                
                if block['type'] == 'link_preview':
                    print(block['link_preview'])
                    block = replace_link_preview_url(block, link_preview_blocks, link_preview_titles)

                if block['type'] == 'video':
                    block = replace_video_meta(block, video_blocks)

                if block['has_children']:
                    for child in block[block['type']]['children']:
                        if child['type'] == 'image':
                            child = replace_image_url(child)
                        
                        if child['type'] == 'link_preview':
                            child = replace_link_preview_url(child, link_preview_blocks, link_preview_titles)

                        if child['type'] == 'video':
                            child = replace_video_meta(child, video_blocks)
                        
    with open('faqs.json', "w") as f:
        json.dump(faqs, f, indent=4)

    
        