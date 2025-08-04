# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTIBILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

from typing import Dict, List, Optional

# Author Addendum: 
#   You will not find this useful, it's trash code, im so sorry.

"""
TBSE Body Kit Blender Addon

This addon provides a free and open-source toolkit for working with TBSE body models in Blender.
Features include:
- Toggling visibility of body parts and gear
- Managing shape keys for multiple body types
- Importing and exporting FBX files with optimal settings for modding
- Bulk renaming and management of models
- Advanced options for piercings, NSFW toggles, and bone groups

Usage:
- Install via Blender's Add-ons menu
- Access via View3D > Sidebar > Body Kit

Author: Crow (FOSS version)
Maintainers: Community
License: GPLv3

For help and documentation, see the README.md or ask in the project repository.
"""

bl_info = {
    "name": "TBSE Body Kit",
    "author": "Crow",
    "description": "Script to be used in conjunction with TBSE Upscale Kit. Includes multiple TBSE bodies.",
    "blender": (2, 80, 0),
    "version": (1, 0, 0),
    "location": "View3D > Sidebar > Body Kit",
}

import bpy
import os
from bpy.props import (BoolProperty,
                       EnumProperty,
                       IntProperty,
                       StringProperty,
                       PointerProperty,
                       CollectionProperty)
from bpy.types import (PropertyGroup,
                       Operator,
                       Panel,
                       UIList,
                       Scene,
                       Menu)

from bpy_extras.io_utils import (ImportHelper,
                                 ExportHelper)
from operators import (
    TBSEKIT_OT_setToDefault,
    TBSEKIT_OT_rename,
    TBSEKIT_OT_importFBX,
    TBSEKIT_OT_exportFBX,
    TBSEKIT_UL_chestGear,
    TBSEKIT_UL_legGear,
    TBSEKIT_UL_handGear,
    TBSEKIT_UL_feetGear,
    TBSEKIT_OT_chestGearAdd,
    TBSEKIT_OT_chestGearRemove,
    TBSEKIT_OT_legGearAdd,
    TBSEKIT_OT_legGearRemove,
    TBSEKIT_OT_handGearAdd,
    TBSEKIT_OT_handGearRemove,
    TBSEKIT_OT_feetGearAdd,
    TBSEKIT_OT_feetGearRemove,
    cleanImport
)
import json
import pathlib

# ==================== #
#   FEATURES + PLANS   #
# ==================== #

# reset to default tbse [DONE]
# hide body parts [DONE]
# all shape keys [DONE]
    # seperate ones for top + bottoms [DONE]
# AMAB + AFAB options [DONE]
    # BPF toggle [DONE]
    # flaccid + erect versions?
# hide piercings/piercing options [DONE]

# importing and exporting: 
    # import settings [DONE]
        # fix bone rotation
        # clearing parents
        # fixing alpha
        # fixing metallic
    # importing automatically assigns the right armature [DONE]
    # export settings [DONE]
        # putting bone rotation back to usual xiv models
    # batch export [TBD]
        # exports all gear options and shapekeys 
        # pick name + iteration

# advanced : 
    # change namings [DONE]
    # adding shapekeys and drivers to new objects/gear [DONE]
    # bone groups [DONE]

# Other to-dos
    # add tbse w models [DONE]
    # add updated chonk models + shapes [DONE]
    # ivcs but with modifiers >:3
    # fucking fix my other modifiers too dumb ass corvid [DONE]
    # add squished amab nsfw option [DONE]

# ==================== #
#   RESET TO DEFAULT   #
# ==================== #

# Resets the blender scene to:
    # Chest, Legs, Hand, and Feet ENABLED
    # NSFW DISABLED
    # TBSE chest shape
    # TBSE leg shape
    # AMAB genital type - Gen A

    # hide chest piercings
    # hide amab piercings

# ================= #
#   MODEL TOGGLES   #
# ================= #

# Toggle visibility of all chest-related models based on user settings.

# - Hides all chest models by default.
# - Shows specific chest models depending on the selected chest shape.
# - Handles piercings if enabled.

# Args:
#     self: The property group or operator instance.
#     context: The Blender context.
def chestToggle(self, context):
    tbse_properties = context.scene.tbse_kit_properties
    chest_shape = tbse_properties.chest_shape
    modelDict = getTextBlock()

    # Get object names of all chest models
    tbse_neck = getModelsInList(modelDict, "body_neck")
    body_chest = getModelsInList(modelDict, "body_chest")
    body_chest_w = getModelsInList(modelDict, "body_chest_w")
    body_chest_chonk = getModelsInList(modelDict, "body_chest_chonk")
    body_chest_chonk1 = getModelsInList(modelDict, "body_chest_chonk1")
    piercings_chest = getModelsInList(modelDict, "piercings_chest")
    
    # Hide all chest models
    bpy.data.objects[tbse_neck[0]].hide_set(True)
    for obj in body_chest: bpy.data.objects[obj].hide_set(True)
    for obj in body_chest_w: bpy.data.objects[obj].hide_set(True)
    for obj in body_chest_chonk: bpy.data.objects[obj].hide_set(True)
    for obj in body_chest_chonk1: bpy.data.objects[obj].hide_set(True)
    for obj in piercings_chest: bpy.data.objects[obj].hide_set(True)

    # Show chest pieces if enabled
    if tbse_properties['show_chest']:
        bpy.data.objects[tbse_neck[0]].hide_set(False) # Enable neck
        if chest_shape == 'w':
            for obj in body_chest_w: bpy.data.objects[obj].hide_set(False)
        elif chest_shape == 'chonk':
            for obj in body_chest_chonk: bpy.data.objects[obj].hide_set(False)
        elif chest_shape in ('chonk1', 'cub'):
            for obj in body_chest_chonk1: bpy.data.objects[obj].hide_set(False)
        else:
            for obj in body_chest: bpy.data.objects[obj].hide_set(False)
        if tbse_properties['show_piercings_chest']:
            chestPiercingToggle(self, context)

def legToggle(self, context):
    """
    Toggle visibility of all leg-related models based on user settings.
    """
    tbse_properties = context.scene.tbse_kit_properties
    leg_shape = tbse_properties.leg_shape
    modelDict = getTextBlock()
    body_legs = getModelsInList(modelDict, "body_legs")
    body_legs_chonk = getModelsInList(modelDict, "body_legs_chonk")
    body_genitals = getModelsInList(modelDict, "body_genitals")
    # Hide all leg models
    for obj in body_legs:
        if obj in bpy.data.objects:
            bpy.data.objects[obj].hide_set(True)
    for obj in body_legs_chonk:
        if obj in bpy.data.objects:
            bpy.data.objects[obj].hide_set(True)
    for obj in body_genitals:
        if obj in bpy.data.objects:
            bpy.data.objects[obj].hide_set(True)
    # Show leg pieces if enabled
    if tbse_properties['show_legs']:
        if leg_shape == 'chonk':
            for obj in body_legs_chonk:
                if obj in bpy.data.objects:
                    bpy.data.objects[obj].hide_set(False)
            setattr(tbse_properties, 'genital_toggle', 'amab')
        else:
            for obj in body_legs:
                if obj in bpy.data.objects:
                    bpy.data.objects[obj].hide_set(False)
            # If LEG SHAPE is tbse xl, force amab legs and genital toggles
            if tbse_properties.genital_toggle == 'amab' or leg_shape == 'xl':
                if leg_shape == 'xl':
                    setattr(tbse_properties, 'genital_toggle', 'amab')
                if body_genitals and body_genitals[0] in bpy.data.objects:
                    bpy.data.objects[body_genitals[0]].hide_set(False)
            else:
                if body_genitals and len(body_genitals) > 1 and body_genitals[1] in bpy.data.objects:
                    bpy.data.objects[body_genitals[1]].hide_set(False)
    # Update NSFW toggles after leg logic
    nsfwToggle(self, context)

def nsfwToggle(self, context):
    """
    Toggle visibility of all NSFW-related models based on user settings.
    """
    tbse_properties = context.scene.tbse_kit_properties
    modelDict = getTextBlock()
    genitals_amab = getModelsInList(modelDict, "genitals_amab")
    genitals_afab = getModelsInList(modelDict, "genitals_afab")
    genitals_bpf = getModelsInList(modelDict, "genitals_bpf")
    piercings_amab = getModelsInList(modelDict, "piercings_amab")
    body_legs_chonk = getModelsInList(modelDict, "body_legs_chonk")
    if body_legs_chonk and len(body_legs_chonk) > 3 and body_legs_chonk[3] in bpy.data.objects:
        bpy.data.objects[body_legs_chonk[3]].hide_set(True)
    for obj in genitals_amab:
        if obj in bpy.data.objects:
            bpy.data.objects[obj].hide_set(True)
    for obj in genitals_afab:
        if obj in bpy.data.objects:
            bpy.data.objects[obj].hide_set(True)
    for obj in genitals_bpf:
        if obj in bpy.data.objects:
            bpy.data.objects[obj].hide_set(True)
    for obj in piercings_amab:
        if obj in bpy.data.objects:
            bpy.data.objects[obj].hide_set(True)
    # Show NSFW pieces if enabled
    if tbse_properties['show_nsfw']:
        if tbse_properties.leg_shape == 'chonk' and tbse_properties['show_legs']:
            if body_legs_chonk and len(body_legs_chonk) > 3 and body_legs_chonk[3] in bpy.data.objects:
                bpy.data.objects[body_legs_chonk[3]].hide_set(False)
        else:
            genitalSet(self, context)
        if tbse_properties['show_piercings_amab']:
            amabPiercingToggle(self, context)

def handToggle(self, context):
    """
    Toggle visibility of hand models based on user settings.
    """
    tbse_properties = context.scene.tbse_kit_properties
    modelDict = getTextBlock()
    body_hands = getModelsInList(modelDict, "body_hands")
    if body_hands and body_hands[0] in bpy.data.objects:
        bpy.data.objects[body_hands[0]].hide_set(not tbse_properties['show_hands'])

def feetGearToggle(self, context) -> None:
    """
    Toggle visibility of feet gear models in the scene based on the property value.
    Args:
        self: The property group instance.
        context: Blender context.
    """
    tbse_properties = context.scene.tbse_kit_properties
    feet_list = context.scene.feet_gear_list
    show_feet_gear = tbse_properties.show_feet_gear
    for item in feet_list:
        obj = item.obj_pointer
        if obj:
            obj.hide_set(not show_feet_gear)

def genitalToggle(self, context):
    """
    Toggle visibility of genital models based on user settings and leg shape.
    """
    tbse_properties = context.scene.tbse_kit_properties
    modelDict = getTextBlock()
    body_genitals = getModelsInList(modelDict, "body_genitals")
    for obj in body_genitals:
        if obj in bpy.data.objects:
            bpy.data.objects[obj].hide_set(True)
    if tbse_properties.leg_shape == 'chonk':
        return
    elif tbse_properties.genital_toggle == 'amab' or tbse_properties.leg_shape == 'xl':
        if body_genitals and body_genitals[0] in bpy.data.objects:
            bpy.data.objects[body_genitals[0]].hide_set(False)
    else:
        if body_genitals and len(body_genitals) > 1 and body_genitals[1] in bpy.data.objects:
            bpy.data.objects[body_genitals[1]].hide_set(False)
    genitalSet(self, context)

def bpfToggle(self, context):
    """
    Toggle visibility of BPF (body part fusion) models based on user settings.
    """
    tbse_properties = context.scene.tbse_kit_properties
    modelDict = getTextBlock()
    genitals_bpf = getModelsInList(modelDict, "genitals_bpf")
    if tbse_properties.leg_shape == 'chonk' or tbse_properties.leg_shape == 'xl':
        return
    elif tbse_properties['show_nsfw'] and tbse_properties['show_bpf'] and tbse_properties.genital_toggle == 'afab':
        for obj in genitals_bpf:
            if obj in bpy.data.objects:
                bpy.data.objects[obj].hide_set(False)
    else:
        for obj in genitals_bpf:
            if obj in bpy.data.objects:
                bpy.data.objects[obj].hide_set(True)

def genitalSet(self, context):
    """
    Set visibility of all genital models based on NSFW and leg settings.
    """
    tbse_properties = context.scene.tbse_kit_properties
    modelDict = getTextBlock()
    genitals_amab = getModelsInList(modelDict, "genitals_amab")
    genitals_afab = getModelsInList(modelDict, "genitals_afab")
    genitals_bpf = getModelsInList(modelDict, "genitals_bpf")
    for obj in genitals_amab:
        if obj in bpy.data.objects:
            bpy.data.objects[obj].hide_set(True)
    for obj in genitals_afab:
        if obj in bpy.data.objects:
            bpy.data.objects[obj].hide_set(True)
    for obj in genitals_bpf:
        if obj in bpy.data.objects:
            bpy.data.objects[obj].hide_set(True)
    if tbse_properties['show_nsfw'] and tbse_properties['show_legs']:
        # If AMAB enabled, or LEG SHAPE is xl or chonk, allow AMAB models to show
        if tbse_properties.genital_toggle == 'amab' or tbse_properties.leg_shape in ('xl', 'chonk'):
            # Find specific AMAB type through enum value
            amab_type_enum = tbse_properties.bl_rna.properties.get('amab_type')
            if amab_type_enum:
                index = amab_type_enum.enum_items.find(tbse_properties.amab_type)
                if genitals_amab and index < len(genitals_amab) and genitals_amab[index] in bpy.data.objects:
                    obj = genitals_amab[index]
                    bpy.data.objects[obj].hide_set(False)
        else:
            if tbse_properties.afab_type == 'bbwvr':
                if genitals_afab and genitals_afab[0] in bpy.data.objects:
                    obj = genitals_afab[0]
                    bpy.data.objects[obj].hide_set(False)
            else:
                if genitals_afab and len(genitals_afab) > 1 and genitals_afab[1] in bpy.data.objects:
                    obj = genitals_afab[1]
                    bpy.data.objects[obj].hide_set(False)
            if tbse_properties['show_bpf']:
                bpfToggle(self, context)
            afab_driver(self, context)

def chestPiercingToggle(self, context):
    """
    Toggle visibility of chest piercing models based on user settings.
    """
    tbse_properties = context.scene.tbse_kit_properties
    chest_toggles = context.scene.tbse_chest_toggles
    modelDict = getTextBlock()
    piercings_chest = getModelsInList(modelDict, "piercings_chest")
    for obj in piercings_chest:
        if obj in bpy.data.objects:
            bpy.data.objects[obj].hide_set(True)
    if tbse_properties['show_piercings_chest']:
        for prop_name, prop in chest_toggles.bl_rna.properties.items():
            if isinstance(prop, bpy.types.BoolProperty):
                if getattr(chest_toggles, prop_name):
                    if prop_name in modelDict['piercings_chest']:
                        obj = modelDict['piercings_chest'][prop_name]
                        if obj in bpy.data.objects:
                            bpy.data.objects[obj].hide_set(False)

def amabPiercingToggle(self, context):
    """
    Toggle visibility of AMAB piercing models based on user settings.
    """
    tbse_properties = context.scene.tbse_kit_properties
    amab_toggles = context.scene.tbse_amab_toggles
    modelDict = getTextBlock()
    piercings_amab = getModelsInList(modelDict, "piercings_amab")
    for obj in piercings_amab:
        if obj in bpy.data.objects:
            bpy.data.objects[obj].hide_set(True)
    if tbse_properties['show_piercings_amab']:
        for prop_name, prop in amab_toggles.bl_rna.properties.items():
            if isinstance(prop, bpy.types.BoolProperty):
                if getattr(amab_toggles, prop_name):
                    if prop_name in modelDict['piercings_amab']:
                        obj = modelDict['piercings_amab'][prop_name]
                        if obj in bpy.data.objects:
                            bpy.data.objects[obj].hide_set(False)


# gear list toggles
def gearListToggle(isEnabled, gearList):
    for obj in gearList:
        if isEnabled and obj.isEnabled: obj.obj_pointer.hide_set(False)
        else: obj.obj_pointer.hide_set(True)

def chestGearToggle(self,context):
    tbse_properties = context.scene.tbse_kit_properties
    gear_list = context.scene.chest_gear_list
    gearListToggle(tbse_properties['show_chest_gear'], gear_list)

def legGearToggle(self,context):
    tbse_properties = context.scene.tbse_kit_properties
    gear_list = context.scene.leg_gear_list
    gearListToggle(tbse_properties['show_leg_gear'],gear_list)

def handGearToggle(self,context):
    tbse_properties = context.scene.tbse_kit_properties
    gear_list = context.scene.hand_gear_list
    gearListToggle(tbse_properties['show_hand_gear'],gear_list)

