# delete()

Deletes entities from a collection by primary keys.

```python
delete(
    collection_name,
    id,
    timeout
)
```

## Examples

- Delete an entity by a primary key of a string:

    ```python
    from pymilvus import MilvusClient

    client = MilvusClient(uri, token)

    client.delete(
        collection_name='my-collection1',
        id='pk-1'
    )
    ```

- Delete an entity by a primary key of an integer:

    ```python
    from pymilvus import MilvusClient

    client = MilvusClient(uri, token)

    client.delete(
        collection_name='my-collection2',
        id=256
    )
    ```

- Delete multiple entities by primary keys:

    ```python
    from pymilvus import MilvusClient

    client = MilvusClient(uri, token)

    client.delete(
        collection_name='my-collection3',
        id=['pk-1', 'pk-2']
    )
    ```

## Parameters

| Parameter           | Description                                                                          | Type    | Required |
|---------------------|--------------------------------------------------------------------------------------|---------|----------|
| `collection_name` | Name of the collection from which data is deleted. | String | True    |
| `id` | Primary keys of the entities to delete. | Union[list, str, int] | True    |
| `timeout` | Maximum time that the method should wait for the operation to complete before raising an exception. | Integer | False    |

## Raises

None

## Returns

None