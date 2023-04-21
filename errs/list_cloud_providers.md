---
title: List Cloud Providers
excerpt: Lists available cloud providers.
category: 64368bb63b18090510bad283
---

## Use cases

This endpoint applies to the scenario where you want to list all available cloud providers on Zilliz Cloud.

## Request

### Parameters

No path or query parameters required

### Body

No request body required

## Response

### Body

- Response body if we process your request successfully

```json
{
    code: 200,
    data: [
     {
        "cloudId": "aws",
        "description": "amazon cloud"
     },
     {
        "cloudId": "gcp",
        "description": "google cloud"
     }
    ]
}
```

- Response body if we failed to process your request

```json
{
    "code": 80001,
    "message": "Invalid API key."
}
```

### Properties

The properties in the returned response are listed in the following table.

| Property | Description                                                                                                                                  |
|----------|----------------------------------------------------------------------------------------------------------------------------------------------|
| `code`     | **integer**<br>Indicates whether the request succeeds.<br><ul><li>`200`: The request succeeds.</li><li>Others: Some error occurs.</li></ul> |
| `data`    | **array of objects**<br>Includes the list of returned cloud providers.
| `data[].cloudId` | **string**<br>Indicates the ID of the cloud provider. |
| `data[].description` | **string**<br>Indicates the description of the cloud provider. |
| `message`  | **string**<br>Indicates the possible reason for the reported error. |

## Errors

The following table lists the errors that the request possibly returns.

| Code  | Message                                                                                 | Possible Reasons                                                                |
|-------|-----------------------------------------------------------------------------------------|---------------------------------------------------------------------------------|
| 80001 | Illegal Api-Key.                                                                        | An anonymous user attempts to use an illegal key to access the OpenAPI service. |
| 80002 | Invalid Api-Key. Please log in to the cloud platform to confirm if your Api-Key exists. | The API key you offer has been deleted or expired.                              |

## Have a try!

Use our API explorer on the side pane to call this API and check the request and responses. Remember to fill in the necessary body parameters below, if applicable.
