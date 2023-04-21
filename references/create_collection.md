---
title: Create Collection
excerpt: Creates a collection in the specified vector database. As to the request body, there are two options available. If you choose to use **Option 1**, Zilliz Cloud will create the `id` and `vector` fields in the created collection.
category: 64368bb63b18090510bad283
---

## Request

### Parameters

- No query parameters required



- No path parameters required

### Body

```json
{
    "collectionName": "string",
    "descriptions": "string",
    "dimensions": "integer"
}
```

| Parameter        | Description                                                                               |
|------------------|-------------------------------------------------------------------------------------------|
| collectionName  | **string**<br>The name of the collection to be created. || dimensions  | **integer**<br>The number of dimensions for the vector field of the collection. || descriptions  | **string**<br>The description of the collection to be created. |

```json
{
    "collectionName": "string",
    "description": "string",
    "fields": "array",
    "indexes": "array",
    "shardsNum": "integer"
}
```

| Parameter        | Description                                                                               |
|------------------|-------------------------------------------------------------------------------------------|
| collectionName  | **string**<br>The name of the collection to be created. || shardsNum  | **integer**<br>The number of shards to be created for the collection. This parameter is optional. || description  | **string**<br>The description of the collection to be created. This parameter is optional || fields  | **array**<br>The fields of the collection to be created. || indexes  | **array**<br>The fields to be indexed along with the creation of the database. This parameter is optional. |



## Response

Empty returns.

### Body

- Response body if we process your request successfully

```json
{
    "code": "integer",
    "data": "object"
}
```

- Response body if we failed to process your request

```json
{
    "code": string,
    "message": string
}
```

### Properties

The properties in the returned response are listed in the following table.

| Property | Description                                                                                                                                  |
|----------|----------------------------------------------------------------------------------------------------------------------------------------------|
| `code`     | **integer**<br>Indicates whether the request succeeds.<br><ul><li>`200`: The request succeeds.</li><li>Others: Some error occurs.</li></ul> |
| `code` | **integer**<br> || `data` | **object**<br> |
| `message`  | **string**<br>Indicates the possible reason for the reported error. |

## Have a try!

Use our API explorer on the side pane to call this API and check the request and responses. Remember to fill in the necessary body parameters below, if applicable.