def feetGearToggle(self, context) -> None:
    """
    Toggle visibility of feet gear models in the scene based on the property value.
    Args:
        self: The property group instance.
        context: Blender context.
    """
    tbse_properties = context.scene.tbse_kit_properties
    feet_list = context.scene.feet_gear_list
    show_feet_gear = tbse_properties.show_feet_gear
    for item in feet_list:
        obj = item.obj_pointer
        if obj:
            obj.hide_set(not show_feet_gear)

#induvidual gear toggles
def gearToggle(self, context) -> None:
    """
    Toggle visibility of individual gear items in the UI list.
    Args:
        self: The PropertyGroup item (e.g., ChestListItem, LegListItem, etc.).
        context: Blender context.
    """
    obj = self.obj_pointer
    if obj:
        obj.hide_set(not self.isEnabled)

# bone visibility toggles
def boneToggles(self, context) -> None:
    """
    Toggle visibility of bone groups in the armature based on property values.
    Args:
        self: The property group instance.
        context: Blender context.
    """
    tbse_properties = context.scene.tbse_kit_properties
    armature = None
    # Find the armature in the scene
    for obj in context.scene.objects:
        if obj.type == 'ARMATURE':
            armature = obj
            break
    if not armature:
        return
    # Example: toggle bone layers (customize as needed)
    # This assumes bone groups are mapped to armature layers
    # You may need to adjust this logic for your specific rig
    armature.data.layers[0] = tbse_properties.show_base_bones
    armature.data.layers[1] = tbse_properties.show_skirt_bones
    armature.data.layers[2] = tbse_properties.show_tail_bones
    armature.data.layers[3] = tbse_properties.show_extra_bones
    # IVCS layers (example indices)
    armature.data.layers[16] = tbse_properties.show_ivcs_bones
    armature.data.layers[17] = tbse_properties.show_ivcs2_bones


# ========================== #
#   DRIVERS FOR SHAPE KEYS   #
# ========================== #

# Currently supported bodies:
    # TBSE
    # Slim
    # Type W
    # SBTL
    # SBTL-slimmer
    # Twink
    # Twunk
    # Offseason Twunk
    # Hunk
    # Offseason Hunk
    # Chonk
    # Chonk 1.0
    # Cub
    # TBSE-XL
# AMAB and AFAB Toggles available for all except Chonk + TBSE-XL

# resets all chest shape keys back to TBSE (Basis)
def chest_resetDrivers ():
    for key in bpy.data.shape_keys["Chest Master"].key_blocks:
        key.value = 0

def chest_driver(self, context):
    tbse_properties = context.scene.tbse_kit_properties
    modelDict = getTextBlock()
    # reset shape before changing to another shape
    chest_resetDrivers()
    index = 0
    if not tbse_properties.chest_shape == 'tbse' : # if not default tbse, change shape depending on shape enum value
        chest_type = tbse_properties.bl_rna.properties.get('chest_shape')
        index = chest_type.enum_items.find(tbse_properties.chest_shape)
        bpy.data.shape_keys["Chest Master"].key_blocks[index].value = 1
    # chest model logic in case shape was changed to/from chonk or w
    chestToggle(self,context)

    # create list of object names of all models with chest shapekeys
    modelList = getModelsInList(modelDict, "body_chest")
    modelList.extend(getModelsInList(modelDict, "gear_chest"))
    modelList.extend(getModelsInList(modelDict, "gear_hands"))

    # change all objects with chest shapekeys to selected shape as active key
    chest_shape = tbse_properties.chest_shape
    for obj in modelList: 
        shp_index = index
        # if models are the elbows and wrists, change index to appropriate type
        if obj == modelList[1] or obj == modelList[2]:
            slim = ['slim','sbtl','sbtlslimmer']
            hunk = ['hunk','offhunk']
            if chest_shape in slim: shp_index = 1
            elif chest_shape in hunk: shp_index = 2
            elif chest_shape == 'xl': shp_index = 3
            else: shp_index = 0
        bpy.data.objects[obj].active_shape_key_index = shp_index

# resets all leg shape keys back to TBSE (Basis)
def leg_resetDrivers ():
    for key in bpy.data.shape_keys["Leg Master"].key_blocks:
        key.value = 0

def leg_driver(self, context):
    tbse_properties = context.scene.tbse_kit_properties
    modelDict = getTextBlock()

    # reset shape before changing to another shape
    leg_resetDrivers()
    index = 0
    if not tbse_properties.leg_shape == 'tbse' : # if not default tbse, change shape depending on shape enum value
        leg_type = tbse_properties.bl_rna.properties.get('leg_shape')
        index = leg_type.enum_items.find(tbse_properties.leg_shape)
        bpy.data.shape_keys["Leg Master"].key_blocks[index].value = 1
    # leg model logic in case shape was changed to or from chonk
    legToggle(self,context)

    # create list of object names of all models with leg shapekeys
    modelList = getModelsInList(modelDict, "body_legs")
    modelList.extend(getModelsInList(modelDict, "gear_legs"))
    modelList.extend(getModelsInList(modelDict, "gear_feet"))

    # change all objects with leg shapekeys to selected shape as active key
    leg_shape = tbse_properties.leg_shape
    for obj in modelList: 
        shp_index = index
        # if models are the shin and knee, change index to appropriate type
        if obj == modelList[0] or obj == modelList[1]:
            hunk_stbl = ['hunk','sbtl']
            if leg_shape in hunk_stbl: shp_index = 1
            elif leg_shape == 'xl': shp_index = 2
            else: shp_index = 0
        bpy.data.objects[obj].active_shape_key_index = shp_index

# resets all afab shape keys back to Gen A (Basis)
def afab_ResetDrivers():
    for key in bpy.data.shape_keys["AFAB Master"].key_blocks:
        key.value = 0

def afab_driver(self, conxtext):
    tbse_properties = conxtext.scene.tbse_kit_properties
    # resets shape before changing to another shape
    afab_ResetDrivers()
    if not tbse_properties.afab_type == 'a' : # if not default Gen A, change shape depending on shape enum value
        afab_shape = tbse_properties.bl_rna.properties.get('afab_type')
        index = afab_shape.enum_items.find(tbse_properties.afab_type)
        bpy.data.shape_keys["AFAB Master"].key_blocks[index].value = 1 
  

# =================== #
#   RENAMING MODELS   #
# =================== #

class TBSEKIT_OT_rename(Operator):
    bl_idname = "object.renaming"
    bl_label = "Rename"
    bl_description = "This allows for bulk renaming of models, changing all models to Part X.Z to Part Y.Z"
    bl_options = {'REGISTER','UNDO'}

    def execute(self, context):
        scene = context.scene
        tbse_properties =  scene.tbse_kit_properties
        partNumber = tbse_properties["partNumber"]
        rename = tbse_properties.rename_options
        # gets json code
        modelDict = getTextBlock()
        modelList = []
        
        if rename == 'chest': 
            # create a list of obj names
            modelList = getModelsInList(modelDict, "body_neck")
            modelList.extend(getModelsInList(modelDict, "body_chest"))
            modelList.extend(getModelsInList(modelDict, "body_chest_w"))
            modelList.extend(getModelsInList(modelDict, "body_chest_chonk"))
        if rename == 'legs':
            modelList = getModelsInList(modelDict, "body_legs")
            modelList.extend(getModelsInList(modelDict, "body_legs_chonk"))
            modelList.extend(getModelsInList(modelDict, "body_genitals"))
            modelList.extend(getModelsInList(modelDict, "genitals_amab"))
            modelList.extend(getModelsInList(modelDict, "genitals_afab"))
        if rename == 'hands': modelList = getModelsInList(modelDict, "body_hands")
        if rename == 'feet': modelList = getModelsInList(modelDict, "body_feet")
        if rename == 'chest_piercings': modelList = getModelsInList(modelDict, "piercings_chest")
        if rename == 'amab_piercings': modelList = getModelsInList(modelDict, "piercings_amab")
        if rename == 'bpf': modelList = getModelsInList(modelDict, "genitals_bpf")

        modelDict = renameModels(modelDict, modelList, partNumber)

        if rename == 'chest_gear': modelDict = renameGear(modelDict, scene.chest_gear_list, partNumber)
        if rename == 'leg_gear': modelDict = renameGear(modelDict, scene.leg_gear_list, partNumber)
        if rename == 'hand_gear': modelDict = renameGear(modelDict, scene.hand_gear_list, partNumber)
        if rename == 'feet_gear': modelDict = renameGear(modelDict, scene.feet_gear_list, partNumber)

        if rename == 'selected':
            selected_objects = context.selected_objects
            for obj in selected_objects:
                split = obj.name.lower()
                index = split.find("part") + 5
                new = obj.name[:index] + str(partNumber) + obj.name[index+1:]
                obj.name = new
        
        if not rename == 'selected': setTextBlock(modelDict)

        return {'FINISHED'}
    
def renameModels(modelDict, modelList, partNumber):
    for name in modelList: # list of obj names
        obj = bpy.data.objects[name]
        split = obj.name.lower()
        index = split.find("part") + 5
        new = obj.name[:index] + str(partNumber) + obj.name[index+1:]
        obj.name = setModelName(modelDict, obj.name, new)
    return modelDict

def renameGear(modelDict, itemlist, partNumber):
    for item in itemlist:
        obj = item.obj_pointer
        old = obj.name.lower()
        index = old.find("part") + 5
        new = obj.name[:index] + str(partNumber) + obj.name[index+1:]
        item.name = new
        item.model_name = new
        obj.name = setModelName(modelDict, obj.name, new)
    return modelDict

def modelNameChange(self,context):
    modelDict = getTextBlock()
    obj = self.obj_pointer
    if obj:
        obj.name = setModelName(modelDict, obj.name, self.model_name)
    setTextBlock(modelDict)


# ============= # 
#   FBX STUFF   #
# ============= #

class TBSEKIT_OT_importFBX(Operator, ImportHelper):
    bl_idname = "object.importfbx"
    bl_label = "Import FBX"
    bl_description = "Bulk import FBXs with optimal setting for XIV modding"
    bl_options = {'REGISTER','UNDO'}

    filter_glob: StringProperty(default='*.fbx',options={'HIDDEN'})

    files: CollectionProperty(
            type=bpy.types.OperatorFileListElement,
            options={'HIDDEN', 'SKIP_SAVE'},
        )
    
    # CUSTOM OPTIONS
    fix_skeleton: BoolProperty(
        default=True,
        name="Fix Skeleton",
        description="Rotates bones of skeleton to make them more readable when editing.")
    fix_materials: BoolProperty(
        default=True,
        name="Fix Materials",
        description="Changes all materials to 'Alpha Hashed' and fixes metalics")
    delete_junk: BoolProperty(
        default=True,
        name="Delete Junk",
        description="Deletes all empty objects, importing only the mesh and armature")
    auto_assign_armature: BoolProperty(
        default=True,
        name="Auto Assign Armature",
        description="Deletes the armature that comes with the fbx and assigns all meshes to existing skeleton.\nRecommended to disable ONLY if fbx skeleton includes ex_ bones")
    
    def draw(self, context):
        layout = self.layout

        layout.label(text="== CUSTOM SETTINGS ==")
        box = layout.box()
        box.prop(self, 'fix_skeleton')
        box.prop(self, 'fix_materials')
        box.prop(self, 'delete_junk')
        row = box.row()
        row.prop(self, 'auto_assign_armature')
        row = layout.row()
        row.label(text="I recommended keeping all options enabled!")
        row.enabled=False

    def execute(self, context):
        folder = os.path.dirname(self.filepath)

        # OPTIONAL SETTING: rotates bone axis on imported skeleton
        if self.fix_skeleton:
            primary_axis = 'X'
            second_axis = 'Y'
        else:
            primary_axis = 'Y'
            second_axis = 'X'

        for meshfile in self.files:
            filepath = (os.path.join(folder, meshfile.name))
            bpy.ops.import_scene.fbx(
                filepath=filepath,
                use_anim=False,
                force_connect_children=True,
                primary_bone_axis=primary_axis,
                secondary_bone_axis=second_axis
            )
            importedfiles = context.selected_objects
            cleanImport(self, importedfiles)

        return {'FINISHED'}
    
# =================== #
#   RENAMING MODELS   #
# =================== #

class TBSEKIT_OT_rename(Operator):
    bl_idname = "object.renaming"
    bl_label = "Rename"
    bl_description = "This allows for bulk renaming of models, changing all models to Part X.Z to Part Y.Z"
    bl_options = {'REGISTER','UNDO'}

    def execute(self, context):
        scene = context.scene
        tbse_properties =  scene.tbse_kit_properties
        partNumber = tbse_properties["partNumber"]
        rename = tbse_properties.rename_options
        # gets json code
        modelDict = getTextBlock()
        modelList = []
        
        if rename == 'chest': 
            # create a list of obj names
            modelList = getModelsInList(modelDict, "body_neck")
            modelList.extend(getModelsInList(modelDict, "body_chest"))
            modelList.extend(getModelsInList(modelDict, "body_chest_w"))
            modelList.extend(getModelsInList(modelDict, "body_chest_chonk"))
        if rename == 'legs':
            modelList = getModelsInList(modelDict, "body_legs")
            modelList.extend(getModelsInList(modelDict, "body_legs_chonk"))
            modelList.extend(getModelsInList(modelDict, "body_genitals"))
            modelList.extend(getModelsInList(modelDict, "genitals_amab"))
            modelList.extend(getModelsInList(modelDict, "genitals_afab"))
        if rename == 'hands': modelList = getModelsInList(modelDict, "body_hands")
        if rename == 'feet': modelList = getModelsInList(modelDict, "body_feet")
        if rename == 'chest_piercings': modelList = getModelsInList(modelDict, "piercings_chest")
        if rename == 'amab_piercings': modelList = getModelsInList(modelDict, "piercings_amab")
        if rename == 'bpf': modelList = getModelsInList(modelDict, "genitals_bpf")

        modelDict = renameModels(modelDict, modelList, partNumber)

        if rename == 'chest_gear': modelDict = renameGear(modelDict, scene.chest_gear_list, partNumber)
        if rename == 'leg_gear': modelDict = renameGear(modelDict, scene.leg_gear_list, partNumber)
        if rename == 'hand_gear': modelDict = renameGear(modelDict, scene.hand_gear_list, partNumber)
        if rename == 'feet_gear': modelDict = renameGear(modelDict, scene.feet_gear_list, partNumber)

        if rename == 'selected':
            selected_objects = context.selected_objects
            for obj in selected_objects:
                split = obj.name.lower()
                index = split.find("part") + 5
                new = obj.name[:index] + str(partNumber) + obj.name[index+1:]
                obj.name = new
        
        if not rename == 'selected': setTextBlock(modelDict)

        return {'FINISHED'}
    
def renameModels(modelDict, modelList, partNumber):
    for name in modelList: # list of obj names
        obj = bpy.data.objects[name]
        split = obj.name.lower()
        index = split.find("part") + 5
        new = obj.name[:index] + str(partNumber) + obj.name[index+1:]
        obj.name = setModelName(modelDict, obj.name, new)
    return modelDict

def renameGear(modelDict, itemlist, partNumber):
    for item in itemlist:
        obj = item.obj_pointer
        old = obj.name.lower()
        index = old.find("part") + 5
        new = obj.name[:index] + str(partNumber) + obj.name[index+1:]
        item.name = new
        item.model_name = new
        obj.name = setModelName(modelDict, obj.name, new)
    return modelDict

def modelNameChange(self,context):
    modelDict = getTextBlock()
    obj = self.obj_pointer
    if obj:
        obj.name = setModelName(modelDict, obj.name, self.model_name)
    setTextBlock(modelDict)


# ============= # 
#   FBX STUFF   #
# ============= #

