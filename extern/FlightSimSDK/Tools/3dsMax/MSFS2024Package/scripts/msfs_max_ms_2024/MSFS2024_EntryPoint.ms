
MSFS2024PluginPath = getFilenamePath (getThisScriptFilename())

-- Order Matters !!!
filein (pathConfig.appendPath MSFS2024PluginPath @"MSFS2024_Material\MSFS2024_Material.ms")
filein (pathConfig.appendPath MSFS2024PluginPath @"MSFS2024_ProjectedDecal.ms")
filein (pathConfig.appendPath MSFS2024PluginPath @"MSFS2024_SphereColliderBoundingVolume.ms")
filein (pathConfig.appendPath MSFS2024PluginPath @"MSFS2024_SphereCollider.ms")
filein (pathConfig.appendPath MSFS2024PluginPath @"MSFS2024_BoxCollider.ms")
filein (pathConfig.appendPath MSFS2024PluginPath @"MSFS2024_SphereFade.ms")
filein (pathConfig.appendPath MSFS2024PluginPath @"MSFS2024_CylinderCollider.ms")
filein (pathConfig.appendPath MSFS2024PluginPath @"MSFS2024_Light.ms")
filein (pathConfig.appendPath MSFS2024PluginPath @"MSFS2024_BlobMeshize.ms")

MSFS2020_IS_PUBLIC_SDK = false
if (globalVars.isglobal #IS_PUBLIC_SDK and globalVars.get #IS_PUBLIC_SDK != undefined) then 
(
    MSFS2020_IS_PUBLIC_SDK = globalVars.get #IS_PUBLIC_SDK
)
    
if not MSFS2020_IS_PUBLIC_SDK then
(
    filein (pathConfig.appendPath MSFS2024PluginPath @"MSFS2020_Material\MSFS2020_Material.ms")
    filein (pathConfig.appendPath MSFS2024PluginPath @"MSFS2020_ProjectedDecal.ms")
    filein (pathConfig.appendPath MSFS2024PluginPath @"MSFS2020_SphereColliderBoundingVolume.ms")
    filein (pathConfig.appendPath MSFS2024PluginPath @"MSFS2020_SphereCollider.ms")
    filein (pathConfig.appendPath MSFS2024PluginPath @"MSFS2020_BoxCollider.ms")
    filein (pathConfig.appendPath MSFS2024PluginPath @"MSFS2020_SphereFade.ms")
    filein (pathConfig.appendPath MSFS2024PluginPath @"MSFS2020_CylinderCollider.ms")
    filein (pathConfig.appendPath MSFS2024PluginPath @"MSFS2020_Light.ms")
)

filein (pathConfig.appendPath MSFS2024PluginPath @"MSFS2024_Functions.ms")

filein (pathConfig.appendPath MSFS2024PluginPath @"MSFS2024_Callbacks.ms")

filein (pathConfig.appendPath MSFS2024PluginPath @"MSFS2024_Menu.ms")