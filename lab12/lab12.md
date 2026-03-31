# Lab 12: Set Up Azure AI Search Index and Deploy Embedding & LLM Models

## Module 1: Provision Azure Resources

### Create a Resource Group

![alt text](images/image.png)

I must deploy in East US 2 due to region restrictions.

### Provision Azure AI Search

![alt text](images/image-1.png)

### Provision Azure OpenAI

![alt text](images/image-2.png)

### Provision Storage Account

![alt text](images/image-3.png)

### Create Storage Container

![alt text](images/image-4.png)

## Module 2: Deploy Embedding and LLM Models

### Open Microsoft Foundry

![alt text](images/image-5.png)

### Deploy Embedding Model

![alt text](images/image-6.png)

### Deploy Chat Model

![alt text](images/image-7.png)

### Env Variables

![alt text](images/image-13.png)
![alt text](images/image-14.png)

## Module 3: Prepare Source Documents

### Upload three policy files into `documents` container in `stsearchlabfiles` Storage Account

![alt text](images/image-9.png)

## Module 4/5: Create the Search Index 

### Azure AI Search -> Add Index (JSON)

![alt text](images/image-10.png)
![alt text](images/image-11.png)

## Module 6: Generate Embeddings and Load Documents

### Install Packages

![alt text](images/image-12.png)

### Env Variables

![alt text](images/image-15.png)

### Run Ingestion Script

![alt text](images/image-31.png)

Implemented in `lab12.py` option 1.

### Search Explorer

![alt text](images/image-17.png)

## Module 7: Run Vector and Hybrid Search Queries

Implemented in `lab12.py` option 2.

### Keyword: "vacation days"

![alt text](images/image-18.png)
![alt text](images/image-25.png)
![alt text](images/image-28.png)

### Vector: "remote work approval"

![alt text](images/image-23.png)
![alt text](images/image-29.png)

### Hybrid: "vacation days" & "remote work approval"

![alt text](images/image-24.png)
![alt text](images/image-30.png)

## Module 8: Add the LLM Layer

### RAG Pipeline - Both Questions

![alt text](images/image-27.png)

Implemented in `lab12.py` option 3.
