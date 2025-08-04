# JSON helper functions for TBSE Body Kit addon.
import bpy
import json

def getTextBlock():
    # Retrieve the persistent text block as a dictionary.
    # The text block ".models" stores a JSON dictionary of all models in the .blend file
    try:
        rawTextBlock = bpy.data.texts.get(".models")
        if rawTextBlock:
            stringBlock = rawTextBlock.as_string()
            return json.loads(stringBlock)
        else:
            # Return empty dictionary if text block doesn't exist
            print("Warning: .models text block not found. Creating empty model dictionary.")
            return {}
    except (json.JSONDecodeError, AttributeError) as e:
        print(f"Warning: Could not parse .models text block as JSON: {e}")
        return {}

def setTextBlock(modelDict):
    # Set the persistent text block from a dictionary.
    # Converts the model dictionary to JSON and stores it in the ".models" text block
    try:
        rawTextBlock = bpy.data.texts.get(".models")
        if not rawTextBlock:
            # Create the text block if it doesn't exist
            rawTextBlock = bpy.data.texts.new(".models")
        
        toJSON = json.dumps(modelDict, indent=4)
        rawTextBlock.from_string(toJSON)
        return True
    except Exception as e:
        print(f"Warning: Could not save model dictionary to text block: {e}")
        return False

def getModelsInList(modelDict, key):
    # Get a list of model names from the dictionary by key.
    # Returns a list of model names (strings) from the specified ModelGroupKey
    try:
        if key in modelDict:
            modelList = list(modelDict[key].values())
            return modelList
        else:
            print(f"Warning: Model group key '{key}' not found in model dictionary.")
            return []
    except (TypeError, AttributeError) as e:
        print(f"Warning: Could not get models from list for key '{key}': {e}")
        return []

def getModelGroupKey(modelDict, obj):
    # Find ModelGroupKey from provided modelDict.
    # Searches through all model groups to find which one contains the specified object
    try:
        for modelGroup in modelDict:
            for modelKey in modelDict[modelGroup]:
                if obj == modelDict[modelGroup][modelKey]:
                    return modelGroup
        print(f"Warning: Object '{obj}' not found in model dictionary.")
        return None
    except (TypeError, AttributeError) as e:
        print(f"Warning: Could not find model group key for object '{obj}': {e}")
        return None

def getModelKey(modelDict, obj):
    # Find ModelKey from provided modelDict.
    # Searches through all model groups to find the specific key for the object
    try:
        for modelGroup in modelDict:
            for modelKey in modelDict[modelGroup]:
                if obj == modelDict[modelGroup][modelKey]:
                    return modelKey
        print(f"Warning: Object '{obj}' not found in model dictionary.")
        return None
    except (TypeError, AttributeError) as e:
        print(f"Warning: Could not find model key for object '{obj}': {e}")
        return None

def setModelName(modelDict, old, new):
    # Set model name within provided modelDict.
    # Changes the model name from 'old' to 'new' while preserving the dictionary structure
    try:
        modelGroupKey = getModelGroupKey(modelDict, old)
        modelKey = getModelKey(modelDict, old)
        
        if modelGroupKey and modelKey:
            modelDict[modelGroupKey][modelKey] = new
            return modelDict[modelGroupKey][modelKey]
        else:
            print(f"Warning: Could not find object '{old}' to rename to '{new}'.")
            return None
    except Exception as e:
        print(f"Warning: Could not rename model from '{old}' to '{new}': {e}")
        return None
