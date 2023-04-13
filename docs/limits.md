---
title: Limits
excerpt: This page lists some known limitations that users may encounter when using Zilliz Cloud.
category: 642e264dc2653e0058a56246
order: 3
---

## Zilliz Cloud platform

This section lists the limitations of Zilliz Cloud platform.

### Zilliz Cloud account password

- Length: 8 to 128 characters.
- Components: Upper case letters, lower case letters, numbers, and special characters.
- Special characters: `~`, `!`, `@`, `#`, `$`, `%`, `^`, `&`, `*`, `?`, `_`, and `-`.

### Project name

- Length: 1 to 64 characters.
- Components: Upper case letters, lower case letters, numbers, or special characters.

### Database name

- Length: 1 to 32 characters.
- Components: Upper case letters, lower case letters, numbers, or special character `-`.

### Database username

- Length: 2 to 32 characters.
- Components: Lowercase letters, numbers, or special character `_`.
- Starts with a letter, and ends with a letter or a digit.
- Database-level unique.

### Database user password

- Length: 8 to 64 characters.
- Components: Upper case letters, lower case letters, numbers, and special characters.
- Special characters: `!`, `@`, `#`, `$`, `%`, `^`, `&`, `*`, `(`, `)`, `_`, `+`, `-` and `=`.

## Zilliz Cloud database

This section lists the limitations of Zilliz Cloud database.

### Length of a resource name

| Resource        | Limit           |
| --------------- | --------------- |
| Collection      | 255 characters  |
| Field           | 255 characters  |
| Index           | 255 characters  |
| Partition       | 255  characters |

### Naming rules

The name of a resource can contain numbers, letters, dollar signs ($), and underscores (\_). A resource name must start with a letter or an underscore (_).

### Number of resources

| Resource      | Limit       |
| -----------   | ----------- |
| Collections   | 1024        |
| Connection/Proxy | 65535    |

### Data types

| Data type     | Primary Key | Available on Zilliz Cloud |
| ------------- | ----------- | ------------------------- |
| BOOL          | No          | Yes                       |
| INT8          | No          | Yes                       |
| INT16         | No          | Yes                       |
| INT32         | No          | Yes                       |
| INT64         | Yes         | Yes                       |
| FLOAT         | No          | Yes                       |
| DOUBLE        | No          | Yes                       |
| VARCHAR       | Yes         | Yes                       |
| FLOAT_VECTOR  | No          | Yes                       |
| BINARY_VECTOR | No          | No                        |

### Index type

Currently, **AUTOINDEX** is the only index type that databases on Zilliz Cloud support. It is a proprietary index type for index auto-optimization and offers extremely high performance.

### Number of resources in a collection

This table lists the maximum number of corresponding resources per collection.

|              | Shards      | Fields      | Indexes     |
| ------------ | ----------- | ----------- | ----------- |
| 1 CU         | 2           | 64          | 1           |
| 2 CU         | 2           | 64          | 1           |
| 4 CU         | 3           | 64          | 1           |
| 8 CU         | 8           | 64          | 1           |
| 12 CU        | 12          | 64          | 1           |
| 16 CU        | 16          | 64          | 1           |
| 20 CU        | 20          | 64          | 1           |
| 24 CU        | 24          | 64          | 1           |
| 28 CU        | 28          | 64          | 1           |
| 32 CU        | 32          | 64          | 1           |

### String length

This table lists the maximum number of characters a VARCHAR field can hold.

| Data type   | Limit   |
| ----------- | --------|
| VARCHAR     | 65,535  |

### Vector dimensions

This table lists the maximum number of dimensions that a vector field can have.

| Property      | Limit       |
| ------------- | ----------- |
| Dimension     | 32,768      |

### Quota and limits

This table lists the upper limits on the RCP requests of the corresponding operation types that a collection processes per second.

|              | Insert      | Search      | Query       | Delete      |
| ------------ | ----------- | ----------- | ----------- | ----------- |
| 1 CU         | 4 MB/s      | 1 req/s     | 1 req/s     | 0.5 MB/s    |
| 2 CU         | 4 MB/s      | 1 req/s     | 1 req/s     | 0.5 MB/s    |
| 4 CU         | 6 MB/s      | 1 req/s     | 1 req/s     | 0.5 MB/s    |
| 8 CU         | 6 MB/s      | 1 req/s     | 1 req/s     | 0.5 MB/s    |
| 12 CU        | 8 MB/s      | 1 req/s     | 1 req/s     | 0.5 MB/s    |
| 16 CU        | 8 MB/s      | 1 req/s     | 1 req/s     | 0.5 MB/s    |
| 20 CU        | 8 MB/s      | 1 req/s     | 1 req/s     | 0.5 MB/s    |
| 24 CU        | 12 MB/s     | 1 req/s     | 1 req/s     | 0.5 MB/s    |
| 28 CU        | 12 MB/s     | 1 req/s     | 1 req/s     | 0.5 MB/s    |
| 32 CU        | 12 MB/s     | 1 req/s     | 1 req/s     | 0.5 MB/s    |


