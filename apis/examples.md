# RESTful API Examples

## List Cloud Providers

Lists all cloud providers available on Zilliz Cloud.

```shell
curl --request GET \
     --url "https://controller.api.${CLOUD_REGION_ID}.zillizcloud.com/v1/clouds" \
     --header "Authorization: Bearer ${API_KEY}" \
     --header "accept: application/json" \
     --header "content-type: application/json"
```

Success response:

```shell
{
    code: 200,
    data: [
     {
        "cloudId": "aws",
        "description": "amazon cloud"
     },
     {
        "cloudId": "gcp",
        "description": "google cloud"
     }
    ]
}
```

## List Cloud Regions

Lists all available cloud regions of a specific cloud provider.

```shell
curl --request GET \
     --url "https://controller.api.${CLOUD_REGION_ID}.zillizcloud.com/v1/regions?cloudId=gcp" \
     --header "Authorization: Bearer ${API_KEY}" \
     --header "accept: application/json" \
     --header "content-type: application/json"
```

You can obtain valid `cloudId` values by performing `ListClouds` operations.

Success response:

```shell
{
    "code": 200,
    "data": [
        {
            "apiBaseUrl": "https://api.gcp-us-west1.zillizcloud.com",
            "cloudId": "gcp",
            "regionId": "gcp-us-west1"
        }
    ]
}
```

## Describe Cluster

Describes the details of a cluster.

```shell
curl --request GET \
     --url "https://controller.api.${CLOUD_REGION_ID}.zillizcloud.com/v1/clusters/<Cluster-ID>" \
     --header "Authorization: Bearer ${API_KEY}" \
     --header "accept: application/json" \
     --header "content-type: application/json"
```

Success response:

```shell
{
    "code": 200,
    "data": {
        "clusterId": "string",
        "clusterName": "string",
        "description": "string",
        "regionId": "string",
        "clusterType": "string",
        "cuSize": "string",
        "status": "string",
        "connectAddress": "string",
        "privateLinkAddress": "string",
        "createTime": "string",
        "storageSize": "string",
        "snapshotNumber": "string",
        "createProgress": "string"
    }
}
```

## Suspend Cluster

Suspends a cluster. This operation will stop the cluster and your data will remain intact.

> 📘 Notes
>
> This applies only to dedicated clusters. You should add a payment method before you can perform this action.

```shell
curl --request POST \ "https://controller.${CLOUD_REGION_ID}.zillizcloud.com/v1/clusters/<Cluster-ID>/suspend" \
     --header "Authorization: Bearer ${API_KEY}" \
     --header "accept: application/json" \
     --header "content-type: application/json"
```

Success response:

```shell
{
  code: 200,
  data: {
     "clusterId": "cluster01",
     "prompt": "Submission successful. Your vector database computing cost is free until you Resume the Cluster, and only storage costs will be charged."
  }
}
```

## Resume Cluster

Resume a cluster that has been suspended.

> 📘 Notes
>
> This applies only to dedicated clusters. You should add a payment method before you can perform this action.

```shell
curl --request POST \ "https://controller.api.${CLOUD_REGION_ID}.zillizcloud.com/v1/clusters/<Cluster-ID>/resume" \
     --header "Authorization: Bearer ${API_KEY}" \
     --header "accept: application/json" \
     --header "content-type: application/json"
```

Success response:

```shell
{
  code: 200,
  data: {
     "clusterId": "cluster01",
     "prompt": "Submission successful. Cluster is currently resuming, which typically takes several minutes. You can use the DescribeCluster interface to obtain the creation progress and the status of the Cluster. When the Cluster's status is RUNNING, you can access your vector database using the SDK."
  }
}
```

## List Clusters

Lists all clusters in a cloud region.

```shell
Request Example:

curl --request GET \
     --url "https://controller.api.${CLOUD_REGION_ID}.zillizcloud.com/v1/clusters?pageSize=&current=" \
     --header "Authorization: Bearer ${API_KEY}" \
     --header "accept: application/json" \
     --header "content-type: application/json"
```

Success response:

```shell
{
    "code": 200,
    "data": {
        "count": 0,
        "currentPage": 1,
        "pageSize": 10,
        "clusters": []
    }
}
```

## Create Collection

Create a collection named `medium_articles`.

> 📘 Notes
>
> For serverless clusters, you should always use an API key as the token.
> For dedicated clusters, you should use your database access credentials separated by a colon (:), such as `user:password`, as the token.

```shell
curl --request POST \
     --url "${CLUSTER_ENDPOINT}/v1/vector/collections/create" \
     --header "Authorization: Bearer ${TOKEN}" \
     --header "accept: application/json" \
     --header "content-type: application/json" \
     -d '{
       "dbName": "default",   
       "collectionName": "medium_articles",
       "dimension": 256,
       "metricType": "L2",
       "primaryField": "id",
       "vectorField": "vector"
      }'
```

