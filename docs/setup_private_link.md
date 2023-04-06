---
title: Set up Private Link
excerpt: Zilliz Cloud offers private access to your databases through private links in case you do not want to have your database traffic go over the Internet.
category: 642e25fca949170a5eda921e
children: 642e8896f9d4b0003b3deb3d, 642e88960bdbcb00351bc765
---

![Private link principle](https://assets.zilliz.com/zillizCloudDocAssets/private_link_principle.png)

To have your application clients privately access the database instances on Zilliz Cloud, you need to create an endpoint in each of the subnets in your application VPC and register the VPC, subnets, and endpoints with Zilliz Cloud, so that Zilliz Cloud allocates a private link for you to set up a DNS record to map the private link to the endpoints.

This guide walks you through the procedures for

- [Setting up Private link for AWS-hosted instances](setup_private_link-aws.md)
- [Setting up Private link for GCP-hosted instances](setup_private_link-gcp.md)
