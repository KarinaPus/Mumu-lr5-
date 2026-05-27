
import os
import re
import zipfile
from typing import List, Optional, Tuple


INPUT_FILE = 'task2_input.txt'
OUT_TEXT = 'results_task2_new.txt'
OUT_ZIP = 'results_task2_new.zip'


class TextAnalyzer:
    VOWELS = set('aeiouyAEIOUYаеёиоуыэюяАЕЁИОУЫЭЮЯ')
    CONSONANTS = set('bcdfghjklmnpqrstvwxyzBCDFGHJKLMNPQRSTVWXYZбвгджзйклмнпрстфхцчшщБВГДЖЗЙКЛМНПРСТФХЦЧШЩ')

    WORD_RE = re.compile(r'[A-Za-zА-Яа-яёЁ]+')
    SENTENCE_SPLIT_RE = re.compile(r'(?<=[.!?])\s+')
    DATE_RE = re.compile(r'\b\d{2}-\d{2}-\d{4}\b')
    EMOTICON_RE = re.compile(r'(?<!\S)(?:[;:])(?:-*)([()\[\]])\1*(?!\S)')
    LOWERCASE_RE = re.compile(r'[a-zа-яё]')
    LATIN_I_RE = re.compile(r'[A-Za-z]*i[A-Za-z]*', re.IGNORECASE)
    START_I_RE = re.compile(r'\b[iI][A-Za-zА-Яа-яёЁ]*\b')

    def __init__(self, text: str):
        self.text = text
        self.words = self.WORD_RE.findall(text)
        self.sentences = self._split_sentences()

    def _split_sentences(self) -> List[str]:
        parts = self.SENTENCE_SPLIT_RE.split(self.text.strip())
        return [part.strip() for part in parts if part.strip()]

    def count_sentences(self) -> int:
        return len(self.sentences)

    def count_sentence_types(self) -> Tuple[int, int, int]:
        declarative = 0
        interrogative = 0
        imperative = 0

        for sentence in self.sentences:
            if re.search(r'\?\s*$', sentence):
                interrogative += 1
            elif re.search(r'!\s*$', sentence):
                imperative += 1
            else:
                declarative += 1

        return declarative, interrogative, imperative

    def avg_sentence_length_chars(self) -> float:
        if not self.sentences:
            return 0.0

        total = 0
        for sentence in self.sentences:
            total += sum(len(word) for word in self.WORD_RE.findall(sentence))

        return total / len(self.sentences)

    def avg_word_length(self) -> float:
        if not self.words:
            return 0.0

        return sum(len(word) for word in self.words) / len(self.words)

    def count_emoticons(self) -> int:
        return len(self.EMOTICON_RE.findall(self.text))

    def find_dates(self) -> List[str]:
        return self.DATE_RE.findall(self.text)

    def words_last_vowel_prev_consonant(self) -> List[str]:
        return [
            word for word in self.words
            if len(word) >= 2 and word[-1] in self.VOWELS and word[-2] in self.CONSONANTS
        ]

    def count_lowercase_letters(self) -> int:
        return len(self.LOWERCASE_RE.findall(self.text))

    def last_word_with_i(self) -> Tuple[Optional[str], Optional[int]]:
        last_word = None
        last_index = None

        for index, word in enumerate(self.words, start=1):
            if self.LATIN_I_RE.fullmatch(word):
                last_word = word
                last_index = index

        return last_word, last_index

    def text_exclude_start_i(self) -> str:
        cleaned = self.START_I_RE.sub('', self.text)
        cleaned = re.sub(r'\s+', ' ', cleaned).strip()
        return cleaned


def ensure_sample_input(path: str):
    if os.path.exists(path):
        return

    sample = (
        'Это пример текста. Он содержит несколько предложений! Как дела? '
        'Сегодня 12-05-2007 был особенный день.\n'
        'В тексте есть смайлики: ;-( ;----((( ;---------[[[[[[[[ :)))) и простые символы.\n'
        'Слова: island irony ink inca idea Amelia iliad biu.\n'
        'Последняя строка содержит несколько слов, и некоторые начинаются с i и I.'
    )

    with open(path, 'w', encoding='utf-8') as file:
        file.write(sample)


def save_results(lines: List[str], out_path: str):
    with open(out_path, 'w', encoding='utf-8') as file:
        file.write('\n'.join(lines))


def zip_and_info(out_path: str, zip_path: str) -> List[str]:
    with zipfile.ZipFile(zip_path, 'w', compression=zipfile.ZIP_DEFLATED) as archive:
        archive.write(out_path, arcname=os.path.basename(out_path))

    info_lines = []
    with zipfile.ZipFile(zip_path, 'r') as archive:
        for info in archive.infolist():
            info_lines.append(
                f'Name: {info.filename}; Compressed: {info.compress_size} bytes; '
                f'Original: {info.file_size} bytes; Date: {info.date_time}'
            )

    return info_lines


def build_report(analyzer: TextAnalyzer) -> List[str]:
    total_sentences = analyzer.count_sentences()
    declarative, interrogative, imperative = analyzer.count_sentence_types()
    avg_sentence_length = analyzer.avg_sentence_length_chars()
    avg_word_length = analyzer.avg_word_length()
    emoticons = analyzer.count_emoticons()
    dates = analyzer.find_dates()
    vowel_consonant_words = analyzer.words_last_vowel_prev_consonant()
    lowercase_count = analyzer.count_lowercase_letters()
    last_i_word, last_i_index = analyzer.last_word_with_i()
    cleaned_text = analyzer.text_exclude_start_i()

    lines = [
        f'Количество предложений: {total_sentences}',
        f'Повествовательные: {declarative}; Вопросительные: {interrogative}; Побудительные: {imperative}',
        f'Средняя длина предложения (символы слов): {avg_sentence_length:.2f}',
        f'Средняя длина слова: {avg_word_length:.2f}',
        f'Количество смайликов: {emoticons}',
        f'Список дат (dd-mm-yyyy): {dates}',
        f'Слова с последней гласной и предпоследней согласной: {vowel_consonant_words}',
        f'Количество строчных букв: {lowercase_count}',
    ]

    if last_i_word:
        lines.append(f"Последнее слово, содержащее 'i': {last_i_word}; номер: {last_i_index}")
    else:
        lines.append("Последнего слова с буквой 'i' нет")

    lines.extend([
        'Текст без слов, начинающихся с i:',
        cleaned_text,
    ])

    return lines


def main(input_file: str = INPUT_FILE):
    ensure_sample_input(input_file)

    with open(input_file, 'r', encoding='utf-8') as file:
        text = file.read()

    analyzer = TextAnalyzer(text)
    lines = build_report(analyzer)

    save_results(lines, OUT_TEXT)
    archive_info = zip_and_info(OUT_TEXT, OUT_ZIP)

    print('Результаты сохранены в', OUT_TEXT)
    print('Архив создан:', OUT_ZIP)
    print('Информация в архиве:')
    for info in archive_info:
        print(' -', info)


if __name__ == '__main__':
    main()
