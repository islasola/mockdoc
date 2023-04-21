---
title: Conduct Scalar Query
excerpt: Conducts a query against scalar fields in the specified collection.
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
    "filter": "string",
    "outputFields": "array"
}
```

| Parameter        | Description                                                                               |
|------------------|-------------------------------------------------------------------------------------------|
| collectionName  | **string**<br>The name of the collection in concern. || filter  | **string**<br>The filtering condition for the query. || outputFields  | **array**<br>The fields to be returned along with the query results. |



## Response

Returns the results of the query.

### Body

- Response body if we process your request successfully

```json
{
    "code": "integer",
    "data": "array"
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
| `code` | **integer**<br> || `data` | **array**<br> |
| `message`  | **string**<br>Indicates the possible reason for the reported error. |

## Have a try!

Use our API explorer on the side pane to call this API and check the request and responses. Remember to fill in the necessary body parameters below, if applicable.