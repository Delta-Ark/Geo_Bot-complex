#!/usr/bin/python
# scraper.py
# Saito 2017

import urllib

import utils
from bs4 import BeautifulSoup


def scrape(url):
    html = urllib.urlopen(url).read()
    soup = BeautifulSoup(html, "html.parser")
    [x.extract() for x in soup.find_all('script')]
    text = soup.get_text(" ", strip=True)
    # ftext = text.split(" ")
    return text


def scrape_and_save_to_file(url, filename="scraped_text.txt"):
    text = scrape(url)
    utils.save_file(filename, text)
    return text


def main():
    url = "http://chrisnovello.com/teaching/risd/computer-utopias/"
    # text = scrape(url)
    text = scrape_and_save_to_file(url)
    print text
    

if __name__ == '__main__':
    main()

