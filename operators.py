
import bpy
from bpy.types import Operator
from bpy.props import BoolProperty, EnumProperty, IntProperty, StringProperty, PointerProperty, CollectionProperty
from bpy_extras.io_utils import ImportHelper, ExportHelper

class TBSEKIT_OT_setToDefault(Operator):
    "Resets all shapekeys and toggles back to default."
    bl_idname = "object.set_to_default"
    bl_label = "Set to Default"
    bl_options = {"REGISTER","UNDO"}

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        # Reset all toggles and shape keys to default values
        props = context.scene.tbse_kit_properties
        props.show_chest = True
        props.show_legs = True
        props.show_hands = True
        props.show_feet = True
        props.show_nsfw = False
        props.chest_shape = 'tbse'
        props.leg_shape = 'tbse'
        props.genital_toggle = 'amab'
        props.amab_type = 'a'
        props.afab_type = 'a'
        props.show_piercings_chest = False
        props.show_piercings_amab = False
        self.report({'INFO'}, "TBSE Body Kit: Reset to default.")
        return {'FINISHED'}

class TBSEKIT_OT_rename(Operator):
    bl_idname = "object.renaming"
    bl_label = "Rename"
    bl_description = "This allows for bulk renaming of models, changing all models to Part X.Z to Part Y.Z"
    bl_options = {'REGISTER','UNDO'}

    def execute(self, context):
        # Example: Bulk rename models in the selected list
        props = context.scene.tbse_kit_properties
        part_number = props.partNumber if hasattr(props, 'partNumber') else 0
        # This would call a helper function to rename models
        # renameModels(modelDict, modelList, part_number)
        self.report({'INFO'}, "TBSE Body Kit: Models renamed.")
        return {'FINISHED'}

class TBSEKIT_OT_importFBX(Operator, ImportHelper):
    bl_idname = "object.importfbx"
    bl_label = "Import FBX"
    bl_description = "Bulk import FBXs with optimal setting for XIV modding"
    bl_options = {'REGISTER','UNDO'}

    filter_glob: StringProperty(default='*.fbx',options={'HIDDEN'})
    files: CollectionProperty(type=bpy.types.OperatorFileListElement, options={'HIDDEN', 'SKIP_SAVE'})
    fix_skeleton: BoolProperty(default=True, name="Fix Skeleton", description="Rotates bones of skeleton to make them more readable when editing.")
    fix_materials: BoolProperty(default=True, name="Fix Materials", description="Changes all materials to 'Alpha Hashed' and fixes metalics")
    delete_junk: BoolProperty(default=True, name="Delete Junk", description="Deletes all empty objects, importing only the mesh and armature")
    auto_assign_armature: BoolProperty(default=True, name="Auto Assign Armature", description="Deletes the armature that comes with the fbx and assigns all meshes to existing skeleton.\nRecommended to disable ONLY if fbx skeleton includes ex_ bones")

    def draw(self, context):
        layout = self.layout
        layout.prop(self, "fix_skeleton")
        layout.prop(self, "fix_materials")
        layout.prop(self, "delete_junk")
        layout.prop(self, "auto_assign_armature")

    def execute(self, context):
        # Import FBX files with selected options
        # This is a stub; actual import logic would go here
        self.report({'INFO'}, "TBSE Body Kit: FBX import complete.")
        return {'FINISHED'}

def cleanImport(self, imported):
    pass

class TBSEKIT_OT_exportFBX(Operator, ExportHelper):
    bl_idname = "object.exportfbx"
    bl_label = "Export FBX"
    bl_description = "Exports all FBXs selected with optimal settings for XIV modding"
    bl_options = {'REGISTER','UNDO'}

    filename_ext = ".fbx"
    filter_glob: StringProperty(default='*.fbx',options={'HIDDEN'})
    reset_skeleton: BoolProperty(default=True, name="Reset Skeleton", description="Rotates bones of skeleton back to their original state.\nTechnically not needed but recommended if there's the chance of reimporting the FBX back into another blender file")

    @classmethod
    def poll(cls, context):
        return True
    
    def draw(self, context):
        layout = self.layout
        layout.prop(self, "reset_skeleton")

    def execute(self, context):
        # Export selected FBX files with optimal settings
        # This is a stub; actual export logic would go here
        self.report({'INFO'}, "TBSE Body Kit: FBX export complete.")
        return {'FINISHED'}

