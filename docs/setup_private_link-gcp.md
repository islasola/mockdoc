---
title: For GCP-hosted Databases
excerpt: Zilliz Cloud offers private access to your GCP-hosted databases through private links in case you do not want to have your database traffic go over the Internet.
category: 642e25fca949170a5eda921e
---

## Set up a Private Link on Zilliz Cloud

Zilliz Cloud offers you an intuitive wizard to add private links. On the **Private Link** tab in one of your databases or that tab on the **Access and Security** page in one of your projects, click **Add Private Link** to create one in the prompted dialog box.

![Add a private link](https://assets.zilliz.com/zillizCloudDocAssets/enter_vpc_endpoint.png)

Private Link is a project-level setting. When you create a private link for a database, it applies to its neighboring databases in the same project deployed in the same cloud region.

### Select Cloud Provider and Region for GCP-hosted instances

To create a private link for a database deployed in a Google Cloud region, select **Google Cloud** from the **Cloud Provider** drop-down list.

In **Region**, select the region that accommodates the database you want to access privately.

Currently, a private link applies to databases deployed in GCP US-West1. Once you have created a private link in a project, it applies immediately to its member databases that have been deployed in the specified region. For those databases that undergo maintenance then, such as scaling or patch-fixing, the private link applies to them after maintenance.

### Obtain Google Cloud Project ID

1. Open the [Google Cloud Dashboard](https://console.cloud.google.com/home/dashboard).  
2. Find the Project ID of your desire and copy its ID.
3. Enter this ID in Google Cloud Project ID on Zilliz Cloud.

### Obtain VPC Name

Before creating a VPC endpoint, you need to have a VPC on your Amazon console. To view your VPCs, do as follows:

1. Open the [Google Cloud VPC Dashboard](https://console.cloud.google.com/networking/networks/list).  
2. In the navigation pane, choose **VPC networks**.
3. Find the VPC of your desire and copy its Name.
4. Enter this name in **VPC Name** on Zilliz Cloud.

To create a VPC network, refer to [Create and manage VPC networks](https://cloud.google.com/vpc/docs/create-modify-vpc-networks).

### Obtain subnet name

Subnets are sub-divisions of your VPC. You need to have a subnet that resides in the same region as the private link to be created. To view your subnets, do as follows:

1. Open your [VPC network list](https://console.cloud.google.com/networking/networks/list).
2. In the navigation pane, choose **VPC networks**.
3. Click the name of the VPC of your desire.
4. Find the subnet of your desire and copy its name.
5. Enter this name in **Subnet Name** on Zilliz Cloud.

### Set an endpoint prefix

For your convenience, you are required to set an endpoint prefix in **Private Service Connect Endpoint prefix** so that any forwarding rules you create will have this prefix.

### Obtain Private Service Connect endpoint

Copy the command generated at the bottom of the **Add Private Link** dialog box on Zilliz Cloud, and run this command in your GCP CloudShell to create a Private Service Connect Endpoint.

In the returned message, copy the endpoint name listed on [this page](https://console.cloud.google.com/net-services/psc/list/consumers).

Then, enter the copied name in **Your Endpoint** and click **Add**.

### Obtain private link for GCP-hosted instances

After verifying and accepting the preceding attributes you have submitted, Zilliz Cloud allocates a private link for this endpoint. You can see it in the Database details tab of your database.

## Set up firewall rules and a DNS record

Before you can access your database via the private link allocated by Zilliz Cloud, it is necessary to create a CNAME record in your DNS zone to resolve the private link to the DNS name of your VPC endpoint.

### Create firewall rules

To allow private access to your managed database, add appropriate firewall rules. The following snippet shows how to allow traffic through TCP port 22. Note that you need to set `VPC_NAME` to the name of your VPC.

```shell
VPC_NAME={{vpc-name}};

gcloud compute firewall-rules create psclab-iap-consumer --network $VPC_NAME --allow tcp:22 --source-ranges=35.235.240.0/20 --enable-logging
```

### Create a hosted zone using Cloud DNS

Cloud DNS is a web-based DNS service. Create a managed DNS zone so that you can add DNS records to it.

Run the following script in your GCP Cloushell to create a managed DNS zone. Note that you need to set `PROJECT_ID` to your GCP project ID and `PRIVATE_DNS_ZONE_NAME` to `zilliz-privatelink-zone`.

```shell
PROJECT_ID={{project-id}};
PRIVATE_DNS_ZONE_NAME=zilliz-privatelink-zone;

gcloud dns --project=$PROJECT_ID managed-zones create $PRIVATE_DNS_ZONE_NAME --description="" --dns-name="vectordb.zillizcloud.com." --visibility="private" --networks=$VPC_NAME
```

### Create a CNAME record in the hosted zone for GCP-hosted instances

A CNAME record is a type of DNS record that maps an alias name to a true or canonical domain name. Create a CNAME record to map the private link allocated by Zilliz Cloud to the DNS name of your VPC endpoint. Then you can use the private link to access your database privately.

Run the following script in your Cloud Shell to create a CNAME record in the hosted DNS zone. Note that you need to set `ENDPOINT_IP` to the IP address of the endpoint created in the previous step and `PRIVATE_LINK_DOMAIN_PREFIX` to the private link listed on the **Database Details** tab of your database instance.

```shell
PRIVATE_LINK_DOMAIN_SUFFIX=vectordb.zillizcloud.com;
## such as in01-61e949d971f841b-privatelink.gcp-us-west1
PRIVATE_LINK_DOMAIN_PREFIX={{privatelink-domain-prefix}};

## get id from endpoint
ENDPOINT_IP={{endpoint-ip}};

gcloud dns --project=$PROJECT_ID record-sets create $PRIVATE_LINK_DOMAIN_PREFIX.$PRIVATE_LINK_DOMAIN_SUFFIX. --zone="$PRIVATE_DNS_ZONE_NAME" --type="A" --ttl="60" --rrdatas="$ENDPOINT_IP"
```

## Verify the connection

Once you complete the preceding steps, you can verify the connection as follows:

![Verify the connection](https://assets.zilliz.com/zillizCloudDocAssets/verify_private_link.png)

1. On the **Database Details** tab of a database in concern, click **Private Link** in the **Cloud Endpoint** area.
2. Copy the private link, then click **View the guides to connect your database via endpoint**.

For any issues reported, refer to the troubleshooting guide for reported issues on [GCP-hosted instances](troubleshooting#why-does-it-always-report-a-timeout-when-connecting-to-the-private-link-of-an-aws-hosted-instance).
