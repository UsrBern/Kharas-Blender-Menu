
# type: ignore
# Pylance ignore for Blender Python API - property definitions use special syntax not compatible with standard type annotations
# If you're not a programmer, you can ignore this comment.

# Property definitions for TBSE Body Kit Blender Addon
# This file contains all the properties used in the addon, including enums and options for body part visibility, shape selection, gear, bone groups, and renaming.
import bpy
from bpy.props import (BoolProperty, EnumProperty, IntProperty, StringProperty, PointerProperty, CollectionProperty)
from bpy.types import PropertyGroup
from bpy.types import UIList
from .json_helpers import getTextBlock, getModelsInList, setTextBlock
from .drivers import chest_resetDrivers, leg_resetDrivers, afab_driver, amab_driver
from .toggles import (
    chestToggle, legToggle, nsfwToggle, handToggle, feetToggle, 
    genitalToggle, bpfToggle, genitalSet, boneToggles,
    chestPiercingToggle, amabPiercingToggle, 
    chestGearToggle, legGearToggle, handGearToggle, feetGearToggle, 
    gearToggle, modelNameChange
)
from .drivers import chest_driver, leg_driver
from .gear_helpers import select_chest_gear, select_leg_gear, select_hand_gear, select_feet_gear


class TBSEKIT_TBSEProperties(PropertyGroup):
    # Main property group for TBSE Body Kit settings.
    # Stores all user options for body part visibility, shape selection, gear, bone groups, and renaming.
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


# Registration
def register():
    bpy.utils.register_class(TBSEKIT_TBSEProperties)
    bpy.utils.register_class(TBSEKIT_chestPiercingToggles)
    bpy.utils.register_class(TBSEKIT_AMABPiercingToggles)
    bpy.utils.register_class(ChestListItem)
    bpy.utils.register_class(LegListItem)
    bpy.utils.register_class(HandListItem)
    bpy.utils.register_class(FeetListItem)
    bpy.utils.register_class(TBSEKIT_BulkExport)
    
    bpy.types.Scene.tbse_kit_properties = PointerProperty(type=TBSEKIT_TBSEProperties)
    bpy.types.Scene.tbse_chest_toggles = PointerProperty(type=TBSEKIT_chestPiercingToggles)
    bpy.types.Scene.tbse_amab_toggles = PointerProperty(type=TBSEKIT_AMABPiercingToggles)
    
    # Gear lists
    bpy.types.Scene.chest_gear_list = CollectionProperty(type=ChestListItem)
    bpy.types.Scene.chest_gear_index = IntProperty(default=0, update=select_chest_gear)
    bpy.types.Scene.leg_gear_list = CollectionProperty(type=LegListItem)
    bpy.types.Scene.leg_gear_index = IntProperty(default=0, update=select_leg_gear)
    bpy.types.Scene.hand_gear_list = CollectionProperty(type=HandListItem)
    bpy.types.Scene.hand_gear_index = IntProperty(default=0, update=select_hand_gear)
    bpy.types.Scene.feet_gear_list = CollectionProperty(type=FeetListItem)
    bpy.types.Scene.feet_gear_index = IntProperty(default=0, update=select_feet_gear)
    
    bpy.types.Scene.tbse_bulk_export = PointerProperty(type=TBSEKIT_BulkExport)

def unregister():
    del bpy.types.Scene.tbse_bulk_export
    del bpy.types.Scene.feet_gear_index
    del bpy.types.Scene.feet_gear_list
    del bpy.types.Scene.hand_gear_index
    del bpy.types.Scene.hand_gear_list
    del bpy.types.Scene.leg_gear_index
    del bpy.types.Scene.leg_gear_list
    del bpy.types.Scene.chest_gear_index
    del bpy.types.Scene.chest_gear_list
    del bpy.types.Scene.tbse_amab_toggles
    del bpy.types.Scene.tbse_chest_toggles
    del bpy.types.Scene.tbse_kit_properties
    
    bpy.utils.unregister_class(TBSEKIT_BulkExport)
    bpy.utils.unregister_class(FeetListItem)
    bpy.utils.unregister_class(HandListItem)
    bpy.utils.unregister_class(LegListItem)
    bpy.utils.unregister_class(ChestListItem)
    bpy.utils.unregister_class(TBSEKIT_AMABPiercingToggles)
    bpy.utils.unregister_class(TBSEKIT_chestPiercingToggles)
    bpy.utils.unregister_class(TBSEKIT_TBSEProperties)