Success response:

```shell
{
    "code": 200,
    "data": {}
}
```

## Drop Collection

Drop a collection named `medium_articles`.

> 📘 Notes
>
> For serverless clusters, you should always use an API key as the token.
> For dedicated clusters, you should use your database access credentials separated by a colon (:), such as `user:password`, as the token.

```shell
curl --request POST \
     --url "${CLUSTER_ENDPOINT}/v1/vector/collections/drop" \
     --header "Authorization: Bearer ${TOKEN}" \
     --header "accept: application/json" \
     --header "content-type: application/json" \
     -d '{
        "collectionName": "medium_articles"
      }'
```

Success response:

```shell
{
    "code": 200,
    "data": {}
}
```

## Describe Collection

Describe the details of a collection named `medium_articles`.

> 📘 Notes
>
> For serverless clusters, you should always use an API key as the token.
> For dedicated clusters, you should use your database access credentials separated by a colon (:), such as `user:password`, as the token.

```shell
curl --request GET \
     --url "${CLUSTER_ENDPOINT}/v1/vector/collections/describe?collectionName=medium_articles" \
     --header "Authorization: Bearer ${TOKEN}" \
     --header "accept: application/json" \
     --header "content-type: application/json"
```

Success response:

```shell
{
    "code": 200,
    "data": {
        "collectionName": "string",
        "description": "string",
        "fields": [
            {
                "autoId": true,
                "description": "string",
                "name": "string",
                "primaryKey": true,
                "type": "string"
            }
        ],
        "indexes": [
            {
                "fieldName": "string",
                "indexName": "string",
                "metricType": "string"
            }
        ],
        "load": "string",
        "shardsNum": 0,
        "enableDynamicField": true
    }
}
```

## List Collections

List all collections in a cluster.

> 📘 Notes
>
> For serverless clusters, you should always use an API key as the token.
> For dedicated clusters, you should use your database access credentials separated by a colon (:), such as `user:password`, as the token.

```shell
curl --request GET \
     --url "${CLUSTER_ENDPOINT}/v1/vector/collections" \
     --header "Authorization: Bearer ${TOKEN}" \
     --header "accept: application/json" \
     --header "content-type: application/json"
```

Sample response:

```shell
{
   code: 200,
   data: [
         "collection1",
         "collection2",
         ...
         "collectionN",
         ]
}
```

## Insert

> 📘 Notes
>
> For serverless clusters, you should always use an API key as the token.
> For dedicated clusters, you should use your database access credentials separated by a colon (:), such as `user:password`, as the token.

- Insert an entity to a collection named `medium_articles`.

