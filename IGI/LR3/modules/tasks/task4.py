"""Launcher for task 4, variant 9."""

from modules.text_math import analyze_reference_text
from modules.ui import print_task_4_header, print_task_4_result

REFERENCE_TEXT = (
    "So she was considering in her own mind, as well as she could, "
    "for the hot day made her feel very sleepy and stupid, whether the "
    "pleasure of making a daisy-chain would be worth the trouble of "
    "getting up and picking the daisies, when suddenly a White Rabbit "
    "with pink eyes ran close by her."
)


def run_task_4() -> None:
    """Run task 4 for variant 9."""
    print_task_4_header()
    result, elapsed_time = analyze_reference_text(REFERENCE_TEXT)
    print_task_4_result(result, elapsed_time)
