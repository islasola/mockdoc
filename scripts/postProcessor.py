import requests as req
import json
import os, re
from docwriter import DocWriter
from dotenv import load_dotenv


if __name__ == "__main__":

    # write guides
    with open("guides.json", "r") as f:
        guides = json.load(f)

        DocWriter(guides).write_docs()


    # write faqs
    load_dotenv()

    README_API_KEY = os.environ.get('README_API_KEY')

    rdme_headers = {
       "accept": "application/json",
       "content-type": "application/json",
       "authorization": f"Basic {README_API_KEY}"
    }

    rdme_url = "https://dash.readme.com/api/v1/categories?perPage=20"

    categories = req.get(rdme_url, headers=rdme_headers).json()

    faqs_id = [ category["_id"] for category in categories if category["title"] == "FAQs" ][0]

    with open("faqs.json", "r") as f:
        faqs = json.load(f)

        DocWriter(faqs, type="faqs").write_faqs(faqs_id)

    # Process code blocks

    docs = [ x for x in os.listdir("docs") if x.endswith(".md") ]

    for doc in docs:
        with open(f"docs/{doc}", "r") as f:
            content = f.read()

        content = re.sub(r"(\s*```)\n*(\s*```)", r"\1\n\2", content)

        with open(f"docs/{doc}", "w") as f:
            f.write(content)
