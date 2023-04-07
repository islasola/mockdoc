---
title: Example Dataset
excerpt: We'll use an example dataset throughout this user guide series. The dataset contains details about over 5,000 medium articles published between Jan 2020 to August 2020 in prominent publications.
category: 642e25b85291100124b05ef4
---

## Obtain the dataset

This dataset is available in a public S3 storage bucket. 

- For a database deployed on Amazon Web Service (AWS), copy the following S3 URL.

  ```shell
  https://s3.us-west-2.amazonaws.com/publicdataset.zillizcloud.com/medium_articles_2020_dpr/medium_articles_2020_dpr.json
  ```

- For a database deployed on Google Cloud Platform (GCP), copy the following Google Cloud Storage (GCS) URL.

  ```shell
  https://storage.cloud.google.com/publicdataset-zillizcloud-com/medium_articles_2020.json
  ```

To know more about the dataset, read [the introduction page on Kaggle](https://www.kaggle.com/datasets/shiyu22chen/cleaned-medium-articles-dataset). 

## Dataset schema

In the dataset, each data record has eight attributes. Use this table as a reference when you create the schema of your collection.

| Field name   | Type         | Dimension / Max length |
|--------------|--------------|------------------------|
| id           | INT64        | N/A                    |
| title_vector | FLOAT_VECTOR | 768                    |
| title        | VARCHAR      | 512                    |
| link         | VARCHAR      | 512                    |
| reading_time | INT64        | N/A                    |
| publication  | VARCHAR      | 512                    |
| claps        | INT64        | N/A                    |
| responses    | INT64        | N/A                    |