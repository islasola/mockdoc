---
title: Connect to Cluster
excerpt: This guide walks you through how to access a cluster on Zilliz Cloud. You will learn how to obtain the cluster endpoint, configure the network access whitelist, and connect to a cluster.
category: 642e25b85291100124b05ef4
---

## Before you start

Ensure that

- You have signed up on Zilliz Cloud.
- You have created a cluster.


## Obtain database endpoint

A cluster endpoint exposes the cluster to the public Internet. After creating a vector cluster on Zilliz Cloud, open the cluster page and

1. Obtain the endpoint in the **Cloud Endpoint** section on the **Database Details** tab.
2. View your user name on the **User** tab. 

![Get endpoint](https://assets.zilliz.com/zillizCloudDocAssets/quick-start-get-endpoint.png)

## Connect to a cluster from the Internet

Initiate a connection to the database as follows:

```python
# Run `python3` in your terminal to operate in the Python interactive mode.
from pymilvus import connections

connections.connect(
  alias="default", 
  uri='endpoint', #  Public endpoint obtained from Zilliz Cloud
  secure=True,
  user='user', # Username specified when you created this database 
  password='password' # Password specified when you created this database
)
```

> 📘 Notes
>
> For Milvus users, adjust your connection settings as needed:
>
> - It is recommended that you use the `uri` for endpoints from Zilliz Cloud instead of host and port for Milvus.
> - Because all endpoints available on Zilliz Cloud use TLS/SSL, make sure that you have set `secure` to `True`.
> - Remember to set `user` and `password` to the values specified when you created the cluster.
