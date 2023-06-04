# RESTful API Examples

## Create Collection

Create a collection named `medium_articles`:

```shell
curl --request POST \
     --url 'https://<Cluster-ID>.api.<Cloud-Region>.vectordb.zilliz.com/v1/vector/collections/create' \
     --header 'Authorization: Bearer: <API-Key>' \
     --header 'accept: application/json' \
     --header 'content-type: application/json'
     -d '{
       "collectionName": "medium_articles",
       "dimension": 256,
       "metricType": "L2",
       "primaryField": "id",
       "vectorField": "vector"
      }'
```

Success response:

```shell
{
    "code": 200,
    "data": {}
}
```

## Drop Collection

Drop a collection named `medium_articles`:

```shell
curl --request POST \
     --url 'https://<Cluster-ID>.api.<Cloud-Region>.vectordb.zilliz.com/v1/vector/collections/drop' \
     --header 'Authorization: Bearer: <API-Key>' \
     --header 'accept: application/json' \
     --header 'content-type: application/json'
     -d '{
        "collectionName": "medium_articles"
      }'
```

Success response:

```shell
{
    "code": 200,
    "data": {}
}
```

## Describe Collection

Describe the details of a collection named `medium_articles`:

```shell
curl --request POST \
     --url 'https://<Cluster-ID>.api.<Cloud-Region>.vectordb.zilliz.com/v1/vector/collections/describe' \
     --header 'Authorization: Bearer: <API-Key>' \
     --header 'accept: application/json' \
     --header 'content-type: application/json'
     -d '{
        "collectionName": "medium_articles"
      }'
```

Success response:

```shell
{
    "code": 200,
    "data": {
        "collectionName": "string",
        "description": "string",
        "fields": [
            {
                "autoId": true,
                "description": "string",
                "name": "string",
                "primaryKey": true,
                "type": "string"
            }
        ],
        "indexes": [
            {
                "fieldName": "string",
                "indexName": "string",
                "metricType": "string"
            }
        ],
        "load": "string",
        "shardsNum": 0,
        "enableDynamic": true
    }
}
```

## List Collections

List all collections in a cluster:

```shell
curl --request POST \
     --url 'https://<Cluster-ID>.api.<Cloud-Region>.vectordb.zilliz.com/v1/vector/collections' \
     --header 'Authorization: Bearer: <API-Key>' \
     --header 'accept: application/json' \
     --header 'content-type: application/json'
```

Sample response:

```shell
{
   code: 200,
   data: [
         "collection1",
         "collection2",
         ...
         "collectionN",
         ]
}
```

## Insert

Insert an entity to a collection named `collection1`:

```shell
curl --request POST \
     --url 'https://<Cluster-ID>.api.<Cloud-Region>.vectordb.zilliz.com/v1/vector/insert' \
     --header 'Authorization: Bearer: <API-Key>' \
     --header 'accept: application/json' \
     --header 'content-type: application/json'
     -d '{
         "collectionName": "collection1",
         "data": {
             "id": "id1",
             "vector": [0.1, 0.2, 0.3],
             "name": "tom",
             "email": "tom@zilliz.com",
             "date": "2023-04-13"
          }
     }'
```

Insert multiple entities:

```shell
curl --request POST \
     --url 'https://<Cluster-ID>.api.<Cloud-Region>.vectordb.zilliz.com/v1/vector/insert' \
     --header 'Authorization: Bearer: <API-Key>' \
     --header 'accept: application/json' \
     --header 'content-type: application/json'
     -d '{
         "collectionName": "collection1",
         "data": [
             {
                "id": "id1",
                "vector": [0.1, 0.2, 0.3],
                "name": "bob",
                "email": "bob@zilliz.com",
                "date": "2023-04-13"
             },{
                "id": "id2",
                "vector": [0.1, 0.2, 0.3],
                "name": "ally",
                "email": "ally@zilliz.com",
                "date": "2023-04-11"
             }
         ]
     }'
```

## Search

Search entities based on a given vector:

```shell
curl --request POST \
     --url 'https://<Cluster-ID>.api.<Cloud-Region>.vectordb.zilliz.com/v1/vector/search' \
     --header 'Authorization: Bearer: <API-Key>' \
     --header 'accept: application/json' \
     --header 'content-type: application/json'
     -d '{
        "collectionName": "collection1",
        "vector": [0.0128121, 0.029119, .... , 0.09121]
      }'
```

Search entities and return specific fields:

