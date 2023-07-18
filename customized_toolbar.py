"""

this is customized toolbar can be added to the application

"""


from PySide2.QtWidgets import QToolBar, QAction, QMessageBox, QFileDialog
from PySide2.QtGui import QIcon, QKeySequence, QKeyEvent, Qt
from PySide2.QtCore import QFile, QIODevice, QTextStream

class Toolbar(QToolBar):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.init_actions()
        self.add_actions()

    def init_actions(self):
        self.new_action = QAction(QIcon("icons/new.png"), "New", self)
        self.new_action.setShortcut(QKeySequence.New)
        self.new_action.setStatusTip("Create new file")

        self.open_action = QAction(QIcon("icons/open.png"), "Open", self)
        self.open_action.setShortcut(QKeySequence.Open)
        self.open_action.setStatusTip("Open existing file")

        self.save_action = QAction(QIcon("icons/save.png"), "Save", self)
        self.save_action.setShortcut(QKeySequence.Save)
        self.save_action.setStatusTip("Save file")

        self.save_as_action = QAction(QIcon("icons/saveAs.png"), "Save As", self)
        self.save_as_action.setShortcut(QKeySequence("Ctrl+Shift+S"))
        self.save_as_action.setStatusTip("Save file as...")

        self.exit_action = QAction(QIcon("icons/exit.png"), "Exit", self)
        self.exit_action.setShortcut(QKeySequence("Ctrl+Q"))
        self.exit_action.setStatusTip("Exit program")

    def add_actions(self):
        self.addAction(self.new_action)
        self.addAction(self.open_action)
        self.addAction(self.save_action)
        self.addAction(self.save_as_action)

    def keyPressEvent(self, event: QKeyEvent):
        if event.modifiers() == Qt.ControlModifier:
            if event.key() == Qt.Key_Plus or event.key() == Qt.Key_Equal:
                # Zoom in logic
                font = self.textarea.font()
                new_size = font.pointSizeF() + 1.0
                font.setPointSizeF(new_size)
                self.textarea.setFont(font)
            elif event.key() == Qt.Key_Minus:
                # Zoom out logic
                font = self.textarea.font()
                new_size = font.pointSizeF() - 1.0
                if new_size >= 1.0:
                    font.setPointSizeF(new_size)
                    self.textarea.setFont(font)

        super().keyPressEvent(event)

    def setCurrentFile(self, filename):
        self.currentFileName = filename
        self.textarea.document().setModified(False)
        self.setWindowModified(False)
        showName = self.currentFileName if self.currentFileName else "untitled.txt"
        self.setWindowFilePath(showName)

    def documentModified(self):
        self.setWindowModified(self.textarea.document().isModified())

    def maybeSave(self):
        if not self.textarea.document().isModified():
            return True

        ret = QMessageBox.warning(
            self, "Warning", "The document is modified.\nDo you want to save?",
            QMessageBox.Save | QMessageBox.Discard | QMessageBox.Cancel
        )

        if ret == QMessageBox.Save:
            self.Save()
        elif ret == QMessageBox.Cancel:
            return False

        return True

    def New(self):
        if self.maybeSave():
            self.textarea.clear()
            self.setCurrentFile(None)

    def Open(self):
        if self.maybeSave():
            filename, _ = QFileDialog.getOpenFileName(self, "Open")
            if filename:
                self.setCurrentFile(filename)
                file = QFile(filename)
                if file.open(QIODevice.ReadOnly | QIODevice.Text):
                    text_stream = QTextStream(file)
                    self.textarea.setPlainText(text_stream.readAll())
                    file.close()

    def Save(self):
        if not self.currentFileName:
            self.SaveAs()
        else:
            file = QFile(self.currentFileName)
            if file.open(QIODevice.WriteOnly | QIODevice.Text):
                text_stream = QTextStream(file)
                text_stream << self.textarea.toPlainText()
                file.close()
                self.textarea.document().setModified(False)
                self.setWindowModified(False)

    def SaveAs(self):
        filename, _ = QFileDialog.getSaveFileName(self, "Save As")
        if filename:
            self.currentFileName = filename
            self.Save()

    def Exit(self):
        if self.maybeSave():
            self.close()
