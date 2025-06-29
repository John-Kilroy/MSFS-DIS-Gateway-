using Autodesk.Max;
using Babylon2GLTF;
using BabylonExport.Entities;
using GLTFExport.Entities;
using System;
using System.Runtime.Serialization;

namespace MSFS2024_Max2Babylon.FlightSimExtension
{

	[DataContract]
	class GLTFExtensionAsoboStreetLight : GLTFProperty
	{
		[DataMember(Name = "color", IsRequired = true)] public float[] color { get; set; }
		[DataMember(Name = "intensity", IsRequired = true)] public float intensity { get; set; }
		[DataMember(Name = "day_night_cycle", IsRequired = true)] public bool dayNightCycle { get; set; }
		[DataMember(Name = "cone_angle", IsRequired = true)] public float coneAngle { get; set; }
		[DataMember(Name = "has_symmetry", IsRequired = true)] public bool hasSymmetry { get; set; }
		[DataMember(Name = "flash_frequency", IsRequired = true)] public float flashFrequency { get; set; }
		[DataMember(Name = "flash_duration", IsRequired = true)] public float flashDuration { get; set; }
		[DataMember(Name = "flash_phase", IsRequired = true)] public float flashPhase { get; set; }
		[DataMember(Name = "rotation_speed", IsRequired = true)] public float rotationSpeed { get; set; }
		[DataMember(Name = "rotation_phase", IsRequired = true)] public float rotationPhase { get; set; }
		[DataMember(Name = "random_phase", IsRequired = true)] public bool randomPhase { get; set; }
	}


	class FlightSimLightExtension : IBabylonExtensionExporter
	{
		readonly MaterialUtilities.ClassIDWrapper MSFS2024_StreetLightClassID = new MaterialUtilities.ClassIDWrapper(0x204167e8, 0x552ef992);
		readonly MaterialUtilities.ClassIDWrapper MSFS2020_LightClassID = new MaterialUtilities.ClassIDWrapper(0x18a3b84e, 0x63ec33ad);

		#region Implementation of IBabylonExtensionExporter

		public string GetGLTFExtensionName()
		{
			return "ASOBO_street_light";
		}

		public ExtendedTypes GetExtendedType()
		{
			return new ExtendedTypes(typeof(GLTFNode));
		}

		public bool IsMSFS2024StreetLight(IObject obj)
		{
			bool isMSFS2024StreetLight = new MaterialUtilities.ClassIDWrapper(obj.ClassID).Equals(MSFS2024_StreetLightClassID);
			return isMSFS2024StreetLight;
		}

		public bool IsMSFS2020Light(IObject obj)
		{
			bool isMSFS2020Light = new MaterialUtilities.ClassIDWrapper(obj.ClassID).Equals(MSFS2020_LightClassID);
			return isMSFS2020Light;
		}

		public bool ExportBabylonExtension<T>(T babylonObject, ref BabylonScene babylonScene, BabylonExporter exporter)
		{
			// just skip this extension is ment only for GLTF
			return false;
		}

		public object ExportGLTFExtension<T1, T2>(T1 babylonObject, ref T2 gltfObject, ref GLTF gltf, GLTFExporter exporter, ExtensionInfo extInfo)
		{
			var logger = exporter.logger;
			if (babylonObject is BabylonNode babylonLight)
			{
				Guid.TryParse(babylonLight.id, out Guid guid);
				IINode maxNode = Tools.GetINodeByGuid(guid);
				if (maxNode != null)
				{
					IObject obj = maxNode.ObjectRef;
					if (IsMSFS2024StreetLight(obj))
					{
						GLTFExtensionAsoboStreetLight streetLightExt = new GLTFExtensionAsoboStreetLight();
						streetLightExt.color = GetColor(maxNode);
						streetLightExt.intensity = GetIntensity(maxNode);
						streetLightExt.dayNightCycle = GetDayNightCycle(maxNode);
						streetLightExt.coneAngle = GetConeAngle(maxNode);
						streetLightExt.hasSymmetry = GetHasSymmetry(maxNode);
						streetLightExt.flashFrequency = GetFlashFrequency(maxNode);
						streetLightExt.flashDuration = GetFlashDuration(maxNode);
						streetLightExt.flashPhase = GetFlashPhase(maxNode);
						streetLightExt.rotationSpeed = GetRotationSpeed(maxNode);
						streetLightExt.rotationPhase = GetRotationPhase(maxNode);
						streetLightExt.randomPhase = GetRandomPhase(maxNode);
						return streetLightExt;
					}
					else if (IsMSFS2020Light(obj))
					{
						string message = $"[GLTFExporter][ERROR][Lights] Object class of {maxNode.Name} has been set up with MSFS2020 tools.";
						throw new System.Exception(message);
					}
				}
			}
			return null;
		}