class TBSEKIT_OT_importFBX(Operator, ImportHelper):
    bl_idname = "object.importfbx"
    bl_label = "Import FBX"
    bl_description = "Bulk import FBXs with optimal setting for XIV modding"
    bl_options = {'REGISTER','UNDO'}

    filter_glob: StringProperty(default='*.fbx',options={'HIDDEN'})

    files: CollectionProperty(
            type=bpy.types.OperatorFileListElement,
            options={'HIDDEN', 'SKIP_SAVE'},
        )
    
    # CUSTOM OPTIONS
    fix_skeleton: BoolProperty(
        default=True,
        name="Fix Skeleton",
        description="Rotates bones of skeleton to make them more readable when editing.")
    fix_materials: BoolProperty(
        default=True,
        name="Fix Materials",
        description="Changes all materials to 'Alpha Hashed' and fixes metalics")
    delete_junk: BoolProperty(
        default=True,
        name="Delete Junk",
        description="Deletes all empty objects, importing only the mesh and armature")
    auto_assign_armature: BoolProperty(
        default=True,
        name="Auto Assign Armature",
        description="Deletes the armature that comes with the fbx and assigns all meshes to existing skeleton.\nRecommended to disable ONLY if fbx skeleton includes ex_ bones")
    
    def draw(self, context):
        layout = self.layout

        layout.label(text="== CUSTOM SETTINGS ==")
        box = layout.box()
        box.prop(self, 'fix_skeleton')
        box.prop(self, 'fix_materials')
        box.prop(self, 'delete_junk')
        row = box.row()
        row.prop(self, 'auto_assign_armature')
        row = layout.row()
        row.label(text="I recommended keeping all options enabled!")
        row.enabled=False

    def execute(self, context):
        folder = os.path.dirname(self.filepath)

        # OPTIONAL SETTING: rotates bone axis on imported skeleton
        if self.fix_skeleton:
            primary_axis = 'X'
            second_axis = 'Y'
        else:
            primary_axis = 'Y'
            second_axis = 'X'

        for meshfile in self.files:
            filepath = (os.path.join(folder, meshfile.name))
            bpy.ops.import_scene.fbx(
                filepath=filepath,
                use_anim=False,
                force_connect_children=True,
                primary_bone_axis=primary_axis,
                secondary_bone_axis=second_axis
            )
            importedfiles = context.selected_objects
            cleanImport(self, importedfiles)

        return {'FINISHED'}
    
# =================== #
#   RENAMING MODELS   #
# =================== #

class TBSEKIT_OT_rename(Operator):
    bl_idname = "object.renaming"
    bl_label = "Rename"
    bl_description = "This allows for bulk renaming of models, changing all models to Part X.Z to Part Y.Z"
    bl_options = {'REGISTER','UNDO'}

    def execute(self, context):
        scene = context.scene
        tbse_properties =  scene.tbse_kit_properties
        partNumber = tbse_properties["partNumber"]
        rename = tbse_properties.rename_options
        # gets json code
        modelDict = getTextBlock()
        modelList = []
        
        if rename == 'chest': 
            # create a list of obj names
            modelList = getModelsInList(modelDict, "body_neck")
            modelList.extend(getModelsInList(modelDict, "body_chest"))
            modelList.extend(getModelsInList(modelDict, "body_chest_w"))
            modelList.extend(getModelsInList(modelDict, "body_chest_chonk"))
        if rename == 'legs':
            modelList = getModelsInList(modelDict, "body_legs")
            modelList.extend(getModelsInList(modelDict, "body_legs_chonk"))
            modelList.extend(getModelsInList(modelDict, "body_genitals"))
            modelList.extend(getModelsInList(modelDict, "genitals_amab"))
            modelList.extend(getModelsInList(modelDict, "genitals_afab"))
        if rename == 'hands': modelList = getModelsInList(modelDict, "body_hands")
        if rename == 'feet': modelList = getModelsInList(modelDict, "body_feet")
        if rename == 'chest_piercings': modelList = getModelsInList(modelDict, "piercings_chest")
        if rename == 'amab_piercings': modelList = getModelsInList(modelDict, "piercings_amab")
        if rename == 'bpf': modelList = getModelsInList(modelDict, "genitals_bpf")

        modelDict = renameModels(modelDict, modelList, partNumber)

        if rename == 'chest_gear': modelDict = renameGear(modelDict, scene.chest_gear_list, partNumber)
        if rename == 'leg_gear': modelDict = renameGear(modelDict, scene.leg_gear_list, partNumber)
        if rename == 'hand_gear': modelDict = renameGear(modelDict, scene.hand_gear_list, partNumber)
        if rename == 'feet_gear': modelDict = renameGear(modelDict, scene.feet_gear_list, partNumber)

        if rename == 'selected':
            selected_objects = context.selected_objects
            for obj in selected_objects:
                split = obj.name.lower()
                index = split.find("part") + 5
                new = obj.name[:index] + str(partNumber) + obj.name[index+1:]
                obj.name = new
        
        if not rename == 'selected': setTextBlock(modelDict)

        return {'FINISHED'}
    
def renameModels(modelDict, modelList, partNumber):
    for name in modelList: # list of obj names
        obj = bpy.data.objects[name]
        split = obj.name.lower()
        index = split.find("part") + 5
        new = obj.name[:index] + str(partNumber) + obj.name[index+1:]
        obj.name = setModelName(modelDict, obj.name, new)
    return modelDict

def renameGear(modelDict, itemlist, partNumber):
    for item in itemlist:
        obj = item.obj_pointer
        old = obj.name.lower()
        index = old.find("part") + 5
        new = obj.name[:index] + str(partNumber) + obj.name[index+1:]
        item.name = new
        item.model_name = new
        obj.name = setModelName(modelDict, obj.name, new)
    return modelDict

def modelNameChange(self,context):
    modelDict = getTextBlock()
    obj = self.obj_pointer
    if obj:
        obj.name = setModelName(modelDict, obj.name, self.model_name)
    setTextBlock(modelDict)


# ============= # 
#   FBX STUFF   #
# ============= #

class TBSEKIT_OT_importFBX(Operator, ImportHelper):
    bl_idname = "object.importfbx"
    bl_label = "Import FBX"
    bl_description = "Bulk import FBXs with optimal setting for XIV modding"
    bl_options = {'REGISTER','UNDO'}

    filter_glob: StringProperty(default='*.fbx',options={'HIDDEN'})

    files: CollectionProperty(
            type=bpy.types.OperatorFileListElement,
            options={'HIDDEN', 'SKIP_SAVE'},
        )
    
    # CUSTOM OPTIONS
    fix_skeleton: BoolProperty(
        default=True,
        name="Fix Skeleton",
        description="Rotates bones of skeleton to make them more readable when editing.")
    fix_materials: BoolProperty(
        default=True,
        name="Fix Materials",
        description="Changes all materials to 'Alpha Hashed' and fixes metalics")
    delete_junk: BoolProperty(
        default=True,
        name="Delete Junk",
        description="Deletes all empty objects, importing only the mesh and armature")
    auto_assign_armature: BoolProperty(
        default=True,
        name="Auto Assign Armature",
        description="Deletes the armature that comes with the fbx and assigns all meshes to existing skeleton.\nRecommended to disable ONLY if fbx skeleton includes ex_ bones")
    
    def draw(self, context):
        layout = self.layout

        layout.label(text="== CUSTOM SETTINGS ==")
        box = layout.box()
        box.prop(self, 'fix_skeleton')
        box.prop(self, 'fix_materials')
        box.prop(self, 'delete_junk')
        row = box.row()
        row.prop(self, 'auto_assign_armature')
        row = layout.row()
        row.label(text="I recommended keeping all options enabled!")
        row.enabled=False

    def execute(self, context):
        folder = os.path.dirname(self.filepath)

        # OPTIONAL SETTING: rotates bone axis on imported skeleton
        if self.fix_skeleton:
            primary_axis = 'X'
            second_axis = 'Y'
        else:
            primary_axis = 'Y'
            second_axis = 'X'

        for meshfile in self.files:
            filepath = (os.path.join(folder, meshfile.name))
            bpy.ops.import_scene.fbx(
                filepath=filepath,
                use_anim=False,
                force_connect_children=True,
                primary_bone_axis=primary_axis,
                secondary_bone_axis=second_axis
            )
            importedfiles = context.selected_objects
            cleanImport(self, importedfiles)

        return {'FINISHED'}
    
# =================== #
#   RENAMING MODELS   #
# =================== #

class TBSEKIT_OT_rename(Operator):
    bl_idname = "object.renaming"
    bl_label = "Rename"
    bl_description = "This allows for bulk renaming of models, changing all models to Part X.Z to Part Y.Z"
    bl_options = {'REGISTER','UNDO'}

    def execute(self, context):
        scene = context.scene
        tbse_properties =  scene.tbse_kit_properties
        partNumber = tbse_properties["partNumber"]
        rename = tbse_properties.rename_options
        # gets json code
        modelDict = getTextBlock()
        modelList = []
        
        if rename == 'chest': 
            # create a list of obj names
            modelList = getModelsInList(modelDict, "body_neck")
            modelList.extend(getModelsInList(modelDict, "body_chest"))
            modelList.extend(getModelsInList(modelDict, "body_chest_w"))
            modelList.extend(getModelsInList(modelDict, "body_chest_chonk"))
        if rename == 'legs':
            modelList = getModelsInList(modelDict, "body_legs")
            modelList.extend(getModelsInList(modelDict, "body_legs_chonk"))
            modelList.extend(getModelsInList(modelDict, "body_genitals"))
            modelList.extend(getModelsInList(modelDict, "genitals_amab"))
            modelList.extend(getModelsInList(modelDict, "genitals_afab"))
        if rename == 'hands': modelList = getModelsInList(modelDict, "body_hands")
        if rename == 'feet': modelList = getModelsInList(modelDict, "body_feet")
        if rename == 'chest_piercings': modelList = getModelsInList(modelDict, "piercings_chest")
        if rename == 'amab_piercings': modelList = getModelsInList(modelDict, "piercings_amab")
        if rename == 'bpf': modelList = getModelsInList(modelDict, "genitals_bpf")

        modelDict = renameModels(modelDict, modelList, partNumber)

        if rename == 'chest_gear': modelDict = renameGear(modelDict, scene.chest_gear_list, partNumber)
        if rename == 'leg_gear': modelDict = renameGear(modelDict, scene.leg_gear_list, partNumber)
        if rename == 'hand_gear': modelDict = renameGear(modelDict, scene.hand_gear_list, partNumber)
        if rename == 'feet_gear': modelDict = renameGear(modelDict, scene.feet_gear_list, partNumber)

        if rename == 'selected':
            selected_objects = context.selected_objects
            for obj in selected_objects:
                split = obj.name.lower()
                index = split.find("part") + 5
                new = obj.name[:index] + str(partNumber) + obj.name[index+1:]
                obj.name = new
        
        if not rename == 'selected': setTextBlock(modelDict)

        return {'FINISHED'}
    
def renameModels(modelDict, modelList, partNumber):
    for name in modelList: # list of obj names
        obj = bpy.data.objects[name]
        split = obj.name.lower()
        index = split.find("part") + 5
        new = obj.name[:index] + str(partNumber) + obj.name[index+1:]
        obj.name = setModelName(modelDict, obj.name, new)
    return modelDict

def renameGear(modelDict, itemlist, partNumber):
    for item in itemlist:
        obj = item.obj_pointer
        old = obj.name.lower()
        index = old.find("part") + 5
        new = obj.name[:index] + str(partNumber) + obj.name[index+1:]
        item.name = new
        item.model_name = new
        obj.name = setModelName(modelDict, obj.name, new)
    return modelDict

def modelNameChange(self,context):
    modelDict = getTextBlock()
    obj = self.obj_pointer
    if obj:
        obj.name = setModelName(modelDict, obj.name, self.model_name)
    setTextBlock(modelDict)


# ============= # 
#   FBX STUFF   #
# ============= #

class TBSEKIT_OT_importFBX(Operator, ImportHelper):
    bl_idname = "object.importfbx"
    bl_label = "Import FBX"
    bl_description = "Bulk import FBXs with optimal setting for XIV modding"
    bl_options = {'REGISTER','UNDO'}

    filter_glob: StringProperty(default='*.fbx',options={'HIDDEN'})

    files: CollectionProperty(
            type=bpy.types.OperatorFileListElement,
            options={'HIDDEN', 'SKIP_SAVE'},
        )
    
    # CUSTOM OPTIONS
    fix_skeleton: BoolProperty(
        default=True,
        name="Fix Skeleton",
        description="Rotates bones of skeleton to make them more readable when editing.")
    fix_materials: BoolProperty(
        default=True,
        name="Fix Materials",
        description="Changes all materials to 'Alpha Hashed' and fixes metalics")
    delete_junk: BoolProperty(
        default=True,
        name="Delete Junk",
        description="Deletes all empty objects, importing only the mesh and armature")
    auto_assign_armature: BoolProperty(
        default=True,
        name="Auto Assign Armature",
        description="Deletes the armature that comes with the fbx and assigns all meshes to existing skeleton.\nRecommended to disable ONLY if fbx skeleton includes ex_ bones")
    
    def draw(self, context):
        layout = self.layout

        layout.label(text="== CUSTOM SETTINGS ==")
        box = layout.box()
        box.prop(self, 'fix_skeleton')
        box.prop(self, 'fix_materials')
        box.prop(self, 'delete_junk')
        row = box.row()
        row.prop(self, 'auto_assign_armature')
        row = layout.row()
        row.label(text="I recommended keeping all options enabled!")
        row.enabled=False

    def execute(self, context):
        folder = os.path.dirname(self.filepath)

        # OPTIONAL SETTING: rotates bone axis on imported skeleton
        if self.fix_skeleton:
            primary_axis = 'X'
            second_axis = 'Y'
        else:
            primary_axis = 'Y'
            second_axis = 'X'

        for meshfile in self.files:
            filepath = (os.path.join(folder, meshfile.name))
            bpy.ops.import_scene.fbx(
                filepath=filepath,
                use_anim=False,
                force_connect_children=True,
                primary_bone_axis=primary_axis,
                secondary_bone_axis=second_axis
            )
            importedfiles = context.selected_objects
            cleanImport(self, importedfiles)

        return {'FINISHED'}
    
# =================== #
#   RENAMING MODELS   #
# =================== #

class TBSEKIT_OT_rename(Operator):
    bl_idname = "object.renaming"
    bl_label = "Rename"
    bl_description = "This allows for bulk renaming of models, changing all models to Part X.Z to Part Y.Z"
    bl_options = {'REGISTER','UNDO'}

    def execute(self, context):
        scene = context.scene
        tbse_properties =  scene.tbse_kit_properties
        partNumber = tbse_properties["partNumber"]
        rename = tbse_properties.rename_options
        # gets json code
        modelDict = getTextBlock()
        modelList = []
        
        if rename == 'chest': 
            # create a list of obj names
            modelList = getModelsInList(modelDict, "body_neck")
            modelList.extend(getModelsInList(modelDict, "body_chest"))
            modelList.extend(getModelsInList(modelDict, "body_chest_w"))
            modelList.extend(getModelsInList(modelDict, "body_chest_chonk"))
        if rename == 'legs':
            modelList = getModelsInList(modelDict, "body_legs")
            modelList.extend(getModelsInList(modelDict, "body_legs_chonk"))
            modelList.extend(getModelsInList(modelDict, "body_genitals"))
            modelList.extend(getModelsInList(modelDict, "genitals_amab"))
            modelList.extend(getModelsInList(modelDict, "genitals_afab"))
        if rename == 'hands': modelList = getModelsInList(modelDict, "body_hands")
        if rename == 'feet': modelList = getModelsInList(modelDict, "body_feet")
        if rename == 'chest_piercings': modelList = getModelsInList(modelDict, "piercings_chest")
        if rename == 'amab_piercings': modelList = getModelsInList(modelDict, "piercings_amab")
        if rename == 'bpf': modelList = getModelsInList(modelDict, "genitals_bpf")

        modelDict = renameModels(modelDict, modelList, partNumber)

        if rename == 'chest_gear': modelDict = renameGear(modelDict, scene.chest_gear_list, partNumber)
        if rename == 'leg_gear': modelDict = renameGear(modelDict, scene.leg_gear_list, partNumber)
        if rename == 'hand_gear': modelDict = renameGear(modelDict, scene.hand_gear_list, partNumber)
        if rename == 'feet_gear': modelDict = renameGear(modelDict, scene.feet_gear_list, partNumber)

        if rename == 'selected':
            selected_objects = context.selected_objects
            for obj in selected_objects:
                split = obj.name.lower()
                index = split.find("part") + 5
                new = obj.name[:index] + str(partNumber) + obj.name[index+1:]
                obj.name = new
        
        if not rename == 'selected': setTextBlock(modelDict)

        return {'FINISHED'}
    
def renameModels(modelDict, modelList, partNumber):
    for name in modelList: # list of obj names
        obj = bpy.data.objects[name]
        split = obj.name.lower()
        index = split.find("part") + 5
        new = obj.name[:index] + str(partNumber) + obj.name[index+1:]
        obj.name = setModelName(modelDict, obj.name, new)
    return modelDict

def renameGear(modelDict, itemlist, partNumber):
    for item in itemlist:
        obj = item.obj_pointer
        old = obj.name.lower()
        index = old.find("part") + 5
        new = obj.name[:index] + str(partNumber) + obj.name[index+1:]
        item.name = new
        item.model_name = new
        obj.name = setModelName(modelDict, obj.name, new)
    return modelDict

