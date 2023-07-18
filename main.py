import sys
import math
import re
import keyboard
from matplotlib.backend_bases import KeyEvent
import matplotlib.pyplot as plt
from PySide2.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, \
    QPushButton, QMessageBox
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from PySide2.QtCore import Qt, QFile
from PySide2.QtGui import QIcon
from function_plotter import FunctionPlotter


# Running the application
if __name__ == '__main__':  # if the file is run directly from the command line then the __name__ variable will be set to __main__
    app = QApplication(sys.argv)

    window = FunctionPlotter()
    # Load and apply the style sheet
    style_file = QFile("style.qss")
    if style_file.open(QFile.ReadOnly | QFile.Text):
        style_sheet = style_file.readAll().data().decode()
        app.setStyleSheet(style_sheet)
    window.show()

    sys.exit(app.exec_())  # running the application using exec_() not exec()