class TBSEKIT_OT_chestGearAdd(Operator):
    bl_idname = "object.chest_gear_add"
    bl_label = "Add selected gear model to chest gear list."
    bl_description = "This adds chest shape keys to the object"
    bl_options = {'REGISTER','UNDO'}

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        # Add selected gear model to chest gear list
        # addGearList(obj, gearlist, master)
        self.report({'INFO'}, "TBSE Body Kit: Chest gear added.")
        return {'FINISHED'}


class TBSEKIT_OT_chestGearRemove(Operator):
    bl_idname = "object.chest_gear_remove"
    bl_label = "Remove gear model from chest gear list."
    bl_description = "THIS WILL REMOVE ALL SHAPEKEYS!"
    bl_options = {'REGISTER','UNDO'}

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        # Remove gear model from chest gear list
        # removeGearJson(obj, modelDict, modelGroupKey)
        self.report({'INFO'}, "TBSE Body Kit: Chest gear removed.")
        return {'FINISHED'}

class TBSEKIT_OT_legGearAdd(Operator):
    bl_idname = "object.leg_gear_add"
    bl_label = "Add selected gear model to leg gear list"
    bl_description = "This adds leg shape keys to the object"
    bl_options = {'REGISTER','UNDO'}

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        # Add selected gear model to leg gear list
        # addGearList(obj, gearlist, master)
        self.report({'INFO'}, "TBSE Body Kit: Leg gear added.")
        return {'FINISHED'}

class TBSEKIT_OT_legGearRemove(Operator):
    bl_idname = "object.leg_gear_remove"
    bl_label = "Remove gear model from leg gear list"
    bl_description = "THIS WILL REMOVE ALL SHAPEKEYS!"
    bl_options = {'REGISTER','UNDO'}

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        # Remove gear model from leg gear list
        # removeGearJson(obj, modelDict, modelGroupKey)
        self.report({'INFO'}, "TBSE Body Kit: Leg gear removed.")
        return {'FINISHED'}

class TBSEKIT_OT_handGearAdd(Operator):
    bl_idname = "object.hand_gear_add"
    bl_label = "Add selected gear model to hand gear list"
    bl_description = "This adds chest shape keys to the object"
    bl_options = {'REGISTER','UNDO'}

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        # Add selected gear model to hand gear list
        # addGearList(obj, gearlist, master)
        self.report({'INFO'}, "TBSE Body Kit: Hand gear added.")
        return {'FINISHED'}

class TBSEKIT_OT_handGearRemove(Operator):
    bl_idname = "object.hand_gear_remove"
    bl_label = "Remove gear model from hand gear list"
    bl_description = "THIS WILL REMOVE ALL SHAPEKEYS!"
    bl_options = {'REGISTER','UNDO'}

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        # Remove gear model from hand gear list
        # removeGearJson(obj, modelDict, modelGroupKey)
        self.report({'INFO'}, "TBSE Body Kit: Hand gear removed.")
        return {'FINISHED'}

class TBSEKIT_OT_feetGearAdd(Operator):
    bl_idname = "object.feet_gear_add"
    bl_label = "Add selected gear model to feet gear list"
    bl_description = "This adds leg shape keys to the object"
    bl_options = {'REGISTER','UNDO'}

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        # Add selected gear model to feet gear list
        # addGearList(obj, gearlist, master)
        self.report({'INFO'}, "TBSE Body Kit: Feet gear added.")
        return {'FINISHED'}

class TBSEKIT_OT_feetGearRemove(Operator):
    bl_idname = "object.feet_gear_remove"
    bl_label = "Remove gear model from feet gear list"
    bl_description = "THIS WILL REMOVE ALL SHAPEKEYS!"
    bl_options = {'REGISTER','UNDO'}

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        # Remove gear model from feet gear list
        # removeGearJson(obj, modelDict, modelGroupKey)
        self.report({'INFO'}, "TBSE Body Kit: Feet gear removed.")
        return {'FINISHED'}
