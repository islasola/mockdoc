---
title: Insert Records to Collection
excerpt: Inserts the records that match the filtering condition from the specified collection. Notes that the size of the POST request should be no greater than 50 MB, the number or rows to be inserted should be no more than 5,000 rows, and the schema of the `data` object should match the schema of the specified collection.
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
    "data": "array"
}
```

| Parameter        | Description                                                                               |
|------------------|-------------------------------------------------------------------------------------------|
| collectionName  | **string**<br>The name of the collection in concern. || data  | **array**<br>The data records to be inserted. |



## Response

Returns the IDs of the inserted records.

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