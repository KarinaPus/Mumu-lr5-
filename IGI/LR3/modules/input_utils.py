"""Helpers for interactive input."""

from modules.validators import (
    parse_float,
    parse_int,
    validate_eps_value,
    validate_positive_int,
    validate_range_bounds,
    validate_x_value,
)


def read_user_input(prompt_text: str) -> str:
    """Read user input and finish gracefully on end-of-file."""
    try:
        return input(prompt_text)
    except EOFError as exc:
        raise SystemExit("Input stream ended. The program has been finished.") from exc


def request_float(prompt_text: str, field_name: str) -> float:
    """Request a floating-point number until it is entered correctly."""
    while True:
        raw_value = read_user_input(prompt_text)
        try:
            return parse_float(raw_value, field_name)
        except ValueError as error:
            print(f"Input error: {error}")


def request_int(prompt_text: str, field_name: str) -> int:
    """Request an integer number until it is entered correctly."""
    while True:
        raw_value = read_user_input(prompt_text)
        try:
            return parse_int(raw_value, field_name)
        except ValueError as error:
            print(f"Input error: {error}")


def request_x_value() -> float:
    """Request a valid x value from the user."""
    while True:
        x_value = request_float("Enter x in [-1, 1]: ", "x")
        try:
            return validate_x_value(x_value)
        except ValueError as error:
            print(f"Input error: {error}")


def request_eps_value() -> float:
    """Request a valid positive epsilon from the user."""
    while True:
        eps_value = request_float("Enter eps (> 0): ", "eps")
        try:
            return validate_eps_value(eps_value)
        except ValueError as error:
            print(f"Input error: {error}")


def request_repeat_choice() -> bool:
    """Ask whether the user wants to continue working with the program."""
    while True:
        answer = read_user_input("Do you want to continue working? (y/n): ").strip().lower()
        if answer in {"y", "yes", "д", "да"}:
            return True
        if answer in {"n", "no", "н", "нет"}:
            return False
        print("Input error: enter 'y' or 'n'.")


def request_main_menu_choice() -> str:
    """Request the task number from the main menu."""
    while True:
        choice = read_user_input("Choose a task (1, 2, 3, 4, 5, 0): ").strip()
        if choice in {"1", "2", "3", "4", "5", "0"}:
            return choice
        print("Input error: enter 1, 2, 3, 4, 5 or 0.")


def request_text(prompt_text: str) -> str:
    """Request a text value from the user."""
    return read_user_input(prompt_text)


def request_positive_int(prompt_text: str, field_name: str) -> int:
    """Request a positive integer number."""
    while True:
        int_value = request_int(prompt_text, field_name)
        try:
            return validate_positive_int(int_value, field_name)
        except ValueError as error:
            print(f"Input error: {error}")


def request_list_initialization_choice() -> str:
    """Request the list initialization mode for task 5."""
    while True:
        choice = read_user_input(
            "Choose list initialization (1 - user input, 2 - generator): "
        ).strip()
        if choice in {"1", "2"}:
            return choice
        print("Input error: enter 1 or 2.")


def request_generation_bounds() -> tuple[float, float]:
    """Request valid bounds for random list generation."""
    while True:
        left_border = request_float("Enter the left border of the range: ", "left border")
        right_border = request_float(
            "Enter the right border of the range: ",
            "right border",
        )
        try:
            return validate_range_bounds(left_border, right_border)
        except ValueError as error:
            print(f"Input error: {error}")
