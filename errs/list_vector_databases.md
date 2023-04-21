---
title: List Vector Databases
excerpt: Lists all available vector databases.
category: 64368bb63b18090510bad283
---

## Use cases

This endpoint applies to the scenario where you want to get a list of vector databases in a specified cloud region.

## Request

### Parameters

- Query parameters

| Parameter   | Description                                                                                                                         |
|-------------|-------------------------------------------------------------------------------------------------------------------------------------|
| pageSize    | **integer** (Optional)<br>The number of records on each page returned.<br>This parameter ranges from 1 to 100 and defaults to 10.   |
| currentPage | **integer** (Optional)<br>The current page number.<br>This parameter ranges from 1 to the maximum number of pages and defaults to 1 |

No path parameters required

### Body

No request body required

## Response

### Body

- Response body if we process your request successfully

```json
{
   code: 200,
   data: {
      count: 32,
      currentPage: 1,
      pageSize: 10,
      clusters: [
         {
            "clusterId": "in01-840ec44485bf25d",
            "clusterName": "cluster122",
            "description": "abc",
            "regionId": "gcp-us-west1",
            "clusterType": "Performance-Optimized",
            "cuSize": 1,
            "status": "RUNNING",
            "connectAddress": "https://in01-840ec44485bf25d.aws-us-west-2.vectordb.zillizcloud.com:19538",
            "privateLinkAddress": "https://in01-840ec44485bf25d-privatelink.aws-us-west-2.vectordb.zillizcloud.com:19531",
            "createTime": "2023-03-17T12:00:00Z"
         },
         {
            "clusterId": "in01-840ec44485bf25e",
            "clusterName": "cluster123",
            "description": "ffee",
            "regionId": "aws-us-west-2",
            "clusterType": "Capacity-Optimized",
            "cuSize": 1,
            "status": "RUNNING",
            "connectAddress": "https://in01-840ec44485bf25e.aws-us-east-1.vectordb.zillizcloud.com:19538",
            "privateLinkAddress": "https://in01-840ec44485bf25e-privatelink.aws-us-east-1.vectordb.zillizcloud.com:19532",
            "createTime": "2023-03-17T14:00:00Z"
         },
      ]
   }
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
| `data[].regionId` | **string**<br>Indicates the ID of the cloud region. |
| `data[].apiBaseUrl` | **string**<br>Indicates the base URL you should use to access the resources in the corresponding region. |
| `message`  | **string**<br>Indicates the possible reason for the reported error. |

## Errors

The following table lists the errors that the request possibly returns.

| Code  | Message                                                                                 | Possible Reasons                                                                |
|-------|-----------------------------------------------------------------------------------------|---------------------------------------------------------------------------------|
| 80001 | Illegal Api-Key.                                                                        | An anonymous user attempts to use an illegal key to access the OpenAPI service. |
| 80002 | Invalid Api-Key. Please log in to the cloud platform to confirm if your Api-Key exists. | The API key you offer has been deleted or expired.                              |
| 80003 | Invalid CloudId. Please use the ListClouds API to obtain a list of supported CloudIds. | The cloud ID you offer does not exist. |

## Have a try!

Use our API explorer on the side pane to call this API and check the request and responses. Remember to fill in the necessary body parameters below, if applicable.
