---
title: Manage Collections
excerpt: Similar to a table in a relational database, a collection in a vector database consists of two dimensions, and they are a fixed number of columns defined in the schema and a variable number of rows corresponding to the inserted entities. In this guide, you are about to create and manage a collection.
category: 
---

## Create a collection

In this example, create a collection named **test**. To get the example dataset, refer to [Example Dataset Overview]().

The following example gives you a simple way to create a collection:

```shell
curl --request POST \
     --url <API-Endpoint>/v1/<Cluster-ID>/collections/create \
     --header 'Authorization: Bearer: <API-Key>' \
     --header 'accept: application/json' \
     --header 'content-type: application/json'
     -d '{
       "collectionName": "test",
       "dimensions": 256
      }'
```

To create a more complex collection, use the following example. This creates a collection that measures similarity by Euclidean distance (L2) and enables custom fields.

```shell
curl --request POST \
     --url <API-Endpoint>/v1/<Cluster-ID>/collections/create \
     --header 'Authorization: Bearer: <API-Key>' \
     --header 'accept: application/json' \
     --header 'content-type: application/json'
     -d '{
       "collectionName": "test",
       "shardsNum": 2,
       "description": "....",
       "fields": [
         {
            "name": "id",
            "type": "int64",
            "primaryKey": true,
            "autoId": true,
            "description": "auto increment id"
         },
         {
            "name": "docUrl",
            "type": "varchar(32)",
            "description": "The address of the document."
         },
         {
            "name": "vector",
            "type": "FloatVector(128)"
         }
       ],
       "indexes": [
         {
            "indexName": "idx_vector_test",
            "fieldName": "vector",
            "metricType": "L2"
         }
       ]
     }'
```

The following table describes the fields.

| Field |  Description  |
|----- | -------- |
| collectionName   | (Required) The name of the collection. Value type: String.| 
| dimensions   | (Required) The dimension of the data. Value type: Int32. Value range: 32 to 32768.|
| shardsNum   |  The number of shards on which data is distributed. Value range: 1 to 32. Default value: **2**.  |
| fields   | The schema of the collection comprising the listed fields. |
| name     | The name of the field. Value type: String. |
| type     | The type of the field data. |
| primaryKey | Whether this field is the primary key. Valid values: **true** and **false**. If you set this value to **true**, you can also consider setting **autoID** to **true**, so that the value in this field automatically increments.
| autoId   | Whether the value of the primary key automatically increments. This field applies when **primaryKey** is set to **true** for this field. |
| indexes  | An array of fields to be indxed. |
| indexName | The name of the index file to be generated. |
| fieldName | The name of the field to be indexed. |
| metricType | The metric type used in the index process. Valid values: **L2** (Euclidean Distance) and **IP** (Inner product).

For your reference, Zilliz Cloud supports the following field data types:

- Boolean value (BOOLEAN)
- 8-byte floating-point (DOUBLE)
- 4-byte floating-point (FLOAT)
- Float vector (FLOAT_VECTOR)
- 8-bit integer (INT8)
- 32-bit integer (INT32)
- 64-bit integer (INT64)
- Variable character (VARCHAR)

## View collections

The following example lists all collections created in the cluster.

```shell
curl --request GET \
     --url <API-Endpoint>/v1/<Cluster-ID>/collections \
     --header 'Authorization: Bearer: <API-Key>' \
     --header 'accept: application/json' \
     --header 'content-type: application/json'
```

## View the details of a collection

If you want to view the details of a specific collection, use the following example:

```shell
curl --location --request GET '<API-Endpoint>/v1/<Cluster-ID>/collections/describe?collectionName=test' \
--header 'Authorization: Bearer <API-Key>' \
--header 'Accept: */*' \
--header 'Host: api.gcp-us-west1.cloud-uat3.zilliz.com' \
--header 'Connection: keep-alive'
```

The expected result is as follows:

```shell
{
    "code": 200,
    "data": {
        "collectionId": 441056023867410897,
        "collectionName": "test",
        "shardsNum": 1,
        "description": "",
        "load": "loaded",
        "fields": [
            {
                "name": "id",
                "type": "int64",
                "primaryKey": true,
                "autoId": true,
                "description": "entity id"
            },
            {
                "name": "title",
                "type": "varchar(32)",
                "primaryKey": false,
                "autoId": false,
                "description": "entity title"
            },
            {
                "name": "title_vector",
                "type": "floatVector",
                "primaryKey": false,
                "autoId": false,
                "description": "title vector"
            }
        ],
        "indexes": [
            {
                "indexName": "vector_index",
                "fieldName": "title_vector",
                "metricType": "L2"
            }
        ]
    }
}
```

## Drop a collection

Dropping a collection deletes all information from the collection, including its data, metadata, and indexes. Exercise caution when dropping a collection because this operation is irreversible.

The following command drops a collection named **test**:

```shell
curl --location --request POST '<API-Endpoint>/v1/<Cluster-ID>/collections/drop' \
--header 'Authorization: Bearer <API-Key>' \
--header 'Content-Type: application/json' \
--header 'Accept: */*' \
--header 'Connection: keep-alive' \
--data-raw '{
    "collectionName": "test"
}'
```

The expected result is as follows:

```shell
{
   code: 200,
   data: {}
}
```