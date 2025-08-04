# Setup utility for TBSE Body Kit addon
# This module helps set up the required .models text block in Blender

import bpy
import json
import os
from .json_helpers import setTextBlock

def install_models_data():
    # Install the models data from the tbse models file into Blender's .models text block.
    # This function should be called when setting up the addon for the first time.
    try:
        # Get the addon directory
        addon_dir = os.path.dirname(os.path.abspath(__file__))
        models_file_path = os.path.join(addon_dir, "data", "tbse models")
        
        # Read the models file
        if os.path.exists(models_file_path):
            with open(models_file_path, 'r') as f:
                models_data = json.load(f)
            
            # Set the text block
            setTextBlock(models_data)
            print("TBSE models data installed successfully!")
            return True
        else:
            print("tbse models file not found in addon directory")
            return False
            
    except Exception as e:
        print(f"Error installing models data: {e}")
        return False

def verify_models_data():
    # Verify that the .models text block exists and contains expected data.
    try:
        from .json_helpers import getTextBlock
        models_data = getTextBlock()
        
        required_groups = [
            "body_chest", "body_legs", "genitals_amab", "genitals_afab",
            "piercings_chest", "piercings_amab"
        ]
        
        missing_groups = []
        for group in required_groups:
            if group not in models_data:
                missing_groups.append(group)
        
        if missing_groups:
            print(f"Missing model groups: {missing_groups}")
            return False
        else:
            print("All required model groups found")
            return True
            
    except Exception as e:
        print(f"Error verifying models data: {e}")
        return False

def list_available_objects():
    # List all objects in the current Blender scene that match the models data.
    # Useful for debugging which objects are missing.
    try:
        from .json_helpers import getTextBlock
        models_data = getTextBlock()
        
        print("\nObject availability check:")
        total_objects = 0
        found_objects = 0
        
        for group_name, group_data in models_data.items():
            print(f"\n{group_name}:")
            for model_key, object_name in group_data.items():
                total_objects += 1
                if object_name in bpy.data.objects:
                    print(f"  ✓ {object_name}")
                    found_objects += 1
                else:
                    print(f"  ✗ {object_name} (MISSING)")
        
        print(f"\nSummary: {found_objects}/{total_objects} objects found in scene")
        return found_objects, total_objects
        
    except Exception as e:
        print(f"Error checking objects: {e}")
        return 0, 0
