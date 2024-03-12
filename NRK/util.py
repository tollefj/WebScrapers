from bs4 import BeautifulSoup
from selenium import webdriver


def get_driver():
    # see https://chromedriver.chromium.org/downloads
    # place in dir
    driver = webdriver.Chrome("chromedriver-mac-arm64/chromedriver")
    return driver


def soup(html, parser="html.parser"):
    return BeautifulSoup(html, parser)
