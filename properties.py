
import bpy
from bpy.props import (BoolProperty, EnumProperty, IntProperty, StringProperty, PointerProperty, CollectionProperty)
from bpy.types import PropertyGroup
from bpy.types import UIList

def chestToggle(self, context):
    tbse_properties = context.scene.tbse_kit_properties
    chest_shape = tbse_properties.chest_shape
    modelDict = getTextBlock()
    tbse_neck = getModelsInList(modelDict, "body_neck")
    body_chest = getModelsInList(modelDict, "body_chest")
    body_chest_w = getModelsInList(modelDict, "body_chest_w")
    body_chest_chonk = getModelsInList(modelDict, "body_chest_chonk")
    body_chest_chonk1 = getModelsInList(modelDict, "body_chest_chonk1")
    piercings_chest = getModelsInList(modelDict, "piercings_chest")
    bpy.data.objects[tbse_neck[0]].hide_set(True)
    for obj in body_chest: bpy.data.objects[obj].hide_set(True)
    for obj in body_chest_w: bpy.data.objects[obj].hide_set(True)
    for obj in body_chest_chonk: bpy.data.objects[obj].hide_set(True)
    for obj in body_chest_chonk1: bpy.data.objects[obj].hide_set(True)
    for obj in piercings_chest: bpy.data.objects[obj].hide_set(True)
    if tbse_properties['show_chest']:
        bpy.data.objects[tbse_neck[0]].hide_set(False)
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
    tbse_properties = context.scene.tbse_kit_properties
    leg_shape = tbse_properties.leg_shape
    modelDict = getTextBlock()
    body_legs = getModelsInList(modelDict, "body_legs")
    body_legs_chonk = getModelsInList(modelDict, "body_legs_chonk")
    body_genitals = getModelsInList(modelDict, "body_genitals")
    for obj in body_legs:
        if obj in bpy.data.objects:
            bpy.data.objects[obj].hide_set(True)
    for obj in body_legs_chonk:
        if obj in bpy.data.objects:
            bpy.data.objects[obj].hide_set(True)
    for obj in body_genitals:
        if obj in bpy.data.objects:
            bpy.data.objects[obj].hide_set(True)
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
            if tbse_properties.genital_toggle == 'amab' or leg_shape == 'xl':
                if leg_shape == 'xl':
                    setattr(tbse_properties, 'genital_toggle', 'amab')
                if body_genitals and body_genitals[0] in bpy.data.objects:
                    pass
            else:
                if body_genitals and len(body_genitals) > 1 and body_genitals[1] in bpy.data.objects:
                    pass
    nsfwToggle(self, context)

def nsfwToggle(self, context):
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
    if tbse_properties['show_nsfw']:
        if tbse_properties.leg_shape == 'chonk' and tbse_properties['show_legs']:
            if body_legs_chonk and len(body_legs_chonk) > 3 and body_legs_chonk[3] in bpy.data.objects:
                bpy.data.objects[body_legs_chonk[3]].hide_set(False)
        else:
            genitalSet(self, context)
        if tbse_properties['show_piercings_amab']:
            amabPiercingToggle(self, context)

def handToggle(self, context):
    tbse_properties = context.scene.tbse_kit_properties
    modelDict = getTextBlock()
    body_hands = getModelsInList(modelDict, "body_hands")
    if body_hands and body_hands[0] in bpy.data.objects:
        bpy.data.objects[body_hands[0]].hide_set(not tbse_properties['show_hands'])

def feetToggle(self, context):
    tbse_properties = context.scene.tbse_kit_properties
    modelDict = getTextBlock()
    body_feet = getModelsInList(modelDict, "body_feet")
    if body_feet and body_feet[0] in bpy.data.objects:
        bpy.data.objects[body_feet[0]].hide_set(not tbse_properties['show_feet'])

