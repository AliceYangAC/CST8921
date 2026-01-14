# Lab 1 – AI and ML (Azure Machine Learning)

## Alice Yang 041200019

## Deploy Azure ML

![alt text](image.png)
I first configured the Azure Machine Learning workspace with the names for the RG `aml-lab-rg` and workspace `aml-lab-workspace` in Canada Central as described in the lab instructions. Afterwards, I deployed the resource to be able to navigate the studio.

## Azure ML Studio Overview

![alt text](image-2.png)
![alt text](image-1.png)

After deploying Azure ML, I opened the studio from the Overview page. Here, I explored the various options in the lefthand bar under Authoring, Assets, and Manage. They allow us to create various ML models, train the models, observe their history, and the various infrastructural requirements to do so.

## Azure ML: Regression - Automobile Price Prediction

![alt text](image-3.png)
![alt text](image-11.png)
![alt text](image-12.png)
![alt text](image-13.png)
![alt text](image-8.png)
![alt text](image-5.png)
![alt text](image-6.png)
![alt text](image-7.png)
![alt text](image-9.png)
![alt text](image-10.png)
![alt text](image-14.png)

I followed the Microsoft Learn tutorial [1] to build the example model for predicting automobile prices based on a cleaned dataset using various Designer components. First, I found the raw automobile dataset component `Automobile price data (Raw)`. It requires preprocessing since it has missing values, which must be cleaned. Therefore, the `Select Columns in Dataset` component helps here by letting us exclude the `normalized-losses` column since it has alot of missing values. Then, the `Clean Missing Data` component lets us clean up the remaining missing data from other columns. Once the raw data is prepared, we can train the data. First, we split it using the `Split Data` component so that we can train the model with part of it and test the model with the other part. Then, we train the data with the `Linear Regression` component, where the algo will construct a model that explores the relationship between the price and the automobile features in the dataset. After training, we use the `Score Model` component to score 30% of the split data using the model trained by the other 70%. Finally, `Evaluate Model` component evaluates how well the model scored the test dataset. We can view those results in the Jobs panel next.

![alt text](image-15.png)
![alt text](image-16.png)
![alt text](image-17.png)
![alt text](image-18.png)
![alt text](image-19.png)
![alt text](image-20.png)
![alt text](image-21.png)
![alt text](image-22.png)
![alt text](image-23.png)
![alt text](image-24.png)

Above shows the details for each complete job run per component in our pipeline. Most interestingly is the results when the model was evaluated by the job `evaluate_model`; Coefficient of Determination: 0.868, Relative Squared Error: 0.132, Mean Absolute Error: 1773.627, Root Mean Squared Error: 2461.696, Relative Absolute Error: 0.389. Each job allows us to view the various output and inputs for the job, its duration, and other details important to track when constructing a pipeline.

## Delete Resources

![alt text](image-25.png)

## References

[1]
likebupt, “Tutorial: Designer - train a no-code regression model - Azure Machine Learning,” learn.microsoft.com, Aug. 02, 2023. https://learn.microsoft.com/en-us/azure/machine-learning/tutorial-designer-automobile-price-train-score?view=azureml-api-1

‌
