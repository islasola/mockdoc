---
title: About Zilliz Cloud
excerpt: Zilliz Cloud is a fully managed service on the cloud for [LF AI Milvus®](https://milvus.io/), you can set up your Milvus cluster to unlock high-performance similarity search with no extra effort needed for infrastructure management.
category: 642a6f4269ec7e000bba19ca
---

## Why should you choose Zilliz Cloud?

Today’s databases aren’t designed to work with vector embeddings effectively. Milvus is born for vector embeddings, it can scale for billions of vector embeddings.

Zilliz Cloud provides an out-of-box Milvus experience based on a fully managed cloud service, freeing you from the headache of database maintenance.

Zilliz Cloud can deliver surpassingly high performance of over 1000 queries per second (QPS) with very low latency for vector search.

You can choose any size and class of databases and pay for what you have actually used only.

In full consideration of your data security, Zilliz Cloud complies with the SOC 2 standard and will provide Role-Based Access Control (RBAC) for your database soon.

## What are the key features of Zilliz Cloud?

- Core Milvus® features
  - High-performance vector search
  - Low latency
  - Built-in data types filtering
  - Intelligent index auto-optimization 
  - Widely adopted metrics, such as Euclidean Distance (L2) and inner product (IP)
- Compute Units (CUs) optimized for high-performance and big-data search
- Deployed on Amazon Web Service (AWS) US West along with AWS US East, Google Cloud Platform (GCP) US West, and soon on Microsoft Azure
- Scale as your need
- Multiple projects and users
- Multi-factor authentication
- Enhanced security features
- Enterprise support

## Where can vector database help?

- **Image similarity search**

    Images are made searchable and instantaneously return the most similar images from a massive database.

- **Video similarity search**:

    By converting keyframes into vectors and then feeding the results into Milvus, billions of videos can be searched and recommended in near real-time.

- **Audio similarity search**:

    Quickly query massive volumes of audio data such as speech, music, sound effects, and surface similar sounds.

- **Molecular similarity search**:

    Blazing fast similarity search, substructure search, or superstructure search for a specified molecule.

- **Recommender system**:

    Recommend information or products based on user behaviors and needs.

- **Question answering system**:

    Interactive digital QA chatbot that automatically answers user questions.

- **DNA sequence classification**:

    Accurately sort out the classification of a gene in milliseconds by comparing similar DNA sequences.

- **Text search engine**:

    Help users find the information they are looking for by comparing keywords against a database of texts.

- **Anomaly detection**:

    Identify data points, events, and/or observations that deviate from a dataset's normal behavior.

## Zilliz Cloud vs Milvus Community Edition

#### Deployment

|                            | Zilliz Cloud vector database          | Community edition |
|----------------------------|---------------------------------------|-------------------|
| Choice of cloud provider   | AWS, GCP, Azure (coming soon)         | No                |
| Choice of deployment scale | Multiple deployment sizes and classes | Self-managed      |
| Storage                    | Infinite data storage                 | Self-managed      |
| Upgrade and bug fixes      | Effortless                            | Self-managed      |
| Availability               | 99.9%                                 | No guarantee      |

#### Database features

|                           | Zilliz Cloud Vector database                                                                                          | Community edition                                                                                                                                                     |
|---------------------------|-----------------------------------------------------------------------------------------------------------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Vector similarity search  | Yes                                                                                                                   | Yes                                                                                                                                                                   |
| Scalar data types         | <ul><li>INT</li><li>FLOAT</li><li>BOOLEAN</li><li>VARCHAR</li></ul>                                                   | <ul><li>INT</li><li>FLOAT</li><li>BOOLEAN</li><li>VARCHAR</li></ul>                                                                                                   |
| ANNS index                | <ul><li>AUTOINDEX optimized for high-performance searches</li><li>AUTOINDEX optimized for big-data searches</li></ul> | <ul><li>FLAT</li><li>IVF_FLAT</li><li>IVF_SQ8</li><li>IVF_PQ</li><li>HNSW</li><li>ANNOY</li><li>DISKANN</li></ul>                                                     |
| Vector similarity metrics | <ul><li>Euclidean distance (L2)</li><li>Inner product (IP)</li></ul>                                                  | <ul><li>Euclidean distance (L2)</li><li>Inner product (IP)</li><li>Hamming</li> <li>Jaccard</li> <li>Tanimoto</li> <li>Superstructure</li> <li>Substructure</li></ul> |
| Hybrid search             | Yes                                                                                                                   | Yes                                                                                                                                                                   |
| Time travel               | Yes                                                                                                                   | Yes                                                                                                                                                                   |
| Multiple users            | Yes                                                                                                                   | Yes                                                                                                                                                                   |
| Clients                   | Python and Java SDK (fully tested)                                                                                    | Community maintained SDKs                                                                                                                                             |

#### Administrative tools

|     | Zilliz Cloud Vector database | Community edition |
| --- | ---------------------------- | ----------------- |
| GUI | Cloud UI                     | Attu, CLI         |

#### Security control

|                            | Zilliz Cloud Vector database | Community edition |
| -------------------------- | ---------------------------- | ----------------- |
| Data encryption in transit | Yes                          | Yes               |

#### System limits

|                       | Zilliz Cloud Vector database | Community edition |
|-----------------------|------------------------------|-------------------|
| Max connection        | 65,536                       | 65,536            |
| Max collection        | 65,536                       | 65,536            |
| Max vector dimensions | 32,768                       | 32,768            |
| Max topK              | 16,384                       | 16,384            |
| Max nq                | 16,384                       | 16,384            |

#### Request limit

|                         | Zilliz Cloud Vector database | Community edition |
|-------------------------|------------------------------|-------------------|
| Insert size per request | 32MB                         | 512 MB            |
| Search size per request | 32MB                         | 512 MB            |
| Query size per request  | 32MB                         | 512 MB            |

#### Support & services

|                  | Zilliz Cloud Vector database | Community edition |
| ---------------- | ---------------------------- | ----------------- |
| Slack and Email  | Yes                          | Yes               |
| Community forum  | Yes                          | Yes               |
| Priority support | SLA                          | No                |