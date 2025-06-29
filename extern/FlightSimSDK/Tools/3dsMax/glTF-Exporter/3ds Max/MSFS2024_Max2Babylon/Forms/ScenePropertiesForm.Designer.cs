namespace MSFS2024_Max2Babylon
{
    partial class ScenePropertiesForm
    {
        /// <summary>
        /// Required designer variable.
        /// </summary>
        private System.ComponentModel.IContainer components = null;

        /// <summary>
        /// Clean up any resources being used.
        /// </summary>
        /// <param name="disposing">true if managed resources should be disposed; otherwise, false.</param>
        protected override void Dispose(bool disposing)
        {
            if (disposing && (components != null))
            {
                components.Dispose();
            }
            base.Dispose(disposing);
        }

        #region Windows Form Designer generated code

        /// <summary>
        /// Required method for Designer support - do not modify
        /// the contents of this method with the code editor.
        /// </summary>
        private void InitializeComponent()
        {
			this.butCancel = new System.Windows.Forms.Button();
			this.butOK = new System.Windows.Forms.Button();
			this.groupBox2 = new System.Windows.Forms.GroupBox();
			this.chkAnimations = new System.Windows.Forms.CheckBox();
			this.ofdOpenSound = new System.Windows.Forms.OpenFileDialog();
			this.groupBox5 = new System.Windows.Forms.GroupBox();
			this.chkMorphExportTangent = new System.Windows.Forms.CheckBox();
			this.ckkMorphExportNormals = new System.Windows.Forms.CheckBox();
			this.groupBox6 = new System.Windows.Forms.GroupBox();
			this.numFlightSimFadeScale = new System.Windows.Forms.NumericUpDown();
			this.lblFlightSimFadeScale = new System.Windows.Forms.Label();
			this.groupBox2.SuspendLayout();
			this.groupBox5.SuspendLayout();
			this.groupBox6.SuspendLayout();
			((System.ComponentModel.ISupportInitialize)(this.numFlightSimFadeScale)).BeginInit();
			this.SuspendLayout();
			// 
			// butCancel
			// 
			this.butCancel.Anchor = System.Windows.Forms.AnchorStyles.Bottom;
			this.butCancel.DialogResult = System.Windows.Forms.DialogResult.Cancel;
			this.butCancel.FlatStyle = System.Windows.Forms.FlatStyle.Flat;
			this.butCancel.Location = new System.Drawing.Point(227, 312);
			this.butCancel.Margin = new System.Windows.Forms.Padding(4, 4, 4, 4);
			this.butCancel.Name = "butCancel";
			this.butCancel.Size = new System.Drawing.Size(100, 28);
			this.butCancel.TabIndex = 101;
			this.butCancel.Text = "Cancel";
			this.butCancel.UseVisualStyleBackColor = true;
			// 
			// butOK
			// 
			this.butOK.Anchor = System.Windows.Forms.AnchorStyles.Bottom;
			this.butOK.DialogResult = System.Windows.Forms.DialogResult.OK;
			this.butOK.FlatStyle = System.Windows.Forms.FlatStyle.Flat;
			this.butOK.Location = new System.Drawing.Point(119, 312);
			this.butOK.Margin = new System.Windows.Forms.Padding(4, 4, 4, 4);
			this.butOK.Name = "butOK";
			this.butOK.Size = new System.Drawing.Size(100, 28);
			this.butOK.TabIndex = 100;
			this.butOK.Text = "OK";
			this.butOK.UseVisualStyleBackColor = true;
			this.butOK.Click += new System.EventHandler(this.butOK_Click);
			// 
			// groupBox2
			// 
			this.groupBox2.Controls.Add(this.chkAnimations);
			this.groupBox2.FlatStyle = System.Windows.Forms.FlatStyle.Flat;
			this.groupBox2.Location = new System.Drawing.Point(16, 13);
			this.groupBox2.Margin = new System.Windows.Forms.Padding(4, 4, 4, 4);
			this.groupBox2.Name = "groupBox2";
			this.groupBox2.Padding = new System.Windows.Forms.Padding(4, 4, 4, 4);
			this.groupBox2.Size = new System.Drawing.Size(425, 71);
			this.groupBox2.TabIndex = 2;
			this.groupBox2.TabStop = false;
			this.groupBox2.Text = "Advanced";
			// 
			// chkAnimations
			// 
			this.chkAnimations.AutoSize = true;
			this.chkAnimations.FlatStyle = System.Windows.Forms.FlatStyle.Flat;
			this.chkAnimations.Location = new System.Drawing.Point(27, 33);
			this.chkAnimations.Margin = new System.Windows.Forms.Padding(4, 4, 4, 4);
			this.chkAnimations.Name = "chkAnimations";
			this.chkAnimations.Size = new System.Drawing.Size(196, 21);
			this.chkAnimations.TabIndex = 2;
			this.chkAnimations.Text = "Do not optimize animations";
			this.chkAnimations.UseVisualStyleBackColor = true;
			// 
			// ofdOpenSound
			// 
			this.ofdOpenSound.Filter = "Sound files|*.wav;*.mp3";
			// 
			// groupBox5
			// 
			this.groupBox5.Controls.Add(this.chkMorphExportTangent);
			this.groupBox5.Controls.Add(this.ckkMorphExportNormals);
			this.groupBox5.FlatStyle = System.Windows.Forms.FlatStyle.Flat;
			this.groupBox5.Location = new System.Drawing.Point(16, 92);
			this.groupBox5.Margin = new System.Windows.Forms.Padding(4, 4, 4, 4);
			this.groupBox5.Name = "groupBox5";
			this.groupBox5.Padding = new System.Windows.Forms.Padding(4, 4, 4, 4);
			this.groupBox5.Size = new System.Drawing.Size(425, 75);
			this.groupBox5.TabIndex = 7;
			this.groupBox5.TabStop = false;
			this.groupBox5.Text = "MorphTarget options";
			// 
			// chkMorphExportTangent
			// 
			this.chkMorphExportTangent.AutoSize = true;
			this.chkMorphExportTangent.FlatStyle = System.Windows.Forms.FlatStyle.Flat;
			this.chkMorphExportTangent.Location = new System.Drawing.Point(249, 37);
			this.chkMorphExportTangent.Margin = new System.Windows.Forms.Padding(4, 4, 4, 4);
			this.chkMorphExportTangent.Name = "chkMorphExportTangent";
			this.chkMorphExportTangent.Size = new System.Drawing.Size(125, 21);
			this.chkMorphExportTangent.TabIndex = 2;
			this.chkMorphExportTangent.Text = "Export tangents";
			this.chkMorphExportTangent.UseVisualStyleBackColor = true;
			// 
			// ckkMorphExportNormals
			// 
			this.ckkMorphExportNormals.AutoSize = true;
			this.ckkMorphExportNormals.Checked = true;
			this.ckkMorphExportNormals.CheckState = System.Windows.Forms.CheckState.Checked;
			this.ckkMorphExportNormals.FlatStyle = System.Windows.Forms.FlatStyle.Flat;
			this.ckkMorphExportNormals.Location = new System.Drawing.Point(28, 37);
			this.ckkMorphExportNormals.Margin = new System.Windows.Forms.Padding(4, 4, 4, 4);
			this.ckkMorphExportNormals.Name = "ckkMorphExportNormals";
			this.ckkMorphExportNormals.Size = new System.Drawing.Size(120, 21);
			this.ckkMorphExportNormals.TabIndex = 1;
			this.ckkMorphExportNormals.Text = "Export normals";
			this.ckkMorphExportNormals.UseVisualStyleBackColor = true;
			// 
			// groupBox6
			// 
			this.groupBox6.Controls.Add(this.numFlightSimFadeScale);
			this.groupBox6.Controls.Add(this.lblFlightSimFadeScale);
			this.groupBox6.FlatStyle = System.Windows.Forms.FlatStyle.Flat;
			this.groupBox6.Location = new System.Drawing.Point(16, 175);
			this.groupBox6.Margin = new System.Windows.Forms.Padding(4, 4, 4, 4);
			this.groupBox6.Name = "groupBox6";
			this.groupBox6.Padding = new System.Windows.Forms.Padding(4, 4, 4, 4);
			this.groupBox6.Size = new System.Drawing.Size(425, 75);
			this.groupBox6.TabIndex = 8;
			this.groupBox6.TabStop = false;
			this.groupBox6.Text = "FlightSim options";
			// 
			// numFlightSimFadeScale
			// 
			this.numFlightSimFadeScale.DecimalPlaces = 2;
			this.numFlightSimFadeScale.Increment = new decimal(new int[] {
            1,
            0,
            0,
            65536});
			this.numFlightSimFadeScale.Location = new System.Drawing.Point(200, 32);
			this.numFlightSimFadeScale.Margin = new System.Windows.Forms.Padding(4, 4, 4, 4);
			this.numFlightSimFadeScale.Minimum = new decimal(new int[] {
            1,
            0,
            0,
            131072});
			this.numFlightSimFadeScale.Name = "numFlightSimFadeScale";
			this.numFlightSimFadeScale.Size = new System.Drawing.Size(160, 22);
			this.numFlightSimFadeScale.TabIndex = 8;
			this.numFlightSimFadeScale.Value = new decimal(new int[] {
            1,
            0,
            0,
            0});
			// 
			// lblFlightSimFadeScale
			// 
			this.lblFlightSimFadeScale.AutoSize = true;
			this.lblFlightSimFadeScale.Location = new System.Drawing.Point(24, 34);
			this.lblFlightSimFadeScale.Margin = new System.Windows.Forms.Padding(4, 0, 4, 0);
			this.lblFlightSimFadeScale.Name = "lblFlightSimFadeScale";
			this.lblFlightSimFadeScale.Size = new System.Drawing.Size(128, 17);
			this.lblFlightSimFadeScale.TabIndex = 7;
			this.lblFlightSimFadeScale.Text = "Fade Global Scale:";
			// 
			// ScenePropertiesForm
			// 
			this.AcceptButton = this.butOK;
			this.AutoScaleDimensions = new System.Drawing.SizeF(8F, 16F);
			this.AutoScaleMode = System.Windows.Forms.AutoScaleMode.Font;
			this.BackColor = System.Drawing.SystemColors.ControlLight;
			this.BackgroundImageLayout = System.Windows.Forms.ImageLayout.Center;
			this.CancelButton = this.butCancel;
			this.ClientSize = new System.Drawing.Size(457, 353);
			this.Controls.Add(this.groupBox6);
			this.Controls.Add(this.groupBox5);
			this.Controls.Add(this.groupBox2);
			this.Controls.Add(this.butCancel);
			this.Controls.Add(this.butOK);
			this.FormBorderStyle = System.Windows.Forms.FormBorderStyle.FixedToolWindow;
			this.Margin = new System.Windows.Forms.Padding(4, 4, 4, 4);
			this.MaximumSize = new System.Drawing.Size(475, 400);
			this.Name = "ScenePropertiesForm";
			this.StartPosition = System.Windows.Forms.FormStartPosition.CenterScreen;
			this.Text = "Scene Properties";
			this.Load += new System.EventHandler(this.ScenePropertiesForm_Load);
			this.groupBox2.ResumeLayout(false);
			this.groupBox2.PerformLayout();
			this.groupBox5.ResumeLayout(false);
			this.groupBox5.PerformLayout();
			this.groupBox6.ResumeLayout(false);
			this.groupBox6.PerformLayout();
			((System.ComponentModel.ISupportInitialize)(this.numFlightSimFadeScale)).EndInit();
			this.ResumeLayout(false);

        }

        #endregion
        private System.Windows.Forms.Button butCancel;
        private System.Windows.Forms.Button butOK;
        private System.Windows.Forms.GroupBox groupBox2;
        private System.Windows.Forms.OpenFileDialog ofdOpenSound;
        private System.Windows.Forms.CheckBox chkAnimations;
        private System.Windows.Forms.GroupBox groupBox5;
        private System.Windows.Forms.CheckBox chkMorphExportTangent;
        private System.Windows.Forms.CheckBox ckkMorphExportNormals;
        private System.Windows.Forms.GroupBox groupBox6;
        private System.Windows.Forms.NumericUpDown numFlightSimFadeScale;
        private System.Windows.Forms.Label lblFlightSimFadeScale;
    }
}