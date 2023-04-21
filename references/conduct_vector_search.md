---
title: Conduct Vector Search
excerpt: Conducts a search against the vector field in the specified collection.
category: 64368bb63b18090510bad283
---

## Request

### Parameters

- No query parameters required



- No path parameters required

### Body

```json
{
    "anns": "object",
    "collectionName": "string",
    "filter": "string",
    "level": "integer",
    "limit": "integer",
    "offset": "integer",
    "outputFields": "array"
}
```

| Parameter        | Description                                                                               |
|------------------|-------------------------------------------------------------------------------------------|
| collectionName  | **string**<br>The name of the collection in concern. || outputFields  | **array**<br>The fields to be returned along with the vector search results. || anns  | **object**<br>The search settings || level  | **integer**<br>The level of accurary of the search results. It defaults to 1 and possible values are 1, 2, and 3. A higher value indicates a more accurate result at a slower performance. || filter  | **string**<br>The filtering condition for the vector search. || limit  | **integer**<br>The maximum number of records to return. || offset  | **integer**<br>The position at which the results are truncated. This usually works with `limit` to return a small set of records in the middle of the returned result. |



## Response

Returns the results of the vector search.

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