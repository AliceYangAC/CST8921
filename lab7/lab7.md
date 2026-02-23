# Lab 7: Serverless Computing

Alice Yang 041200019 CST8921

## Phase 1: Infrastructure Setup

**Note: I do not have East US, so I used Canada Central in the lab.**

### Resource Group
![alt text](images/image.png)

### Storage Account
![alt text](images/image-2.png)
![alt text](images/image-1.png)

### Event Hub Namespace & Event Hub

![alt text](images/image-3.png)
![alt text](images/image-4.png)
![alt text](images/image-5.png)
![alt text](images/image-6.png)

### Function App (Consumption)
![alt text](images/image-7.png)
![alt text](images/image-8.png)

### Azure Table Storage
![alt text](images/image-9.png)
![alt text](images/image-10.png)

## Phase 2: Building the Brain -> .NET 8.0 

#### FunctionDWDumper.cs
![alt text](images/image-13.png)

```c#
using Azure.Data.Tables;
using Microsoft.Azure.Functions.Worker;
using Microsoft.Extensions.Logging;
using System.Text.Json;

namespace FunctionDWDumper
{
    public class FunctionDWDumper
    {
        private readonly ILogger<FunctionDWDumper> _logger;

        public FunctionDWDumper(ILogger<FunctionDWDumper> logger)
        {
            _logger = logger;
        }

        [Function("FunctionDWDumper")]
        public async Task Run(
            [EventHubTrigger("turbine-telemetry", Connection = "EventHubConnection", IsBatched = false)] string eventData,
            FunctionContext context)
        {
            _logger.LogInformation($"Event received: {eventData}");

            // Parse the incoming JSON
            var telemetry = JsonSerializer.Deserialize<TelemetryPayload>(eventData,
                new JsonSerializerOptions { PropertyNameCaseInsensitive = true });

            // 2.2 Health scoring rule
            string status = (telemetry.WindSpeed > 15 && telemetry.GeneratedPower < 5)
                ? "URGENT"
                : "HEALTHY";

            // 2.3 Connect to Table Storage and write the row
            string connectionString = Environment.GetEnvironmentVariable("AzureWebJobsStorage");
            var tableClient = new TableClient(connectionString, "TurbineMetrics");
            await tableClient.CreateIfNotExistsAsync();

            var entity = new TableEntity(telemetry.DeviceId, telemetry.Timestamp)
            {
                { "WindSpeed", telemetry.WindSpeed },
                { "GeneratedPower", telemetry.GeneratedPower },
                { "TurbineSpeed", telemetry.TurbineSpeed },
                { "Status", status }
            };

            await tableClient.AddEntityAsync(entity);
            _logger.LogInformation($"Saved: DeviceId={telemetry.DeviceId}, Status={status}");
        }
    }
}
```

### Rule: If WindSpeed > 15 AND GeneratedPower < 5 → Status="URGENT" Else →  Status="HEALTHY"

```c#
string status = (telemetry.WindSpeed > 15 && telemetry.GeneratedPower < 5)
    ? "URGENT"
    : "HEALTHY";
```

### Table Storage Output Binding

```c#
string connectionString = Environment.GetEnvironmentVariable("AzureWebJobsStorage");
var tableClient = new TableClient(connectionString, "TurbineMetrics");
await tableClient.CreateIfNotExistsAsync();

var entity = new TableEntity(telemetry.DeviceId, telemetry.Timestamp)
{
    { "WindSpeed", telemetry.WindSpeed },
    { "GeneratedPower", telemetry.GeneratedPower },
    { "TurbineSpeed", telemetry.TurbineSpeed },
    { "Status", status }
};

await tableClient.AddEntityAsync(entity);
_logger.LogInformation($"Saved: DeviceId={telemetry.DeviceId}, Status={status}");
```

### Entity Model: TurbineMetricEntity.cs
![alt text](images/image-12.png)

```c#
namespace FunctionDWDumper
{
    public class TurbineMetricEntity
    {
        public string PartitionKey { get; set; }
        public string RowKey { get; set; }
        public double WindSpeed { get; set; }
        public double GeneratedPower { get; set; }
        public double TurbineSpeed { get; set; }
        public string Status { get; set; }
    }

    public class TelemetryPayload
    {
        public string DeviceId { get; set; }
        public string Timestamp { get; set; }
        public double WindSpeed { get; set; }
        public double GeneratedPower { get; set; }
        public double TurbineSpeed { get; set; }
    }
}
```

### Function Output Binding: host.json
![alt text](images/image-47.png)

```json
{
    "version": "2.0",
    "logging": {
        "applicationInsights": {
            "samplingSettings": {
                "isEnabled": true,
                "excludedTypes": "Request"
            },
            "enableLiveMetricsFilters": true
        }
    }
}
```

### Function App Settings
![alt text](images/image-22.png)
![alt text](images/image-14.png)
![alt text](images/image-16.png)

Note: all these secrets are deleted so no longer risky.
```json
{
  "IsEncrypted": false,
  "Values": {
    "AzureWebJobsStorage": "Gwl0dE7HM7SE5S7TyfTrXIMWdVk4OVPJR1ZEsDvtPSAEd0ZYihqXcQoSogrSHt2dd83jK/MRhd4X+ASttdpK+Q==",
    "FUNCTIONS_WORKER_RUNTIME": "dotnet-isolated",
    "EventHubConnection": "Endpoint=sb://hubdatamigration-ay-17.servicebus.windows.net/;SharedAccessKeyName=RootManageSharedAccessKey;SharedAccessKey=wiOtnNEUMA4chrIfjQAqWyj8VeZ9pWudV+AEhMC8U/A="
  }
}
```

