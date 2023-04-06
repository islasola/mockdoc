---
title: Zilliz Cloud Limits
excerpt: Find answers to frequently asked questions about the usage of Zilliz Cloud. If you cannot find the answer to you problem here, please contact our support team at <a href="mailto:support@zilliz.com">support@zilliz.com</a>.
category: 642e264dc2653e0058a56246
order: 2
---

#### Why can't I connect to the database after the database is created?

You can identify the problem by following these steps:

1. Check if the database status is **AVAILABLE**. You cannot connect to the database if the database is initializing, deleted, or when its IP whitelist is being updated.
2. Check if the IP address of your connection is included in the IP white list.
3. Test the connectivity of the port by running `telnet in01-<xxx>.<region>.vectordb.zillizcloud.com 19530`.
If the issue remains unsolved after all above steps are tried, please contact our support team at <a href="mailto:support@zilliz.com">support@zilliz.com</a>.

#### What should I know when I set up the IP address white list?

1. You can deploy a group of databases in one project so that you can set a unified IP white list for the group.
2. For the convenience of connection after the database is created, a default IP `0.0.0.0/0` is added to the white list. The default IP can be deleted.
3. Each account has a `Default_project`. You can manage your databases under it if you do not have many databases.
4. The IP white list is project-level. It takes effect on all **AVAILABLE** databases under the project.
5. If a database is changing its status from **STOPPED** to **AVAILABLE**, the IP white list of the project will take effect again.

#### Why can't I delete a project?

1. `Default_project` cannot be deleted.
2. A project with database(s) in it cannot be deleted.
3. You cannot delete a project that does not belong to you.