```shell
curl --request POST \
     --url "${CLUSTER_ENDPOINT}/v1/vector/insert" \
     --header "Authorization: Bearer ${TOKEN}" \
     --header "accept: application/json" \
     --header "content-type: application/json" \
     -d '{
          "collectionName": "medium_articles", 
          "data": { 
               "vector": [0.23254494, 0.01374953, 0.88497432, 0.05292784, 0.02204868, 0.21890409, 0.35428028, 0.97024438, 0.58635726, 0.67980838, 0.67202523, 0.16375636, 0.52829526, 0.80185865, 0.71167799, 0.98615784, 0.86350404, 0.64295726, 0.37624468, 0.99708253, 0.46243643, 0.32893164, 0.32094438, 0.47701896, 0.85275669, 0.13127097, 0.5889451, 0.97648346, 0.74876674, 0.66409428, 0.92279568, 0.59029588, 0.495616, 0.12791323, 0.90082737, 0.84513226, 0.47542935, 0.74928086, 0.44922073, 0.1020575, 0.37431645, 0.29738807, 0.71098564, 0.35390859, 0.87792487, 0.89928066, 0.4995833, 0.61043433, 0.55303136, 0.02036885, 0.02231103, 0.67648899, 0.72165575, 0.15671427, 0.00546115, 0.28756084, 0.15077446, 0.65105982, 0.44063386, 0.07762012, 0.59994796, 0.19935778, 0.58911788, 0.54601686, 0.47097711, 0.90082361, 0.05595469, 0.38546197, 0.91447695, 0.33456871, 0.12778749, 0.82224433, 0.3223666, 0.56243253, 0.72730363, 0.42176339, 0.02008885, 0.11265533, 0.71246733, 0.86685866, 0.5204902, 0.1653007, 0.80375364, 0.14031363, 0.76868394, 0.35325028, 0.1142984, 0.95218926, 0.37508951, 0.01396396, 0.16322817, 0.69052937, 0.30264489, 0.40555134, 0.06153988, 0.00101791, 0.18618961, 0.77599691, 0.3445008, 0.7106463, 0.13440427, 0.64690627, 0.40818622, 0.07025781, 0.89639434, 0.00494204, 0.10540909, 0.47865809, 0.47316137, 0.46836499, 0.93197388, 0.24012326, 0.49471039, 0.21283529, 0.47370547, 0.95777027, 0.50557255, 0.12809693, 0.79998351, 0.76532556, 0.3412945, 0.72270631, 0.3432966, 0.81465781, 0.6924483, 0.2885265, 0.84673871, 0.38711232, 0.18702427, 0.49496971, 0.65431764, 0.39590077, 0.31226873, 0.20910631, 0.86433119, 0.51681312, 0.77759473, 0.42447517, 0.05762998, 0.17887886, 0.41045186, 0.09120965, 0.6447974, 0.49632173, 0.72730052, 0.26646776, 0.48899696, 0.33221734, 0.98206029, 0.82591894, 0.28478645, 0.37324246, 0.35833242, 0.96558445, 0.5003729, 0.66676758, 0.7230707, 0.21599462, 0.70457393, 0.11649283, 0.03034646, 0.00318578, 0.57941155, 0.80640383, 0.30106438, 0.84618622, 0.02321722, 0.6453211, 0.31889303, 0.20069267, 0.19202631, 0.84127804, 0.06014367, 0.53307321, 0.78079442, 0.32043145, 0.30207626, 0.08691769, 0.07230655, 0.8059663, 0.03810803, 0.05415744, 0.44057945, 0.19306693, 0.75747746, 0.89299566, 0.82985846, 0.5958096, 0.89525864, 0.07336388, 0.38396764, 0.04846415, 0.56839423, 0.56106259, 0.14302027, 0.85109589, 0.6298057, 0.62168794, 0.24771729, 0.54924417, 0.9061572, 0.97241046, 0.33025088, 0.56675472, 0.72474551, 0.48314604, 0.26248324, 0.22614522, 0.13087051, 0.9292656, 0.80039537, 0.38300443, 0.78520422, 0.29857615, 0.19121419, 0.47509572, 0.35981825, 0.55131999, 0.04348036, 0.02168964, 0.80645188, 0.62876989, 0.70794394, 0.72093526, 0.85172951, 0.24799777, 0.97620833, 0.74877332, 0.92792629, 0.89200055, 0.74500415, 0.84596926, 0.97469625, 0.7171343, 0.30020491, 0.97313677, 0.241573, 0.15498676, 0.21273237, 0.58910547, 0.46249576, 0.01109894, 0.0180376, 0.80975073, 0.12900483, 0.96509751, 0.57304458, 0.73290638, 0.94211456, 0.35197941, 0.15532272, 0.76150926, 0.19317378, 0.72826792, 0.38820115, 0.94187109],
               "title": "Top 10 In-Demand programming languages to learn in 2020",
               "link": "https://towardsdatascience.com/top-10-in-demand-programming-languages-to-learn-in-2020-4462eb7d8d3e"
          }
     }'
```

- Insert multiple entities.

