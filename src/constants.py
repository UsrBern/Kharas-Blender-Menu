# Constants for TBSE Body Kit addon
# This module contains all constants, enums, and configuration values used throughout the addon
# Model group identifiers used in the JSON dictionary
MODEL_GROUPS = {
    'BODY_NECK': 'body_neck',
    'BODY_CHEST': 'body_chest',
    'BODY_CHEST_W': 'body_chest_w',
    'BODY_CHEST_CHONK': 'body_chest_chonk',
    'BODY_CHEST_CHONK1': 'body_chest_chonk1',
    'BODY_LEGS': 'body_legs',
    'BODY_LEGS_CHONK': 'body_legs_chonk',
    'BODY_HANDS': 'body_hands',
    'BODY_FEET': 'body_feet',
    'BODY_BPF': 'body_bpf',
    'BODY_GENITALS': 'body_genitals',
    'GEAR_CHEST': 'gear_chest',
    'GEAR_LEGS': 'gear_legs',
    'GEAR_HANDS': 'gear_hands',
    'GEAR_FEET': 'gear_feet',
    'PIERCINGS_CHEST': 'piercings_chest',
    'PIERCINGS_AMAB': 'piercings_amab',
    'GENITALS_AMAB': 'genitals_amab',
    'GENITALS_AFAB': 'genitals_afab',
    'GENITALS_BPF': 'genitals_bpf',
}

# Shape key master names
SHAPE_KEY_MASTERS = {
    'CHEST': 'Chest Master',
    'LEG': 'Leg Master',
    'AFAB': 'AFAB Master',
    'AMAB': 'AMAB Master',
}

# Shape categories for optimized processing
CHEST_SHAPE_CATEGORIES = {
    'SLIM': ['slim', 'sbtl', 'sbtlslimmer'],
    'HUNK': ['hunk', 'offhunk'],
    'CHONK': ['chonk', 'chonk1', 'cub'],
    'TYPE_W': ['w'],
    'XL': ['xl'],
}

LEG_SHAPE_CATEGORIES = {
    'HUNK_SBTL': ['hunk', 'sbtl'],
    'XL': ['xl'],
}

# Body part shapes that require specific model variants
SHAPE_SPECIFIC_MODELS = {
    'w': MODEL_GROUPS['BODY_CHEST_W'],
    'chonk': MODEL_GROUPS['BODY_CHEST_CHONK'],
    'chonk1': MODEL_GROUPS['BODY_CHEST_CHONK1'],
    'cub': MODEL_GROUPS['BODY_CHEST_CHONK1'],
}

# Gear list property names for dynamic access
GEAR_PROPERTIES = {
    'chest': 'show_chest_gear',
    'leg': 'show_leg_gear',
    'hand': 'show_hand_gear',
    'feet': 'show_feet_gear',
}

# Bone layer groups for organized bone management
BONE_LAYERS = {
    'BASE': ('show_base_bones', 0),
    'SKIRT': ('show_skirt_bones', 1),
    'EXTRA': ('show_extra_bones', 2),
    'TAIL': ('show_tail_bones', 3),
    'IVCS': ('show_ivcs_bones', 16),
    'IVCS2': ('show_ivcs2_bones', 17),
}

# NSFW model groups for organized access
NSFW_MODEL_GROUPS = [
    MODEL_GROUPS['GENITALS_AMAB'],
    MODEL_GROUPS['GENITALS_AFAB'], 
    MODEL_GROUPS['GENITALS_BPF'],
    MODEL_GROUPS['PIERCINGS_AMAB']
]

# Skeleton object constants
SKELETON_OBJECTS = {
    'OBJECT': 'Skeleton',
    'ARMATURE': 'Skeleton'
}

# Special model indices for complex logic
SPECIAL_INDICES = {
    'CHONK_NSFW_INDEX': 3,  # Index for chonk NSFW model in body_legs_chonk
    'AMAB_BUTT_INDEX': 0,   # Index for AMAB butt in body_genitals
    'AFAB_BUTT_INDEX': 1,   # Index for AFAB butt in body_genitals
    'BBWVR_INDEX': 0,       # Index for BBWVR AFAB model
    'BIBO_INDEX': 1,        # Index for Bibo AFAB model
}

# Error messages for consistent logging
ERROR_MESSAGES = {
    'SHAPE_KEY_NOT_FOUND': "Warning: {master} shape keys not found. Skipping {type} shape reset.",
    'SHAPE_KEY_INDEX_ERROR': "Warning: Could not set {type} shape key at index {index}. Shape keys may not exist or index is invalid.",
    'OBJECT_NOT_FOUND': "Warning: Object '{obj}' not found in scene.",
    'MODEL_DICT_ERROR': "Warning: Could not access model dictionary: {error}",
    'JSON_PARSE_ERROR': "Warning: Could not parse .models text block as JSON: {error}",
}
