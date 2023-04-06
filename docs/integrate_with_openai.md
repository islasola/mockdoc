---
title: Integrate with OpenAI Embedding APIs
excerpt: A similarity search example for integrating Zilliz Cloud with OpenAI Embedding APIs
category: 642e263f5c3da50210f1e869
---

This page discusses vector database integration with OpenAI's embedding API.

We'll showcase how [OpenAI's Embedding API](https://beta.openai.com/docs/guides/embeddings) can be used with our vector database to search across book titles. Many existing book search solutions (such as those used by public libraries, for example) rely on keyword matching rather than a semantic understanding of what the title is actually about. Using a trained model to represent the input data is known as _semantic search_, and can be expanded to a variety of different text-based use cases, including anomaly detection and document search.

## Getting started

The only prerequisite you'll need here is an API key from the [OpenAI website](https://openai.com/api/). Be sure to head over to our [cloud landing page](https://zilliz.com/cloud) for $400 in free credits which you can use to spin up a new database if you haven't done so already.

We'll also prepare the data that we're going to use for this example. You can grab the book titles [here](https://www.kaggle.com/datasets/jealousleopard/goodreadsbooks). Let's create a function to load book titles from our CSV.

```python
import csv
import json
import random
import openai
import time
from pymilvus import connections, FieldSchema, CollectionSchema, DataType, Collection, utility
```

```python
# Extract the book titles
def csv_load(file):
    with open(file, newline='') as f:
        reader=csv.reader(f, delimiter=',')
        for row in reader:
            yield row[1]
```

With this, we're ready to move on to generating embeddings.

## Searching book titles with OpenAI & Zilliz Cloud

Here we can find the main parameters that need to be modified for running with your own accounts. Beside each is a description of what it is.

```python
FILE = '/content/books.csv'  # Download it from https://www.kaggle.com/datasets/jealousleopard/goodreadsbooks and save it in the folder that holds your script.
COLLECTION_NAME = 'title_db'  # Collection name
DIMENSION = 1536  # Embeddings size
COUNT = 100  # How many titles to embed and insert.
URI = ''  # Endpoint URI obtained from Zilliz Cloud
USER = 'db_admin'  # Username specified when you created this database
PASSWORD = ''  # Password set for that account 
OPENAI_ENGINE = 'text-embedding-ada-002'  # Which engine to use
openai.api_key = ''  # Use your own Open AI API Key here
```

> 📘 Notes
>
> Because the embedding process for a free OpenAI account is relatively time-consuming, we use a set of data small enough to reach a balance between the script executing time and the precision of the search results. You can change the `COUNT` constant to fit your needs.

This segment deals with Zilliz Cloud and setting up the database for this use case. Within Zilliz Cloud we need to set up a collection and index the collection. For more information on how to set up and use Zilliz Cloud, look [here](https://zilliz.com/doc/quick_start).

```python
# Connect to Zilliz Cloud
connections.connect(uri=URI, user=USER, password=PASSWORD, secure=True)

# Remove collection if it already exists
if utility.has_collection(COLLECTION_NAME):
    utility.drop_collection(COLLECTION_NAME)

# Create collection which includes the id, title, and embedding.
fields = [
    FieldSchema(name='id', dtype=DataType.INT64, descrition='Ids', is_primary=True, auto_id=False),
    FieldSchema(name='title', dtype=DataType.VARCHAR, description='Title texts', max_length=200),
    FieldSchema(name='embedding', dtype=DataType.FLOAT_VECTOR, description='Embedding vectors', dim=DIMENSION)
]
schema = CollectionSchema(fields=fields, description='Title collection')
collection = Collection(name=COLLECTION_NAME, schema=schema)

# Create an index for the collection.
index_params = {
    'metric_type': 'L2',
    'index_type': "AUTOINDEX",
    'params': {}
}
collection.create_index(field_name="embedding", index_params=index_params)
```

Once we have the collection setup we need to start inserting our data. This is in three steps: reading the data, embedding the titles, and inserting into Zilliz Cloud.

```python
# Extract embedding from text using OpenAI
def embed(text):
    return openai.Embedding.create(
        input=text, 
        engine=OPENAI_ENGINE)["data"][0]["embedding"]

# Insert each title and its embedding
for idx, text in enumerate(random.sample(sorted(csv_load(FILE)), k=COUNT)):  # Load COUNT amount of random values from dataset
    ins=[[idx], [(text[:198] + '..') if len(text) > 200 else text], [embed(text)]]  # Insert the title id, the title text, and the title embedding vector
    collection.insert(ins)
    time.sleep(3)  # Free OpenAI account limited to 60 RPM
```

```python
# Load the collection into memory for searching
collection.load()

# Search the database based on input text
def search(text):
    # Search parameters for the index
    search_params={
        "metric_type": "L2", 
        "params": {"level": 1}
    }

    results=collection.search(
        data=[embed(text)],  # Embeded search value
        anns_field="embedding",  # Search across embeddings
        param=search_params,
        limit=5,  # Limit to five results per search
        output_fields=['title']  # Include title field in result
    )

    ret=[]
    for hit in results[0]:
        row=[]
        row.extend([hit.id, hit.score, hit.entity.get('title')])  # Get the id, distance, and title for the results
        ret.append(row)
    return ret

search_terms=['self-improvement', 'landscape']

for x in search_terms:
    print('Search term:', x)
    for result in search(x):
        print(result)
    print()
```

You should see the following as the output:

```shell
Search term: self-improvement
[70, 0.34909766912460327, 'Life Management for Busy Woman: Growth and Study Guide']
[18, 0.4245884120464325, 'From Socrates to Sartre: The Philosophic Quest']
[63, 0.4264194667339325, 'Love']
[88, 0.44693559408187866, "The Innovator's Dilemma: The Revolutionary Book that Will Change the Way You Do Business"]
[29, 0.4684774875640869, 'The Thousandfold Thought (The Prince of Nothing  #3)']

Search term: landscape
[63, 0.34171175956726074, 'Love']
[48, 0.4100739061832428, 'Outlander']
[67, 0.41952890157699585, 'Ice Castles']
[98, 0.42765650153160095, 'The Long Walk']
[24, 0.43053609132766724, 'Notes from a Small Island']
```

A full example of this is available on [here](https://colab.research.google.com/drive/1bAX1Ah7ub4uVibQIT82LvdPmrRCzCXKM?usp=sharing).
