"""Business logic for sequence processing tasks.задачи 2"""

from modules.decorators import log_execution_time


@log_execution_time
def calculate_average_of_even_numbers(numbers: list[int]) -> dict:
    """Calculate the arithmetic mean of even integers in a sequence."""
    even_numbers = [number for number in numbers if number % 2 == 0]

    if not even_numbers:
        raise ArithmeticError("The sequence does not contain even numbers.")

    average_value = sum(even_numbers) / len(even_numbers)
    return {
        "numbers_count": len(numbers),
        "even_numbers_count": len(even_numbers),
        "even_numbers": even_numbers,
        "average_value": average_value,
    }
#ctnbvcr nfqv pjyf b ltajkyf nfqcv pjyf?чтобы не была закорхожена. тайп зона 