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