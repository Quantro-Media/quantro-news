import time
import requests
import feedparser
from bs4 import BeautifulSoup

HEADERS = {"User-Agent": "Mozilla/5.0 (compatible; AI-Intel-Publisher/1.0)"}

def fetch_rss(urls, max_items=15):
    items = []
    for u in urls:
        try:
            feed = feedparser.parse(u)
            for entry in feed.entries[:max_items]:
                items.append({
                    "title": entry.get("title", ""),
                    "link": entry.get("link", ""),
                    "summary": entry.get("summary", "")
                })
        except Exception:
            continue
    return items

def fetch_page_snippet(url, max_chars=1200):
    try:
        resp = requests.get(url, timeout=10, headers=HEADERS)
        resp.raise_for_status()
        html = resp.text
        soup = BeautifulSoup(html, "html.parser")
        paragraphs = soup.select("p")
        text = " ".join(p.get_text(" ", strip=True) for p in paragraphs)
        return text[:max_chars]
    except Exception:
        return ""

def fetch_web(urls):
    data = []
    for u in urls:
        snippet = fetch_page_snippet(u)
        if snippet:
            data.append({
                "title": u,
                "link": u,
                "summary": snippet
            })
        time.sleep(1)
    return data
