---
title: Manage Organizations
excerpt: This tutorial guides you through how to manage organizations.
category: 642e25fca949170a5eda921e
---

Zilliz Cloud allows users to create and manage organizations, and each organization can contain one or more projects. By grouping projects under a single organization, it's easy to manage users and permissions across multiple projects. Each project in an organization uses the same billing method, so you don't need to worry about keeping track of multiple billing configurations.

Organizations also allow one or more users to control billing and user permissions for all projects within the organization. This makes it easy to enable access control and ensure that users have the right permissions to perform their tasks.

In an organization, Zilliz Cloud provides the following types of user roles:

- **Organization owner**: can manage organization settings and users in the organization. For example, you can create an organization, invite or remove a user to or from the organization, edit the roles of users in the organization, and modify organization settings.
- **Organization member**: can access or leave the organization to which you belong and has read-only permissions on organization settings.

This tutorial guides you through how to manage organizations.

For information on how to manage users and roles in an organization, refer to [Manage Users and Roles]().

## Create an organization

In default settings, each user can create one organization only. If you have not created an organization yet after signup, you can take the following steps to create one:

1. Log in to the [Zilliz Cloud console](https://cloud.zilliz.com/login).

2. Click **Organization** in the upper-right corner.

3. In the **Create Organization** dialog box, specify **Organization Name**, **Company**, and **Country** and click **Create**.

![Create an organization]()

## Edit organization settings

If you are an organization owner, you can take the following steps to edit organization settings:

1. In the left-side navigation pane of the organization homepage, click **Settings**.

2. On the **Organization Settings** page, click **Edit** in the **Summary**, **Time Zone**, or **System Maintenance Time** card as needed.

3. Modify the settings and click **Confirm**.

![Modify organization settings]()

## Switch between organizations

If you belong to multiple organizations, you can take the following steps to switch between organizations:

1. In the top navigation bar, expand the organization drop-down list in the upper-left corner.

2. Select **View All Organizations** from the drop-down list. All organizations to which you belong will appear.

3. On the page that appears, click the name of the organization you want to view. You'll be redirected to the project list page of the organization.

![Switch between organizations]()

## Leave an organization

If you no longer belong to an organization, you can take the following steps to leave an organization:

1. In the left-side navigation pane, click **Memebers**.

2. Find the target user, click the more icon in the **Actions** column, and then select **Leave** from the drop-down list.

    > 📘 Note
    >
    > If you are an organization owner, you can perform this operation to remove yourself or other users from the organization. However, if you are the unique owner of an organization, you cannot remove yourself from the organization.

3. In the dialog box that appears, click **Yes** to confirm the operation.

![Leave an organization]()