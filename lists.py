
import bpy
from bpy.types import UIList

class TBSEKIT_UL_chestGear(UIList):
    """UIList for chest gear items."""
    def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):
        pass

class TBSEKIT_UL_legGear(UIList):
    """UIList for leg gear items."""
    def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):
        pass

class TBSEKIT_UL_handGear(UIList):
    """UIList for hand gear items."""
    def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):
        pass

class TBSEKIT_UL_feetGear(UIList):
    """UIList for feet gear items."""
    def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):
        pass

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