```shell
curl --request POST \
     --url 'https://<Cluster-ID>.api.<Cloud-Region>.vectordb.zilliz.com/v1/vector/search' \
     --header 'Authorization: Bearer: <API-Key>' \
     --header 'accept: application/json' \
     --header 'content-type: application/json'
     -d '{
       "collectionName": "collection1",
       "outputFields": ["id", "name", "feature", "distance"],
       "vector": [0.0128121, 0.029119, .... , 0.09121],
       "filter": "id in (1, 2, 3)",
       "limit": 100,
       "offset": 0
     }'
```

## Query

Query entities that meet specific conditions:

```shell
curl --request POST \
     --url 'https://<Cluster-ID>.api.<Cloud-Region>.vectordb.zilliz.com/v1/vector/query' \
     --header 'Authorization: Bearer: <API-Key>' \
     --header 'accept: application/json' \
     --header 'content-type: application/json'
     -d '{
       "collectionName": "collection1",
       "outputFields": ["id", "name", "feature", "distance"],
       "filter": "id in (1, 2, 3)",
       "limit": 100,
       "offset": 0
     }'
```

## Get

Get a specified entity whose ID is an integer:

```shell
curl --request POST \
     --url 'https://<Cluster-ID>.api.<Cloud-Region>.vectordb.zilliz.com/v1/vector/get' \
     --header 'Authorization: Bearer: <API-Key>' \
     --header 'accept: application/json' \
     --header 'content-type: application/json'
     -d '{
       "collectionName": "collection1",
       "outputFields": ["id", "name", "feature", "distance"],
       "id": 1
     }'
```

Get a specified entity whose ID is a string:

```shell
curl --request POST \
     --url 'https://<Cluster-ID>.api.<Cloud-Region>.vectordb.zilliz.com/v1/vector/get' \
     --header 'Authorization: Bearer: <API-Key>' \
     --header 'accept: application/json' \
     --header 'content-type: application/json'
     -d '{
       "collectionName": "collection1",
       "outputFields": ["id", "name", "feature", "distance"],
       "id": "id1"
     }'
```

Get a list of entities whose IDs are integers:

```shell
curl --request POST \
     --url 'https://<Cluster-ID>.api.<Cloud-Region>.vectordb.zilliz.com/v1/vector/get' \
     --header 'Authorization: Bearer: <API-Key>' \
     --header 'accept: application/json' \
     --header 'content-type: application/json'
     -d '{
       "collectionName": "collection1",
       "outputFields": ["id", "name", "feature", "distance"],
       "id": [1,2,3,...]
     }'
```

Get a list of entities whose IDs are strings:

```shell
curl --request POST \
     --url 'https://<Cluster-ID>.api.<Cloud-Region>.vectordb.zilliz.com/v1/vector/get' \
     --header 'Authorization: Bearer: <API-Key>' \
     --header 'accept: application/json' \
     --header 'content-type: application/json'
     -d '{
       "collectionName": "collection1",
       "outputFields": ["id", "name", "feature", "distance"],
       "id": ["id1", "id2", "id3",...]
     }'
```

## Delete

Delete a collection whose ID is an integer:

```shell
curl --request POST \
     --url 'https://<Cluster-ID>.api.<Cloud-Region>.vectordb.zilliz.com/v1/vector/delete' \
     --header 'Authorization: Bearer: <API-Key>' \
     --header 'accept: application/json' \
     --header 'content-type: application/json'
     -d '{
       "collectionName": "collection1",
       "id": 1
     }'
```

Delete a collection whose ID is a string:

```shell
curl --request POST \
     --url 'https://<Cluster-ID>.api.<Cloud-Region>.vectordb.zilliz.com/v1/vector/delete' \
     --header 'Authorization: Bearer: <API-Key>' \
     --header 'accept: application/json' \
     --header 'content-type: application/json'
     -d '{
       "collectionName": "collection1",
       "id": "id1"
     }'
```

Delete a list of collections whose IDs are integers:

```shell
curl --request POST \
     --url 'https://<Cluster-ID>.api.<Cloud-Region>.vectordb.zilliz.com/v1/vector/delete' \
     --header 'Authorization: Bearer: <API-Key>' \
     --header 'accept: application/json' \
     --header 'content-type: application/json'
     -d '{
        "collectionName": "collection1",
        "id": [1,2,3,4]
      }'
```

Delete a list of collections whose IDs are strings:

```shell
curl --request POST \
     --url 'https://<Cluster-ID>.api.<Cloud-Region>.vectordb.zilliz.com/v1/vector/delete' \
     --header 'Authorization: Bearer: <API-Key>' \
     --header 'accept: application/json' \
     --header 'content-type: application/json'
     -d '{
        "collectionName": "collection1",
        "id": ["id1", "id2", "id3","id4"]
      }'
```
