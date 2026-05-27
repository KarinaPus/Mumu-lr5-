"""Lab work 4, task 5, variant 9.

Matrix analysis with NumPy:
1. Generate an integer matrix A[n, m] using random values.
2. Swap the largest elements in the first and last columns.
3. Compute the correlation coefficient between the first and last columns.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Tuple

import numpy as np


class InputMixin:
    """Utility methods for safe user input."""

    @staticmethod
    def read_int(prompt: str, min_value: int | None = None) -> int:
        while True:
            raw = input(prompt).strip()
            try:
                value = int(raw)
                if min_value is not None and value < min_value:
                    raise ValueError
                return value
            except ValueError:
                if min_value is None:
                    print("Ошибка: введите целое число.")
                else:
                    print(f"Ошибка: введите целое число не меньше {min_value}.")

    @staticmethod
    def read_yes_no(prompt: str) -> bool:
        while True:
            try:
                raw = input(prompt).strip().lower()
            except EOFError:
                return False
            if raw in {"да", "д", "y", "yes"}:
                return True
            if raw in {"нет", "н", "n", "no"}:
                return False
            print("Ошибка: введите 'да' или 'нет'.")


@dataclass
class MatrixConfig:
    rows: int
    cols: int
    low: int
    high: int

    def __post_init__(self) -> None:
        if self.rows <= 0 or self.cols <= 0:
            raise ValueError("Размеры матрицы должны быть положительными.")
        if self.high < self.low:
            raise ValueError("Правая граница диапазона не может быть меньше левой.")


class CorrelationMixin:
    """Additional helpers for correlation calculations."""

    @staticmethod
    def correlation_numpy(first: np.ndarray, last: np.ndarray) -> float:
        if len(first) < 2:
            return float("nan")
        if np.all(first == first[0]) or np.all(last == last[0]):
            return float("nan")
        return float(np.corrcoef(first, last)[0, 1])

    @staticmethod
    def correlation_manual(first: np.ndarray, last: np.ndarray) -> float:
        if len(first) < 2:
            return float("nan")

        first_mean = float(np.mean(first))
        last_mean = float(np.mean(last))
        first_centered = first - first_mean
        last_centered = last - last_mean

        numerator = float(np.sum(first_centered * last_centered))
        denominator = float(
            np.sqrt(np.sum(first_centered ** 2) * np.sum(last_centered ** 2))
        )

        if denominator == 0:
            return float("nan")
        return numerator / denominator


class MatrixTask(InputMixin, CorrelationMixin):
    """Implements variant 9 of task 5."""

    task_name = "Задание 5, вариант 9"

    def __init__(self) -> None:
        self.matrix: np.ndarray | None = None

    def read_config(self) -> MatrixConfig:
        print(f"\n{self.task_name}")
        rows = self.read_int("Введите количество строк n: ", min_value=1)
        cols = self.read_int(
            "Введите количество столбцов m (не меньше 2): ", min_value=2
        )
        low = self.read_int("Введите нижнюю границу случайных чисел: ")
        high = self.read_int("Введите верхнюю границу случайных чисел: ")
        return MatrixConfig(rows=rows, cols=cols, low=low, high=high)

    @staticmethod
    def generate_matrix(config: MatrixConfig) -> np.ndarray:
        return np.random.randint(config.low, config.high + 1, size=(config.rows, config.cols))

    @staticmethod
    def max_positions(matrix: np.ndarray) -> Tuple[Tuple[int, int], Tuple[int, int]]:
        first_col_row = int(np.argmax(matrix[:, 0]))
        last_col_row = int(np.argmax(matrix[:, -1]))
        return (first_col_row, 0), (last_col_row, matrix.shape[1] - 1)

    @staticmethod
    def swap_column_maximums(matrix: np.ndarray) -> Tuple[np.ndarray, Tuple[Tuple[int, int], Tuple[int, int]]]:
        result = matrix.copy()
        first_pos, last_pos = MatrixTask.max_positions(result)
        result[first_pos], result[last_pos] = result[last_pos], result[first_pos]
        return result, (first_pos, last_pos)

    def solve(self) -> None:
        config = self.read_config()
        source_matrix = self.generate_matrix(config)
        changed_matrix, (first_pos, last_pos) = self.swap_column_maximums(source_matrix)

        first_column = changed_matrix[:, 0].astype(float)
        last_column = changed_matrix[:, -1].astype(float)

        corr_np = self.correlation_numpy(first_column, last_column)
        corr_manual = self.correlation_manual(first_column, last_column)

        print("\nИсходная матрица A:")
        print(source_matrix)

        print(
            "\nМаксимальный элемент первого столбца: "
            f"{source_matrix[first_pos]} в позиции {first_pos}"
        )
        print(
            "Максимальный элемент последнего столбца: "
            f"{source_matrix[last_pos]} в позиции {last_pos}"
        )

        print("\nМатрица после обмена:")
        print(changed_matrix)

        print("\nПервый столбец после обмена:")
        print(first_column.astype(int))
        print("Последний столбец после обмена:")
        print(last_column.astype(int))

        if np.isnan(corr_np):
            print(
                "\nКоэффициент корреляции вычислить нельзя: "
                "один из столбцов содержит одинаковые значения "
                "или в матрице меньше двух строк."
            )
        else:
            print(f"\nКоэффициент корреляции (numpy.corrcoef): {corr_np:.2f}")
            print(f"Коэффициент корреляции (по формуле): {corr_manual:.2f}")

    def run(self) -> None:
        while True:
            try:
                self.solve()
            except ValueError as error:
                print(f"\nОшибка: {error}")
            except Exception as error:
                print(f"\nНепредвиденная ошибка: {error}")

            if not self.read_yes_no("\nПовторить выполнение программы? (да/нет): "):
                print("Работа программы завершена.")
                break


def main() -> None:
    MatrixTask().run()


if __name__ == "__main__":
    main()
