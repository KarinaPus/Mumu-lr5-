"""Launcher for task 2, variant 9."""

from modules.input_utils import request_int
from modules.sequence_math import calculate_average_of_even_numbers
from modules.ui import print_task_2_header, print_task_2_result


def run_task_2() -> None:
    """Run task 2 for variant 9."""
    print_task_2_header()
    numbers = []

    while True:
        current_number = request_int(
            "Enter an integer (0 to finish input): ",
            "sequence element",
        )
        if current_number == 0:
            break
        numbers.append(current_number)

    if not numbers:
        print("No numbers were entered before the terminating 0.")
        return

    try:
        result, elapsed_time = calculate_average_of_even_numbers(numbers)
        print_task_2_result(result, elapsed_time)
    except ArithmeticError as error:
        print(f"Calculation error: {error}")
