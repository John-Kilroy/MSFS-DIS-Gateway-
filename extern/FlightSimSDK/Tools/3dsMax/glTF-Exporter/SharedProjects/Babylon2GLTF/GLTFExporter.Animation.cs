using BabylonExport.Entities;
using GLTFExport.Entities;
using GLTFExport.Tools;
using System;
using System.Collections.Generic;
using System.Linq;
using Utilities;
using System.Drawing;

namespace Babylon2GLTF
{
	public partial class GLTFExporter
	{

		private void ExportAnimatedNode(GLTF gltf, BabylonNode node, GLTFNode gltfNode, GLTFAnimation gltfAnimation, int startFrame, int endFrame, BabylonAnimationGroup animGroup = null)
		{
			bool nodeHasAnimations = node.animations != null && node.animations.Length > 0 && node.animations[0] != null;
			bool nodeHasExtraAnimations = node.extraAnimations != null && node.extraAnimations.Count > 0 && node.extraAnimations[0] != null;
			BabylonMorphTargetManager morphTargetManager = null;
			bool nodeHasAnimatedMorphTargets = false;

			if (node is BabylonMesh meshNode && meshNode.morphTargetManagerId != null)
			{
				morphTargetManager = GetBabylonMorphTargetManager(babylonScene, meshNode);
				if (morphTargetManager != null)
				{
					nodeHasAnimatedMorphTargets = morphTargetManager.targets.Any(target => target.animations != null && target.animations.Length > 0 && target.animations[0] != null);
				}
			}

			if (!nodeHasAnimations && !nodeHasExtraAnimations && !nodeHasAnimatedMorphTargets)
				return;

			if (nodeHasAnimations && node.animations[0].property == "_matrix")
			{
				ExportBoneAnimation(gltfAnimation, startFrame, endFrame, gltf, node, gltfNode, animGroup);
			}
			else
			{
				ExportNodeAnimation(gltfAnimation, startFrame, endFrame, gltf, node, gltfNode, babylonScene, animGroup);
			}

			if (nodeHasAnimatedMorphTargets)
			{
				ExportMorphTargetWeightAnimation(morphTargetManager, gltf, gltfNode, gltfAnimation.ChannelList, gltfAnimation.SamplerList, startFrame, endFrame, babylonScene);
			}
		}
		private void ExportAnimationGroups(GLTF gltf, BabylonScene babylonScene)
		{
			// Retreive and parse animation group data
			IList<BabylonAnimationGroup> animationGroupList = babylonScene.animationGroups;
			int animationGroupCount = animationGroupList == null ? 0 : animationGroupList.Count;

			gltf.AnimationsList.Clear();
			gltf.AnimationsList.Capacity = Math.Max(gltf.AnimationsList.Capacity, animationGroupCount);

			if (animationGroupCount <= 0)
			{
				logger?.RaiseMessage("GLTFExporter.Animation | No AnimationGroups: exporting all animations together.", 1);
				GLTFAnimation gltfAnimation = new GLTFAnimation
				{
					name = "All Animations"
				};

				int startFrame = babylonScene.TimelineStartFrame;
				int endFrame = babylonScene.TimelineEndFrame;

				foreach (var pair in nodeToGltfNodeMap)
				{
					BabylonNode node = pair.Key;
					GLTFNode gltfNode = pair.Value;

					ExportAnimatedNode(gltf, node, gltfNode, gltfAnimation, startFrame, endFrame);
				}

				if (gltfAnimation.ChannelList.Count > 0)
				{
					gltf.AnimationsList.Add(gltfAnimation);
				}
				else
				{
					logger?.RaiseWarning("[GLTFExporter][WARNING][Animation] No animation data for animation : " + gltfAnimation.name + ". It is ignored.", 1);
				}
			}
			else
			{
				foreach (BabylonAnimationGroup animGroup in animationGroupList)
				{
					logger?.Print("[GLTFExporter][Animation] Exporting Animation : " + animGroup.name, Color.Black);

					GLTFAnimation gltfAnimation = new GLTFAnimation
					{
						name = animGroup.name
					};

					int startFrame = MathUtilities.RoundToInt(animGroup.from);
					int endFrame = MathUtilities.RoundToInt(animGroup.to);

					IEnumerable<string> uniqueIDs = animGroup.targetedAnimations.Select(targetAnim => targetAnim.targetId).Distinct();
					foreach (string id in uniqueIDs)
					{
						// Export custom property animation
						BabylonMaterial babylonMaterial = babylonMaterials.Find(material => material.id.Equals(id));
						GLTFMaterial gltfMaterial = null;

						if (babylonMaterial != null)
						{
							if (!materialToGltfMaterialMap.TryGetValue(babylonMaterial, out gltfMaterial))
							{
								continue;
							}
							bool materialHasAnimations = babylonMaterial.animations != null && babylonMaterial.animations.Length > 0 && babylonMaterial.animations[0] != null;
							if (materialHasAnimations)
							{
								ExportMaterialAnimation(gltfAnimation, startFrame, endFrame, gltf, babylonMaterial);
							}
							continue;
						}

						// Export standard KHRONOS animation Translation/Rotation/Scale
						BabylonNode babylonNode = babylonNodes.Find(node => node.id.Equals(id));
						GLTFNode gltfNode = null;
						// search the babylon scene id map for the babylon node that matches this id
						if (babylonNode != null)
						{
							// Search our babylon->gltf node mapping to see if this node is included in the exported gltf scene
							if (!nodeToGltfNodeMap.TryGetValue(babylonNode, out gltfNode))
							{
								logger?.RaiseWarning("[GLTFExporter][WARNING][Animation] Node " + babylonNode.name + " is not exported, it will be ignored in the animation " + animGroup.name + ".");
								continue;
							}

							ExportAnimatedNode(gltf, babylonNode, gltfNode, gltfAnimation, startFrame, endFrame, animGroup);
						}
						else
						{
							// if the node isn't found in the scene id map, check if it is the id for a morph target
							if (babylonScene.morphTargetManagers != null)
							{
								BabylonMorphTargetManager morphTargetManager = babylonScene.morphTargetManagers.FirstOrDefault(mtm => mtm.targets.Any(target => target.animations != null && target.animations.Length > 0 && target.animations[0] != null));
								if (morphTargetManager != null)
								{
									BabylonMesh mesh = morphTargetManager.sourceMesh;
									if (mesh != null && nodeToGltfNodeMap.TryGetValue(mesh, out gltfNode))
									{
										ExportMorphTargetWeightAnimation(morphTargetManager, gltf, gltfNode, gltfAnimation.ChannelList, gltfAnimation.SamplerList, startFrame, endFrame, babylonScene);
									}
								}
							}
						}
					}

					if (gltfAnimation.ChannelList.Count > 0)
					{
						gltf.AnimationsList.Add(gltfAnimation);
					}
					else
					{
						logger?.RaiseWarning("[GLTFExporter][WARNING][Animation] No animation data for animation : " + animGroup.name + ". It is ignored.");
					}
					// Clear the exported morph target cache, since we are exporting a new animation group. //TODO: we should probably do this more elegantly.
					exportedMorphTargets.Clear();
				}
			}
		}
		private void ExportBoneAnimation(GLTFAnimation gltfAnimation, int startFrame, int endFrame, GLTF gltf, BabylonNode babylonNode, GLTFNode gltfNode, BabylonAnimationGroup animationGroup = null)
		{
			List<GLTFChannel> channelList = gltfAnimation.ChannelList;
			List<GLTFAnimationSampler> samplerList = gltfAnimation.SamplerList;

			if (babylonNode.animations != null && babylonNode.animations[0].property == "_matrix")
			{
				logger.RaiseMessage("GLTFExporter.Animation | Export animation of bone named: " + babylonNode.name, 2);

				BabylonAnimation babylonAnimation = null;
				if (animationGroup != null)
				{
					BabylonTargetedAnimation targetedAnimation = animationGroup.targetedAnimations.FirstOrDefault(animation => animation.targetId == babylonNode.id);
					if (targetedAnimation != null)
					{
						babylonAnimation = targetedAnimation.animation;
					}
				}

				// otherwise fall back to the full animation track on the node.
				if (babylonAnimation == null)
				{
					babylonAnimation = babylonNode.animations[0];
				}

				IEnumerable<BabylonAnimationKey> babylonAnimationKeysInRange = babylonAnimation.keys.Where(key => key.frame >= startFrame && key.frame <= endFrame);
				if (babylonAnimationKeysInRange.Count() <= 0)
					return;

				// --- Input ---
				GLTFAccessor accessorInput = CreateAndPopulateInput(gltf, babylonAnimation, startFrame, endFrame);
				if (accessorInput == null)
					return;

				// --- Output ---
				var paths = new string[] { "translation", "rotation", "scale" };
				var accessorOutputByPath = new Dictionary<string, GLTFAccessor>();

				foreach (string path in paths)
				{
					GLTFAccessor accessorOutput = CreateAccessorOfPath(path, gltf);
					accessorOutputByPath.Add(path, accessorOutput);
				}

				// Populate accessors
				foreach (BabylonAnimationKey babylonAnimationKey in babylonAnimationKeysInRange)
				{
					var matrix = new BabylonMatrix
					{
						m = babylonAnimationKey.values
					};

					var translationBabylon = new BabylonVector3();
					var rotationQuatBabylon = new BabylonQuaternion();
					var scaleBabylon = new BabylonVector3();
					matrix.decompose(scaleBabylon, rotationQuatBabylon, translationBabylon);

					// Switch coordinate system at object level
					translationBabylon.Z *= -1;
					rotationQuatBabylon.X *= -1;
					rotationQuatBabylon.Y *= -1;

					var outputValuesByPath = new Dictionary<string, float[]>
					{
						{ "translation", translationBabylon.ToArray() },
						{ "rotation", rotationQuatBabylon.ToArray() },
						{ "scale", scaleBabylon.ToArray() }
					};

					// Store values as bytes
					foreach (string path in paths)
					{
						GLTFAccessor accessorOutput = accessorOutputByPath[path];
						float[] outputValues = outputValuesByPath[path];

						foreach (var outputValue in outputValues)
						{
							accessorOutput.bytesList.AddRange(BitConverter.GetBytes(outputValue));
						}
						accessorOutput.count++;
					}
				};

				foreach (string path in paths)
				{
					GLTFAccessor accessorOutput = accessorOutputByPath[path];

					// Animation sampler
					var gltfAnimationSampler = new GLTFAnimationSampler
					{
						input = accessorInput.index,
						output = accessorOutput.index
					};
					gltfAnimationSampler.index = samplerList.Count;
					samplerList.Add(gltfAnimationSampler);

					// Target
					var gltfTarget = new GLTFChannelTarget
					{
						node = gltfNode.index
					};
					gltfTarget.path = path;

					// Channel
					var gltfChannel = new GLTFChannel
					{
						sampler = gltfAnimationSampler.index,
						target = gltfTarget
					};
					channelList.Add(gltfChannel);
				}
			}

			ExportGLTFExtension(babylonNode, ref gltfAnimation, gltf);
		}
		