		#region Parameters
		private float[] GetColor(IINode node)
		{
			string mxs = String.Empty;
			mxs = $"(maxOps.getNodeByHandle {node.Handle}).Color";

			IFPValue mxsRetVal = Loader.Global.FPValue.Create();
			ScriptsUtilities.ExecuteMAXScriptScript(mxs, true, mxsRetVal);
			var r = mxsRetVal.Clr.ToArray();

			return r;
		}


		private float GetIntensity(IINode node)
		{
			string mxs = String.Empty;
			mxs = $"(maxOps.getNodeByHandle {node.Handle}).delegate.Intensity";

			IFPValue mxsRetVal = Loader.Global.FPValue.Create();
			ScriptsUtilities.ExecuteMAXScriptScript(mxs, true, mxsRetVal);
			var r = mxsRetVal.F;
			return r;
		}

		private float GetConeAngle(IINode node)
		{
			string mxs = String.Empty;
			mxs = $"(maxOps.getNodeByHandle {node.Handle}).ConeAngle";

			IFPValue mxsRetVal = Loader.Global.FPValue.Create();
			ScriptsUtilities.ExecuteMAXScriptScript(mxs, true, mxsRetVal);
			var r = mxsRetVal.F;
			return r;
		}

		private bool GetHasSymmetry(IINode node)
		{
			string mxs = String.Empty;
			mxs = $"(maxOps.getNodeByHandle {node.Handle}).HasSimmetry";

			IFPValue mxsRetVal = Loader.Global.FPValue.Create();
			ScriptsUtilities.ExecuteMAXScriptScript(mxs, true, mxsRetVal);
			var r = mxsRetVal.B;
			return r;
		}

		private float GetFlashFrequency(IINode node)
		{
			string mxs = String.Empty;
			mxs = $"(maxOps.getNodeByHandle {node.Handle}).FlashFrequency";

			IFPValue mxsRetVal = Loader.Global.FPValue.Create();
			ScriptsUtilities.ExecuteMAXScriptScript(mxs, true, mxsRetVal);
			var r = mxsRetVal.F;
			return r;
		}

		private float GetFlashDuration(IINode node)
		{
			string mxs = String.Empty;
			mxs = $"(maxOps.getNodeByHandle {node.Handle}).FlashDuration";

			IFPValue mxsRetVal = Loader.Global.FPValue.Create();
			ScriptsUtilities.ExecuteMAXScriptScript(mxs, true, mxsRetVal);
			var r = mxsRetVal.F;
			return r;
		}

		private float GetRotationSpeed(IINode node)
		{
			string mxs = String.Empty;
			mxs = $"(maxOps.getNodeByHandle {node.Handle}).RotationSpeed";

			IFPValue mxsRetVal = Loader.Global.FPValue.Create();
			ScriptsUtilities.ExecuteMAXScriptScript(mxs, true, mxsRetVal);
			var r = mxsRetVal.F;
			return r;
		}

		private float GetRotationPhase(IINode node)
		{
			string mxs = String.Empty;
			mxs = $"(maxOps.getNodeByHandle {node.Handle}).RotationPhase";

			IFPValue mxsRetVal = Loader.Global.FPValue.Create();
			ScriptsUtilities.ExecuteMAXScriptScript(mxs, true, mxsRetVal);
			var r = mxsRetVal.F;
			return r;
		}

