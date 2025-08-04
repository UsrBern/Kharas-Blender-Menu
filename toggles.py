# Toggle functions for TBSE Body Kit addon
# These functions handle visibility toggles for various gear and piercing models
import bpy
from .constants import MODEL_GROUPS, SHAPE_SPECIFIC_MODELS
from .utils import ModelCache, safe_hide_objects, get_models_by_groups, batch_toggle_visibility
from .json_helpers import getTextBlock, getModelsInList, setTextBlock, setModelName


def chestToggle(self, context):
    # Toggle visibility of chest models
    tbse_properties = context.scene.tbse_kit_properties
    chest_shape = tbse_properties.chest_shape
    
    # Get all chest-related model groups efficiently
    chest_groups = [
        MODEL_GROUPS['BODY_NECK'],
        MODEL_GROUPS['BODY_CHEST'],
        MODEL_GROUPS['BODY_CHEST_W'],
        MODEL_GROUPS['BODY_CHEST_CHONK'],
        MODEL_GROUPS['BODY_CHEST_CHONK1'],
        MODEL_GROUPS['PIERCINGS_CHEST']
    ]
    
    model_data = get_models_by_groups(chest_groups)
    
    # Hide all chest models initially
    for group in chest_groups:
        if group in model_data:
            safe_hide_objects(model_data[group], hide=True)
    
    # Show appropriate models if chest toggle is enabled
    if tbse_properties['show_chest']:
        # Always show neck
        neck_models = model_data.get(MODEL_GROUPS['BODY_NECK'], [])
        if neck_models:
            safe_hide_objects(neck_models, hide=False)
        
        # Show appropriate chest models based on shape
        if chest_shape == 'w':
            safe_hide_objects(model_data.get(MODEL_GROUPS['BODY_CHEST_W'], []), hide=False)
        elif chest_shape == 'chonk':
            safe_hide_objects(model_data.get(MODEL_GROUPS['BODY_CHEST_CHONK'], []), hide=False)
        elif chest_shape in ['chonk1', 'cub']:
            safe_hide_objects(model_data.get(MODEL_GROUPS['BODY_CHEST_CHONK1'], []), hide=False)
        else:
            # Default to base TBSE chest models
            safe_hide_objects(model_data.get(MODEL_GROUPS['BODY_CHEST'], []), hide=False)
        
        # Handle chest piercings if enabled
        if tbse_properties['show_piercings_chest']:
            chestPiercingToggle(self, context)


def legToggle(self, context):
    # Toggle visibility of leg models
    tbse_properties = context.scene.tbse_kit_properties
    leg_shape = tbse_properties.leg_shape
    
    # Get all leg-related model groups efficiently  
    leg_groups = [
        MODEL_GROUPS['BODY_LEGS'],
        'body_legs_chonk',  # This seems to be a special case
        'body_genitals'     # This also seems to be special
    ]
    
    model_data = get_models_by_groups(leg_groups)
    
    # Hide all leg models initially
    for group in leg_groups:
        if group in model_data:
            safe_hide_objects(model_data[group], hide=True)
    
    # Show appropriate models if leg toggle is enabled
    if tbse_properties['show_legs']:
        genitals = model_data.get('body_genitals', [])
        
        if leg_shape == 'chonk':
            # Show chonk leg models and force AMAB genital toggle
            safe_hide_objects(model_data.get('body_legs_chonk', []), hide=False)
            setattr(tbse_properties, 'genital_toggle', 'amab')
        else:
            # Show base TBSE leg models
            safe_hide_objects(model_data.get(MODEL_GROUPS['BODY_LEGS'], []), hide=False)
            
            # Handle genital visibility based on genital toggle and XL shape
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
    
    # Trigger NSFW toggle check
    nsfwToggle(self, context)


