import time
import random
import json
import os
from azure.iot.device import IoTHubDeviceClient
from google.cloud import pubsub_v1  # NEW: GCP Library
from dotenv import load_dotenv

load_dotenv()

# --- Azure Credentials ---
AZURE_CONN = os.getenv("CONNECTION_STRING")

# --- NEW: GCP Credentials ---
GCP_PROJECT_ID = os.getenv("GCP_PROJECT_ID")
GCP_TOPIC_ID = os.getenv("GCP_TOPIC_ID")

def send_telemetry():
    try:
        # 1. Initialize Azure Client
        azure_client = IoTHubDeviceClient.create_from_connection_string(AZURE_CONN)
        print("Macha, connecting to Azure...")

        # 2. NEW: Initialize GCP Publisher
        publisher = pubsub_v1.PublisherClient()
        topic_path = publisher.topic_path(GCP_PROJECT_ID, GCP_TOPIC_ID)
        print("Macha, connecting to Google Cloud...")
        
        while True:
            # Generate fake IoT data
            temperature = round(random.uniform(20.0, 35.0), 2)
            humidity = round(random.uniform(40.0, 60.0), 2)
            
            # Prepare the message payload
            data = {
                "temperature": temperature, 
                "humidity": humidity,
                "timestamp": time.time()
            }
            msg_content = json.dumps(data)
            
            # --- BROADCASTING TO BOTH CLOUDS ---
            
            # Send to Azure
            print(f"Sending to Azure: {msg_content}")
            azure_client.send_message(msg_content)
            
            # NEW: Send to GCP (Data must be encoded to bytes)
            print(f"Sending to GCP:   {msg_content}")
            gcp_future = publisher.publish(topic_path, msg_content.encode("utf-8"))
            # gcp_future.result()  # Optional: Wait for GCP to confirm receipt
            
            time.sleep(10) # Wait 10 seconds (standard for student projects)
            
    except KeyboardInterrupt:
        print("Stopped by user.")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        azure_client.shutdown()

if __name__ == "__main__":
    send_telemetry()