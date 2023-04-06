---
title: Integrate with SentenceTransformers
excerpt: A movie search example for integrating Zilliz Cloud with SentenceTransformers
category: 642e263f5c3da50210f1e869
---

In this example, we are going to be going over a Wikipedia article search using Zilliz Cloud and the SentenceTransformers library. The dataset we are searching through is the Wikipedia-Movie-Plots Dataset found on [Kaggle](https://www.kaggle.com/datasets/jrobischon/wikipedia-movie-plots). For this example, we have rehosted the data in a public google drive.

This example was run on a Zilliz Cloud instance using 1CU.

Let's get started.

## Installing requirements

For this example, we are going to be using `pymilvus` to connect to use Zilliz Cloud, `sentencetransformers` to generate vector embeddings, and `gdown` to download the example dataset.

```shell
pip install pymilvus sentence-transformers gdown
```

## Grabbing the data

We are going to use `gdown` to grab the zip from Google Drive and then decompress it with the built-in `zipfile` library.

```python
import gdown
url = 'https://drive.google.com/uc?id=11ISS45aO2ubNCGaC3Lvd3D7NT8Y7MeO8'
output = './movies.zip'
gdown.download(url, output)

import zipfile

with zipfile.ZipFile("./movies.zip","r") as zip_ref:
    zip_ref.extractall("./movies")
```

## Global parameters

Here we can find the main arguments that need to be modified for running with your own accounts. Beside each is a description of what it is.

```python
# Zilliz Cloud Setup Arguments
COLLECTION_NAME = 'movies_db'  # Collection name
DIMENSION = 384  # Embeddings size
URI = 'https://replace-this-with-your-zilliz-cloud-endpoint'  # Endpoint URI obtained from Zilliz Cloud
USER = 'replace-this-with-your-zilliz-cloud-database-user'  # Username specified when you created this database
PASSWORD = 'replace-this-with-your-zilliz-cloud-database-password'  # Password set for that account

# Inference Arguments
BATCH_SIZE = 128

# Search Arguments
TOP_K = 3
```

## Setting up Zilliz Cloud

At this point, we are going to begin setting up Zilliz Cloud. The steps are as follows:

1. Connect to the Zilliz Cloud instance using the provided URI.

    ```python
    from pymilvus import connections

    # Connect to Milvus Database
    connections.connect(uri=URI, user=USER, password=PASSWORD, secure=True)
    ```

2. If the collection already exists, drop it.

    ```python
    from pymilvus import utility

    # Remove any previous collections with the same name
    if utility.has_collection(COLLECTION_NAME):
        utility.drop_collection(COLLECTION_NAME)
    ```

3. Create the collection that holds the id, title of the movie, and the embeddings of the plot text.

    ```python
    from pymilvus import FieldSchema, CollectionSchema, DataType, Collection


    # Create collection which includes the id, title, and embedding.
    fields = [
        FieldSchema(name='id', dtype=DataType.INT64, is_primary=True, auto_id=True),
        FieldSchema(name='title', dtype=DataType.VARCHAR, max_length=200),  # VARCHARS need a maximum length, so for this example they are set to 200 characters
        FieldSchema(name='embedding', dtype=DataType.FLOAT_VECTOR, dim=DIMENSION)
    ]
    schema = CollectionSchema(fields=fields)
    collection = Collection(name=COLLECTION_NAME, schema=schema)
    ```

4. Create an index on the newly created collection and load it into memory.

    ```python
    # Create an IVF_FLAT index for collection.
    index_params = {
        'metric_type': 'L2',
        'index_type': "AUTOINDEX",
        'params': {}
    }
    collection.create_index(field_name="embedding", index_params=index_params)
    collection.load()
    ```

Once these steps are done the collection is ready to be inserted into and searched. Any data added will be indexed automatically and be available to search immediately. If the data is very fresh, the search might be slower as brute force searching will be used on data that is still in process of getting indexed.

## Inserting the data

For this example, we are going to use the SentenceTransformers miniLM model to create embeddings of the plot text. This model returns 384-dim embeddings.

In these next few steps we will be: 

1. Loading the data.
2. Embedding the plot text data using SentenceTransformers.
3. Inserting the data into Zilliz Cloud.

```python
import csv
from sentence_transformers import SentenceTransformer

transformer = SentenceTransformer('all-MiniLM-L6-v2')

# Extract the book titles
def csv_load(file):
    with open(file, newline='') as f:
        reader = csv.reader(f, delimiter=',')
        for row in reader:
            if '' in (row[1], row[7]):
                continue
            yield (row[1], row[7])


# Extract embeding from text using OpenAI
def embed_insert(data):
    embeds = transformer.encode(data[1]) 
    ins = [
            data[0],
            [x for x in embeds]
    ]
    collection.insert(ins)

import time

data_batch = [[],[]]

for title, plot in csv_load('./movies/plots.csv'):
    data_batch[0].append(title)
    data_batch[1].append(plot)
    if len(data_batch[0]) % BATCH_SIZE == 0:
        embed_insert(data_batch)
        data_batch = [[],[]]

# Embed and insert the remainder
if len(data_batch[0]) != 0:
    embed_insert(data_batch)

# Call a flush to index any unsealed segments.
collection.flush()
```

## Performing the search

With all the data inserted into Zilliz Cloud, we can start performing our searches. In this example, we are going to search for movies based on the plot. Because we are doing a batch search, the search time is shared across the movie searches. 

```python
# Search for titles that closest match these phrases.
search_terms = ['A movie about cars', 'A movie about monsters']

# Search the database based on input text
def embed_search(data):
    embeds = transformer.encode(data) 
    return [x for x in embeds]

search_data = embed_search(search_terms)

start = time.time()
res = collection.search(
    data=search_data,  # Embeded search value
    anns_field="embedding",  # Search across embeddings
    param={},
    limit = TOP_K,  # Limit to top_k results per search
    output_fields=['title']  # Include title field in result
)
end = time.time()

for hits_i, hits in enumerate(res):
    print('Title:', search_terms[hits_i])
    print('Search Time:', end-start)
    print('Results:')
    for hit in hits:
        print( hit.entity.get('title'), '----', hit.distance)
    print()
```

The output should be similar to the following:

```shell
Title: A movie about cars
Search Time: 0.04272913932800293
Results:
Red Line 7000 ---- 0.9104408621788025
The Mysterious Mr. Valentine ---- 0.9127437472343445
Tomboy ---- 0.9254708290100098

Title: A movie about monsters
Search Time: 0.04272913932800293
Results:
Monster Hunt ---- 0.8105474710464478
The Astro-Zombies ---- 0.8998500108718872
Wild Country ---- 0.9238440990447998
```
