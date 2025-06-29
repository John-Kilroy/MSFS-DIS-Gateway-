using System;
using System.Collections.Generic;
using System.Windows.Forms;
using Autodesk.Max;

namespace MSFS2024_Max2Babylon
{
    public partial class ScenePropertiesForm : Form
    {
        public ScenePropertiesForm()
        {
            InitializeComponent();
        }

        private void butOK_Click(object sender, EventArgs e)
        {
            //flight sim
            Tools.UpdateNumericUpDown(numFlightSimFadeScale, new List<IINode> { Loader.Core.RootNode }, "flightsim_fade_globalscale");
        }

        private void ScenePropertiesForm_Load(object sender, EventArgs e)
        {

            //flightsim
            Tools.PrepareNumericUpDown(numFlightSimFadeScale, new List<IINode> { Loader.Core.RootNode }, "flightsim_fade_globalscale",1.0f);
        }
    }
}