### Search

| Vectors                                                            | Recommended  |
| ------------------------------------------------------------------ | ------------ |
| <code>topk</code> (number of the most similar results to return)   | 10,000       |
| <code>nq</code> (number of the search requests)                    | 10,000       |

## Zilliz Cloud APIs

You can use Milvus SDK directly to manipulate the databases on Zilliz Cloud. Each managed vector database on Zilliz Cloud has a default user named `db_admin`. This section focuses on the default privileges that this user has, and they are

<table>
    <thead>
        <tr>
            <th rowspan="2" style="vertical-align: middle;">Category</th>
            <th width="30%" rowspan="2" style="vertical-align: middle;">Interface</th>
            <th colspan="2" style="text-align:center;">Privileges</th>
        </tr>
        <tr>
            <th>Zilliz Cloud UI</th>
            <th>SDK</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td rowspan="3" style="vertical-align: middle;">Alias</td>
            <td>AlterAlias</td>
            <td>No</td>
            <td>No</td>
        </tr>
        <tr>
            <td>CreateAlias</td>
            <td>No</td>
            <td>No</td>
        </tr>
        <tr>
            <td>DropAlias</td>
            <td>No</td>
            <td>No</td>
        </tr>
        <tr>
            <td rowspan="4" style="vertical-align: middle;">Authentication</td>
            <td>CreateCredential</td>
            <td>Yes</td>
            <td>No</td>
        </tr>
        <tr>
            <td>DeleteCredential</td>
            <td>Yes</td>
            <td>No</td>
        </tr>
        <tr>
            <td>ListCredUsers</td>
            <td>Yes</td>
            <td>No</td>
        </tr>
        <tr>
            <td>UpdateCredential</td>
            <td>Yes</td>
            <td>No</td>
        </tr>
        <tr>
            <td rowspan="3" style="vertical-align: middle;">Bulk-insert</td>
            <td>BulkInsert</td>
            <td>Yes</td>
            <td>No</td>
        </tr>
        <tr>
            <td>GetBulkInsertState</td>
            <td>Yes</td>
            <td>No</td>
        </tr>
        <tr>
            <td>ListBulkInsertTasks</td>
            <td>Yes</td>
            <td>No</td>
        </tr>
        <tr>
            <td rowspan="15" style="vertical-align: middle;">Collection</td>
            <td>CreateCollection</td>
            <td>Yes</td>
            <td>Yes</td>
        </tr>
        <tr>
            <td>Delete</td>
            <td>No</td>
            <td>Yes</td>
        </tr>
        <tr>
            <td>DescribeCollection</td>
            <td>Yes</td>
            <td>Yes</td>
        </tr> 
        <tr>
            <td>DropCollection</td>
            <td>Yes</td>
            <td>Yes</td>
        </tr> 
        <tr>
            <td>Flush</td>
            <td>No</td>
            <td>Yes</td>
        </tr> 
        <tr>
            <td>GetCollectionStatistics</td>
            <td>No</td>
            <td>Yes</td>
        </tr> 
        <tr>
            <td>GetLoadingProgress</td>
            <td>Yes</td>
            <td>Yes</td>
        </tr> 
        <tr>
            <td>GetPersistentSegmentInfo</td>
            <td>No</td>
            <td>No</td>
        </tr>  
        <tr>
            <td>GetQuerySegmentInfo</td>
            <td>No</td>
            <td>No</td>
        </tr> 
        <tr>
            <td>GetReplicas</td>
            <td>No</td>
            <td>No</td>
        </tr>    
        <tr>
            <td>Insert</td>
            <td>No</td>
            <td>Yes</td>
        </tr> 
        <tr>
            <td>LoadCollection</td>
            <td>Yes</td>
            <td>Yes</td>
        </tr>      
        <tr>
            <td>ReleaseCollection</td>
            <td>Yes</td>
            <td>Yes</td>
        </tr> 
        <tr>
            <td>ShowCollection</td>
            <td>Yes</td>
            <td>Yes</td>
        </tr> 
        <tr>
            <td>GetLoadState</td>
            <td>Yes</td>
            <td>Yes</td>
        </tr> 
        <tr>
            <td rowspan="5" style="vertical-align: middle;">Index</td>
            <td>CreateIndex</td>
            <td>Yes</td>
            <td>Yes</td>
        </tr>
        <tr>
            <td>DescribeIndex</td>
            <td>Yes</td>
            <td>Yes</td>
        </tr> 
        <tr>
            <td>DropIndex</td>
            <td>Yes</td>
            <td>Yes</td>
        </tr> 
        <tr>
            <td>GetIndexBuildProgress</td>
            <td>Yes</td>
            <td>Yes</td>
        </tr> 
        <tr>
            <td>GetIndexState</td>
            <td>Yes</td>
            <td>Yes</td>
        </tr> 
        <tr>
            <td rowspan="6" style="vertical-align: middle;">Management</td>
            <td>GetCompactionState</td>
            <td>No</td>
            <td>No</td>
        </tr>
        <tr>
            <td>GetCompactionStateWithPlan</td>
            <td>No</td>
            <td>No</td>
        </tr> 
        <tr>
            <td>GetFlushState</td>
            <td>No</td>
            <td>Yes</td>
        </tr> 
        <tr>
            <td>GetMetrics</td>
            <td>Yes</td>
            <td>Yes</td>
        </tr> 
        <tr>
            <td>LoadBalance</td>
            <td>No</td>
            <td>No</td>
        </tr> 
        <tr>
            <td>ManualCompact</td>
            <td>No</td>
            <td>Yes</td>
        </tr> 
        <tr>
            <td rowspan="7" style="vertical-align: middle;">Partition</td>
            <td>CreatePartition</td>
            <td>No</td>
            <td>No</td>
        </tr>
        <tr>
            <td>DropPartition</td>
            <td>No</td>
            <td>No</td>
        </tr>  
        <tr>
            <td>GetPartitionStatistics</td>
            <td>No</td>
            <td>No</td>
        </tr>  
        <tr>
            <td>HasPartition</td>
            <td>No</td>
            <td>No</td>
        </tr> 
        <tr>
            <td>LoadPartitions</td>
            <td>No</td>
            <td>No</td>
        </tr> 
        <tr>
            <td>ReleasePartition</td>
            <td>No</td>
            <td>No</td>
        </tr> 
        <tr>
            <td>ShowPartitions</td>
            <td>No</td>
            <td>No</td>
        </tr> 
        <tr>
            <td rowspan="2" style="vertical-align: middle;">Query and Search</td>
            <td>Query</td>
            <td>No</td>
            <td>Yes</td>
        </tr> 
        <tr>
            <td>Search</td>
            <td>Yes</td>
            <td>Yes</td>
        </tr> 
        <tr>
            <td rowspan="10" style="vertical-align: middle;">RBAC</td>
            <td>AddUserToRole</td>
            <td>No</td>
            <td>No</td>
        </tr> 
        <tr>
            <td>CreateRole</td>
            <td>No</td>
            <td>No</td>
        </tr> 
        <tr>
            <td>DropRole</td>
            <td>No</td>
            <td>No</td>
        </tr> 
        <tr>
            <td>GrantRolePrivilege</td>
            <td>No</td>
            <td>No</td>
        </tr>  
        <tr>
            <td>RemoveUserFromRole</td>
            <td>No</td>
            <td>No</td>
        </tr> 
        <tr>
            <td>RevokeRolePrivilege</td>
            <td>No</td>
            <td>No</td>
        </tr>    
        <tr>
            <td>SelectGrantForRole</td>
            <td>No</td>
            <td>No</td>
        </tr>  
        <tr>
            <td>SelectGrantForRoleAndObject</td>
            <td>No</td>
            <td>No</td>
        </tr>
        <tr>
            <td>SelectRole</td>
            <td>No</td>
            <td>No</td>
        </tr>   
        <tr>
            <td>SelectUser</td>
            <td>No</td>
            <td>No</td>
        </tr> 
        <tr>
            <td rowspan="2" style="vertical-align: middle;">System</td>
            <td>GetVersion</td>
            <td>No</td>
            <td>Yes</td>
        </tr>
        <tr>
            <td>CheckHealth</td>
            <td>No</td>
            <td>Yes</td>
        </tr>
    </tbody>
</table>