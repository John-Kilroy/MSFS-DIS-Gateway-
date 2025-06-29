# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'settingsWindow.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *


class Ui_settingsWindow(object):
    def setupUi(self, settingsWindow):
        if not settingsWindow.objectName():
            settingsWindow.setObjectName(u"settingsWindow")
        settingsWindow.resize(780, 430)
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(settingsWindow.sizePolicy().hasHeightForWidth())
        settingsWindow.setSizePolicy(sizePolicy)
        settingsWindow.setMinimumSize(QSize(780, 430))
        self.verticalLayout_2 = QVBoxLayout(settingsWindow)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.horizontalLayout_8 = QHBoxLayout()
        self.horizontalLayout_8.setObjectName(u"horizontalLayout_8")
        self.label_3 = QLabel(settingsWindow)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.horizontalLayout_8.addWidget(self.label_3)

        self.comboOptionPreset = QComboBox(settingsWindow)
        self.comboOptionPreset.setObjectName(u"comboOptionPreset")
        sizePolicy1 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        sizePolicy1.setHorizontalStretch(1)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.comboOptionPreset.sizePolicy().hasHeightForWidth())
        self.comboOptionPreset.setSizePolicy(sizePolicy1)
        self.comboOptionPreset.setMinimumSize(QSize(570, 0))
        self.comboOptionPreset.setEditable(True)
        self.comboOptionPreset.setInsertPolicy(QComboBox.InsertAtCurrent)

        self.horizontalLayout_8.addWidget(self.comboOptionPreset)

        self.line = QFrame(settingsWindow)
        self.line.setObjectName(u"line")
        self.line.setFrameShape(QFrame.VLine)
        self.line.setFrameShadow(QFrame.Sunken)

        self.horizontalLayout_8.addWidget(self.line)

        self.btnAddOptionPreset = QToolButton(settingsWindow)
        self.btnAddOptionPreset.setObjectName(u"btnAddOptionPreset")
        self.btnAddOptionPreset.setMinimumSize(QSize(26, 0))

        self.horizontalLayout_8.addWidget(self.btnAddOptionPreset)

        self.btnRemoveOptionPreset = QToolButton(settingsWindow)
        self.btnRemoveOptionPreset.setObjectName(u"btnRemoveOptionPreset")
        self.btnRemoveOptionPreset.setMinimumSize(QSize(26, 0))

        self.horizontalLayout_8.addWidget(self.btnRemoveOptionPreset)


        self.verticalLayout_2.addLayout(self.horizontalLayout_8)

        self.tabWidget = QTabWidget(settingsWindow)
        self.tabWidget.setObjectName(u"tabWidget")
        self.tabSettings = QWidget()
        self.tabSettings.setObjectName(u"tabSettings")
        self.verticalLayout_7 = QVBoxLayout(self.tabSettings)
        self.verticalLayout_7.setObjectName(u"verticalLayout_7")
        self.verticalLayout_7.setContentsMargins(7, 7, 7, 7)
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.cbAutosave = QCheckBox(self.tabSettings)
        self.cbAutosave.setObjectName(u"cbAutosave")

        self.horizontalLayout.addWidget(self.cbAutosave)

        self.cbExportHidden = QCheckBox(self.tabSettings)
        self.cbExportHidden.setObjectName(u"cbExportHidden")
        self.cbExportHidden.setChecked(True)

        self.horizontalLayout.addWidget(self.cbExportHidden)

        self.cbSelectionAsSubmodel = QCheckBox(self.tabSettings)
        self.cbSelectionAsSubmodel.setObjectName(u"cbSelectionAsSubmodel")
        sizePolicy2 = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.cbSelectionAsSubmodel.sizePolicy().hasHeightForWidth())
        self.cbSelectionAsSubmodel.setSizePolicy(sizePolicy2)

        self.horizontalLayout.addWidget(self.cbSelectionAsSubmodel)


        self.verticalLayout_7.addLayout(self.horizontalLayout)

        self.horizontalLayout_6 = QHBoxLayout()
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.glGroupBox = QGridLayout()
        self.glGroupBox.setObjectName(u"glGroupBox")
        self.gbExtensions = QGroupBox(self.tabSettings)
        self.gbExtensions.setObjectName(u"gbExtensions")
        self.gbExtensions.setMaximumSize(QSize(300, 100))
        self.verticalLayout_5 = QVBoxLayout(self.gbExtensions)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.horizontalLayout_4.setContentsMargins(-1, 7, -1, 7)
        self.cbAsoboUniqueID = QCheckBox(self.gbExtensions)
        self.cbAsoboUniqueID.setObjectName(u"cbAsoboUniqueID")
        self.cbAsoboUniqueID.setEnabled(True)
        self.cbAsoboUniqueID.setChecked(True)

        self.horizontalLayout_4.addWidget(self.cbAsoboUniqueID)


        self.verticalLayout_5.addLayout(self.horizontalLayout_4)

        self.verticalSpacer_2 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_5.addItem(self.verticalSpacer_2)


        self.glGroupBox.addWidget(self.gbExtensions, 1, 0, 1, 1)

        self.gbObjects = QGroupBox(self.tabSettings)
        self.gbObjects.setObjectName(u"gbObjects")
        self.gbObjects.setMinimumSize(QSize(300, 100))
        self.verticalLayout_3 = QVBoxLayout(self.gbObjects)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.cbExportMaterials = QCheckBox(self.gbObjects)
        self.cbExportMaterials.setObjectName(u"cbExportMaterials")
        self.cbExportMaterials.setChecked(True)

        self.horizontalLayout_2.addWidget(self.cbExportMaterials)


        self.verticalLayout_3.addLayout(self.horizontalLayout_2)

        self.line_3 = QFrame(self.gbObjects)
        self.line_3.setObjectName(u"line_3")
        self.line_3.setFrameShape(QFrame.HLine)
        self.line_3.setFrameShadow(QFrame.Sunken)

        self.verticalLayout_3.addWidget(self.line_3)

        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.cbRemoveLODPrefix = QCheckBox(self.gbObjects)
        self.cbRemoveLODPrefix.setObjectName(u"cbRemoveLODPrefix")
        self.cbRemoveLODPrefix.setChecked(True)

        self.horizontalLayout_5.addWidget(self.cbRemoveLODPrefix)


        self.verticalLayout_3.addLayout(self.horizontalLayout_5)

        self.line_2 = QFrame(self.gbObjects)
        self.line_2.setObjectName(u"line_2")
        self.line_2.setFrameShape(QFrame.HLine)
        self.line_2.setFrameShadow(QFrame.Sunken)

        self.verticalLayout_3.addWidget(self.line_2)

        self.horizontalLayout_10 = QHBoxLayout()
        self.horizontalLayout_10.setObjectName(u"horizontalLayout_10")
        self.horizontalLayout_10.setContentsMargins(-1, -1, -1, 0)
        self.cbFlattenNodes = QCheckBox(self.gbObjects)
        self.cbFlattenNodes.setObjectName(u"cbFlattenNodes")
        self.cbFlattenNodes.setChecked(True)

        self.horizontalLayout_10.addWidget(self.cbFlattenNodes)

        self.cbKeepInstances = QCheckBox(self.gbObjects)
        self.cbKeepInstances.setObjectName(u"cbKeepInstances")

        self.horizontalLayout_10.addWidget(self.cbKeepInstances)


        self.verticalLayout_3.addLayout(self.horizontalLayout_10)


        self.glGroupBox.addWidget(self.gbObjects, 0, 0, 1, 1)


        self.horizontalLayout_6.addLayout(self.glGroupBox)

        self.glGroupBox1 = QGridLayout()
        self.glGroupBox1.setObjectName(u"glGroupBox1")
        self.gbUsePreExport = QGroupBox(self.tabSettings)
        self.gbUsePreExport.setObjectName(u"gbUsePreExport")
        self.gbUsePreExport.setCheckable(True)
        self.gbUsePreExport.setChecked(False)
        self.verticalLayout_4 = QVBoxLayout(self.gbUsePreExport)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.cbMergeContainers = QCheckBox(self.gbUsePreExport)
        self.cbMergeContainers.setObjectName(u"cbMergeContainers")

        self.verticalLayout_4.addWidget(self.cbMergeContainers)

        self.cbApplyPreprocessToScene = QCheckBox(self.gbUsePreExport)
        self.cbApplyPreprocessToScene.setObjectName(u"cbApplyPreprocessToScene")

        self.verticalLayout_4.addWidget(self.cbApplyPreprocessToScene)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.label = QLabel(self.gbUsePreExport)
        self.label.setObjectName(u"label")

        self.horizontalLayout_3.addWidget(self.label)

        self.comboBakeAnimationOptions = QComboBox(self.gbUsePreExport)
        self.comboBakeAnimationOptions.addItem("")
        self.comboBakeAnimationOptions.addItem("")
        self.comboBakeAnimationOptions.addItem("")
        self.comboBakeAnimationOptions.setObjectName(u"comboBakeAnimationOptions")
        self.comboBakeAnimationOptions.setMinimumSize(QSize(140, 0))

        self.horizontalLayout_3.addWidget(self.comboBakeAnimationOptions)


        self.verticalLayout_4.addLayout(self.horizontalLayout_3)


        self.glGroupBox1.addWidget(self.gbUsePreExport, 3, 0, 1, 1)

        self.gbTextures = QGroupBox(self.tabSettings)
        self.gbTextures.setObjectName(u"gbTextures")
        sizePolicy3 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.MinimumExpanding)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.gbTextures.sizePolicy().hasHeightForWidth())
        self.gbTextures.setSizePolicy(sizePolicy3)
        self.gbTextures.setCheckable(True)
        self.gbTextures.setChecked(True)
        self.horizontalLayout_9 = QHBoxLayout(self.gbTextures)
        self.horizontalLayout_9.setObjectName(u"horizontalLayout_9")
        self.horizontalLayout_9.setContentsMargins(7, 7, 7, 7)
        self.lbTexturePath = QLabel(self.gbTextures)
        self.lbTexturePath.setObjectName(u"lbTexturePath")
        self.lbTexturePath.setEnabled(True)

        self.horizontalLayout_9.addWidget(self.lbTexturePath)

        self.lineTexturePath = QLineEdit(self.gbTextures)
        self.lineTexturePath.setObjectName(u"lineTexturePath")
        self.lineTexturePath.setEnabled(True)

        self.horizontalLayout_9.addWidget(self.lineTexturePath)

        self.btnBrowseTexture = QToolButton(self.gbTextures)
        self.btnBrowseTexture.setObjectName(u"btnBrowseTexture")
        self.btnBrowseTexture.setEnabled(True)
        self.btnBrowseTexture.setMinimumSize(QSize(26, 0))

        self.horizontalLayout_9.addWidget(self.btnBrowseTexture)


        self.glGroupBox1.addWidget(self.gbTextures, 2, 0, 1, 1)

        self.gbAnimations = QGroupBox(self.tabSettings)
        self.gbAnimations.setObjectName(u"gbAnimations")
        self.verticalLayout = QVBoxLayout(self.gbAnimations)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.comboAnimationExport = QComboBox(self.gbAnimations)
        self.comboAnimationExport.addItem("")
        self.comboAnimationExport.addItem("")
        self.comboAnimationExport.addItem("")
        self.comboAnimationExport.setObjectName(u"comboAnimationExport")

        self.verticalLayout.addWidget(self.comboAnimationExport)


        self.glGroupBox1.addWidget(self.gbAnimations, 1, 0, 1, 1)


        self.horizontalLayout_6.addLayout(self.glGroupBox1)


        self.verticalLayout_7.addLayout(self.horizontalLayout_6)

        self.tabWidget.addTab(self.tabSettings, "")

        self.verticalLayout_2.addWidget(self.tabWidget)

        self.horizontalLayout_7 = QHBoxLayout()
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.horizontalSpacer_7 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_7.addItem(self.horizontalSpacer_7)

        self.btnSave = QPushButton(settingsWindow)
        self.btnSave.setObjectName(u"btnSave")

        self.horizontalLayout_7.addWidget(self.btnSave)

        self.btnCancel = QPushButton(settingsWindow)
        self.btnCancel.setObjectName(u"btnCancel")

        self.horizontalLayout_7.addWidget(self.btnCancel)


        self.verticalLayout_2.addLayout(self.horizontalLayout_7)


        self.retranslateUi(settingsWindow)

        self.tabWidget.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(settingsWindow)
    # setupUi

    def retranslateUi(self, settingsWindow):
        settingsWindow.setWindowTitle(QCoreApplication.translate("settingsWindow", u"Export Options", None))
        self.label_3.setText(QCoreApplication.translate("settingsWindow", u"Options preset:", None))
