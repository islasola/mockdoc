---
title: Get Started
slug: get-started-rest
category: 647c078bd6af81043a8430be
---

# Get Started

Zilliz Cloud offers RESTful API for you to manipulate your clusters and data hosted in them. Before you dive in, there are several things that are worth noting:

## Understanding the API endpoints

The RESTful API endpoints fall into the following main categories:

- Cloud API & Cluster endpoints

    These API endpoints involve selecting cloud providers and regions on Zilliz Cloud as well as creating, describing, suspending, and resuming a specific cluster.

    A valid Cloud & Cluster API endpoint always starts with `controller.api.{cloud_region}.zillizcloud.com` with a variable `cloud-region` in it. You can refer to [List Cloud Regions](https://docs.zilliz.com/reference/list-cloud-regions) for the applicable cloud regions.

    The following is the endpoint used to list available cloud providers:

    ```shell
    curl --request GET \
     --url 'https://controller.api.aws-us-west-2.zillizcloud.com/v1/clouds' \
     --header 'Authorization: Bearer <API-Key>' \
     --header 'accept: application/json' \
     --header 'content-type: application/json'
    ```

- Collection & Vector APIs

    These API endpoints involve manipulating collections in a specified cluster as well as the data in a specific collection.

    The prefix of a valid Collection & Vector API endpoint should always be the public or private endpoint of a Zilliz Cloud cluster.

    The following is the API endpoint used to list collections in a cluster.

    ```shell
    curl --request GET \
     --url '${PUBLIC_ENDPOINT}/v1/vector/collections' \
     --header 'Authorization: Bearer <API-Key>' \
     --header 'accept: application/json' \
     --header 'content-type: application/json'
    ```

## Authentication credentials

For serverless clusters, you should always use one of your API key as the only authentication credential for all API endpoints.

For dedicated clusters, there are two types of authentication credentials available:

- API key

    You can use your API key as the authentication method when you use the Cloud or Cluster API endpoints. To obtain an API key, refer to [Manage API Keys](https://docs.zilliz.com/docs/manage-api-keys).

- Token

    You can use a token as the authentication method when you use the Collection or Vector APIs. To obtain a token, you should use a colon (:) to concatenate the username and password that you use to access one of your cluster. For example, `user:password`.

