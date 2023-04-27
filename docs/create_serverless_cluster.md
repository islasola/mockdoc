---
title: Create a Serverless Cluster
excerpt: This guide walks you through how to create a serverless cluster on Zilliz Cloud.
category: 
---

To meet diverse business requirements, Zilliz Cloud offers three subscription plans, **Free**, **Standard**, and **Enterprise**. If you're new to vector databases and want to quickly get started, you can try out with the **Free** plan to create a serverless cluster without any charge.

> Note: Due to resource limits, the **Free** plan allows you to create a serverless cluster only on Google Cloud Platform (GCP), and the cluster region and name cannot be modified. If you want to scale cluster resources or create a cluster in a more flexible manner, upgrade to the **Standard** or **Enterprise** plan.

## Create a serverless cluster

To create a serverless cluster, perform the following steps:

1. Log in to the [Zilliz Cloud console](https://cloud.zilliz.com/login).

2. In the left-side navigation pane of the homepage, select a project where you want to create a serverless cluster and click **Create Cluster**.

3. In the first step of the wizard, select **Free** for the subscription plan, retain the default settings of other parameters, and click **Next: Create Collection**.

    > Note: By default, the name of a serverless cluster is **Cluster1**, and you cannot modify it.

4. In the **Create Collection** step, configure parameters for the collection.

    | Parameter    | Description  |
    |--------------|--------------|
    | Name         | The name of the collection.        |
    | Vector Dimension | The vector dimension defined for the collection.  |
    | Metric Type        | The metric type defined for the collection. Valid values: **Euclidean** and **Inner Product**.      |
    | Description (Optional)        | The description of the collection.      |

5. Click **Create Collection and Cluster**. You can view the serverless cluster in the database list after it is created.


## Next steps