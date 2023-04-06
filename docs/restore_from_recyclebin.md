---
title: Restore from Recycle Bin
excerpt: Recycle bin is a security feature provided by Zilliz Cloud to ensure data security. Every dropped database will find a trace in the recycle bin.
category: 642e25fca949170a5eda921e
---

Zilliz Cloud provides a free 30-day retention period for any database that you drop or that is dropped due to prolonged inactivity during free trials and service suspensions. If you regret dropping a database, you can give it a try to find your data back.

![Recycle bin](https://assets.zilliz.com/zillizCloudDocAssets/recycle_bin.png)

While restoring a database, note that:

- You can restore the database to a different project, but not in a different cloud region.
- You can choose to retain the load status of the collections in the database.
- You can rename the database and reset its size and password.

Once you click **Restore** in **Restore Database**, Zilliz Cloud will start creating the database with the specified attributes and restore your data to the created database.

During restoration, the status of your database will change from **CREATING** to **RESTORING** and finally **RUNNING**. Until then, your lost data will greet you from Zilliz Cloud.
