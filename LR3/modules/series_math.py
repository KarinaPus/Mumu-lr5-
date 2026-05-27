"""Business logic for the series-based computation. 1задача"""

import math

from modules.decorators import log_execution_time

MAX_ITERATIONS = 500


@log_execution_time
def calculate_arccos_series(x_value: float, eps_value: float) -> dict:
    """Calculate arccos(x) using the arcsin(x) power series."""
    if x_value == 1.0:
        return {
            "x": x_value,
            "series_value": 0.0,
            "terms_used": 1,
            "math_value": math.acos(x_value),
            "absolute_error": 0.0,
        }

    if x_value == -1.0:
        return {
            "x": x_value,
            "series_value": math.pi,
            "terms_used": 1,
            "math_value": math.acos(x_value),
            "absolute_error": 0.0,
        }

    term_value = x_value
    series_sum = 0.0
    used_terms = 0

    for iteration in range(MAX_ITERATIONS):
        series_sum += term_value
        used_terms += 1

        if abs(term_value) < eps_value:
            break

        numerator = (2 * iteration + 1) ** 2 * x_value * x_value
        denominator = 2 * (iteration + 1) * (2 * iteration + 3)
        term_value *= numerator / denominator
    else:
        raise ArithmeticError(
            "The required precision was not reached in 500 iterations."
        )

    series_value = math.pi / 2 - series_sum
    math_value = math.acos(x_value)
    absolute_error = abs(series_value - math_value)

    return {
        "x": x_value,
        "series_value": series_value,
        "terms_used": used_terms,
        "math_value": math_value,
        "absolute_error": absolute_error,
    }