def bpfToggle(self, context):
    tbse_properties = context.scene.tbse_kit_properties
    modelDict = getTextBlock()
    genitals_bpf = getModelsInList(modelDict, "genitals_bpf")
    if tbse_properties.leg_shape == 'chonk' or tbse_properties.leg_shape == 'xl':
        return
    elif tbse_properties['show_nsfw'] and tbse_properties['show_bpf'] and tbse_properties.genital_toggle == 'afab':
        for obj in genitals_bpf:
            if obj in bpy.data.objects:
                pass
    else:
        for obj in genitals_bpf:
            if obj in bpy.data.objects:
                pass

def chest_driver(self, context):
    tbse_properties = context.scene.tbse_kit_properties
    modelDict = getTextBlock()
    chest_resetDrivers()
    index = 0
    if not tbse_properties.chest_shape == 'tbse':
        pass
    chestToggle(self, context)
    modelList = getModelsInList(modelDict, "body_chest")
    modelList.extend(getModelsInList(modelDict, "gear_chest"))
    modelList.extend(getModelsInList(modelDict, "gear_hands"))
    chest_shape = tbse_properties.chest_shape
    for obj in modelList:
        pass

def leg_driver(self, context):
    tbse_properties = context.scene.tbse_kit_properties
    modelDict = getTextBlock()
    leg_resetDrivers()
    index = 0
    if not tbse_properties.leg_shape == 'tbse':
        pass
    legToggle(self, context)
    modelList = getModelsInList(modelDict, "body_legs")
    modelList.extend(getModelsInList(modelDict, "gear_legs"))
    modelList.extend(getModelsInList(modelDict, "gear_feet"))
    leg_shape = tbse_properties.leg_shape
    for obj in modelList:
        pass

def genitalToggle(self, context):
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

def genitalSet(self, context):
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
        if tbse_properties.genital_toggle == 'amab' or tbse_properties.leg_shape in ('xl', 'chonk'):
            pass
        else:
            pass

def modelNameChange(self, context):
    modelDict = getTextBlock()
    obj = self.obj_pointer
    if obj:
        pass
    setTextBlock(modelDict)

def gearToggle(self, context):
    obj = self.obj_pointer
    if obj:
        pass

def boneToggles(self, context):
    tbse_properties = context.scene.tbse_kit_properties
    armature = None
    for obj in context.scene.objects:
        pass
    if not armature:
        pass
    armature.data.layers[0] = tbse_properties.show_base_bones
    armature.data.layers[1] = tbse_properties.show_skirt_bones
    armature.data.layers[2] = tbse_properties.show_tail_bones
    armature.data.layers[3] = tbse_properties.show_extra_bones
    armature.data.layers[16] = tbse_properties.show_ivcs_bones
    armature.data.layers[17] = tbse_properties.show_ivcs2_bones

    tbse_properties = context.scene.tbse_kit_properties
    chest_toggles = context.scene.tbse_chest_toggles
    modelDict = getTextBlock()
    piercings_chest = getModelsInList(modelDict, "piercings_chest")
    # Hide all chest piercings by default
    for obj in piercings_chest:
        if obj in bpy.data.objects:
            bpy.data.objects[obj].hide_set(True)
    # Show enabled piercings if toggle is on
    if tbse_properties['show_piercings_chest']:
        if hasattr(chest_toggles, "nipple_ring") and chest_toggles.nipple_ring:
            if len(piercings_chest) > 0 and piercings_chest[0] in bpy.data.objects:
                bpy.data.objects[piercings_chest[0]].hide_set(False)
        if hasattr(chest_toggles, "nipple_bar") and chest_toggles.nipple_bar:
            if len(piercings_chest) > 1 and piercings_chest[1] in bpy.data.objects:
                bpy.data.objects[piercings_chest[1]].hide_set(False)
        if hasattr(chest_toggles, "nipple_spike") and chest_toggles.nipple_spike:
            if len(piercings_chest) > 2 and piercings_chest[2] in bpy.data.objects:
                bpy.data.objects[piercings_chest[2]].hide_set(False)
        if hasattr(chest_toggles, "navel_bar") and chest_toggles.navel_bar:
            if len(piercings_chest) > 3 and piercings_chest[3] in bpy.data.objects:
                bpy.data.objects[piercings_chest[3]].hide_set(False)
        if hasattr(chest_toggles, "navel_spike") and chest_toggles.navel_spike:
            if len(piercings_chest) > 4 and piercings_chest[4] in bpy.data.objects:
                bpy.data.objects[piercings_chest[4]].hide_set(False)
        if hasattr(chest_toggles, "hip_bar") and chest_toggles.hip_bar:
            if len(piercings_chest) > 5 and piercings_chest[5] in bpy.data.objects:
                bpy.data.objects[piercings_chest[5]].hide_set(False)
        if hasattr(chest_toggles, "hip_spike") and chest_toggles.hip_spike:
            if len(piercings_chest) > 6 and piercings_chest[6] in bpy.data.objects:
                bpy.data.objects[piercings_chest[6]].hide_set(False)
    pass
