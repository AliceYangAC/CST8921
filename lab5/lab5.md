# Lab 5: Serverless Computing

Alice Yang 041200019 CST8921

## Task A1 - Create Storage Account

![alt text](images/image.png)
![alt text](images/image-1.png)

## Task A2 - Create Blob Container

![alt text](images/image-2.png)
![alt text](images/image-3.png)

## Task B1 - Create Function App

![alt text](images/image-4.png)
![alt text](images/image-5.png)
![alt text](images/image-6.png)

## Task B2 - Create Function

![alt text](images/image-7.png)
![alt text](images/image-9.png)
![alt text](images/image-8.png)

## Task C1 - Create Event Subscription

![alt text](images/image-10.png)
![alt text](images/image-11.png)
![alt text](images/image-12.png)

## Task D1 - Update Function Code

![alt text](images/image-13.png)

## Task D2 - Verify Function Settings

![alt text](images/image-14.png)
![alt text](images/image-15.png)

## Task E1 - Create Sample Data File

![alt text](images/image-16.png)

## Task E2 - Upload File

![alt text](images/image-17.png)
![alt text](images/image-18.png)

## Task F1 - Confirm Function Invocation

![alt text](images/image-20.png)
![alt text](images/image-19.png)
![alt text](images/image-23.png)

Below is the modified code to work with modern v2 Event Grid Trigger.
```
import logging
import urllib.request
import azure.functions as func

app = func.FunctionApp()

@app.event_grid_trigger(arg_name="azeventgrid")
def ProcessBlobUpload(azeventgrid: func.EventGridEvent):
    logging.info("Event Grid v2 trigger received")

    data = azeventgrid.get_json()
    blob_url = data["url"]
    logging.info(f"Blob URL: {blob_url}")

    with urllib.request.urlopen(blob_url) as response:
        blob_content = response.read().decode("utf-8")

    logging.info("Blob content retrieved successfully")
    logging.info(blob_content)
```

## Task F2 - View Logs (Blob Content)

![alt text](images/image-22.png)

## Task G - Cleanup

![alt text](images/image-24.png)