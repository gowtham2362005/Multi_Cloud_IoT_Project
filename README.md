# 🌐 Multi-Cloud IoT Management

## 🚀 Project Overview
This project demonstrates a multi-cloud IoT architecture using **Terraform** for Infrastructure as Code (IaC) and **Python** for IoT device simulation. It establishes bi-directional communication between a local IoT device and two major cloud providers:

* **Microsoft Azure** (IoT Hub)
* **Google Cloud Platform** (Pub/Sub)

The solution highlights telemetry ingestion, command & control, and device state synchronization across cloud platforms.

---

## 🛠️ Tech Stack

### **Infrastructure**
* **Terraform**
* **Azure RM Provider**
* **Google Cloud Provider**

### **Cloud Platforms**
* **Azure IoT Hub**
* **Google Cloud Pub/Sub**

### **Programming Language**
* **Python 3.x**

### **Libraries & SDKs**
* `azure-iot-device`
* `google-cloud-pubsub`
* `python-dotenv`

---

## ☁️ Cloud Provider Status

| Provider | Status | Notes |
| :--- | :--- | :--- |
| **Azure** | ✅ Active | Full telemetry, command & control, and device twin synchronization implemented. |
| **GCP** | ✅ Verified | Telemetry and C2 verified during lab session (screenshots attached as evidence). |
| **AWS** | ⏳ Omitted | Skipped due to extended verification delays for AWS student accounts. |

---

## 🌟 Key Features

### 1️⃣ Multi-Cloud Telemetry Ingestion
* Python-based IoT simulator broadcasts real-time **JSON telemetry**.
* **Data includes:** Temperature, Humidity, and Timestamps.
* **Simultaneous Transmission:** Data is sent to both **Azure IoT Hub** and **GCP Pub/Sub**.

### 2️⃣ Command & Control (C2)
* **🔹 Azure IoT Hub:** * Implemented **Direct Method** handlers.
    * Supports cloud-to-device commands such as `reboot` and status checks.
* **🔹 Google Cloud Pub/Sub:**
    * Active subscription listener.
    * Commands published from the GCP Console are received and executed by the device.

### 3️⃣ Device Twin Synchronization (Azure)
* **Desired State Sync:** Device listens for "Desired Property" patches (e.g., `fan_speed`). Configuration updates are applied instantly.
* **Reported State Sync:** Device reports `status: running` and last update timestamps, which are synced back to the Azure Device Twin as **Reported Properties**.

---

## 📸 Evidence of Implementation

### **Infrastructure**
Terraform code successfully provisions:
* Azure Resource Groups
* Azure IoT Hub
* GCP Pub/Sub Topics & Subscriptions

### **Metrics**
* **Azure Monitor** confirms **700+ telemetry messages** successfully processed.

### **Live Logs**
Terminal logs demonstrate:
* Parallel telemetry transmission to both clouds.
* Successful cloud-to-device command execution in real-time.