def nsfwToggle(self, context):
    # Toggle visibility of NSFW models
    tbse_properties = context.scene.tbse_kit_properties
    modelDict = getTextBlock()

    # get object names of all nsfw models
    genitals_amab = getModelsInList(modelDict, "genitals_amab")
    genitals_afab = getModelsInList(modelDict, "genitals_afab")
    genitals_bpf = getModelsInList(modelDict, "genitals_bpf")
    piercings_amab = getModelsInList(modelDict, "piercings_amab")
    body_legs_chonk = getModelsInList(modelDict, "body_legs_chonk")

    # hides all nsfw models
    bpy.data.objects[body_legs_chonk[3]].hide_set(True)
    for obj in genitals_amab: bpy.data.objects[obj].hide_set(True)
    for obj in genitals_afab: bpy.data.objects[obj].hide_set(True)
    for obj in genitals_bpf: bpy.data.objects[obj].hide_set(True)
    for obj in piercings_amab: bpy.data.objects[obj].hide_set(True)

    # if NSFW TOGGLE enabled, show nsfw pieces -->
    if tbse_properties['show_nsfw']:
        if tbse_properties.leg_shape == 'chonk' and tbse_properties['show_legs']: # if LEG SHAPE is chonk, show chonk nsfw model
            bpy.data.objects[body_legs_chonk[3]].hide_set(False)
        else: # if LEG SHAPE is anything else, check nsfw logic
            genitalSet(self, context) 
        if tbse_properties['show_piercings_amab']: amabPiercingToggle(self, context)


def _simple_body_part_toggle(context, part_name: str, show_property: str):
    # Generic function for simple body part visibility toggles.
    tbse_properties = context.scene.tbse_kit_properties
    
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
    model_data = get_models_by_groups([model_group])
    models = model_data.get(model_group, [])
    
    # Toggle visibility based on property
    show = tbse_properties.get(show_property, False)
    safe_hide_objects(models, hide=not show)


def handToggle(self, context):
    """Toggle visibility of hand models."""
    _simple_body_part_toggle(context, 'hands', 'show_hands')


def feetToggle(self, context):
    """Toggle visibility of feet models.""" 
    _simple_body_part_toggle(context, 'feet', 'show_feet')


def bpfToggle(self, context):
    """Toggle visibility of BPF models."""
    _simple_body_part_toggle(context, 'bpf', 'show_bpf')


def genitalToggle(self, context):
    # Toggle between AMAB and AFAB genital types
    tbse_properties = context.scene.tbse_kit_properties
    modelDict = getTextBlock()

    # get object names of butt models
    body_genitals = getModelsInList(modelDict, "body_genitals")

    # hides all butt models
    for obj in body_genitals : bpy.data.objects[obj].hide_set(True)
    # if LEG SHAPE is chonk, don't toggle enable any other leg model
    if tbse_properties.leg_shape == 'chonk': return
    # if LEG SHAPE is xl OR genital toggle is AMAB, show AMAB leg model
    elif tbse_properties.genital_toggle == 'amab' or tbse_properties.leg_shape == 'xl':
        bpy.data.objects[body_genitals[0]].hide_set(False)
    # if toggle is AFAB, show AFAB leg model
    else: bpy.data.objects[body_genitals[1]].hide_set(False)
    # genital model logic
    genitalSet(self, context)


def bpfToggle(self, context):
    # Toggle visibility of BPF models with complex logic.
    tbse_properties = context.scene.tbse_kit_properties
    
    # Get BPF models efficiently
    model_data = get_models_by_groups(['genitals_bpf'])
    bpf_models = model_data.get('genitals_bpf', [])
    
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

    # get object names of all genital models
    genitals_amab = getModelsInList(modelDict, "genitals_amab")
    genitals_afab = getModelsInList(modelDict, "genitals_afab")
    genitals_bpf = getModelsInList(modelDict, "genitals_bpf")

    # hide all genital models
    for obj in genitals_amab: bpy.data.objects[obj].hide_set(True)
    for obj in genitals_afab: bpy.data.objects[obj].hide_set(True)
    for obj in genitals_bpf: bpy.data.objects[obj].hide_set(True)

    # if NSFW is enabled, show models -->
    if tbse_properties['show_nsfw'] and tbse_properties['show_legs']:
        # if AMAB enabled, OR if LEG SHAPE is xl or chonk, allow AMAB models to show
        if tbse_properties.genital_toggle == 'amab' or tbse_properties.leg_shape == 'xl' or tbse_properties.leg_shape == 'chonk':
            # find specific AMAB type through enum value
            # model name list includes same set of types
            amab_type = tbse_properties.bl_rna.properties.get('amab_type')
            obj = genitals_amab[amab_type.enum_items.find(tbse_properties.amab_type)]
        else:  # if AFAB enabled, allow AFAB models to show
            if tbse_properties.afab_type == 'bbwvr': obj = genitals_afab[0] # show seperate bbwvr model
            else: obj = genitals_afab[1] # if not bbwvr, show bibo genital model
            if tbse_properties['show_bpf'] : bpfToggle(self, context) # if BPF enabled, toggle bpf model
            # change bibo shape
            from .drivers import afab_driver
            afab_driver(self, context)


