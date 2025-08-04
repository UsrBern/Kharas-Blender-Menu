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
