"""
Core HCL parsing functionality for Terraform files.
"""

import hcl2
from typing import Dict, Any
import os


class TerraformParser:
    """Handles parsing of Terraform HCL files with metadata preservation."""
    
    def __init__(self):
        self.parsed_data = None
        self.file_path = None
    
    def parse_file(self, file_path: str) -> Dict[str, Any]:
        """
        Parse a Terraform file and return the dictionary with line metadata.
        
        Args:
            file_path: Path to the .tf file
            
        Returns:
            Dictionary representation of the HCL with __start_line__ and __end_line__ metadata
        """
        self.file_path = file_path
        
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Terraform file not found: {file_path}")
        
        try:
            with open(file_path, "r") as file:
                # Use hcl2.load with with_meta=True to preserve line numbers
                self.parsed_data = hcl2.load(file, with_meta=True)
            return self.parsed_data
        except Exception as e:
            raise ValueError(f"Failed to parse Terraform file {file_path}: {str(e)}")
    
    def parse_content(self, content: str) -> Dict[str, Any]:
        """
        Parse Terraform content from a string.
        
        Args:
            content: HCL content as string
            
        Returns:
            Dictionary representation of the HCL with line metadata
        """
        try:
            # Create a file-like object from the string content
            from io import StringIO
            content_io = StringIO(content)
            self.parsed_data = hcl2.load(content_io, with_meta=True)
            return self.parsed_data
        except Exception as e:
            raise ValueError(f"Failed to parse Terraform content: {str(e)}")
    
    def get_resources(self) -> Dict[str, Any]:
        """Get all resources from the parsed data."""
        if not self.parsed_data:
            raise ValueError("No data parsed yet. Call parse_file() or parse_content() first.")
        
        return self.parsed_data.get("resource", [])
    
    def get_databricks_jobs(self) -> Dict[str, Any]:
        """Extract all databricks_job resources."""
        resources = self.get_resources()
        jobs = {}
        
        for i, resource in enumerate(resources):
            if "databricks_job" in resource:
                for job_name, job_data in resource["databricks_job"].items():
                    jobs[job_name] = {
                        "data": job_data,
                        "resource_index": i,
                        "start_line": job_data.get("__start_line__"),
                        "end_line": job_data.get("__end_line__")
                    }
        
        return jobs
    
    def get_databricks_clusters(self) -> Dict[str, Any]:
        """Extract all databricks_cluster resources."""
        resources = self.get_resources()
        clusters = {}
        
        for i, resource in enumerate(resources):
            if "databricks_cluster" in resource:
                for cluster_name, cluster_data in resource["databricks_cluster"].items():
                    clusters[cluster_name] = {
                        "data": cluster_data,
                        "resource_index": i,
                        "start_line": cluster_data.get("__start_line__"),
                        "end_line": cluster_data.get("__end_line__")
                    }
        
        return clusters