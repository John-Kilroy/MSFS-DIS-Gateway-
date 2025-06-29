using System;
using Autodesk.Max;
using Utilities;

namespace MSFS2024_Max2Babylon
{
    public static class CameraUtilities
    {
        public static ICameraObject GetGenCameraFromNode(this IINode iNode, ILoggingProvider logger)
        {
            ICameraObject result = null;
            IObject obj = iNode.EvalWorldState(Loader.Core.Time, false).Obj;
            try
            {
                result = (ICameraObject)obj;
            }
            catch (Exception)
            {
                logger.RaiseWarning($"[BABYLON][WARINING][Camera] Camera type format of node {iNode.Name} is not supported");
            }
            return result;
        }
    }
}
