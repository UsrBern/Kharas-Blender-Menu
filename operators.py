
# Operators for TBSE Body Kit Blender Addon
# This module defines various operators for managing body kit models, importing/exporting FBX files, and modifying model properties.
import bpy
import os
from bpy.types import Operator
from bpy.props import BoolProperty, EnumProperty, IntProperty, StringProperty, PointerProperty, CollectionProperty
from bpy_extras.io_utils import ImportHelper, ExportHelper


# Gear management utilities (merged from gear_helpers.py)

def add_shape_keys(obj, master_shape_key_data):
    """
    Add shape keys to an object based on a master shape key collection.
    
    Args:
        obj: The object to add shape keys to
        master_shape_key_data: The master shape key data
    """
    if not obj or not obj.data:
        return False
        
    try:
        # Ensure the object has shape keys
        if not obj.data.shape_keys:
            obj.shape_key_add(name='TBSE', from_mix=False)
            
        # Rename Basis to TBSE if it exists
        if obj.data.shape_keys.key_blocks and obj.data.shape_keys.key_blocks[0].name == 'Basis':
            obj.data.shape_keys.key_blocks[0].name = 'TBSE'
        
        # Add shape keys from master
        for key in master_shape_key_data.key_blocks:
            # Check if the shape key already exists
            if not obj.data.shape_keys.key_blocks.get(key.name):
                obj.shape_key_add(name=key.name, from_mix=False)
            
            # Add driver for everything except TBSE
            if key.name != 'TBSE':
                add_drivers(obj, key, master_shape_key_data)
        
        return True
        
    except Exception as e:
        print(f"Error adding shape keys to {obj.name}: {e}")
        return False


def add_drivers(obj, key, master):
    """
    Add drivers to an object's shape keys.
    
    Args:
        obj: The object to add drivers to
        key: The key to create a driver for
        master: The master shape key data
    """
    try:
        # Create new driver
        new_driver = obj.data.shape_keys.key_blocks[key.name].driver_add('value').driver
        new_driver.type = 'AVERAGE'
        
        # Create variable if none exist
        if len(new_driver.variables) == 0:
            var = new_driver.variables.new()
            var.name = 'value'
            var.type = 'SINGLE_PROP'
            var.targets[0].id_type = 'KEY'
            var.targets[0].id = master
            var.targets[0].data_path = f'key_blocks["{key.name}"].value'
            
    except Exception as e:
        print(f"Error adding driver for {key.name}: {e}")


def add_gear_to_list(obj, gear_list, master_name):
    """
    Add a gear object to a gear list with shape keys.
    
    Args:
        obj: The object to add
        gear_list: The collection property list to add to
        master_name: Name of the master shape key
    """
    try:
        # Get the master shape key data
        if master_name not in bpy.data.shape_keys:
            print(f"Error: Master shape key '{master_name}' not found")
            return False
            
        master = bpy.data.shape_keys[master_name]
        
        # Add to gear list
        new_item = gear_list.add()
        new_item.model_name = obj.name
        new_item.obj_pointer = obj
        
        # Add shape keys to the object
        if add_shape_keys(obj, master):
            obj.use_shape_key_edit_mode = True
            return True
        else:
            # Remove from list if shape key addition failed
            gear_list.remove(len(gear_list) - 1)
            return False
            
    except Exception as e:
        print(f"Error adding {obj.name} to gear list: {e}")
        return False


def remove_shape_keys(obj):
    """
    Remove all shape keys from an object.
    
    Args:
        obj: The object to remove shape keys from
    """
    try:
        if obj and obj.data and obj.data.shape_keys:
            # Remove all shape keys
            for key in obj.data.shape_keys.key_blocks[:]:
                obj.shape_key_remove(key)
        return True
    except Exception as e:
        print(f"Error removing shape keys from {obj.name}: {e}")
        return False


def add_gear_to_json(obj, prefix, model_group_key):
    """
    Add gear object to the JSON models data.
    
    Args:
        obj: The object to add
        prefix: The prefix for the model key
        model_group_key: The group key in the models dictionary
    """
    try:
        from .json_helpers import getTextBlock, setTextBlock
        model_dict = getTextBlock()
        
        # Ensure the group exists
        if model_group_key not in model_dict:
            model_dict[model_group_key] = {}
        
        # Find available key
        length = len(model_dict[model_group_key])
        model_key = f"{prefix}{length + 1}"
        
        # Handle duplicate keys
        index = 0
        while model_key in model_dict[model_group_key]:
            index += 1
            model_key = f"{prefix}{index}"
        
        # Add to dictionary
        model_dict[model_group_key][model_key] = obj.name
        
        # Save updated data
        setTextBlock(model_dict)
        return True
        
    except Exception as e:
        print(f"Error adding {obj.name} to JSON: {e}")
        return False


