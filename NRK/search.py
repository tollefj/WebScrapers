import argparse
import os

import jsonlines
from article import get_article_urls, process_article
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("query", help="Query/search term")
    parser.add_argument(
        "-c", "--count", help="Number of articles to fetch", type=int, default=20
    )
    parser.add_argument("-o", "--output", help="Output folder", default="data")

    args = parser.parse_args()

    os.makedirs(args.output, exist_ok=True)

    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))

    urls = get_article_urls(
        driver,
        args.query,
        max_count=args.count,
    )

    outfile = f"{args.output}/{args.query}.jsonl"
    with jsonlines.open(outfile, "w") as writer:
        for url in urls:
            article = process_article(driver, url)
            writer.write(article)


if __name__ == "__main__":
    main()