def boneToggles(self, context):
    # Toggle visibility of different bone layers
    tbse_properties = context.scene.tbse_kit_properties
    obj = bpy.data.objects["Skeleton"]
    skele = bpy.data.armatures["Skeleton"]

    if tbse_properties['show_armature']: obj.hide_set(False)
    else: obj.hide_set(True)

    if tbse_properties['show_base_bones']: skele.layers[0] = True
    else: skele.layers[0] = False

    if tbse_properties['show_skirt_bones']: skele.layers[1] = True
    else: skele.layers[1] = False

    if tbse_properties['show_extra_bones']: skele.layers[2] = True
    else: skele.layers[2] = False

    if tbse_properties.get('show_tail_bones'): skele.layers[3] = True
    else: skele.layers[3] = False

    if tbse_properties.get('show_ivcs_bones'): skele.layers[16] = True
    else: skele.layers[16] = False

    if tbse_properties.get('show_ivcs2_bones'): skele.layers[17] = True
    else: skele.layers[17] = False


def chestPiercingToggle(self, context):
    # Toggle visibility of chest piercing models
    tbse_properties = context.scene.tbse_kit_properties
    chest_toggles = context.scene.tbse_chest_toggles
    modelDict = getTextBlock()

    # hides all chest piercing models
    piercings_chest = getModelsInList(modelDict, "piercings_chest")
    for obj in piercings_chest: 
        bpy.data.objects[obj].hide_set(True)

    # goes through all properties in property group
    if tbse_properties['show_piercings_chest']:  # if chest piercings enabled -->
        for prop_name, prop in chest_toggles.bl_rna.properties.items():
            if type(prop) == bpy.types.BoolProperty:  # if prop is a bool -->
                if getattr(chest_toggles, prop_name):  # if bool is true -->
                    obj = modelDict['piercings_chest'][prop_name]
                    bpy.data.objects[obj].hide_set(False)  # show piercing model


def amabPiercingToggle(self, context):
    # Toggle visibility of amab piercing models
    tbse_properties = context.scene.tbse_kit_properties
    amab_toggles = context.scene.tbse_amab_toggles
    modelDict = getTextBlock()

    # hides all amab piercing models
    piercings_amab = getModelsInList(modelDict, "piercings_amab")
    for obj in piercings_amab: 
        bpy.data.objects[obj].hide_set(True)

    # goes through all properties in property group
    if tbse_properties['show_piercings_amab']:  # if amab piercings enabled -->
        for prop_name, prop in amab_toggles.bl_rna.properties.items():
            if type(prop) == bpy.types.BoolProperty:  # if prop is a bool ->
                if getattr(amab_toggles, prop_name):  # if bool is true ->
                    obj = modelDict['piercings_amab'][prop_name]
                    bpy.data.objects[obj].hide_set(False)  # show piercing model


def gearListToggle(isEnabled, gearList):
    # Helper function to toggle visibility of a gear list
    for obj in gearList:
        if isEnabled and obj.isEnabled: 
            obj.obj_pointer.hide_set(False)
        else: 
            obj.obj_pointer.hide_set(True)


def chestGearToggle(self, context):
    # Toggle visibility of chest gear
    tbse_properties = context.scene.tbse_kit_properties
    gear_list = context.scene.chest_gear_list
    gearListToggle(tbse_properties['show_chest_gear'], gear_list)


def legGearToggle(self, context):
    # Toggle visibility of leg gear
    tbse_properties = context.scene.tbse_kit_properties
    gear_list = context.scene.leg_gear_list
    gearListToggle(tbse_properties['show_leg_gear'], gear_list)


def handGearToggle(self, context):
    # Toggle visibility of hand gear
    tbse_properties = context.scene.tbse_kit_properties
    gear_list = context.scene.hand_gear_list
    gearListToggle(tbse_properties['show_hand_gear'], gear_list)


def feetGearToggle(self, context):
    # Toggle visibility of feet gear
    tbse_properties = context.scene.tbse_kit_properties
    gear_list = context.scene.feet_gear_list
    gearListToggle(tbse_properties['show_feet_gear'], gear_list)


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
