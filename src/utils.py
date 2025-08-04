# Utility functions for TBSE Body Kit addon
# This module provides common utility functions for object manipulation, error handling, and performance optimization
import bpy
from typing import List, Dict, Optional, Any, Union
from .constants import MODEL_GROUPS, SHAPE_KEY_MASTERS, ERROR_MESSAGES
from .json_helpers import getTextBlock, getModelsInList


def safe_hide_objects(obj_names: List[str], hide: bool = True) -> int:
    """
    Safely hide/show multiple objects with error handling.
    
    Args:
        obj_names: List of object names to hide/show
        hide: True to hide, False to show
        
    Returns:
        Number of objects successfully processed
    """
    processed_count = 0
    
    for obj_name in obj_names:
        if obj_name in bpy.data.objects:
            try:
                bpy.data.objects[obj_name].hide_set(hide)
                processed_count += 1
            except Exception as e:
                print(f"Warning: Could not {'hide' if hide else 'show'} object '{obj_name}': {e}")
        else:
            print(ERROR_MESSAGES['OBJECT_NOT_FOUND'].format(obj=obj_name))
    
    return processed_count


def set_shape_key_value(master_name: str, index: int, value: float = 1.0) -> bool:
    """
    Safely set shape key value with error handling.
    
    Args:
        master_name: Name of the shape key master
        index: Index of the shape key to set
        value: Value to set (default 1.0)
        
    Returns:
        True if successful, False otherwise
    """
    try:
        if master_name not in bpy.data.shape_keys:
            print(ERROR_MESSAGES['SHAPE_KEY_NOT_FOUND'].format(
                master=master_name, 
                type=master_name.replace(' Master', '')
            ))
            return False
            
        shape_keys = bpy.data.shape_keys[master_name].key_blocks
        if 0 <= index < len(shape_keys):
            shape_keys[index].value = value
            return True
        else:
            print(ERROR_MESSAGES['SHAPE_KEY_INDEX_ERROR'].format(
                type=master_name.replace(' Master', ''),
                index=index
            ))
            return False
            
    except Exception as e:
        print(f"Warning: Error setting shape key {master_name}[{index}] = {value}: {e}")
        return False


def reset_shape_keys(master_name: str) -> bool:
    """
    Reset all shape keys in a master to 0.
    
    Args:
        master_name: Name of the shape key master
        
    Returns:
        True if successful, False otherwise
    """
    try:
        if master_name not in bpy.data.shape_keys:
            print(ERROR_MESSAGES['SHAPE_KEY_NOT_FOUND'].format(
                master=master_name,
                type=master_name.replace(' Master', '')
            ))
            return False
            
        for key in bpy.data.shape_keys[master_name].key_blocks:
            key.value = 0
        return True
        
    except Exception as e:
        print(f"Warning: Error resetting shape keys for {master_name}: {e}")
        return False


def set_active_shape_key_for_objects(obj_names: List[str], index: int) -> int:
    """
    Set active shape key index for multiple objects.
    
    Args:
        obj_names: List of object names
        index: Shape key index to set as active
        
    Returns:
        Number of objects successfully processed
    """
    processed_count = 0
    
    for obj_name in obj_names:
        if obj_name in bpy.data.objects:
            try:
                obj = bpy.data.objects[obj_name]
                if hasattr(obj, 'active_shape_key_index'):
                    obj.active_shape_key_index = index
                    processed_count += 1
            except Exception as e:
                print(f"Warning: Could not set active shape key for '{obj_name}': {e}")
        else:
            print(ERROR_MESSAGES['OBJECT_NOT_FOUND'].format(obj=obj_name))
    
    return processed_count


def batch_toggle_visibility(model_groups: Dict[str, List[str]], show_groups: List[str]) -> None:
    """
    Toggle visibility for multiple model groups.
    
    Args:
        model_groups: Dictionary of group names to model lists
        show_groups: Groups to show (others will be hidden)
    """
    # Hide all groups not in show_groups
    for group, models in model_groups.items():
        hide = group not in show_groups
        safe_hide_objects(models, hide=hide)


