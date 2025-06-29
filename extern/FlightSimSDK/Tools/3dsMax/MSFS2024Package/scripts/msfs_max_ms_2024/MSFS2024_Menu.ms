

macroScript MSFS2024_MaterialsTools category:"MSFS2024" buttontext:"Materials Tools" tooltip:"Materials Tools" Icon:#("Material_Modifiers",2)
(
	filein (pathConfig.appendPath MSFS2024PluginPath @"MSFS2024_MaterialsTools.ms")
)

macroScript MSFS2024_ObjectRenamer category:"MSFS2024" buttontext:"Objects Renamer" tooltip:"Objects Renamer"
(
	filein	(pathConfig.appendPath MSFS2024PluginPath @"MSFS2024_ObjectRenamer.ms")
)

macroScript MSFS2024_CreateAnimationGroupFromSelection category:"MSFS2024" buttontext:"Create AnimationGroup From Selection" tooltip:"Create AnimationGroup From Selection"
(
    filein	(pathConfig.appendPath MSFS2024PluginPath @"Utilities\\MSFS2024_create_animation_group_from_selection.ms")
)

macroScript MSFS2024_EnvironmentLODsTools category:"MSFS2024" buttontext:"Environment LODs Tools" tooltip:"Generic utilities to generate LODs"
(
    filein	(pathConfig.appendPath MSFS2024PluginPath @"MSFS2024_EnvironmentLODsTools.ms")
)

macroScript MSFS2024_DisplayUvShellBorder category:"MSFS2024" buttontext:"Display Uv Shell Border" tooltip:"Display Uv Shell Border"
(
    filein	(pathConfig.appendPath MSFS2024PluginPath @"MSFS2024_DisplayUvShellBorder.ms")
)

macroScript MSFS2024_SceneConversion category:"MSFS2024" buttontext:"Convert your scene to MSFS2024" tooltip:"Convert your scene to be able to use MSFS2024 parameters"
(
    filein	(pathConfig.appendPath MSFS2024PluginPath @"MSFS2024_SceneConversion.ms")
)

fn MSFS2024Menu_hasItem maxMenu itemTitle = 
(
	for i = 1 to maxMenu.numItems() do (
		local item = maxMenu.getItem i
		if item.getTitle() == itemTitle then return i
	)
	return -1
)

fn MSFS2024Menu_safeAddItem maxMenu item =
(	
	local itemIndex = MSFS2024Menu_hasItem maxMenu (item.getTitle())
	maxMenu.addItem item itemIndex
)

fn MSFS2024Menu_getMenu menuName unregister:True =
(
	local menu = menuMan.findMenu menuName
	if menu == undefined then
	(
		return (menuMan.createMenu menuName)
	)
	else
	(
		if (unregister) then
		(
			menuMan.unRegisterMenu menu
			return (menuMan.createMenu menuName)
		) 
	)
	return menu
)

