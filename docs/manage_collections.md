---
title: Manage Collections
excerpt: Similar to a table in a relational database, a collection in a vector database consists of two dimensions, and they are a fixed number of columns defined in the schema and a variable number of rows corresponding to the inserted entities. In this guide, you are about to create and drop a collection.
category: 642e25b85291100124b05ef4
---

## Create a collection

In this example, create a collection named **medium_articles_2020**. To get the example dataset, refer to [Example Dataset Overview](example_dataset_overview).

```Python
from pymilvus import FieldSchema, CollectionSchema, DataType, Collection

fields = [
    FieldSchema(name="id", dtype=DataType.INT64, is_primary=True),
    FieldSchema(name="title", dtype=DataType.VARCHAR, max_length=512),   
    FieldSchema(name="title_vector", dtype=DataType.FLOAT_VECTOR, dim=768),
    FieldSchema(name="link", dtype=DataType.VARCHAR, max_length=512),
    FieldSchema(name="reading_time", dtype=DataType.INT64),
    FieldSchema(name="publication", dtype=DataType.VARCHAR, max_length=512),
    FieldSchema(name="claps", dtype=DataType.INT64),
    FieldSchema(name="responses", dtype=DataType.INT64)
]

# Build the schema
schema = CollectionSchema(
    fields,
    description="Schema of Medium articles"
)

collection = Collection(
    name="medium_articles_2020", 
    description="Medium articles published between Jan 2020 to August 2020 in prominent publications",
    schema=schema
)
```

In the above snippet,

- `id` is the primary field. For this field, the parameter `is_primary` is set to `True`.
- `title_vector` is a vector field. The parameter `dim` specifies the vector dimension.
- `title`, `link`, and `publication` are string fields. The parameter `max_length` specifies the maximum number of characters allowed in the string.
- `reading_time`, `claps`, and `responses` are integer fields. No extra parameters need to be set on these fields.

For your reference, Zilliz Cloud supports the following field data types:

- Boolean value (BOOLEAN)
- 8-byte floating-point (DOUBLE)
- 4-byte floating-point (FLOAT)
- Float vector (FLOAT_VECTOR)
- 8-bit integer (INT8)
- 32-bit integer (INT32)
- 64-bit integer (INT64)
- Variable character (VARCHAR)

## Rename a collection

To rename a collection, you can use the collection-renaming API to interact with Zilliz Cloud. In the following code snippet, we rename the collection created above from **medium_articles_2020** to **medium_passages_2020**.

```python
from pymilvus import utility

utility.rename_collection("medium_articles_2020", "medium_passages_2020")
```

## Drop a collection

Dropping a collection deletes all information from the collection, including its data, metadata, and indexes. Exercise caution when dropping a collection because this operation is irreversible.

```Python
from pymilvus import utility

utility.drop_collection("medium_articles_2020")
```
