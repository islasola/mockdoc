---
title: Set up Maintenance Window
excerpt: You can set up a maintenance window to have Zilliz Cloud schedule maintenance for your hosted database instances, making impactful maintenance events more predictable and less disruptive for your workload. 
category: 642f92917dee450065e34297
order: 2
---

![Set up the maintenance window](https://assets.zilliz.com/zillizCloudDocAssets/setup_maintenance_window.png)

Currently, the maintenance window setting is one of the global settings and applies to all your database instances hosted on Zilliz Cloud.

By default, Zilliz Cloud maintenance policy blocks most impactful updates from 0 AM to 2 PM local time daily to avoid disruptions during typical peak business hours. You will receive a notification in advance for an upcoming maintenance event on a specific day. On that day, Zilliz Cloud takes action during the preferred window hours. 

A maintenance event usually lasts two hours and may cause service interruptions. The default maintenance window is between 2 AM and 4 AM local time. You can adjust the maintenance window by selecting an option in Preferred Time to fit your needs.

You will receive another notification after a maintenance event has finished. Zilliz Cloud also lists the start and end of every maintenance event in Activities for further checks in case you miss the notifications.
