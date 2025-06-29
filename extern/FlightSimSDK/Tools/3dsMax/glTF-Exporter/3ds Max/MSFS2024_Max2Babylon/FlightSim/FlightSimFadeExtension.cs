using System;
using System.Collections.Generic;
using System.Runtime.Serialization;
using Autodesk.Max;
using Babylon2GLTF;
using BabylonExport.Entities;
using GLTFExport.Entities;
using MSFS2024_Max2Babylon.FlightSim;

namespace MSFS2024_Max2Babylon.FlightSimExtension
{
	[DataContract]
	class GLTFExtensionAsoboFade : GLTFProperty
	{
		[DataMember(Name = "fade_objects")]
		public List<GLTFExtensionFade> fades { get; set; }
	}
	[DataContract]
	class GLTFExtensionFade : GLTFProperty
	{
		[DataMember(EmitDefaultValue = false, Name = "type", IsRequired = true)] public string Type { get; set; }
		[DataMember(EmitDefaultValue = false, Name = "translation")] public object Translation;
		[DataMember(Name = "params", IsRequired = true)] public object Params { get; set; }
	}

	[DataContract]
	class GLTFExtensionAsoboFadeSphereParams : GLTFProperty
	{
		[DataMember(EmitDefaultValue = false)] public float? radius;
	}


	class FlightSimFadeExtension : IBabylonExtensionExporter
	{
		readonly MaterialUtilities.ClassIDWrapper MSFS2020_SphereFadeClassID = new MaterialUtilities.ClassIDWrapper(0x794b56ca, 0x172623ba);
		readonly MaterialUtilities.ClassIDWrapper MSFS2024_SphereFadeClassID = new MaterialUtilities.ClassIDWrapper(0x69ac20f9, 0x533132d3);

		#region Implementation of IBabylonExtensionExporter

		public string GetGLTFExtensionName()
		{
			return "ASOBO_fade_object";
		}

		public ExtendedTypes GetExtendedType()
		{
			return new ExtendedTypes(typeof(GLTFMesh));
		}

		public bool IsMSFS2024SphereFade(IObject obj)
		{
			bool isMSFS2024SphereFade = new MaterialUtilities.ClassIDWrapper(obj.ClassID).Equals(MSFS2024_SphereFadeClassID);
			return isMSFS2024SphereFade;
		}

		public bool IsMSFS2020SphereFade(IObject obj)
		{
			bool isMSFS2020SphereFade = new MaterialUtilities.ClassIDWrapper(obj.ClassID).Equals(MSFS2020_SphereFadeClassID);
			return isMSFS2020SphereFade;
		}

		public bool ExportBabylonExtension<T>(T babylonObject, ref BabylonScene babylonScene, BabylonExporter exporter)
		{
			// just skip this extension is ment only for GLTF
			return false;
		}

		public object ExportGLTFExtension<T1, T2>(T1 babylonObject, ref T2 gltfObject, ref GLTF gltf, GLTFExporter exporter, ExtensionInfo extInfo)
		{
			var logger = exporter.logger;
			if (babylonObject is BabylonMesh babylonMesh)
			{
				GLTFExtensionAsoboFade fade = new GLTFExtensionAsoboFade();
				List<GLTFExtensionFade> fadeObjects = new List<GLTFExtensionFade>();
				fade.fades = fadeObjects;

				Guid.TryParse(babylonMesh.id, out Guid guid);
				IINode maxNode = Tools.GetINodeByGuid(guid);

				foreach (IINode node in maxNode.DirectChildren())
				{
					IObject obj = node.ObjectRef;
					if (IsMSFS2024SphereFade(obj))
					{
						GLTFExtensionFade fadeSphere = new GLTFExtensionFade();
						GLTFExtensionAsoboFadeSphereParams sphereParams = new GLTFExtensionAsoboFadeSphereParams();
						float radius = FlightSimExtensionUtility.GetGizmoParameterFloat(node, "SphereGizmo", "radius");
						fadeSphere.Translation = FlightSimExtensionUtility.GetTranslation(node, maxNode);
						sphereParams.radius = radius;
						fadeSphere.Type = "sphere";
						fadeSphere.Params = sphereParams;
						fadeObjects.Add(fadeSphere);
					}
					else if (IsMSFS2020SphereFade(obj))
					{
						string message = $"[GLTFExporter][ERROR] Object class of {node.Name} has been set up with MSFS2020 tools.";
						throw new System.Exception(message);
					}
				}

				if (fadeObjects.Count > 0)
				{
					return fade;
				}
			}
			return null;
		}
		#endregion

	}
}
