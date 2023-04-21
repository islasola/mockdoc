---
title: Describe Collection
excerpt: Describes the specified collection in detail.
category: 64368bb63b18090510bad283
---

## Request

### Parameters

- No query parameters required



- No path parameters required

### Body



## Response

Returns the detailed information about the specified collection.

### Body

- Response body if we process your request successfully

```json
{
    "collectionName": "string",
    "description": "string",
    "fields": "array",
    "indexes": "array",
    "shardsNum": "integer"
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
| `collectionName` | **string**<br>The name of the collection to be created. || `shardsNum` | **integer**<br>The number of shards to be created for the collection. This parameter is optional. || `description` | **string**<br>The description of the collection to be created. This parameter is optional || `fields` | **array**<br>The fields of the collection to be created. || `indexes` | **array**<br>The fields to be indexed along with the creation of the database. This parameter is optional. |
| `message`  | **string**<br>Indicates the possible reason for the reported error. |

## Have a try!

Use our API explorer on the side pane to call this API and check the request and responses. Remember to fill in the necessary body parameters below, if applicable.