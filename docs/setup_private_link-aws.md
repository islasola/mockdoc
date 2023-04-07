---
title: For AWS-hosted Databases
excerpt: Zilliz Cloud offers private access to your AWS-hosted databases through private links in case you do not want to have your database traffic go over the Internet.
category: 642e25fca949170a5eda921e
parentDoc: 642e422d08adbb0051c8ded1
---

## Set up a Private link on Zilliz Cloud

Zilliz Cloud offers you an intuitive wizard to add private links. On the **Private Link** tab in one of your databases or that tab on the **Access and Security** page in one of your projects, click **Add Private Link** to create one in the prompted dialog box.

![Enter VPC ID and subnet IDs](https://assets.zilliz.com/zillizCloudDocAssets/enter_vpc_id_and_subnet_ids.png)

Private Link is a project-level setting. When you create a private link for a database, it applies to its neighboring databases in the same project deployed in the same cloud region.

### Select Cloud Provider and Region for AWS-hosted instances

To create a private link for a database deployed in an AWS region, select **AWS** from the **Cloud Provider** drop-down list.

In **Region**, select the region that accommodates the database you want to access privately.

Currently, a private link applies to databases deployed in AWS US-West-2 and AWS US-East-2. Once you have created a private link in a project, it applies immediately to its member databases that have been deployed in the specified region. For those databases that undergo maintenance then, such as scaling or patch-fixing, the private link applies to them after maintenance.

### Obtain VPC ID

Before creating a VPC endpoint, you need to have a VPC on your Amazon console. To view your VPCs, do as follows:

1. Open the [Amazon VPC console](https://console.aws.amazon.com/vpc/).
2. In the navigation pane, choose **VPCs**.
3. Find the VPC of your desire and copy its ID.
4. Enter this ID in **VPC ID** on Zilliz Cloud.

To create a VPC, refer to [Create a VPC](https://docs.aws.amazon.com/vpc/latest/userguide/working-with-vpcs.html#Create-VPC).

### Obtain subnet ID

Subnets are sub-divisions of your VPC. You need to have a subnet that resides in the same region as the private link to be created. To view your subnets, do as follows:

1. Open the Amazon VPC console at [https://console.aws.amazon.com/vpc/](https://console.aws.amazon.com/vpc/).
2. Change the current region to the one specified for creating the private link.
3. In the navigation pane, choose **Subnets**.
4. Find the subnet of your desire and copy its ID.
5. Enter this ID in **Subnet IDs** on Zilliz Cloud.
To create a subnet, refer to [Create a Subnet in Your VPC](https://docs.aws.amazon.com/vpc/latest/userguide/working-with-subnets.html#create-subnets).

### Obtain VPN endpoint ID

Copy the command generated at the bottom of the **Add Private Link** dialog box on Zilliz Cloud, and run this command in your Amazon CloudShell to create a VPC endpoint.

The returned message is similar to the following:

```shell
{
    "VpcEndpoint": {
        # Copy this and fill it in "Your VPC Private Link ID"
        "VpcEndpointId": "vpce-0ce90d01341533a5c",
        "VpcEndpointType": "Interface",
        ...
        "DnsEntries": [
            {
                # Copy this one and use it as "VPCE_DNS" in the next step.
                "DnsName": "vpce-0ce90d01341533a5c-ngbqfdnj.vpce-svc-0b62964bfd0edfb74.us-west-2.vpce.amazonaws.com",
                "HostedZoneId": "Z1YSA3EXCYUU9Z"
            },
            {
                "DnsName": "vpce-0ce90d01341533a5c-ngbqfdnj-us-west-2a.vpce-svc-0b62964bfd0edfb74.us-west-2.vpce.amazonaws.com",
                "HostedZoneId": "Z1YSA3EXCYUU9Z"
            }
        ]
}
```

In the returned message, copy the ID and DNS name of the created VPC endpoint.

Then, enter the VPC endpoint ID in **Your VPC Private Link ID** and click **Add**.

![Enter VPC endpoint ID](https://assets.zilliz.com/zillizCloudDocAssets/enter_vpc_endpiont_id.png)

### Obtain private link for AWS-hosted instances

After verifying and accepting the VPC endpoint you have submitted, Zilliz Cloud allocates a private link for this endpoint. You can see it in the Database details tab of your database.

## Set up a DNS record

Before you can access your database via the private link allocated by Zilliz Cloud, it is necessary to create a CNAME record in your DNS zone to resolve the private link to the DNS name of your VPC endpoint.

### Create a hosted zone using Amazon Route 53

Amazon Route 53 is a web-based DNS service. Create a hosted DNS zone so that you can add DNS records to it.

Run the following script in your AWS Cloushell to create a hosted DNS zone. Note that you need to set `VPCE_DNS` to the DNS name of your VPC endpoint and `VPC_ID` to the ID of your VPC.

```shell
# Use the value you have copied from the output of the previous step.
# The value is similar to 
# vpce-0ce90d01341533a5c-ngbqfdnj.vpce-svc-0b62964bfd0edfb74.us-west-2.vpce.amazonaws.com
VPCE_DNS=vpce-xxxxxxxx.vpce-svc-xxxxxxxx.<region_name>.vpce.amazonaws.com

ROOT_DNS='vectordb.zillizcloud.com'


# Variable for AWS Region
REGION_ID='us-east-1'

# Variable for VPC ID
VPC_ID='vpc-xxxxxxxxxxxx'


# Create a private Route 53 hosted zone
aws route53 create-hosted-zone \
  --name ${ROOT_DNS} \
  --vpc VPCRegion=${REGION_ID},VPCId=${VPC_ID} \
  --caller-reference $(date +"%s")
```

### Create a CNAME record in the hosted zone

A CNAME record is a type of DNS record that maps an alias name to a true or canonical domain name. Create a CNAME record to map the private link allocated by Zilliz Cloud to the DNS name of your VPC endpoint. Then you can use the private link to access your database privately.

Run the following script in your AWS Cloushell to create a CNAME record in the hosted DNS zone. Note that you need to set `ZONE_ID` to the ID of the hosted DNS zone created in the previous step and `SFC_PL_Data_DNS` to the private link listed on the **Database Details** tab of your database instance.

```shell
# Variable for the hosted zone ID returned in the output for the Route 53 zone
ZONE_ID='/hosted_zone/xxxxxx'

# Variable for PrivateLink DNS hostname.
# Such as in0001-vpcexxxx.aws-us-west-2.vectordb.zillizcloud.com 
SFC_PL_Data_DNS='in0001-vpcexxxx.${REGION_ID}.vectordb.zillizcloud.com '

# Create a CNAME record and modify the Route 53 zone to use it
# Create CNAME records for PrivateLink DNS and then modify the Route 53 zone to use it.
dns_record='{
  "Comment": "Create CNAME records for PrivateLink",
  "Changes": [
    {
      "Action": "CREATE",
      "ResourceRecordSet": {
        "Name": "'${SFC_PL_Data_DNS}'",
        "Type": "CNAME",
        "TTL": 300,
        "ResourceRecords": [
          {
            "Value": "'${VPCE_DNS}'"
          }
        ]
      }
    }
  ]
}'

aws route53 change-resource-record-sets \
  --hosted-zone-id ${ZONE_ID} \
  --change-batch "${dns_record}"
```

## Verify the connection

Once you complete the preceding steps, you can verify the connection as follows:

![Verify the connection](https://assets.zilliz.com/zillizCloudDocAssets/verify_private_link.png)

1. On the **Database Details** tab of a database in concern, click **Private Link** in the **Cloud Endpoint** area.
2. Copy the private link, then click **View the guides to connect your database via endpoint**.

For any issues reported, refer to the troubleshooting guide for reported issues on [AWS-hosted databases](troubleshooting#why-does-it-always-report-name-or-service-not-known-when-i-ping-the-private-link-of-a-gcp-hosted-instance).
