using System.Windows.Forms;
using ActionItem = Autodesk.Max.Plugins.ActionItem;

namespace MSFS2024_Max2Babylon
{
    public class BabylonResolveUniqueIDActionItem : ActionItem
    {

        public override bool ExecuteAction()
        {
            Tools.ResolveUniqueIDConflict();
            MessageBox.Show("UniqueID has been resolved...please save the scene to apply those modifications");

            return true;
        }

        public void Close()
        {
        }

        public override int Id_
        {
            get { return 1; }
        }

        public override string ButtonText
        {
            get { return "Babylon Resolve UniqueIDs"; }
        }

        public override string MenuText
        {
            get { return "&Babylon Resolve UniqueIDs..."; }
        }

        public override string DescriptionText
        {
            get { return "Resolve UniqueIDs in scene"; }
        }

        public override string CategoryText
        {
            get { return "Babylon"; }
        }

        public override bool IsChecked_
        {
            get { return false; }
        }

        public override bool IsItemVisible
        {
            get { return true; }
        }

        public override bool IsEnabled_
        {
            get { return true; }
        }
    }
}