```shell
curl --request POST \
     --url "${CLUSTER_ENDPOINT}/v1/vector/insert" \
     --header "Authorization: Bearer ${TOKEN}" \
     --header "accept: application/json" \
     --header "content-type: application/json" \
     -d '{
          "collectionName": "medium_articles", 
          "data": [{ 
               "vector": [0.23254494, 0.01374953, 0.88497432, 0.05292784, 0.02204868, 0.21890409, 0.35428028, 0.97024438, 0.58635726, 0.67980838, 0.67202523, 0.16375636, 0.52829526, 0.80185865, 0.71167799, 0.98615784, 0.86350404, 0.64295726, 0.37624468, 0.99708253, 0.46243643, 0.32893164, 0.32094438, 0.47701896, 0.85275669, 0.13127097, 0.5889451, 0.97648346, 0.74876674, 0.66409428, 0.92279568, 0.59029588, 0.495616, 0.12791323, 0.90082737, 0.84513226, 0.47542935, 0.74928086, 0.44922073, 0.1020575, 0.37431645, 0.29738807, 0.71098564, 0.35390859, 0.87792487, 0.89928066, 0.4995833, 0.61043433, 0.55303136, 0.02036885, 0.02231103, 0.67648899, 0.72165575, 0.15671427, 0.00546115, 0.28756084, 0.15077446, 0.65105982, 0.44063386, 0.07762012, 0.59994796, 0.19935778, 0.58911788, 0.54601686, 0.47097711, 0.90082361, 0.05595469, 0.38546197, 0.91447695, 0.33456871, 0.12778749, 0.82224433, 0.3223666, 0.56243253, 0.72730363, 0.42176339, 0.02008885, 0.11265533, 0.71246733, 0.86685866, 0.5204902, 0.1653007, 0.80375364, 0.14031363, 0.76868394, 0.35325028, 0.1142984, 0.95218926, 0.37508951, 0.01396396, 0.16322817, 0.69052937, 0.30264489, 0.40555134, 0.06153988, 0.00101791, 0.18618961, 0.77599691, 0.3445008, 0.7106463, 0.13440427, 0.64690627, 0.40818622, 0.07025781, 0.89639434, 0.00494204, 0.10540909, 0.47865809, 0.47316137, 0.46836499, 0.93197388, 0.24012326, 0.49471039, 0.21283529, 0.47370547, 0.95777027, 0.50557255, 0.12809693, 0.79998351, 0.76532556, 0.3412945, 0.72270631, 0.3432966, 0.81465781, 0.6924483, 0.2885265, 0.84673871, 0.38711232, 0.18702427, 0.49496971, 0.65431764, 0.39590077, 0.31226873, 0.20910631, 0.86433119, 0.51681312, 0.77759473, 0.42447517, 0.05762998, 0.17887886, 0.41045186, 0.09120965, 0.6447974, 0.49632173, 0.72730052, 0.26646776, 0.48899696, 0.33221734, 0.98206029, 0.82591894, 0.28478645, 0.37324246, 0.35833242, 0.96558445, 0.5003729, 0.66676758, 0.7230707, 0.21599462, 0.70457393, 0.11649283, 0.03034646, 0.00318578, 0.57941155, 0.80640383, 0.30106438, 0.84618622, 0.02321722, 0.6453211, 0.31889303, 0.20069267, 0.19202631, 0.84127804, 0.06014367, 0.53307321, 0.78079442, 0.32043145, 0.30207626, 0.08691769, 0.07230655, 0.8059663, 0.03810803, 0.05415744, 0.44057945, 0.19306693, 0.75747746, 0.89299566, 0.82985846, 0.5958096, 0.89525864, 0.07336388, 0.38396764, 0.04846415, 0.56839423, 0.56106259, 0.14302027, 0.85109589, 0.6298057, 0.62168794, 0.24771729, 0.54924417, 0.9061572, 0.97241046, 0.33025088, 0.56675472, 0.72474551, 0.48314604, 0.26248324, 0.22614522, 0.13087051, 0.9292656, 0.80039537, 0.38300443, 0.78520422, 0.29857615, 0.19121419, 0.47509572, 0.35981825, 0.55131999, 0.04348036, 0.02168964, 0.80645188, 0.62876989, 0.70794394, 0.72093526, 0.85172951, 0.24799777, 0.97620833, 0.74877332, 0.92792629, 0.89200055, 0.74500415, 0.84596926, 0.97469625, 0.7171343, 0.30020491, 0.97313677, 0.241573, 0.15498676, 0.21273237, 0.58910547, 0.46249576, 0.01109894, 0.0180376, 0.80975073, 0.12900483, 0.96509751, 0.57304458, 0.73290638, 0.94211456, 0.35197941, 0.15532272, 0.76150926, 0.19317378, 0.72826792, 0.38820115, 0.94187109],
               "title": "Top 10 In-Demand programming languages to learn in 2020",
               "link": "https://towardsdatascience.com/top-10-in-demand-programming-languages-to-learn-in-2020-4462eb7d8d3e"
          },{
               "vector": [0.4882628, 0.85768371, 0.48556888, 0.9681036, 0.94807827, 0.80656861, 0.72123286, 0.81810534, 0.83713905, 0.73258409, 0.97732714, 0.09869599, 0.83189308, 0.33537219, 0.88647192, 0.66132137, 0.703723, 0.34379603, 0.74785059, 0.84559156, 0.65074354, 0.61864253, 0.73546132, 0.84872955, 0.6006182, 0.04830389, 0.37780669, 0.96101751, 0.22319285, 0.88504273, 0.44813016, 0.69746754, 0.5707871, 0.37386075, 0.25382573, 0.42397712, 0.89749552, 0.39729882, 0.38485115, 0.12583234, 0.47243267, 0.74576701, 0.45814588, 0.88024839, 0.72812605, 0.6622232, 0.31803479, 0.74101011, 0.76141925, 0.5024863, 0.47431501, 0.40002184, 0.45752955, 0.54383915, 0.67569667, 0.52164475, 0.33647519, 0.93068322, 0.65766685, 0.95959175, 0.83665213, 0.1753687, 0.27341319, 0.34550907, 0.79669369, 0.95065082, 0.30838918, 0.79784458, 0.37323557, 0.97728813, 0.11170225, 0.87876854, 0.85212036, 0.88599461, 0.76916602, 0.6094099, 0.4427332, 0.87373443, 0.18576099, 0.81970137, 0.74932009, 0.92106027, 0.76417889, 0.35671825, 0.09990157, 0.14570871, 0.43084067, 0.30551776, 0.63985873, 0.45777184, 0.16172334, 0.32226743, 0.27613814, 0.18182943, 0.7019827, 0.45446168, 0.31359211, 0.17426952, 0.19392872, 0.59816543, 0.31679765, 0.60059089, 0.92800561, 0.95165562, 0.55177484, 0.49510178, 0.60250447, 0.1519485, 0.33565446, 0.92865767, 0.86723503, 0.85392181, 0.85337828, 0.01631286, 0.25257909, 0.00124323, 0.59344951, 0.78468014, 0.61854741, 0.61980932, 0.87467147, 0.44361724, 0.97777631, 0.42543721, 0.5290862, 0.12384163, 0.45287003, 0.30333621, 0.10408064, 0.71930918, 0.90741917, 0.09838064, 0.66319033, 0.08133113, 0.30527365, 0.40877414, 0.11552966, 0.76451148, 0.00529968, 0.76741598, 0.90358724, 0.05710312, 0.32659557, 0.66143926, 0.3258203, 0.62721598, 0.18690116, 0.00184847, 0.11355109, 0.33962499, 0.64671448, 0.67297271, 0.02416349, 0.3173442, 0.54041374, 0.33752188, 0.75654937, 0.08236666, 0.40054276, 0.1021504, 0.20874325, 0.75615835, 0.54953906, 0.44659766, 0.16064502, 0.58682242, 0.15547067, 0.57503622, 0.07797247, 0.1559962, 0.94815864, 0.12474807, 0.0999395, 0.85504252, 0.55633022, 0.56959553, 0.75966109, 0.70444125, 0.66884798, 0.81692129, 0.06837097, 0.9714623, 0.86751075, 0.42125912, 0.44367403, 0.49978621, 0.32267559, 0.67220653, 0.56167557, 0.25248436, 0.94191099, 0.71508807, 0.64564731, 0.56824345, 0.29187781, 0.93961505, 0.28196959, 0.92713673, 0.7256734, 0.51042292, 0.81504509, 0.55849401, 0.19380059, 0.46767559, 0.52275063, 0.66075204, 0.97290358, 0.57524932, 0.7219121, 0.85188581, 0.26220385, 0.75686621, 0.51934907, 0.185452, 0.49708297, 0.95783663, 0.61397962, 0.45956795, 0.49311061, 0.49464425, 0.43094667, 0.76768303, 0.29252745, 0.57964633, 0.72950803, 0.94616381, 0.60436868, 0.47828997, 0.90345857, 0.92971537, 0.64784105, 0.18095567, 0.94852017, 0.05224637, 0.50829763, 0.89020778, 0.008269, 0.9500583, 0.20305412, 0.21179052, 0.28443536, 0.39540241, 0.20286982, 0.30968133, 0.2141927, 0.4390286, 0.12686093, 0.59583271, 0.88270185, 0.28187656, 0.90096987, 0.29104497, 0.38480562, 0.40069773, 0.52293091, 0.37621525],
               "title": "Dashboards in Python: 3 Advanced Examples for Dash Beginners and Everyone Else",
               "link": "https://medium.com/swlh/dashboards-in-python-3-advanced-examples-for-dash-beginners-and-everyone-else"
          }]
     }'
```

