# Driver functions for TBSE Body Kit addon.
import bpy
from .json_helpers import getTextBlock, getModelsInList

def chest_resetDrivers():
    # Reset all chest shape keys back to TBSE (Basis).
    try:
        for key in bpy.data.shape_keys["Chest Master"].key_blocks:
            key.value = 0
    except KeyError:
        # Handle case where "Chest Master" shape keys don't exist
        print("Warning: Chest Master shape keys not found. Skipping chest shape reset.")
        return False
    return True

def chest_driver(self, context):
    # Driver logic for chest shape keys.
    tbse_properties = context.scene.tbse_kit_properties
    modelDict = getTextBlock()
    
    # Reset shape before changing to another shape
    chest_resetDrivers()
    index = 0
    
    if not tbse_properties.chest_shape == 'tbse':  # if not default tbse, change shape depending on shape enum value
        chest_type = tbse_properties.bl_rna.properties.get('chest_shape')
        index = chest_type.enum_items.find(tbse_properties.chest_shape)
        try:
            bpy.data.shape_keys["Chest Master"].key_blocks[index].value = 1
        except (KeyError, IndexError):
            # Handle case where shape keys don't exist or index is invalid
            print(f"Warning: Could not set chest shape key at index {index}. Shape keys may not exist or index is invalid.")
            return False
    
    # Chest model logic in case shape was changed to/from chonk or w
    from .toggles import chestToggle  # Import here to avoid circular imports
    chestToggle(self, context)

    # Create list of object names of all models with chest shapekeys
    modelList = getModelsInList(modelDict, "body_chest")
    modelList.extend(getModelsInList(modelDict, "gear_chest"))
    modelList.extend(getModelsInList(modelDict, "gear_hands"))

    # Change all objects with chest shapekeys to selected shape as active key
    chest_shape = tbse_properties.chest_shape
    for obj in modelList:
        if obj in bpy.data.objects:
            shp_index = index
            # If models are the elbows and wrists, change index to appropriate type
            if len(modelList) > 2 and (obj == modelList[1] or obj == modelList[2]):
                slim = ['slim', 'sbtl', 'sbtlslimmer']
                hunk = ['hunk', 'offhunk']
                if chest_shape in slim:
                    shp_index = 1
                elif chest_shape in hunk:
                    shp_index = 2
                elif chest_shape == 'xl':
                    shp_index = 3
                else:
                    shp_index = 0
            
            try:
                bpy.data.objects[obj].active_shape_key_index = shp_index
            except (AttributeError, IndexError):
                # Handle case where object doesn't have shape keys or index is invalid
                print(f"Warning: Could not set chest shape key index {shp_index} for object '{obj}'. Object may not have shape keys or index is invalid.")

def leg_resetDrivers():
    # Reset all leg shape keys back to TBSE (Basis).
    try:
        for key in bpy.data.shape_keys["Leg Master"].key_blocks:
            key.value = 0
    except KeyError:
        # Handle case where "Leg Master" shape keys don't exist
        print("Warning: Leg Master shape keys not found. Skipping leg shape reset.")
        return False
    return True

def leg_driver(self, context):
    # Driver logic for leg shape keys.
    tbse_properties = context.scene.tbse_kit_properties
    modelDict = getTextBlock()

    # Reset shape before changing to another shape
    leg_resetDrivers()
    index = 0
    
    if not tbse_properties.leg_shape == 'tbse':  # if not default tbse, change shape depending on shape enum value
        leg_type = tbse_properties.bl_rna.properties.get('leg_shape')
        index = leg_type.enum_items.find(tbse_properties.leg_shape)
        try:
            bpy.data.shape_keys["Leg Master"].key_blocks[index].value = 1
        except (KeyError, IndexError):
            # Handle case where shape keys don't exist or index is invalid
            print(f"Warning: Could not set leg shape key at index {index}. Shape keys may not exist or index is invalid.")
            return False
    
    # Leg model logic in case shape was changed to or from chonk
    from .toggles import legToggle  # Import here to avoid circular imports
    legToggle(self, context)

    # Create list of object names of all models with leg shapekeys
    modelList = getModelsInList(modelDict, "body_legs")
    modelList.extend(getModelsInList(modelDict, "gear_legs"))
    modelList.extend(getModelsInList(modelDict, "gear_feet"))

    # Change all objects with leg shapekeys to selected shape as active key
    leg_shape = tbse_properties.leg_shape
    for obj in modelList:
        if obj in bpy.data.objects:
            shp_index = index
            # If models are the shin and knee, change index to appropriate type
            if len(modelList) >= 2 and (obj == modelList[0] or obj == modelList[1]):
                hunk_stbl = ['hunk', 'sbtl']
                if leg_shape in hunk_stbl:
                    shp_index = 1
                elif leg_shape == 'xl':
                    shp_index = 2
                else:
                    shp_index = 0
            
            try:
                bpy.data.objects[obj].active_shape_key_index = shp_index
            except (AttributeError, IndexError):
                # Handle case where object doesn't have shape keys or index is invalid
                print(f"Warning: Could not set leg shape key index {shp_index} for object '{obj}'. Object may not have shape keys or index is invalid.")

def afab_ResetDrivers():
    # Reset all afab shape keys back to Gen A (Basis).
    try:
        for key in bpy.data.shape_keys["AFAB Master"].key_blocks:
            key.value = 0
    except KeyError:
        # Handle case where "AFAB Master" shape keys don't exist
        print("Warning: AFAB Master shape keys not found. Skipping AFAB shape reset.")
        return False
    return True

def afab_driver(self, context):
    # Driver logic for AFAB genital shape changes.
    tbse_properties = context.scene.tbse_kit_properties
    
    # Reset shape before changing to another shape
    afab_ResetDrivers()
    
    if not tbse_properties.afab_type == 'a':  # if not default Gen A, change shape depending on shape enum value
        afab_shape = tbse_properties.bl_rna.properties.get('afab_type')
        index = afab_shape.enum_items.find(tbse_properties.afab_type)
        try:
            bpy.data.shape_keys["AFAB Master"].key_blocks[index].value = 1
        except (KeyError, IndexError):
            # Handle case where shape keys don't exist or index is invalid
            print(f"Warning: Could not set AFAB shape key at index {index}. Shape keys may not exist or index is invalid.")
            return False
    return True

def amab_ResetDrivers():
    # Reset all amab shape keys back to Gen A (Basis).
    try:
        for key in bpy.data.shape_keys["AMAB Master"].key_blocks:
            key.value = 0
    except KeyError:
        # Handle case where "AMAB Master" shape keys don't exist
        print("Warning: AMAB Master shape keys not found. Skipping AMAB shape reset.")
        return False
    return True

def amab_driver(self, context):
    # Driver logic for AMAB genital shape changes.
    tbse_properties = context.scene.tbse_kit_properties

    # Reset shape before changing to another shape
    amab_ResetDrivers()

    if not tbse_properties.amab_type == 'a':  # if not default Gen A, change shape depending on shape enum value
        amab_shape = tbse_properties.bl_rna.properties.get('amab_type')
        index = amab_shape.enum_items.find(tbse_properties.amab_type)
        try:
            bpy.data.shape_keys["AMAB Master"].key_blocks[index].value = 1
        except (KeyError, IndexError):
            # Handle case where shape keys don't exist or index is invalid
            print(f"Warning: Could not set AMAB shape key at index {index}. Shape keys may not exist or index is invalid.")
            return False
    return True
