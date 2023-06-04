import os, sys, json, re
import requests
import concurrent.futures

def groupgen(sdks):
    for sdk in sdks:
        for group in sdk['groups']:

            short_descs = []
            for page in group['pages']:
                with open('sdks/{}/{}/{}.md'.format(sdk['lang'], group['title'], page['title']), 'r') as f:
                    lines = f.readlines()
                    page_link = f"## [{page['title']}](doc:{page['slug']})"
                    short_desc = [ x for x in lines if re.match(r'^[A-Z]', x[0]) ][0]
                    short_descs.append('\n'.join([page_link, short_desc]))

            short_descs = '\n\n'.join(short_descs)

            
            with open('sdkref/{}-{}.md'.format(sdk['slug'], group['slug']), 'w') as f:
                f.write(f"""---
title: {group['title']}
category: {sdk['id']}
slug: {group['slug']}
---

{short_descs}

""")
                
def pagegen(sdks):
    for sdk in sdks:
        for group in sdk['groups']:
            for page in group['pages']:
                with open('sdks/{}/{}/{}.md'.format(sdk['lang'], group['title'], page['title']), 'r') as f:
                    lines = f.readlines()
                    page_content = ''.join(lines[1:])
                    with open('sdkref/{}.md'.format(page['slug']), 'w') as f:
                        f.write(f"""---
title: {page['title']}
category: {sdk['id']}
parentDoc: {group['id']}
slug: {page['slug']}
---

{page_content}

""")

if __name__ == '__main__':

    api_key = sys.argv[1]

    headers = {
        'Authorization': 'Basic {}'.format(api_key),
    }
    
    url = 'https://dash.readme.com/api/v1/categories?perPage=20'

    r = requests.get(url, headers=headers)

    if r.status_code != 200:
        print('Error fetching categories')
        sys.exit(1)

    categories = r.json()

    sdks = [ dict(lang=x) for x in os.listdir('sdks') if os.path.isdir(os.path.join('sdks', x)) and not x.startswith('.') ]

    for sdk in sdks:
        for category in categories:
            if category['slug'].startswith(sdk['lang']):
                sdk['slug'] = category['slug']
                sdk['title'] = category['title']
                sdk['id'] = category['_id']
                break

    # Add new categories
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        [ executor.submit(
            requests.post, 'https://dash.readme.com/api/v1/categories', 
            headers=headers, 
            json={"title": "{} SDK REFERENCE".format(sdk['lang'].upper()), "type": "reference"}
        ) if 'slug' not in sdk else sdk for sdk in sdks  ]

    print('Categories created')

    # Fetch doc pages per category
    categories = requests.get(url, headers=headers).json()

    # Add missing properties to every sdk
    for sdk in sdks:
        for category in categories:
            if category['slug'].startswith(sdk['lang']):
                sdk['slug'] = category['slug']
                sdk['id'] = category['_id']
                break
        
        groups = [ dict(
            title=x,
            pages=[ dict(
                title=y.split('.')[0],
            ) for y in os.listdir(os.path.join('sdks', sdk['lang'], x)) if os.path.isfile(os.path.join('sdks', sdk['lang'], x, y)) and y.endswith('.md')]
        ) for x in os.listdir(os.path.join('sdks', sdk['lang'])) if os.path.isdir(os.path.join('sdks', sdk['lang'], x)) and not x.startswith('.') ]

        remote_groups = requests.get('https://dash.readme.com/api/v1/categories/{}/docs'.format(sdk['slug']), headers=headers).json()

        for group in groups:
            for remote_group in remote_groups:
                if remote_group['title'] == group['title']:
                    group['id'] = remote_group['_id']
                    group['slug'] = remote_group['slug']
                    break


        with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
            [ executor.submit(
                requests.post, 'https://dash.readme.com/api/v1/docs',
                headers=headers,
                json=dict(title=x['title'], category=sdk['id'])
            ) if 'slug' not in x else x for x in groups ]

        remote_groups = requests.get('https://dash.readme.com/api/v1/categories/{}/docs'.format(sdk['slug']), headers=headers).json()

        for group in groups:
            for remote_group in remote_groups:
                if remote_group['title'] == group['title']:
                    group['id'] = remote_group['_id']
                    group['slug'] = remote_group['slug']
                    break

        print('Groups created for {}'.format(sdk['lang']))

        for group in groups:
            for page in group['pages']:

                for remote_group in remote_groups:
                    for remote_page in remote_group['children']:
                        if remote_page['title'] == page['title']:
                            page['id'] = remote_page['_id']
                            page['slug'] = remote_page['slug']
                            break

            with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
                [ executor.submit(
                    requests.post, 'https://dash.readme.com/api/v1/docs',
                    headers=headers,
                    json=dict(title=x['title'], category=sdk['id'], parentDoc=group['id'])
                ) if 'slug' not in x else x for x in group['pages'] ]

        remote_groups = requests.get('https://dash.readme.com/api/v1/categories/{}/docs'.format(sdk['slug']), headers=headers).json()   

        for group in groups:
            for remote_group in remote_groups:
                if remote_group['title'] == group['title']:
                    group['id'] = remote_group['_id']
                    group['slug'] = remote_group['slug']
                    group['pages'] = [ dict(
                        title=x['title'],
                        id=x['_id'],
                        slug=x['slug']
                    ) for x in remote_group['children'] ]
                    break
        
            print('Pages created in group {} for {}'.format(group['title'], sdk['lang']))

        sdk['groups'] = groups
        
    groupgen(sdks)
    pagegen(sdks)