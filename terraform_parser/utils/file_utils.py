"""
File utility functions for terraform parsing.
"""

import os
import json
from typing import List, Dict, Any


class FileUtils:
    """Handles file operations for the terraform parser."""
    
    @staticmethod
    def find_terraform_files(directory: str, pattern: str = "*.tf") -> List[str]:
        """
        Find all terraform files in a directory.
        
        Args:
            directory: Directory to search
            pattern: File pattern to match (default: "*.tf")
            
        Returns:
            List of full file paths
        """
        if not os.path.exists(directory):
            raise FileNotFoundError(f"Directory not found: {directory}")
        
        tf_files = []
        for file_name in os.listdir(directory):
            if pattern == "*.tf" and file_name.endswith("main.tf"):
                tf_files.append(os.path.join(directory, file_name))
            elif pattern in file_name:
                tf_files.append(os.path.join(directory, file_name))
        
        return tf_files
    
    @staticmethod
    def save_json(data: Dict[str, Any], file_path: str) -> None:
        """Save dictionary as JSON file."""
        with open(file_path, "w") as file:
            json.dump(data, file, indent=4)
    
    @staticmethod
    def save_text(content: str, file_path: str) -> None:
        """Save text content to file."""
        with open(file_path, "w") as file:
            file.write(content)
    
    @staticmethod
    def ensure_directory(directory: str) -> None:
        """Ensure directory exists, create if it doesn't."""
        os.makedirs(directory, exist_ok=True)