---
title: Troubleshootings
excerpt: Find answers to frequently asked questions about the usage of Zilliz Cloud. If you cannot find the answer to you problem here, please contact our support team at <a href="mailto:support@zilliz.com">support@zilliz.com</a>.
category: 642e264dc2653e0058a56246
order: 2
---

### Why can't I connect to the database after the database is created?

You can identify the problem by following these steps:

1. Check if the database status is **AVAILABLE**. You cannot connect to the database if the database is initializing, deleted, or when its IP whitelist is being updated.
2. Check if the IP address of your connection is included in the IP white list.
3. Test the connectivity of the port by running `telnet in01-<xxx>.<region>.vectordb.zillizcloud.com 19530`.
If the issue remains unsolved after all above steps are tried, please contact our support team at <a href="mailto:support@zilliz.com">support@zilliz.com</a>.

### What should I know when I set up the IP address white list?

1. You can deploy a group of databases in one project so that you can set a unified IP white list for the group.
2. For the convenience of connection after the database is created, a default IP `0.0.0.0/0` is added to the white list. The default IP can be deleted.
3. Each account has a `Default_project`. You can manage your databases under it if you do not have many databases.
4. The IP white list is project-level. It takes effect on all **AVAILABLE** databases under the project.
5. If a database is changing its status from **STOPPED** to **AVAILABLE**, the IP white list of the project will take effect again.

### Why can't I delete a project?

1. `Default_project` cannot be deleted.
2. A project with database(s) in it cannot be deleted.
3. You cannot delete a project that does not belong to you.

### Why does it always report `Name or service not known` when I ping the private link of a GCP-hosted instance?

Check your DNS settings by referring to [Set up firewall rules and a DNS record](setup_private_link.md#set-up-firewall-rules-and-a-dns-record).

- If the configuration is correct, when you ping your private link, you should see

![Succeeded in resolving the private link](https://assets.zilliz.com/zillizCloudDocAssets/private_link_gcp_ts_01.png)

- If the configuration is incorrect, when you ping your private link, you may see 

![Failed to resolve the private link](https://assets.zilliz.com/zillizCloudDocAssets/private_link_gcp_ts_02.png)

### Why does it always report a timeout when connecting to the private link of an AWS-hosted instance?

A timeout usually occurs for the following reasons:

- No private DNS records exist.

    If a DNS record exists, you can ping the private link as follows:

    ![A normal `ping` test](https://assets.zilliz.com/zillizCloudDocAssets/private_link_ts_1.png)

    If you see the following, you need to [set up the DNS record](setup_private_link.md#create-a-cname-record-in-the-hosted-zone).

    ![A failed `ping` test](https://assets.zilliz.com/zillizCloudDocAssets/private_link_ts_2.png)

- No or invalid security group rules exist.

    You need to properly set the security group rules for the traffic from your EC2 instance to your VPC endpoint in the AWS console. A proper security group within your VPC should allow inbound access from your EC2 instances on the port suffixed to your private link.

    You can use a `curl` command to test the connectivity of the private link. In a normal case, it returns a 400 response.

    ![A normal `curl` connectivity test](https://assets.zilliz.com/zillizCloudDocAssets/private_link_ts_3.png)

    If the `curl` command hangs without any response as in the following screenshot, you need to set up proper security group rules by referring to step 9 in [Create a VPC endpoint](https://docs.amazonaws.cn/en_us/vpc/latest/privatelink/create-interface-endpoint.html).

    ![A hung `curl` connectivity test](https://assets.zilliz.com/zillizCloudDocAssets/private_link_ts_4.png)
