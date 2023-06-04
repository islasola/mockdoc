# query()

Queries entities that meet specific criteria in a collection.

```python
query(
    collection_name,
    filter,
    output_fields,
    timeout
)
```

## Examples

- Query data in a fixed schema:

    ```python
    from pymilvus import MilvusClient

    client = MilvusClient(uri, token)

    client.query(
        filter='book_id in [2,4,6,8]',
        output_fields=["book_id", "book_intro"] # book_id and book_intro are pre-defined in the schema.
    )
    ```

- Query data in a dynamic schema:

    ```python
    from pymilvus import MilvusClient

    client = MilvusClient(uri, token)
    
    client.query(
        filter='$meta["claps"] > 30 and responses < 10',
        output_fields=["title", "claps", "responses"] # claps and responses are not defined in the schema.
    )
    ```

    The preceding code block shows how to access fields `claps` and `responses` that are not defined in the schema.

## Parameters

| Parameter          | Description                          | Type     | Required |
|--------------------|--------------------------------------|----------|----------|
| `collection_name` | Name of the collection to query. | String | True     |
| `filter` | Filter used to query data. | String | True     |
| `output_fields` | A list of fields to return. If you leave this parameter empty, all fields excluding the vector field will be returned.| list[String] | False    | |
| `timeout` | Maximum time that the method should wait for the operation to complete before raising an exception.| Integer | False    |

## Raises

`ValueError`: Error if the collection is missing.

## Returns

A list of dictionaries, excluding the vector field.