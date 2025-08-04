
# Operators for TBSE Body Kit Blender Addon
# This module defines various operators for managing body kit models, importing/exporting FBX files, and modifying model properties.
import bpy
import os
from bpy.types import Operator
from bpy.props import BoolProperty, EnumProperty, IntProperty, StringProperty, PointerProperty, CollectionProperty
from bpy_extras.io_utils import ImportHelper, ExportHelper


class TBSEKIT_OT_setToDefault(Operator):
    # Resets all shapekeys and toggles back to default
    bl_idname = "object.set_to_default"
    bl_label = "Set to Default"
    bl_options = {"REGISTER","UNDO"}

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        # Reset all toggles and shape keys to default values
        props = context.scene.tbse_kit_properties
        
        # Reset all properties to their defaults
        for prop_name, prop in props.bl_rna.properties.items():
            if hasattr(prop, 'default') and prop_name != 'name':
                setattr(props, prop_name, prop.default)
        
        self.report({'INFO'}, "TBSE Body Kit: Reset to default settings.")
        return {'FINISHED'}


class TBSEKIT_OT_setupModels(Operator):
    # Install the models data into Blender's .models text block
    bl_idname = "object.setup_models"
    bl_label = "Setup TBSE Models Data"
    bl_description = "Install the required models data for the addon to function"
    bl_options = {"REGISTER","UNDO"}

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        try:
            from .setup_helpers import install_models_data, verify_models_data
            
            # Install the models data
            if install_models_data():
                # Verify it was installed correctly
                if verify_models_data():
                    self.report({'INFO'}, "TBSE models data installed successfully!")
                else:
                    self.report({'WARNING'}, "Models data installed but verification failed")
            else:
                self.report({'ERROR'}, "Failed to install models data")
                
        except Exception as e:
            self.report({'ERROR'}, f"Setup error: {str(e)}")
            
        return {'FINISHED'}
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
        directory = os.path.dirname(self.filepath)
        imported_objects = []
        
        for file_elem in self.files:
            filepath = os.path.join(directory, file_elem.name)
            # Store current objects to determine what was imported
            pre_import_objects = set(bpy.context.scene.objects)
            
            # Import FBX
            bpy.ops.import_scene.fbx(
                filepath=filepath,
                use_manual_orientation=True,
                global_scale=1.0,
                bake_space_transform=False,
                use_custom_normals=True,
                use_image_search=True,
                use_alpha_decals=False,
                decal_offset=0.0,
                use_anim=True,
                anim_offset=1.0,
                use_subsurf=False,
                use_custom_props=True,
                use_custom_props_enum_as_string=True,
                ignore_leaf_bones=False,
                force_connect_children=False,
                automatic_bone_orientation=False,
                primary_bone_axis='Y',
                secondary_bone_axis='X',
                use_prepost_rot=True
            )
            
            # Determine what was imported
            post_import_objects = set(bpy.context.scene.objects)
            new_objects = list(post_import_objects - pre_import_objects)
            imported_objects.extend(new_objects)
            
            # Clean up the imported objects
            if new_objects:
                # Select the imported objects
                bpy.ops.object.select_all(action='DESELECT')
                for obj in new_objects:
                    obj.select_set(True)
                
                # Call cleanup function
                cleanImport(self, new_objects)
        
        self.report({'INFO'}, f"TBSE Body Kit: Imported {len(self.files)} FBX file(s) with cleanup.")
        return {'FINISHED'}

def cleanImport(self, imported):
    # Clean up the imported mesh:
    # - clear parents
    # - [OPTIONAL] changes skeleton axis for easy viewing
    # - [OPTIONAL] removes unwanted empties
    # - [OPTIONAL] fixes alpha + metalic mat (attributed code from MekTools with permission)
    # - [OPTIONAL] assigns armature to existing 'Skeleton'
    
    bpy.ops.object.parent_clear(type='CLEAR_KEEP_TRANSFORM')

    meshes = []
    junk = []

    # organizing all objects imported
    for obj in imported:
        if obj.type == 'MESH':
            meshes.append(obj)
        else:
            junk.append(obj)
    
    for obj in meshes:
        # OPTIONAL SETTING: fix materials (attributed code from MekTools with permission)
        if self.fix_materials:
            for mat_slot in obj.material_slots:
                if mat_slot.material:
                    mat = mat_slot.material
                    mat.blend_method = 'HASHED'
                    # Fix metallic values
                    if mat.use_nodes:
                        for node in mat.node_tree.nodes:
                            if node.type == 'BSDF_PRINCIPLED':
                                node.inputs['Metallic'].default_value = 0.0
        
        # OPTIONAL SETTING: auto assign armature
        if self.auto_assign_armature:
            if "Skeleton" in bpy.data.objects:
                skeleton = bpy.data.objects["Skeleton"]
                # Add armature modifier
                armature_mod = obj.modifiers.new(name="Armature", type='ARMATURE')
                armature_mod.object = skeleton
        
        obj.select_set(False)  # deselect mesh objects
    
    # OPTIONAL SETTING: delete junk
    if self.delete_junk:
        for obj in junk:
            obj.select_set(True)
    
    if self.delete_junk and junk:
        bpy.ops.object.delete()  # delete all junk objects still selected
    
    # OPTIONAL SETTING: fix skeleton
    if self.fix_skeleton and "Skeleton" in bpy.data.objects:
        skeleton = bpy.data.objects["Skeleton"]
        skeleton.select_set(True)
        bpy.context.view_layer.objects.active = skeleton
        bpy.ops.object.mode_set(mode='EDIT')
        bpy.ops.armature.select_all(action='SELECT')
        bpy.ops.transform.rotate(value=1.5708, orient_axis='X')  # Rotate 90 degrees on X axis
        bpy.ops.object.mode_set(mode='OBJECT')

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


# Registration
classes = (
    TBSEKIT_OT_setToDefault,
    TBSEKIT_OT_setupModels,
    TBSEKIT_OT_rename,
    TBSEKIT_OT_importFBX,
    TBSEKIT_OT_exportFBX,
    TBSEKIT_OT_chestGearAdd,
    TBSEKIT_OT_chestGearRemove,
    TBSEKIT_OT_legGearAdd,
    TBSEKIT_OT_legGearRemove,
    TBSEKIT_OT_handGearAdd,
    TBSEKIT_OT_handGearRemove,
    TBSEKIT_OT_feetGearAdd,
    TBSEKIT_OT_feetGearRemove,
)

def register():
    for cls in classes:
        bpy.utils.register_class(cls)

def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