		private void ExportMaterialAnimation(GLTFAnimation gltfAnimation, int startFrame, int endFrame, GLTF gltf, BabylonMaterial babylonMaterial)
		{
			AnimationExtensionInfo info = new AnimationExtensionInfo(startFrame,endFrame);
			ExportGLTFExtension(babylonMaterial, ref gltfAnimation, gltf, info);
		}
		private void ExportNodeAnimation(GLTFAnimation gltfAnimation, int startFrame, int endFrame, GLTF gltf, BabylonNode babylonNode, GLTFNode gltfNode, BabylonScene babylonScene, BabylonAnimationGroup animationGroup = null)
		{
			List<GLTFChannel> channelList = gltfAnimation.ChannelList;
			List<GLTFAnimationSampler> samplerList = gltfAnimation.SamplerList;

			// Combine babylon animations from .babylon file and cached ones
			var babylonAnimations = new List<BabylonAnimation>();
			if (animationGroup != null)
			{
				var targetedAnimations = animationGroup.targetedAnimations.Where(animation => animation.targetId == babylonNode.id);
				foreach (var targetedAnimation in targetedAnimations)
				{
					babylonAnimations.Add(targetedAnimation.animation);
				}
			}

			// Do not include the node animations if a provided animation group already includes them.
			if (babylonAnimations.Count <= 0)
			{
				if (babylonNode.animations != null)
				{
					babylonAnimations.AddRange(babylonNode.animations);
				}

				if (babylonNode.extraAnimations != null)
				{
					babylonAnimations.AddRange(babylonNode.extraAnimations);
				}
			}

			// Filter animations to only keep TRS ones
			babylonAnimations = babylonAnimations.FindAll(babylonAnimation => GetTargetPath(babylonAnimation.property) != null);

			if (babylonAnimations.Count > 0)
			{
				logger?.RaiseMessage("GLTFExporter.Animation | Export animations of node named: " + babylonNode.name, 2);


				foreach (BabylonAnimation babylonAnimation in babylonAnimations)
				{
					var babylonAnimationKeysInRange = babylonAnimation.keys.Where(key => key.frame >= startFrame && key.frame <= endFrame);
					if (babylonAnimationKeysInRange.Count() <= 0)
					{
						logger?.RaiseWarning("[GLTFExporter][WARINING][Animations] No frames to export in node animation " + babylonAnimation.name + " of node named " + babylonNode.name + ". Animation will be ignored.");
						continue;
					}

					// Target
					var gltfTarget = new GLTFChannelTarget
					{
						node = gltfNode.index
					};
					gltfTarget.path = GetTargetPath(babylonAnimation.property);

					// --- Input ---
					GLTFAccessor accessorInput = CreateAndPopulateInput(gltf, babylonAnimation, startFrame, endFrame);
					if (accessorInput == null)
						continue;

					// --- Output ---
					GLTFAccessor accessorOutput = CreateAccessorOfPath(gltfTarget.path, gltf);
					if (accessorOutput == null)
						continue;

					// Populate accessor
					int numKeys = 0;
					foreach (BabylonAnimationKey babylonAnimationKey in babylonAnimationKeysInRange)
					{
						numKeys++;

						// copy data before changing it in case animation groups overlap
						float[] outputValues = new float[babylonAnimationKey.values.Length];
						babylonAnimationKey.values.CopyTo(outputValues, 0);

						// Switch coordinate system at object level
						if (babylonAnimation.property == "position")
						{
							outputValues[2] *= -1;
						}
						else if (babylonAnimation.property == "rotationQuaternion")
						{
							outputValues[0] *= -1;
							outputValues[1] *= -1;
						}

						// Store values as bytes
						foreach (float outputValue in outputValues)
						{
							accessorOutput.bytesList.AddRange(BitConverter.GetBytes(outputValue));
						}
					};

					if (numKeys == 0)
					{
						logger?.RaiseWarning("[GLTFExporter][WARINING][Animations] No frames to export in node animation " + babylonAnimation.name + " of node named " + babylonNode.name + ". This will cause an error in the output gltf.");
					}

					accessorOutput.count = numKeys;

					// Animation sampler
					GLTFAnimationSampler gltfAnimationSampler = new GLTFAnimationSampler
					{
						input = accessorInput.index,
						output = accessorOutput.index
					};
					gltfAnimationSampler.index = samplerList.Count;
					samplerList.Add(gltfAnimationSampler);

					// Channel
					GLTFChannel gltfChannel = new GLTFChannel
					{
						sampler = gltfAnimationSampler.index,
						target = gltfTarget
					};

					channelList.Add(gltfChannel);
				}
			}
			AnimationExtensionInfo info = new AnimationExtensionInfo(startFrame, endFrame);
			ExportGLTFExtension(babylonNode, ref gltfAnimation, gltf,info);
		}

