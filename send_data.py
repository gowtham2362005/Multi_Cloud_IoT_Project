import time
import random
import json
import os
from azure.iot.device import IoTHubDeviceClient, MethodResponse
from google.cloud import pubsub_v1
from dotenv import load_dotenv

load_dotenv()

# --- Credentials ---
AZURE_CONN = os.getenv("CONNECTION_STRING")
GCP_PROJECT_ID = os.getenv("GCP_PROJECT_ID")
GCP_TOPIC_ID = os.getenv("GCP_TOPIC_ID")

# --- 1. Command & Control: Azure Direct Method Handler ---
def azure_method_handler(method_request):
    """Handles incoming commands like 'toggle_light' or 'reboot' from Azure."""
    print(f"\n[COMMAND] Received from Azure: {method_request.name}")
    
    # Logic to handle specific commands
    payload = {"result": "Successfully executed command"}
    status = 200
    
    if method_request.name == "reboot":
        print("Device is rebooting...")
    
    # Send response back to Azure Cloud
    resp = MethodResponse.create_from_method_request(method_request, status, payload)
    azure_client.send_method_response(resp)

# --- 2. Sync Device Twin: Azure Twin Handler ---
def azure_twin_patch_handler(patch):
    """Syncs state changes from Cloud to Device (Twin Sync)."""
    print(f"\n[TWIN SYNC] Received Twin Patch: {patch}")
    # Example: If Azure says 'target_temp': 25, we could sync this to GCP metadata
    # or just acknowledge it here.

def send_telemetry():
    global azure_client
    try:
        # Initialize Azure Client with Handlers
        azure_client = IoTHubDeviceClient.create_from_connection_string(AZURE_CONN)
        azure_client.on_method_request_received = azure_method_handler
        azure_client.on_twin_desired_properties_patch_received = azure_twin_patch_handler
        azure_client.connect()

        # Initialize GCP Publisher
        publisher = pubsub_v1.PublisherClient()
        topic_path = publisher.topic_path(GCP_PROJECT_ID, GCP_TOPIC_ID)

        print("Macha, Device is LIVE and listening for Commands/Twin Sync...")

        while True:
            data = {
                "temperature": round(random.uniform(20.0, 35.0), 2),
                "humidity": round(random.uniform(40.0, 60.0), 2),
                "timestamp": time.time()
            }
            msg_content = json.dumps(data)

            # Telemetry to Azure
            azure_client.send_message(msg_content)
            
            # Telemetry to GCP
            publisher.publish(topic_path, msg_content.encode("utf-8"))
            
            # Update 'Reported' properties in Azure Twin to show current status
            reported_state = {"last_sync": time.ctime(), "status": "online"}
            azure_client.patch_twin_reported_properties(reported_state)

            time.sleep(10)
            
    except KeyboardInterrupt:
        print("Stopped by user.")
    finally:
        azure_client.shutdown()

if __name__ == "__main__":
    send_telemetry()