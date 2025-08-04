# Utility functions for TBSE Body Kit addon
# This module provides common utility functions for object manipulation, error handling, and performance optimization
import bpy
from typing import List, Dict, Optional, Any, Union
from .constants import MODEL_GROUPS, SHAPE_KEY_MASTERS, ERROR_MESSAGES
from .json_helpers import getTextBlock, getModelsInList


class ModelCache:
    """Cache for frequently accessed model data to improve performance."""
    _model_dict_cache = None
    _cache_dirty = True
    
    @classmethod
    def get_model_dict(cls) -> Dict[str, Any]:
        """Get cached model dictionary, refresh if dirty."""
        if cls._cache_dirty or cls._model_dict_cache is None:
            cls._model_dict_cache = getTextBlock()
            cls._cache_dirty = False
        return cls._model_dict_cache
    
    @classmethod
    def invalidate_cache(cls):
        """Mark cache as dirty to force refresh on next access."""
        cls._cache_dirty = True


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


def get_models_by_groups(groups: List[str], use_cache: bool = True) -> Dict[str, List[str]]:
    """
    Get model lists for multiple groups efficiently.
    
    Args:
        groups: List of model group keys to retrieve
        use_cache: Whether to use cached model dictionary
        
    Returns:
        Dictionary mapping group names to model lists
    """
    model_dict = ModelCache.get_model_dict() if use_cache else getTextBlock()
    result = {}
    
    for group in groups:
        result[group] = getModelsInList(model_dict, group)
    
    return result


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


def get_shape_category_index(shape_name: str, categories: Dict[str, List[str]]) -> int:
    """
    Get the index for a shape based on its category.
    
    Args:
        shape_name: Name of the shape
        categories: Dictionary of category mappings
        
    Returns:
        Index for the shape category, 0 if not found
    """
    for i, (category, shapes) in enumerate(categories.items(), 1):
        if shape_name in shapes:
            return i
    return 0


def batch_toggle_visibility(model_groups: Dict[str, List[str]], show_groups: List[str], hide_groups: List[str] = None) -> Dict[str, int]:
    """
    Efficiently toggle visibility for multiple model groups.
    
    Args:
        model_groups: Dictionary of group names to model lists
        show_groups: Groups to show
        hide_groups: Groups to hide (if None, hides all groups not in show_groups)
        
    Returns:
        Dictionary with counts of processed objects per group
    """
    results = {}
    
    # Hide specified groups or all groups not in show_groups
    groups_to_hide = hide_groups if hide_groups else [g for g in model_groups.keys() if g not in show_groups]
    
    for group in groups_to_hide:
        if group in model_groups:
            results[f"{group}_hidden"] = safe_hide_objects(model_groups[group], hide=True)
    
    # Show specified groups
    for group in show_groups:
        if group in model_groups:
            results[f"{group}_shown"] = safe_hide_objects(model_groups[group], hide=False)
    
    return results


def manage_skeleton_visibility(properties, skeleton_name: str = "Skeleton") -> bool:
    """
    Manage skeleton object visibility and bone layers.
    
    Args:
        properties: TBSE properties object
        skeleton_name: Name of the skeleton object
        
    Returns:
        True if successful, False otherwise
    """
    try:
        if skeleton_name not in bpy.data.objects:
            print(f"Warning: Skeleton object '{skeleton_name}' not found.")
            return False
            
        if skeleton_name not in bpy.data.armatures:
            print(f"Warning: Skeleton armature '{skeleton_name}' not found.")
            return False
            
        skeleton_obj = bpy.data.objects[skeleton_name]
        skeleton_armature = bpy.data.armatures[skeleton_name]
        
        # Toggle skeleton object visibility
        skeleton_obj.hide_set(not properties.get('show_armature', True))
        
        # Handle bone layers
        from .constants import BONE_LAYERS
        for layer_name, (prop_name, layer_index) in BONE_LAYERS.items():
            show_layer = properties.get(prop_name, True)
            skeleton_armature.layers[layer_index] = show_layer
            
        return True
        
    except Exception as e:
        print(f"Warning: Error managing skeleton visibility: {e}")
        return False


