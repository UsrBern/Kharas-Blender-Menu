# Gear management utilities for TBSE Body Kit addon
# This module handles adding/removing gear items and managing their shape keys

import bpy
from .constants import SHAPE_KEY_MASTERS
from .json_helpers import getTextBlock, setTextBlock


def add_shape_keys(obj, master_shape_key_data):
    """
    Add shape keys to an object based on a master shape key collection.
    
    Args:
        obj: The object to add shape keys to
        master_shape_key_data: The master shape key data
    """
    if not obj or not obj.data:
        return False
        
    try:
        # Ensure the object has shape keys
        if not obj.data.shape_keys:
            obj.shape_key_add(name='TBSE', from_mix=False)
            
        # Rename Basis to TBSE if it exists
        if obj.data.shape_keys.key_blocks and obj.data.shape_keys.key_blocks[0].name == 'Basis':
            obj.data.shape_keys.key_blocks[0].name = 'TBSE'
        
        # Add shape keys from master
        for key in master_shape_key_data.key_blocks:
            # Check if the shape key already exists
            if not obj.data.shape_keys.key_blocks.get(key.name):
                obj.shape_key_add(name=key.name, from_mix=False)
            
            # Add driver for everything except TBSE
            if key.name != 'TBSE':
                add_drivers(obj, key, master_shape_key_data)
        
        return True
        
    except Exception as e:
        print(f"Error adding shape keys to {obj.name}: {e}")
        return False


def add_drivers(obj, key, master):
    """
    Add drivers to an object's shape keys.
    
    Args:
        obj: The object to add drivers to
        key: The key to create a driver for
        master: The master shape key data
    """
    try:
        # Create new driver
        new_driver = obj.data.shape_keys.key_blocks[key.name].driver_add('value').driver
        new_driver.type = 'AVERAGE'
        
        # Create variable if none exist
        if len(new_driver.variables) == 0:
            var = new_driver.variables.new()
            var.name = 'value'
            var.type = 'SINGLE_PROP'
            var.targets[0].id_type = 'KEY'
            var.targets[0].id = master
            var.targets[0].data_path = f'key_blocks["{key.name}"].value'
            
    except Exception as e:
        print(f"Error adding driver for {key.name}: {e}")


def add_gear_to_list(obj, gear_list, master_name):
    """
    Add a gear object to a gear list with shape keys.
    
    Args:
        obj: The object to add
        gear_list: The collection property list to add to
        master_name: Name of the master shape key
    """
    try:
        # Get the master shape key data
        if master_name not in bpy.data.shape_keys:
            print(f"Error: Master shape key '{master_name}' not found")
            return False
            
        master = bpy.data.shape_keys[master_name]
        
        # Add to gear list
        new_item = gear_list.add()
        new_item.model_name = obj.name
        new_item.obj_pointer = obj
        
        # Add shape keys to the object
        if add_shape_keys(obj, master):
            obj.use_shape_key_edit_mode = True
            return True
        else:
            # Remove from list if shape key addition failed
            gear_list.remove(len(gear_list) - 1)
            return False
            
    except Exception as e:
        print(f"Error adding {obj.name} to gear list: {e}")
        return False


def remove_shape_keys(obj):
    """
    Remove all shape keys from an object.
    
    Args:
        obj: The object to remove shape keys from
    """
    try:
        if obj and obj.data and obj.data.shape_keys:
            # Remove all shape keys
            for key in obj.data.shape_keys.key_blocks[:]:
                obj.shape_key_remove(key)
        return True
    except Exception as e:
        print(f"Error removing shape keys from {obj.name}: {e}")
        return False


def add_gear_to_json(obj, prefix, model_group_key):
    """
    Add gear object to the JSON models data.
    
    Args:
        obj: The object to add
        prefix: The prefix for the model key
        model_group_key: The group key in the models dictionary
    """
    try:
        model_dict = getTextBlock()
        
        # Ensure the group exists
        if model_group_key not in model_dict:
            model_dict[model_group_key] = {}
        
        # Find available key
        length = len(model_dict[model_group_key])
        model_key = f"{prefix}{length + 1}"
        
        # Handle duplicate keys
        index = 0
        while model_key in model_dict[model_group_key]:
            index += 1
            model_key = f"{prefix}{index}"
        
        # Add to dictionary
        model_dict[model_group_key][model_key] = obj.name
        
        # Save updated data
        setTextBlock(model_dict)
        return True
        
    except Exception as e:
        print(f"Error adding {obj.name} to JSON: {e}")
        return False


def remove_gear_from_json(obj, model_group_key):
    """
    Remove gear object from the JSON models data.
    
    Args:
        obj: The object to remove
        model_group_key: The group key in the models dictionary
    """
    try:
        model_dict = getTextBlock()
        
        if model_group_key in model_dict:
            # Find the model key for this object
            model_key = None
            for key, value in model_dict[model_group_key].items():
                if value == obj.name:
                    model_key = key
                    break
            
            if model_key:
                model_dict[model_group_key].pop(model_key)
                setTextBlock(model_dict)
                return True
        
        return False
        
    except Exception as e:
        print(f"Error removing {obj.name} from JSON: {e}")
        return False


def remove_gear_from_list(gear_list, index):
    """
    Remove gear from the list at the specified index.
    
    Args:
        gear_list: The collection property list
        index: The index to remove
    """
    try:
        if 0 <= index < len(gear_list):
            gear_list.remove(index)
            return True
        return False
    except Exception as e:
        print(f"Error removing gear from list at index {index}: {e}")
        return False


def select_gear(gear_list, index):
    """
    Select the gear object in the 3D viewport when clicked in UI list.
    
    Args:
        gear_list: The collection property list
        index: The index of the item to select
    """
    try:
        # Deselect all objects first
        for obj in bpy.context.selected_objects:
            obj.select_set(False)
        
        # Select the gear object if valid index
        if index >= 0 and index < len(gear_list):
            gear_item = gear_list[index]
            obj = gear_item.obj_pointer
            if obj:
                obj.select_set(True)
                bpy.context.view_layer.objects.active = obj
                
    except Exception as e:
        print(f"Error selecting gear at index {index}: {e}")


# Update callback functions for gear list selection
def select_chest_gear(self, context):
    # Update callback for chest gear list selection.
    gear_list = context.scene.chest_gear_list
    index = context.scene.chest_gear_index
    select_gear(gear_list, index)


def select_leg_gear(self, context):
    # Update callback for leg gear list selection.
    gear_list = context.scene.leg_gear_list
    index = context.scene.leg_gear_index
    select_gear(gear_list, index)


def select_hand_gear(self, context):
    # Update callback for hand gear list selection.
    gear_list = context.scene.hand_gear_list
    index = context.scene.hand_gear_index
    select_gear(gear_list, index)


def select_feet_gear(self, context):
    # Update callback for feet gear list selection.
    gear_list = context.scene.feet_gear_list
    index = context.scene.feet_gear_index
    select_gear(gear_list, index)
