using Autodesk.Max;

namespace MSFS2024_Max2Babylon
{
    public static class MeshUtlities
    {
        public static ITriObject GetTriObjectFromNode(this IINode iNode)
        {
            IObject obj = iNode.EvalWorldState(Loader.Core.Time, false).Obj;
            if (obj.CanConvertToType(Loader.Global.TriObjectClassID) == 1)
            {
                return (ITriObject) obj.ConvertToType(Loader.Core.Time, Loader.Global.TriObjectClassID);
            }
            return null;
        }

        public static IPolyObject GetPolyObjectFromNode(this IINode iNode)
        {
            IObject obj = iNode.EvalWorldState(Loader.Core.Time, false).Obj;
            if (obj.CanConvertToType(Loader.Global.PolyObjectClassID) == 1)
            {
                return (IPolyObject) obj.ConvertToType(Loader.Core.Time, Loader.Global.PolyObjectClassID);
            }
            return null;
        }

        public static bool IsMesh(this IINode node) 
        {
            IObject obj = node.EvalWorldState(Loader.Core.Time, false).Obj;
            return (obj.CanConvertToType(Loader.Global.TriObjectClassID) == 1);
        }
    }
}
