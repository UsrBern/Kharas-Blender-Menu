# Panel definitions for TBSE Body Kit addon
# This file contains all the UI panels for the addon, including main controls, body part toggles, shape options, gear lists, and advanced features.
import bpy
from bpy.types import Panel, Menu

class TBSEKIT_View3DPanel:
    # Parent class for all TBSE Body Kit panels.
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Body Kit'

class TBSEKIT_PT_mainPanel(TBSEKIT_View3DPanel, Panel):
    # Main panel for TBSE Body Kit addon.
    bl_idname = "TBSEKIT_PT_mainPanel"
    bl_label = "TBSE Body Kit"

    def draw(self, context):
        layout = self.layout
        layout.label(text="TBSE Body Kit Controls")

class TBSEKIT_PT_modelPanel(TBSEKIT_View3DPanel, Panel):
    # Panel for body part model toggles.
    bl_idname = "TBSEKIT_PT_modelPanel"
    bl_label = "Body Part Toggles"

    def draw(self, context):
        layout = self.layout
        layout.label(text="Body Part Toggles")

class TBSEKIT_PT_chestPanel(TBSEKIT_View3DPanel, Panel):
    # Panel for chest shape options.
    bl_idname = "TBSEKIT_PT_chestPanel"
    bl_label = "Chest Shape"

    def draw(self, context):
        layout = self.layout
        layout.label(text="Chest Shape Options")

class TBSEKIT_PT_legPanel(TBSEKIT_View3DPanel, Panel):
    # Panel for leg shape options.
    bl_idname = "TBSEKIT_PT_legPanel"
    bl_label = "Leg Shape"

    def draw(self, context):
        layout = self.layout
        layout.label(text="Leg Shape Options")

class TBSEKIT_PT_nsfwPanel(TBSEKIT_View3DPanel, Panel):
    # Panel for NSFW options.
    bl_idname = "TBSEKIT_PT_nsfwPanel"
    bl_label = "NSFW Options"

    def draw(self, context):
        layout = self.layout
        layout.label(text="NSFW Options")

class TBSEKIT_PT_piercingPanel(TBSEKIT_View3DPanel, Panel):
    # Panel for piercing model toggles.
    bl_idname = "TBSEKIT_PT_piercingPanel"
    bl_label = "Piercing Models"

    def draw(self, context):
        layout = self.layout
        layout.label(text="Piercing Model Options")

class TBSEKIT_PT_advancedPanel(TBSEKIT_View3DPanel, Panel):
    # Panel for advanced features (bone groups, etc).
    bl_idname = "TBSEKIT_PT_advancedPanel"
    bl_label = "Advanced Features"

    def draw(self, context):
        layout = self.layout
        layout.label(text="Advanced Features")

class TBSEKIT_PT_renamePanel(TBSEKIT_View3DPanel, Panel):
    # Panel for bulk renaming models.
    bl_idname = "TBSEKIT_PT_renamePanel"
    bl_label = "Bulk Rename"

    def draw(self, context):
        layout = self.layout
        layout.label(text="Bulk Rename Models")

class TBSEKIT_PT_gearToggle(TBSEKIT_View3DPanel, Panel):
    # Panel for gear model toggles.
    bl_idname = "TBSEKIT_PT_gearToggle"
    bl_label = "Gear Model Toggles"

    def draw(self, context):
        layout = self.layout
        layout.label(text="Gear Model Toggles")

class TBSEKIT_PT_chestGearList(TBSEKIT_View3DPanel, Panel):
    # Panel for chest gear list.
    bl_idname = "TBSEKIT_PT_chestGearList"
    bl_label = "Chest Gear List"

    def draw(self, context):
        layout = self.layout
        layout.label(text="Chest Gear List")

class TBSEKIT_PT_legGearList(TBSEKIT_View3DPanel, Panel):
    # Panel for leg gear list.
    bl_idname = "TBSEKIT_PT_legGearList"
    bl_label = "Leg Gear List"

    def draw(self, context):
        layout = self.layout
        layout.label(text="Leg Gear List")

class TBSEKIT_PT_handGearList(TBSEKIT_View3DPanel, Panel):
    # Panel for hand gear list.
    bl_idname = "TBSEKIT_PT_handGearList"
    bl_label = "Hand Gear List"

    def draw(self, context):
        layout = self.layout
        layout.label(text="Hand Gear List")

class TBSEKIT_PT_feetGearList(TBSEKIT_View3DPanel, Panel):
    # Panel for feet gear list.
    bl_idname = "TBSEKIT_PT_feetGearList"
    bl_label = "Feet Gear List"

    def draw(self, context):
        layout = self.layout
        layout.label(text="Feet Gear List")

class TBSEKIT_PT_boneGroups(TBSEKIT_View3DPanel, Panel):
    # Panel for bone group toggles.
    bl_idname = "TBSEKIT_PT_boneGroups"
    bl_label = "Bone Groups"

    def draw(self, context):
        layout = self.layout
        layout.label(text="Bone Groups")

class TBSEKIT_PT_testingPanel(TBSEKIT_View3DPanel, Panel):
    # Panel for testing purposes.
    bl_idname = "TBSEKIT_PT_testingPanel"
    bl_label = "Testing Panel"

    def draw(self, context):
        layout = self.layout
        layout.label(text="Testing Panel")

class TBSEKIT_MT_chestPiercingsMenu(TBSEKIT_View3DPanel, Menu):
    # Menu for chest piercings.
    bl_idname = "TBSEKIT_MT_chestPiercingsMenu"
    bl_label = "Chest Piercings Menu"

    def draw(self, context):
        layout = self.layout
        layout.label(text="Chest Piercings Menu")

class TBSEKIT_MT_amabPiercingsMenu(TBSEKIT_View3DPanel, Menu):
    # Menu for AMAB piercings.
    bl_idname = "TBSEKIT_MT_amabPiercingsMenu"
    bl_label = "AMAB Piercings Menu"

    def draw(self, context):
        layout = self.layout
        layout.label(text="AMAB Piercings Menu")

# Registration
classes = [
    TBSEKIT_PT_mainPanel,
    TBSEKIT_PT_modelPanel,
    TBSEKIT_PT_chestPanel,
    TBSEKIT_PT_legPanel,
    TBSEKIT_PT_nsfwPanel,
    TBSEKIT_PT_piercingPanel,
    TBSEKIT_PT_advancedPanel,
    TBSEKIT_PT_renamePanel,
    TBSEKIT_PT_gearToggle,
    TBSEKIT_PT_chestGearList,
    TBSEKIT_PT_legGearList,
    TBSEKIT_PT_handGearList,
    TBSEKIT_PT_feetGearList,
    TBSEKIT_PT_boneGroups,
    TBSEKIT_PT_testingPanel,
    TBSEKIT_MT_chestPiercingsMenu,
    TBSEKIT_MT_amabPiercingsMenu,
]

def register():
    for cls in classes:
        bpy.utils.register_class(cls)

def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