#if QT_CONFIG(tooltip)
        self.comboOptionPreset.setToolTip(QCoreApplication.translate("settingsWindow", u"Set the \"Option Preset\" which will receive the options applied to.", None))
#endif // QT_CONFIG(tooltip)
        self.comboOptionPreset.setCurrentText("")
#if QT_CONFIG(tooltip)
        self.btnAddOptionPreset.setToolTip(QCoreApplication.translate("settingsWindow", u"Add new option preset", None))
#endif // QT_CONFIG(tooltip)
        self.btnAddOptionPreset.setText(QCoreApplication.translate("settingsWindow", u"+", None))
#if QT_CONFIG(tooltip)
        self.btnRemoveOptionPreset.setToolTip(QCoreApplication.translate("settingsWindow", u"Remove selected option preset", None))
#endif // QT_CONFIG(tooltip)
        self.btnRemoveOptionPreset.setText(QCoreApplication.translate("settingsWindow", u"-", None))
#if QT_CONFIG(tooltip)
        self.cbAutosave.setToolTip(QCoreApplication.translate("settingsWindow", u"When you export, it will automatically save the scene.", None))
#endif // QT_CONFIG(tooltip)
        self.cbAutosave.setText(QCoreApplication.translate("settingsWindow", u"Autosave 3ds Max file", None))