		private bool GetRandomPhase(IINode node)
		{
			string mxs = String.Empty;
			mxs = $"(maxOps.getNodeByHandle {node.Handle}).RandomPhase";

			IFPValue mxsRetVal = Loader.Global.FPValue.Create();
			ScriptsUtilities.ExecuteMAXScriptScript(mxs, true, mxsRetVal);
			var r = mxsRetVal.B;
			return r;
		}


		private float GetFlashPhase(IINode node)
		{
			string mxs = String.Empty;
			mxs = $"(maxOps.getNodeByHandle {node.Handle}).FlashPhase";

			IFPValue mxsRetVal = Loader.Global.FPValue.Create();
			ScriptsUtilities.ExecuteMAXScriptScript(mxs, true, mxsRetVal);
			var r = mxsRetVal.F;
			return r;
		}


		private bool GetDayNightCycle(IINode node)
		{
			string mxs = String.Empty;
			mxs = $"(maxOps.getNodeByHandle {node.Handle}).ActivationMode";

			IFPValue mxsRetVal = Loader.Global.FPValue.Create();
			ScriptsUtilities.ExecuteMAXScriptScript(mxs, true, mxsRetVal);
			bool r = mxsRetVal.I == 1;
			return r;
		}
		#endregion

		#endregion

	}

	[DataContract]
	class GLTFExtensionAsoboAdvancedLight : GLTFProperty
	{
		[DataMember(Name = "color", IsRequired = true)] public float[] color { get; set; }
		[DataMember(Name = "intensity", IsRequired = true)] public float intensity { get; set; }
		[DataMember(Name = "shape_type", IsRequired = true)] public int shapeType { get; set; }
		[DataMember(Name = "source_radius", IsRequired = true)] public float sourceRadius { get; set; }
		[DataMember(Name = "inner_cone_angle", IsRequired = true)] public float innerConeAngle { get; set; }
		[DataMember(Name = "outer_cone_angle", IsRequired = true)] public float outerConeAngle { get; set; }
		[DataMember(Name = "channel_exterior", IsRequired = true)] public bool channelExterior { get; set; }
		[DataMember(Name = "channel_interior", IsRequired = true)] public bool channelInterior { get; set; }
	}


	class FlightSimAdvancedLightExtension : IBabylonExtensionExporter
	{
		readonly MaterialUtilities.ClassIDWrapper MSFS2024_FlightSimAdvancedLightClassID = new MaterialUtilities.ClassIDWrapper(0xb0c612d, 0x143591cf);

		#region Implementation of IBabylonExtensionExporter

		public string GetGLTFExtensionName()
		{
			return "ASOBO_advanced_light";
		}

		public ExtendedTypes GetExtendedType()
		{
			return new ExtendedTypes(typeof(GLTFNode));
		}

		public bool IsMSFS2024AdvancedLight(IObject obj)
		{
			bool isMSFS2024FlightSimAdvancedLight = new MaterialUtilities.ClassIDWrapper(obj.ClassID).Equals(MSFS2024_FlightSimAdvancedLightClassID);
			return isMSFS2024FlightSimAdvancedLight;
		}

		public bool ExportBabylonExtension<T>(T babylonObject, ref BabylonScene babylonScene, BabylonExporter exporter)
		{
			// just skip this extension is ment only for GLTF
			return false;
		}

		public object ExportGLTFExtension<T1, T2>(T1 babylonObject, ref T2 gltfObject, ref GLTF gltf, GLTFExporter exporter, ExtensionInfo extInfo)
		{
			if (babylonObject is BabylonNode babylonLight)
			{
				GLTFExtensionAsoboAdvancedLight lightExt = new GLTFExtensionAsoboAdvancedLight();

				Guid.TryParse(babylonLight.id, out Guid guid);
				IINode maxNode = Tools.GetINodeByGuid(guid);
				if (maxNode != null)
				{
					IObject obj = maxNode.ObjectRef;
					if (IsMSFS2024AdvancedLight(obj))
					{
						lightExt.color = GetColor(maxNode);
						lightExt.intensity = GetIntensity(maxNode);
						lightExt.shapeType = GetShapeType(maxNode);
						lightExt.sourceRadius = GetSourceRadius(maxNode);
						lightExt.innerConeAngle = GetInnerConeAngle(maxNode);
						lightExt.outerConeAngle = GetOuterConeAngle(maxNode);
						lightExt.channelExterior = GetChannelExterior(maxNode);
						lightExt.channelInterior = GetChannelInterior(maxNode);
						return lightExt;
					}
				}
			}
			return null;
		}

