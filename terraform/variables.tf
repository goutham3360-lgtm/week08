variable "resource_group_name" {
  type = string
}

variable "location" {
  type    = string
  default = "Australia East"
}

variable "acr_name" {
  type = string
}

variable "aks_cluster_name" {
  type = string
}

variable "storage_account_name" {
  type = string
}

variable "node_count" {
  type    = number
  default = 3
}