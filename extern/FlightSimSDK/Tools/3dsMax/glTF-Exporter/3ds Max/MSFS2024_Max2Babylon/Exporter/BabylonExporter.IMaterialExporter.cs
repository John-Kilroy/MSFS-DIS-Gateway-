using Babylon2GLTF;

namespace MSFS2024_Max2Babylon
{
    public interface IBabylonMaterialExtensionExporter: IBabylonExtensionExporter
    {
        MaterialUtilities.ClassIDWrapper MaterialClassID { get; }
    }
}