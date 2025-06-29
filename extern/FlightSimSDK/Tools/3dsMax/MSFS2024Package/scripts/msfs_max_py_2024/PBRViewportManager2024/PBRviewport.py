from pymxs import runtime as rt
import os
from maxsdk_2024.globals import *

scripts = (os.path.join(os.path.join(os.path.dirname(__file__),os.pardir),os.pardir))
MSFS2024_Material = os.path.abspath(os.path.join(os.path.join(scripts,"msfs_max_ms_2024"),"Material"))
IBLFOLDER = os.path.join(MSFS2024_Material, "IBLmap")


def SetIBLmaps(radianceMap, irradianceMap):
    multimats = filter(lambda m: rt.classOf(m) == rt.MultiMaterial, list(rt.sceneMaterials))
    MSFS2024Mats = filter(lambda m: rt.ClassOf(m) == rt.MSFS2024_Material, list(rt.sceneMaterials))
    if(MAXVERSION() >= MAX2021):
        multimats = list(multimats)
        MSFS2024Mats = list(MSFS2024Mats)
    for multi in multimats:
        for m in multi.materialList:
            if rt.ClassOf(m) == rt.MSFS2024_Material:
                MSFS2024Mats.append(m)
    for mat in MSFS2024Mats:
        mat.loadShader()
        mat.radianceMap = radianceMap
        mat.irradianceMap = irradianceMap
        # make use switching from legacy to PBR viewport set the right Tech



def UseStudioIBL():
    radianceMap = os.path.join(IBLFOLDER, "Studio_Radiance.dds")
    irradianceMap = os.path.join(IBLFOLDER, "Studio_Irradiance.dds")
    SetIBLmaps(radianceMap, irradianceMap)


def UseExteriorIBL():
    radianceMap = os.path.join(IBLFOLDER, "Exterior_Radiance.dds")
    irradianceMap = os.path.join(IBLFOLDER, "Exterior_Irradiance.dds")
    SetIBLmaps(radianceMap, irradianceMap)


def UseInteriorIBL():
    radianceMap = os.path.join(IBLFOLDER, "Interior_Radiance.dds")
    irradianceMap = os.path.join(IBLFOLDER, "Interior_Irradiance.dds")
    SetIBLmaps(radianceMap, irradianceMap)


def UseLegacyShader():
    multimats = list(filter(lambda m: rt.classOf(m) == rt.MultiMaterial, rt.sceneMaterials))
    MSFS2024Mats = list(filter(lambda m: rt.ClassOf(m) == rt.MSFS2024_Material, rt.sceneMaterials))
    for multi in multimats:
        for m in multi.materialList:
            if rt.ClassOf(m) == rt.MSFS2024_Material:
                MSFS2024Mats.append(m)
    for mat in MSFS2024Mats:
        mat.setShaderTechniqueByName("Tech_Legacy")