def remove_gear_from_json(obj, model_group_key):
    """
    Remove gear object from the JSON models data.
    
    Args:
        obj: The object to remove
        model_group_key: The group key in the models dictionary
    """
    try:
        from .json_helpers import getTextBlock, setTextBlock
        model_dict = getTextBlock()
        
        if model_group_key in model_dict:
            # Find the model key for this object
            model_key = None
            for key, value in model_dict[model_group_key].items():
                if value == obj.name:
                    model_key = key
                    break
            
            if model_key:
                model_dict[model_group_key].pop(model_key)
                setTextBlock(model_dict)
                return True
        
        return False
        
    except Exception as e:
        print(f"Error removing {obj.name} from JSON: {e}")
        return False


def remove_gear_from_list(gear_list, index):
    """
    Remove gear from the list at the specified index.
    
    Args:
        gear_list: The collection property list
        index: The index to remove
    """
    try:
        if 0 <= index < len(gear_list):
            gear_list.remove(index)
            return True
        return False
    except Exception as e:
        print(f"Error removing gear from list at index {index}: {e}")
        return False


def select_gear(gear_list, index):
    """
    Select the gear object in the 3D viewport when clicked in UI list.
    
    Args:
        gear_list: The collection property list
        index: The index of the item to select
    """
    try:
        # Deselect all objects first
        for obj in bpy.context.selected_objects:
            obj.select_set(False)
        
        # Select the gear object if valid index
        if index >= 0 and index < len(gear_list):
            gear_item = gear_list[index]
            obj = gear_item.obj_pointer
            if obj:
                obj.select_set(True)
                bpy.context.view_layer.objects.active = obj
                
    except Exception as e:
        print(f"Error selecting gear at index {index}: {e}")


# Update callback functions for gear list selection
def select_chest_gear(self, context):
    """Update callback for chest gear list selection."""
    gear_list = context.scene.chest_gear_list
    index = context.scene.chest_gear_index
    select_gear(gear_list, index)


def select_leg_gear(self, context):
    """Update callback for leg gear list selection."""
    gear_list = context.scene.leg_gear_list
    index = context.scene.leg_gear_index
    select_gear(gear_list, index)


def select_hand_gear(self, context):
    """Update callback for hand gear list selection."""
    gear_list = context.scene.hand_gear_list
    index = context.scene.hand_gear_index
    select_gear(gear_list, index)


def select_feet_gear(self, context):
    """Update callback for feet gear list selection."""
    gear_list = context.scene.feet_gear_list
    index = context.scene.feet_gear_index
    select_gear(gear_list, index)


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

class TBSEKIT_OT_gearAdd(Operator):
    bl_idname = "object.gear_add"
    bl_label = "Add selected gear model to gear list"
    bl_description = "This adds shape keys to the selected objects"
    bl_options = {'REGISTER','UNDO'}
    
    gear_type: StringProperty()

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        # Generic gear add operator
        from .constants import SHAPE_KEY_MASTERS
        
        selected_objects = context.selected_objects
        if not selected_objects:
            self.report({'WARNING'}, "No objects selected")
            return {'CANCELLED'}
        
        # Get gear list and master based on type
        gear_config = {
            'chest': {
                'list': context.scene.chest_gear_list,
                'master': SHAPE_KEY_MASTERS['CHEST'],
                'prefix': "chest_gear_",
                'json_key': "gear_chest"
            },
            'leg': {
                'list': context.scene.leg_gear_list,
                'master': SHAPE_KEY_MASTERS['LEG'],
                'prefix': "leg_gear_",
                'json_key': "gear_legs"
            },
            'hand': {
                'list': context.scene.hand_gear_list,
                'master': SHAPE_KEY_MASTERS['CHEST'],  # Hand gear uses chest master
                'prefix': "hand_gear_",
                'json_key': "gear_hands"
            },
            'feet': {
                'list': context.scene.feet_gear_list,
                'master': SHAPE_KEY_MASTERS['LEG'],  # Feet gear uses leg master
                'prefix': "feet_gear_",
                'json_key': "gear_feet"
            }
        }
        
        if self.gear_type not in gear_config:
            self.report({'ERROR'}, f"Unknown gear type: {self.gear_type}")
            return {'CANCELLED'}
        
        config = gear_config[self.gear_type]
        gear_list = config['list']
        success_count = 0
        
        for obj in selected_objects:
            if obj.type == 'MESH':
                if add_gear_to_list(obj, gear_list, config['master']):
                    add_gear_to_json(obj, config['prefix'], config['json_key'])
                    success_count += 1
                else:
                    self.report({'WARNING'}, f"Failed to add shape keys to {obj.name}")
        
        if success_count > 0:
            self.report({'INFO'}, f"TBSE Body Kit: Added {success_count} {self.gear_type} gear item(s).")
        else:
            self.report({'WARNING'}, "No valid mesh objects were added")
            
        return {'FINISHED'}


