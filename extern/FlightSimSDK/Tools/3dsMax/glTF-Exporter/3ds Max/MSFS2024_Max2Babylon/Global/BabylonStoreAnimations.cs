using Autodesk.Max;
using ActionItem = Autodesk.Max.Plugins.ActionItem;

namespace MSFS2024_Max2Babylon
{
    class BabylonSaveAnimations:ActionItem
    {

        public override bool ExecuteAction()
        {
            Tools.InitializeGuidsMap();
            var selectedContainers = Tools.GetContainerInSelection();

            if (selectedContainers.Count <= 0)
            {
                AnimationGroupList.SaveDataToAnimationHelper();
                return true;
            }

            foreach (IIContainerObject containerObject in selectedContainers)
            {
                AnimationGroupList.SaveDataToContainerHelper(containerObject);
            }

            return true;
        }

        public void Close()
        {
            return;
        }

        public override int Id_
        {
            get { return 1; }
        }

        public override string ButtonText
        {
            get { return "Store Animation Groups"; }
        }

        public override string MenuText
        {
            get
            {
                var selectedContainers = Tools.GetContainerInSelection();
                if (selectedContainers?.Count > 0)
                {
                    return "& Store AnimationGroups to selected containers";
                }
                else
                {
                    return "&(Xref/Merge) Store Animation Groups";
                }
            }
        }

        public override string DescriptionText
        {
            get { return "Copy AnimationGroups into a BabylonAnimationHelper or a BabylonContainerHelper"; }
        }

        public override string CategoryText
        {
            get { return "MSFS2024"; }
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