		public BabylonAnimation GetDummyAnimation(GLTFNode gltfNode, int startFrame, int endFrame, BabylonScene babylonScene)
		{
			var dummyAnimation = new BabylonAnimation
			{
				name = "Dummy",
				property = "scaling",
				framePerSecond = babylonScene.TimelineFramesPerSecond,
				dataType = (int)BabylonAnimation.DataType.Vector3
			};

			var startKey = new BabylonAnimationKey
			{
				frame = startFrame,
				values = gltfNode.scale
			};

			var endKey = new BabylonAnimationKey
			{
				frame = endFrame,
				values = gltfNode.scale
			};

			dummyAnimation.keys = new BabylonAnimationKey[] { startKey, endKey };

			return dummyAnimation;
		}

		public GLTFAccessor CreateAndPopulateInput(GLTF gltf, BabylonAnimation babylonAnimation, int startFrame, int endFrame, bool offsetToStartAtFrameZero = true)
		{
			IEnumerable<BabylonAnimationKey> babylonAnimationKeysInRange = babylonAnimation.keys.Where(key => key.frame >= startFrame && key.frame <= endFrame);
			if (babylonAnimationKeysInRange.Count() <= 0) // do not make empty accessors, so bail out.
				return null;

			GLTFBuffer buffer = GLTFBufferService.Instance.GetBuffer(gltf);
			GLTFAccessor accessorInput = GLTFBufferService.Instance.CreateAccessor(
				gltf,
				GLTFBufferService.Instance.GetBufferViewAnimationFloatScalar(gltf, buffer),
				"accessorAnimationInput",
				GLTFAccessor.ComponentType.FLOAT,
				GLTFAccessor.TypeEnum.SCALAR
			);
			// Populate accessor
			accessorInput.min = new float[] { float.MaxValue };
			accessorInput.max = new float[] { float.MinValue };

			int numKeys = 0;
			foreach (BabylonAnimationKey babylonAnimationKey in babylonAnimationKeysInRange)
			{
				numKeys++;
				float inputValue = babylonAnimationKey.frame;
				if (offsetToStartAtFrameZero) inputValue -= startFrame;
				inputValue /= babylonAnimation.framePerSecond;
				// Store values as bytes
				accessorInput.bytesList.AddRange(BitConverter.GetBytes(inputValue));
				// Update min and max values
				GLTFBufferService.UpdateMinMaxAccessor(accessorInput, inputValue);
			};
			accessorInput.count = numKeys;

			if (accessorInput.count == 0)
			{
				logger?.RaiseWarning(String.Format("[GLTFExporter][WARINING][Animations] No input frames in GLTF Accessor for animation \"{0}\". This will cause an error in the output gltf.", babylonAnimation.name));
			}

			return accessorInput;
		}