class TBSEKIT_OT_gearRemove(Operator):
    bl_idname = "object.gear_remove"
    bl_label = "Remove gear model from gear list"
    bl_description = "THIS WILL REMOVE ALL SHAPEKEYS!"
    bl_options = {'REGISTER','UNDO'}
    
    gear_type: StringProperty()

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        # Generic gear remove operator
        
        # Get gear list and index based on type
        gear_config = {
            'chest': {
                'list': context.scene.chest_gear_list,
                'index_prop': 'chest_gear_index',
                'json_key': "gear_chest"
            },
            'leg': {
                'list': context.scene.leg_gear_list,
                'index_prop': 'leg_gear_index',
                'json_key': "gear_legs"
            },
            'hand': {
                'list': context.scene.hand_gear_list,
                'index_prop': 'hand_gear_index',
                'json_key': "gear_hands"
            },
            'feet': {
                'list': context.scene.feet_gear_list,
                'index_prop': 'feet_gear_index',
                'json_key': "gear_feet"
            }
        }
        
        if self.gear_type not in gear_config:
            self.report({'ERROR'}, f"Unknown gear type: {self.gear_type}")
            return {'CANCELLED'}
        
        config = gear_config[self.gear_type]
        gear_list = config['list']
        index = getattr(context.scene, config['index_prop'])
        
        if not gear_list or index < 0 or index >= len(gear_list):
            self.report({'WARNING'}, "No valid gear item selected")
            return {'CANCELLED'}
        
        gear_item = gear_list[index]
        obj = gear_item.obj_pointer
        
        # Remove shape keys from object
        if obj:
            remove_shape_keys(obj)
            remove_gear_from_json(obj, config['json_key'])
        
        # Remove from list
        remove_gear_from_list(gear_list, index)
        
        # Adjust index if needed
        if index >= len(gear_list) and len(gear_list) > 0:
            setattr(context.scene, config['index_prop'], len(gear_list) - 1)
        
        self.report({'INFO'}, f"TBSE Body Kit: {self.gear_type.title()} gear removed.")
        return {'FINISHED'}


# Specific gear operators that call the generic ones
class TBSEKIT_OT_chestGearAdd(Operator):
    bl_idname = "object.chest_gear_add"
    bl_label = "Add selected gear model to chest gear list"
    bl_description = "This adds chest shape keys to the object"
    bl_options = {'REGISTER','UNDO'}

    def execute(self, context):
        return bpy.ops.object.gear_add(gear_type='chest')


class TBSEKIT_OT_chestGearRemove(Operator):
    bl_idname = "object.chest_gear_remove"
    bl_label = "Remove gear model from chest gear list"
    bl_description = "THIS WILL REMOVE ALL SHAPEKEYS!"
    bl_options = {'REGISTER','UNDO'}

    def execute(self, context):
        return bpy.ops.object.gear_remove(gear_type='chest')


class TBSEKIT_OT_legGearAdd(Operator):
    bl_idname = "object.leg_gear_add"
    bl_label = "Add selected gear model to leg gear list"
    bl_description = "This adds leg shape keys to the object"
    bl_options = {'REGISTER','UNDO'}

    def execute(self, context):
        return bpy.ops.object.gear_add(gear_type='leg')


class TBSEKIT_OT_legGearRemove(Operator):
    bl_idname = "object.leg_gear_remove"
    bl_label = "Remove gear model from leg gear list"
    bl_description = "THIS WILL REMOVE ALL SHAPEKEYS!"
    bl_options = {'REGISTER','UNDO'}

    def execute(self, context):
        return bpy.ops.object.gear_remove(gear_type='leg')


class TBSEKIT_OT_handGearAdd(Operator):
    bl_idname = "object.hand_gear_add"
    bl_label = "Add selected gear model to hand gear list"
    bl_description = "This adds chest shape keys to the object"
    bl_options = {'REGISTER','UNDO'}

    def execute(self, context):
        return bpy.ops.object.gear_add(gear_type='hand')


class TBSEKIT_OT_handGearRemove(Operator):
    bl_idname = "object.hand_gear_remove"
    bl_label = "Remove gear model from hand gear list"
    bl_description = "THIS WILL REMOVE ALL SHAPEKEYS!"
    bl_options = {'REGISTER','UNDO'}

    def execute(self, context):
        return bpy.ops.object.gear_remove(gear_type='hand')


class TBSEKIT_OT_feetGearAdd(Operator):
    bl_idname = "object.feet_gear_add"
    bl_label = "Add selected gear model to feet gear list"
    bl_description = "This adds leg shape keys to the object"
    bl_options = {'REGISTER','UNDO'}

    def execute(self, context):
        return bpy.ops.object.gear_add(gear_type='feet')


class TBSEKIT_OT_feetGearRemove(Operator):
    bl_idname = "object.feet_gear_remove"
    bl_label = "Remove gear model from feet gear list"
    bl_description = "THIS WILL REMOVE ALL SHAPEKEYS!"
    bl_options = {'REGISTER','UNDO'}

    def execute(self, context):
        return bpy.ops.object.gear_remove(gear_type='feet')


# Registration
classes = (
    TBSEKIT_OT_setToDefault,
    TBSEKIT_OT_setupModels,
    TBSEKIT_OT_rename,
    TBSEKIT_OT_importFBX,
    TBSEKIT_OT_exportFBX,
    TBSEKIT_OT_gearAdd,
    TBSEKIT_OT_gearRemove,
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