### Ensure Storage Setting Exists
![alt text](images/image-46.png)

### Checkpoint & Deploy
![alt text](images/image-15.png)
![alt text](images/image-17.png)
![alt text](images/image-19.png)
![alt text](images/image-18.png)

## Phase 3: The Automation Layer

### Create Logic App
![alt text](images/image-20.png)
![alt text](images/image-21.png)

### Build the Workflow
![alt text](images/image-23.png)
![alt text](images/image-34.png)
![alt text](images/image-35.png)
![alt text](images/image-24.png)

Note: As shown above, I could not find any Trigger by searching either "Azure Table Storage → When an entity is added." As a result, I used an HTTP trigger so that when URGENT status is in the result, it hits the URL endpoint to trigger the downstream email processes. Below is additional code I added to the function using the HTTP trigger URL `LogicAppUrl`:

```c#
// If URGENT, call the Logic App
if (status == "URGENT")
{
    string logicAppUrl = Environment.GetEnvironmentVariable("LogicAppUrl");

    var payload = new
    {
        DeviceId = telemetry.DeviceId,
        Timestamp = telemetry.Timestamp,
        WindSpeed = telemetry.WindSpeed,
        GeneratedPower = telemetry.GeneratedPower,
        TurbineSpeed = telemetry.TurbineSpeed,
        Status = status
    };

    var json = JsonSerializer.Serialize(payload);
    var content = new StringContent(json, Encoding.UTF8, "application/json");
    await _httpClient.PostAsync(logicAppUrl, content);
    _logger.LogInformation($"URGENT alert sent to Logic App for DeviceId={telemetry.DeviceId}");
}
```

![alt text](images/image-25.png)
![alt text](images/image-32.png)
![alt text](images/image-33.png)

After setting the new secret `LogicAppUrl` via the CLI, I rebuilt and redeployed the function.

![alt text](images/image-27.png)
![alt text](images/image-28.png)
![alt text](images/image-26.png)
![alt text](images/image-29.png)
![alt text](images/image-30.png)
![alt text](images/image-31.png)

## Phase 4: Live Simulation & Monitoring

### WindTurbineGenerator.py
I made a Python script that functionally does what WindTurbineDataGenerator would do:

```python
import json
import random
import time
from datetime import datetime, timezone
from azure.eventhub import EventHubProducerClient, EventData

# Paste your Event Hub connection string here
CONNECTION_STRING = "Endpoint=sb://hubdatamigration-ay-17.servicebus.windows.net/;SharedAccessKeyName=RootManageSharedAccessKey;SharedAccessKey=wiOtnNEUMA4chrIfjQAqWyj8VeZ9pWudV+AEhMC8U/A="
EVENTHUB_NAME = "turbine-telemetry"

DEVICE_IDS = ["Turbine001", "Turbine002", "Turbine003"]

def generate_telemetry(device_id):
    # Randomly decide if this reading should be URGENT
    # URGENT condition: WindSpeed > 15 AND GeneratedPower < 5
    is_urgent = random.random() < 0.3  # 30% chance of urgent reading

    if is_urgent:
        wind_speed = round(random.uniform(16, 25), 2)      # above 15
        generated_power = round(random.uniform(0.5, 4.9), 2)  # below 5
    else:
        wind_speed = round(random.uniform(5, 15), 2)       # normal range
        generated_power = round(random.uniform(5, 20), 2)  # normal range

    return {
        "DeviceId": device_id,
        "Timestamp": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S"),
        "WindSpeed": wind_speed,
        "GeneratedPower": generated_power,
        "TurbineSpeed": round(random.uniform(10, 60), 2)
    }

def main():
    print("Starting Wind Turbine Data Generator...")
    print("Sending telemetry every 5 seconds. Press Ctrl+C to stop.\n")

    producer = EventHubProducerClient.from_connection_string(
        conn_str=CONNECTION_STRING,
        eventhub_name=EVENTHUB_NAME
    )

    try:
        while True:
            with producer:
                event_data_batch = producer.create_batch()

                for device_id in DEVICE_IDS:
                    telemetry = generate_telemetry(device_id)
                    event_data_batch.add(EventData(json.dumps(telemetry)))
                    
                    status = "URGENT" if (telemetry["WindSpeed"] > 15 and telemetry["GeneratedPower"] < 5) else "HEALTHY"
                    print(f"[{telemetry['Timestamp']}] {device_id} | "
                          f"Wind: {telemetry['WindSpeed']} | "
                          f"Power: {telemetry['GeneratedPower']} | "
                          f"Status: {status}")

                producer.send_batch(event_data_batch)
            
            print("--- Batch sent ---\n")
            time.sleep(5)  # wait 5 seconds between batches

            # Re-create producer for next batch
            producer = EventHubProducerClient.from_connection_string(
                conn_str=CONNECTION_STRING,
                eventhub_name=EVENTHUB_NAME
            )

    except KeyboardInterrupt:
        print("\nGenerator stopped.")

if __name__ == "__main__":
    main()
```
![alt text](images/image-40.png)

### Function Logs
![alt text](images/image-41.png)

### Table Storage Writes
![alt text](images/image-37.png)
![alt text](images/image-38.png)

### Confirm Email Alerts
![alt text](images/image-39.png)
![alt text](images/image-42.png)
![alt text](images/image-43.png)
![alt text](images/image-44.png)

## Phase 5: Delete Resources
![alt text](images/image-45.png)
![alt text](images/image-48.png)