# Driver functions for TBSE Body Kit addon.
# This module contains driver logic for chest and leg shape keys, as well as genital shape changes.
import bpy
from .constants import SHAPE_KEY_MASTERS, CHEST_SHAPE_CATEGORIES, LEG_SHAPE_CATEGORIES, MODEL_GROUPS
from .utils import (
    reset_shape_keys, set_shape_key_value, 
    set_active_shape_key_for_objects
)
from .json_helpers import getTextBlock, getModelsInList

def chest_resetDrivers():
    # Reset all chest shape keys back to TBSE (Basis).
    return reset_shape_keys(SHAPE_KEY_MASTERS['CHEST'])


def chest_driver(self, context):
    # Driver logic for chest shape keys.
    tbse_properties = context.scene.tbse_kit_properties
    
    # Reset shape before changing to another shape
    chest_resetDrivers()
    index = 0
    
    if tbse_properties.chest_shape != 'tbse':
        # Get index from enum items
        chest_type = tbse_properties.bl_rna.properties.get('chest_shape')
        index = chest_type.enum_items.find(tbse_properties.chest_shape)
        
        # Set the shape key value
        if not set_shape_key_value(SHAPE_KEY_MASTERS['CHEST'], index):
            return False
    
    # Trigger chest model visibility toggle
    from .toggles import chestToggle  # Import here to avoid circular imports
    chestToggle(self, context)

    # Get model lists
    model_dict = getTextBlock()
    chest_models = getModelsInList(model_dict, MODEL_GROUPS['BODY_CHEST'])
    gear_chest_models = getModelsInList(model_dict, MODEL_GROUPS['GEAR_CHEST'])
    gear_hands_models = getModelsInList(model_dict, MODEL_GROUPS['GEAR_HANDS'])
    
    # Combine all model lists
    all_models = chest_models + gear_chest_models + gear_hands_models
    
    # Set active shape key for all objects with chest shape keys
    chest_shape = tbse_properties.chest_shape
    for obj_name in all_models:
        if obj_name in bpy.data.objects:
            shape_index = index
            
            # Special handling for hands gear - use simpler mapping
            if obj_name in gear_hands_models:
                shape_categories = {
                    'tbse': 0, 'slim': 1, 'w': 1, 'sbtl': 1, 'sbtlslimmer': 1,
                    'twink': 2, 'twunk': 2, 'hunk': 2, 'offtwunk': 2, 'offhunk': 2,
                    'chonk': 3, 'chonk1': 3, 'cub': 3, 'xl': 3
                }
                shape_index = shape_categories.get(chest_shape, 0)
            
            set_active_shape_key_for_objects([obj_name], shape_index)

def leg_resetDrivers():
    # Reset all leg shape keys back to TBSE (Basis).
    return reset_shape_keys(SHAPE_KEY_MASTERS['LEG'])


def leg_driver(self, context):
    # Driver logic for leg shape keys.
    tbse_properties = context.scene.tbse_kit_properties

    # Reset shape before changing to another shape
    leg_resetDrivers()
    index = 0
    
    if tbse_properties.leg_shape != 'tbse':
        # Get index from enum items
        leg_type = tbse_properties.bl_rna.properties.get('leg_shape')
        index = leg_type.enum_items.find(tbse_properties.leg_shape)
        
        # Set the shape key value
        if not set_shape_key_value(SHAPE_KEY_MASTERS['LEG'], index):
            return False
    
    # Trigger leg model visibility toggle
    from .toggles import legToggle  # Import here to avoid circular imports
    legToggle(self, context)

    # Get model lists
    model_dict = getTextBlock()
    leg_models = getModelsInList(model_dict, MODEL_GROUPS['BODY_LEGS'])
    gear_legs_models = getModelsInList(model_dict, MODEL_GROUPS['GEAR_LEGS'])
    gear_feet_models = getModelsInList(model_dict, MODEL_GROUPS['GEAR_FEET'])
    
    # Combine all model lists
    all_models = leg_models + gear_legs_models + gear_feet_models

    # Set active shape key for all objects with leg shape keys
    for obj_name in all_models:
        if obj_name in bpy.data.objects:
            set_active_shape_key_for_objects([obj_name], index)

def afab_ResetDrivers():
    # Reset all AFAB shape keys back to Gen A (Basis).
    return reset_shape_keys(SHAPE_KEY_MASTERS['AFAB'])


def afab_driver(self, context):
    # Driver logic for AFAB genital shape changes.
    tbse_properties = context.scene.tbse_kit_properties
    
    # Reset shape before changing to another shape
    afab_ResetDrivers()
    
    if tbse_properties.afab_type != 'a':
        # Get index from enum items
        afab_shape = tbse_properties.bl_rna.properties.get('afab_type')
        index = afab_shape.enum_items.find(tbse_properties.afab_type)
        return set_shape_key_value(SHAPE_KEY_MASTERS['AFAB'], index)
    
    return True


def amab_ResetDrivers():
    # Reset all AMAB shape keys back to Gen A (Basis).

    return reset_shape_keys(SHAPE_KEY_MASTERS['AMAB'])


def amab_driver(self, context):
    # Driver logic for AMAB genital shape changes.
    tbse_properties = context.scene.tbse_kit_properties

    # Reset shape before changing to another shape
    amab_ResetDrivers()

    if tbse_properties.amab_type != 'a':
        # Get index from enum items
        amab_shape = tbse_properties.bl_rna.properties.get('amab_type')
        index = amab_shape.enum_items.find(tbse_properties.amab_type)
        return set_shape_key_value(SHAPE_KEY_MASTERS['AMAB'], index)
    
    return True
