from pymxs import runtime as rt

from maxsdk_2024.globals import *
from maxsdk_2024.menu import *

from MultiExporter2024 import multiExporter as ME


def installMenu():
    createMacroScriptQt(_module=ME, _widget=ME.MainWindow,_func=ME.MainWindow.run, category=CATEGORY_MACRO, name="MultiExporter2024", button_text="Multi Exporter")

    actionItem = rt.menuMan.createActionItem("MultiExporter2024", CATEGORY_MACRO)
    maxMenuBar = rt.menuMan.getMainMenuBar()

    MSFS2024Menu = getMenu(CATEGORY_MACRO)

    safeAddItem(MSFS2024Menu, actionItem)
    safeAddItem(maxMenuBar, rt.menuMan.createSubMenuItem(CATEGORY_MACRO, MSFS2024Menu))

    rt.menuMan.updateMenuBar()

try:
    installMenu()
    print("Loaded MultiExporter2024")
except Exception as error: 
    print("MultiExporter2024 failed import because {}".format(error))