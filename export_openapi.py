"""
Export OpenAPI Specification Script

This script exports the FastAPI OpenAPI (Swagger) specification
to a JSON file that can be shared with the frontend team.
"""

import json
import os
from main import app

def export_openapi_spec():
    """Export the OpenAPI specification to a JSON file"""
    
    # Get the OpenAPI schema from FastAPI
    openapi_schema = app.openapi()
    
    # Define output file path
    output_file = "onenet_api_spec.json"
    
    # Write to JSON file with pretty formatting
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(openapi_schema, f, indent=2, ensure_ascii=False)
    
    # Get absolute path for display
    abs_path = os.path.abspath(output_file)
    
    print("[SUCCESS] API specification exported successfully!")
    print(f"File location: {abs_path}")
    print(f"Total endpoints: {len([p for p in openapi_schema.get('paths', {}).values()])}")
    print("\nShare this file with your frontend team!")

if __name__ == "__main__":
    export_openapi_spec()
