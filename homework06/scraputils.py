# type: ignore
import random
import time

import requests
from bs4 import BeautifulSoup


def extract_news(parser):
    """Extract news from a given web page"""
    news_list = []

    if len(parser.findAll("table")) < 3:
        print(parser.findAll("table"))
    body = parser.findAll("table")[2]
    all_titles = [title.text for title in body.findAll("a", {"class": "titlelink"})]
    all_authors = [user.text for user in body.findAll("a", {"class": "hnuser"})]
    all_urls = [link["href"] for link in body.findAll("a", {"class": "titlelink"})]
    all_urls = [
        "https://news.ycombinator.com/" + url if url[:4] == "item" else url for url in all_urls
    ]
    all_points = [score.text.split()[0] for score in body.findAll("span", {"class": "score"})]
    all_ids = [post["id"] for post in body.findAll("tr", {"class": "athing"})]
    all_discussions = [
        body.findAll("span", {"id": f"unv_{id}"})[0].findNext("a", {"href": f"item?id={id}"}).text
        for id in all_ids
    ]
    all_comments = [
        0 if element.isalpha() else int(element.split()[0]) for element in all_discussions
    ]

    for i, n in enumerate(all_titles):
        news_list.append(
            {
                "author": all_authors[i],
                "comments": all_comments[i],
                "points": all_points[i],
                "title": all_titles[i],
                "url": all_urls[i],
            }
        )

    return news_list


def extract_next_page(parser):
    """Extract next page URL"""
    next_page = parser.findAll("table")[2].findAll("a", {"class": "morelink"})[0]["href"]
    return next_page


def get_news(url, n_pages=1):
    """Collect news from a given web page"""
    news = []
    for i in range(n_pages):
        print("Collecting data from page: {}".format(url))
        headers = {
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
            "accept-encoding": "gzip, deflate, br",
            "accept-language": "uk,en-US;q=0.9,en;q=0.8,ru;q=0.7",
            "sec-ch-ua": '"Google Chrome";v="89", "Chromium";v="89", ";Not A Brand";v="99"',
            "sec-ch-ua-mobile": "?0",
            "sec-fetch-dest": "document",
            "sec-fetch-mode": "navigate",
            "sec-fetch-site": "none",
            "sec-fetch-user": "?1",
            "upgrade-insecure-requests": "1",
            "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36",
        }
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, "html.parser")
        news_list = extract_news(soup)
        next_page = extract_next_page(soup)
        url = "https://news.ycombinator.com/" + next_page
        news.extend(news_list)
    return news


# print(get_news("https://news.ycombinator.com/newest", n_pages=35)[:4])
