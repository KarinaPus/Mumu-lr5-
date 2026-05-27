"""Launcher for task 3, variant 9."""

from modules.input_utils import request_text
from modules.text_math import count_spaces_and_punctuation
from modules.ui import print_task_3_header, print_task_3_result


def run_task_3() -> None:
    """Run task 3 for variant 9."""
    print_task_3_header()
    text_value = request_text("Enter a text line: ")

    result, elapsed_time = count_spaces_and_punctuation(text_value)
    print_task_3_result(result, elapsed_time)
