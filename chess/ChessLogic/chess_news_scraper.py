import requests
from bs4 import BeautifulSoup
import json
import time
import random
import xml.etree.ElementTree as ET
from datetime import datetime
import os


def scrape_chesscom():
    print("Scraping chess.com/news...")
    url = "https://www.chess.com/news"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5",
    }
    try:
        res = requests.get(url, headers=headers, timeout=10)
        res.raise_for_status()
        soup = BeautifulSoup(res.text, "html.parser")

        news = []
        articles = soup.find_all("a", class_="post-preview-title", limit=5)

        print(f"Found {len(articles)} articles")

        for article in articles:
            title_text = article.text.strip()
            href = article.get("href")

            if title_text and href:
                if href and not href.startswith("http"):
                    href = "https://www.chess.com" + href

                news.append(
                    {
                        "source": "chess.com",
                        "title": title_text,
                        "link": href,
                        "date": datetime.now().strftime("%Y-%m-%d"),
                    }
                )
                print(f"Added article: {title_text}")

        return news
    except Exception as e:
        print(f"Error scraping chess.com: {e}")
        return [
            {
                "source": "chess.com",
                "title": "Chess.com News (Fallback)",
                "link": "https://www.chess.com/news",
                "date": datetime.now().strftime("%Y-%m-%d"),
            }
        ]


def scrape_fide():
    print("Scraping FIDE feed...")
    url = "https://www.fide.com/feed"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Accept": "application/rss+xml, application/xml",
    }

    try:
        res = requests.get(url, headers=headers, timeout=10)
        res.raise_for_status()
        root = ET.fromstring(res.content)
        news = []

        channel = root.find("channel")
        if channel is not None:
            items = channel.findall("item")
            print(f"Found {len(items)} articles")

            for item in items[:5]:
                title = item.find("title")
                link = item.find("link")
                pub_date = item.find("pubDate")

                if title is not None and link is not None:
                    date_str = datetime.now().strftime("%Y-%m-%d")
                    if pub_date is not None and pub_date.text:
                        try:
                            date_obj = datetime.strptime(
                                pub_date.text, "%a, %d %b %Y %H:%M:%S %z"
                            )
                            date_str = date_obj.strftime("%Y-%m-%d")
                        except:
                            pass

                    news.append(
                        {
                            "source": "fide.com",
                            "title": title.text,
                            "link": link.text,
                            "date": date_str,
                        }
                    )
                    print(f"Added article: {title.text}")

        return news
    except Exception as e:
        print(f"Error scraping FIDE RSS: {e}")
        return [
            {
                "source": "fide.com",
                "title": "FIDE News (Fallback)",
                "link": "https://www.fide.com/news",
                "date": datetime.now().strftime("%Y-%m-%d"),
            }
        ]


def scrape_lichess():
    print("[+] Scraping Lichess Atom feed...")
    url = "https://lichess.org/blog.atom"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Accept": "application/atom+xml",
    }

    try:
        res = requests.get(url, headers=headers, timeout=10)
        res.raise_for_status()
        print(f"Status code: {res.status_code}")

        root = ET.fromstring(res.content)
        news = []

        namespace = {"atom": "http://www.w3.org/2005/Atom"}
        entries = root.findall("atom:entry", namespace)
        print(f"Found {len(entries)} articles")

        for entry in entries[:5]:
            title = entry.find("atom:title", namespace)
            link = entry.find("atom:link", namespace)
            published = entry.find("atom:published", namespace)

            if title is not None and link is not None:
                date_str = datetime.now().strftime("%Y-%m-%d")
                if published is not None and published.text:
                    try:
                        date_obj = datetime.strptime(
                            published.text, "%Y-%m-%dT%H:%M:%SZ"
                        )
                        date_str = date_obj.strftime("%Y-%m-%d")
                    except:
                        pass

                news.append(
                    {
                        "source": "lichess.org",
                        "title": title.text,
                        "link": link.get("href"),
                        "date": date_str,
                    }
                )
                print(f"Added article: {title.text}")

        return news
    except Exception as e:
        print(f"Error scraping Lichess Atom feed: {e}")
        return [
            {
                "source": "lichess.org",
                "title": "Lichess News (Fallback)",
                "link": "https://lichess.org/blog",
                "date": datetime.now().strftime("%Y-%m-%d"),
            }
        ]


def get_all_news():
    """Get news from all sources and return them as a dictionary with source-specific lists"""
    all_news = []

    cached_news = load_cached_news()
    if cached_news:
        return cached_news

    chesscom_news = scrape_chesscom()
    all_news.extend(chesscom_news)
    time.sleep(random.uniform(1, 5))

    fide_news = scrape_fide()
    all_news.extend(fide_news)
    time.sleep(random.uniform(1, 5))

    lichess_news = scrape_lichess()
    all_news.extend(lichess_news)

    news_by_source = {"all_news": all_news}

    save_news_to_cache(news_by_source)

    print("[✓] News saved to cache")
    return news_by_source


def load_cached_news():
    try:
        if os.path.exists("chess_news.json"):
            if time.time() - os.path.getmtime("chess_news.json") < 3600:
                with open("chess_news.json", "r", encoding="utf-8") as f:
                    all_news = json.load(f)

                news_by_source = {
                    "chesscom_news": [
                        article
                        for article in all_news
                        if article["source"] == "chess.com"
                    ],
                    "fide_news": [
                        article
                        for article in all_news
                        if article["source"] == "fide.com"
                    ],
                    "lichess_news": [
                        article
                        for article in all_news
                        if article["source"] == "lichess.org"
                    ],
                    "all_news": all_news,
                }

                return news_by_source
    except Exception as e:
        print(f"Error loading cached news: {e}")

    return None


def save_news_to_cache(news_by_source):
    try:
        with open("chess_news.json", "w", encoding="utf-8") as f:
            json.dump(news_by_source["all_news"], f, indent=2, ensure_ascii=False)
    except Exception as e:
        print(f"Error saving news to cache: {e}")


def main():
    news_by_source = get_all_news()

    print("\n📰 Latest Chess News:\n")
    if not news_by_source["all_news"]:
        print(" No news found at this moment.")
    else:
        for article in news_by_source["all_news"]:
            print(f"→ [{article['source']}] {article['title']}")
            print(f"   {article['link']}\n")


if __name__ == "__main__":
    main()
