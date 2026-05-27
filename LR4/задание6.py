"""Lab work 4, task 6, variant 9.

Pandas practice with the Video Game Sales dataset.
The program works with a local CSV file if it exists.
If the file is missing, a small demo dataset is used.
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd


class InputMixin:
    """Helpers for simple user input."""

    @staticmethod
    def read_yes_no(prompt: str) -> bool:
        while True:
            try:
                answer = input(prompt).strip().lower()
            except EOFError:
                return False

            if answer in {"да", "д", "y", "yes"}:
                return True
            if answer in {"нет", "н", "n", "no"}:
                return False

            print("Введите да или нет.")


class BaseTask:
    """Base class for console tasks."""

    task_name = "Task"

    def run(self) -> None:
        while True:
            print(f"\n{self.task_name}")
            self.solve()
            if not self.read_yes_no("\nПовторить программу? (да/нет): "):
                print("Программа завершена.")
                break


class VideoGameSalesTask(BaseTask, InputMixin):
    """Task 6, variant 9."""

    task_name = "Задание 6, вариант 9"

    def __init__(self) -> None:
        self.base_dir = Path(__file__).resolve().parent

    @staticmethod
    def demo_dataset() -> pd.DataFrame:
        return pd.DataFrame(
            {
                "Name": [
                    "Wii Sports",
                    "Brain Game",
                    "FIFA 20",
                    "Tetris Plus",
                    "NBA 2K21",
                    "Puzzle Quest",
                    "Sports Hero",
                    "Logic World",
                ],
                "Platform": ["Wii", "DS", "PS4", "GB", "PS5", "PC", "X360", "3DS"],
                "Genre": ["Sports", "Puzzle", "Sports", "Puzzle", "Sports", "Puzzle", "Sports", "Puzzle"],
                "Global_Sales": [82.74, 1.20, 3.50, 2.00, 4.10, 0.80, 2.60, 0.90],
            }
        )

    def find_csv_file(self) -> Path | None:
        possible_names = [
            "vgsales.csv",
            "video_game_sales.csv",
            "video_games_sales.csv",
            "Video_Games_Sales.csv",
            "Video Game Sales.csv",
        ]

        for name in possible_names:
            path = self.base_dir / name
            if path.exists():
                return path

        for path in self.base_dir.glob("*.csv"):
            if "sale" in path.name.lower() or "game" in path.name.lower() or "vg" in path.name.lower():
                return path

        return None

    def load_dataset(self) -> pd.DataFrame:
        csv_file = self.find_csv_file()
        if csv_file is not None:
            print(f"\nНайден файл: {csv_file.name}")
            return pd.read_csv(csv_file)

        print("\nФайл с датасетом не найден, поэтому используется маленький демонстрационный пример.")
        return self.demo_dataset()

    @staticmethod
    def find_column(df: pd.DataFrame, variants: list[str]) -> str:
        columns_map = {column.lower(): column for column in df.columns}
        for name in variants:
            if name.lower() in columns_map:
                return columns_map[name.lower()]
        raise KeyError(f"Не найден столбец. Подходящие варианты: {', '.join(variants)}")

    def prepare_dataset(self, df: pd.DataFrame) -> pd.DataFrame:
        result = df.copy()

        platform_col = self.find_column(result, ["Platform"])
        genre_col = self.find_column(result, ["Genre"])
        sales_col = self.find_column(result, ["Global_Sales", "Global Sales"])

        result[platform_col] = result[platform_col].astype(str).str.strip()
        result[genre_col] = result[genre_col].astype(str).str.strip()
        result[sales_col] = pd.to_numeric(result[sales_col], errors="coerce")

        result = result.dropna(subset=[platform_col, genre_col, sales_col])
        return result

    @staticmethod
    def show_dataframe(title: str, obj: pd.Series | pd.DataFrame) -> None:
        print(title)
        print(obj)

    def part_a(self, df: pd.DataFrame) -> None:
        platform_col = self.find_column(df, ["Platform"])

        unique_platforms = df[platform_col].drop_duplicates().reset_index(drop=True)
        platform_series = pd.Series(unique_platforms.values)
        platform_series.index = [f"platform_{i + 1}" for i in range(len(platform_series))]

        platform_frame = platform_series.to_frame(name="Platform")

        print("\nЧасть A")
        self.show_dataframe("Series из уникальных платформ:", platform_series)
        self.show_dataframe("\nDataFrame, созданный из Series:", platform_frame)

    def part_b(self, df: pd.DataFrame) -> None:
        genre_col = self.find_column(df, ["Genre"])
        sales_col = self.find_column(df, ["Global_Sales", "Global Sales"])

        sports_sales = df.loc[df[genre_col].str.lower() == "sports", sales_col]
        puzzle_sales = df.loc[df[genre_col].str.lower() == "puzzle", sales_col]

        sports_mean = sports_sales.mean()
        puzzle_mean = puzzle_sales.mean()

        print("\nЧасть Б")
        print("\nИнформация о таблице:")
        print(df.info())

        print("\nПервые 5 строк:")
        print(df.head())

        print("\nОписание числовых данных:")
        print(df.describe(include="number"))

        print(f"\nСредние глобальные продажи игр жанра Sports: {sports_mean:.2f}")
        print(f"Средние глобальные продажи игр жанра Puzzle: {puzzle_mean:.2f}")

        if pd.isna(sports_mean) or pd.isna(puzzle_mean) or puzzle_mean == 0:
            print("Нельзя посчитать отношение средних значений.")
            return

        ratio = sports_mean / puzzle_mean
        print(f"Средние глобальные продажи игр жанра Sports больше в {ratio:.2f} раза.")

    def solve(self) -> None:
        raw_df = self.load_dataset()
        df = self.prepare_dataset(raw_df)

        if df.empty:
            print("После обработки данных таблица пустая.")
            return

        self.part_a(df)
        self.part_b(df)


def main() -> None:
    VideoGameSalesTask().run()


if __name__ == "__main__":
    main()
