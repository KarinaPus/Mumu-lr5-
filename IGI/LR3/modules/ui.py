"""Presentation helpers for the console interface."""


def print_main_header() -> None:
    """Show the main program heading."""
    print("=" * 72)
    print("Laboratory work 3. Variant 9")
    print("Interactive launcher for the laboratory tasks")
    print("=" * 72)


def print_task_menu() -> None:
    """Display the available tasks."""
    print("\nAvailable tasks")
    print("-" * 72)
    print("1 - Task 1: arccos(x) using a power series")
    print("2 - Task 2: sequence processing")
    print("3 - Task 3: count spaces and punctuation marks")
    print("4 - Task 4: analyze the reference text")
    print("5 - Task 5: process a real-valued list")
    print("0 - Exit")
    print("-" * 72)


def print_task_1_header() -> None:
    """Show the heading for task 1."""
    print("\nTask 1. Variant 9")
    print("Function: arccos(x) = pi/2 - arcsin(x)")
    print("Series domain: |x| <= 1")
    print("-" * 72)


def print_task_2_header() -> None:
    """Show the heading for task 2."""
    print("\nTask 2. Variant 9")
    print("Goal: calculate the arithmetic mean of even integers")
    print("Input ends when you enter 0")
    print("-" * 72)


def print_task_3_header() -> None:
    """Show the heading for task 3."""
    print("\nTask 3. Variant 9")
    print("Goal: count spaces and punctuation marks in the entered text")
    print("Regular expressions are not used")
    print("-" * 72)


def print_task_4_header() -> None:
    """Show the heading for task 4."""
    print("\nTask 4. Variant 9")
    print("Goal: analyze the predefined text without regular expressions")
    print("Checks vowels, character frequencies, and comma followers")
    print("-" * 72)


def print_task_5_header() -> None:
    """Show the heading for task 5."""
    print("\nTask 5. Variant 9")
    print("Goal: process a real-valued list with two initialization modes")
    print("Find the product of negative elements and a partial positive sum")
    print("-" * 72)


def print_result(result: dict, elapsed_time: float) -> None:
    """Display the calculation result in a user-friendly form."""
    print("\nCalculation result")
    print("-" * 72)
    print(f"x              = {result['x']:.10f}")
    print(f"F(x)           = {result['series_value']:.10f}")
    print(f"n              = {result['terms_used']}")
    print(f"Math F(x)      = {result['math_value']:.10f}")
    print(f"Absolute error = {result['absolute_error']:.10e}")
    print(f"Elapsed time   = {elapsed_time:.6f} s")
    print("-" * 72)


def print_task_2_result(result: dict, elapsed_time: float) -> None:
    """Display the result for task 2."""
    print("\nCalculation result")
    print("-" * 72)
    print(f"Entered numbers     = {result['numbers_count']}")
    print(f"Even numbers count  = {result['even_numbers_count']}")
    print(f"Even numbers        = {result['even_numbers']}")
    print(f"Average value       = {result['average_value']:.10f}")
    print(f"Elapsed time        = {elapsed_time:.6f} s")
    print("-" * 72)


def print_task_3_result(result: dict, elapsed_time: float) -> None:
    """Display the result for task 3."""
    print("\nCalculation result")
    print("-" * 72)
    print(f"Entered text length = {result['text_length']}")
    print(f"Spaces count        = {result['spaces_count']}")
    print(f"Punctuation count   = {result['punctuation_count']}")
    print(f"Elapsed time        = {elapsed_time:.6f} s")
    print("-" * 72)


def format_character_counts(character_counts: dict[str, int]) -> str:
    """Prepare a readable string for character frequency output."""
    formatted_items = []

    for symbol, count in character_counts.items():
        label = "<space>" if symbol == " " else symbol
        formatted_items.append(f"{label}: {count}")

    return ", ".join(formatted_items)


def print_task_4_result(result: dict, elapsed_time: float) -> None:
    """Display the result for task 4."""
    print("\nReference text")
    print("-" * 72)
    print(result["text"])
    print("-" * 72)
    print("Calculation result")
    print("-" * 72)
    print(f"Words count                     = {len(result['words'])}")
    print(f"Words starting or ending vowel  = {result['vowel_edge_words_count']}")
    print(
        "Character frequencies          = "
        f"{format_character_counts(result['character_counts'])}"
    )
    print(f"Words after commas             = {result['words_after_commas']}")
    print(f"Elapsed time                   = {elapsed_time:.6f} s")
    print("-" * 72)


def print_task_5_result(result: dict, elapsed_time: float) -> None:
    """Display the result for task 5."""
    print("\nCalculation result")
    print("-" * 72)
    print(f"Generated list                 = {result['numbers']}")
    print(f"Maximum element                = {result['max_value']:.10f}")
    print(f"Index of maximum element       = {result['max_index']}")
    print(f"Negative elements              = {result['negative_elements']}")
    print(f"Product of negative elements   = {result['negative_product']:.10f}")
    print(f"Positive elements before max   = {result['positive_before_max']}")
    print(
        "Sum before maximum element     = "
        f"{result['positive_sum_before_max']:.10f}"
    )
    print(f"Elapsed time                   = {elapsed_time:.6f} s")
    print("-" * 72)
