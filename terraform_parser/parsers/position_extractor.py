"""
Extracts line position information from parsed HCL data.
"""

from typing import Dict, Any, Tuple


class PositionExtractor:
    """Handles extraction of line positions from HCL metadata."""
    
    def __init__(self):
        self.resource_positions = {}
        self.task_positions = {}
    
    def extract_all_positions(self, tf_dict: Dict[str, Any]) -> Tuple[Dict[str, Tuple], Dict[str, Tuple]]:
        """
        Extract all resource and task positions from the terraform dictionary.
        
        Args:
            tf_dict: Parsed terraform dictionary with metadata
            
        Returns:
            Tuple of (resource_positions, task_positions)
        """
        self.resource_positions = {}
        self.task_positions = {}
        
        self._extract_positions_recursive(tf_dict)
        
        return self.resource_positions, self.task_positions
    
    def _extract_positions_recursive(self, data: Any, path: str = "") -> None:
        """Recursively extract line positions from the HCL dictionary."""
        if isinstance(data, dict):
            # Check for line metadata
            start_line = data.get("__start_line__")
            end_line = data.get("__end_line__")
            
            if start_line is not None and end_line is not None and path:
                if "task" in path.lower():
                    self.task_positions[path] = (start_line, end_line)
                else:
                    self.resource_positions[path] = (start_line, end_line)
            
            # Recursively process all dictionary items
            for key, value in data.items():
                if not key.startswith("__"):  # Skip metadata keys
                    new_path = f"{path}_{key}" if path else key
                    self._extract_positions_recursive(value, new_path)
        
        elif isinstance(data, list):
            # Process list items
            for i, item in enumerate(data):
                new_path = f"{path}[{i}]" if path else f"[{i}]"
                self._extract_positions_recursive(item, new_path)
    
    def get_resource_position(self, resource_type: str, resource_name: str, resource_index: int = 0) -> Tuple[int, int]:
        """Get position for a specific resource."""
        key = f"resource[{resource_index}]_{resource_type}_{resource_name}"
        return self.resource_positions.get(key, (None, None))
    
    def get_task_position(self, job_name: str, task_index: int, resource_index: int = 0) -> Tuple[int, int]:
        """Get position for a specific task."""
        key = f"resource[{resource_index}]_databricks_job_{job_name}_task[{task_index}]"
        return self.task_positions.get(key, (None, None))