from pymxs import runtime as rt
from maxsdk_2024.globals import *
from maxsdk_2024.menu import *

from . import xml2jsonAnimationGroup as xml2json

# This tools is OBSOLETE (NOT USED ANYMORE)

def installMenu():
    createMacroScript(_func=xml2json.run, category=CATEGORY_MACRO, name="ConvertModelDefToJson2024", button_text="Legacy modeldef Converter")

    actionItem = rt.menuMan.createActionItem("ConvertModelDefToJson2024", CATEGORY_MACRO)

    MSFS2024Menu = getMenu(CATEGORY_MACRO)

    MSFS2024UtilitiesMenu = getMenu(UTILITIES_MENU_NAME)
    MSFS2024UtilitiesItem = rt.menuMan.createSubMenuItem(UTILITIES_MENU_NAME, MSFS2024UtilitiesMenu)

    MSFS2024SceneUtilitiesMenu = getMenu(SCENE_MENU_NAME)
    MSFS2024SceneUtilitiesItem = rt.menuMan.createSubMenuItem(SCENE_MENU_NAME, MSFS2024SceneUtilitiesMenu)
    
    safeAddItem(MSFS2024SceneUtilitiesMenu, actionItem)
    safeAddItem(MSFS2024UtilitiesMenu, MSFS2024SceneUtilitiesItem)
    safeAddItem(MSFS2024Menu, MSFS2024UtilitiesItem)

    rt.menuMan.updateMenuBar()
 
try:
    installMenu()
    print("Loaded ConvertModelDefToJson2024")
except Exception as error: 
    print("ConvertModelDefToJson2024 failed import because {}".format(error))