def modelNameChange(self,context):
    modelDict = getTextBlock()
    obj = self.obj_pointer
    if obj:
        obj.name = setModelName(modelDict, obj.name, self.model_name)
    setTextBlock(modelDict)


# ============= # 
#   FBX STUFF   #
# ============= #

class TBSEKIT_OT_importFBX(Operator, ImportHelper):
    bl_idname = "object.importfbx"
    bl_label = "Import FBX"
    bl_description = "Bulk import FBXs with optimal setting for XIV modding"
    bl_options = {'REGISTER','UNDO'}

    filter_glob: StringProperty(default='*.fbx',options={'HIDDEN'})

    files: CollectionProperty(
            type=bpy.types.OperatorFileListElement,
            options={'HIDDEN', 'SKIP_SAVE'},
        )
    
    # CUSTOM OPTIONS
    fix_skeleton: BoolProperty(
        default=True,
        name="Fix Skeleton",
        description="Rotates bones of skeleton to make them more readable when editing.")
    fix_materials: BoolProperty(
        default=True,
        name="Fix Materials",
        description="Changes all materials to 'Alpha Hashed' and fixes metalics")
    delete_junk: BoolProperty(
        default=True,
        name="Delete Junk",
        description="Deletes all empty objects, importing only the mesh and armature")
    auto_assign_armature: BoolProperty(
        default=True,
        name="Auto Assign Armature",
        description="Deletes the armature that comes with the fbx and assigns all meshes to existing skeleton.\nRecommended to disable ONLY if fbx skeleton includes ex_ bones")
    
    def draw(self, context):
        layout = self.layout

        layout.label(text="== CUSTOM SETTINGS ==")
        box = layout.box()
        box.prop(self, 'fix_skeleton')
        box.prop(self, 'fix_materials')
        box.prop(self, 'delete_junk')
        row = box.row()
        row.prop(self, 'auto_assign_armature')
        row = layout.row()
        row.label(text="I recommended keeping all options enabled!")
        row.enabled=False

    def execute(self, context):
        folder = os.path.dirname(self.filepath)

        # OPTIONAL SETTING: rotates bone axis on imported skeleton
        if self.fix_skeleton:
            primary_axis = 'X'
            second_axis = 'Y'
        else:
            primary_axis = 'Y'
            second_axis = 'X'

        for meshfile in self.files:
            filepath = (os.path.join(folder, meshfile.name))
            bpy.ops.import_scene.fbx(
                filepath=filepath,
                use_anim=False,
                force_connect_children=True,
                primary_bone_axis=primary_axis,
                secondary_bone_axis=second_axis
            )
            importedfiles = context.selected_objects
            cleanImport(self, importedfiles)

        return {'FINISHED'}
    
# =================== #
#   RENAMING MODELS   #
# =================== #

class TBSEKIT_OT_rename(Operator):
    bl_idname = "object.renaming"
    bl_label = "Rename"
    bl_description = "This allows for bulk renaming of models, changing all models to Part X.Z to Part Y.Z"
    bl_options = {'REGISTER','UNDO'}

    def execute(self, context):
        scene = context.scene
        tbse_properties =  scene.tbse_kit_properties
        partNumber = tbse_properties["partNumber"]
        rename = tbse_properties.rename_options
        # gets json code
        modelDict = getTextBlock()
        modelList = []
        
        if rename == 'chest': 
            # create a list of obj names
            modelList = getModelsInList(modelDict, "body_neck")
            modelList.extend(getModelsInList(modelDict, "body_chest"))
            modelList.extend(getModelsInList(modelDict, "body_chest_w"))
            modelList.extend(getModelsInList(modelDict, "body_chest_chonk"))
        if rename == 'legs':
            modelList = getModelsInList(modelDict, "body_legs")
            modelList.extend(getModelsInList(modelDict, "body_legs_chonk"))
            modelList.extend(getModelsInList(modelDict, "body_genitals"))
            modelList.extend(getModelsInList(modelDict, "genitals_amab"))
            modelList.extend(getModelsInList(modelDict, "genitals_afab"))
        if rename == 'hands': modelList = getModelsInList(modelDict, "body_hands")
        if rename == 'feet': modelList = getModelsInList(modelDict, "body_feet")
        if rename == 'chest_piercings': modelList = getModelsInList(modelDict, "piercings_chest")
        if rename == 'amab_piercings': modelList = getModelsInList(modelDict, "piercings_amab")
        if rename == 'bpf': modelList = getModelsInList(modelDict, "genitals_bpf")

        modelDict = renameModels(modelDict, modelList, partNumber)

        if rename == 'chest_gear': modelDict = renameGear(modelDict, scene.chest_gear_list, partNumber)
        if rename == 'leg_gear': modelDict = renameGear(modelDict, scene.leg_gear_list, partNumber)
        if rename == 'hand_gear': modelDict = renameGear(modelDict, scene.hand_gear_list, partNumber)
        if rename == 'feet_gear': modelDict = renameGear(modelDict, scene.feet_gear_list, partNumber)

        if rename == 'selected':
            selected_objects = context.selected_objects
            for obj in selected_objects:
                split = obj.name.lower()
                index = split.find("part") + 5
                new = obj.name[:index] + str(partNumber) + obj.name[index+1:]
                obj.name = new
        
        if not rename == 'selected': setTextBlock(modelDict)

        return {'FINISHED'}
    
def renameModels(modelDict, modelList, partNumber):
    for name in modelList: # list of obj names
        obj = bpy.data.objects[name]
        split = obj.name.lower()
        index = split.find("part") + 5
        new = obj.name[:index] + str(partNumber) + obj.name[index+1:]
        obj.name = setModelName(modelDict, obj.name, new)
    return modelDict

def renameGear(modelDict, itemlist, partNumber):
    for item in itemlist:
        obj = item.obj_pointer
        old = obj.name.lower()
        index = old.find("part") + 5
        new = obj.name[:index] + str(partNumber) + obj.name[index+1:]
        item.name = new
        item.model_name = new
        obj.name = setModelName(modelDict, obj.name, new)
    return modelDict

def modelNameChange(self,context):
    modelDict = getTextBlock()
    obj = self.obj_pointer
    if obj:
        obj.name = setModelName(modelDict, obj.name, self.model_name)
    setTextBlock(modelDict)


# ============= # 
#   FBX STUFF   #
# ============= #

class TBSEKIT_OT_importFBX(Operator, ImportHelper):
    bl_idname = "object.importfbx"
    bl_label = "Import FBX"
    bl_description = "Bulk import FBXs with optimal setting for XIV modding"
    bl_options = {'REGISTER','UNDO'}

    filter_glob: StringProperty(default='*.fbx',options={'HIDDEN'})

    files: CollectionProperty(
            type=bpy.types.OperatorFileListElement,
            options={'HIDDEN', 'SKIP_SAVE'},
        )
    
    # CUSTOM OPTIONS
    fix_skeleton: BoolProperty(
        default=True,
        name="Fix Skeleton",
        description="Rotates bones of skeleton to make them more readable when editing.")
    fix_materials: BoolProperty(
        default=True,
        name="Fix Materials",
        description="Changes all materials to 'Alpha Hashed' and fixes metalics")
    delete_junk: BoolProperty(
        default=True,
        name="Delete Junk",
        description="Deletes all empty objects, importing only the mesh and armature")
    auto_assign_armature: BoolProperty(
        default=True,
        name="Auto Assign Armature",
        description="Deletes the armature that comes with the fbx and assigns all meshes to existing skeleton.\nRecommended to disable ONLY if fbx skeleton includes ex_ bones")
    
    def draw(self, context):
        layout = self.layout

        layout.label(text="== CUSTOM SETTINGS ==")
        box = layout.box()
        box.prop(self, 'fix_skeleton')
        box.prop(self, 'fix_materials')
        box.prop(self, 'delete_junk')
        row = box.row()
        row.prop(self, 'auto_assign_armature')
        row = layout.row()
        row.label(text="I recommended keeping all options enabled!")
        row.enabled=False

    def execute(self, context):
        folder = os.path.dirname(self.filepath)

        # OPTIONAL SETTING: rotates bone axis on imported skeleton
        if self.fix_skeleton:
            primary_axis = 'X'
            second_axis = 'Y'
        else:
            primary_axis = 'Y'
            second_axis = 'X'

        for meshfile in self.files:
            filepath = (os.path.join(folder, meshfile.name))
            bpy.ops.import_scene.fbx(
                filepath=filepath,
                use_anim=False,
                force_connect_children=True,
                primary_bone_axis=primary_axis,
                secondary_bone_axis=second_axis
            )
            importedfiles = context.selected_objects
            cleanImport(self, importedfiles)

        return {'FINISHED'}
    
# =================== #
#   RENAMING MODELS   #
# =================== #

class TBSEKIT_OT_rename(Operator):
    bl_idname = "object.renaming"
    bl_label = "Rename"
    bl_description = "This allows for bulk renaming of models, changing all models to Part X.Z to Part Y.Z"
    bl_options = {'REGISTER','UNDO'}

    def execute(self, context):
        scene = context.scene
        tbse_properties =  scene.tbse_kit_properties
        partNumber = tbse_properties["partNumber"]
        rename = tbse_properties.rename_options
        # gets json code
        modelDict = getTextBlock()
        modelList = []
        
        if rename == 'chest': 
            # create a list of obj names
            modelList = getModelsInList(modelDict, "body_neck")
            modelList.extend(getModelsInList(modelDict, "body_chest"))
            modelList.extend(getModelsInList(modelDict, "body_chest_w"))
            modelList.extend(getModelsInList(modelDict, "body_chest_chonk"))
        if rename == 'legs':
            modelList = getModelsInList(modelDict, "body_legs")
            modelList.extend(getModelsInList(modelDict, "body_legs_chonk"))
            modelList.extend(getModelsInList(modelDict, "body_genitals"))
            modelList.extend(getModelsInList(modelDict, "genitals_amab"))
            modelList.extend(getModelsInList(modelDict, "genitals_afab"))
        if rename == 'hands': modelList = getModelsInList(modelDict, "body_hands")
        if rename == 'feet': modelList = getModelsInList(modelDict, "body_feet")
        if rename == 'chest_piercings': modelList = getModelsInList(modelDict, "piercings_chest")
        if rename == 'amab_piercings': modelList = getModelsInList(modelDict, "piercings_amab")
        if rename == 'bpf': modelList = getModelsInList(modelDict, "genitals_bpf")

        modelDict = renameModels(modelDict, modelList, partNumber)

        if rename == 'chest_gear': modelDict = renameGear(modelDict, scene.chest_gear_list, partNumber)
        if rename == 'leg_gear': modelDict = renameGear(modelDict, scene.leg_gear_list, partNumber)
        if rename == 'hand_gear': modelDict = renameGear(modelDict, scene.hand_gear_list, partNumber)
        if rename == 'feet_gear': modelDict = renameGear(modelDict, scene.feet_gear_list, partNumber)

        if rename == 'selected':
            selected_objects = context.selected_objects
            for obj in selected_objects:
                split = obj.name.lower()
                index = split.find("part") + 5
                new = obj.name[:index] + str(partNumber) + obj.name[index+1:]
                obj.name = new
        
        if not rename == 'selected': setTextBlock(modelDict)

        return {'FINISHED'}
    
def renameModels(modelDict, modelList, partNumber):
    for name in modelList: # list of obj names
        obj = bpy.data.objects[name]
        split = obj.name.lower()
        index = split.find("part") + 5
        new = obj.name[:index] + str(partNumber) + obj.name[index+1:]
        obj.name = setModelName(modelDict, obj.name, new)
    return modelDict

def renameGear(modelDict, itemlist, partNumber):
    for item in itemlist:
        obj = item.obj_pointer
        old = obj.name.lower()
        index = old.find("part") + 5
        new = obj.name[:index] + str(partNumber) + obj.name[index+1:]
        item.name = new
        item.model_name = new
        obj.name = setModelName(modelDict, obj.name, new)
    return modelDict

def modelNameChange(self,context):
    modelDict = getTextBlock()
    obj = self.obj_pointer
    if obj:
        obj.name = setModelName(modelDict, obj.name, self.model_name)
    setTextBlock(modelDict)


# ============= # 
#   FBX STUFF   #
# ============= #

class TBSEKIT_OT_importFBX(Operator, ImportHelper):
    bl_idname = "object.importfbx"
    bl_label = "Import FBX"
    bl_description = "Bulk import FBXs with optimal setting for XIV modding"
    bl_options = {'REGISTER','UNDO'}

    filter_glob: StringProperty(default='*.fbx',options={'HIDDEN'})

    files: CollectionProperty(
            type=bpy.types.OperatorFileListElement,
            options={'HIDDEN', 'SKIP_SAVE'},
        )
    
    # CUSTOM OPTIONS
    fix_skeleton: BoolProperty(
        default=True,
        name="Fix Skeleton",
        description="Rotates bones of skeleton to make them more readable when editing.")
    fix_materials: BoolProperty(
        default=True,
        name="Fix Materials",
        description="Changes all materials to 'Alpha Hashed' and fixes metalics")
    delete_junk: BoolProperty(
        default=True,
        name="Delete Junk",
        description="Deletes all empty objects, importing only the mesh and armature")
    auto_assign_armature: BoolProperty(
        default=True,
        name="Auto Assign Armature",
        description="Deletes the armature that comes with the fbx and assigns all meshes to existing skeleton.\nRecommended to disable ONLY if fbx skeleton includes ex_ bones")
    
    def draw(self, context):
        layout = self.layout

        layout.label(text="== CUSTOM SETTINGS ==")
        box = layout.box()
        box.prop(self, 'fix_skeleton')
        box.prop(self, 'fix_materials')
        box.prop(self, 'delete_junk')
        row = box.row()
        row.prop(self, 'auto_assign_armature')
        row = layout.row()
        row.label(text="I recommended keeping all options enabled!")
        row.enabled=False

    def execute(self, context):
        folder = os.path.dirname(self.filepath)

        # OPTIONAL SETTING: rotates bone axis on imported skeleton
        if self.fix_skeleton:
            primary_axis = 'X'
            second_axis = 'Y'
        else:
            primary_axis = 'Y'
            second_axis = 'X'

        for meshfile in self.files:
            filepath = (os.path.join(folder, meshfile.name))
            bpy.ops.import_scene.fbx(
                filepath=filepath,
                use_anim=False,
                force_connect_children=True,
                primary_bone_axis=primary_axis,
                secondary_bone_axis=second_axis
            )
            importedfiles = context.selected_objects
            cleanImport(self, importedfiles)

        return {'FINISHED'}
    
# =================== #
#   RENAMING MODELS   #
# =================== #

class TBSEKIT_OT_rename(Operator):
    bl_idname = "object.renaming"
    bl_label = "Rename"
    bl_description = "This allows for bulk renaming of models, changing all models to Part X.Z to Part Y.Z"
    bl_options = {'REGISTER','UNDO'}

    def execute(self, context):
        scene = context.scene
        tbse_properties =  scene.tbse_kit_properties
        partNumber = tbse_properties["partNumber"]
        rename = tbse_properties.rename_options
        # gets json code
        modelDict = getTextBlock()
        modelList = []
        
        if rename == 'chest': 
            # create a list of obj names
            modelList = getModelsInList(modelDict, "body_neck")
            modelList.extend(getModelsInList(modelDict, "body_chest"))
            modelList.extend(getModelsInList(modelDict, "body_chest_w"))
            modelList.extend(getModelsInList(modelDict, "body_chest_chonk"))
        if rename == 'legs':
            modelList = getModelsInList(modelDict, "body_legs")
            modelList.extend(getModelsInList(modelDict, "body_legs_chonk"))
            modelList.extend(getModelsInList(modelDict, "body_genitals"))
            modelList.extend(getModelsInList(modelDict, "genitals_amab"))
            modelList.extend(getModelsInList(modelDict, "genitals_afab"))
        if rename == 'hands': modelList = getModelsInList(modelDict, "body_hands")
        if rename == 'feet': modelList = getModelsInList(modelDict, "body_feet")
        if rename == 'chest_piercings': modelList = getModelsInList modelDict, "piercings_chest")
        if rename == 'amab_piercings': modelList = getModelsInList(modelDict, "piercings_amab")
        if rename == 'bpf': modelList = getModelsInList(modelDict, "genitals_bpf")

        modelDict = renameModels(modelDict, modelList, partNumber)

        if rename == 'chest_gear': modelDict = renameGear(modelDict, scene.chest_gear_list, partNumber)
        if rename == 'leg_gear': modelDict = renameGear(modelDict, scene.leg_gear_list, partNumber)
        if rename == 'hand_gear': modelDict = renameGear(modelDict, scene.hand_gear_list, partNumber)
        if rename == 'feet_gear': modelDict = renameGear(modelDict, scene.feet_gear_list, partNumber)

        if rename == 'selected':
            selected_objects = context.selected_objects
            for obj in selected_objects:
                split = obj.name.lower()
                index = split.find("part") + 5
                new = obj.name[:index] + str(partNumber) + obj.name[index+1:]
                obj.name = new
        
        if not rename == 'selected': setTextBlock(modelDict)

        return {'FINISHED'}
    
