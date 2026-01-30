# Lab 3: Cosmos DB Change Feed

Alice Yang 041200019 CST8921

## Azure Cosmos DB for NoSQL

### Create Azure Cosmos DB for NoSQL
![alt text](images/image.png)

### Capacity mode
![alt text](images/image-31.png)

Note: I changed the `Serverless` instructions to `Provisioned thoroughput` using the free 1000 RU, and provisioned the `cosmicworks` database to those free 1000 RU. Otherwise, trying to seed the DB on serverless runs into an authorization error later on when using the `cosmicworks` command line tool. I documented the error later.

### Review keys pane in Cosmos DB
![alt text](images/image-2.png)

### Create database `cosmicworks`
![alt text](images/image-3.png)
![alt text](images/image-4.png)

Here, I also provisioned the database to 1000 RU in my working implementation.

### Create container `products` with partition key `/category/name/`
![alt text](images/image-5.png)

Here I followed instructions and used `/categoryId` for the partition key, but in the end I used `/category/name/` so I was able to seed the database.

### Create container `productslease` with partition key `/partitionKey`
![alt text](images/image-6.png)
![alt text](images/image-7.png)

### Observe `product.cs` class properties
![alt text](images/image-8.png)

### Observe `script.cs` code
![alt text](images/image-9.png)

### Update variable `key` with Azure Cosmos DB key
![alt text](images/image-10.png)

### Update 'script.cs' with provided code
![alt text](images/image-11.png)

This script does the following:

1. Connects to your Cosmos DB account
2. Watches the products container for inserts/updates
3. Uses the productslease container to track progress
4. Prints out every changed document’s ID and name
5. Keeps running until you press a key

It serves as a change feed listener that runs until manually quit.

### Run `script.cs` with `dotnet run`
![alt text](images/image-12.png)
![alt text](images/image-13.png)

### Install `cosmicworks` command line tool 
![alt text](images/image-14.png)

Here, I later updated it to 2.3.1 to work with the other elements like the seeding script.

### Run `cosmicworks` to seed the Azure Cosmos DB database
![alt text](images/image-15.png)
![alt text](images/image-16.png)

If I try to run with the given command in the lab, I run into errors since it tries to populate the employee table by default if you don't specify 0 employees. If I ran it on serverless, I run into the auth error above. I solved the issue by instead running:
```bash
cosmicworks -c "<conn-str>" --number-of-employees 0 --disable-hierarchical-partition-keys
```
### Observe the populated `products` container in the `cosmicworks` database
![alt text](images/image-17.png)

### Verify the changes in `product` and `productlease` containers
![alt text](images/image-18.png)
![alt text](images/image-19.png)

## Azure Cosmos DB-triggered Function 

### Create a Function App
![alt text](images/image-20.png)
![alt text](images/image-30.png)

Azure no longer supports the .NET runtime or script style required in the lab. As a result, I converted the logic to Python 3.12 and moved forward with a Python function.

### Create function with the provided settings (v1)
![alt text](images/image-21.png)
![alt text](images/image-22.png)

### Update contents of `Code + Test` pane in the `__init__.py` and `function.json` files
![alt text](images/image-27.png)
![alt text](images/image-28.png)

Here, I converted the listener logic in the lab from C# to Python and updated the variables to match to properly connect the Cosmos DB trigger to the database. Since it's Python, there is no compilation I have to observe.

### Re-run `cosmicworks` script from earlier to re-seed the `cosmicworks` database in Cosmos DB
![alt text](images/image-26.png)
![alt text](images/image-25.png)

### Observe expanded log output
![alt text](images/image-24.png)

### Delete all resources
![alt text](images/image-29.png)