#if QT_CONFIG(tooltip)
        self.cbExportHidden.setToolTip(QCoreApplication.translate("settingsWindow", u"If you have hidden object(s) in the layer(s) that should be exported they will be exported anyway.", None))
#endif // QT_CONFIG(tooltip)
        self.cbExportHidden.setText(QCoreApplication.translate("settingsWindow", u"Export hidden objects", None))
#if QT_CONFIG(tooltip)
        self.cbSelectionAsSubmodel.setToolTip(QCoreApplication.translate("settingsWindow", u"This option is to be set if you are using the merge model methods, without it, you will not be able to merge any model in the game. Make sure to have all your hierarchy under the same dummy object named \"Root\".", None))
#endif // QT_CONFIG(tooltip)
        self.cbSelectionAsSubmodel.setText(QCoreApplication.translate("settingsWindow", u"Export as submodel", None))
        self.gbExtensions.setTitle(QCoreApplication.translate("settingsWindow", u"MSFS2024 extensions", None))
#if QT_CONFIG(tooltip)
        self.cbAsoboUniqueID.setToolTip(QCoreApplication.translate("settingsWindow", u"The GLTF format is calling node(s), several node(s) with the same node name will cause issue. This option will prevent this kind of blocker.", None))
#endif // QT_CONFIG(tooltip)
        self.cbAsoboUniqueID.setText(QCoreApplication.translate("settingsWindow", u"ASOBO_uniqueID", None))
        self.gbObjects.setTitle(QCoreApplication.translate("settingsWindow", u"Objects", None))
        self.cbExportMaterials.setText(QCoreApplication.translate("settingsWindow", u"Export Materials", None))
