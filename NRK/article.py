import time
from typing import List

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from util import soup

SEARCH_HIT_CLS = "nrkno-search-hit__content"  # <div class=...>
SEARCH_HIT_TYPE = "nrkno-search-hit__details"  # <small class=...>


def process_article(driver: WebDriver, url: str) -> dict:
    """
    Process an article given the driver and URL.

    Args:
        driver (WebDriver): The Selenium WebDriver instance.
        url (str): The URL of the article.

    Returns:
        dict: A dictionary containing the processed article data.
    """
    driver.get(url)
    nyhet = soup(driver.page_source)
    # find a div that contains the class "fact-reference"
    div = nyhet.find("div", {"class": "fact-reference"})
    summaries = []
    if div is not None:
        for li in div.find_all("li"):
            summaries.append(li.text)

    # find all figure captions, that is,
    # any p under a <figure> tag
    figure_captions = []
    for figure in nyhet.find_all("figure"):
        for p in figure.find_all("p"):
            figure_captions.append(p.text)

    # title is the first h1 with class article-title:
    title = nyhet.find("h1", {"class": "article-title"}).text
    # lead is the <p> tag inside the div with class article-lead
    lead = nyhet.find("div", {"class": "article-lead"}).find("p").text

    text = []
    # text is all contained within article-body class
    body = nyhet.find("div", {"class": "article-body"})
    for p in body.find_all("p"):
        # only non-class p:
        if p.get("class") is None:
            txt = p.text.strip()
            if len(txt) > 0:
                text.append(txt)

    author = []
    author_classes = ["author__name"]
    for a in nyhet.select("a"):
        a_class = a.get("class")
        if a_class is not None and a_class[0] in author_classes:
            author.append(a.text)

    # time is the spans inside <time> with class datePublished
    time = nyhet.find("time", {"class": "datePublished"})
    if time is not None and time.find("span") is not None:
        time = time.find("span").text
    else:
        time = str(time)
    return {
        "url": url,
        "title": title,
        "lead": lead,
        "author": author,
        "datetime": time,
        "text": text,
        "summary": summaries,
        "captions": figure_captions,
    }


def get_article_urls(driver, search_term: str, max_count: int = 100) -> List[str]:
    """
    Get a list of article URLs for a given search term.

    Args:
        search_term (str): The search term.
        max_count (int, optional): The maximum number of articles to fetch. Defaults to 100.

    Returns:
        List[str]: A list of article URLs.
    """
    urls = []
    if max_count < 20:
        raise ValueError("max_count must be at least 20")
    num_batches = max_count // 20
    for index in range(0, num_batches):
        print(f"Fetching batch {index+1}/{num_batches}...")
        index = index * 20
        url = f"https://www.nrk.no/sok/?q={search_term}&scope=nrkno&from={index}"
        driver.get(url)
        time.sleep(0.5)
        # fetch all search_hits and retrieve urls
        search_hits = driver.find_elements(By.CLASS_NAME, SEARCH_HIT_CLS)

        for hit in search_hits:
            details = hit.find_element(By.CLASS_NAME, SEARCH_HIT_TYPE)
            if "Artikkel" in details.text:
                urls.append(hit.find_element(By.TAG_NAME, "a").get_attribute("href"))
    print(f"Found {len(urls)} articles for '{search_term}'.")
    return urls