## Search

> 📘 Notes
>
> For serverless clusters, you should always use an API key as the token.
> For dedicated clusters, you should use your database access credentials separated by a colon (:), such as `user:password`, as the token.

- Search entities based on a given vector.

```shell
curl --request POST \
     --url "${CLUSTER_ENDPOINT}/v1/vector/search" \
     --header "Authorization: Bearer ${TOKEN}" \
     --header "accept: application/json" \
     --header "content-type: application/json" \
     -d '{
        "collectionName": "medium_articles",
        "vector": [0.4882628, 0.85768371, 0.48556888, 0.9681036, 0.94807827, 0.80656861, 0.72123286, 0.81810534, 0.83713905, 0.73258409, 0.97732714, 0.09869599, 0.83189308, 0.33537219, 0.88647192, 0.66132137, 0.703723, 0.34379603, 0.74785059, 0.84559156, 0.65074354, 0.61864253, 0.73546132, 0.84872955, 0.6006182, 0.04830389, 0.37780669, 0.96101751, 0.22319285, 0.88504273, 0.44813016, 0.69746754, 0.5707871, 0.37386075, 0.25382573, 0.42397712, 0.89749552, 0.39729882, 0.38485115, 0.12583234, 0.47243267, 0.74576701, 0.45814588, 0.88024839, 0.72812605, 0.6622232, 0.31803479, 0.74101011, 0.76141925, 0.5024863, 0.47431501, 0.40002184, 0.45752955, 0.54383915, 0.67569667, 0.52164475, 0.33647519, 0.93068322, 0.65766685, 0.95959175, 0.83665213, 0.1753687, 0.27341319, 0.34550907, 0.79669369, 0.95065082, 0.30838918, 0.79784458, 0.37323557, 0.97728813, 0.11170225, 0.87876854, 0.85212036, 0.88599461, 0.76916602, 0.6094099, 0.4427332, 0.87373443, 0.18576099, 0.81970137, 0.74932009, 0.92106027, 0.76417889, 0.35671825, 0.09990157, 0.14570871, 0.43084067, 0.30551776, 0.63985873, 0.45777184, 0.16172334, 0.32226743, 0.27613814, 0.18182943, 0.7019827, 0.45446168, 0.31359211, 0.17426952, 0.19392872, 0.59816543, 0.31679765, 0.60059089, 0.92800561, 0.95165562, 0.55177484, 0.49510178, 0.60250447, 0.1519485, 0.33565446, 0.92865767, 0.86723503, 0.85392181, 0.85337828, 0.01631286, 0.25257909, 0.00124323, 0.59344951, 0.78468014, 0.61854741, 0.61980932, 0.87467147, 0.44361724, 0.97777631, 0.42543721, 0.5290862, 0.12384163, 0.45287003, 0.30333621, 0.10408064, 0.71930918, 0.90741917, 0.09838064, 0.66319033, 0.08133113, 0.30527365, 0.40877414, 0.11552966, 0.76451148, 0.00529968, 0.76741598, 0.90358724, 0.05710312, 0.32659557, 0.66143926, 0.3258203, 0.62721598, 0.18690116, 0.00184847, 0.11355109, 0.33962499, 0.64671448, 0.67297271, 0.02416349, 0.3173442, 0.54041374, 0.33752188, 0.75654937, 0.08236666, 0.40054276, 0.1021504, 0.20874325, 0.75615835, 0.54953906, 0.44659766, 0.16064502, 0.58682242, 0.15547067, 0.57503622, 0.07797247, 0.1559962, 0.94815864, 0.12474807, 0.0999395, 0.85504252, 0.55633022, 0.56959553, 0.75966109, 0.70444125, 0.66884798, 0.81692129, 0.06837097, 0.9714623, 0.86751075, 0.42125912, 0.44367403, 0.49978621, 0.32267559, 0.67220653, 0.56167557, 0.25248436, 0.94191099, 0.71508807, 0.64564731, 0.56824345, 0.29187781, 0.93961505, 0.28196959, 0.92713673, 0.7256734, 0.51042292, 0.81504509, 0.55849401, 0.19380059, 0.46767559, 0.52275063, 0.66075204, 0.97290358, 0.57524932, 0.7219121, 0.85188581, 0.26220385, 0.75686621, 0.51934907, 0.185452, 0.49708297, 0.95783663, 0.61397962, 0.45956795, 0.49311061, 0.49464425, 0.43094667, 0.76768303, 0.29252745, 0.57964633, 0.72950803, 0.94616381, 0.60436868, 0.47828997, 0.90345857, 0.92971537, 0.64784105, 0.18095567, 0.94852017, 0.05224637, 0.50829763, 0.89020778, 0.008269, 0.9500583, 0.20305412, 0.21179052, 0.28443536, 0.39540241, 0.20286982, 0.30968133, 0.2141927, 0.4390286, 0.12686093, 0.59583271, 0.88270185, 0.28187656, 0.90096987, 0.29104497, 0.38480562, 0.40069773, 0.52293091, 0.37621525]
      }'
```

