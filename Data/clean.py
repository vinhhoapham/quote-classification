import os
import sys
import string
import time
from nltk import word_tokenize, download
from nltk.corpus import words, wordnet

download('words')
download('wordnet')
ENGLISH_WORDS = set(words.words())
PUNCTUATION = set(string.punctuation)


def is_valid_token(token):
    token_lower = token.lower()
    return (token_lower in ENGLISH_WORDS or
            len(wordnet.synsets(token_lower)) > 0 or
            token.isdigit() or
            token_lower in PUNCTUATION)


def is_english_sentence(sentence):
    tokens = word_tokenize(sentence)
    valid_token_count = sum(1 for token in tokens if is_valid_token(token))
    return (valid_token_count / len(tokens)) > 0.6


def clean_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    cleaned_lines = []
    start_time = time.time()

    for index, line in enumerate(lines, start=1):
        if is_english_sentence(line):
            cleaned_lines.append(line)

        elapsed_time = time.time() - start_time
        print(f"Processing {filepath}: {index}/{len(lines)} lines processed - Elapsed Time: {elapsed_time:.2f} seconds", end='\r')

    lines_removed = len(lines) - len(cleaned_lines)

    with open(filepath, 'w', encoding='utf-8') as file:
        file.writelines(cleaned_lines)

    print(f"\nFinished processing {filepath} - {len(cleaned_lines)} lines left")
    print(f"Number of lines removed: {lines_removed}")
    print(f"Total runtime: {time.time() - start_time:.2f} seconds")


if __name__ == "__main__":
    filename = sys.argv[1]
    clean_file(filename)