		public GLTFAccessor CreateAccessorOfPath(string path, GLTF gltf)
		{
			var buffer = GLTFBufferService.Instance.GetBuffer(gltf);
			GLTFAccessor accessorOutput = null;
			switch (path)
			{
				case "translation":
					accessorOutput = GLTFBufferService.Instance.CreateAccessor(
						gltf,
						GLTFBufferService.Instance.GetBufferViewAnimationFloatVec3(gltf, buffer),
						"accessorAnimationPositions",
						GLTFAccessor.ComponentType.FLOAT,
						GLTFAccessor.TypeEnum.VEC3
					);
					break;
				case "rotation":
					accessorOutput = GLTFBufferService.Instance.CreateAccessor(
						gltf,
						GLTFBufferService.Instance.GetBufferViewAnimationFloatVec4(gltf, buffer),
						"accessorAnimationRotations",
						GLTFAccessor.ComponentType.FLOAT,
						GLTFAccessor.TypeEnum.VEC4
					);
					break;
				case "scale":
					accessorOutput = GLTFBufferService.Instance.CreateAccessor(
						gltf,
						GLTFBufferService.Instance.GetBufferViewAnimationFloatVec3(gltf, buffer),
						"accessorAnimationScales",
						GLTFAccessor.ComponentType.FLOAT,
						GLTFAccessor.TypeEnum.VEC3
					);
					break;
				case "fov":
					accessorOutput = GLTFBufferService.Instance.CreateAccessor(
						gltf,
						GLTFBufferService.Instance.GetBufferViewAnimationFloatScalar(gltf, buffer),
						"accessorAnimationFovs",
						GLTFAccessor.ComponentType.FLOAT,
						GLTFAccessor.TypeEnum.SCALAR
					);
					break;
				case "weights":
					accessorOutput = GLTFBufferService.Instance.CreateAccessor(
						gltf,
						GLTFBufferService.Instance.GetBufferViewAnimationFloatScalar(gltf, buffer),
						"accessorAnimationWeights",
						GLTFAccessor.ComponentType.FLOAT,
						GLTFAccessor.TypeEnum.SCALAR
					);
					break;
			}
			return accessorOutput;
		}

