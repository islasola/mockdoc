from notionparser import NotionPageParser, NotionDatabaseParser, ReadmeOperator
import requests
import json
import os 

if __name__ == '__main__':

    root = os.environ["ROOT_DATABASE"]

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
                    "property": "Progress",
                    "select": {
                        "equals": "Drafted"
                    }
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

    dbparser = NotionDatabaseParser()
    results = dbparser.retrieve(root, payload)
    
    rdme = ReadmeOperator()
    categories = rdme.retrieve_categories()
    category_names = [item["title"] for item in categories]

    for item in results:
        if item["page_title"] not in category_names:
            rdme.add_category(item["page_title"])

    categories = rdme.retrieve_categories()
    category_slugs = [item["slug"] for item in categories]
            
    for idx, item in enumerate(results):
        category = categories[idx]
        category_slug = category_slugs[idx]

        books = list(filter(lambda x: x["type"] == "child_database", item["children"].blocks))

        if books:
            category_id = category["id"]
            for book in books:
                title = dbparser.book_title(book["id"])
                pages = dbparser.retrieve(book["id"], payload)
                body = dbparser.overview(pages)

                docs = list(filter(lambda x: x['title'] == title, rdme.retrieve_docs_in_category(category_slug)))

                if docs:
                    r = rdme.update_page(docs[0]['slug'])
                    print(f"Updated {title} in {category_slug}!")
                    parent_id = r['_id']
                    parent_slug = r['slug']
                else:
                    r = rdme.add_page(title=title, body=body, category=category_id)
                    parent_id = r['_id']
                    parent_slug = r['slug']
                    print(f"Added {title} to {category_slug}!")
                
                for page in pages:
                    page_title = page["page_title"]
                    page_id = page["page_id"]
                    page_body = NotionPageParser(page_id).markdown()

                    docs = list(filter(lambda x: x['title'] == page_title, rdme.retrieve_sub_pages_in_doc(category_slug, doc_id=parent_id)))

                    if docs:
                        rdme.update_page(docs[0]['slug'], body=page_body)
                        print(f"Updated {page_title} in {category_slug}'s {parent_slug}!")
                    else:
                        rdme.add_page(title=page_title, body=page_body, category=category_id, parent=parent_id)
                        print(f"Added {page_title} to {category_slug}'s {parent_slug}!")