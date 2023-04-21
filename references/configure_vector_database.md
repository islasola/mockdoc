---
title: Configure Vector Database
excerpt: Configures the specified vector database. Currently, you can configure the its CU size using this API.
category: 64368bb63b18090510bad283
---

## Request

### Parameters

- No query parameters required



- No path parameters required

### Body



## Response

Returns the ID of the vector database affected by this operation with a prompt message indicating the success or an error message with an error code.

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