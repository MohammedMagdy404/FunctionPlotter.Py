import sys
import math
import re
import keyboard
from matplotlib.backend_bases import KeyEvent
import matplotlib.pyplot as plt
from PySide2.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, \
    QPushButton, QMessageBox, QSizePolicy, QAction
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from PySide2.QtCore import Qt, QSize
from PySide2.QtGui import QIcon, QPixmap, QColor

# Defining FunctionPlotter class inheriting from QMainWindow


class FunctionPlotter(QMainWindow):
    # defining the constructor and declaring self explicitly.
    def __init__(self):
        # calling the constructor of the parent class.
        super().__init__()

        # Set window properties
        self.setWindowTitle("Plot it")
        self.setWindowIcon(QIcon("icons/icon.png"))
        self.resize(1000, 700)

        # Create central widget and set it as central widget
        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)

        # Set layout
        # QVBoxLayout is a vertical layout widget that is used to arrange child widgets vertically in a single column.
        self.layout = QVBoxLayout(self.central_widget)
        self.layout_for_inputs = QHBoxLayout()

        # Create input layout for function input
        self.input_layout_fun = QHBoxLayout()
        self.function_label = QLabel("F(x) = ")
        self.function_input = QLineEdit()
        self.function_input.setPlaceholderText("Enter a function")
        # Adding function label and input to the input layout for function input
        self.input_layout_fun.addWidget(self.function_label)
        self.input_layout_fun.addWidget(self.function_input)

        # canvas is drawn to display the plot
        self.figure = plt.figure()
        self.canvas = FigureCanvas(self.figure)

        # Create navigation toolbar
        self.toolbar = NavigationToolbar(self.canvas, self.central_widget)
        self.toolbar.setIconSize(QSize(25, 25))
        self.layout.addWidget(self.toolbar)

        # adding the canvas
        self.layout.addWidget(self.canvas)

        # Create range layout for min and max input
        self.range_layout = QHBoxLayout()

        self.min_label = QLabel("Min X:")
        self.min_input = QLineEdit()
        self.min_input.setPlaceholderText("min value")

        self.max_label = QLabel("Max X:")
        self.max_input = QLineEdit()
        self.max_input.setPlaceholderText("max value")

        # adding labels and inputs for min and max to range layout
        self.range_layout.addWidget(self.min_label)
        self.range_layout.addWidget(self.min_input)
        self.range_layout.addWidget(self.max_label)
        self.range_layout.addWidget(self.max_input)

        # Create plot button and connect it to plot_function method
        self.plot_button = QPushButton("Plot")
        self.plot_button.clicked.connect(self.plot_function)

        # Add layouts and button to the main layout
        self.layout_for_inputs.addLayout(self.input_layout_fun)
        self.layout_for_inputs.addLayout(self.range_layout)
        self.layout_for_inputs.addWidget(self.plot_button)

        self.layout.addLayout(self.layout_for_inputs)

        # Register 'esc' key to exit the program gracefully
        keyboard.add_hotkey('esc', self.exit_program)

        """
        drawing the empty canvas 
        """
        x_values = []
        y_values = []
        self.canvas.figure.clear()
        ax = self.canvas.figure.add_subplot(111)
        ax.plot(x_values, y_values)
        ax.set_xlabel('x')
        ax.set_ylabel('f(x)')
        ax.set_title('f(x) = ')
        ax.grid(True)
        ax.legend(['f(x) = '])

        self.canvas.draw()

    def validate_input(self, function_str, min_x, max_x):
        """
        Validate the function input and range inputs.
        """

        # Check if the function field is empty
        if not function_str:
            raise ValueError("Function field cannot be empty.")

        # Validate function expression
        x = 0
        try:
            # using regex to substitute the "math." + "operation" functions
            n_str = function_str.replace('^', '**')
            pattern = r'\b(sqrt|exp|pi|e|(sin|cos|tan)h?)\b'
            modified_input = re.sub(pattern, r'math.\1', n_str)
            # eval() -> is used to evaluate and execute a string expression as a Python expression.
            eval(modified_input)
        except SyntaxError:
            raise ValueError("Invalid function expression.")

        # Validate min and max x values
        try:
            min_x = int(min_x)
            max_x = int(max_x)
            if min_x >= max_x:
                raise ValueError("Min X should be less than Max X.")
        except ValueError:
            raise ValueError("Invalid Min X or Max X value.")

        return min_x, max_x

    def plot_function(self):
        """
            Plot the function on a graph.
        """
        # Get input values
        function_str = self.function_input.text()
        min_x = self.min_input.text()
        max_x = self.max_input.text()

        try:
            min_x, max_x = self.validate_input(function_str, min_x, max_x)
        except ValueError as e:
            self.show_message(str(e))
            return

        # Generate x and y values for the plot
        x_values = []
        y_values = []
        step = (max_x - min_x) / 1000
        x = min_x
        while x <= max_x:
            try:
                # using regex to substitute the math.* functions
                n_str = function_str.replace('^', '**')
                pattern = r'\b(sqrt|exp|pi|e|(sin|cos|tan)h?)\b'
                modified_input = re.sub(pattern, r'math.\1', n_str)
                # eval() -> is used to evaluate and execute a string expression as a Python expression.
                y = eval(modified_input)
                x_values.append(x)  # append the x value to the x_values list
                y_values.append(y)  # append the y value to the y_values list
            except:
                pass
            x += step

        # Plot the graph using matplotlib
        self.canvas.figure.clear()
        ax = self.canvas.figure.add_subplot(111)
        ax.plot(x_values, y_values)
        ax.set_xlabel('x')
        ax.set_ylabel('f(x)')
        ax.set_title('f(x) = ' + function_str)
        ax.grid(True)
        ax.legend(['f(x) = ' + function_str])
        # ax.spines['left'].set_position('zero')

        self.canvas.draw()

    # which will be helpful using the keyboard interrupt ("enter") in the main thread
    def keyPressEvent(self, event: KeyEvent):
        # Checking if the Enter key was pressed
        if event.key() == Qt.Key_Enter or event.key() == Qt.Key_Return:
            self.plot_function()

        # Calling the base class implementation
        super().keyPressEvent(event)

    # display a message box with the given error message
    def show_message(self, message):
        # Display a message box with the given error message
        QMessageBox.warning(self, "Error", message, QMessageBox.Ok)

    # exit the program
    def exit_program(self):
        QApplication.quit()  # quit the application
