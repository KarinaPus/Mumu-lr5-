"""Business logic for text analysis tasks 4."""

import string

from modules.decorators import log_execution_time

REFERENCE_VOWELS = set("aeiouy")
WORD_SEPARATORS = {" ", ",", "."}


@log_execution_time
def count_spaces_and_punctuation(text_value: str) -> dict:
    """Count spaces and punctuation marks in a text without regex."""
    spaces_count = 0
    punctuation_count = 0

    for symbol in text_value:
        if symbol == " ":
            spaces_count += 1
        if symbol in string.punctuation:
            punctuation_count += 1

    return {
        "text_length": len(text_value),
        "spaces_count": spaces_count,
        "punctuation_count": punctuation_count,
    }


def extract_words(text_value: str) -> list[str]:
    """Extract words from a text where spaces, commas, and periods are separators."""
    words = []
    current_word = []

    for symbol in text_value:
        if symbol in WORD_SEPARATORS:
            if current_word:
                words.append("".join(current_word))
                current_word.clear()
            continue
        current_word.append(symbol)

    if current_word:
        words.append("".join(current_word))

    return words


def count_characters(text_value: str) -> dict[str, int]:
    """Count every character in a text in a case-insensitive way."""
    character_counts: dict[str, int] = {}

    for symbol in text_value.lower():
        character_counts[symbol] = character_counts.get(symbol, 0) + 1

    return dict(sorted(character_counts.items(), key=lambda item: item[0]))


def extract_words_after_commas(text_value: str) -> list[str]:
    """Collect words that immediately follow commas in a text."""
    words_after_commas = []

    for fragment in text_value.lower().split(",")[1:]:
        fragment_words = extract_words(fragment.strip())
        if fragment_words:
            words_after_commas.append(fragment_words[0])

    return sorted(words_after_commas)


@log_execution_time
def analyze_reference_text(text_value: str) -> dict:
    """Analyze the reference text for task 4 without regular expressions."""
    lowered_text = text_value.lower()
    words = extract_words(lowered_text)
    vowel_edge_words = [
        word for word in words if word[0] in REFERENCE_VOWELS or word[-1] in REFERENCE_VOWELS
    ]

    return {
        "text": text_value,
        "words": words,
        "vowel_edge_words_count": len(vowel_edge_words),
        "character_counts": count_characters(text_value),
        "words_after_commas": extract_words_after_commas(text_value),
    }
