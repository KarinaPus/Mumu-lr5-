"""Launcher for task 1, variant 9."""

from modules.input_utils import request_eps_value, request_x_value
from modules.series_math import calculate_arccos_series
from modules.ui import print_result, print_task_1_header


def run_task_1() -> None:
    """Run task 1 for variant 9."""
    print_task_1_header()
    x_value = request_x_value()
    eps_value = request_eps_value()

    try:
        result, elapsed_time = calculate_arccos_series(x_value, eps_value)
        print_result(result, elapsed_time)
    except ArithmeticError as error:
        print(f"Calculation error: {error}")
