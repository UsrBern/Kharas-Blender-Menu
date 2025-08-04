# Toggle functions for TBSE Body Kit addon
# These functions handle visibility toggles for various gear and piercing models
import bpy
from .constants import MODEL_GROUPS, SHAPE_SPECIFIC_MODELS, SPECIAL_INDICES, SKELETON_OBJECTS
from .utils import (
    safe_hide_objects, batch_toggle_visibility, show_single_model,
    manage_skeleton_visibility
)
from .json_helpers import getTextBlock, getModelsInList, setTextBlock, setModelName


def generic_body_toggle(context, part_type: str, groups: list, shape_prop: str = None):
    """Generic toggle function for body parts with shape variants."""
    tbse_properties = context.scene.tbse_kit_properties
    model_dict = getTextBlock()
    
    # Hide all models in groups initially
    for group in groups:
        models = getModelsInList(model_dict, group)
        safe_hide_objects(models, hide=True)
    
    # Show appropriate models if toggle is enabled
    show_prop = f'show_{part_type}'
    if tbse_properties.get(show_prop, True):
        if shape_prop and hasattr(tbse_properties, shape_prop):
            shape_value = getattr(tbse_properties, shape_prop)
            
            # Handle shape-specific logic
            if part_type == 'chest':
                _handle_chest_shapes(tbse_properties, model_dict, groups, shape_value)
            elif part_type == 'legs':
                _handle_leg_shapes(tbse_properties, model_dict, groups, shape_value)
            else:
                # Default: show first group
                models = getModelsInList(model_dict, groups[0])
                safe_hide_objects(models, hide=False)
        else:
            # No shape variants, show first group
            models = getModelsInList(model_dict, groups[0])
            safe_hide_objects(models, hide=False)


def _handle_chest_shapes(tbse_properties, model_dict, groups, chest_shape):
    """Handle chest shape-specific visibility logic."""
    # Always show neck
    neck_models = getModelsInList(model_dict, MODEL_GROUPS['BODY_NECK'])
    safe_hide_objects(neck_models, hide=False)
    
    # Show appropriate chest models based on shape
    if chest_shape == 'w':
        models = getModelsInList(model_dict, MODEL_GROUPS['BODY_CHEST_W'])
    elif chest_shape == 'chonk':
        models = getModelsInList(model_dict, MODEL_GROUPS['BODY_CHEST_CHONK'])
    elif chest_shape in ['chonk1', 'cub']:
        models = getModelsInList(model_dict, MODEL_GROUPS['BODY_CHEST_CHONK1'])
    else:
        models = getModelsInList(model_dict, MODEL_GROUPS['BODY_CHEST'])
    
    safe_hide_objects(models, hide=False)
    
    # Handle chest piercings if enabled
    if tbse_properties.get('show_piercings_chest', False):
        piercing_models = getModelsInList(model_dict, MODEL_GROUPS['PIERCINGS_CHEST'])
        safe_hide_objects(piercing_models, hide=False)


def _handle_leg_shapes(tbse_properties, model_dict, groups, leg_shape):
    """Handle leg shape-specific visibility logic."""
    genitals = getModelsInList(model_dict, 'body_genitals')
    
    if leg_shape == 'chonk':
        # Show chonk leg models and force AMAB genital toggle
        chonk_models = getModelsInList(model_dict, 'body_legs_chonk')
        safe_hide_objects(chonk_models, hide=False)
        setattr(tbse_properties, 'genital_toggle', 'amab')
    else:
        # Show base TBSE leg models
        leg_models = getModelsInList(model_dict, MODEL_GROUPS['BODY_LEGS'])
        safe_hide_objects(leg_models, hide=False)
        
        # Handle genital visibility
        if tbse_properties.genital_toggle == 'amab' or leg_shape == 'xl':
            if leg_shape == 'xl':
                setattr(tbse_properties, 'genital_toggle', 'amab')
            # Show AMAB butt (index 0)
            if genitals and len(genitals) > 0:
                safe_hide_objects([genitals[0]], hide=False)
        else:
            # Show AFAB butt (index 1)
            if genitals and len(genitals) > 1:
                safe_hide_objects([genitals[1]], hide=False)


