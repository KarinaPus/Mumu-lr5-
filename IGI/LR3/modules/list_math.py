"""Business logic for list processing tasks."""

from modules.decorators import log_execution_time


@log_execution_time
def analyze_real_number_list(numbers: list[float]) -> dict:
    """Process a real-valued list for task 5 of variant 9."""
    negative_elements = [number for number in numbers if number < 0]

    if not negative_elements:
        raise ArithmeticError("The list does not contain negative elements.")

    negative_product = 1.0
    for number in negative_elements:
        negative_product *= number

    max_value = max(numbers)
    max_index = numbers.index(max_value)
    positive_before_max = [number for number in numbers[:max_index] if number > 0]

    return {
        "numbers": numbers,
        "max_value": max_value,
        "max_index": max_index + 1,
        "negative_elements": negative_elements,
        "negative_product": negative_product,
        "positive_before_max": positive_before_max,
        "positive_sum_before_max": sum(positive_before_max),
    }
