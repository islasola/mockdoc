---
title: Manage Snapshots
excerpt: Snapshots are point-of-time backup copies of managed vector databases on Zilliz Cloud. You can use it as a baseline for new databases or just for data backup. This guide demonstrates how you can create a snapshot of a database, restore the snapshot to create a new database, and delete the snapshot if it is no longer needed.  
category: 642e25fca949170a5eda921e
---

## Create a snapshot

Snapshots occur asynchronously. The time spent taking one varies with the size of the database and that of the CU accommodating the database. For a single-collection database holding over 120 million records of 128-dimensional vectors on a 4-CU instance, creating a snapshot takes just about 5 minutes.

You can take a snapshot of your database by referring to the following figure. Your database is still in service while Zilliz Cloud is taking the snapshot.

![Create a snapshot](https://assets.zilliz.com/zillizCloudDocAssets/create_snapshot.png)

You can determine how long Zilliz Cloud keeps your snapshot by setting **Retention Period** in days. The default retention period is currently 7 days, with a maximum of 30 days.

> 📘 Notes
> 
> - Data transfer used to create the snapshots is separately charged at the rate of **$0.025/GB**. For example, a 20 GB snapshot will incur a one-time data transfer charge of **$0.025 x 20 = $0.5**.
> - Currently, a snapshot can live on Zilliz Cloud for up to 30 days free of charge.

## Create a snapshot schedule

Also, you can create a snapshot schedule for a database so that Zilliz Cloud can take regular snapshots.

![Edit a snapshot schedule](https://assets.zilliz.com/zillizCloudDocAssets/edit_snapshot_schedule.png)

A record appears in the **Snapshots** list immediately after a snapshot occurs. However, you will not be able to use the snapshot until its status changes to **AVAILABLE**.

You can cancel any **CREATING** snapshot records at any time. In such a case, its status will change to **CANCELLING** and finally to **CANCELLED**.

## View snapshot details

As soon as you create a snapshot, a snapshot record will be listed with the status of **CREATING**. You can click the name of the snapshot to view its details or click **...** in **Actions** and select **Show collection** to check just the collections included in the snapshot.

![View snapshot details](https://assets.zilliz.com/zillizCloudDocAssets/view_snapshot_details.png)

## Restore a snapshot

You can only restore the snapshots in the **AVAILABLE** state. To restore a snapshot, click **...** in **Actions** and select **Restore database**. 

Then you need to set certain attributes for the database to be restored from the snapshot.

![Restore database](https://assets.zilliz.com/zillizCloudDocAssets/restore_database.png)

While setting these attributes, note that:

- You can restore from a snapshot to create a target database in a different project, but not in a different cloud region.
- You can choose to retain the load status of the collections in the target database.
- You can rename the target database and reset its size and password.

Once you click **Restore** in **Restore Database**, Zilliz Cloud will start creating the target database with the specified attributes and then restore the collections in the snapshot to the target database.

After the status of the target database changes from **CREATING** to **RESTORING**, a record appears in the **Restore History** list of the source database.

![View restore history](https://assets.zilliz.com/zillizCloudDocAssets/view_restore_history.png)

## Delete snapshot

Zilliz Cloud automatically removes the snapshots when they reach the end of their retention period. You can manually delete any available snapshots before then.

![Delete snapshot](https://assets.zilliz.com/zillizCloudDocAssets/delete_snapshot.png)

You will be prompted to verify your request to delete a snapshot before Zilliz Cloud actually performs the deletion.
