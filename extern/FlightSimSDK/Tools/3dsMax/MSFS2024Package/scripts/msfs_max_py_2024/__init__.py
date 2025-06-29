import importlib
import os

from pymxs import runtime as rt

from maxsdk_2024.globals import *

import sys
msfs_max_py_2024_path = os.path.dirname(__file__)
if msfs_max_py_2024_path not in sys.path:
    sys.path.append(msfs_max_py_2024_path)

pythonScriptFileName = os.path.dirname(__file__)

# start installing MSFS2024_Material material and legacy maxscript script
entryPointScriptFileName = os.path.dirname(pythonScriptFileName) + "\\msfs_max_ms_2024\\MSFS2024_EntryPoint.ms"
cmd = 'filein @"{0}"'.format(entryPointScriptFileName)
rt.execute(cmd)

MSFS2024_IS_PUBLIC_SDK = False
if rt.globalVars.isglobal("MSFS2024_IS_PUBLIC_SDK"):
    MSFS2024_IS_PUBLIC_SDK = rt.globalVars.get("MSFS2024_IS_PUBLIC_SDK")
    
if not MSFS2024_IS_PUBLIC_SDK:
    print("-----------Maxscripts Package installed-----------")
    if MAXVERSION() >= MAX2021:
        from configparser import ConfigParser
        configur = ConfigParser()
        configur.read(os.path.join(pythonScriptFileName,'internal_tools.ini'))
        internal_modules = []
        for k in configur["INTERNAL"]:
            internal_modules.append(configur["INTERNAL"].get(k).replace('"',''))
    else:
        from ConfigParser import RawConfigParser
        configur = RawConfigParser()
        configur.read(os.path.join(pythonScriptFileName,'internal_tools.ini'))
        internal_modules = [] 
        for (a,b) in configur.items("INTERNAL"):
            internal_modules.append((a,b)[1].replace('"',''))
  
if isMAX2019V3_SUP():
    ## Order of modules matters here !!!
    modules = [
        "PBRViewportManager2024",
        "TextureTool2024",
        "MultiExporter2024",
        "WiperTool2024"
    ]
    
    print ("-----------Installing public tools-----------")
    for module in modules:
        importlib.import_module(module)

    ## Import internal tools
    if not MSFS2024_IS_PUBLIC_SDK:
        print ("-----------Installing internal tools-----------")
        for module in internal_modules:
            if MAXVERSION() > MAX2019 and module == "AnimationTool2024" :
                # AnimationTools has too many dependencies with MaxPlus, skip it
                continue
            importlib.import_module(module)

print("-----------MSFS2024 Python Package installed-----------") 

