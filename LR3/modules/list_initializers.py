"""List initialization helpers for task 5."""

from random import uniform

from modules.input_utils import request_float, request_generation_bounds


def initialize_list_from_input(length: int) -> list[float]:
    """Fill a list with user-entered floating-point values."""
    numbers = []

    for index in range(length):
        numbers.append(
            request_float(
                f"Enter element #{index + 1}: ",
                f"element #{index + 1}",
            )
        )

    return numbers


def generate_random_numbers(
    length: int,
    left_border: float,
    right_border: float,
):
    """Yield random floating-point values one by one."""
    for _ in range(length):
        yield round(uniform(left_border, right_border), 3)


def initialize_list_with_generator(length: int) -> list[float]:
    """Fill a list with generated floating-point values."""
    left_border, right_border = request_generation_bounds()
    return list(generate_random_numbers(length, left_border, right_border))
