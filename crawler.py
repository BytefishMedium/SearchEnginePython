import os

import requests
from bs4 import BeautifulSoup

visited_pages = set()  # record the visited pages
to_visit_pages = []  # record the pages to visit


def scrape_wikipedia_page(url):
    print(f"Visiting: {url}")
    visited_pages.add(url)

    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    if response.status_code != 200:
        print(f"Failed to process page {url}")
        return

    # save the page to a file
    title = url.split("/")[-1]
    with open(f"./wiki/{title}.html", "w") as f:
        f.write(response.text)

    # find all the wiki links in the page
    for link in soup.find_all('a', href=True):
        url: str = link['href']
        if url.startswith("/wiki/") and url.find(":") == -1:
            full_url = f"https://en.wikipedia.org{url}"
            if full_url not in visited_pages:
                to_visit_pages.append(full_url)


def scrape_wikipedia(start_url, max_pages):
    pages_visited = 0
    to_visit_pages.append(start_url)

    while len(to_visit_pages) > 0 and pages_visited < max_pages:
        url = to_visit_pages.pop(0)
        scrape_wikipedia_page(url)
        pages_visited += 1

    print(f"Total pages visited: {pages_visited}")


if __name__ == "__main__":
    start_url = 'https://en.wikipedia.org/wiki/Python_(programming_language)'

    # create  `wiki` folder if not exist
    folder_name = "wiki"
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)

    # Start scraping
    scrape_wikipedia(start_url, 500)
