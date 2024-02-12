import json
import string
import os
from math import log

from bs4 import BeautifulSoup

folder_path = 'wiki'
total_files = len([name for name in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, name))])

word_index = json.load(open('word_index.json', 'r'))


def normalize_string(input_string: str) -> str:
    translation_table = str.maketrans(string.punctuation, ' ' * len(string.punctuation))
    string_without_punc = input_string.translate(translation_table)
    string_without_double_spaces = ' '.join(string_without_punc.split())
    return string_without_double_spaces.lower()


# read all file in the wiki folder to get the documents
documents: dict[str, str] = {}
for filename in os.listdir(folder_path):
    file_path = os.path.join(folder_path, filename)
    current_url = f"https://en.wikipedia.org/wiki/{filename.split('.')[0]}"
    with open(file_path, 'r', encoding='utf-8') as file:
        html = file.read()
        soup = BeautifulSoup(html, 'html.parser')
        content = soup.get_text()
        documents[current_url] = content

# 计算document的平均长度
average_document_length = sum(len(d) for d in documents.values()) / len(documents)


def idf(keyword: str) -> float:
    N = total_files
    keyword_appeared_files = len(word_index.get(keyword, {}))
    return log((N - keyword_appeared_files + 0.5) / (keyword_appeared_files + 0.5) + 1)


def bm25(keyword: str) -> dict[str, float]:
    result = {}
    idf_score = idf(keyword)
    for url, freq in word_index.get(keyword, {}).items():
        numerator = freq * (1.5 + 1)
        denominator = freq + 1.5 * (1 - 0.75 + 0.75 * len(documents[url]) / average_document_length)
        result[url] = idf_score * numerator / denominator
    return result


def search(query: str) -> dict[str, float]:
    keywords = normalize_string(query).split(" ")
    url_scores: dict[str, float] = {}
    for kw in keywords:
        kw_urls_score = bm25(kw)
        for url, score in kw_urls_score.items():
            if url in url_scores:
                url_scores[url] += score
            else:
                url_scores[url] = score

    # rank the urls by scores
    url_scores = dict(sorted(url_scores.items(), key=lambda item: item[1], reverse=True))

    # only need top 10
    url_scores = dict(list(url_scores.items())[:10])
    return url_scores

if __name__ == "__main__":
    keyword = "python"
    print('idf of python is ', idf(keyword))

    print('bm25 of python is', bm25(keyword))

    query = "what is python flask"
    result = search(query)
    print(f"Search result for query:", result)

    # read param from user input and get the urls
    while True:
        query = input("Please input the query: ")
        result = search(query)
        print(f"Search result for query '{query}':")
        for url, score in result.items():
            print(f"{url}: {score}")
        if query == "exit":
            break