		public List<BabylonMorphTargetManager> exportedMorphTargets = new List<BabylonMorphTargetManager>();
		private bool ExportMorphTargetWeightAnimation(BabylonMorphTargetManager babylonMorphTargetManager, GLTF gltf, GLTFNode gltfNode, List<GLTFChannel> channelList, List<GLTFAnimationSampler> samplerList, int startFrame, int endFrame, BabylonScene babylonScene, bool offsetToStartAtFrameZero = true)
		{
			if (exportedMorphTargets.Contains(babylonMorphTargetManager) || !IsBabylonMorphTargetManagerAnimationValid(babylonMorphTargetManager))
			{
				return false;
			}

			Dictionary<int, List<float>> influencesPerFrame = GetTargetManagerAnimationsData(babylonMorphTargetManager);
			List<int> frames = new List<int>(influencesPerFrame.Keys);

			List<int> framesInRange = frames.Where(frame => frame >= startFrame && frame <= endFrame).ToList();
			framesInRange.Sort(); // Mandatory to sort otherwise gltf loader of babylon doesn't understand
			if (framesInRange.Count() <= 0)
				return false;

			logger.RaiseMessage("GLTFExporter.Animation | Export animation of morph target manager with id: " + babylonMorphTargetManager.id, 2);

			// Target
			var gltfTarget = new GLTFChannelTarget
			{
				node = gltfNode.index
			};
			gltfTarget.path = "weights";

			// Buffer
			GLTFBuffer buffer = GLTFBufferService.Instance.GetBuffer(gltf);

			// --- Input ---
			GLTFAccessor accessorInput = GLTFBufferService.Instance.CreateAccessor(
				gltf,
				GLTFBufferService.Instance.GetBufferViewAnimationFloatScalar(gltf, buffer),
				"accessorAnimationInput",
				GLTFAccessor.ComponentType.FLOAT,
				GLTFAccessor.TypeEnum.SCALAR
			);
			// Populate accessor
			accessorInput.min = new float[] { float.MaxValue };
			accessorInput.max = new float[] { float.MinValue };

			int numKeys = 0;
			foreach (int frame in framesInRange)
			{
				numKeys++;
				float inputValue = frame;
				if (offsetToStartAtFrameZero) inputValue -= startFrame;
				inputValue /= (float)babylonScene.TimelineFramesPerSecond;
				// Store values as bytes
				accessorInput.bytesList.AddRange(BitConverter.GetBytes(inputValue));
				// Update min and max values
				GLTFBufferService.UpdateMinMaxAccessor(accessorInput, inputValue);
			}
			accessorInput.count = numKeys;

			if (accessorInput.count == 0)
			{
				logger.RaiseWarning(String.Format("[GLTFExporter][WARINING][Animations] No frames to export in morph target animation \"weight\" for mesh named \"{0}\". This will cause an error in the output gltf.", babylonMorphTargetManager.sourceMesh.name));
			}

			// --- Output ---
			GLTFAccessor accessorOutput = GLTFBufferService.Instance.CreateAccessor(
				gltf,
				GLTFBufferService.Instance.GetBufferViewAnimationFloatScalar(gltf, buffer),
				"accessorAnimationWeights",
				GLTFAccessor.ComponentType.FLOAT,
				GLTFAccessor.TypeEnum.SCALAR
			);
			// Populate accessor
			foreach (int frame in framesInRange)
			{
				List<float> outputValues = influencesPerFrame[frame];
				// Store values as bytes
				foreach (float outputValue in outputValues)
				{
					accessorOutput.count++;
					accessorOutput.bytesList.AddRange(BitConverter.GetBytes(outputValue));
				}
			}

			// Animation sampler
			var gltfAnimationSampler = new GLTFAnimationSampler
			{
				input = accessorInput.index,
				output = accessorOutput.index
			};
			gltfAnimationSampler.index = samplerList.Count;
			samplerList.Add(gltfAnimationSampler);

			// Channel
			var gltfChannel = new GLTFChannel
			{
				sampler = gltfAnimationSampler.index,
				target = gltfTarget
			};
			channelList.Add(gltfChannel);

			// Mark this morph target as exported.
			exportedMorphTargets.Add(babylonMorphTargetManager);
			return true;
		}

