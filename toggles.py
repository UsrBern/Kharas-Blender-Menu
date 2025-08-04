# Toggle functions for TBSE Body Kit addon
# These functions handle visibility toggles for various gear and piercing models
import bpy
from .json_helpers import getTextBlock, getModelsInList, setTextBlock, setModelName


def chestToggle(self, context):
    # Toggle visibility of chest models
    tbse_properties = context.scene.tbse_kit_properties
    chest_shape = tbse_properties.chest_shape
    modelDict = getTextBlock()

    # get object names of all chest models
    tbse_neck = getModelsInList(modelDict, "body_neck")
    body_chest = getModelsInList(modelDict, "body_chest")
    body_chest_w = getModelsInList(modelDict, "body_chest_w")
    body_chest_chonk = getModelsInList(modelDict, "body_chest_chonk")
    body_chest_chonk1 = getModelsInList(modelDict, "body_chest_chonk1")
    piercings_chest = getModelsInList(modelDict, "piercings_chest")
    
    # hides all chest models
    bpy.data.objects[tbse_neck[0]].hide_set(True)
    for obj in body_chest: bpy.data.objects[obj].hide_set(True)
    for obj in body_chest_w: bpy.data.objects[obj].hide_set(True)
    for obj in body_chest_chonk: bpy.data.objects[obj].hide_set(True)
    for obj in body_chest_chonk1: bpy.data.objects[obj].hide_set(True)
    for obj in piercings_chest: bpy.data.objects[obj].hide_set(True)

    # if CHEST TOGGLE enabled, show chest pieces -->
    if tbse_properties['show_chest']:
        bpy.data.objects[tbse_neck[0]].hide_set(False) # enable neck
        if chest_shape == 'w': # if CHEST SHAPE is type w, show type w body models
            for obj in body_chest_w: bpy.data.objects[obj].hide_set(False)
        elif chest_shape == 'chonk': # if CHEST SHAPE is chonk, show chonk body models
            for obj in body_chest_chonk: bpy.data.objects[obj].hide_set(False)
        elif chest_shape == 'chonk1' or chest_shape == 'cub': #if CHEST SHAPE is chonk 1.0 or cub, show other chonk body models
            for obj in body_chest_chonk1: bpy.data.objects[obj].hide_set(False)
        else: # if CHEST SHAPE is anything else, show base tbse body models
            for obj in body_chest: bpy.data.objects[obj].hide_set(False)
        if tbse_properties['show_piercings_chest']: chestPiercingToggle(self, context)


def legToggle(self, context):
    # Toggle visibility of leg models
    tbse_properties = context.scene.tbse_kit_properties
    leg_shape = tbse_properties.leg_shape
    modelDict = getTextBlock()

    # get object names of all leg models
    body_legs = getModelsInList(modelDict, "body_legs")
    body_legs_chonk = getModelsInList(modelDict, "body_legs_chonk")
    body_genitals = getModelsInList(modelDict, "body_genitals")

    # hides all leg models
    for obj in body_legs: bpy.data.objects[obj].hide_set(True)
    for obj in body_legs_chonk: bpy.data.objects[obj].hide_set(True)
    for obj in body_genitals: bpy.data.objects[obj].hide_set(True)

    # if LEG TOGGLE enabled, show leg pieces -->
    if tbse_properties['show_legs']:
        if leg_shape == 'chonk' : # if LEG SHAPE is chonk, show chonk leg models
            for obj in body_legs_chonk: bpy.data.objects[obj].hide_set(False)
            setattr(tbse_properties,'genital_toggle','amab') # force set genital toggles to amab
        else: # if LEG SHAPE is anything else, show base tbse leg models
            for obj in body_legs: bpy.data.objects[obj].hide_set(False)
            # if LEG SHAPE is tbse xl, force amab legs and genital toggles
            if tbse_properties.genital_toggle == 'amab' or leg_shape == 'xl':
                if leg_shape == 'xl': setattr(tbse_properties,'genital_toggle','amab')
                bpy.data.objects[body_genitals[0]].hide_set(False) # body_genitals[0] = AMAB butt
            else: bpy.data.objects[body_genitals[1]].hide_set(False) # body_genitals[1] = AFAB butt
    # else: setattr(tbse_properties,'show_nsfw',False)
    nsfwToggle(self, context) # check nsfw toggles


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


def handToggle(self, context):
    # Toggle visibility of hand models
    tbse_properties = context.scene.tbse_kit_properties
    modelDict = getTextBlock()

    body_hands = getModelsInList(modelDict, "body_hands")
    if tbse_properties['show_hands']:
        bpy.data.objects[body_hands[0]].hide_set(False)
    else: 
        bpy.data.objects[body_hands[0]].hide_set(True)


def feetToggle(self, context):
    # Toggle visibility of feet models
    tbse_properties = context.scene.tbse_kit_properties
    modelDict = getTextBlock()
    
    body_feet = getModelsInList(modelDict, "body_feet")
    if tbse_properties['show_feet']:
        bpy.data.objects[body_feet[0]].hide_set(False)
    else: 
        bpy.data.objects[body_feet[0]].hide_set(True)


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
    # Toggle visibility of BPF models
    tbse_properties = context.scene.tbse_kit_properties
    modelDict = getTextBlock()

    # get object names of bpf models
    genitals_bpf = getModelsInList(modelDict, "genitals_bpf")

    # if LEG SHAPE is chonk or xl, do nothing
    if tbse_properties.leg_shape == 'chonk' or tbse_properties.leg_shape == 'xl':
        return
    # if NSFW is enabled, and if BPF is enabled, and genital toggle is on AFAB, show BPF model
    elif tbse_properties['show_nsfw'] and tbse_properties['show_bpf'] and tbse_properties.genital_toggle == 'afab':
        for obj in genitals_bpf: bpy.data.objects[obj].hide_set(False)
    else: 
        for obj in genitals_bpf: bpy.data.objects[obj].hide_set(True)


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
