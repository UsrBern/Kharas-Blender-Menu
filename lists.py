import bpy
from bpy.types import UIList

class TBSEKIT_UL_chestGear(UIList):
    # UIList for chest gear items.
    def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):
        
        if self.layout_type in {'DEFAULT','COMPACT'}:
            row = layout.row()
            row.prop(item, "model_name", text="", emboss=False)
            custom_icon = 'HIDE_ON'
            if item.isEnabled: custom_icon='HIDE_OFF'
            row.prop(item, "isEnabled", text="", icon=custom_icon)
            if not context.scene.tbse_kit_properties['show_chest_gear']: row.enabled = False
        elif self.layout_type in {'GRID'}:
            layout.alignment = 'CENTER'
            layout.label(text="")

class TBSEKIT_UL_legGear(UIList):
    # UIList for leg gear items.
    def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):
        
        if self.layout_type in {'DEFAULT','COMPACT'}:
            row = layout.row()
            row.prop(item, "model_name", text="", emboss=False)
            custom_icon = 'HIDE_ON'
            if item.isEnabled: custom_icon='HIDE_OFF'
            row.prop(item, "isEnabled", text="", icon=custom_icon)
            if not context.scene.tbse_kit_properties['show_leg_gear']: row.enabled = False
        elif self.layout_type in {'GRID'}:
            layout.alignment = 'CENTER'
            layout.label(text="")

class TBSEKIT_UL_handGear(UIList):
    # UIList for hand gear items.
    def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):
        
        if self.layout_type in {'DEFAULT','COMPACT'}:
            row = layout.row()
            row.prop(item, "model_name", text="", emboss=False)
            custom_icon = 'HIDE_ON'
            if item.isEnabled: custom_icon='HIDE_OFF'
            row.prop(item, "isEnabled", text="", icon=custom_icon)
            if not context.scene.tbse_kit_properties['show_hand_gear']: row.enabled = False
        elif self.layout_type in {'GRID'}:
            layout.alignment = 'CENTER'
            layout.label(text="")

class TBSEKIT_UL_feetGear(UIList):
    # UIList for feet gear items.
    def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):
        
        if self.layout_type in {'DEFAULT','COMPACT'}:
            row = layout.row()
            row.prop(item, "model_name", text="", emboss=False)
            custom_icon = 'HIDE_ON'
            if item.isEnabled: custom_icon='HIDE_OFF'
            row.prop(item, "isEnabled", text="", icon=custom_icon)
            if not context.scene.tbse_kit_properties['show_feet_gear']: row.enabled = False
        elif self.layout_type in {'GRID'}:
            layout.alignment = 'CENTER'
            layout.label(text="")

# Registration
classes = [
    TBSEKIT_UL_chestGear,
    TBSEKIT_UL_legGear,
    TBSEKIT_UL_handGear,
    TBSEKIT_UL_feetGear,
]

def register():
    for cls in classes:
        bpy.utils.register_class(cls)

def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