		#region Parameters
		private float[] GetColor(IINode node)
		{
			string mxs = String.Empty;
			mxs = $"(maxOps.getNodeByHandle {node.Handle}).Color";

			IFPValue mxsRetVal = Loader.Global.FPValue.Create();
			ScriptsUtilities.ExecuteMAXScriptScript(mxs, true, mxsRetVal);
			return mxsRetVal.Clr.ToArray();
		}


		private float GetIntensity(IINode node)
		{
			string mxs = String.Empty;
			mxs = $"(maxOps.getNodeByHandle {node.Handle}).delegate.Intensity";

			IFPValue mxsRetVal = Loader.Global.FPValue.Create();
			ScriptsUtilities.ExecuteMAXScriptScript(mxs, true, mxsRetVal);
			return mxsRetVal.F;
		}

		private int GetShapeType(IINode node)
		{
			string mxs = String.Empty;
			mxs = $"(maxOps.getNodeByHandle {node.Handle}).ShapeType";

			IFPValue mxsRetVal = Loader.Global.FPValue.Create();
			ScriptsUtilities.ExecuteMAXScriptScript(mxs, true, mxsRetVal);
			return mxsRetVal.I;
		}

		private float GetSourceRadius(IINode node)
		{
			string mxs = String.Empty;
			mxs = $"(maxOps.getNodeByHandle {node.Handle}).SourceRadius";

			IFPValue mxsRetVal = Loader.Global.FPValue.Create();
			ScriptsUtilities.ExecuteMAXScriptScript(mxs, true, mxsRetVal);
			return mxsRetVal.F;
		}

		private float GetInnerConeAngle(IINode node)
		{
			string mxs = String.Empty;
			mxs = $"(maxOps.getNodeByHandle {node.Handle}).InnerConeAngle";

			IFPValue mxsRetVal = Loader.Global.FPValue.Create();
			ScriptsUtilities.ExecuteMAXScriptScript(mxs, true, mxsRetVal);
			return mxsRetVal.F;
		}

		private float GetOuterConeAngle(IINode node)
		{
			string mxs = String.Empty;
			mxs = $"(maxOps.getNodeByHandle {node.Handle}).OuterConeAngle";

			IFPValue mxsRetVal = Loader.Global.FPValue.Create();
			ScriptsUtilities.ExecuteMAXScriptScript(mxs, true, mxsRetVal);
			return mxsRetVal.F;
		}

		private bool GetChannelExterior(IINode node)
		{
			string mxs = String.Empty;
			mxs = $"(maxOps.getNodeByHandle {node.Handle}).ChannelExterior";

			IFPValue mxsRetVal = Loader.Global.FPValue.Create();
			ScriptsUtilities.ExecuteMAXScriptScript(mxs, true, mxsRetVal);
			return mxsRetVal.B;
		}
		private bool GetChannelInterior(IINode node)
		{
			string mxs = String.Empty;
			mxs = $"(maxOps.getNodeByHandle {node.Handle}).ChannelInterior";

			IFPValue mxsRetVal = Loader.Global.FPValue.Create();
			ScriptsUtilities.ExecuteMAXScriptScript(mxs, true, mxsRetVal);
			return mxsRetVal.B;
		}
		#endregion

		#endregion

	}

