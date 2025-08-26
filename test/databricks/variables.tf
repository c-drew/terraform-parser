# variables.tf
variable "databricks_host" {
  description = "Databricks workspace host URL"
  type        = string
}

variable "databricks_token" {
  description = "Databricks access token"
  type        = string
  sensitive   = true
}

variable "cluster_name" {
  description = "Name of the ETL cluster"
  type        = string
  default     = "ETL-Cluster"
}

variable "spark_version" {
  description = "Spark version for the cluster"
  type        = string
  default     = "13.3.x-scala2.12"
}

variable "node_type_id" {
  description = "Node type ID for the cluster"
  type        = string
  default     = "i3.xlarge"
}

variable "num_workers" {
  description = "Number of workers in the cluster"
  type        = number
  default     = 2
}

variable "job_name" {
  description = "Name of the ETL workflow job"
  type        = string
  default     = "ETL-Workflow"
}