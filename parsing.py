import requests
from bs4 import BeautifulSoup
import json
import os

base_url = "https://comtehno.kg/category/news/page/"
all_news = {}
page_number = 1


if not os.path.exists("data"):
    os.makedirs("data")


while True:
    page_url = f"{base_url}{page_number}"
    response = requests.get(page_url)
    soup = BeautifulSoup(response.content, "html.parser")


    if not soup.find(class_="blog-entry-title entry-title"):
        break


    with open(f"data/page{page_number}.html", "w", encoding="utf-8") as html_file:
        html_file.write(response.text)


    news_list = soup.find_all(class_="blog-entry-title entry-title")

    for news in news_list:
        news_title = news.text.strip()
        news_link = news.find_all("a", {"rel": "bookmark"})[0].get("href")
        all_news[news_title] = news_link


    page_number += 1


    print(f"Страница {page_number - 1} обработана")


with open("comtehno_news.json", "w", encoding="utf-8") as file:
    json.dump(all_news, file, ensure_ascii=False, indent=4)