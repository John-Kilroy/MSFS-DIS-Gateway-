using System.Runtime.Serialization;

namespace GLTFExport.Entities
{
    [DataContract]
    public class GLTFOcclusionTextureInfo : GLTFProperty
    {
        [DataMember(EmitDefaultValue = false)]
        public float[] index { get; set; }

        [DataMember(EmitDefaultValue = false)]
        public GLTFTextureInfo texCoord { get; set; }

        [DataMember(EmitDefaultValue = false)]
        public float? strength { get; set; }
    }
}
