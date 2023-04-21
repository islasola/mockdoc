---
title: Create Vector Database
excerpt: Creates a vector database.
category: 64368bb63b18090510bad283
---

## Request

### Parameters

- No query parameters required



- No path parameters required

### Body

```json
{
    "adminPwd": "string",
    "clusterName": "string",
    "clusterType": "string",
    "cuSize": "integer",
    "description": "string"
}
```

| Parameter        | Description                                                                               |
|------------------|-------------------------------------------------------------------------------------------|
| clusterType  | **string**<br>The type of the vector database to be created. Available options are **Performance-optimized** and **Capacity-optimized**, This parameter is optional and it defaults to **Performance-optimized**. || cuSize  | **integer**<br>The size of the CU to be used for the created vector database. It is an integer from 1 to 256. || clusterName  | **string**<br>The name of the vector database to be created. It is a string of no more than 32 characters. || description  | **string**<br>The description of the vector database to be created. This parameter is optional. || adminPwd  | **string**<br>The admin password of the vector database. It is a string of 8 to 128 characters containing uppercase and lowercase alphanumerical characters and special characters such as `~`, `!`, `@`, `#`, `$`, `%`, `^`, `&`, `*`, `?`, `_`, and `-`. |



## Response

Returns the ID of the created vector database with a prompt message indicating the success.

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