- Search entities and return specific fields.

```shell
curl --request POST \
     --url "${CLUSTER_ENDPOINT}/v1/vector/search" \
     --header "Authorization: Bearer ${TOKEN}" \
     --header "accept: application/json" \
     --header "content-type: application/json" \
     -d '{
       "collectionName": "medium_articles",
       "outputFields": ["id", "title", "link", "distance"],
       "vector": [0.4882628, 0.85768371, 0.48556888, 0.9681036, 0.94807827, 0.80656861, 0.72123286, 0.81810534, 0.83713905, 0.73258409, 0.97732714, 0.09869599, 0.83189308, 0.33537219, 0.88647192, 0.66132137, 0.703723, 0.34379603, 0.74785059, 0.84559156, 0.65074354, 0.61864253, 0.73546132, 0.84872955, 0.6006182, 0.04830389, 0.37780669, 0.96101751, 0.22319285, 0.88504273, 0.44813016, 0.69746754, 0.5707871, 0.37386075, 0.25382573, 0.42397712, 0.89749552, 0.39729882, 0.38485115, 0.12583234, 0.47243267, 0.74576701, 0.45814588, 0.88024839, 0.72812605, 0.6622232, 0.31803479, 0.74101011, 0.76141925, 0.5024863, 0.47431501, 0.40002184, 0.45752955, 0.54383915, 0.67569667, 0.52164475, 0.33647519, 0.93068322, 0.65766685, 0.95959175, 0.83665213, 0.1753687, 0.27341319, 0.34550907, 0.79669369, 0.95065082, 0.30838918, 0.79784458, 0.37323557, 0.97728813, 0.11170225, 0.87876854, 0.85212036, 0.88599461, 0.76916602, 0.6094099, 0.4427332, 0.87373443, 0.18576099, 0.81970137, 0.74932009, 0.92106027, 0.76417889, 0.35671825, 0.09990157, 0.14570871, 0.43084067, 0.30551776, 0.63985873, 0.45777184, 0.16172334, 0.32226743, 0.27613814, 0.18182943, 0.7019827, 0.45446168, 0.31359211, 0.17426952, 0.19392872, 0.59816543, 0.31679765, 0.60059089, 0.92800561, 0.95165562, 0.55177484, 0.49510178, 0.60250447, 0.1519485, 0.33565446, 0.92865767, 0.86723503, 0.85392181, 0.85337828, 0.01631286, 0.25257909, 0.00124323, 0.59344951, 0.78468014, 0.61854741, 0.61980932, 0.87467147, 0.44361724, 0.97777631, 0.42543721, 0.5290862, 0.12384163, 0.45287003, 0.30333621, 0.10408064, 0.71930918, 0.90741917, 0.09838064, 0.66319033, 0.08133113, 0.30527365, 0.40877414, 0.11552966, 0.76451148, 0.00529968, 0.76741598, 0.90358724, 0.05710312, 0.32659557, 0.66143926, 0.3258203, 0.62721598, 0.18690116, 0.00184847, 0.11355109, 0.33962499, 0.64671448, 0.67297271, 0.02416349, 0.3173442, 0.54041374, 0.33752188, 0.75654937, 0.08236666, 0.40054276, 0.1021504, 0.20874325, 0.75615835, 0.54953906, 0.44659766, 0.16064502, 0.58682242, 0.15547067, 0.57503622, 0.07797247, 0.1559962, 0.94815864, 0.12474807, 0.0999395, 0.85504252, 0.55633022, 0.56959553, 0.75966109, 0.70444125, 0.66884798, 0.81692129, 0.06837097, 0.9714623, 0.86751075, 0.42125912, 0.44367403, 0.49978621, 0.32267559, 0.67220653, 0.56167557, 0.25248436, 0.94191099, 0.71508807, 0.64564731, 0.56824345, 0.29187781, 0.93961505, 0.28196959, 0.92713673, 0.7256734, 0.51042292, 0.81504509, 0.55849401, 0.19380059, 0.46767559, 0.52275063, 0.66075204, 0.97290358, 0.57524932, 0.7219121, 0.85188581, 0.26220385, 0.75686621, 0.51934907, 0.185452, 0.49708297, 0.95783663, 0.61397962, 0.45956795, 0.49311061, 0.49464425, 0.43094667, 0.76768303, 0.29252745, 0.57964633, 0.72950803, 0.94616381, 0.60436868, 0.47828997, 0.90345857, 0.92971537, 0.64784105, 0.18095567, 0.94852017, 0.05224637, 0.50829763, 0.89020778, 0.008269, 0.9500583, 0.20305412, 0.21179052, 0.28443536, 0.39540241, 0.20286982, 0.30968133, 0.2141927, 0.4390286, 0.12686093, 0.59583271, 0.88270185, 0.28187656, 0.90096987, 0.29104497, 0.38480562, 0.40069773, 0.52293091, 0.37621525],
       "filter": "id in [443300716234671427, 443300716234671426]",
       "limit": 100,
       "offset": 0
     }'
```

