# Lab 4: Azure Databricks and analyzing files with Databricks

Alice Yang 041200019 CST8921

## Task 1: Upload Data to Azure Data Lake

![alt text](images/image.png)
![alt text](images/image-2.png)
![alt text](images/image-1.png)

## Task 2: Explore Data using Serverless SQL

![alt text](images/image-3.png)
![alt text](images/image-4.png)
![alt text](images/image-5.png)
![alt text](images/image-6.png)

## Task 3: Explore Data using Spark Notebook

![alt text](images/image-7.png)
![alt text](images/image-8.png)
![alt text](images/image-9.png)
![alt text](images/image-10.png)
![alt text](images/image-11.png)

## Task 4: Remove Duplicates

![alt text](images/image-12.png)

## Task 5: Fix Data Types

![alt text](images/image-13.png)

## Task 6: Create Derived Column

![alt text](images/image-14.png)
![alt text](images/image-15.png)

## Task 7: Write Transformed Data to Refined Zone

![alt text](images/image-16.png)
![alt text](images/image-17.png)
![alt text](images/image-18.png)
![alt text](images/image-19.png)

## Task 8: Create External Table using SQL

![alt text](images/image-20.png)
![alt text](images/image-21.png)
![alt text](images/image-22.png)

```SQL
CREATE DATABASE cst8921;

USE cst8921;

CREATE EXTERNAL DATA SOURCE MyDataLake
WITH (
    LOCATION = 'https://cst8921storage.dfs.core.windows.net'
);

CREATE EXTERNAL FILE FORMAT ParquetFormat
WITH (
    FORMAT_TYPE = PARQUET
);

CREATE EXTERNAL TABLE refined_events
WITH (
    LOCATION = 'refined/events_table/',
    DATA_SOURCE = MyDataLake,
    FILE_FORMAT = ParquetFormat
)
AS
SELECT *
FROM OPENROWSET(
    BULK 'https://cst8921storage.dfs.core.windows.net/refined/events/*.parquet',
    FORMAT = 'PARQUET'
) AS data;
```

## Task 9: Analyze & Visualize Data

![alt text](images/image-23.png)

## Task 9: Delete Resources

![alt text](images/image-24.png)