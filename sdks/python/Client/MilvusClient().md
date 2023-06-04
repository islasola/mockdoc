# MilvusClient()

Creates a Milvus client for a cluster.

```python
MilvusClient(
    uri,
    token, # API key or username and password
    timeout
)
```

> 📘 Note
>
> If you’re running a serverless cluster, specify an API key as `token`. If you’re running a dedicated cluster, use `token='user:password'` to establish the connection.

## Examples

- Create a Milvus client for a cluster using an API key:

    ```python
    from pymilvs import MilvusClient

    client = MilvusClient(
    uri='https://<CLUSTER-ID>.<CLOUD-REGION>.vectordb.zillizcloud.com',
    token='<API-KEY>',
    )
    ```

- Create a Milvus client for a cluster using `user` and `password`:

    ```python
    from pymilvs import MilvusClient

    client = MilvusClient(
    uri='https://<CLUSTER-ID>.<CLOUD-REGION>.vectordb.zillizcloud.com:<ACCESS-PORT>',
    token='<USER:PASSWORD>',
    )
    ```

## Parameters

| Parameter          | Description                          | Type     | Required |
|--------------------|--------------------------------------|----------|----------|
| `uri` | Endpoint used to connect to your cluster. | String | True     |
| `token` | Credentials used to connect to your cluster. It can be an API key or a pair of username and password depending on cluster types. | String | True     |
| `timeout` | Maximum time that the method should wait for the operation to complete before raising an exception. | Integer | False     |

## Raises

None

## Returns

A MilvusClient instance.