	[DataContract]
	class GLTFExtensionSkyPortalLight : GLTFProperty
	{
		[DataMember(Name = "shape_type", IsRequired = true)] public int shapeType { get; set; }
		[DataMember(Name = "source_radius", IsRequired = true)] public float sourceRadius { get; set; }
		[DataMember(Name = "inner_cone_angle", IsRequired = true)] public float innerConeAngle { get; set; }
		[DataMember(Name = "outer_cone_angle", IsRequired = true)] public float outerConeAngle { get; set; }
	}


	class FlightSimSkyPortalExtension : IBabylonExtensionExporter
	{
		readonly MaterialUtilities.ClassIDWrapper MSFS2024_FlightSimSkyPortalClassID = new MaterialUtilities.ClassIDWrapper(0x3e4d58ee, 0x370452e4);

		#region Implementation of IBabylonExtensionExporter

		public string GetGLTFExtensionName()
		{
			return "ASOBO_sky_portal";
		}

		public ExtendedTypes GetExtendedType()
		{
			return new ExtendedTypes(typeof(GLTFNode));
		}

		public bool ExportBabylonExtension<T>(T babylonObject, ref BabylonScene babylonScene, BabylonExporter exporter)
		{
			// just skip this extension is ment only for GLTF
			return false;
		}

		public bool IsMSFS2024SkyPortalLight(IObject obj)
		{
			bool isMSFS2024FlightSimSkyPortalLight = new MaterialUtilities.ClassIDWrapper(obj.ClassID).Equals(MSFS2024_FlightSimSkyPortalClassID);
			return isMSFS2024FlightSimSkyPortalLight;
		}

		public object ExportGLTFExtension<T1, T2>(T1 babylonObject, ref T2 gltfObject, ref GLTF gltf, GLTFExporter exporter, ExtensionInfo extInfo)
		{
			if (babylonObject is BabylonNode babylonLight)
			{
				GLTFExtensionSkyPortalLight lightExt = new GLTFExtensionSkyPortalLight();

				Guid.TryParse(babylonLight.id, out Guid guid);
				IINode maxNode = Tools.GetINodeByGuid(guid);
				if (maxNode != null)
				{
					IObject obj = maxNode.ObjectRef;
					if (IsMSFS2024SkyPortalLight(obj))
					{
						lightExt.shapeType = GetShapeType(maxNode);
						lightExt.sourceRadius = GetSourceRadius(maxNode);
						lightExt.innerConeAngle = GetInnerConeAngle(maxNode);
						lightExt.outerConeAngle = GetOuterConeAngle(maxNode);
						return lightExt;
					}
				}
			}
			return null;
		}

		#region Parameters
		private int GetShapeType(IINode node)
		{
			string mxs = String.Empty;
			mxs = $"(maxOps.getNodeByHandle {node.Handle}).ShapeType";

			IFPValue mxsRetVal = Loader.Global.FPValue.Create();
			ScriptsUtilities.ExecuteMAXScriptScript(mxs, true, mxsRetVal);
			return mxsRetVal.I;
		}

		private float GetSourceRadius(IINode node)
		{
			string mxs = String.Empty;
			mxs = $"(maxOps.getNodeByHandle {node.Handle}).SourceRadius";

			IFPValue mxsRetVal = Loader.Global.FPValue.Create();
			ScriptsUtilities.ExecuteMAXScriptScript(mxs, true, mxsRetVal);
			return mxsRetVal.F;
		}

		private float GetInnerConeAngle(IINode node)
		{
			string mxs = String.Empty;
			mxs = $"(maxOps.getNodeByHandle {node.Handle}).InnerConeAngle";

			IFPValue mxsRetVal = Loader.Global.FPValue.Create();
			ScriptsUtilities.ExecuteMAXScriptScript(mxs, true, mxsRetVal);
			return mxsRetVal.F;
		}

		private float GetOuterConeAngle(IINode node)
		{
			string mxs = String.Empty;
			mxs = $"(maxOps.getNodeByHandle {node.Handle}).OuterConeAngle";

			IFPValue mxsRetVal = Loader.Global.FPValue.Create();
			ScriptsUtilities.ExecuteMAXScriptScript(mxs, true, mxsRetVal);
			return mxsRetVal.F;
		}
		#endregion

		#endregion

	}
}
