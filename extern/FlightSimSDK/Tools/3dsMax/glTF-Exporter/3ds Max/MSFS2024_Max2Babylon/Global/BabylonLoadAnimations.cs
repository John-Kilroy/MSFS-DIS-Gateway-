using Autodesk.Max;
using ActionItem = Autodesk.Max.Plugins.ActionItem;

namespace MSFS2024_Max2Babylon
{
    class BabylonLoadAnimations:ActionItem
    {
        public override bool ExecuteAction()
        {
            var selectedContainers = Tools.GetContainerInSelection();

            if (selectedContainers?.Count <= 0)
            {
                AnimationGroupList.LoadDataFromAnimationHelpers();
                return true;
            }

            foreach (IIContainerObject containerObject in selectedContainers)
            {
                AnimationGroupList.LoadDataFromContainerHelper(containerObject);
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
            get { return "Load Animation Groups"; }
        }

        public override string MenuText
        {
            get
            {
                var selectedContainers = Tools.GetContainerInSelection();
                if (selectedContainers?.Count > 0)
                {
                    return "& Load Animation Groups from selected containers";
                }
                else
                {
                    return "&(Xref/Merge) Load Animation Groups";
                }
            }
        }

        public override string DescriptionText
        {
            get { return "Load AnimationGroups from Scnene or selected Containers"; }
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