(
	MSFS2020_IS_PUBLIC_SDK = False
	if globalVars.isglobal #IS_PUBLIC_SDK then MSFS2020_IS_PUBLIC_SDK = globalVars.get #IS_PUBLIC_SDK
	if (MSFS2020_IS_PUBLIC_SDK == False) then
	(		
		-- Remove MSFS2020
		local FlightSimMenu = menuMan.findMenu "FlightSim"
		if FlightSimMenu != undefined then
		(
			menuMan.unRegisterMenu(FlightSimMenu)
		)

		-- Remove MSFS2020
		local MSFS2020Menu = menuMan.findMenu "MSFS2020"
		if MSFS2020Menu != undefined then
		(
			menuMan.unRegisterMenu(MSFS2020Menu)
		)
		
		local BabylonMenu = menuMan.findMenu "Babylon"
		if BabylonMenu != undefined then
		(		
			menuMan.unRegisterMenu(BabylonMenu)
		)

		local BabylonPropMenu = menuMan.findMenu "Babylon..."
		if BabylonPropMenu != undefined then
		(		
			menuMan.unRegisterMenu(BabylonPropMenu)
		)

		local babylonUtilitiesSubMenu = menuMan.findMenu "Babylon Utilities"
		if babylonUtilitiesSubMenu != undefined then
		(		
			menuMan.unRegisterMenu(babylonUtilitiesSubMenu)
		)

		-- Remove MSFS2020
		local MSFS2020PropMenu = menuMan.findMenu "MSFS2020..."
		if MSFS2020PropMenu != undefined then
		(
			menuMan.unRegisterMenu(MSFS2020PropMenu)
		)
	)

	local MSFS2024Menu = MSFS2024Menu_getMenu "MSFS2024"

	-- Create New Menus
	local MSFS2024UtilitiesMenu = MSFS2024Menu_getMenu "MSFS2024 Utilities"
	local MSFS2024UtilMenuItem = menuMan.createSubMenuItem "MSFS2024 Utilities" MSFS2024UtilitiesMenu
	
	local MSFS2024SceneUtilMenu = MSFS2024Menu_getMenu "Scene"
	local MSFS2024SceneUtilMenuItem = menuMan.createSubMenuItem "Scene" MSFS2024SceneUtilMenu

	local MSFS2024MaterialUtilMenu = MSFS2024Menu_getMenu "Materials"
	local MSFS2024MaterialUtilMenuItem = menuMan.createSubMenuItem "MSFS2024" MSFS2024MaterialUtilMenu
	
	local MSFS2024AnimationsUtilMenu = MSFS2024Menu_getMenu "Animations"
	local MSFS2024AnimationsUtilMenuItem = menuMan.createSubMenuItem "Animations" MSFS2024AnimationsUtilMenu

	/* SIMPLYGON */
	local MSFS2024simplygonUtilitiesMenu = MSFS2024Menu_getMenu "Simplygon Utilities"
	local MSFS2024simplygonUtilitiesItem = menuMan.createSubMenuItem "Simplygon Utilities" MSFS2024simplygonUtilitiesMenu

	local generateBlobMeshItem = menuMan.createActionItem "MSFS2024_BlobMeshize" "MSFS2024"
	MSFS2024Menu_safeAddItem MSFS2024simplygonUtilitiesMenu generateBlobMeshItem
	/* END SIMPLYGON */
	
	local createAnimationGroupFromSelItem = menuMan.createActionItem "MSFS2024_CreateAnimationGroupFromSelection" "MSFS2024"
	MSFS2024Menu_safeAddItem MSFS2024AnimationsUtilMenu createAnimationGroupFromSelItem

	local sceneConversionItem = menuMan.createActionItem "MSFS2024_SceneConversion" "MSFS2024"
	MSFS2024Menu_safeAddItem MSFS2024SceneUtilMenu sceneConversionItem
	
	local environmentLodsToolsItem = menuMan.createActionItem "MSFS2024_EnvironmentLODsTools" "MSFS2024"
	MSFS2024Menu_safeAddItem MSFS2024SceneUtilMenu environmentLodsToolsItem
	
	local displayUVItem = menuMan.createActionItem "MSFS2024_DisplayUvShellBorder" "MSFS2024"
	MSFS2024Menu_safeAddItem MSFS2024SceneUtilMenu displayUVItem
	
	local objectRenamerItem = menuMan.createActionItem "MSFS2024_ObjectRenamer" "MSFS2024"
	MSFS2024Menu_safeAddItem MSFS2024SceneUtilMenu objectRenamerItem
	
	local materialToolsItem = menuMan.createActionItem "MSFS2024_MaterialsTools" "MSFS2024"
	MSFS2024Menu_safeAddItem MSFS2024MaterialUtilMenu materialToolsItem

	MSFS2024Menu_safeAddItem MSFS2024UtilitiesMenu MSFS2024SceneUtilMenuItem
	MSFS2024Menu_safeAddItem MSFS2024UtilitiesMenu MSFS2024MaterialUtilMenuItem
	MSFS2024Menu_safeAddItem MSFS2024UtilitiesMenu MSFS2024AnimationsUtilMenuItem
	
	MSFS2024Menu_safeAddItem MSFS2024Menu MSFS2024UtilMenuItem
	MSFS2024Menu_safeAddItem MSFS2024Menu MSFS2024simplygonUtilitiesItem

	local mainMenu = menuMan.getMainMenuBar()
	mainMenu.addItem (menuMan.createSubMenuItem "MSFS2024" MSFS2024Menu) -1
	menuMan.updateMenuBar()

	global visibleMSFS2024Material = False
)