def renameModels(modelDict, modelList, partNumber):
    for name in modelList: # list of obj names
        obj = bpy.data.objects[name]
        split = obj.name.lower()
        index = split.find("part") + 5
        new = obj.name[:index] + str(partNumber) + obj.name[index+1:]
        obj.name = setModelName(modelDict, obj.name, new)
    return modelDict

def renameGear(modelDict, itemlist, partNumber):
    for item in itemlist:
        obj = item.obj_pointer
        old = obj.name.lower()
        index = old.find("part") + 5
        new = obj.name[:index] + str(partNumber) + obj.name[index+1:]
        item.name = new
        item.model_name = new
        obj.name = setModelName(modelDict, obj.name, new)
    return modelDict

def modelNameChange(self,context):
    modelDict = getTextBlock()
    obj = self.obj_pointer
    if obj:
        obj.name = setModelName(modelDict, obj.name, self.model_name)
    setTextBlock(modelDict)


# ============= # 
#   FBX STUFF   #
# ============= #

class TBSEKIT_OT_importFBX(Operator, ImportHelper):
    bl_idname = "object.importfbx"
    bl_label = "Import FBX"
    bl_description = "Bulk import FBXs with optimal setting for XIV modding"
    bl_options = {'REGISTER','UNDO'}

    filter_glob: StringProperty(default='*.fbx',options={'HIDDEN'})

    files: CollectionProperty(
            type=bpy.types.OperatorFileListElement,
            options={'HIDDEN', 'SKIP_SAVE'},
        )
    
    # CUSTOM OPTIONS
    fix_skeleton: BoolProperty(
        default=True,
        name="Fix Skeleton",
        description="Rotates bones of skeleton to make them more readable when editing.")
    fix_materials: BoolProperty(
        default=True,
        name="Fix Materials",
        description="Changes all materials to 'Alpha Hashed' and fixes metalics")
    delete_junk: BoolProperty(
        default=True,
        name="Delete Junk",
        description="Deletes all empty objects, importing only the mesh and armature")
    auto_assign_armature: BoolProperty(
        default=True,
        name="Auto Assign Armature",
        description="Deletes the armature that comes with the fbx and assigns all meshes to existing skeleton.\nRecommended to disable ONLY if fbx skeleton includes ex_ bones")
    
    def draw(self, context):
        layout = self.layout

        layout.label(text="== CUSTOM SETTINGS ==")
        box = layout.box()
        box.prop(self, 'fix_skeleton')
        box.prop(self, 'fix_materials')
        box.prop(self, 'delete_junk')
        row = box.row()
        row.prop(self, 'auto_assign_armature')
        row = layout.row()
        row.label(text="I recommended keeping all options enabled!")
        row.enabled=False

    def execute(self, context):
        folder = os.path.dirname(self.filepath)

        # OPTIONAL SETTING: rotates bone axis on imported skeleton
        if self.fix_skeleton:
            primary_axis = 'X'
            second_axis = 'Y'
        else:
            primary_axis = 'Y'
            second_axis = 'X'

        for meshfile in self.files:
            filepath = (os.path.join(folder, meshfile.name))
            bpy.ops.import_scene.fbx(
                filepath=filepath,
                use_anim=False,
                force_connect_children=True,
                primary_bone_axis=primary_axis,
                secondary_bone_axis=second_axis
            )
            importedfiles = context.selected_objects
            cleanImport(self, importedfiles)

        return {'FINISHED'}
    
# =================== #
#   RENAMING MODELS   #
# =================== #

class TBSEKIT_OT_rename(Operator):
    bl_idname = "object.renaming"
    bl_label = "Rename"
    bl_description = "This allows for bulk renaming of models, changing all models to Part X.Z to Part Y.Z"
    bl_options = {'REGISTER','UNDO'}

    def execute(self, context):
        scene = context.scene
        tbse_properties =  scene.tbse_kit_properties
        partNumber = tbse_properties["partNumber"]
        rename = tbse_properties.rename_options
        # gets json code
        modelDict = getTextBlock()
        modelList = []
        
        if rename == 'chest': 
            # create a list of obj names
            modelList = getModelsInList(modelDict, "body_neck")
            modelList.extend(getModelsInList(modelDict, "body_chest"))
            modelList.extend(getModelsInList(modelDict, "body_chest_w"))
            modelList.extend(getModelsInList(modelDict, "body_chest_chonk"))
        if rename == 'legs':
            modelList = getModelsInList(modelDict, "body_legs")
            modelList.extend(getModelsInList(modelDict, "body_legs_chonk"))
            modelList.extend(getModelsInList(modelDict, "body_genitals"))
            modelList.extend(getModelsInList(modelDict, "genitals_amab"))
            modelList.extend(getModelsInList(modelDict, "genitals_afab"))
        if rename == 'hands': modelList = getModelsInList(modelDict, "body_hands")
        if rename == 'feet': modelList = getModelsInList(modelDict, "body_feet")
        if rename == 'chest_piercings': modelList = getModelsInList(modelDict, "piercings_chest")
        if rename == 'amab_piercings': modelList = getModelsInList(modelDict, "piercings_amab")
        if rename == 'bpf': modelList = getModelsInList(modelDict, "genitals_bpf")

        modelDict = renameModels(modelDict, modelList, partNumber)

        if rename == 'chest_gear': modelDict = renameGear(modelDict, scene.chest_gear_list, partNumber)
        if rename == 'leg_gear': modelDict = renameGear(modelDict, scene.leg_gear_list, partNumber)
        if rename == 'hand_gear': modelDict = renameGear(modelDict, scene.hand_gear_list, partNumber)
        if rename == 'feet_gear': modelDict = renameGear(modelDict, scene.feet_gear_list, partNumber)

        if rename == 'selected':
            selected_objects = context.selected_objects
            for obj in selected_objects:
                split = obj.name.lower()
                index = split.find("part") + 5
                new = obj.name[:index] + str(partNumber) + obj.name[index+1:]
                obj.name = new
        
        if not rename == 'selected': setTextBlock(modelDict)

        return {'FINISHED'}
    
def renameModels(modelDict, modelList, partNumber):
    for name in modelList: # list of obj names
        obj = bpy.data.objects[name]
        split = obj.name.lower()
        index = split.find("part") + 5
        new = obj.name[:index] + str(partNumber) + obj.name[index+1:]
        obj.name = setModelName(modelDict, obj.name, new)
    return modelDict

def renameGear(modelDict, itemlist, partNumber):
    for item in itemlist:
        obj = item.obj_pointer
        old = obj.name.lower()
        index = old.find("part") + 5
        new = obj.name[:index] + str(partNumber) + obj.name[index+1:]
        item.name = new
        item.model_name = new
        obj.name = setModelName(modelDict, obj.name, new)
    return modelDict

def modelNameChange(self,context):
    modelDict = getTextBlock()
    obj = self.obj_pointer
    if obj:
        obj.name = setModelName(modelDict, obj.name, self.model_name)
    setTextBlock(modelDict)


# ============= # 
#   FBX STUFF   #
# ============= #

class TBSEKIT_OT_importFBX(Operator, ImportHelper):
    bl_idname = "object.importfbx"
    bl_label = "Import FBX"
    bl_description = "Bulk import FBXs with optimal setting for XIV modding"
    bl_options = {'REGISTER','UNDO'}

    filter_glob: StringProperty(default='*.fbx',options={'HIDDEN'})

    files: CollectionProperty(
            type=bpy.types.OperatorFileListElement,
            options={'HIDDEN', 'SKIP_SAVE'},
        )
    
    # CUSTOM OPTIONS
    fix_skeleton: BoolProperty(
        default=True,
        name="Fix Skeleton",
        description="Rotates bones of skeleton to make them more readable when editing.")
    fix_materials: BoolProperty(
        default=True,
        name="Fix Materials",
        description="Changes all materials to 'Alpha Hashed' and fixes metalics")
    delete_junk: BoolProperty(
        default=True,
        name="Delete Junk",
        description="Deletes all empty objects, importing only the mesh and armature")
    auto_assign_armature: BoolProperty(
        default=True,
        name="Auto Assign Armature",
        description="Deletes the armature that comes with the fbx and assigns all meshes to existing skeleton.\nRecommended to disable ONLY if fbx skeleton includes ex_ bones")
    
    def draw(self, context):
        layout = self.layout

        layout.label(text="== CUSTOM SETTINGS ==")
        box = layout.box()
        box.prop(self, 'fix_skeleton')
        box.prop(self, 'fix_materials')
        box.prop(self, 'delete_junk')
        row = box.row()
        row.prop(self, 'auto_assign_armature')
        row = layout.row()
        row.label(text="I recommended keeping all options enabled!")
        row.enabled=False

    def execute(self, context):
        folder = os.path.dirname(self.filepath)

        # OPTIONAL SETTING: rotates bone axis on imported skeleton
        if self.fix_skeleton:
            primary_axis = 'X'
            second_axis = 'Y'
        else:
            primary_axis = 'Y'
            second_axis = 'X'

        for meshfile in self.files:
            filepath = (os.path.join(folder, meshfile.name))
            bpy.ops.import_scene.fbx(
                filepath=filepath,
                use_anim=False,
                force_connect_children=True,
                primary_bone_axis=primary_axis,
                secondary_bone_axis=second_axis
            )
            importedfiles = context.selected_objects
            cleanImport(self, importedfiles)

        return {'FINISHED'}
    
# =================== #
#   RENAMING MODELS   #
# =================== #

class TBSEKIT_OT_rename(Operator):
    bl_idname = "object.renaming"
    bl_label = "Rename"
    bl_description = "This allows for bulk renaming of models, changing all models to Part X.Z to Part Y.Z"
    bl_options = {'REGISTER','UNDO'}

    def execute(self, context):
        scene = context.scene
        tbse_properties =  scene.tbse_kit_properties
        partNumber = tbse_properties["partNumber"]
        rename = tbse_properties.rename_options
        # gets json code
        modelDict = getTextBlock()
        modelList = []
        
        if rename == 'chest': 
            # create a list of obj names
            modelList = getModelsInList(modelDict, "body_neck")
            modelList.extend(getModelsInList(modelDict, "body_chest"))
            modelList.extend(getModelsInList(modelDict, "body_chest_w"))
            modelList.extend(getModelsInList(modelDict, "body_chest_chonk"))
        if rename == 'legs':
            modelList = getModelsInList(modelDict, "body_legs")
            modelList.extend(getModelsInList(modelDict, "body_legs_chonk"))
            modelList.extend(getModelsInList(modelDict, "body_genitals"))
            modelList.extend(getModelsInList(modelDict, "genitals_amab"))
            modelList.extend(getModelsInList(modelDict, "genitals_afab"))
        if rename == 'hands': modelList = getModelsInList(modelDict, "body_hands")
        if rename == 'feet': modelList = getModelsInList(modelDict, "body_feet")
        if rename == 'chest_piercings': modelList = getModelsInList(modelDict, "piercings_chest")
        if rename == 'amab_piercings': modelList = getModelsInList(modelDict, "piercings_amab")
        if rename == 'bpf': modelList = getModelsInList(modelDict, "genitals_bpf")

        modelDict = renameModels(modelDict, modelList, partNumber)

        if rename == 'chest_gear': modelDict = renameGear(modelDict, scene.chest_gear_list, partNumber)
        if rename == 'leg_gear': modelDict = renameGear(modelDict, scene.leg_gear_list, partNumber)
        if rename == 'hand_gear': modelDict = renameGear(modelDict, scene.hand_gear_list, partNumber)
        if rename == 'feet_gear': modelDict = renameGear(modelDict, scene.feet_gear_list, partNumber)

        if rename == 'selected':
            selected_objects = context.selected_objects
            for obj in selected_objects:
                split = obj.name.lower()
                index = split.find("part") + 5
                new = obj.name[:index] + str(partNumber) + obj.name[index+1:]
                obj.name = new
        
        if not rename == 'selected': setTextBlock(modelDict)

        return {'FINISHED'}
    
def renameModels(modelDict, modelList, partNumber):
    for name in modelList: # list of obj names
        obj = bpy.data.objects[name]
        split = obj.name.lower()
        index = split.find("part") + 5
        new = obj.name[:index] + str(partNumber) + obj.name[index+1:]
        obj.name = setModelName(modelDict, obj.name, new)
    return modelDict

def renameGear(modelDict, itemlist, partNumber):
    for item in itemlist:
        obj = item.obj_pointer
        old = obj.name.lower()
        index = old.find("part") + 5
        new = obj.name[:index] + str(partNumber) + obj.name[index+1:]
        item.name = new
        item.model_name = new
        obj.name = setModelName(modelDict, obj.name, new)
    return modelDict

def modelNameChange(self,context):
    modelDict = getTextBlock()
    obj = self.obj_pointer
    if obj:
        obj.name = setModelName(modelDict, obj.name, self.model_name)
    setTextBlock(modelDict)


# ============= # 
#   FBX STUFF   #
# ============= #

class TBSEKIT_OT_importFBX(Operator, ImportHelper):
    bl_idname = "object.importfbx"
    bl_label = "Import FBX"
    bl_description = "Bulk import FBXs with optimal setting for XIV modding"
    bl_options = {'REGISTER','UNDO'}

    filter_glob: StringProperty(default='*.fbx',options={'HIDDEN'})

    files: CollectionProperty(
            type=bpy.types.OperatorFileListElement,
            options={'HIDDEN', 'SKIP_SAVE'},
        )
    
    # CUSTOM OPTIONS
    fix_skeleton: BoolProperty(
        default=True,
        name="Fix Skeleton",
        description="Rotates bones of skeleton to make them more readable when editing.")
    fix_materials: BoolProperty(
        default=True,
        name="Fix Materials",
        description="Changes all materials to 'Alpha Hashed' and fixes metalics")
    delete_junk: BoolProperty(
        default=True,
        name="Delete Junk",
        description="Deletes all empty objects, importing only the mesh and armature")
    auto_assign_armature: BoolProperty(
        default=True,
        name="Auto Assign Armature",
        description="Deletes the armature that comes with the fbx and assigns all meshes to existing skeleton.\nRecommended to disable ONLY if fbx skeleton includes ex_ bones")
    
    def draw(self, context):
        layout = self.layout

        layout.label(text="== CUSTOM SETTINGS ==")
        box = layout.box()
        box.prop(self, 'fix_skeleton')
        box.prop(self, 'fix_materials')
        box.prop(self, 'delete_junk')
        row = box.row()
        row.prop(self, 'auto_assign_armature')
        row = layout.row()
        row.label(text="I recommended keeping all options enabled!")
        row.enabled=False

    def execute(self, context):
        folder = os.path.dirname(self.filepath)

        # OPTIONAL SETTING: rotates bone axis on imported skeleton
        if self.fix_skeleton:
            primary_axis = 'X'
            second_axis = 'Y'
        else:
            primary_axis = 'Y'
            second_axis = 'X'

        for meshfile in self.files:
            filepath = (os.path.join(folder, meshfile.name))
            bpy.ops.import_scene.fbx(
                filepath=filepath,
                use_anim=False,
                force_connect_children=True,
                primary_bone_axis=primary_axis,
                secondary_bone_axis=second_axis
            )
            importedfiles = context.selected_objects
            cleanImport(self, importedfiles)

        return {'FINISHED'}
    
# =================== #
#   RENAMING MODELS   #
# =================== #

