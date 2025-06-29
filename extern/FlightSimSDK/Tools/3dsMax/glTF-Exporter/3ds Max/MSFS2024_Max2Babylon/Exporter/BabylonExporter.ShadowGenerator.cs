using System.Collections.Generic;
using Autodesk.Max;
using BabylonExport.Entities;

namespace MSFS2024_Max2Babylon
{
    public partial class BabylonExporter
    {
		//        private BabylonShadowGenerator ExportShadowGenerator(IINode lightNode, BabylonScene babylonScene)
		//        {
		//            ILightObject maxLight = (lightNode.ObjectRef as ILightObject);
		//            BabylonShadowGenerator babylonShadowGenerator = new BabylonShadowGenerator
		//            {
		//                lightId = lightNode.GetGuid().ToString(),
		//                mapSize = maxLight.GetMapSize(0, Tools.Forever),
		//                bias = lightNode.GetFloatProperty("babylonjs_shadows_bias", 0.00005f),
		//                forceBackFacesOnly = lightNode.GetBoolProperty("babylonjs_forcebackfaces")
		//            };

		//            logger?.RaiseMessage("Exporting shadow map", 2);

		//            string shadowsType = lightNode.GetStringProperty("babylonjs_shadows_type", "Blurred ESM");
		//            switch (shadowsType)
		//            {
		//                case "Hard shadows":
		//                    break;
		//                case "Poisson Sampling":
		//                    babylonShadowGenerator.usePoissonSampling = true;
		//                    break;
		//                case "ESM":
		//                    babylonShadowGenerator.useExponentialShadowMap = true;
		//                    break;
		//                case"Blurred ESM":
		//                    babylonShadowGenerator.useBlurExponentialShadowMap = true;
		//                    babylonShadowGenerator.blurScale = lightNode.GetFloatProperty("babylonjs_shadows_blurScale", 2);
		//                    babylonShadowGenerator.blurBoxOffset = lightNode.GetFloatProperty("babylonjs_shadows_blurBoxOffset", 1);
		//                    break;
		//            }

		//            List<string> list = new List<string>();
		//            bool inclusion = maxLight.ExclList.TestFlag(1); //NT_INCLUDE 
		//            bool checkExclusionList = maxLight.ExclList.TestFlag(4); //NT_AFFECT_SHADOWCAST 

		//            foreach (var meshNode in Loader.Core.RootNode.NodesListBySuperClass(SClass_ID.Geomobject))
		//            {
		//#if MAX2017 || MAX2018 || MAX2019 || MAX2020 || MAX2021 || MAX2022 || MAX2023 || MAX2024
		//                if (meshNode.CastShadows)
		//#else
		//                if (meshNode.CastShadows == 1)
		//#endif
		//                {
		//                    bool inList = maxLight.ExclList.FindNode(meshNode) != -1;
		//                    if (!checkExclusionList || (inList && inclusion) || (!inList && !inclusion))
		//                    {
		//                        list.Add(meshNode.GetGuid().ToString());
		//                    }
		//                }
		//            }
		//            babylonShadowGenerator.renderList = list.ToArray();
		//            babylonScene.ShadowGeneratorsList.Add(babylonShadowGenerator);
		//            return babylonShadowGenerator;
		//        }
	}
}
