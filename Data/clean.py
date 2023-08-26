import os
import sys
import string
import time
from nltk import word_tokenize
from nltk.corpus import words, wordnet

# Load words and punctuation into sets for faster lookup
ENGLISH_WORDS = set(words.words())
PUNCTUATION = set(string.punctuation)


def is_valid_token(token):
    """Check if a token is recognized as an English word, a number, or punctuation."""
    token_lower = token.lower()

    return (token_lower in ENGLISH_WORDS or
            len(wordnet.synsets(token_lower)) > 0 or
            token.isdigit() or
            token_lower in PUNCTUATION)


def is_english_sentence(sentence):
    """Check if the majority of tokens in a sentence are recognized as English."""
    tokens = word_tokenize(sentence)
    valid_token_count = sum(1 for token in tokens if is_valid_token(token))
    return (valid_token_count / len(tokens)) > 0.6


def clean_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    # Filter out lines that aren't mostly English
    cleaned_lines = []
    start_time = time.time()  # Track the start time for the operation

    for index, line in enumerate(lines, start=1):
        if is_english_sentence(line):
            cleaned_lines.append(line)

        elapsed_time = time.time() - start_time
        # Print progress along with elapsed time
        print(f"Processing {filepath}: {index}/{len(lines)} lines processed - Elapsed Time: {elapsed_time:.2f} seconds",
              end='\r')

    lines_removed = len(lines) - len(cleaned_lines)

    # Write cleaned lines back to the file
    with open(filepath, 'w', encoding='utf-8') as file:
        file.writelines(cleaned_lines)

    print(f"\nFinished processing {filepath} - {len(cleaned_lines)} lines left")
    print(f"Number of lines removed: {lines_removed}")
    print(f"Total runtime: {time.time() - start_time:.2f} seconds")


if __name__ == "__main__":
    filename = sys.argv[1]  # Get the filename from the command line arguments
    clean_file(filename)
