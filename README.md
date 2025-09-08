# terraform-parser
Automated Terraform workflow visualization for Databricks using Mermaid diagrams

## Quick Start
```bash
pip install -r requirements.txt
python parse_tf.py
```

## example mermaid
```mermaid
graph TD
    subgraph etl_workflow
        etl_workflow_Extract[Extract 17-23]
        etl_workflow_Transform[Transform 25-32]
        etl_workflow_Extract --> etl_workflow_Transform
        etl_workflow_Load[Load 34-41]
        etl_workflow_Transform --> etl_workflow_Load
    end
    cluster_etl_cluster[etl_cluster 6-12]
    cluster_etl_cluster -->|uses| etl_workflow_Extract
    cluster_etl_cluster -->|uses| etl_workflow_Transform
    cluster_etl_cluster -->|uses| etl_workflow_Load
    click cluster_etl_cluster "https://github.com"
    click etl_workflow_extract "https://github.com/c-drew/terraform-parser/blob/main/test/databricks/main.tf#L25-L32"
```