#if QT_CONFIG(tooltip)
        self.cbRemoveLODPrefix.setToolTip(QCoreApplication.translate("settingsWindow", u"It cleans the names of all the meshes so this way if we refer in the xml code for example to animate the push_button_01 it will work on all the LODS by removing the xX_.", None))
#endif // QT_CONFIG(tooltip)
        self.cbRemoveLODPrefix.setText(QCoreApplication.translate("settingsWindow", u"Remove LOD prefix", None))
#if QT_CONFIG(tooltip)
        self.cbFlattenNodes.setToolTip(QCoreApplication.translate("settingsWindow", u"Collapse hierarchy during export.\n"
"Note: gizmos and lights will be kept as independant nodes.", None))
#endif // QT_CONFIG(tooltip)
        self.cbFlattenNodes.setText(QCoreApplication.translate("settingsWindow", u"Flatten nodes", None))
#if QT_CONFIG(tooltip)
        self.cbKeepInstances.setToolTip(QCoreApplication.translate("settingsWindow", u"If you have instances in the max file(s), these instances will be kept in the GLTF (it can be important for performance optimization in the game). Be cautious, too many instances can also have a negative impact on performances.", None))
#endif // QT_CONFIG(tooltip)
        self.cbKeepInstances.setText(QCoreApplication.translate("settingsWindow", u"Keep instances", None))
