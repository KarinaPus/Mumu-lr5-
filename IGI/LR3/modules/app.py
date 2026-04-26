"""Application entry logic."""

from modules.input_utils import request_main_menu_choice, request_repeat_choice
from modules.tasks.task1 import run_task_1
from modules.tasks.task2 import run_task_2
from modules.tasks.task3 import run_task_3
from modules.tasks.task4 import run_task_4
from modules.tasks.task5 import run_task_5
from modules.ui import print_main_header, print_task_menu


def run_application() -> None:
    """Run the interactive laboratory work application."""
    print_main_header()

    while True:
        print_task_menu()
        task_choice = request_main_menu_choice()

        if task_choice == "1":
            run_task_1()
        elif task_choice == "2":
            run_task_2()
        elif task_choice == "3":
            run_task_3()
        elif task_choice == "4":
            run_task_4()
        elif task_choice == "5":
            run_task_5()
        else:
            print("The program has been finished.")
            break

        if not request_repeat_choice():
            print("The program has been finished.")
            break