def generic_gear_toggle(context, gear_type: str):
    """Generic toggle function for gear visibility."""
    tbse_properties = context.scene.tbse_kit_properties
    gear_list = getattr(context.scene, f'{gear_type}_gear_list')
    show_prop = f'show_{gear_type}_gear'
    is_enabled = tbse_properties.get(show_prop, True)
    
    for obj in gear_list:
        if is_enabled and obj.isEnabled: 
            obj.obj_pointer.hide_set(False)
        else: 
            obj.obj_pointer.hide_set(True)


def generic_piercing_toggle(context, piercing_type: str, model_group: str):
    """Generic toggle function for piercing visibility."""
    tbse_properties = context.scene.tbse_kit_properties
    piercing_toggles = getattr(context.scene, f'tbse_{piercing_type}_toggles')
    model_dict = getTextBlock()
    
    piercing_models = getModelsInList(model_dict, model_group)
    
    # Hide all first
    safe_hide_objects(piercing_models, hide=True)
    
    # Show based on individual piercing toggles
    for prop_name in dir(piercing_toggles):
        if not prop_name.startswith('_') and hasattr(piercing_toggles, prop_name):
            prop_value = getattr(piercing_toggles, prop_name)
            if isinstance(prop_value, bool) and prop_value:
                # Find corresponding model (this is simplified)
                for model in piercing_models:
                    if prop_name.replace('_', ' ').lower() in model.lower():
                        safe_hide_objects([model], hide=False)


# Specific toggle functions using generic implementations
def chestToggle(self, context):
    """Toggle visibility of chest models."""
    groups = [
        MODEL_GROUPS['BODY_NECK'],
        MODEL_GROUPS['BODY_CHEST'],
        MODEL_GROUPS['BODY_CHEST_W'],
        MODEL_GROUPS['BODY_CHEST_CHONK'],
        MODEL_GROUPS['BODY_CHEST_CHONK1'],
        MODEL_GROUPS['PIERCINGS_CHEST']
    ]
    generic_body_toggle(context, 'chest', groups, 'chest_shape')


def legToggle(self, context):
    # Toggle visibility of leg models.
    groups = [
        MODEL_GROUPS['BODY_LEGS'],
        'body_legs_chonk',
        'body_genitals'
    ]
    generic_body_toggle(context, 'legs', groups, 'leg_shape')
    
    # Trigger NSFW toggle check
    nsfwToggle(self, context)


def handToggle(self, context):
    # Toggle visibility of hand models.
    generic_body_toggle(context, 'hands', [MODEL_GROUPS.get('BODY_HANDS', 'body_hands')])


def feetToggle(self, context):
    # Toggle visibility of feet models.
    generic_body_toggle(context, 'feet', [MODEL_GROUPS.get('BODY_FEET', 'body_feet')])


def bpfToggle(self, context):
    # Toggle visibility of BPF models.
    generic_body_toggle(context, 'bpf', [MODEL_GROUPS.get('GENITALS_BPF', 'genitals_bpf')])
    generic_body_toggle(context, 'bpf', ['genitals_bpf'])


def chestGearToggle(self, context):
    # Toggle visibility of chest gear.
    generic_gear_toggle(context, 'chest')


def legGearToggle(self, context):
    # Toggle visibility of leg gear.
    generic_gear_toggle(context, 'leg')


def handGearToggle(self, context):
    # Toggle visibility of hand gear.
    generic_gear_toggle(context, 'hand')


def feetGearToggle(self, context):
    # Toggle visibility of feet gear.
    generic_gear_toggle(context, 'feet')


def chestPiercingToggle(self, context):
    # Toggle visibility of chest piercings.
    generic_piercing_toggle(context, 'chest', MODEL_GROUPS['PIERCINGS_CHEST'])


def amabPiercingToggle(self, context):
    # Toggle visibility of AMAB piercings.
    generic_piercing_toggle(context, 'amab', MODEL_GROUPS.get('PIERCINGS_AMAB', 'piercings_amab'))
    nsfwToggle(self, context)


