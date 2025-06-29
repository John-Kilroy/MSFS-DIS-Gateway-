using System.Collections.Generic;
using Autodesk.Max;
using BabylonExport.Entities;

namespace MSFS2024_Max2Babylon
{
    public enum BakeAnimationType
    {
        DoNotBakeAnimation,
        BakeAllAnimations,
        BakeSelective
    }

    public class MaxExportParameters : ExportParameters
    {
        public Autodesk.Max.IINode exportNode;
        private List<Autodesk.Max.IILayer> _exportLayers;

        public List<Autodesk.Max.IILayer> ExportLayers
        {
            get { return _exportLayers; }
            set 
            { 
                _exportLayers = value;
                LayerUtilities.ShowExportItemLayers(_exportLayers);
            }
        }
        public bool usePreExportProcess = false;
        public bool applyPreprocessToScene = false;
        public bool flattenNodes = false;
        public bool mergeContainersAndXRef = false;
        public BakeAnimationType bakeAnimationType = BakeAnimationType.DoNotBakeAnimation;
        public LogLevel logLevel = LogLevel.ERROR;

        public IINode GetNodeByHandle(uint handle) 
        {
            return Loader.Core.GetINodeByHandle(handle);
        }

        public List<IILayer> NameToIILayer(string[] layers)
        {
            List<IILayer> result = new List<IILayer>();
            foreach (var l in layers)
            {
                IILayer lay = Loader.Core.LayerManager.GetLayer(l);

                if ( lay != null) 
                {
                    result.Add(lay);
                }
            }

            return result;
        }

        public List<IINode> GetNodesByHandle(uint[] handles)
        {
            List<IINode> nodes = new List<IINode>();
            foreach ( var handle in handles)
            {
                IINode node = GetNodeByHandle(handle);
                if(node != null)
                {
                    nodes.Add(node);
                }
            }
            return nodes;
        }

    }
}
