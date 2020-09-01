from collections import Counter
import random

WORDS = "words.txt"
BIG_WORDS = "bigWords.txt"
ALL_WORDS = "allWords.txt"


def process_words() -> None:
    with open(WORDS) as data:
        with open(BIG_WORDS, 'w') as bigWords:
            with open(ALL_WORDS, 'w') as allWords:
                for word in data:
                    word = word.lower().strip()
                    if len(word) > 6:
                        print(word, file=bigWords)
                    if len(word) > 2:
                        print(word, file=allWords)


def get_source_word():
    with open(BIG_WORDS) as bW:
        word = random.choice(bW.readlines())
    return word.strip()


def check_letters(sourceword: str, checkword: str) -> str:
    letters = []
    checkword_counter = Counter(checkword)
    sourceword_counter = Counter(sourceword)
    for a, b in checkword_counter.items():
        if sourceword_counter[a] < b:
            letters.append((a, False))
        if sourceword_counter[a] > b:
            letters.append((a, True))
    return letters


def check_size(words: list, size: int = 3) -> list:
    length = []
    for word in words:
        if len(word) >= size:
            length.append((word, True))
        else:
            length.append((word, False))
    return length


def check_duplicates(words: list) -> list:
    if len(words) > len(set(words)):
        return True


def check_source_word(words: list, sourceword: str) -> list:
    for word in words:
        if word == sourceword:
            return words
