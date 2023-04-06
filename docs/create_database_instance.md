---
title: Create Database Instance
excerpt: This guide walks you through the procedures to create a database instance on Zilliz Cloud and the principles of how to choose the proper CU type and decide the total number of CUs in need.
category: 642e25b85291100124b05ef4
---

## Create your database

You can create a database in one of your projects. Upon your first login, a default project has already been created. To create a database instance, you need to specify the database name, the project to which it belongs, cloud providers and cloud regions, CU settings, and database credentials. Currently, Amazon Web Service (AWS) US West, AWS US East, and Google Cloud Platform (GCP) US West are available. Microsoft Azure will be available soon.

![Create your database](https://assets.zilliz.com/zillizCloudDocAssets/create_the_first_database.png)

## How to choose between CUs
 
On Zilliz Cloud, two types of CUs are available. They are high-performance CUs and big-data CUs.

### What are the key differences?

A high-performance CU is optimized for high search performance. It is suitable for low latency or high throughput similarity searches.

A big-data CU is optimized for high storage capacity. It can serve data volume five times larger than the high-performance CU but at the cost of higher search latency.

### How many CUs do you need?

The following table lists the relationship between vector dimensions and the number of vectors a CU can hold. Use it as a reference if you need to calculate the actual number of CUs to accommodate your data.

Note that the recommended numbers in the table are calculated based on the condition that the collection contains only a vector field. For those containing multiple fields, consider making more room (for example, extra 20% CU resources) for your data, according to the collection schema.

| Vector dimensions | Vector counts per capacity-optimized CU (M) | Vector counts per performance-optimized CU (M) |
|-------------------|---------------------------------------------|------------------------------------------------|
| 128               | 25                                          | 5                                              |
| 256               | 14.87                                       | 2.96                                           |
| 512               | 8.22                                        | 1.63                                           |
| 1024              | 4.34                                        | 0.86                                           |
