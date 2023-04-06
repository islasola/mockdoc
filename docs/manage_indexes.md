---
title: Manage Indexes
excerpt: All ANN searches on Zilliz Cloud rely on indexes for extremely high performance. Before any ANN searches, you have to create indexes on your collection and load the indexes into CUs.
category: 642e25b85291100124b05ef4
---

## Create an index

The following example creates an index on the `title_vector` field in the **medium_article_2020** collection created in [this guide](manage_collections).

``` Python
from pymilvus import Collection

index_params = {
    "index_type": "AUTOINDEX",
    "metric_type": "L2",
    "params": {}
}

collection = Collection("medium_articles_2020")
collection.create_index(
  field_name="title_vector", 
  index_params=index_params
)
```

**AUTOINDEX** is a proprietary index type available on Zilliz Cloud for index auto-optimization. 

> 📘 Note
>
> Currently, Zilliz Cloud does not allow indexes on scalar fields.

## Load an index

Load the index of the collection for ANN searches.

``` Python
from pymilvus import Collection

collection = Collection("medium_articles_2020")      
collection.load()
```

## Release an index 

For some collections that are not frequently used, you can release their indexes to save CUs. You can load them again later when needed. Note that this operation only releases indexes from CUs, but does not delete data or its index from the collection.

``` Python
from pymilvus import Collection

collection = Collection("medium_articles_2020")     
collection.release()
```

Since reloading a collection is time-consuming, only release the collections that will stay idle for a long time, e.g. more than 10 hours.

## Drop an index

For those indexes no longer in need, drop them as follows:

``` Python
from pymilvus import Collection

collection = Collection("medium_articles_2020")     
collection.drop_index()
```

Note that, if you want to change index parameters, such as changing `metric_type` from `L2` to `IP`, you need to drop the current index and create a new one.
