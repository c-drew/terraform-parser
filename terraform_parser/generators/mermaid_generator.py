"""
Generates Mermaid diagrams from terraform data.
"""

from typing import Dict, Any, Tuple


class MermaidGenerator:
    """Generates Mermaid diagrams from parsed terraform data."""
    
    def __init__(self):
        self.lines = []
    
    def generate_diagram(self, jobs: Dict[str, Any], clusters: Dict[str, Any], 
                        resource_positions: Dict[str, Tuple], task_positions: Dict[str, Tuple]) -> str:
        """
        Generate a complete Mermaid diagram.
        
        Args:
            jobs: Dictionary of databricks jobs
            clusters: Dictionary of databricks clusters
            resource_positions: Resource line positions
            task_positions: Task line positions
            
        Returns:
            Complete Mermaid diagram as string
        """
        self.lines = ["```mermaid", "graph TD"]
        
        self._generate_job_subgraphs(jobs, task_positions)
        self._generate_cluster_nodes(clusters, resource_positions)
        self._generate_cluster_job_connections(jobs, clusters)
        
        self.lines.append("```")
        return "\n".join(self.lines)
    
    def _generate_job_subgraphs(self, jobs: Dict[str, Any], task_positions: Dict[str, Tuple]) -> None:
        """Generate subgraphs for databricks jobs."""
        for job_name, job_info in jobs.items():
            self.lines.append(f"    subgraph {job_name}")
            
            tasks = job_info["data"].get("task", [])
            for i, task in enumerate(tasks):
                task_key = task.get("task_key", f"task_{i}")
                task_node_id = f"{job_name}_{task_key}"
                
                # Try to get task position
                task_path = f"resource[{job_info['resource_index']}]_databricks_job_{job_name}_task[{i}]"
                start, end = task_positions.get(task_path, (None, None))
                
                # Fallback to task metadata
                if start is None and isinstance(task, dict):
                    start = task.get("__start_line__")
                    end = task.get("__end_line__")
                
                line_info = f" {start}-{end}" if start and end else ""
                self.lines.append(f"        {task_node_id}[{task_key}{line_info}]")
                
                # Add dependencies
                depends_on = task.get("depends_on_task")
                if depends_on:
                    dep_node_id = f"{job_name}_{depends_on}"
                    self.lines.append(f"        {dep_node_id} --> {task_node_id}")
            
            self.lines.append("    end")
    
    def _generate_cluster_nodes(self, clusters: Dict[str, Any], resource_positions: Dict[str, Tuple]) -> None:
        """Generate nodes for databricks clusters."""
        for cluster_name, cluster_info in clusters.items():
            cluster_node_id = f"cluster_{cluster_name}"
            
            # Get cluster position
            start = cluster_info.get("start_line")
            end = cluster_info.get("end_line")
            
            line_info = f" {start}-{end}" if start and end else ""
            self.lines.append(f"    {cluster_node_id}[{cluster_name}{line_info}]")
    
    def _generate_cluster_job_connections(self, jobs: Dict[str, Any], clusters: Dict[str, Any]) -> None:
        """Generate connections between clusters and job tasks."""
        for cluster_name in clusters.keys():
            cluster_node_id = f"cluster_{cluster_name}"
            
            for job_name, job_info in jobs.items():
                tasks = job_info["data"].get("task", [])
                for task in tasks:
                    task_key = task.get("task_key", "unknown")
                    task_node_id = f"{job_name}_{task_key}"
                    self.lines.append(f"    {cluster_node_id} -->|uses| {task_node_id}")