		private bool IsBabylonMorphTargetManagerAnimationValid(BabylonMorphTargetManager babylonMorphTargetManager)
		{
			bool hasAnimation = false;
			bool areAnimationsValid = true;
			foreach (BabylonMorphTarget babylonMorphTarget in babylonMorphTargetManager.targets)
			{
				if (babylonMorphTarget.animations != null && babylonMorphTarget.animations.Length > 0)
				{
					hasAnimation = true;
					// Ensure target has only one animation
					if (babylonMorphTarget.animations.Length > 1)
					{
						areAnimationsValid = false;
						logger.RaiseWarning("[GLTFExporter][WARINING][Animations] Only one animation is supported for morph targets", 3);
						continue;
					}

					// Ensure the target animation property is 'influence'
					bool targetHasInfluence = false;
					foreach (BabylonAnimation babylonAnimation in babylonMorphTarget.animations)
					{
						if (babylonAnimation.property == "influence")
						{
							targetHasInfluence = true;
						}
					}
					if (targetHasInfluence == false)
					{
						areAnimationsValid = false;
						logger.RaiseWarning("[GLTFExporter][WARINING][Animations] Only 'influence' animation is supported for morph targets", 3);
						continue;
					}
				}
			}

			return hasAnimation && areAnimationsValid;
		}

