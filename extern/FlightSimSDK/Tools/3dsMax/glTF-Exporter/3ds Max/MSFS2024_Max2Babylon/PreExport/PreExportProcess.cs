using Autodesk.Max;
using BabylonExport.Entities;
using System.Collections.Generic;
using System.Diagnostics;
using System.Drawing;
using Utilities;

namespace MSFS2024_Max2Babylon.PreExport
{
	public class PreExportProcess
	{
		private readonly ExportParameters exportParameters;
		public ILoggingProvider logger;

		public PreExportProcess(ExportParameters _exportParameters, ILoggingProvider _logger)
		{
			exportParameters = _exportParameters;
			logger = _logger;
		}

		public void BakeSelectiveAnimations(MaxExportParameters maxExportParameters)
		{
			logger?.Print("[BABYLON][PRE-EXPORT] Bake Selective Animations", Color.Black, 0);
			IINode hierachyRoot = maxExportParameters.exportNode ?? Loader.Core.RootNode;

			IINodeTab selection = Tools.CreateNodeTab();
			foreach (IINode iNode in hierachyRoot.NodeTree())
			{
				if (iNode.IsMarkedAsObjectToBakeAnimation())
				{
					selection.AppendNode(iNode, false, 0);
				}
			}

			if (!hierachyRoot.IsRootNode) selection.AppendNode(hierachyRoot, false, 0);

			Loader.Core.SelectNodeTab(selection, true, false);

			RunBakeAnimationScript();
		}

		public void BakeAllAnimations(MaxExportParameters maxExportParameters)
		{
			logger?.Print("[BABYLON][PRE-EXPORT] Bake All Animations", Color.Black, 0);

			IINodeTab selection = Tools.CreateNodeTab();
			IINode hierachyRoot = maxExportParameters.exportNode ?? Loader.Core.RootNode;

			foreach (IINode iNode in hierachyRoot.NodeTree())
			{
				selection.AppendNode(iNode, false, 0);
			}

			if (!hierachyRoot.IsRootNode) selection.AppendNode(hierachyRoot, false, 0);

			Loader.Core.SelectNodeTab(selection, true, false);

			RunBakeAnimationScript();
		}

		public void RunBakeAnimationScript()
		{
			ScriptsUtilities.ExecuteMaxScriptCommand(@"
				sel = $selection
				temps = #()

				allObjs = for obj in sel where isvalidnode obj collect obj

				for obj in allObjs do 
				(
					tmp = Point name:obj.name

					append temps tmp

					--store anim to a point
					for t = animationRange.start to animationRange.end do (
					   with animate on at time t tmp.transform = obj.transform
					 )
				)

				i = 1
				for obj in allObjs do 
				(
					print (""Bake animation on node : "" + obj.name as string)
					obj.controller = Link_Constraint()
					obj.controller = prs()
	
					--copy back anim from point
					 for t = animationRange.start to animationRange.end do (
						with animate on at time t obj.transform = temps[i].transform
					   )

					i += 1
				)

				for t in temps do (
					delete t
				)

				clearSelection()
			 ");
		}
		
		public void ExportClosedContainers()
		{
			List<IILayer> containerLayers = new List<IILayer>();
			List<IIContainerObject> sceneContainers = Tools.GetAllContainers();
			foreach (IIContainerObject containerObject in sceneContainers)
			{
				if (!containerObject.IsInherited) continue;
				containerLayers.Clear();
				if (!containerObject.LoadContainer)
				{
					logger?.RaiseWarning($"[BABYLON][WARINING][PRE-EXPORT] Impossible to load container {containerObject.ContainerNode.Name}...");
				}
				if (!containerObject.UnloadContainer)
				{
					logger?.RaiseWarning($"[BABYLON][WARINING][PRE-EXPORT] Impossible to update container {containerObject.ContainerNode.Name}...");
				}
				if (!containerObject.MakeUnique)
				{
					logger?.RaiseWarning($"[BABYLON][WARINING][PRE-EXPORT] Impossible to make unique container{containerObject.ContainerNode.Name}...");
				}
				int resolvePropertySet = 0;
				if (containerObject.ContainerNode.GetUserPropBool("flightsim_resolved", ref resolvePropertySet) && resolvePropertySet > 0)
				{
					throw new System.Exception($"{containerObject.ContainerNode.Name} has an invalid object property 'flightsim_resolved', " +
						$"remove it manually through Right Click -> Object Properties -> UserDefined  and save the scene");
				}
				containerLayers = containerObject.GetContainerLayers();
				foreach (var layer in containerLayers)
				{
					layer.Hide(false, false);
				}
				foreach (IINode node in containerObject.ContainerNode.NodeTree())
				{
					node.Hide(false);
				}

				logger?.Print($"[BABYLON][PRE-EXPORT] Update and merge container {containerObject.ContainerNode.Name}...", Color.Green);

			}
			AnimationGroupList.LoadDataFromAllContainers();

			foreach (IIContainerObject containerObject in sceneContainers)
			{
				// this property must be set to false at the and on the export of a containers
				// saving the scene with the property stored end to conflict and error on the IDresolved for multiple inherited containers
				containerObject.ContainerNode.SetUserPropBool("flightsim_resolved", false);
			}
		}

		public void MergeAllXrefRecords()
		{
			if (Loader.IIObjXRefManager.RecordCount <= 0) return;
			while (Loader.IIObjXRefManager.RecordCount > 0)
			{
				var record = Loader.IIObjXRefManager.GetRecord(0);
				logger?.Print($"[BABYLON][PRE-EXPORT] Merge XRef record {record.SrcFile.FileName}...", Color.Black);
				Loader.IIObjXRefManager.MergeRecordIntoScene(record);
				//todo: load data from animation helper of xref scene merged
				//to prevent to load animations from helper created without intention
			}
			AnimationGroupList.LoadDataFromAnimationHelpers();
		}

		public void ApplyPreExport()
		{
			var watch = new Stopwatch();
			watch.Start();
			if (exportParameters is MaxExportParameters)
			{
				MaxExportParameters maxExporterParameters = (exportParameters as MaxExportParameters);

				if (maxExporterParameters.mergeContainersAndXRef)
				{
					logger?.Print("[BABYLON][PRE-EXPORT] Merging containers and Xref", Color.Black, 0);
					ExportClosedContainers();
					MergeAllXrefRecords();

					var containersXrefMergeTime = watch.ElapsedMilliseconds / 1000.0;
					logger?.Print(string.Format("[BABYLON][PRE-EXPORT] Containers and Xref  merged in {0:0.00}s", containersXrefMergeTime), Color.Blue);
				}

				switch (maxExporterParameters.bakeAnimationType)
				{
					case BakeAnimationType.BakeAllAnimations:
						BakeAllAnimations(maxExporterParameters);
						break;
					case BakeAnimationType.BakeSelective:
						BakeSelectiveAnimations(maxExporterParameters);
						break;
					default:
						logger?.Print("[BABYLON][PRE-EXPORT] Do not bake animations.", Color.Black);
						break;
				}
			}
			watch.Stop();
		}

	}
}
