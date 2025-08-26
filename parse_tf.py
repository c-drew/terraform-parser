"""
Main script for parsing Terraform files and generating outputs.
"""

import os
import json
from terraform_parser.parsers import TerraformParser, PositionExtractor
from terraform_parser.generators import MermaidGenerator, JsonGenerator
from terraform_parser.utils import FileUtils


def main():
    """Main function to process Terraform files."""
    output_dir = "parsed_output"
    databricks_dir = "test/databricks"
    
    # Initialize components
    parser = TerraformParser()
    position_extractor = PositionExtractor()
    mermaid_gen = MermaidGenerator()
    json_gen = JsonGenerator()
    file_utils = FileUtils()
    
    # Ensure output directory exists
    file_utils.ensure_directory(output_dir)
    
    # Find all main.tf files
    tf_files = file_utils.find_terraform_files(databricks_dir, pattern="main.tf")
    
    if not tf_files:
        print(f"No main.tf files found in {databricks_dir}")
        return
    
    for tf_file_path in tf_files:
        tf_file = os.path.basename(tf_file_path)
        print(f"\nProcessing: {tf_file}")
        
        try:
            # Parse the terraform file
            tf_dict = parser.parse_file(tf_file_path)
            
            # Extract line positions
            resource_positions, task_positions = position_extractor.extract_all_positions(tf_dict)
            
            print("Resource positions:", resource_positions)
            print("Task positions:", task_positions)
            
            # Get structured data
            jobs = parser.get_databricks_jobs()
            clusters = parser.get_databricks_clusters()
            
            print(f"Found {len(jobs)} jobs and {len(clusters)} clusters")
            
            # Generate simplified JSON
            simplified = json_gen.create_simplified_structure(jobs, clusters)
            
            # Generate Mermaid diagram
            mermaid_content = mermaid_gen.generate_diagram(
                jobs, clusters, resource_positions, task_positions
            )
            
            # Save outputs
            json_output = os.path.join(output_dir, f"simplified_{tf_file}.json")
            mermaid_output = os.path.join(output_dir, f"diagram_{tf_file}.md")
            
            file_utils.save_json(simplified, json_output)
            file_utils.save_text(mermaid_content, mermaid_output)
            
            print(f"✓ Simplified JSON saved to: {json_output}")
            print(f"✓ Mermaid diagram saved to: {mermaid_output}")
            
        except Exception as e:
            print(f"✗ Error processing {tf_file}: {str(e)}")


if __name__ == "__main__":
    main()