resource "azurerm_resource_group" "rg" {
  name     = "iot-challenge-rg"
  location = "Central India"  # Change this line
}

resource "azurerm_iothub" "hub" {
  name                = "iiitdm-gowtham-hub" 
  resource_group_name = azurerm_resource_group.rg.name
  location            = azurerm_resource_group.rg.location # This will now be Central India

  sku {
    name     = "F1" 
    capacity = "1"
  }
}

# The "Blueprint" for Google Cloud
provider "google" {
  project = "qwiklabs-gcp-03-9ad0135e3cd9" # Copy exactly from your image
  region  = "us-central1"
}

# Create a Topic for your IoT data (This is like the Hub's inbox)
resource "google_pubsub_topic" "iot_topic" {
  name = "gowtham-iot-topic"
}

# Create a Subscription to read the data
resource "google_pubsub_subscription" "iot_sub" {
  name  = "gowtham-iot-sub"
  topic = google_pubsub_topic.iot_topic.name
}