def amabPiercingToggle(self, context):
    tbse_properties = context.scene.tbse_kit_properties
    amab_toggles = context.scene.tbse_amab_toggles
    modelDict = getTextBlock()
    piercings_amab = getModelsInList(modelDict, "piercings_amab")
    # Hide all AMAB piercings by default
    for obj in piercings_amab:
        if obj in bpy.data.objects:
            bpy.data.objects[obj].hide_set(True)
    # Show enabled piercings if toggle is on
    if tbse_properties['show_piercings_amab']:
        if hasattr(amab_toggles, "jacob_piercing") and amab_toggles.jacob_piercing:
            if len(piercings_amab) > 0 and piercings_amab[0] in bpy.data.objects:
                bpy.data.objects[piercings_amab[0]].hide_set(False)
        if hasattr(amab_toggles, "albert_piercing") and amab_toggles.albert_piercing:
            if len(piercings_amab) > 1 and piercings_amab[1] in bpy.data.objects:
                bpy.data.objects[piercings_amab[1]].hide_set(False)

class TBSEKIT_TBSEProperties(PropertyGroup):
    """
    Main property group for TBSE Body Kit settings.
    Stores all user toggles, enums, and options for body part visibility, shape selection, gear, bone groups, and renaming.
    """
    show_chest:             BoolProperty(default=True,  update=chestToggle) 
    show_legs:              BoolProperty(default=True,  update=legToggle)
    show_nsfw:              BoolProperty(default=False, update=nsfwToggle)
    show_hands:             BoolProperty(default=True,  update=handToggle)
    show_feet:              BoolProperty(default=True,  update=feetToggle)
    show_bpf:               BoolProperty(default=True,  update=bpfToggle)
    show_piercings_chest:   BoolProperty(default=False, update=chestToggle)
    show_piercings_amab:    BoolProperty(default=False, update=nsfwToggle)

    chest_shape: EnumProperty(
        name="Chest Shapes",
        description="Toggle between all chest shapes.",
        update=chest_driver,
        items=[
            ('tbse',        "TBSE",             "Original body shape created by Tsar"),
            ('slim',        "Slim",             "Body edit created by Mimi"),
            ('w',           "Type W",           "Body edit created by Westlaketea"),
            ('sbtl',        "SBTL",             "Body edit created by Chibi + LunarEclipse"),
            ('sbtlslimmer', "SBTL Slim",        "Body edit created by Chibi + LunarEclipse"),
            ('twink',       "Twink",            "Body edit created by Red"),
            ('twunk',       "Twunk",            "Body edit created by Red"),
            ('hunk',        "Hunk",             "Body edit created by Red"),
            ('offtwunk',    "Off-season Twunk", "Body edit created by Red"),
            ('offhunk',     "Off-season Hunk",  "Body edit created by Red"),
            ('chonk',       "Chonk",            "Body edit created by Nick"),
            ('chonk1',      "Chonk 1.0",        "Body edit created by Nick"),
            ('cub',         "Cub",              "Body edit created by Nick"),
            ('xl',          "TBSE XL",          "Body edit created by Cheembs"),
        ]
    )
    leg_shape: EnumProperty(
        name="Leg Shapes",
        description="Toggle between all leg shapes.",
        update=leg_driver,
        items=[
            ('tbse',    "TBSE",     "Original leg shape created by Tsar"),
            ('twink',   "Twink",    "Leg edit created by Red"),
            ('sbtl',    "SBTL",     "Leg edit created by Chibi + LunarEclipse"),
            ('hunk',    "Hunk",     "Leg edit created by Red"),
            ('chonk',   "Chonk",    "Leg edit created by Nick"),
            ('xl',      "TBSE XL",  "Leg edit created by Cheembs")
        ]
    )
    genital_toggle: EnumProperty(
        name="Genital Type",
        description="Toggle between AMAB and AFAB.",
        update=genitalToggle,
        items=[ 
            ('amab',    "AMAB",     ""),
            ('afab',    "AFAB",     "")
            ]
    )
    amab_type: EnumProperty(
        name="AMAB Type",
        description="Toggle between different AMAB gential types.",
        update=genitalSet,
        items=[
            ('a',       "Gen A",    ""),
            ('b',       "Gen B",    ""),
            ('c',       "Gen C",    ""),
            ('d',       "Gen D",    ""),
            ('squish',  "Squish", "Used for nsfw outfits that would show part of the amab model but squished while in an outfit.")
            ]
    )
    afab_type: EnumProperty(
        description="Toggle between different AFAB gential types.",
        update=genitalSet,
        items=[
            ('a',       "Gen A",    ""),
            ('b',       "Gen B",    ""),
            ('c',       "Gen C",    ""),
            ('bbwvr',   "BBWVR",    "")
            ]
    )
    rename_options: EnumProperty(
        name="Renaming Models",
        description="Options groups for renaming models",
        items = [
            ('chest',           "Chest Models",         ""),
            ('legs',            "Leg Models",           ""),
            ('hands',           "Hand Models",          ""),
            ('feet',            "Feet Models",          ""),
            ('chest_piercings', "Chest Piercings",      ""),
            ('amab_piercings',  "AMAB Piercings",       ""),
            ('bpf',             "BPF Models",           ""),
            ('chest_gear',      "Chest Gear Models",    ""),
            ('leg_gear',        "Leg Gear Models",      ""),
            ('hand_gear',       "Hand Gear Models",     ""),
            ('feet_gear',       "Feet Gear Models",     ""),
            ('selected',        "Selected Models Only", "")
        ]
    )
    partNumber: IntProperty(default=0,min=0)
    show_chest_gear:        BoolProperty(default=True,  update=chestGearToggle)
    show_leg_gear:          BoolProperty(default=True,  update=legGearToggle)
    show_hand_gear:         BoolProperty(default=True,  update=handGearToggle)
    show_feet_gear:         BoolProperty(default=True,  update=feetGearToggle)
    show_armature:          BoolProperty(default=True,  update=boneToggles)
    show_base_bones:        BoolProperty(default=True,  update=boneToggles)
    show_skirt_bones:       BoolProperty(default=True,  update=boneToggles)
    show_extra_bones:       BoolProperty(default=True,  update=boneToggles)
    show_tail_bones:        BoolProperty(default=True,  update=boneToggles)
    show_ivcs_bones:        BoolProperty(default=False, update=boneToggles)
    show_ivcs2_bones:       BoolProperty(default=False, update=boneToggles)

