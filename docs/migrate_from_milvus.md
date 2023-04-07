---
title: Migrate from Milvus
excerpt: Zilliz Cloud provides a state-of-the-art data infrastructure for optimized search across vector embeddings, making it easy to bring your AI applications to life. As a Milvus user who wants to make the most of this data infrastructure, you are advised to migrate your data to Zilliz Cloud.
category: 642e25fca949170a5eda921e
---

This guide walks you through preparing the migration data, performing the migration, and verifying the results.

## Prepare migration data

Zilliz Cloud allows data migration from Milvus v0.9.x and later versions. As a promising vector database, there are usually drastic changes between its releases.

In this section, you will learn how to:

- [Prepare migration data on Milvus v2.x](#prepare-migration-data-on-milvus-v2x)
- [Prepare migration data on Milvus v1.x](#prepare-migration-data-on-milvus-v1x)

### Prepare migration data on Milvus v2.x

To prepare migration data for Milvus v2.x, do as follows:

1. Download [**milvus-backup**](https://github.com/zilliztech/milvus-backup/releases). Always use the latest release.
2. Create a `configs` folder side by side with the downloaded binary, and download [`backup.yaml`](https://raw.githubusercontent.com/zilliztech/milvus-backup/master/configs/backup.yaml) into the `configs` folder.

    Once the step is done, the structure of your workspace folder should look like this:

    ```
    workspace
    ├── milvus-backup
    └── configs
         └── backup.yaml
    ```

3. Customize `backup.yaml`.

    In normal cases, you do not need to customize this file. But before going on, check whether the following configuration items are correct:

    - `milvus.address`
    - `mivlus.port`
    - `minio.address`
    - `minio.port`
    - `minio.bucketName`
    - `minio.backupBucketName`
    - `rootPath`

    > 📘 Notes
    >
    > - For a Milvus instance installed using Docker Compose, `minio.bucketName` defaults to `a-bucket` and `rootPath` defaults to `files`.
    > - For a Milvus instance installed on Kubernetes, `minio.bucketName` defaults to `milvus-bucket` and `rootPath` defaults to `file`.

4. Create a backup of your Milvus installation.

    ```shell
    ./milvus-backup --config backup.yaml create -n my_backup 
    ```

5. Get the backup file.

    ```shell
    ./milvus-backup --config backup.yaml get -n my_backup
    ```

6. Check the backup files.
    
    - If you set `minio.address` and `minio.port` to an S3 bucket, your backup file are already in the S3 bucket.
    - If you set `minio.address` and `minio.port` to a MinIO bucket, you can download them using Minio Console or the **mc** client. For details on how to download files from MinIO, see [How can I download files from MinIO?](faqs.md#how-can-i-download-files-from-minio).

7. Decompress the downloaded archive and upload only the content of the backup folder to Zilliz Cloud.

    ```
    backup
    └── my_backup  <= **Upload this subfolder**
    ```

### Prepare migration data on Milvus v1.x

To prepare migration data for Milvus v0.9.x through v1.x, you need to

1. Download [**milvus-migration**](https://assets.zilliz.com/tools/milvus-migration). Always use the latest release.
2. Stop the Milvus installation or at least stop performing any DML operations in it.
3. Export the metadata of the installation to `meta.json`.

    - For those installations using MySQL as the backend, run

        ```shell
        ./milvus-migration export -m "user:password@tcp(adderss)/milvus?charset=utf8mb4&parseTime=True&loc=Local" -o outputDir
        ```

    - For those installations using SQLite as the backend, run

        ```shell
        ./milvus-migration export -s /milvus/db/meta.sqlite -o outputDir
        ```

4. Copy the `tables` folder of your Milvus installation, then move both `meta.json` and the `tables` folder to an empty folder. 

    Once this step is done, the structure of the empty folder should look like this:

    ```
    migration_data
    ├── meta.json
    └── tables  
    ```

5. Upload the folder prepared in the preceding step to an S3 block storage bucket or directly use this local folder in the next section.

## Migrate data to Zilliz Cloud

Once the migration data is ready, upload it to Zilliz Cloud.

![Upload_migration_data](https://assets.zilliz.com/zillizCloudDocAssets/upload_migration_data.png)

If you have uploaded the prepared migration data to a personal S3 block storage bucket, select **Import a folder from S3** and fill in the folder path and authentication credentials. For details on the supported URL formats, see [How can I transfer data from AWS S3 to Zilliz Cloud?](faqs.md#How-can-I-transfer-data-from-AWS-S3-to-Zilliz-Cloud) and [How can I transfer data from Google Cloud Storage to Zilliz Cloud?](faqs.md#How-can-I-transfer-data-from-Google-Cloud-Storage-to-Zilliz-Cloud)

To upload a local folder to Zilliz Cloud, select **Import a local folder** and drag the folder to the drop zone. Note that you can upload a local folder of no more than 1 GB to Zilliz Cloud.

## Verify the migration results

After the status of the migration job changes from **MIGRATING** to **SUCCESSFUL**, the migration process ends.

![Verify migration results](https://assets.zilliz.com/zillizCloudDocAssets/verify_migration_results.png)

Zilliz Cloud only supports **AUTO_INDEX**, an optimized indexing algorithm, and will automatically index your migrated collection using this algorithm.  

After loading the collections, you can use the way of your choice to communicate with them.
