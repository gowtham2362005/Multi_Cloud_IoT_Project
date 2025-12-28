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
GCP_SUB_ID = "gowtham-iot-sub" # This matches your main.tf

# --- 1. AZURE HANDLERS (Command & Twin) ---
def azure_method_handler(method_request):
    """Handles Direct Methods (Commands) from Azure Portal"""
    print(f"\n[AZURE COMMAND] Received: {method_request.name}")
    payload = {"result": "Command executed successfully"}
    status = 200
    resp = MethodResponse.create_from_method_request(method_request, status, payload)
    azure_client.send_method_response(resp)

def azure_twin_patch_handler(patch):
    """Syncs Device Twin state from Azure Cloud to Device"""
    print(f"\n[AZURE TWIN SYNC] New settings received: {patch}")

# --- 2. GCP HANDLER (Command & Control) ---
def gcp_callback(message):
    data_str = message.data.decode('utf-8')
    # If the message contains "temperature", it's telemetry, NOT a command
    if "temperature" in data_str:
        message.ack() # Ignore it
        return 
        
    print(f"\n[GCP COMMAND] Received: {data_str}")
    message.ack()

def send_telemetry():
    global azure_client
    try:
        # --- Initialize Azure ---
        azure_client = IoTHubDeviceClient.create_from_connection_string(AZURE_CONN)
        azure_client.on_method_request_received = azure_method_handler
        azure_client.on_twin_desired_properties_patch_received = azure_twin_patch_handler
        azure_client.connect()

        # --- Initialize GCP ---
        publisher = pubsub_v1.PublisherClient()
        topic_path = publisher.topic_path(GCP_PROJECT_ID, GCP_TOPIC_ID)
        
        subscriber = pubsub_v1.SubscriberClient()
        subscription_path = subscriber.subscription_path(GCP_PROJECT_ID, GCP_SUB_ID)
        subscriber.subscribe(subscription_path, callback=gcp_callback)

        print("Device is LIVE. Listening for commands from BOTH Azure and GCP...")

        while True:
            # Generate Data
            data = {
                "temperature": round(random.uniform(20.0, 35.0), 2),
                "humidity": round(random.uniform(40.0, 60.0), 2),
                "timestamp": time.time()
            }
            msg_content = json.dumps(data)

            # Send Telemetry to BOTH
            print(f"Broadcasting: {msg_content}")
            azure_client.send_message(msg_content)
            publisher.publish(topic_path, msg_content.encode("utf-8"))

            # Sync Twin (Reported Property)
            reported_state = {"status": "running", "last_update": time.ctime()}
            azure_client.patch_twin_reported_properties(reported_state)

            time.sleep(10)
            
    except KeyboardInterrupt:
        print("Stopping...")
    finally:
        azure_client.shutdown()

if __name__ == "__main__":
    send_telemetry()