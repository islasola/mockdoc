---
title: Connect to Database
excerpt: This guide walks you through how to access a database on Zilliz Cloud. You will learn how to obtain the database endpoint, configure the network access whitelist, and connect to a database.
category: 642e25b85291100124b05ef4
---

## Before you start

Ensure that

- You have signed up on Zilliz Cloud.
- You have created a vector database.

## Configure the network access whitelist

To make your project publicly accessible from your IP address, you need to add your IP address to the network access list.

1. In the **Summary** section on the **Database Details** tab of a database, click **Go and Configure** on the right of **Network Access** to open the project page.
2. On the **IP Access List** tab, click **Add IP Address**.
3. In the prompted dialog box, click **Submit** or enter the IP address manually in **Network Access (CIDR)**. 
4. Click **Submit** to save the record. Note that you can add a maximum of 20 records to a project.

![Add network access whitelist](https://assets.zilliz.com/zillizCloudDocAssets/add_whitelist.png)

Alternatively, you can access your databases from VPCs through AWS PrivateLink without having your traffic go through the Internet. For details, refer to [Set up a Private Link](setup_private_link).

## Obtain database endpoint

A database endpoint exposes the database to the public Internet. After creating a vector database on Zilliz Cloud, open the database page and

1. Obtain the endpoint in the **Cloud Endpoint** section on the **Database Details** tab.
2. View your user name on the **User** tab. 

![Get endpoint](https://assets.zilliz.com/zillizCloudDocAssets/quick-start-get-endpoint.png)

## Connect to a vector database from the Internet

Initiate a connection to the database as follows:

```Python
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
