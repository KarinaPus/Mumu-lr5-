"""Validation helpers for user input."""

def parse_float(user_input: str, field_name: str) -> float:
    """Convert user input to float with a clear error message."""
    try:
        return float(user_input.replace(",", ".").strip())
    except ValueError as exc:
        raise ValueError(f"{field_name} must be a real number.") from exc


def parse_int(user_input: str, field_name: str) -> int:
    """Convert user input to int with a clear error message."""
    try:
        return int(user_input.strip())
    except ValueError as exc:
        raise ValueError(f"{field_name} must be an integer.") from exc


def validate_x_value(x_value: float) -> float:
    """Validate the argument range for arccos(x)."""
    if not -1.0 <= x_value <= 1.0:
        raise ValueError("x must belong to the interval [-1, 1].")
    return x_value


def validate_eps_value(eps_value: float) -> float:
    """Validate the required positive accuracy."""
    if eps_value <= 0:
        raise ValueError("eps must be greater than 0.")
    return eps_value


def validate_positive_int(int_value: int, field_name: str) -> int:
    """Validate that a number is a positive integer."""
    if int_value <= 0:
        raise ValueError(f"{field_name} must be greater than 0.")
    return int_value


def validate_range_bounds(left_border: float, right_border: float) -> tuple[float, float]:
    """Validate a floating-point interval for random generation."""
    if left_border > right_border:
        raise ValueError("the left border must not exceed the right border.")
    return left_border, right_border