class TBSEKIT_OT_rename(Operator):
    bl_idname = "object.renaming"
    bl_label = "Rename"
    bl_description = "This allows for bulk renaming of models, changing all models to Part X.Z to Part Y.Z"
    bl_options = {'REGISTER','UNDO'}

    def execute(self, context):
        scene = context.scene
        tbse_properties =  scene.tbse_kit_properties
        partNumber = tbse_properties["partNumber"]
        rename = tbse_properties.rename_options
        # gets json code
        modelDict = getTextBlock()
        modelList = []
        
        if rename == 'chest': 
            # create a list of obj names
            modelList = getModelsInList(modelDict, "body_neck")
            modelList.extend(getModelsInList(modelDict, "body_chest"))
            modelList.extend(getModelsInList(modelDict, "body_chest_w"))
            modelList.extend(getModelsInList(modelDict, "body_chest_chonk"))
        if rename == 'legs':
            modelList = getModelsInList(modelDict, "body_legs")
            modelList.extend(getModelsInList(modelDict, "body_legs_chonk"))
            modelList.extend(getModelsInList(modelDict, "body_genitals"))
            modelList.extend(getModelsInList(modelDict, "genitals_amab"))
            modelList.extend(getModelsInList(modelDict, "genitals_afab"))
        if rename == 'hands': modelList = getModelsInList(modelDict, "body_hands")
        if rename == 'feet': modelList = getModelsInList(modelDict, "body_feet")
        if rename == 'chest_piercings': modelList = getModelsInList(modelDict, "piercings_chest")
        if rename == 'amab_piercings': modelList = getModelsInList(modelDict, "piercings_amab")
        if rename == 'bpf': modelList = getModelsInList(modelDict, "genitals_bpf")

        modelDict = renameModels(modelDict, modelList, partNumber)

        if rename == 'chest_gear': modelDict = renameGear(modelDict, scene.chest_gear_list, partNumber)
        if rename == 'leg_gear': modelDict = renameGear(modelDict, scene.leg_gear_list, partNumber)
        if rename == 'hand_gear': modelDict = renameGear(modelDict, scene.hand_gear_list, partNumber)
        if rename == 'feet_gear': modelDict = renameGear(modelDict, scene.feet_gear_list, partNumber)

        if rename == 'selected':
            selected_objects = context.selected_objects
            for obj in selected_objects:
                split = obj.name.lower()
                index = split.find("part") + 5
                new = obj.name[:index] + str(partNumber) + obj.name[index+1:]
                obj.name = new
        
        if not rename == 'selected': setTextBlock(modelDict)

        return {'FINISHED'}
    
def renameModels(modelDict, modelList, partNumber):
    for name in modelList: # list of obj names
        obj = bpy.data.objects[name]
        split = obj.name.lower()
        index = split.find("part") + 5
        new = obj.name[:index] + str(partNumber) + obj.name[index+1:]
        obj.name = setModelName(modelDict, obj.name, new)
    return modelDict

def renameGear(modelDict, itemlist, partNumber):
    for item in itemlist:
        obj = item.obj_pointer
        old = obj.name.lower()
        index = old.find("part") + 5
        new = obj.name[:index] + str(partNumber) + obj.name[index+1:]
        item.name = new
        item.model_name = new
        obj.name = setModelName(modelDict, obj.name, new)
    return modelDict

def modelNameChange(self,context):
    modelDict = getTextBlock()
    obj = self.obj_pointer
    if obj:
        obj.name = setModelName(modelDict, obj.name, self.model_name)
    setTextBlock(modelDict)


# ============= # 
#   FBX STUFF   #
# ============= #

class TBSEKIT_OT_importFBX(Operator, ImportHelper):
    bl_idname = "object.importfbx"
    bl_label = "Import FBX"
    bl_description = "Bulk import FBXs with optimal setting for XIV modding"
    bl_options = {'REGISTER','UNDO'}

    filter_glob: StringProperty(default='*.fbx',options={'HIDDEN'})

    files: CollectionProperty(
            type=bpy.types.OperatorFileListElement,
            options={'HIDDEN', 'SKIP_SAVE'},
        )
    
    # CUSTOM OPTIONS
    fix_skeleton: BoolProperty(
        default=True,
        name="Fix Skeleton",
        description="Rotates bones of skeleton to make them more readable when editing.")
    fix_materials: BoolProperty(
        default=True,
        name="Fix Materials",
        description="Changes all materials to 'Alpha Hashed' and fixes metalics")
    delete_junk: BoolProperty(
        default=True,
        name="Delete Junk",
        description="Deletes all empty objects, importing only the mesh and armature")
    auto_assign_armature: BoolProperty(
        default=True,
        name="Auto Assign Armature",
        description="Deletes the armature that comes with the fbx and assigns all meshes to existing skeleton.\nRecommended to disable ONLY if fbx skeleton includes ex_ bones")
    
    def draw(self, context):
        layout = self.layout

        layout.label(text="== CUSTOM SETTINGS ==")
        box = layout.box()
        box.prop(self, 'fix_skeleton')
        box.prop(self, 'fix_materials')
        box.prop(self, 'delete_junk')
        row = box.row()
        row.prop(self, 'auto_assign_armature')
        row = layout.row()
        row.label(text="I recommended keeping all options enabled!")
        row.enabled=False

    def execute(self, context):
        folder = os.path.dirname(self.filepath)

        # OPTIONAL SETTING: rotates bone axis on imported skeleton
        if self.fix_skeleton:
            primary_axis = 'X'
            second_axis = 'Y'
        else:
            primary_axis = 'Y'
            second_axis = 'X'

        for meshfile in self.files:
            filepath = (os.path.join(folder, meshfile.name))
            bpy.ops.import_scene.fbx(
                filepath=filepath,
                use_anim=False,
                force_connect_children=True,
                primary_bone_axis=primary_axis,
                secondary_bone_axis=second_axis
            )
            importedfiles = context.selected_objects
            cleanImport(self, importedfiles)

        return {'FINISHED'}
    
# =================== #
#   RENAMING MODELS   #
# =================== #

class TBSEKIT_OT_rename(Operator):
    bl_idname = "object.renaming"
    bl_label = "Rename"
    bl_description = "This allows for bulk renaming of models, changing all models to Part X.Z to Part Y.Z"
    bl_options = {'REGISTER','UNDO'}

    def execute(self, context):
        scene = context.scene
        tbse_properties =  scene.tbse_kit_properties
        partNumber = tbse_properties["partNumber"]
        rename = tbse_properties.rename_options
        # gets json code
        modelDict = getTextBlock()
        modelList = []
        
        if rename == 'chest': 
            # create a list of obj names
            modelList = getModelsInList(modelDict, "body_neck")
            modelList.extend(getModelsInList(modelDict, "body_chest"))
            modelList.extend(getModelsInList(modelDict, "body_chest_w"))
            modelList.extend(getModelsInList(modelDict, "body_chest_chonk"))
        if rename == 'legs':
            modelList = getModelsInList(modelDict, "body_legs")
            modelList.extend(getModelsInList(modelDict, "body_legs_chonk"))
            modelList.extend(getModelsInList(modelDict, "body_genitals"))
            modelList.extend(getModelsInList(modelDict, "genitals_amab"))
            modelList.extend(getModelsInList(modelDict, "genitals_afab"))
        if rename == 'hands': modelList = getModelsInList(modelDict, "body_hands")
        if rename == 'feet': modelList = getModelsInList(modelDict, "body_feet")
        if rename == 'chest_piercings': modelList = getModelsInList(modelDict, "piercings_chest")
        if rename == 'amab_piercings': modelList = getModelsInList(modelDict, "piercings_amab")
        if rename == 'bpf': modelList = getModelsInList(modelDict, "genitals_bpf")

        modelDict = renameModels(modelDict, modelList, partNumber)

        if rename == 'chest_gear': modelDict = renameGear(modelDict, scene.chest_gear_list, partNumber)
        if rename == 'leg_gear': modelDict = renameGear(modelDict, scene.leg_gear_list, partNumber)
        if rename == 'hand_gear': modelDict = renameGear(modelDict, scene.hand_gear_list, partNumber)
        if rename == 'feet_gear': modelDict = renameGear(modelDict, scene.feet_gear_list, partNumber)

        if rename == 'selected':
            selected_objects = context.selected_objects
            for obj in selected_objects:
                split = obj.name.lower()
                index = split.find("part") + 5
                new = obj.name[:index] + str(partNumber) + obj.name[index+1:]
                obj.name = new
        
        if not rename == 'selected': setTextBlock(modelDict)

        return {'FINISHED'}
    
def renameModels(modelDict, modelList, partNumber):
    for name in modelList: # list of obj names
        obj = bpy.data.objects[name]
        split = obj.name.lower()
        index = split.find("part") + 5
        new = obj.name[:index] + str(partNumber) + obj.name[index+1:]
        obj.name = setModelName(modelDict, obj.name, new)
    return modelDict

def renameGear(modelDict, itemlist, partNumber):
    for item in itemlist:
        obj = item.obj_pointer
        old = obj.name.lower()
        index = old.find("part") + 5
        new = obj.name[:index] + str(partNumber) + obj.name[index+1:]
        item.name = new
        item.model_name = new
        obj.name = setModelName(modelDict, obj.name, new)
    return modelDict

def modelNameChange(self,context):
    modelDict = getTextBlock()
    obj = self.obj_pointer
    if obj:
        obj.name = setModelName(modelDict, obj.name, self.model_name)
    setTextBlock(modelDict)


# ============= # 
#   FBX STUFF   #
# ============= #

class TBSEKIT_OT_importFBX(Operator, ImportHelper):
    bl_idname = "object.importfbx"
    bl_label = "Import FBX"
    bl_description = "Bulk import FBXs with optimal setting for XIV modding"
    bl_options = {'REGISTER','UNDO'}

    filter_glob: StringProperty(default='*.fbx',options={'HIDDEN'})

    files: CollectionProperty(
            type=bpy.types.OperatorFileListElement,
            options={'HIDDEN', 'SKIP_SAVE'},
        )
    
    # CUSTOM OPTIONS
    fix_skeleton: BoolProperty(
        default=True,
        name="Fix Skeleton",
        description="Rotates bones of skeleton to make them more readable when editing.")
    fix_materials: BoolProperty(
        default=True,
        name="Fix Materials",
        description="Changes all materials to 'Alpha Hashed' and fixes metalics")
    delete_junk: BoolProperty(
        default=True,
        name="Delete Junk",
        description="Deletes all empty objects, importing only the mesh and armature")
    auto_assign_armature: BoolProperty(
        default=True,
        name="Auto Assign Armature",
        description="Deletes the armature that comes with the fbx and assigns all meshes to existing skeleton.\nRecommended to disable ONLY if fbx skeleton includes ex_ bones")
    
    def draw(self, context):
        layout = self.layout

        layout.label(text="== CUSTOM SETTINGS ==")
        box = layout.box()
        box.prop(self, 'fix_skeleton')
        box.prop(self, 'fix_materials')
        box.prop(self, 'delete_junk')
        row = box.row()
        row.prop(self, 'auto_assign_armature')
        row = layout.row()
        row.label(text="I recommended keeping all options enabled!")
        row.enabled=False

    def execute(self, context):
        folder = os.path.dirname(self.filepath)

        # OPTIONAL SETTING: rotates bone axis on imported skeleton
        if self.fix_skeleton:
            primary_axis = 'X'
            second_axis = 'Y'
        else:
            primary_axis = 'Y'
            second_axis = 'X'

        for meshfile in self.files:
            filepath = (os.path.join(folder, meshfile.name))
            bpy.ops.import_scene.fbx(
                filepath=filepath,
                use_anim=False,
                force_connect_children=True,
                primary_bone_axis=primary_axis,
                secondary_bone_axis=second_axis
            )
            importedfiles = context.selected_objects
            cleanImport(self, importedfiles)

        return {'FINISHED'}
    
# =================== #
#   RENAMING MODELS   #
# =================== #

class TBSEKIT_OT_rename(Operator):
    bl_idname = "object.renaming"
    bl_label = "Rename"
    bl_description = "This allows for bulk renaming of models, changing all models to Part X.Z to Part Y.Z"
    bl_options = {'REGISTER','UNDO'}

    def execute(self, context):
        scene = context.scene
        tbse_properties =  scene.tbse_kit_properties
        partNumber = tbse_properties["partNumber"]
        rename = tbse_properties.rename_options
        # gets json code
        modelDict = getTextBlock()
        modelList = []
        
        if rename == 'chest': 
            # create a list of obj names
            modelList = getModelsInList(modelDict, "body_neck")
            modelList.extend(getModelsInList(modelDict, "body_chest"))
            modelList.extend(getModelsInList(modelDict, "body_chest_w"))
            modelList.extend(getModelsInList(modelDict, "body_chest_chonk"))
        if rename == 'legs':
            modelList = getModelsInList(modelDict, "body_legs")
            modelList.extend(getModelsInList(modelDict, "body_legs_chonk"))
            modelList.extend(getModelsInList(modelDict, "body_genitals"))
            modelList.extend(getModelsInList(modelDict, "genitals_amab"))
            modelList.extend(getModelsInList(modelDict, "genitals_afab"))
        if rename == 'hands': modelList = getModelsInList(modelDict, "body_hands")
        if rename == 'feet': modelList = getModelsInList(modelDict, "body_feet")
        if rename == 'chest_piercings': modelList = getModelsInList(modelDict, "piercings_chest")
        if rename == 'amab_piercings': modelList = getModelsInList(modelDict, "piercings_amab")
        if rename == 'bpf': modelList = getModelsInList(modelDict, "genitals_bpf")

        modelDict = renameModels(modelDict, modelList, partNumber)

        if rename == 'chest_gear': modelDict = renameGear(modelDict, scene.chest_gear_list, partNumber)
        if rename == 'leg_gear': modelDict = renameGear(modelDict, scene.leg_gear_list, partNumber)
        if rename == 'hand_gear': modelDict = renameGear(modelDict, scene.hand_gear_list, partNumber)
        if rename == 'feet_gear': modelDict = renameGear(modelDict, scene.feet_gear_list, partNumber)

        if rename == 'selected':
            selected_objects = context.selected_objects
            for obj in selected_objects:
                split = obj.name.lower()
                index = split.find("part") + 5
                new = obj.name[:index] + str(partNumber) + obj.name[index+1:]
                obj.name = new
        
        if not rename == 'selected': setTextBlock(modelDict)

        return {'FINISHED'}
    
def renameModels(modelDict, modelList, partNumber):
    for name in modelList: # list of obj names
        obj = bpy.data.objects[name]
        split = obj.name.lower()
        index = split.find("part") + 5
        new = obj.name[:index] + str(partNumber) + obj.name[index+1:]
        obj.name = setModelName(modelDict, obj.name, new)
    return modelDict

def renameGear(modelDict, itemlist, partNumber):
    for item in itemlist:
        obj = item.obj_pointer
        old = obj.name.lower()
        index = old.find("part") + 5
        new = obj.name[:index] + str(partNumber) + obj.name[index+1:]
        item.name = new
        item.model_name = new
        obj.name = setModelName(modelDict, obj.name, new)
    return modelDict

def modelNameChange(self,context):
    modelDict = getTextBlock()
    obj = self.obj_pointer
    if obj:
        obj.name = setModelName(modelDict, obj.name, self.model_name)
    setTextBlock(modelDict)


# ============= # 
#   FBX STUFF   #
# ============= #

class TBSEKIT_OT_importFBX(Operator, ImportHelper):
    bl_idname = "object.importfbx"
    bl_label = "Import FBX"
    bl_description = "Bulk import FBXs with optimal setting for XIV modding"
    bl_options = {'REGISTER','UNDO'}

    filter_glob: StringProperty(default='*.fbx',options={'HIDDEN'})

    files: CollectionProperty(
            type=bpy.types.OperatorFileListElement,
            options={'HIDDEN', 'SKIP_SAVE'},
        )
    
    # CUSTOM OPTIONS
    fix_skeleton: BoolProperty(
        default=True,
        name="Fix Skeleton",
        description="Rotates bones of skeleton to make them more readable when editing.")
    fix_materials: BoolProperty(
        default=True,
        name="Fix Materials",
        description="Changes all materials to 'Alpha Hashed' and fixes metalics")
    delete_junk: BoolProperty(
        default=True,
        name="Delete Junk",
        description="Deletes all empty objects, importing only the mesh and armature")
    auto_assign_armature: BoolProperty(
        default=True,
        name="Auto Assign Armature",
        description="Deletes the armature that comes with the fbx and assigns all meshes to existing skeleton.\nRecommended to disable ONLY if fbx skeleton includes ex_ bones")
    
    def draw(self, context):
        layout = self.layout

        layout.label(text="== CUSTOM SETTINGS ==")
        box = layout.box()
        box.prop(self, 'fix_skeleton')
        box.prop(self, 'fix_materials')
        box.prop(self, 'delete_junk')
        row = box.row()
        row.prop(self, 'auto_assign_armature')
        row = layout.row()
        row.label(text="I recommended keeping all options enabled!")
        row.enabled=False

    def execute(self, context):
        folder = os.path.dirname(self.filepath)

        # OPTIONAL SETTING: rotates bone axis on imported skeleton
        if self.fix_skeleton:
            primary_axis = 'X'
            second_axis = 'Y'
        else:
            primary_axis = 'Y'
            second_axis = 'X'

        for meshfile in self.files:
            filepath = (os.path.join(folder, meshfile.name))
            bpy.ops.import_scene.fbx(
                filepath=filepath,
                use_anim=False,
                force_connect_children=True,
                primary_bone_axis=primary_axis,
                secondary_bone_axis=second_axis
            )
            importedfiles = context.selected_objects
            cleanImport(self, importedfiles)

        return {'FINISHED'}
    