		/// <summary>
		/// The keys of each BabylonMorphTarget animation ARE NOT assumed to be identical.
		/// This function merges together all keys and binds to each an influence value for all targets.
		/// A target influence value is automatically computed when necessary.
		/// Computation rules are:
		/// - linear interpolation between target key range
		/// - constant value outside target key range
		/// </summary>
		/// <example>
		/// When:
		/// animation1.keys = {0, 25, 50, 100}
		/// animation2.keys = {50, 75, 100}
		/// 
		/// Gives:
		/// mergedKeys = {0, 25, 50, 100, 75}
		/// range1=[0, 100]
		/// range2=[50, 100]
		/// for animation1, the value associated to key=75 is the interpolation of its values between 50 and 100
		/// for animation2, the value associated to key=0 is equal to the one at key=50 since 0 is out of range [50, 100] (same for key=25)</example>
		/// <param name="babylonMorphTargetManager"></param>
		/// <returns>A map which for each frame, gives the influence value of all targets</returns>
		public Dictionary<int, List<float>> GetTargetManagerAnimationsData(BabylonMorphTargetManager babylonMorphTargetManager)
		{
			// Merge all keys into a single set (no duplicated frame)
			var mergedFrames = new HashSet<int>();
			foreach (var babylonMorphTarget in babylonMorphTargetManager.targets)
			{
				if (babylonMorphTarget.animations != null)
				{
					var animation = babylonMorphTarget.animations[0];
					foreach (BabylonAnimationKey animationKey in animation.keys)
					{
						mergedFrames.Add((int)Math.Floor(animationKey.frame));
					}
				}
			}

			// For each frame, gives the influence value of all targets (gltf structure)
			Dictionary<int, List<float>> influencesPerFrame = new Dictionary<int, List<float>>();
			foreach (int frame in mergedFrames)
			{
				influencesPerFrame.Add(frame, new List<float>());
			}

			foreach (BabylonMorphTarget babylonMorphTarget in babylonMorphTargetManager.targets)
			{
				// For a given target, for each frame, gives the influence value of the target (babylon structure)
				Dictionary<int, float> influencePerFrameForTarget = new Dictionary<int, float>();

				if (babylonMorphTarget.animations != null && babylonMorphTarget.animations.Length > 0)
				{
					BabylonAnimation animation = babylonMorphTarget.animations[0];
					if (animation.keys.Length == 1)
					{
						// Same influence for all frames
						float influence = animation.keys[0].values[0];
						foreach (int frame in mergedFrames)
						{
							influencePerFrameForTarget.Add(frame, influence);
						}
					}
					else
					{
						// Retreive target animation key range [min, max]
						List<BabylonAnimationKey> babylonAnimationKeys = new List<BabylonAnimationKey>(animation.keys);
						babylonAnimationKeys.Sort();
						BabylonAnimationKey minAnimationKey = babylonAnimationKeys[0];
						BabylonAnimationKey maxAnimationKey = babylonAnimationKeys[babylonAnimationKeys.Count - 1];
						
						foreach (int frame in mergedFrames)
						{
							// Surround the current frame with closest keys available for the target
							BabylonAnimationKey lowerAnimationKey = minAnimationKey;
							BabylonAnimationKey upperAnimationKey = maxAnimationKey;
							foreach (BabylonAnimationKey animationKey in animation.keys)
							{
								if (lowerAnimationKey.frame < animationKey.frame && animationKey.frame <= frame)
								{
									lowerAnimationKey = animationKey;
								}
								if (frame <= animationKey.frame && animationKey.frame < upperAnimationKey.frame)
								{
									upperAnimationKey = animationKey;
								}
							}

							// In case the target has a key for this frame
							// or the current frame is out of target animation key range
							if (lowerAnimationKey.frame == upperAnimationKey.frame)
							{
								influencePerFrameForTarget.Add(frame, lowerAnimationKey.values[0]);
							}
							else
							{
								// Interpolate influence values
								float t = 1.0f * (frame - lowerAnimationKey.frame) / (upperAnimationKey.frame - lowerAnimationKey.frame);
								float influence = MathUtilities.Lerp(lowerAnimationKey.values[0], upperAnimationKey.values[0], t);
								influencePerFrameForTarget.Add(frame, influence);
							}
						}
					}
				}
				else
				{
					// Target is not animated
					// Fill all frames with 0
					foreach (int frame in mergedFrames)
					{
						influencePerFrameForTarget.Add(frame, 0);
					}
				}

				// Switch from babylon to gltf storage representation
				foreach (int frame in mergedFrames)
				{
					List<float> influences = influencesPerFrame[frame];
					influences.Add(influencePerFrameForTarget[frame]);
				}
			}

			return influencesPerFrame;
		}

