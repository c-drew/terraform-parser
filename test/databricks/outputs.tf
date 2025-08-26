# outputs.tf
output "cluster_id" {
  description = "ID of the ETL cluster"
  value       = databricks_cluster.etl_cluster.id
}

output "job_id" {
  description = "ID of the ETL workflow job"
  value       = databricks_job.etl_workflow.id
}