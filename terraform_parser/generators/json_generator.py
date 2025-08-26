"""
Generates simplified JSON structures from terraform data.
"""

from typing import Dict, Any, List


class JsonGenerator:
    """Generates simplified JSON representations of terraform resources."""
    
    def create_simplified_structure(self, jobs: Dict[str, Any], clusters: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create a simplified structure from jobs and clusters.
        
        Args:
            jobs: Dictionary of databricks jobs
            clusters: Dictionary of databricks clusters
            
        Returns:
            Simplified dictionary structure
        """
        simplified = {"jobs": {}, "clusters": {}}
        
        # Process jobs
        for job_name, job_info in jobs.items():
            simplified["jobs"][job_name] = self._simplify_job(job_info["data"])
        
        # Process clusters
        for cluster_name, cluster_info in clusters.items():
            simplified["clusters"][cluster_name] = self._simplify_cluster(cluster_info["data"])
        
        return simplified
    
    def _simplify_job(self, job_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Simplify a databricks job to just the essential task information."""
        tasks = []
        for task in job_data.get("task", []):
            task_data = {
                "task_key": task.get("task_key"),
                "depends_on_task": task.get("depends_on_task")
            }
            tasks.append(task_data)
        return tasks
    
    def _simplify_cluster(self, cluster_data: Dict[str, Any]) -> Dict[str, Any]:
        """Simplify a databricks cluster to essential information."""
        return {
            "cluster_name": cluster_data.get("cluster_name"),
            "spark_version": cluster_data.get("spark_version"),
            "node_type_id": cluster_data.get("node_type_id"),
            "autotermination_minutes": cluster_data.get("autotermination_minutes"),
            "num_workers": cluster_data.get("num_workers")
        }