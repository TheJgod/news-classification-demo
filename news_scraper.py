import feedparser
import pyshorteners
import pandas as pd
from datetime import datetime

def shorten_url(url):
    s = pyshorteners.Shortener()
    try:
        return s.tinyurl.short(url)
    except:
        return url

def parse_date(date_str):
    parsed_date = datetime.strptime(date_str, "%a, %d %b %Y %H:%M:%S %Z")
    return parsed_date.strftime("%d/%m/%Y")

def clean_title(title):
    return title.rsplit(" - ", 1)[0].strip()

def fetch_news(search_terms, max_articles):
    news_data = []
    for term in search_terms:
        gn_url = f"https://news.google.com/rss/search?q={term.replace(' ', '+')}&hl=en-US&gl=US&ceid=US:en"
        gn_feed = feedparser.parse(gn_url)
        for item in gn_feed.entries[:max_articles]:
            news_data.append({
                "Headline": clean_title(item.title),
                "URL": shorten_url(item.link),
                "Published": parse_date(item.published),
                "Source": item.source.get("title"),
                "Source URL": item.source.get("href"),
            })
    return pd.DataFrame(news_data)