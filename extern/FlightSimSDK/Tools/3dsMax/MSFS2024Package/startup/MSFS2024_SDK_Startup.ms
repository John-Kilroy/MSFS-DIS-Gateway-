MSFS2024PluginPath = systemTools.getEnvVariable "MSFS2024_SDK"

if MSFS2024PluginPath == undefined then
(
    MSFS2024PluginPath = pathConfig.appendPath (symbolicPaths.getPathValue(9)) "FlightSimTools"    
)
else
(
    MSFS2024PluginPath = MSFS2024PluginPath + "Tools\3dsMax\MSFS2024Package\scripts"
)

if ((getfiles (MSFS2024PluginPath+"\\*")).count == 0) then
(
    print("The Microsoft Flight Simulator SDK tools are not properly installed.\nPlease re-run the installer to fix the issue\n")
) 
else
(
    if ((maxversion())[1] >= 20000) then
    (
        try
        (
            global MSFS2024_IS_PUBLIC_SDK = true
            python.Init()
            sys = python.Import("sys")
            sys.path.append(MSFS2024PluginPath)
            python.Import("msfs_max_py_2024") -- importing the package trigger the installation of menu
        )
        catch
        (
            errorMessage = getCurrentException()
            messageBox ("Error opening msfs_max_py_2024.py:\n" + errorMessage) title:"MSFS2024" beep:true
        )
    )
    else
    (
        try
        (
            filein(pathConfig.appendPath MSFS2024PluginPath @"msfs_max_ms_2024\MSFS2024_EntryPoint.ms")
        )
        catch
        (
            errorMessage = getCurrentException()
            messageBox ("Error opening MSFS2024_EntryPoint.ms:\n" + errorMessage) title:"MSFS2024" beep:true
        )
    )
)  