# dropCollection()

Drops a specified collection.

> 📘 Note
>
> This method drops all data in a collection.

```Java
R<RpcStatus> dropCollection(DropCollectionParam requestParam);
```

## Examples

```Java
import io.milvus.param.*;

DropCollectionParam dropParam = DropCollectionParam.newBuilder()
        .withCollectionName(collectionName)
        .build();

R<RpcStatus> response = client.dropCollection(dropParam);
if (response.getStatus() != R.Status.Success.getCode()) {
    System.out.println(response.getMessage());
}
```

## DropCollectionParam

Use the `DropCollectionParam.Builder` to construct a `DropCollectionParam` object.

```Java
import io.milvus.param.DropCollectionParam;
DropCollectionParam.Builder builder = DropCollectionParam.newBuilder();
```

Methods of `DropCollectionParam.Builder`:

| Method                                      | Description                                                  | Parameter                                            |
| ------------------------------------------- | ------------------------------------------------------------ | ----------------------------------------------------- |
| `withCollectionName(String collectionName)` | Sets the collection name. The collection name cannot be empty or null. | `collectionName`: The name of the collection to drop. |
| `build()`                                   | Constructs a `DropCollectionParam` object.                    | N/A                                                   |

The `DropCollectionParam.Builder.build()` can throw the following exceptions:

- `ParamException`: error if the parameter is invalid.

## Returns

This method catches all the exceptions and returns an `R<RpcStatus>` object.

- If the API fails on the server side, it returns the error code and message from the server.

- If the API fails by RPC exception, it returns `R.Status.Unknow` and the error message of the exception.

- If the API succeeds, it returns `R.Status.Success`.