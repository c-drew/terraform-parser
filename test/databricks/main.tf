provider "databricks" {
  host  = var.databricks_host
  token = var.databricks_token
}

resource "databricks_cluster" "etl_cluster" {
  cluster_name            = "ETL-Cluster"
  spark_version           = "13.3.x-scala2.12"
  node_type_id            = "i3.xlarge"
  autotermination_minutes = 20
  num_workers             = 2
}

resource "databricks_job" "etl_workflow" {
  name = "ETL-Workflow"

  task {
    task_key = "Extract"
    existing_cluster_id = databricks_cluster.etl_cluster.id
    notebook_task {
      notebook_path = "/ETL/ExtractNotebook"
    }
  }

  task {
    task_key = "Transform"
    depends_on_task = "Extract"
    existing_cluster_id = databricks_cluster.etl_cluster.id
    notebook_task {
      notebook_path = "/ETL/TransformNotebook"
    }
  }

  task {
    task_key = "Load"
    depends_on_task = "Transform"
    existing_cluster_id = databricks_cluster.etl_cluster.id
    notebook_task {
      notebook_path = "/ETL/LoadNotebook"
    }
  }

  schedule {
    quartz_cron_expression = "0 0 * * * ?"
    timezone_id            = "UTC"
  }
}