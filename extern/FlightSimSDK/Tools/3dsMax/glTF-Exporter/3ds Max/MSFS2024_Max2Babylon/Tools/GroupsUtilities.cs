using System.Collections.Generic;
using Autodesk.Max;

namespace MSFS2024_Max2Babylon
{
    static class GroupsUtilities 
    {
        public static List<IINode> GetAllGroups(IINode topNode = null)
        {
            IINode startNode = topNode ?? Loader.Core.RootNode;
            List <IINode> objectList = new List<IINode>();
            foreach (IINode node in startNode.NodeTree())
            {
                if (node.IsHidden(NodeHideFlags.None, false)) continue;
                if (node.IsGroupHead) objectList.Add(node);

            }
            return objectList;
        }

    }
}
