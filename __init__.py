# TBSE Body Kit Blender Addon initialization.
bl_info = {
    "name": "TBSE Body Kit",
    "author": "Crow, UsrBern",
    "description": "This is a refactored version of Crow's original scriptkid. Script to be used in conjunction with TBSE Upscale Kit. Includes multiple TBSE bodies.",
    "blender": (2, 80, 0),
    "version": (2, 0, 0),
    "location": "View3D > Sidebar > Body Kit",
    "category": "3D View"
}

import bpy
from . import properties
from . import operators
from . import panels
from . import lists
from . import json_helpers
from . import drivers
from . import constants
from . import utils
from . import setup_helpers
from . import gear_helpers

def register():
    # Register in dependency order: properties first, then UI components
    properties.register()
    lists.register()
    operators.register()
    panels.register()
    
    # json_helpers and drivers are utility modules, no registration needed

def unregister():
    # Unregister in reverse order
    panels.unregister()
    operators.unregister()
    lists.unregister()
    properties.unregister()

if __name__ == "__main__":
    register()
