from pymxs import runtime as rt

from maxsdk_2024.globals import *
from maxsdk_2024.menu import *

from TextureTool2024 import textureTool as TT

def installMenu():
    
    createMacroScriptQt(_module=TT, _widget=TT.MainWindow,_func=TT.MainWindow.run, category=CATEGORY_MACRO, name="TextureTool2024", button_text="Texture Tool")
    
    actionItem = rt.menuMan.createActionItem("TextureTool2024", CATEGORY_MACRO)

    maxMenuBar = rt.menuMan.getMainMenuBar()
    
    MSFS2024Menu = getMenu(CATEGORY_MACRO)
        
    safeAddItem(MSFS2024Menu, actionItem)
    safeAddItem(maxMenuBar, rt.menuMan.createSubMenuItem(CATEGORY_MACRO, MSFS2024Menu))
    
    rt.menuMan.updateMenuBar()
    
try:
    installMenu()
    print("Loaded TextureTool2024")
except Exception as error: 
    print("TextureTool2024 failed import because {}".format(error))