def manage_skeleton_visibility(show_armature: bool, show_base: bool = True, 
                              show_skirt: bool = True, show_extra: bool = True, 
                              show_tail: bool = True, show_ivcs: bool = False, 
                              show_ivcs2: bool = False) -> bool:
    """
    Manage skeleton object visibility and bone layers.
    
    Args:
        show_armature: Whether to show the skeleton object
        show_base/show_skirt/etc: Whether to show specific bone layers
        
    Returns:
        True if successful, False otherwise
    """
    try:
        if "Skeleton" not in bpy.data.objects or "Skeleton" not in bpy.data.armatures:
            return False
            
        skeleton_obj = bpy.data.objects["Skeleton"]
        skeleton_armature = bpy.data.armatures["Skeleton"]
        
        # Toggle skeleton object visibility
        skeleton_obj.hide_set(not show_armature)
        
        # Handle bone layers (simplified from constants)
        skeleton_armature.layers[0] = show_base     # Base bones
        skeleton_armature.layers[1] = show_skirt    # Skirt bones  
        skeleton_armature.layers[2] = show_extra    # Extra bones
        skeleton_armature.layers[3] = show_tail     # Tail bones
        skeleton_armature.layers[4] = show_ivcs     # IVCS bones
        skeleton_armature.layers[5] = show_ivcs2    # IVCS2 bones
            
        return True
        
    except Exception as e:
        print(f"Warning: Error managing skeleton visibility: {e}")
        return False


def show_single_model(model_list: List[str], model_name: str) -> bool:
    """
    Show a single model from a list, hiding all others.
    
    Args:
        model_list: List of model names
        model_name: Name of model to show
        
    Returns:
        True if successful, False otherwise
    """
    if not model_list or model_name not in model_list:
        return False
        
    # Hide all models first
    safe_hide_objects(model_list, hide=True)
    
    # Show the selected model
    return safe_hide_objects([model_name], hide=False) > 0


def fix_ffxiv_materials(mesh_obj) -> None:
    """Fix material properties for FFXIV compatibility."""
    for mat_slot in mesh_obj.material_slots:
        if mat_slot.material:
            mat = mat_slot.material
            try:
                mat.blend_method = 'HASHED'
                if mat.use_nodes:
                    for node in mat.node_tree.nodes:
                        if node.type == 'BSDF_PRINCIPLED':
                            node.inputs['Metallic'].default_value = 0.0
            except Exception as e:
                print(f"Warning: Error fixing material '{mat.name}': {e}")


def assign_skeleton_armature(mesh_obj) -> bool:
    """Assign skeleton armature to mesh object."""
    try:
        if "Skeleton" in bpy.data.objects:
            skeleton = bpy.data.objects["Skeleton"]
            armature_mod = mesh_obj.modifiers.new(name="Armature", type='ARMATURE')
            armature_mod.object = skeleton
            return True
        return False
    except Exception as e:
        print(f"Warning: Error assigning armature to '{mesh_obj.name}': {e}")
        return False


def fix_skeleton_rotation(skeleton_name: str = "Skeleton") -> bool:
    """
    Fix skeleton rotation for FFXIV standard pose.
    
    Args:
        skeleton_name: Name of the skeleton object
        
    Returns:
        True if successful, False otherwise
    """
    try:
        if skeleton_name not in bpy.data.objects:
            print(f"Warning: Skeleton '{skeleton_name}' not found for rotation fix.")
            return False
            
        skeleton = bpy.data.objects[skeleton_name]
        
        # Select skeleton and enter edit mode
        bpy.ops.object.select_all(action='DESELECT')
        skeleton.select_set(True)
        bpy.context.view_layer.objects.active = skeleton
        
        bpy.ops.object.mode_set(mode='EDIT')
        bpy.ops.armature.select_all(action='SELECT')
        
        # Rotate 90 degrees on X axis for FFXIV standard
        bpy.ops.transform.rotate(value=1.5708, orient_axis='X')
        
        bpy.ops.object.mode_set(mode='OBJECT')
        
        return True
        
    except Exception as e:
        print(f"Warning: Error fixing skeleton rotation: {e}")
        return False
