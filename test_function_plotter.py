from function_plotter import FunctionPlotter
import pytest
import numpy as np


# Test the validate_input function


def test_validate_input():
    # Valid input
    testClass = FunctionPlotter()
    function_str = "x"
    min_x = "0"
    max_x = "10"
    result = testClass.validate_input(function_str, min_x, max_x)
    assert result == (0, 10)

    # Empty function field
    with pytest.raises(ValueError):
        function_str = ""
        testClass.validate_input(function_str, min_x, max_x)

    # Invalid function expression
    with pytest.raises(ValueError):
        function_str = "x$2"
        testClass.validate_input(function_str, min_x, max_x)

    # Invalid min_x or max_x value
    with pytest.raises(ValueError):
        min_x = "abc"
        testClass.validate_input(function_str, min_x, max_x)

    # min_x >= max_x
    with pytest.raises(ValueError):
        min_x = "10"
        max_x = "5"
        testClass.validate_input(function_str, min_x, max_x)
    # Clean up
    testClass.exit_program()


# Test the plot_function function
def test_plot_function():
    plotter = FunctionPlotter()

    # Test a valid function and range inputs
    plotter.function_input.setText("x**2")
    plotter.min_input.setText("0")
    plotter.max_input.setText("10")
    plotter.plot_function()

    x_input = 5
    y = 25

    # Find the y-axis value for the given x-coordinate
    y_output = None
    for x, y in zip(plotter.x_values, plotter.y_values):
        if np.isclose(x, x_input, atol=1e-6):
            y_output = y
            break
    # Assert the plot is generated correctly
    assert y_output == y


# Run all the tests
if __name__ == "__main__":
    pytest.main()