# =================== #
#   RENAMING MODELS   #
# =================== #

class TBSEKIT_OT_rename(Operator):
    bl_idname = "object.renaming"
    bl_label = "Rename"
    bl_description = "This allows for bulk renaming of models, changing all models to Part X.Z to Part Y.Z"
    bl_options = {'REGISTER','UNDO'}

    def execute(self, context):
        scene = context.scene
        tbse_properties =  scene.tbse_kit_properties
        partNumber = tbse_properties["partNumber"]
        rename = tbse_properties.rename_options
        # gets json code
        modelDict = getTextBlock()
        modelList = []
        
        if rename == 'chest': 
            # create a list of obj names
            modelList = getModelsInList(modelDict, "body_neck")
            modelList.extend(getModelsInList(modelDict, "body_chest"))
            modelList.extend(getModelsInList(modelDict, "body_chest_w"))
            modelList.extend(getModelsInList(modelDict, "body_chest_chonk"))
        if rename == 'legs':
            modelList = getModelsInList(modelDict, "body_legs")
            modelList.extend(getModelsInList(modelDict, "body_legs_chonk"))
            modelList.extend(getModelsInList(modelDict, "body_genitals"))
            modelList.extend(getModelsInList(modelDict, "genitals_amab"))
            modelList.extend(getModelsInList(modelDict, "genitals_afab"))
        if rename == 'hands': modelList = getModelsInList(modelDict, "body_hands")
        if rename == 'feet': modelList = getModelsInList(modelDict, "body_feet")
        if rename == 'chest_piercings': modelList = getModelsInList(modelDict, "piercings_chest")
        if rename == 'amab_piercings': modelList = getModelsInList(modelDict, "piercings_amab")
        if rename == 'bpf': modelList = getModelsInList(modelDict, "genitals_bpf")

        modelDict = renameModels(modelDict, modelList, partNumber)

        if rename == 'chest_gear': modelDict = renameGear(modelDict, scene.chest_gear_list, partNumber)
        if rename == 'leg_gear': modelDict = renameGear(modelDict, scene.leg_gear_list, partNumber)
        if rename == 'hand_gear': modelDict = renameGear(modelDict, scene.hand_gear_list, partNumber)
        if rename == 'feet_gear': modelDict = renameGear(modelDict, scene.feet_gear_list, partNumber)

        if rename == 'selected':
            selected_objects = context.selected_objects
            for obj in selected_objects:
                split = obj.name.lower()
                index = split.find("part") + 5
                new = obj.name[:index] + str(partNumber) + obj.name[index+1:]
                obj.name = new
        
        if not rename == 'selected': setTextBlock(modelDict)

        return {'FINISHED'}
    
def renameModels(modelDict, modelList, partNumber):
    for name in modelList: # list of obj names
        obj = bpy.data.objects[name]
        split = obj.name.lower()
        index = split.find("part") + 5
        new = obj.name[:index] + str(partNumber) + obj.name[index+1:]
        obj.name = setModelName(modelDict, obj.name, new)
    return modelDict

def renameGear(modelDict, itemlist, partNumber):
    for item in itemlist:
        obj = item.obj_pointer
        old = obj.name.lower()
        index = old.find("part") + 5
        new = obj.name[:index] + str(partNumber) + obj.name[index+1:]
        item.name = new
        item.model_name = new
        obj.name = setModelName(modelDict, obj.name, new)
    return modelDict

def modelNameChange(self,context):
    modelDict = getTextBlock()
    obj = self.obj_pointer
    if obj:
        obj.name = setModelName(modelDict, obj.name, self.model_name)
    setTextBlock(modelDict)


# ============= # 
#   FBX STUFF   #
# ============= #

class TBSEKIT_OT_importFBX(Operator, ImportHelper):
    bl_idname = "object.importfbx"
    bl_label = "Import FBX"
    bl_description = "Bulk import FBXs with optimal setting for XIV modding"
    bl_options = {'REGISTER','UNDO'}

    filter_glob: StringProperty(default='*.fbx',options={'HIDDEN'})

    files: CollectionProperty(
            type=bpy.types.OperatorFileListElement,
            options={'HIDDEN', 'SKIP_SAVE'},
        )
    
    # CUSTOM OPTIONS
    fix_skeleton: BoolProperty(
        default=True,
        name="Fix Skeleton",
        description="Rotates bones of skeleton to make them more readable when editing.")
    fix_materials: BoolProperty(
        default=True,
        name="Fix Materials",
        description="Changes all materials to 'Alpha Hashed' and fixes metalics")
    delete_junk: BoolProperty(
        default=True,
        name="Delete Junk",
        description="Deletes all empty objects, importing only the mesh and armature")
    auto_assign_armature: BoolProperty(
        default=True,
        name="Auto Assign Armature",
        description="Deletes the armature that comes with the fbx and assigns all meshes to existing skeleton.\nRecommended to disable ONLY if fbx skeleton includes ex_ bones")
    
    def draw(self, context):
        layout = self.layout

        layout.label(text="== CUSTOM SETTINGS ==")
        box = layout.box()
        box.prop(self, 'fix_skeleton')
        box.prop(self, 'fix_materials')
        box.prop(self, 'delete_junk')
        row = box.row()
        row.prop(self, 'auto_assign_armature')
        row = layout.row()
        row.label(text="I recommended keeping all options enabled!")
        row.enabled=False

    def execute(self, context):
        folder = os.path.dirname(self.filepath)

        # OPTIONAL SETTING: rotates bone axis on imported skeleton
        if self.fix_skeleton:
            primary_axis = 'X'
            second_axis = 'Y'
        else:
            primary_axis = 'Y'
            second_axis = 'X'

        for meshfile in self.files:
            filepath = (os.path.join(folder, meshfile.name))
            bpy.ops.import_scene.fbx(
                filepath=filepath,
                use_anim=False,
                force_connect_children=True,
                primary_bone_axis=primary_axis,
                secondary_bone_axis=second_axis
            )
            importedfiles = context.selected_objects
            cleanImport(self, importedfiles)

        return {'FINISHED'}
    
# =================== #
#   RENAMING MODELS   #
# =================== #

class TBSEKIT_OT_rename(Operator):
    bl_idname = "object.renaming"
    bl_label = "Rename"
    bl_description = "This allows for bulk renaming of models, changing all models to Part X.Z to Part Y.Z"
    bl_options = {'REGISTER','UNDO'}

    def execute(self, context):
        scene = context.scene
        tbse_properties =  scene.tbse_kit_properties
        partNumber = tbse_properties["partNumber"]
        rename = tbse_properties.rename_options
        # gets json code
        modelDict = getTextBlock()
        modelList = []
        
        if rename == 'chest': 
            # create a list of obj names
            modelList = getModelsInList(modelDict, "body_neck")
            modelList.extend(getModelsInList(modelDict, "body_chest"))
            modelList.extend(getModelsInList(modelDict, "body_chest_w"))
            modelList.extend(getModelsInList(modelDict, "body_chest_chonk"))
        if rename == 'legs':
            modelList = getModelsInList(modelDict, "body_legs")
            modelList.extend(getModelsInList(modelDict, "body_legs_chonk"))
            modelList.extend(getModelsInList(modelDict, "body_genitals"))
            modelList.extend(getModelsInList(modelDict, "genitals_amab"))
            modelList.extend(getModelsInList(modelDict, "genitals_afab"))
        if rename == 'hands': modelList = getModelsInList(modelDict, "body_hands")
        if rename == 'feet': modelList = getModelsInList(modelDict, "body_feet")
        if rename == 'chest_piercings': modelList = getModelsInList(modelDict, "piercings_chest")
        if rename == 'amab_piercings': modelList = getModelsInList(modelDict, "piercings_amab")
        if rename == 'bpf': modelList = getModelsInList(modelDict, "genitals_bpf")

        modelDict = renameModels(modelDict, modelList, partNumber)

        if rename == 'chest_gear': modelDict = renameGear(modelDict, scene.chest_gear_list, partNumber)
        if rename == 'leg_gear': modelDict = renameGear(modelDict, scene.leg_gear_list, partNumber)
        if rename == 'hand_gear': modelDict = renameGear(modelDict, scene.hand_gear_list, partNumber)
        if rename == 'feet_gear': modelDict = renameGear(modelDict, scene.feet_gear_list, partNumber)

        if rename == 'selected':
            selected_objects = context.selected_objects
            for obj in selected_objects:
                split = obj.name.lower()
                index = split.find("part") + 5
                new = obj.name[:index] + str(partNumber) + obj.name[index+1:]
                obj.name = new
        
        if not rename == 'selected': setTextBlock(modelDict)

        return {'FINISHED'}
    
def renameModels(modelDict, modelList, partNumber):
    for name in modelList: # list of obj names
        obj = bpy.data.objects[name]
        split = obj.name.lower()
        index = split.find("part") + 5
        new = obj.name[:index] + str(partNumber) + obj.name[index+1:]
        obj.name = setModelName(modelDict, obj.name, new)
    return modelDict

def renameGear(modelDict, itemlist, partNumber):
    for item in itemlist:
        obj = item.obj_pointer
        old = obj.name.lower()
        index = old.find("part") + 5
        new = obj.name[:index] + str(partNumber) + obj.name[index+1:]
        item.name = new
        item.model_name = new
        obj.name = setModelName(modelDict, obj.name, new)
    return modelDict

def modelNameChange(self,context):
    modelDict = getTextBlock()
    obj = self.obj_pointer
    if obj:
        obj.name = setModelName(modelDict, obj.name, self.model_name)
    setTextBlock(modelDict)


# ============= # 
#   FBX STUFF   #
# ============= #

class TBSEKIT_OT_importFBX(Operator, ImportHelper):
    bl_idname = "object.importfbx"
    bl_label = "Import FBX"
    bl_description = "Bulk import FBXs with optimal setting for XIV modding"
    bl_options = {'REGISTER','UNDO'}

    filter_glob: StringProperty(default='*.fbx',options={'HIDDEN'})

    files: CollectionProperty(
            type=bpy.types.OperatorFileListElement,
            options={'HIDDEN', 'SKIP_SAVE'},
        )
    
    # CUSTOM OPTIONS
    fix_skeleton: BoolProperty(
        default=True,
        name="Fix Skeleton",
        description="Rotates bones of skeleton to make them more readable when editing.")
    fix_materials: BoolProperty(
        default=True,
        name="Fix Materials",
        description="Changes all materials to 'Alpha Hashed' and fixes metalics")
    delete_junk: BoolProperty(
        default=True,
        name="Delete Junk",
        description="Deletes all empty objects, importing only the mesh and armature")
    auto_assign_armature: BoolProperty(
        default=True,
        name="Auto Assign Armature",
        description="Deletes the armature that comes with the fbx and assigns all meshes to existing skeleton.\nRecommended to disable ONLY if fbx skeleton includes ex_ bones")
    
    def draw(self, context):
        layout = self.layout

        layout.label(text="== CUSTOM SETTINGS ==")
        box = layout.box()
        box.prop(self, 'fix_skeleton')
        box.prop(self, 'fix_materials')
        box.prop(self, 'delete_junk')
        row = box.row()
        row.prop(self, 'auto_assign_armature')
        row = layout.row()
        row.label(text="I recommended keeping all options enabled!")
        row.enabled=False

    def execute(self, context):
        folder = os.path.dirname(self.filepath)

        # OPTIONAL SETTING: rotates bone axis on imported skeleton
        if self.fix_skeleton:
            primary_axis = 'X'
            second_axis = 'Y'
        else:
            primary_axis = 'Y'
            second_axis = 'X'

        for meshfile in self.files:
            filepath = (os.path.join(folder, meshfile.name))
            bpy.ops.import_scene.fbx(
                filepath=filepath,
                use_anim=False,
                force_connect_children=True,
                primary_bone_axis=primary_axis,
                secondary_bone_axis=second_axis
            )
            importedfiles = context.selected_objects
            cleanImport(self, importedfiles)

        return {'FINISHED'}
    
# =================== #
#   RENAMING MODELS   #
# =================== #

class TBSEKIT_OT_rename(Operator):
    bl_idname = "object.renaming"
    bl_label = "Rename"
    bl_description = "This allows for bulk renaming of models, changing all models to Part X.Z to Part Y.Z"
    bl_options = {'REGISTER','UNDO'}

    def execute(self, context):
        scene = context.scene
        tbse_properties =  scene.tbse_kit_properties
        partNumber = tbse_properties["partNumber"]
        rename = tbse_properties.rename_options
        # gets json code
        modelDict = getTextBlock()
        modelList = []
        
        if rename == 'chest': 
            # create a list of obj names
            modelList = getModelsInList(modelDict, "body_neck")
            modelList.extend(getModelsInList(modelDict, "body_chest"))
            modelList.extend(getModelsInList(modelDict, "body_chest_w"))
            modelList.extend(getModelsInList(modelDict, "body_chest_chonk"))
        if rename == 'legs':
            modelList = getModelsInList(modelDict, "body_legs")
            modelList.extend(getModelsInList(modelDict, "body_legs_chonk"))
            modelList.extend(getModelsInList(modelDict, "body_genitals"))
            modelList.extend(getModelsInList(modelDict, "genitals_amab"))
            modelList.extend(getModelsInList(modelDict, "genitals_afab"))
        if rename == 'hands': modelList = getModelsInList(modelDict, "body_hands")
        if rename == 'feet': modelList = getModelsInList(modelDict, "body_feet")
        if rename == 'chest_piercings': modelList = getModelsInList(modelDict, "piercings_chest")
        if rename == 'amab_piercings': modelList = getModelsInList(modelDict, "piercings_amab")
        if rename == 'bpf': modelList = getModelsInList(modelDict, "genitals_bpf")

        modelDict = renameModels(modelDict, modelList, partNumber)

        if rename == 'chest_gear': modelDict = renameGear(modelDict, scene.chest_gear_list, partNumber)
        if rename == 'leg_gear': modelDict = renameGear(modelDict, scene.leg_gear_list, partNumber)
        if rename == 'hand_gear': modelDict = renameGear(modelDict, scene.hand_gear_list, partNumber)
        if rename == 'feet_gear': modelDict = renameGear(modelDict, scene.feet_gear_list, partNumber)

        if rename == 'selected':
            selected_objects = context.selected_objects
            for obj in selected_objects:
                split = obj.name.lower()
                index = split.find("part") + 5
                new = obj.name[:index] + str(partNumber) + obj.name[index+1:]
                obj.name = new
        
        if not rename == 'selected': setTextBlock(modelDict)

        return {'FINISHED'}
    
def renameModels(modelDict, modelList, partNumber):
    for name in modelList: # list of obj names
        obj = bpy.data.objects[name]
        split = obj.name.lower()
        index = split.find("part") + 5
        new = obj.name[:index] + str(partNumber) + obj.name[index+1:]
        obj.name = setModelName(modelDict, obj.name, new)
    return modelDict

def renameGear(modelDict, itemlist, partNumber):
    for item in itemlist:
        obj = item.obj_pointer
        old = obj.name.lower()
        index = old.find("part") + 5
        new = obj.name[:index] + str(partNumber) + obj.name[index+1:]
        item.name = new
        item.model_name = new
        obj.name = setModelName(modelDict, obj.name, new)
    return modelDict

def modelNameChange(self,context):
    modelDict = getTextBlock()
    obj = self.obj_pointer
    if obj:
        obj.name = setModelName(modelDict, obj.name, self.model_name)
    setTextBlock(modelDict)


# ============= # 
#   FBX STUFF   #
# ============= #

