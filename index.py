import os
from collections import defaultdict
import string
import json


# path to the folder containing the files
folder_path = 'wiki'

# word_index
word_index: dict[str, dict[str, int]] = defaultdict(lambda: defaultdict(int))


# remove punctuation and normalize the string
# all the words are converted to lower case
def normalize_string(input_string: str) -> str:
    translation_table = str.maketrans(string.punctuation, " " * len(string.punctuation))
    string_without_punc = input_string.translate(translation_table)
    string_without_double_spaces = " ".join(string_without_punc.split())
    return string_without_double_spaces.lower()


# get all the file names in the folder
filenames = os.listdir(folder_path)

# read all documents in wiki folder
for filename in filenames:
    file_path = os.path.join(folder_path, filename)
    current_url = f"https://en.wikipedia.org/wiki/{filename.split('.')[0]}"

    if os.path.isfile(file_path):
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
            words = normalize_string(content).split(" ")
            # Exclude words starting with numbers
            words = [word for word in words if not word[0].isdigit()]
            for word in words:
                word_index[word][current_url] += 1


# save the word_index to a file
with open('word_index.json', 'w') as f:
    json.dump(word_index, f, indent=4)
    print("word_index.json is saved.")
