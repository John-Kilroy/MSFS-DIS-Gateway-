import os

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *

from maxsdk_2024 import uiTheme as uiColors

class CustomFileDialog(QFileDialog):
    def __init__(self, parent, caption, dir, filter, fileMode=QFileDialog.FileMode.AnyFile, acceptMode=QFileDialog.AcceptOpen.AcceptOpen, confirmOverwrite=True):
        QFileDialog.__init__(self, parent, caption, dir, filter)
        self.setOption(QFileDialog.DontConfirmOverwrite, not confirmOverwrite)
        self.setViewMode(QFileDialog.ViewMode.List)
        self.setFileMode(fileMode)
        self.setAcceptMode(acceptMode)

        self.fileList = list()

        if not self.exec():
            return

        filenames = self.selectedFiles()
        if filenames:
            self.fileList.extend(filenames)

class ScrollMessageBox(QMessageBox):
    def __init__(self, text, title="", *args, **kwargs):
        lineCount = text.count("\n")
        print(lineCount)
        self.minHeight = 150 + lineCount * 10
        if self.minHeight > 400:
            self.minHeight = 400
        QMessageBox.__init__(self, *args, **kwargs)
        scroll = QScrollArea(self)
        scroll.setWidgetResizable(True)
        self.content = QWidget()
        self.setWindowTitle(title)
        scroll.setWidget(self.content)
        lay = QVBoxLayout(self.content)
        self.content.setSizePolicy(
            QSizePolicy.Expanding, QSizePolicy.Expanding)
        txt = QLabel(text, self)
        txt.setWordWrap(True)
        lay.addWidget(txt)
        self.layout().addWidget(scroll, 0, 0, 1, self.layout().columnCount())
        self.setSizeGripEnabled(True)

    def event(self, e):
        result = QMessageBox.event(self, e)
        if(self.minHeight is not None):
            self.setMinimumHeight(self.minHeight)
        self.setMaximumHeight(16777215)
        self.setMinimumWidth(400)
        self.setMaximumWidth(16777215)
        self.setSizePolicy(QSizePolicy.MinimumExpanding,
                           QSizePolicy.MinimumExpanding)
        return result


def truncateStringFromLeft(string, maxLength):
    """Truncate a string from the left side until the string's length is less than maxLength
    """
    stringLen = len(string)
    truncString = string[max(stringLen-maxLength, 0):stringLen]
    if (stringLen > maxLength):
        truncString = "..." + truncString
    return truncString

def validateFloatLineEdit(x):
    """ Turn a string into a float. Will replace comma by full stop if needed
    """
    try:
        return float(x)
    except:
        try:
            # turns comma into period and try again
            return float(x.replace(",", "."))
        except:
            print("Invalid float entered")
    return None

#region BUTTONS
def setButtonBackgroundColor(btn, color):
    btnPalette = btn.palette()
    btnPalette.setBrush(QPalette.Button, color)
    btn.setPalette(btnPalette)

def setButtonTristateWithColors(btn, tristate):
    if tristate:
        btn.setChecked(False)
        setButtonBackgroundColor(btn, uiColors.colorButtonTristateUndetermined)
    else:
        setButtonBackgroundColor(btn, uiColors.colorButtonTristateDefault)
#endregion

#region CHECKBOX
def createCheckBox(qtWidget, x=14, y=5, w=17, h=17):
    """
        Adds a checkbox to a widget and returns a reference to it
        x=0 y=0 represent the top left corner of the widget
    """
    headerGeom = qtWidget.geometry()
    frameTopLeft = headerGeom.topLeft()
    fx = frameTopLeft.x()
    fy = frameTopLeft.y()
    posX = x + fx
    posY = y + fy
    topLeft = QPoint(posX, posY)
    botRight = QPoint(posX + w, posY + h)
    geom = QRect(topLeft, botRight)
    checkBox = QCheckBox(qtWidget)
    checkBox.setGeometry(geom)
    return checkBox
#endregion

#region FILE DIALOG
def openSaveFileNameDialog(parent=None, caption="", _dir="", _filter="", forcedExtension=".gltf"):
    """Opens a Save File dialog and returns the chosen path
    """
    dialog = QFileDialog(parent, caption, _dir, _filter)
    dialog.setDirectory(_dir)
    if dialog.exec_() == 1:
        filePath = dialog.selectedFiles()
        if len(filePath) > 0:
            ext = os.path.splitext(filePath[0])
            if forcedExtension is not None:
                if (ext[1] != forcedExtension):
                    filePath[0] = ext[0] + forcedExtension
            if (filePath[0] != ""):
                return filePath[0]
    return None

def openSaveFileNamesDialog(parent=None, caption="", _dir="", _filter=""):
    """Opens a Save File dialog and returns the chosen path
    """
    dialog = QFileDialog.getOpenFileNames(parent, caption, _dir, _filter)
    if len(dialog[0]) > 0:
        return dialog[0]
    
    return None