def nsfwToggle(self, context):
    # Toggle visibility of NSFW models
    tbse_properties = context.scene.tbse_kit_properties
    
    # Get all NSFW-related model groups efficiently
    nsfw_groups = [
        MODEL_GROUPS['GENITALS_AMAB'],
        MODEL_GROUPS['GENITALS_AFAB'],
        MODEL_GROUPS['GENITALS_BPF'],
        MODEL_GROUPS['PIERCINGS_AMAB'],
        MODEL_GROUPS['BODY_LEGS_CHONK']
    ]
    
    modelDict = getTextBlock()
    
    # Hide all NSFW models initially
    for group in nsfw_groups[:-1]:  # All except body_legs_chonk
        group_models = getModelsInList(modelDict, group)
        safe_hide_objects(group_models, hide=True)
    
    # Special handling for chonk legs NSFW model (index 3)
    chonk_legs = getModelsInList(modelDict, MODEL_GROUPS['BODY_LEGS_CHONK'])
    if chonk_legs and len(chonk_legs) > SPECIAL_INDICES['CHONK_NSFW_INDEX']:
        safe_hide_objects([bpy.data.objects[chonk_legs[SPECIAL_INDICES['CHONK_NSFW_INDEX']]]], hide=True)
    
    # Show appropriate NSFW models if enabled
    if tbse_properties['show_nsfw']:
        if (tbse_properties.leg_shape == 'chonk' and 
            tbse_properties['show_legs'] and
            chonk_legs and len(chonk_legs) > SPECIAL_INDICES['CHONK_NSFW_INDEX']):
            # Show chonk NSFW model
            safe_hide_objects([bpy.data.objects[chonk_legs[SPECIAL_INDICES['CHONK_NSFW_INDEX']]]], hide=False)
        else:
            # Handle other NSFW logic
            genitalSet(self, context)
        
        # Handle AMAB piercings if enabled
        if tbse_properties['show_piercings_amab']:
            amabPiercingToggle(self, context)


def _simple_body_part_toggle(context, part_name: str, show_property: str):
    # Generic function for simple body part visibility toggles.
    tbse_properties = context.scene.tbse_kit_properties
    modelDict = getTextBlock()
    
    # Map part names to model groups
    part_to_group = {
        'hands': MODEL_GROUPS['BODY_HANDS'],
        'feet': MODEL_GROUPS['BODY_FEET'],
        'bpf': 'genitals_bpf'  # Special case for BPF
    }
    
    if part_name not in part_to_group:
        print(f"Warning: Unknown body part '{part_name}' in toggle function.")
        return
    
    model_group = part_to_group[part_name]
    models = getModelsInList(modelDict, model_group)
    
    # Toggle visibility based on property
    show = tbse_properties.get(show_property, False)
    safe_hide_objects(models, hide=not show)


def handToggle(self, context):
    # Toggle visibility of hand models.
    _simple_body_part_toggle(context, 'hands', 'show_hands')


def feetToggle(self, context):
    # Toggle visibility of feet models.
    _simple_body_part_toggle(context, 'feet', 'show_feet')


def genitalToggle(self, context):
    # Toggle between AMAB and AFAB genital types
    tbse_properties = context.scene.tbse_kit_properties
    modelDict = getTextBlock()
    
    # Get body genitals (butt models)
    genitals = getModelsInList(modelDict, MODEL_GROUPS['BODY_GENITALS'])
    
    # Hide all butt models initially
    safe_hide_objects(genitals, hide=True)
    
    # Don't show anything if leg shape is chonk
    if tbse_properties.leg_shape == 'chonk':
        return
    
    # Show appropriate genital model based on toggle and leg shape
    if (tbse_properties.genital_toggle == 'amab' or 
        tbse_properties.leg_shape == 'xl'):
        # Show AMAB butt model
        if len(genitals) > SPECIAL_INDICES['AMAB_BUTT_INDEX']:
            safe_hide_objects([bpy.data.objects[genitals[SPECIAL_INDICES['AMAB_BUTT_INDEX']]]], hide=False)
    else:
        # Show AFAB butt model
        if len(genitals) > SPECIAL_INDICES['AFAB_BUTT_INDEX']:
            safe_hide_objects([bpy.data.objects[genitals[SPECIAL_INDICES['AFAB_BUTT_INDEX']]]], hide=False)
    
    # Handle specific genital model logic
    genitalSet(self, context)


def bpfToggle(self, context):
    # Toggle visibility of BPF models with complex logic.
    tbse_properties = context.scene.tbse_kit_properties
    modelDict = getTextBlock()
    
    # Get BPF models efficiently
    bpf_models = getModelsInList(modelDict, 'genitals_bpf')
    
    # If leg shape is chonk or xl, do nothing
    if tbse_properties.leg_shape in ['chonk', 'xl']:
        return
    
    # Show BPF models only if NSFW, BPF, and AFAB are all enabled
    show_bpf = (tbse_properties['show_nsfw'] and 
                tbse_properties['show_bpf'] and 
                tbse_properties.genital_toggle == 'afab')
    
    safe_hide_objects(bpf_models, hide=not show_bpf)


