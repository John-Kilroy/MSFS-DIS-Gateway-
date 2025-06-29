"""
Holds the constants used throughout the Texture Tool
"""
#TOOLS
PATH_FORBIDDEN_TEXTURE_NAMES = [
    'MSFS2024Material_Black.bmp', 
    'MSFS2024_Material_BRDFLUT.png', 
    'MSFS2024_Material_Flat.bmp', 
    'MSFS2024_Material_Grey.bmp', 
    'MSFS2024_Material_PBR_FullMetal.bmp',
    'MSFS2024Material_White.bmp',
    'Exterior_Irradiance.dds',
    'Exterior_Radiance.dds',
    'Interior_Irradiance.dds',
    'Interior_Radiance.dds',
    'Studio_Irradiance.dds',
    'Studio_Radiance.dds'
]

# OBJECT TEXTURE
PROP_TEXTURE_LIST = "MSFS2024_texture"
PROP_TEXTURE_GROUP_LIST = "MSFS2024_texture_group"
PROP_TEXTURE_ENTRY_PREFIX = "fs_texture_{}"
PROP_TEXTURE_GROUP_ENTRY_PREFIX = "fs_texture_group_{}"

# TEXTURE PARAM
PROP_TEXTURE_PARAM_NAME_ID = 0
PROP_TEXTURE_PARAM_PATH_ID = 1
PROP_TEXTURE_PARAM_GROUP_ID = 2
PROP_TEXTURE_PARAM_FORCENOALPHA_ID = 3
PROP_TEXTURE_PARAM_MATERIALBITMAP_ID = 4
PROP_TEXTURE_PARAM_OFFSET = 5

# TEXTURE GROUP PARAM
PROP_TEXTURE_GROUP_PARAM_NAME_ID = 0
PROP_TEXTURE_GROUP_PARAM_OFFSET = 1