def openSaveFolderPathDialog(_caption ="Choose a folder", _dir ="" ):
    dialog = QFileDialog.getExistingDirectory(caption = _caption, dir = _dir, options=QFileDialog.ShowDirsOnly)
    return dialog

def newFile(_caption="Add file name", _dir="", _filter=""):
    fileName = QFileDialog.getSaveFileName(caption=_caption, dir=_dir, filter=_filter)
    if fileName:
        return (fileName[0])

def openCustomFileNamesDialog(parent=None, caption="", _dir="", _filter="", fileMode=QFileDialog.FileMode.AnyFile, acceptMode=QFileDialog.AcceptOpen.AcceptSave, confirmOverwrite=True):
    if fileMode == None:
        fileMode = QFileDialog.FileMode.ExistingFiles
    filenames = CustomFileDialog(parent, caption, _dir, _filter, fileMode, acceptMode, confirmOverwrite)
    if (len(filenames.fileList) > 0):
        return filenames.fileList
    return None
#endregion

#region POPUPS
def getNewMessageBox(text, title=""):
    """Creates a message box and returns a reference to it
    """
    msgBox = QMessageBox()
    msgBox.setWindowTitle(title)
    msgBox.setMaximumHeight(500) #Is this working?
    msgBox.setText(text)
    flagsOnTop = Qt.WindowFlags(Qt.WindowStaysOnTopHint)
    msgBox.setWindowFlags(flagsOnTop)
    return msgBox

def popup(text, title=""):
    """Opens a message popup
    """
    msgBox = getNewMessageBox(text, title)
    msgBox.exec_()

def popup_detail(text, title="", detail=""):
    """Opens a message popup with a detail rollout
    """
    msgBox = getNewMessageBox(text, title)
    msgBox.setDetailedText(detail)
    msgBox.exec_()

def popup_scroll(text, title=""):
    """Opens a message popup with a scrollbar
    """
    msgBox = ScrollMessageBox(text=text, title=title)
    msgBox.exec_()

def popup_Yes_No(text, title=""):
    """Opens a Yes or No message popup.
    Returns True if yes is pressed"""
    msgBox = getNewMessageBox(text, title)
    buttons = QMessageBox.Yes | QMessageBox.No
    msgBox.setStandardButtons(buttons)
    output = msgBox.exec_()
    if (output == QMessageBox.Yes):
        return True
    else:
        return False

def popup_Yes_Cancel(text, title=""):
    """Opens a Yes or Cancel message popup.
    Returns True if yes is pressed"""
    msgBox = getNewMessageBox(text, title)
    buttons = QMessageBox.Yes | QMessageBox.Cancel
    msgBox.setStandardButtons(buttons)
    output = msgBox.exec_()
    if (output == QMessageBox.Yes):
        return True
    else:
        return False

def popup_Yes_No_Cancel(text, title=""):
    """Opens a Yes, No or Cancel message popup.
    Returns 0 for No, 1 for Yes and 2 for Cancel"""
    msgBox = getNewMessageBox(text, title)
    buttons = QMessageBox.Yes | QMessageBox.No |QMessageBox.Cancel
    msgBox.setStandardButtons(buttons)
    output = msgBox.exec_()
    return output

def popup_Yes_YesToAll_No(text, title=""):
    """Opens a Yes YesToAll and No message popup
    Returns 2 for yes, 1 for YesToAll and 0 for No
    """
    msgBox = getNewMessageBox(text, title)
    buttons = QMessageBox.Yes | QMessageBox.YesToAll | QMessageBox.No
    msgBox.setStandardButtons(buttons)
    output = msgBox.exec_()
    return output

def popup_Yes_YesToAll_No_NoToAll(text, title=""):
    """Opens a Yes, YesToAll, No and NoToAll message popup.
    Returns 3 for Yes, 2 for YesToAll, 1 for No and 0 for NoToAll
    """
    msgBox = getNewMessageBox(text, title)
    buttons = QMessageBox.Yes | QMessageBox.YesToAll | QMessageBox.No | QMessageBox.NoToAll
    msgBox.setStandardButtons(buttons)
    output = msgBox.exec_()
    return output
#endregion

#region PROGRESS BAR
def initProgressBar(progressBar = None, labelProgressBar = None, maxRange = 1, actionTitle = "Processing"):
    if progressBar is not None:
        progressBar.setRange(0, maxRange)
        progressBar.setValue(0)
        progressBar.setEnabled(True)
    if labelProgressBar is not None:
        labelProgressBar.setText(actionTitle + ":")
        labelProgressBar.setEnabled(True)

def resetProgressBar(progressBar = None, labelProgressBar = None):
    if progressBar is not None:
        progressBar.setRange(0, 1)
        progressBar.setValue(0)
        progressBar.setEnabled(False)
    if labelProgressBar is not None:
        labelProgressBar.setText("(Doing nothing):")
        labelProgressBar.setEnabled(False)
#endregion