def genitalSet(self, context):
    # Set specific genital model based on type selection
    tbse_properties = context.scene.tbse_kit_properties
    modelDict = getTextBlock()
    
    # Get all genital model groups
    genital_groups = [
        MODEL_GROUPS['GENITALS_AMAB'],
        MODEL_GROUPS['GENITALS_AFAB'],
        MODEL_GROUPS['GENITALS_BPF']
    ]
    
    # Hide all genital models initially
    for group in genital_groups:
        group_models = getModelsInList(modelDict, group)
        safe_hide_objects(group_models, hide=True)
    
    # Show models only if NSFW and legs are enabled
    if not (tbse_properties['show_nsfw'] and tbse_properties['show_legs']):
        return
    
    # Handle AMAB models
    if (tbse_properties.genital_toggle == 'amab' or 
        tbse_properties.leg_shape in ['xl', 'chonk']):
        
        amab_models = getModelsInList(modelDict, MODEL_GROUPS['GENITALS_AMAB'])
        if amab_models:
            # Get specific AMAB model by type (simplified)
            amab_type_map = {'default': 0, 'cut': 1, 'pierced': 2}
            model_index = amab_type_map.get(tbse_properties.amab_type, 0)
            if len(amab_models) > model_index:
                safe_hide_objects([bpy.data.objects[amab_models[model_index]]], hide=False)
    
    # Handle AFAB models  
    else:
        afab_models = getModelsInList(modelDict, MODEL_GROUPS['GENITALS_AFAB'])
        if afab_models:
            # Special handling for BBWVR vs Bibo models
            if tbse_properties.afab_type == 'bbwvr':
                if len(afab_models) > SPECIAL_INDICES['BBWVR_INDEX']:
                    safe_hide_objects([bpy.data.objects[afab_models[SPECIAL_INDICES['BBWVR_INDEX']]]], hide=False)
            else:
                if len(afab_models) > SPECIAL_INDICES['BIBO_INDEX']:
                    safe_hide_objects([bpy.data.objects[afab_models[SPECIAL_INDICES['BIBO_INDEX']]]], hide=False)
                
                # Handle BPF if enabled
                if tbse_properties['show_bpf']:
                    bpfToggle(self, context)
                
                # Change bibo shape
                from .drivers import afab_driver
                afab_driver(self, context)


def boneToggles(self, context):
    # Toggle visibility of different bone layers
    tbse_properties = context.scene.tbse_kit_properties
    
    # Use the utility function for skeleton management
    manage_skeleton_visibility(tbse_properties, SKELETON_OBJECTS['OBJECT'])


def chestPiercingToggle(self, context):
    # Toggle visibility of chest piercing models using generic function
    generic_piercing_toggle(context, 'chest', 'show_piercings_chest')


def amabPiercingToggle(self, context):
    # Toggle visibility of amab piercing models using generic function
    generic_piercing_toggle(context, 'amab', 'show_piercings_amab')


def chestGearToggle(self, context):
    # Toggle visibility of chest gear using generic function
    generic_gear_toggle(context, 'chest', 'show_chest_gear')


def legGearToggle(self, context):
    # Toggle visibility of leg gear using generic function
    generic_gear_toggle(context, 'leg', 'show_leg_gear')


def handGearToggle(self, context):
    # Toggle visibility of hand gear using generic function
    generic_gear_toggle(context, 'hand', 'show_hand_gear')


def feetGearToggle(self, context):
    # Toggle visibility of feet gear using generic function
    generic_gear_toggle(context, 'feet', 'show_feet_gear')


def gearToggle(self, context):
    # Toggle visibility of individual gear item
    obj = self.obj_pointer
    if self.isEnabled: 
        obj.hide_set(False)
    else: 
        obj.hide_set(True)


def modelNameChange(self, context):
    # Update model name when gear list item name is changed
    modelDict = getTextBlock()
    obj = self.obj_pointer
    if obj:
        obj.name = setModelName(modelDict, obj.name, self.model_name)
    setTextBlock(modelDict)
