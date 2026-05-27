"""Launcher for task 5, variant 9."""

from modules.input_utils import request_list_initialization_choice, request_positive_int
from modules.list_initializers import (
    initialize_list_from_input,
    initialize_list_with_generator,
)
from modules.list_math import analyze_real_number_list
from modules.ui import print_task_5_header, print_task_5_result


def run_task_5() -> None:
    """Run task 5 for variant 9."""
    print_task_5_header()
    list_size = request_positive_int("Enter the list size: ", "list size")
    init_choice = request_list_initialization_choice()

    if init_choice == "1":
        numbers = initialize_list_from_input(list_size)
    else:
        numbers = initialize_list_with_generator(list_size)

    try:
        result, elapsed_time = analyze_real_number_list(numbers)
        print_task_5_result(result, elapsed_time)
    except ArithmeticError as error:
        print(f"Calculation error: {error}")
