Multi-Cloud IoT Device Management
Azure IoT Hub & GCP Pub/Sub Integration

This project demonstrates a multi-cloud IoT architecture where a single device (simulated via Python) communicates with both Microsoft Azure and Google Cloud Platform (GCP). It implements bi-directional communication, state synchronization, and remote command execution.

🚀 Features
Infrastructure as Code (IaC): Automated provisioning of Azure IoT Hub and GCP Pub/Sub using Terraform.

Multi-Cloud Telemetry: Simultaneous data broadcasting to Azure and GCP.

Command & Control (C2): * Azure: Supports Direct Methods (e.g., triggering a reboot from the portal).

GCP: Supports asynchronous command reception via Pub/Sub subscriptions.

Device Twin Synchronization: * Syncs "Desired Properties" from Azure to the device.

Reports device health and status back to the cloud via "Reported Properties".

🛠️ Tech Stack
Cloud: Azure IoT Hub, GCP Pub/Sub

IaC: Terraform

Language: Python 3.x

Libraries: azure-iot-device, google-cloud-pubsub, python-dotenv

📂 Project Structure
Plaintext

├── main.tf              # Terraform configuration for Azure & GCP resources
├── send_data.py         # Main IoT logic (Telemetry + Command Listeners)
├── .env                 # Environment variables (Connection strings & Project IDs)
└── requirements.txt     # Python dependencies
⚙️ Setup & Installation
1. Infrastructure Provisioning
Initialize and apply the Terraform configuration to create the cloud resources:

Bash

terraform init
terraform apply
2. Environment Configuration
Create a .env file in the root directory:

Code snippet

CONNECTION_STRING="HostName=iiitdm-gowtham-hub.azure-devices.net;DeviceId=...;SharedAccessKey=..."
GCP_PROJECT_ID="your-gcp-project-id"
GCP_TOPIC_ID="gowtham-iot-topic"
3. Run the Device Simulator
Bash

python send_data.py
🧪 Testing Scenarios
Scenario 1: Command & Control (Cloud-to-Device)
Azure: Navigate to the Azure Portal -> IoT Hub -> Devices. Select your device and click Direct Method. Invoke a method (e.g., reboot) and observe the device terminal logs.

GCP: Navigate to the GCP Console -> Pub/Sub -> Topics. Click Publish Message. Send a string (e.g., START_FAN). The device will acknowledge the message via the subscription listener.

Scenario 2: Device Twin Sync
Desired State: Modify the desired property in the Azure Device Twin JSON. The device script will detect the "patch" and print the new configuration.

Reported State: Check the reported section of the Twin in the portal to see the last_sync timestamp updated by the device.

📊 Monitoring
Azure: Use az iot hub monitor-events --hub-name <hub-name> to see live telemetry.

GCP: Use the Pub/Sub Messages tab in the console to "Pull" and verify incoming telemetry data.