class TBSEKIT_chestPiercingToggles(PropertyGroup):
    nipple_ring:        BoolProperty(name="Nipple Ring",    default=True, update=chestPiercingToggle)
    nipple_bar:         BoolProperty(name="Nipple Bar",     default=True, update=chestPiercingToggle)
    nipple_spike:       BoolProperty(name="Nipple Spike",   default=True, update=chestPiercingToggle)
    navel_bar:          BoolProperty(name="Navel Bar",      default=True, update=chestPiercingToggle)
    navel_spike:        BoolProperty(name="Navel Spike",    default=True, update=chestPiercingToggle)
    hip_bar:            BoolProperty(name="Hip Bar",        default=True, update=chestPiercingToggle)
    hip_spike:          BoolProperty(name="Hip Spike",      default=True, update=chestPiercingToggle)

class TBSEKIT_AMABPiercingToggles(PropertyGroup):
    jacob_piercing:     BoolProperty(name="Jacob's Ladder", default=True, update=amabPiercingToggle)
    albert_piercing:    BoolProperty(name="Prince Albert",  default=True, update=amabPiercingToggle)

class ChestListItem(PropertyGroup):
    model_name:         StringProperty(name="Chest Model",
                                       default="Empty Chest Piece",
                                       update=modelNameChange)
    obj_pointer:        PointerProperty(type=bpy.types.Object)
    isEnabled:          BoolProperty(default=True, update=gearToggle)
