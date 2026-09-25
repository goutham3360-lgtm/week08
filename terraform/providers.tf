terraform {
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~>4.0"
    }
  }

  backend "azurerm" {
    resource_group_name  = "koalatech-tfstate-rg"
    storage_account_name = "kttfstate2316609"
    container_name       = "tfstate"
    key                  = "week08.terraform.tfstate"
  }
}

provider "azurerm" {
  features {}
  subscription_id                 = "451d688e-0bac-48e8-95c3-bc25d256b09d"
  resource_provider_registrations = "none"
}