#if QT_CONFIG(tooltip)
        self.gbUsePreExport.setToolTip(QCoreApplication.translate("settingsWindow", u"Apply pre-export settings", None))
#endif // QT_CONFIG(tooltip)
        self.gbUsePreExport.setTitle(QCoreApplication.translate("settingsWindow", u"Use pre-export process", None))
#if QT_CONFIG(tooltip)
        self.cbMergeContainers.setToolTip(QCoreApplication.translate("settingsWindow", u"For all the elements that are shared between several max files, the best example is the containers of instruments that will be merged before the export", None))
#endif // QT_CONFIG(tooltip)
        self.cbMergeContainers.setText(QCoreApplication.translate("settingsWindow", u"Merge containers and XRef", None))
#if QT_CONFIG(tooltip)
        self.cbApplyPreprocessToScene.setToolTip(QCoreApplication.translate("settingsWindow", u"If you want the options above to be permanent no way back from there. It may break your scene if you don\u2019t pay attention to this option", None))
#endif // QT_CONFIG(tooltip)
        self.cbApplyPreprocessToScene.setText(QCoreApplication.translate("settingsWindow", u"Apply preprocess to scene", None))
#if QT_CONFIG(tooltip)
        self.label.setToolTip("")
#endif // QT_CONFIG(tooltip)
        self.label.setText(QCoreApplication.translate("settingsWindow", u"Bake animation options:", None))
        self.comboBakeAnimationOptions.setItemText(0, QCoreApplication.translate("settingsWindow", u"Dont bake animations", None))
        self.comboBakeAnimationOptions.setItemText(1, QCoreApplication.translate("settingsWindow", u"Bake all animations", None))
        self.comboBakeAnimationOptions.setItemText(2, QCoreApplication.translate("settingsWindow", u"Selective bake", None))

#if QT_CONFIG(tooltip)
        self.comboBakeAnimationOptions.setToolTip(QCoreApplication.translate("settingsWindow", u"To avoid some animation issues, the animation will be baked on every key of the timeline. Also, some of the meshes with constraints will work in the game only if their animation has been baked.", None))
#endif // QT_CONFIG(tooltip)
        self.comboBakeAnimationOptions.setCurrentText(QCoreApplication.translate("settingsWindow", u"Dont bake animations", None))
        self.gbTextures.setTitle(QCoreApplication.translate("settingsWindow", u"Textures", None))
        self.lbTexturePath.setText(QCoreApplication.translate("settingsWindow", u"Texture path", None))
#if QT_CONFIG(tooltip)
        self.lineTexturePath.setToolTip(QCoreApplication.translate("settingsWindow", u"Folder where to export the textures (if empty will be exported next to gltf)", None))
#endif // QT_CONFIG(tooltip)
        self.btnBrowseTexture.setText(QCoreApplication.translate("settingsWindow", u"...", None))
        self.gbAnimations.setTitle(QCoreApplication.translate("settingsWindow", u"Animations", None))
        self.comboAnimationExport.setItemText(0, QCoreApplication.translate("settingsWindow", u"Export meshes and animations", None))
        self.comboAnimationExport.setItemText(1, QCoreApplication.translate("settingsWindow", u"Export meshes only (no animation)", None))
        self.comboAnimationExport.setItemText(2, QCoreApplication.translate("settingsWindow", u"Export animations only (no mesh)", None))

#if QT_CONFIG(tooltip)
        self.comboAnimationExport.setToolTip(QCoreApplication.translate("settingsWindow", u"Choose the export type for the animation(s)", None))
#endif // QT_CONFIG(tooltip)
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabSettings), QCoreApplication.translate("settingsWindow", u"Settings", None))
#if QT_CONFIG(tooltip)
        self.btnSave.setToolTip(QCoreApplication.translate("settingsWindow", u"Save settings for the selected \"Option Preset\"", None))
#endif // QT_CONFIG(tooltip)
        self.btnSave.setText(QCoreApplication.translate("settingsWindow", u"Save", None))
        self.btnCancel.setText(QCoreApplication.translate("settingsWindow", u"Exit", None))
    # retranslateUi