class LegListItem(PropertyGroup):
    model_name:         StringProperty(name="Leg Model",
                                       default="Empty Leg Piece",
                                       update=modelNameChange)
    obj_pointer:        PointerProperty(type=bpy.types.Object)
    isEnabled:          BoolProperty(default=True, update=gearToggle)
class HandListItem(PropertyGroup):
    model_name:         StringProperty(name="Hand Model",
                                       default="Empty Hand Piece",
                                       update=modelNameChange)
    obj_pointer:        PointerProperty(type=bpy.types.Object)
    isEnabled:          BoolProperty(default=True, update=gearToggle)
class FeetListItem(PropertyGroup):
    model_name:         StringProperty(name="Feet Model",
                                       default="Empty Feet Piece",
                                       update=modelNameChange)
    obj_pointer:        PointerProperty(type=bpy.types.Object)
    isEnabled:          BoolProperty(default=True, update=gearToggle)

class TBSEKIT_BulkExport(PropertyGroup):
    file_name:              StringProperty(default="Untitled")
    iteration_ver:          IntProperty(default=1)

    export_chest:           BoolProperty(default=False)
    export_legs:            BoolProperty(default=False)
    export_hands:           BoolProperty(default=False)
    hands_with_arms:        BoolProperty(default=False)
    export_feet:            BoolProperty(default=False)
    feet_with_legs:        BoolProperty(default=False)

    export_chest_tbse:      BoolProperty(default=True)
    export_chest_slim:      BoolProperty(default=False)
    export_chest_w:         BoolProperty(default=False)
    export_chest_sblt:      BoolProperty(default=False)
    export_chest_sbltslim:  BoolProperty(default=False)
    export_chest_twink:     BoolProperty(default=False)
    export_chest_twunk:     BoolProperty(default=False)
    export_chest_hunk:      BoolProperty(default=False)
    export_chest_offtwunk:  BoolProperty(default=False)
    export_chest_offhunk:   BoolProperty(default=False)
    export_chest_chonk1:    BoolProperty(default=False)
    export_chest_chonk2:    BoolProperty(default=False)
    export_chest_cub:       BoolProperty(default=False)
    export_chest_xl:        BoolProperty(default=False)

    export_legs_tbse:       BoolProperty(default=True)
    export_legs_twink:      BoolProperty(default=False)
    export_legs_sbtl:       BoolProperty(default=False)
    export_legs_hunk:       BoolProperty(default=False)
    export_legs_chonk:      BoolProperty(default=False)
    export_legs_xl:         BoolProperty(default=False)

    export_nsfw_amab:       BoolProperty(default=True)
    export_nsfw_afab:       BoolProperty(default=False)

    with_nsfw:              BoolProperty(default=False)
    with_chest_piercings:   BoolProperty(default=False)
    with_amab_piercings:    BoolProperty(default=False)
