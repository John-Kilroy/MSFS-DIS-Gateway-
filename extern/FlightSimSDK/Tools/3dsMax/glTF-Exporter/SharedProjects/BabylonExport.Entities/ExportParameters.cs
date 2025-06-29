using FlightSimExtension;

namespace BabylonExport.Entities
{
    public enum AnimationExportType
    {
        Export = 0,
        NotExport = 1,
        ExportOnly = 2
    }

    public class ExportParameters
    {
        public string outputPath; // The directory to store the generated files
        public string outputFormat;
        public string textureFolder = string.Empty;
        public float scaleFactor = 1.0f;
        public AnimationExportType animationExportType = AnimationExportType.Export;
        public bool enableASBUniqueID = true;
        public bool exportHiddenObjects = true;
        public bool exportMaterials = true;
        public bool exportOnlySelected = true;
        public bool exportAsSubmodel = false;
        public bool autoSaveSceneFile = false;
        public bool exportTangents = false;
        public bool exportSkins = true;
        public long txtQuality = 100;
        public bool mergeAOwithMR = false;
        public bool dracoCompression = false;
        public bool enableKHRLightsPunctual = false;
        public bool enableKHRTextureTransform = false;
        public bool enableKHRMaterialsUnlit = false;
        public bool pbrFull = false;
        public bool pbrNoLight = false;
        
        public bool keepInstances = true;
		public bool removeLodPrefix = true;
        public string srcTextureExtension;
        public string dstTextureExtension;
        public TangentSpaceConvention tangentSpaceConvention = TangentSpaceConvention.DirectX;

		public const string ModelFilePathProperty = "modelFilePathProperty";
		public const string TextureFolderPathProperty = "textureFolderPathProperty";

        public const string PBRFullPropertyName = "babylonjs_pbr_full";
        public const string PBRNoLightPropertyName = "babylonjs_pbr_nolight";
        public const string PBREnvironmentPathPropertyName = "babylonjs_pbr_environmentPathProperty";

        #region Morph
        public bool rebuildMorphTarget = true;
        public bool exportMorphTangents = false;
        public bool exportMorphNormals = true;
        public bool exportTargetColors = true;
        public bool exportTargetUVs = true;
        #endregion
    }
}
