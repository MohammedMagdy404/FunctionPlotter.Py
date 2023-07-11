import sys
import math
import re
import keyboard
import matplotlib.pyplot as plt
from PySide2.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, \
    QPushButton, QMessageBox
from PySide2.QtCore import Qt
from PySide2.QtGui import QIcon
import pytest
import pytestqt


# Defining FunctionPlotter class inheriting from QMainWindow
class FunctionPlotter(QMainWindow):
    # defining the constructor and declaring self explicitly.
    def __init__(self):
        # calling the constructor of the parent class.
        super().__init__()

        # Set window properties
        self.setWindowTitle("Function Plotter")
        self.setWindowIcon(QIcon("icon.png"))
        self.resize(600, 400)

        # Create central widget
        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)

        # Set layout
        self.layout = QVBoxLayout(self.central_widget)

        # Create input layout for function input
        self.input_layout = QHBoxLayout()
        self.function_label = QLabel("Function:")
        self.function_input = QLineEdit()
        # Adding function label and input to the input layout for function input
        self.input_layout.addWidget(self.function_label)
        self.input_layout.addWidget(self.function_input)

        # Create range layout for min and max input
        self.range_layout = QHBoxLayout()
        self.min_label = QLabel("Min X:")
        self.min_input = QLineEdit()
        self.max_label = QLabel("Max X:")
        self.max_input = QLineEdit()
        # adding labels and inputs for min and max to range layout
        self.range_layout.addWidget(self.min_label)
        self.range_layout.addWidget(self.min_input)
        self.range_layout.addWidget(self.max_label)
        self.range_layout.addWidget(self.max_input)

        # Create plot button and connect it to plot_function method
        self.plot_button = QPushButton("Plot")
        self.plot_button.clicked.connect(self.plot_function)
        # controlling keyboard
        keyboard.add_hotkey('enter', self.plot_function)

        # Add layouts and button to the main layout
        self.layout.addLayout(self.input_layout)
        self.layout.addLayout(self.range_layout)
        self.layout.addWidget(self.plot_button)

        # Register 'esc' key to exit the program gracefully
        keyboard.add_hotkey('esc', self.exit_program)

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
            # using regex to substitute the math.* functions
            n_str = function_str.replace('^', '**')
            pattern = pattern = r'\b(sin|cos|tan|sqrt)\b'
            modified_input = re.sub(pattern, r'math.\1', n_str)
            # eval() -> is used to evaluate and execute a string expression as a Python expression.
            eval(modified_input)
        except SyntaxError:
            raise ValueError("Invalid function expression.")

        # Validate min and max x values
        try:
            min_x = float(min_x)
            max_x = float(max_x)
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
                pattern = pattern = r'\b(sin|cos|tan|sqrt)\b'
                modified_input = re.sub(pattern, r'math.\1', n_str)
                # eval() -> is used to evaluate and execute a string expression as a Python expression.
                y = eval(modified_input)
                x_values.append(x)
                y_values.append(y)
            except:
                pass
            x += step

        # Plot the graph using matplotlib
        plt.figure()
        plt.plot(x_values, y_values)
        plt.xlabel('x')
        plt.ylabel('f(x)')
        plt.title('Function Plot')
        plt.grid(True)
        plt.show()

    def show_message(self, message):
        """
        Show an error message in a message box.
        """
        QMessageBox.warning(self, "Error", message, QMessageBox.Ok)

    def exit_program(self):
        """
        Exit the program gracefully.
        """
        QApplication.quit()


# Running the application
if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = FunctionPlotter()
    window.show()
    sys.exit(app.exec_())
