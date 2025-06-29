from pymxs import runtime as rt
from maxsdk_2024.globals import *
from maxsdk_2024.menu import * 

from . import PBRviewport as  PBRviewport



def installMenu():
    createMacroScript(_func=PBRviewport.UseStudioIBL, category=CATEGORY_MACRO, name="SetStudioIBL")
    createMacroScript(_func=PBRviewport.UseExteriorIBL, category=CATEGORY_MACRO, name="SetExteriorIBL")
    createMacroScript(_func=PBRviewport.UseInteriorIBL, category=CATEGORY_MACRO, name="SetInteriorIBL")
    createMacroScript(_func=PBRviewport.UseLegacyShader, category=CATEGORY_MACRO, name="UseLegacyShader")

    actionItem0 = rt.menuMan.createActionItem("SetStudioIBL", CATEGORY_MACRO)
    actionItem1 = rt.menuMan.createActionItem("SetExteriorIBL", CATEGORY_MACRO)
    actionItem2 = rt.menuMan.createActionItem("SetInteriorIBL", CATEGORY_MACRO)
    actionItem3 = rt.menuMan.createActionItem("UseLegacyShader", CATEGORY_MACRO)

    generalLabelMenu = rt.menuman.findmenu("Views - General Viewport Label Menu")
    deleteItemByName(generalLabelMenu, "FlightSim IBL")
    
    flightSimIBLMenu = rt.menuman.findmenu("FlightSim IBL")
    if flightSimIBLMenu :
        rt.menuman.unRegisterMenu(flightSimIBLMenu)

    flightSimIBLMenu = rt.menuman.findmenu("MSFS2024_Material IBL")
    if flightSimIBLMenu :
        rt.menuman.unRegisterMenu(flightSimIBLMenu)
    
    MSFS2024IBLMenu = getMenu(IBL_MENU_NAME)
    MSFS2024IBLItem = rt.menuMan.createSubMenuItem(IBL_MENU_NAME, MSFS2024IBLMenu)

    safeAddItem(MSFS2024IBLMenu, actionItem0)
    safeAddItem(MSFS2024IBLMenu, actionItem1)
    safeAddItem(MSFS2024IBLMenu, actionItem2)
    safeAddItem(MSFS2024IBLMenu, actionItem3)
    safeAddItem(generalLabelMenu, MSFS2024IBLItem)

    PBRviewport.UseLegacyShader()

try:
    installMenu()
    print("Loaded PBRViewportManager2024")
except Exception as error: 
    print("PBRViewportManager2024 failed to install because {}".format(error))