def get_genital_model_by_type(genital_models: List[str], genital_type: str, enum_property) -> Optional[str]:
    """
    Get specific genital model based on type selection.
    
    Args:
        genital_models: List of genital model names
        genital_type: The selected genital type
        enum_property: The enum property for finding the index
        
    Returns:
        Model name if found, None otherwise
    """
    try:
        if not genital_models or not enum_property:
            return None
            
        type_index = enum_property.enum_items.find(genital_type)
        if 0 <= type_index < len(genital_models):
            return genital_models[type_index]
        else:
            print(f"Warning: Genital type index {type_index} out of range for {len(genital_models)} models.")
            return None
            
    except Exception as e:
        print(f"Warning: Error getting genital model by type: {e}")
        return None


def show_single_model_by_index(model_list: List[str], index: int) -> bool:
    """
    Show a single model from a list by index, hiding all others.
    
    Args:
        model_list: List of model names
        index: Index of model to show
        
    Returns:
        True if successful, False otherwise
    """
    if not model_list or index < 0 or index >= len(model_list):
        return False
        
    # Hide all models first
    safe_hide_objects(model_list, hide=True)
    
    # Show the selected model
    return safe_hide_objects([model_list[index]], hide=False) > 0


def process_imported_fbx_objects(imported_objects: List, fix_materials: bool = True, 
                                auto_assign_armature: bool = True, delete_junk: bool = True) -> Dict[str, List]:
    """
    Process imported FBX objects with optimized cleanup operations.
    
    Args:
        imported_objects: List of imported Blender objects
        fix_materials: Whether to fix material properties for FFXIV
        auto_assign_armature: Whether to auto-assign armature modifiers
        delete_junk: Whether to delete non-mesh objects
        
    Returns:
        Dictionary with 'meshes' and 'junk' object lists
    """
    meshes = []
    junk = []
    
    # Organize objects by type
    for obj in imported_objects:
        if obj.type == 'MESH':
            meshes.append(obj)
        else:
            junk.append(obj)
    
    # Process mesh objects
    processed_count = 0
    for mesh_obj in meshes:
        try:
            # Fix materials for FFXIV compatibility
            if fix_materials:
                _fix_ffxiv_materials(mesh_obj)
            
            # Auto-assign armature if skeleton exists
            if auto_assign_armature and "Skeleton" in bpy.data.objects:
                _assign_skeleton_armature(mesh_obj)
            
            processed_count += 1
            
        except Exception as e:
            print(f"Warning: Error processing mesh '{mesh_obj.name}': {e}")
    
    # Handle junk objects
    if delete_junk and junk:
        try:
            # Select junk objects for deletion
            bpy.ops.object.select_all(action='DESELECT')
            for obj in junk:
                obj.select_set(True)
            bpy.ops.object.delete()
            print(f"Deleted {len(junk)} junk objects during FBX import cleanup.")
        except Exception as e:
            print(f"Warning: Error deleting junk objects: {e}")
    
    return {
        'meshes': meshes,
        'junk': junk,
        'processed_count': processed_count
    }


def _fix_ffxiv_materials(mesh_obj) -> int:
    """
    Fix material properties for FFXIV compatibility.
    
    Args:
        mesh_obj: Mesh object to fix materials for
        
    Returns:
        Number of materials processed
    """
    materials_fixed = 0
    
    for mat_slot in mesh_obj.material_slots:
        if mat_slot.material:
            mat = mat_slot.material
            try:
                # Set blend method to Alpha Hashed for FFXIV compatibility
                mat.blend_method = 'HASHED'
                
                # Fix metallic values in principled BSDF nodes
                if mat.use_nodes:
                    for node in mat.node_tree.nodes:
                        if node.type == 'BSDF_PRINCIPLED':
                            node.inputs['Metallic'].default_value = 0.0
                
                materials_fixed += 1
                
            except Exception as e:
                print(f"Warning: Error fixing material '{mat.name}': {e}")
    
    return materials_fixed


def _assign_skeleton_armature(mesh_obj) -> bool:
    """
    Assign skeleton armature to mesh object.
    
    Args:
        mesh_obj: Mesh object to assign armature to
        
    Returns:
        True if successful, False otherwise
    """
    try:
        skeleton = bpy.data.objects["Skeleton"]
        
        # Add armature modifier
        armature_mod = mesh_obj.modifiers.new(name="Armature", type='ARMATURE')
        armature_mod.object = skeleton
        
        return True
        
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