		public string GetTargetPath(string babylonProperty)
		{
			switch (babylonProperty)
			{
				case "position":
					return "translation";
				case "rotationQuaternion":
					return "rotation";
				case "scaling":
					return "scale";
				default:
					return null;
			}
		}
		public string GetExtensionTargetPath(string babylonProperty)
		{
			switch (babylonProperty)
			{
				case "fov":
					return "fov";
				default:
					return null;
			}
		}

		private void ExportBoneAnimation(GLTFAnimation gltfAnimation, int startFrame, int endFrame, GLTF gltf, BabylonNode babylonNode, GLTFNode gltfNode)
		{
			var channelList = gltfAnimation.ChannelList;
			var samplerList = gltfAnimation.SamplerList;

			if (babylonNode.animations != null && babylonNode.animations[0].property == "_matrix")
			{
				logger?.RaiseMessage("GLTFExporter.Animation | Export animation of bone named: " + babylonNode.name, 2);

				var babylonAnimation = babylonNode.animations[0];

				var babylonAnimationKeysInRange = babylonAnimation.keys.Where(key => key.frame >= startFrame && key.frame <= endFrame);
				if (babylonAnimationKeysInRange.Count() <= 0)
					return;

				// --- Input ---
				var accessorInput = CreateAndPopulateInput(gltf, babylonAnimation, startFrame, endFrame);
				if (accessorInput == null)
					return;

				// --- Output ---
				var paths = new string[] { "translation", "rotation", "scale" };
				var accessorOutputByPath = new Dictionary<string, GLTFAccessor>();

				foreach (string path in paths)
				{
					GLTFAccessor accessorOutput = CreateAccessorOfPath(path, gltf);
					accessorOutputByPath.Add(path, accessorOutput);
				}

				// Populate accessors
				foreach (var babylonAnimationKey in babylonAnimationKeysInRange)
				{
					var matrix = new BabylonMatrix();
					matrix.m = babylonAnimationKey.values;

					var translationBabylon = new BabylonVector3();
					var rotationQuatBabylon = new BabylonQuaternion();
					var scaleBabylon = new BabylonVector3();
					matrix.decompose(scaleBabylon, rotationQuatBabylon, translationBabylon);
					
					// Switch coordinate system at object level
					translationBabylon.Z *= -1;
					translationBabylon *= exportParameters.scaleFactor;
					rotationQuatBabylon.X *= -1;
					rotationQuatBabylon.Y *= -1;

					var outputValuesByPath = new Dictionary<string, float[]>();
					outputValuesByPath.Add("translation", translationBabylon.ToArray());
					outputValuesByPath.Add("rotation", rotationQuatBabylon.ToArray());
					outputValuesByPath.Add("scale", scaleBabylon.ToArray());

					// Store values as bytes
					foreach (string path in paths)
					{
						var accessorOutput = accessorOutputByPath[path];
						var outputValues = outputValuesByPath[path];

						foreach (var outputValue in outputValues)
						{
							accessorOutput.bytesList.AddRange(BitConverter.GetBytes(outputValue));
						}
						accessorOutput.count++;
					}
				};

				foreach (string path in paths)
				{
					var accessorOutput = accessorOutputByPath[path];

					// Animation sampler
					var gltfAnimationSampler = new GLTFAnimationSampler
					{
						input = accessorInput.index,
						output = accessorOutput.index
					};
					gltfAnimationSampler.index = samplerList.Count;
					samplerList.Add(gltfAnimationSampler);

					// Target
					var gltfTarget = new GLTFChannelTarget
					{
						node = gltfNode.index
					};
					gltfTarget.path = path;

					// Channel
					var gltfChannel = new GLTFChannel
					{
						sampler = gltfAnimationSampler.index,
						target = gltfTarget
					};

					channelList.Add(gltfChannel);
				}
			}
			 AnimationExtensionInfo info = new AnimationExtensionInfo(startFrame, endFrame);
			ExportGLTFExtension(babylonNode, ref gltfAnimation,gltf,info);
		}
		private void ExportGenericPropertyAnimation<T1,T2>(GLTFAnimation gltfAnimation, int startFrame, int endFrame, GLTF gltf, T1 babylonObject, T2 gltfObject, BabylonScene babylonScene)
		{
			AnimationExtensionInfo info = new AnimationExtensionInfo(startFrame, endFrame);
			ExportGLTFExtension(babylonObject, ref gltfAnimation, gltf, info);
		}
	}
}