class TBSEKIT_OT_importFBX(Operator, ImportHelper):
    bl_idname = "object.importfbx"
    bl_label = "Import FBX"
    bl_description = "Bulk import FBXs with optimal setting for XIV modding"
    bl_options = {'REGISTER','UNDO'}

    filter_glob: StringProperty(default='*.fbx',options={'HIDDEN'})

    files: CollectionProperty(
            type=bpy.types.OperatorFileListElement,
            options={'HIDDEN', 'SKIP_SAVE'},
        )
    
    # CUSTOM OPTIONS
    fix_skeleton: BoolProperty(
        default=True,
        name="Fix Skeleton",
        description="Rotates bones of skeleton to make them more readable when editing.")
    fix_materials: BoolProperty(
        default=True,
        name="Fix Materials",
        description="Changes all materials to 'Alpha Hashed' and fixes metalics")
    delete_junk: BoolProperty(
        default=True,
        name="Delete Junk",
        description="Deletes all empty objects, importing only the mesh and armature")
    auto_assign_armature: BoolProperty(
        default=True,
        name="Auto Assign Armature",
        description="Deletes the armature that comes with the fbx and assigns all meshes to existing skeleton.\nRecommended to disable ONLY if fbx skeleton includes ex_ bones")
    
    def draw(self, context):
        layout = self.layout

        layout.label(text="== CUSTOM SETTINGS ==")
        box = layout.box()
        box.prop(self, 'fix_skeleton')
        box.prop(self, 'fix_materials')
        box.prop(self, 'delete_junk')
        row = box.row()
        row.prop(self, 'auto_assign_armature')
        row = layout.row()
        row.label(text="I recommended keeping all options enabled!")
        row.enabled=False

    def execute(self, context):
        folder = os.path.dirname(self.filepath)

        # OPTIONAL SETTING: rotates bone axis on imported skeleton
        if self.fix_skeleton:
            primary_axis = 'X'
            second_axis = 'Y'
        else:
            primary_axis = 'Y'
            second_axis = 'X'

        for meshfile in self.files:
            filepath = (os.path.join(folder, meshfile.name))
            bpy.ops.import_scene.fbx(
                filepath=filepath,
                use_anim=False,
                force_connect_children=True,
                primary_bone_axis=primary_axis,
                secondary_bone_axis=second_axis
            )
            importedfiles = context.selected_objects
            cleanImport(self, importedfiles)

        return {'FINISHED'}
    
# =================== #
#   RENAMING MODELS   #
# =================== #

class TBSEKIT_OT_rename(Operator):
    bl_idname = "object.renaming"
    bl_label = "Rename"
    bl_description = "This allows for bulk renaming of models, changing all models to Part X.Z to Part Y.Z"
    bl_options = {'REGISTER','UNDO'}

    def execute(self, context):
        scene = context.scene
        tbse_properties =  scene.tbse_kit_properties
        partNumber = tbse_properties["partNumber"]
        rename = tbse_properties.rename_options
        # gets json code
        modelDict = getTextBlock()
        modelList = []
        
        if rename == 'chest': 
            # create a list of obj names
            modelList = getModelsInList(modelDict, "body_neck")
            modelList.extend(getModelsInList(modelDict, "body_chest"))
            modelList.extend(getModelsInList(modelDict, "body_chest_w"))
            modelList.extend(getModelsInList(modelDict, "body_chest_chonk"))
        if rename == 'legs':
            modelList = getModelsInList(modelDict, "body_legs")
            modelList.extend(getModelsInList(modelDict, "body_legs_chonk"))
            modelList.extend(getModelsInList(modelDict, "body_genitals"))
            modelList.extend(getModelsInList(modelDict, "genitals_amab"))
            modelList.extend(getModelsInList(modelDict, "genitals_afab"))
        if rename == 'hands': modelList = getModelsInList(modelDict, "body_hands")
        if rename == 'feet': modelList = getModelsInList(modelDict, "body_feet")
        if rename == 'chest_piercings': modelList = getModelsInList(modelDict, "piercings_chest")
        if rename == 'amab_piercings': modelList = getModelsInList(modelDict, "piercings_amab")
        if rename == 'bpf': modelList = getModelsInList(modelDict, "genitals_bpf")

        modelDict = renameModels(modelDict, modelList, partNumber)

        if rename == 'chest_gear': modelDict = renameGear(modelDict, scene.chest_gear_list, partNumber)
        if rename == 'leg_gear': modelDict = renameGear(modelDict, scene.leg_gear_list, partNumber)
        if rename == 'hand_gear': modelDict = renameGear(modelDict, scene.hand_gear_list, partNumber)
        if rename == 'feet_gear': modelDict = renameGear(modelDict, scene.feet_gear_list, partNumber)

        if rename == 'selected':
            selected_objects = context.selected_objects
            for obj in selected_objects:
                split = obj.name.lower()
                index = split.find("part") + 5
                new = obj.name[:index] + str(partNumber) + obj.name[index+1:]
                obj.name = new
        
        if not rename == 'selected': setTextBlock(modelDict)

        return {'FINISHED'}
    
def renameModels(modelDict, modelList, partNumber):
    for name in modelList: # list of obj names
        obj = bpy.data.objects[name]
        split = obj.name.lower()
        index = split.find("part") + 5
        new = obj.name[:index] + str(partNumber) + obj.name[index+1:]
        obj.name = setModelName(modelDict, obj.name, new)
    return modelDict

def renameGear(modelDict, itemlist, partNumber):
    for item in itemlist:
        obj = item.obj_pointer
        old = obj.name.lower()
        index = old.find("part") + 5
        new = obj.name[:index] + str(partNumber) + obj.name[index+1:]
        item.name = new
        item.model_name = new
        obj.name = setModelName(modelDict, obj.name, new)
    return modelDict

def modelNameChange(self,context):
    modelDict = getTextBlock()
    obj = self.obj_pointer
    if obj:
        obj.name = setModelName(modelDict, obj.name, self.model_name)
    setTextBlock(modelDict)


# ============= # 
#   FBX STUFF   #
# ============= #

class TBSEKIT_OT_importFBX(Operator, ImportHelper):
    bl_idname = "object.importfbx"
    bl_label = "Import FBX"
    bl_description = "Bulk import FBXs with optimal setting for XIV modding"
    bl_options = {'REGISTER','UNDO'}

    filter_glob: StringProperty(default='*.fbx',options={'HIDDEN'})

    files: CollectionProperty(
            type=bpy.types.OperatorFileListElement,
            options={'HIDDEN', 'SKIP_SAVE'},
        )
    
    # CUSTOM OPTIONS
    fix_skeleton: BoolProperty(
        default=True,
        name="Fix Skeleton",
        description="Rotates bones of skeleton to make them more readable when editing.")
    fix_materials: BoolProperty(
        default=True,
        name="Fix Materials",
        description="Changes all materials to 'Alpha Hashed' and fixes metalics")
    delete_junk: BoolProperty(
        default=True,
        name="Delete Junk",
        description="Deletes all empty objects, importing only the mesh and armature")
    auto_assign_armature: BoolProperty(
        default=True,
        name="Auto Assign Armature",
        description="Deletes the armature that comes with the fbx and assigns all meshes to existing skeleton.\nRecommended to disable ONLY if fbx skeleton includes ex_ bones")
    
    def draw(self, context):
        layout = self.layout

        layout.label(text="== CUSTOM SETTINGS ==")
        box = layout.box()
        box.prop(self, 'fix_skeleton')
        box.prop(self, 'fix_materials')
        box.prop(self, 'delete_junk')
        row = box.row()
        row.prop(self, 'auto_assign_armature')
        row = layout.row()
        row.label(text="I recommended keeping all options enabled!")
        row.enabled=False

    def execute(self, context):
        folder = os.path.dirname(self.filepath)

        # OPTIONAL SETTING: rotates bone axis on imported skeleton
        if self.fix_skeleton:
            primary_axis = 'X'
            second_axis = 'Y'
        else:
            primary_axis = 'Y'
            second_axis = 'X'

        for meshfile in self.files:
            filepath = (os.path.join(folder, meshfile.name))
            bpy.ops.import_scene.fbx(
                filepath=filepath,
                use_anim=False,
                force_connect_children=True,
                primary_bone_axis=primary_axis,
                secondary_bone_axis=second_axis
            )
            importedfiles = context.selected_objects
            cleanImport(self, importedfiles)

        return {'FINISHED'}
    
# =================== #
#   RENAMING MODELS   #
# =================== #

class TBSEKIT_OT_rename(Operator):
    bl_idname = "object.renaming"
    bl_label = "Rename"
    bl_description = "This allows for bulk renaming of models, changing all models to Part X.Z to Part Y.Z"
    bl_options = {'REGISTER','UNDO'}

    def execute(self, context):
        scene = context.scene
        tbse_properties =  scene.tbse_kit_properties
        partNumber = tbse_properties["partNumber"]
        rename = tbse_properties.rename_options
        # gets json code
        modelDict = getTextBlock()
        modelList = []
        
        if rename == 'chest': 
            # create a list of obj names
            modelList = getModelsInList(modelDict, "body_neck")
            modelList.extend(getModelsInList(modelDict, "body_chest"))
            modelList.extend(getModelsInList(modelDict, "body_chest_w"))
            modelList.extend(getModelsInList(modelDict, "body_chest_chonk"))
        if rename == 'legs':
            modelList = getModelsInList(modelDict, "body_legs")
            modelList.extend(getModelsInList(modelDict, "body_legs_chonk"))
            modelList.extend(getModelsInList(modelDict, "body_genitals"))
            modelList.extend(getModelsInList(modelDict, "genitals_amab"))
            modelList.extend(getModelsInList(modelDict, "genitals_afab"))
        if rename == 'hands': modelList = getModelsInList(modelDict, "body_hands")
        if rename == 'feet': modelList = getModelsInList(modelDict, "body_feet")
        if rename == 'chest_piercings': modelList = getModelsInList(modelDict, "piercings_chest")
        if rename == 'amab_piercings': modelList = getModelsInList(modelDict, "piercings_amab")
        if rename == 'bpf': modelList = getModelsInList(modelDict, "genitals_bpf")

        modelDict = renameModels(modelDict, modelList, partNumber)

        if rename == 'chest_gear': modelDict = renameGear(modelDict, scene.chest_gear_list, partNumber)
        if rename == 'leg_gear': modelDict = renameGear(modelDict, scene.leg_gear_list, partNumber)
        if rename == 'hand_gear': modelDict = renameGear(modelDict, scene.hand_gear_list, partNumber)
        if rename == 'feet_gear': modelDict = renameGear(modelDict, scene.feet_gear_list, partNumber)

        if rename == 'selected':
            selected_objects = context.selected_objects
            for obj in selected_objects:
                split = obj.name.lower()
                index = split.find("part") + 5
                new = obj.name[:index] + str(partNumber) + obj.name[index+1:]
                obj.name = new
        
        if not rename == 'selected': setTextBlock(modelDict)

        return {'FINISHED'}
    
def renameModels(modelDict, modelList, partNumber):
    for name in modelList: # list of obj names
        obj = bpy.data.objects[name]
        split = obj.name.lower()
        index = split.find("part") + 5
        new = obj.name[:index] + str(partNumber) + obj.name[index+1:]
        obj.name = setModelName(modelDict, obj.name, new)
    return modelDict

def renameGear(modelDict, itemlist, partNumber):
    for item in itemlist:
        obj = item.obj_pointer
        old = obj.name.lower()
        index = old.find("part") + 5
        new = obj.name[:index] + str(partNumber) + obj.name[index+1:]
        item.name = new
        item.model_name = new
        obj.name = setModelName(modelDict, obj.name, new)
    return modelDict

def modelNameChange(self,context):
    modelDict = getTextBlock()
    obj = self.obj_pointer
    if obj:
        obj.name = setModelName(modelDict, obj.name, self.model_name)
    setTextBlock(modelDict)


# ============= # 
#   FBX STUFF   #
# ============= #

class TBSEKIT_OT_importFBX(Operator, ImportHelper):
    bl_idname = "object.importfbx"
    bl_label = "Import FBX"
    bl_description = "Bulk import FBXs with optimal setting for XIV modding"
    bl_options = {'REGISTER','UNDO'}

    filter_glob: StringProperty(default='*.fbx',options={'HIDDEN'})

    files: CollectionProperty(
            type=bpy.types.OperatorFileListElement,
            options={'HIDDEN', 'SKIP_SAVE'},
        )
    
    # CUSTOM OPTIONS
    fix_skeleton: BoolProperty(
        default=True,
        name="Fix Skeleton",
        description="Rotates bones of skeleton to make them more readable when editing.")
    fix_materials: BoolProperty(
        default=True,
        name="Fix Materials",
        description="Changes all materials to 'Alpha Hashed' and fixes metalics")
    delete_junk: BoolProperty(
        default=True,
        name="Delete Junk",
        description="Deletes all empty objects, importing only the mesh and armature")
    auto_assign_armature: BoolProperty(
        default=True,
        name="Auto Assign Armature",
        description="Deletes the armature that comes with the fbx and assigns all meshes to existing skeleton.\nRecommended to disable ONLY if fbx skeleton includes ex_ bones")
    
    def draw(self, context):
        layout = self.layout

        layout.label(text="== CUSTOM SETTINGS ==")
        box = layout.box()
        box.prop(self, 'fix_skeleton')
        box.prop(self, 'fix_materials')
        box.prop(self, 'delete_junk')
        row = box.row()
        row.prop(self, 'auto_assign_armature')
        row = layout.row()
        row.label(text="I recommended keeping all options enabled!")
        row.enabled=False

    def execute(self, context):
        folder = os.path.dirname(self.filepath)

        # OPTIONAL SETTING: rotates bone axis on imported skeleton
        if self.fix_skeleton:
            primary_axis = 'X'
            second_axis = 'Y'
        else:
            primary_axis = 'Y'
            second_axis = 'X'

        for meshfile in self.files:
            filepath = (os.path.join(folder, meshfile.name))
            bpy.ops.import_scene.fbx(
                filepath=filepath,
                use_anim=False,
                force_connect_children=True,
                primary_bone_axis=primary_axis,
                secondary_bone_axis=second_axis
            )
            importedfiles = context.selected_objects
            cleanImport(self, importedfiles)

        return {'FINISHED'}
    
# =================== #
#   RENAMING MODELS   #
# =================== #

class TBSEKIT_OT_rename(Operator):
    bl_idname = "object.renaming"
    bl_label = "Rename"
    bl_description = "This allows for bulk renaming of models, changing all models to Part X.Z to Part Y.Z"
    bl_options = {'REGISTER','UNDO'}

    def execute(self, context):
        scene = context.scene
        tbse_properties =  scene.tbse_kit_properties
        partNumber = tbse_properties["partNumber"]
        rename = tbse_properties.rename_options
        # gets json code
        modelDict = getTextBlock()
        modelList = []
        
        if rename == 'chest': 
            # create a list of obj names
            modelList = getModelsInList(modelDict, "body_neck")
            modelList.extend(getModelsInList(modelDict, "body_chest"))
            modelList.extend(getModelsInList(modelDict, "body_chest_w"))
            modelList.extend(getModelsInList(modelDict, "body_chest_chonk"))
        if rename == 'legs':
            modelList = getModelsInList(modelDict, "body_legs")
            modelList.extend(getModelsInList(modelDict, "body_legs_chonk"))
            modelList.extend(getModelsInList(modelDict, "body_genitals"))
            modelList.extend(getModelsInList(modelDict, "genitals_amab"))
            modelList.extend(getModelsInList(modelDict, "genitals_afab"))
        if rename == 'hands': modelList = getModelsInList(modelDict, "body_hands")
        if rename == 'feet': modelList = getModelsInList(modelDict, "body_feet")
        if rename == 'chest_piercings': modelList = getModelsInList(modelDict, "piercings_chest")
        if rename == 'amab_piercings': modelList = getModelsInList(modelDict, "piercings_amab")
        if rename == 'bpf': modelList = getModelsInList(modelDict, "genitals_bpf")

        modelDict = renameModels(modelDict, modelList, partNumber)

        if rename == 'chest_gear': modelDict = renameGear(modelDict, scene.chest_gear_list, partNumber)
        if rename == 'leg_gear': modelDict = renameGear(modelDict, scene.leg_gear_list, partNumber)
        if rename == 'hand_gear': modelDict = renameGear(modelDict, scene.hand_gear_list, partNumber)
        if rename == 'feet_gear': modelDict = renameGear(modelDict, scene.feet_gear_list, partNumber)

        if rename == 'selected':
            selected_objects = context.selected_objects
            for obj in selected_objects:
                split = obj.name.lower()
                index = split.find("part") + 5
                new = obj.name[:index] + str(partNumber) + obj.name[index+1:]
                obj.name = new
        
        if not rename == 'selected': setTextBlock(modelDict)

        return {'FINISHED'}
    
def renameModels(modelDict, modelList, partNumber):
    for name in modelList: # list of obj names
        obj = bpy.data.objects[name]
        split = obj.name.lower()
        index = split.find("part") + 5
        new = obj.name[:index] + str(partNumber) + obj.name[index+1:]
        obj.name = setModelName(modelDict, obj.name, new)
    return modelDict

def renameGear(modelDict, itemlist, partNumber):
    for item in itemlist:
        obj = item.obj_pointer
        old = obj.name.lower()
        index = old.find("part") + 5
        new = obj.name[:index] + str(partNumber) + obj.name[index+1:]
        item.name = new
        item.model_name = new
        obj.name = setModelName(modelDict, obj.name, new)
    return modelDict

def modelNameChange(self,context):
    modelDict = getText