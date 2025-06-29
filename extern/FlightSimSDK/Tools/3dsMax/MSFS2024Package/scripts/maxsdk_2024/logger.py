from PySide2 import QtWidgets, QtCore, QtGui
import logging
from maxsdk_2024 import uiTheme as uiColors
from maxsdk_2024 import sharedGlobals

class QSignaler(QtCore.QObject):
    logRecord = QtCore.Signal(object)

class SignalHandler(logging.Handler):
    """Logging handler to emit QtSignal with log record text."""

    def __init__(self, *args, **kwargs):
        super(SignalHandler, self).__init__(*args, **kwargs)
        self.emitter = QSignaler()

    def emit(self, logRecord):
        self.emitter.logRecord.emit(logRecord)
        QtWidgets.QApplication.processEvents()

class LoggerWidget(QtWidgets.QWidget):
    def __init__(self, parent = None):
        super(LoggerWidget, self).__init__(parent)

        self.autoClear = True

        # UI common
        # horizontal spacer
        self.horizontalSpacer = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)

        layout = QtWidgets.QVBoxLayout(self)

        # text_browser
        self.text_browser = QtWidgets.QTextBrowser()
        self.text_browser.setStyleSheet("QTextBrowser { background-color: rgb(56, 56, 56) }") #Background color is brighter than the rest by default, let's darken it a bit for errors to "pop" :)
        self.font = QtGui.QFont()
        self.text_browser.setFontPointSize(8)
        layout.addWidget(self.text_browser)

        self.blockFmt = QtGui.QTextBlockFormat()
        self.blockFmt.setLineHeight(150, QtGui.QTextBlockFormat.ProportionalHeight)
        self.updateTextCursor()
        
        # bottom section
        self.bottomSection = QtWidgets.QHBoxLayout()
        layout.addLayout(self.bottomSection)

        # left section
        self.bottomSectionLeft = QtWidgets.QHBoxLayout()
        self.bottomSection.addLayout(self.bottomSectionLeft)

        # spacer
        self.bottomSectionLeft.addSpacerItem(self.horizontalSpacer)

        # center section
        self.bottomSectionCenter = QtWidgets.QHBoxLayout()
        self.bottomSection.addLayout(self.bottomSectionCenter)

        # btn clear log
        self.btn_clear = QtWidgets.QPushButton("Clear Log")
        self.btn_clear.clicked.connect(self.clearLog)
        self.btn_clear.setMinimumSize(200, 25)
        self.bottomSectionCenter.addWidget(self.btn_clear)
        
        # right section
        # self.bottomSectionRight = QtWidgets.QHBoxLayout()
        # self.bottomSection.addLayout(self.bottomSectionRight)

        # auto clear option
        # self.cbAutoClear = QtWidgets.QCheckBox("Clear on new export")
        # self.cbAutoClear.setChecked(True)
        # self.cbAutoClear.stateChanged.connect(self.updateAutoClearOption)
        # self.bottomSectionRight.addWidget(self.cbAutoClear)

        # spacer
        # self.bottomSectionRight.addSpacerItem(self.horizontalSpacer)

        # # btn cancel export
        # self.btn_cancelExport = QtWidgets.QPushButton("CANCEL EXPORT")
        # self.btn_cancelExport.setToolTip("Attempt to cancel export. This cannot interrupt a single process, but will stop any remaining operations after current one has finished")
        # self.btn_cancelExport.clicked.connect(self.cancelExport)
        # self.btn_cancelExport.setMinimumSize(200, 25)
        # self.bottomSectionRight.addWidget(self.btn_cancelExport)
        # self.btn_cancelExport.setEnabled(False)

    def adjustLoggerLineHeight(self, percentage = 150):
        self.document = self.text_browser.document()
        self.textCursor = QtGui.QTextCursor(self.document)
        self.textStyle = QtGui.QTextBlockFormat(self.document.firstBlock().blockFormat())
        self.blockFmt.setLineHeight(150, QtGui.QTextBlockFormat.ProportionalHeight)
        self.textCursor.setBlockFormat(self.textStyle)
        self.text_browser.setTextCursor(self.textCursor)

    # def updateAutoClearOption(self):
    #     self.autoClearOnExport = self.cbAutoClear.isChecked()

    def updateTextCursor(self):
        textCursor = self.text_browser.textCursor()
        textCursor.clearSelection()
        textCursor.select(QtGui.QTextCursor.Document)
        textCursor.mergeBlockFormat(self.blockFmt)

    def clearLog(self):
        self.text_browser.clear()
        self.updateTextCursor()
        

    def cancelExport(self):
        sharedGlobals.G_ME_cancelExport = True

    # def enableCancelExportBtn(self):
    #     self.btn_cancelExport.setEnabled(True)

    # def disableCancelExportBtn(self):
    #     self.btn_cancelExport.setEnabled(False)

    def appendLogRecord(self, logRecord):
        l = logRecord.levelno
        if l >= logging.ERROR: #CRITICAL/#ERROR
            self.text_browser.setTextColor(uiColors.colorError)
        elif l==logging.WARNING: #WARNING
            self.text_browser.setTextColor(uiColors.colorWarning)
        elif l == logging.INFO:  #INFO
            self.text_browser.setTextColor(uiColors.colorDullWhite) # No full white here, these are just infos and should not pop out
        else: #DEBUG or anything unhandled
            self.text_browser.setTextColor(uiColors.colorBlack)
        self.text_browser.append(logRecord.getMessage())
        