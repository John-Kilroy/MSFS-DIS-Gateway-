from pymxs import runtime as rt

from maxsdk_2024.globals import *
from maxsdk_2024.menu import * 

from . import WiperToolLoader as WT



def installMenu():

    createMacroScript(_func=WT.run, category=CATEGORY_MACRO, name="WiperMaskGenerator", button_text="Wiper Mask Generator")

    actionItem = rt.menuMan.createActionItem("WiperMaskGenerator", CATEGORY_MACRO)
    MSFS2024Menu = rt.menuman.findmenu(CATEGORY_MACRO)
    maxMenuBar = rt.menuMan.getMainMenuBar()

    MSFS2024Menu = getMenu(CATEGORY_MACRO)

    safeAddItem( MSFS2024Menu, actionItem)
    safeAddItem(maxMenuBar, rt.menuMan.createSubMenuItem(CATEGORY_MACRO, MSFS2024Menu))

    rt.menuMan.updateMenuBar()

try:
    installMenu()
    print("Loading WiperMaskGenerator2024")
except Exception as error: 
    print("WiperMaskGenerator2024 failed import because {}".format(error))