## Query

> 📘 Notes
>
> For serverless clusters, you should always use an API key as the token.
> For dedicated clusters, you should use your database access credentials separated by a colon (:), such as `user:password`, as the token.

Query entities that meet specific conditions.

```shell
curl --request POST \
     --url "${CLUSTER_ENDPOINT}/v1/vector/query" \
     --header "Authorization: Bearer ${TOKEN}" \
     --header "accept: application/json" \
     --header "content-type: application/json" \
     -d '{
       "collectionName": "medium_articles",
       "outputFields": ["id", "title", "link"],
       "filter": "id in [443300716234671427, 443300716234671426]",
       "limit": 100,
       "offset": 0
     }'
```

## Get

> 📘 Notes
>
> For serverless clusters, you should always use an API key as the token.
> For dedicated clusters, you should use your database access credentials separated by a colon (:), such as `user:password`, as the token.

- Get a specified entity whose ID is an integer.

```shell
curl --request POST \
     --url "${CLUSTER_ENDPOINT}/v1/vector/get" \
     --header "Authorization: Bearer ${TOKEN}" \
     --header "accept: application/json" \
     --header "content-type: application/json" \
     -d '{
       "collectionName": "medium_articles",
       "outputFields": ["id", "title", "link"],
       "id": 1
     }'
```

