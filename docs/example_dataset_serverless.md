---
title: Example Dataset
excerpt: We'll use an example dataset throughout this user guide series. The dataset contains details about 100 titles and their vector representations.
category: 644ba9105afa34006010ac54
---

## Obtain the dataset

This dataset is available in a public S3 storage bucket. 

- For a database deployed on Amazon Web Service (AWS), copy the following S3 URL.

  ```shell
  
  ```

- For a database deployed on Google Cloud Platform (GCP), copy the following Google Cloud Storage (GCS) URL.

  ```shell
  
  ```

## Dataset schema

In the dataset, each data record has three attributes. Use this table as a reference when you create the schema of your collection.

| Field name   | Type         | Dimension / Max length |
|--------------|--------------|------------------------|
| id           | INT64        | N/A                    |
| title_vector | FloatVector  | 384                    |
| title        | VARCHAR      | N/A                    |