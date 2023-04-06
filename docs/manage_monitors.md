---
title: Manage Monitors
excerpt: This guide walks you through the procedures for setting up resource monitors and monitoring database metrics.
category: 642e25fca949170a5eda921e
---

## Set up Resource Monitors

To help ensure that the system is not overloaded and avoid unexpected service termination caused by credit card expiration, Zilliz Cloud provides resource monitors. 

Zilliz Cloud offers four types of monitors. They are the credit card expiration monitor, CU resource monitor, QPS monitor, and query latency monitor. Limits can be set on each of the monitors. When these limits are reached, the resource monitor can trigger email notifications.

These monitors are disabled by default, as shown in the following figure. Click **Resouce Monitors** in the main menu to view, enable, and modify these monitors. 

![setup_monitors](https://assets.zilliz.com/zillizCloudDocAssets/setup_monitors.png)

### Credit card expiration monitor

After you enable the credit card expiration monitor, you will receive a notification once your credit card expires. In this case, you are advised to renew your credit card settings.

### CU resource monitor

To create a new CU resource monitor, you need to set

- Threshold

  Indicates the upper limit of CU usage. The default value is 90.

- Duration

  Indicates a lasting duration in which the CU usage stays above the specified threshold. The default value is 10.

Once the CU usage reaches above the threshold and keeps this state longer than the specified duration, the CU resource monitor will send you a notification. In such cases, you are advised to scale your database with more CUs.

### QPS resource monitor

To create a QPS monitor, you need to set

- Threshold

  Indicates the upper limit of served queries per second. The default value is 10.

- Duration

  Indicates a lasting duration in which the number of served queries stays above the specified threshold. The default value is 10.

Once the number of served queries per second reaches above the threshold and keeps this state longer than the specified duration, the QPS monitor will send you a notification.

### Latency resource monitor

To create a query latency monitor, you need to set

- Threshold

  Indicates the upper limit of query latency in milliseconds. The default value is 90.

- Duration

  Indicates a lasting duration in which query latency stays above the specified threshold. The default value is 10.

Once query latency exceeds the threshold and the time in which query latency stays above the threshold is longer than the specified duration, the query latency monitor will send you a notification. In such cases, you are advised to reduce the number of vectors carried in a bulk search request, check whether your database is overloaded, or check your network conditions.

## Monitor Database Metrics

Zilliz Cloud offers a dashboard for you to view database-specific metrics. You can find it on the **Overview** tab of the database details page, as shown in the following figure.

![dashboard_metrics](https://assets.zilliz.com/zillizCloudDocAssets/dashboard_metrics.png)

- CU

  Indicates the CU resources consumed by your vector database in percentage.

- Storage

  Indicates the size of the storage in use.

- QPS

  Indicates the number of served queries per second.

- Query latency

  Indicate the average latency of served queries.