- Get a specified entity whose ID is a string:

```shell
curl --request POST \
     --url "${CLUSTER_ENDPOINT}/v1/vector/get" \
     --header "Authorization: Bearer ${TOKEN}" \
     --header "accept: application/json" \
     --header "content-type: application/json" \
     -d '{
       "collectionName": "medium_articles",
       "outputFields": ["id", "title", "link"],
       "id": "id1"
     }'
```

- Get a list of entities whose IDs are integers:

```shell
curl --request POST \
     --url "${CLUSTER_ENDPOINT}/v1/vector/get" \
     --header "Authorization: Bearer ${TOKEN}" \
     --header "accept: application/json" \
     --header "content-type: application/json" \
     -d '{
       "collectionName": "medium_articles",
       "outputFields": ["id", "title", "link"],
       "id": [1, 2]
     }'
```

- Get a list of entities whose IDs are strings:

```shell
curl --request POST \
     --url "${CLUSTER_ENDPOINT}/v1/vector/get" \
     --header "Authorization: Bearer ${TOKEN}" \
     --header "accept: application/json" \
     --header "content-type: application/json" \
     -d "{
       "collectionName": "medium_articles",
       "outputFields": ["id", "title", "link"],
       "id": ["id1", "id2"]
     }"
```

## Delete

> 📘 Notes
>
> For serverless clusters, you should always use an API key as the token.
> For dedicated clusters, you should use your database access credentials separated by a colon (:), such as `user:password`, as the token.

- Delete a collection whose ID is an integer.

```shell
curl --request POST \
     --url "${CLUSTER_ENDPOINT}/v1/vector/delete" \
     --header "Authorization: Bearer ${TOKEN}" \
     --header "accept: application/json" \
     --header "content-type: application/json" \
     -d '{
       "collectionName": "medium_articles",
       "id": 1
     }'
```

- Delete a collection whose ID is a string.

```shell
curl --request POST \
     --url "${CLUSTER_ENDPOINT}/v1/vector/delete" \
     --header "Authorization: Bearer ${TOKEN}" \
     --header "accept: application/json" \
     --header "content-type: application/json" \
     -d '{
       "collectionName": "medium_articles",
       "id": "id1"
     }'
```

- Delete a list of collections whose IDs are integers.

```shell
curl --request POST \
     --url "${CLUSTER_ENDPOINT}/v1/vector/delete" \
     --header "Authorization: Bearer ${TOKEN}" \
     --header "accept: application/json" \
     --header "content-type: application/json" \
     -d '{
        "collectionName": "medium_articles",
        "id": [1,2,3,4]
      }'
```

- Delete a list of collections whose IDs are strings.

```shell
curl --request POST \
     --url "${CLUSTER_ENDPOINT}/v1/vector/delete" \
     --header "Authorization: Bearer ${TOKEN}" \
     --header "accept: application/json" \
     --header "content-type: application/json" \
     -d '{
        "collectionName": "medium_articles",
        "id": ["id1", "id2", "id3","id4"]
      }'
```

## Import

Imports data from files stored in a specified object storage bucket. Note that the bucket should be in the same cloud as the target cluster of the import.

```shell
curl --request POST \
     --url "https://controller.api.${CLOUD_REGION_ID}.zillizcloud.com/v1/vector/collections/import" \
     --header "Authorization: Bearer ${API_KEY}" \
     --header "accept: application/json" \
     --header "content-type: application/json" \
     -d '{
       "clusterId": "in03-181766e3f9556b7",
       "collectionName": "medium_articles",
       "objectUrl": "gs://publicdataset-zillizcloud-com/medium_articles_2020.json"
       "accessKey": "your-access-key"
       "secretKey": "your-secret-key"
     }'
```

## Get Import Progress

Retrieves the progress of a specified import task.

```shell
curl --request GET \
     --url "https://controller.api.${CLOUD_REGION_ID}.zillizcloud.com/v1/vector/collections/import/get?jobId=${JOBID}&clusterId=${CLUSTERID}" \
     --header "Authorization: Bearer ${API_KEY}" \
     --header "accept: application/json" \
     --header "content-type: application/json" \
```

## List Import Jobs

List all import jobs specific to a cluster.

```shell
curl --request GET \
     --url "https://controller.api.${CLOUD_REGION_ID}.zillizcloud.com/v1/vector/collections/import/list?clusterId=${CLUSTERID}" \
     --header "Authorization: Bearer ${API_KEY}" \
     --header "accept: application/json" \
     --header "content-type: application/json" \
```