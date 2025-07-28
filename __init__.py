
"""TBSE Body Kit Blender Addon initialization."""

import bpy
from . import properties
from . import operators
from . import panels
from . import lists
from . import json_helpers
from . import drivers

def register():
    properties.register()
    operators.register()
    panels.register()
    lists.register()
    json_helpers.register()
    drivers.register()

def unregister():
    drivers.unregister()
    json_helpers.unregister()
    lists.unregister()
    panels.unregister()
    operators.unregister()
    properties.unregister()
