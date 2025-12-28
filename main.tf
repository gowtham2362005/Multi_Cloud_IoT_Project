resource "azurerm_resource_group" "rg" {
  name     = "iot-challenge-rg"
  location = "Central India"  
}

resource "azurerm_iothub" "hub" {
  name                = "iiitdm-gowtham-hub" 
  resource_group_name = azurerm_resource_group.rg.name
  location            = azurerm_resource_group.rg.location 

  sku {
    name     = "F1" 
    capacity = "1"
  }
}

provider "google" {
  project = "qwiklabs-gcp-03-9ad0135e3cd9" 
  region  = "us-central1"
}

resource "google_pubsub_topic" "iot_topic" {
  name = "gowtham-iot-topic"
}

resource "google_pubsub_subscription" "iot_sub" {
  name  = "gowtham-iot-sub"
  topic = google_pubsub_topic.iot_topic.name
}
