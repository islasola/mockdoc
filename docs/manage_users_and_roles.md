---
title: Manage Users and Roles
excerpt: This tutorial guides you through how to manage users and roles.
category: 642e25fca949170a5eda921e
---

In an organization, Zilliz Cloud provides the following types of user roles:

- **Organization owner**: can manage organization settings and users in the organization. For example, you can create an organization, invite or remove a user to or from the organization, edit the roles of users in the organization, and modify organization settings.
- **Organization member**: can access or leave the organization to which you belong and has read-only permissions on organization settings.

This tutorial guides you through how to manage users and roles.

For information on how to manage organizations, refer to [Manage Organizations]().

## Invite a user to an organization

If you are an organization owner, you can take the following steps to invite a user to the organization:

1. Log in to the [Zilliz Cloud console](https://cloud.zilliz.com/login).

2. In the left-side navigation pane of the organization homepage, click **Members**.

3. On the page that appears, click **Invite User** in the upper-right corner.

4. In the **Invite User** dialog box, enter one or more email addresses in **New User(s)**, specify **Organization Role** and **Project Access (Optional)**, and then click **Invite**.

    > 📘 Note
    >
    > If you assign a user with the **Organization Member** role, the user will be granted read-only permissions on the organization, including organization settings and billing, but has no project-level permissions.

![Invite a user]()

You can invite one or more users to an organization at a time. After the preceding operations are performed, Zilliz Cloud sends an invitation email to each user. By accepting the invitation, they can join the organization.

## Modify the role of a user

If you are an organization owner, you can take the following steps to modify the role of another organization member:

1. In the left-side navigation pane of the organization page, click **Members**.

2. Find the target user, click the more icon in the **Actions** column, and then select **Edit Role** from the drop-down list.

    > 📘 Note
    >
    > You can modify the role of a user who is in a **Verified** state only.

3. In the **Edit Role** dialog box, select **Organization Member** or **Organization Owner** as needed and click **Save**.

![Modify the role of a user]()

After the preceding operations are performed, Zilliz Cloud sends an email notifcation to the user whose role has been modified.

## Delete a user

If you are an organization owner, you can revoke invitation from a user in the **Pending** state or remove a user in the **Verified** state from the organization.

### Revoke invitation from a user

When you invite a user to an organization, Zilliz Cloud sends an invitation email to the user. Before accepting invitation, the user is in the **Pending** state. If you want to revoke invitation during the process, take the following steps:

1. In the left-side navigation pane of the organization page, click **Members**.

2. Find the target user who is in the **Pending** state, click the more icon in the **Actions** column, and then select **Revoke Invitation**.

3. In the dialog box that appears, click **Yes** to confirm the operation.

![Revoke invitation]()

After the preceding operations are performed, Zilliz Cloud sends an email notifcation to the user from whom invitation has been revoked.

### Remove a user from an organization

Users who accept invitation to an organization enter the **Verified** state. If a user no longer belongs to an organization, you can take the following steps to remove the user from the organization:

1. In the left-side navigation pane of the organization page, click **Members**.

2. Find the target user who is in the **Verified** state,, click the more icon in the **Actions** column, and then select **Leave** from the drop-down list.

3. In the dialog box that appears, click **Yes** to confirm the operation.

![Remove a user]()

After the preceding operations are performed, Zilliz Cloud sends an email notifcation to the user who has been removed from the organization.

