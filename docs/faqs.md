---
title: FAQs
excerpt: Find answers to frequently asked questions about Zilliz Cloud.
category: 642e264dc2653e0058a56246
order: 1
---

### What's the difference between Zilliz Cloud and open-source Milvus?

Zilliz Cloud is Milvus built on the cloud. Zilliz Cloud provides 24 x 365 Premier Support, which will free you from the cost of maintenance.

### In which AWS regions is Zilliz Cloud available?

In the current release, Zilliz Cloud supports the **US West 2** and **US East 2** regions on AWS.

### In which GCP regions is Zilliz Cloud available?

In this current release, Zilliz Cloud supports the **US West 1** region on GCP.

### Which PyMilvus version should I use?

Zilliz Cloud will always upgrade all hosted databases to the latest Milvus version. Therefore, a compatible PyMilvus version is recommended. The following compatibility table specifies the recommended version of Pymilvus for use with a specific version of Milvus.

| Milvus version | Compatible PyMilvus version  |
| ---------------| ---------------------------- |
| 1.0.x          | 1.0.1                        |
| 1.1.x          | 1.1.2                        |
| 2.0.x          | 2.0.2                        |
| 2.1.x          | 2.1.3                        |
| 2.2.x (latest) | 2.2.4                        |

On Zilliz Cloud, you should always use the PyMilvus version that is compatible with the latest Milvus version.

### Which vector database size do I need?

In the current release, a Standard Small database can hold 5,000,000 rows of 128-dimensional vectors. If you need a database with a larger size, please contact us at <a href="mailto:support@zilliz.com">support@zilliz.com</a>.

### Do you provide technical support?

Yes. You can reach us by email to <a href="mailto:support@zilliz.com">support@zilliz.com</a> if you meet any technical difficulties, and we will reach back to you soon.

### Can I use Milvus SDK to connect to Zilliz Cloud database?

Yes. Zilliz Cloud is 100% compatible with PyMilvus and Milvus Java SDK. If you want to use other Milvus SDKs, it is recommended to test them first.

#### Can I upgrade the free trial database to a paid database after expiration?

Zilliz Cloud will automatically provide a 30-day free trial for you when you create the first Standard Small database. If you haven't added a valid payment method, Zilliz will inform you 3 days before the database expires. The free trial database will be upgraded to a paid database automatically after expiration if a valid payment method is added. Otherwise, it will be deleted. If you need multiple databases, type upgrade, or extension of free trial, please contact our support team at <a href="mailto:support@zilliz.com">support@zilliz.com</a>.

### What's the pricing policy of Zilliz Cloud database?

Zilliz Cloud database charges on an hourly basis and incurs bills every month. The expense will be charged from the credit card added to the payment method. 

The hardware resources consist of compute and storage. Compute resource is mainly used for vector search. Zilliz provides resources for vector index building and data write for free.

Zilliz will inform you via your registration email if the payment is unsuccessful. You can solve it by changing your credit card. If the payment is still unsuccessful for 7 days, you will lose the write access to the database. The database will be deleted if the payment is unsuccessful for 9 days.

### What types of AWS S3 URLs are allowed on Zilliz Cloud?

To transfer data from AWS S3 buckets, you can use virtual-host-style URLs, path-style URLs, or URLs with the `S3://` scheme.

- Amazon S3 virtual-hosted-style URLs in the following format:

    ```shell
    https://<bucket-name>.s3.<region-code>.amazonaws.com/<key-name>
    ```

- Amazon S3 path-style URLs in the following format:

    ```shell
    https://s3.<region-code>.amazonaws.com/<bucket-name>/<key-name>
    ```

- URLs using the Amazon S3:// scheme in the following format:

    ```shell
    S3://<bucket-name>/<key-name>
    ```

    You can use URLs of this type only if you need to [bulk-insert data](insert_entities.md#Bulk-insert) from an Amazon S3 bucket.

### What types of Google Cloud Storage URLs are allowed on Zilliz Cloud?

To transfer data from Google Cloud Storage buckets, you can use either of the following:

- A Google Cloud Storage URL in the following format:

    ```shell
    https://storage.cloud.google.com/<bucket-name>/<object-name>
    ```

- A URL using the `gs://` scheme in the following format:

    ```shell
    gs://<bucket-name>/<object-name>
    ```

### How can I download files from MinIO?

You can use either of the following methods to download files from MinIO:

- To download from [MinIO Console](https://min.io/docs/minio/kubernetes/upstream/administration/minio-console.html)

    Log into MinIO Console, locate the bucket specified in `minio.address`, select the files in the bucket, and click **Download** to download them.

- To download using [the **mc** client](https://min.io/docs/minio/linux/reference/minio-mc.html#mc-install), do as follows:

    ```shell
    # configure a Minio host
    mc alias set my_minio https://<minio_endpoint> <accessKey> <secretKey>

    # List the available buckets
    mc ls my_minio

    # Download a file from the bucket
    mc cp --recursive my_minio/<your-bucket-path> <local_dir_path>
    ```
