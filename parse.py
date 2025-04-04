from bs4 import BeautifulSoup
from datetime import datetime
import re

SITE_SELECTORS = {
    "thefederalist.com": {
        "title": ["h1.title-lg", "h1.article-title"],
        "date": ["div.article-meta-date time[datetime]", "time.entry-date"],
        "content": ["div.article-content", "div.entry-content"]
    },

        # ================= DAILY WIRE =================
    "dailywire.com": {
        "title": ["h1.css-lwvlmc", "h1.headline"],
        "date": ["div.css-oxx0so time", "time[datetime]"],
        "content": ["div.e1gd2pcl0", "div.article-body"]
    },

        # ========== AMERICAN CONSERVATIVE ==========
    "theamericanconservative.com": {
        "title": ["h1.entry-title", "h1.title"],
        "date": ["time.entry-date", "time[datetime]"],
        "content": ["div.entry-content", "div.article-body"]
    },

        # ============ POST MILLENNIAL ============
    "thepostmillennial.com": {
        "title": ["h1.article__title", "h1.headline"],
        "date": ["div.article__date time", "time[datetime]"],
        "content": ["div.article__content", "article"]
    },

        # ============== FEDERALIST ===============
    "thefederalist.com": {
        "title": ["h1.title-lg", "h1.article-title"],
        "date": ["div.article-meta-date time[datetime]", "time.entry-date"],
        "content": ["div.article-content", "div.entry-content"]
    },

        # ============== SPECTATOR ===============
    "spectator.org": {
        "title": ["h1.article-title", "h1.title"],
        "date": ["time.article-date", "span.date"],
        "content": ["div.article-content", "div.body-content"]
    }
}
# Keep your existing format_date() and parse_news() functions


def parse_news(html):
    if not html:
        return {
            "title": "Scraping Failed",
            "date": "N/A",
            "content": "",
            "leaning": "far right"
        }
    
    soup = BeautifulSoup(html, "html.parser")
    domain = None
    
    # Improved domain detection
    canonical_link = soup.find('link', {'rel': 'canonical'}) or soup.find('meta', {'property': 'og:url'})
    if canonical_link:
        url = canonical_link.get('href') or canonical_link.get('content')
        for site in SITE_SELECTORS:
            if site in url:
                domain = site
                break

    selectors = SITE_SELECTORS.get(domain, {})
    
    # Title extraction with fallback
    title = "No Title Found"
    for selector in selectors.get("title", ["h1"]):
        if element := soup.select_one(selector):
            title = element.get_text(strip=True)
            break

    # Date extraction with improved parsing
    date_str = "N/A"
    for selector in selectors.get("date", ["time"]):
        if element := soup.select_one(selector):
            date_str = element.get("datetime") or element.get_text(strip=True)
            break

    # Content extraction with depth
    content = []
    for selector in selectors.get("content", ["article"]):
        if container := soup.select_one(selector):
            paragraphs = container.find_all(['p', 'h2', 'h3', 'blockquote'])
            content = [p.get_text(strip=True) for p in paragraphs if p.get_text(strip=True)]
            if content:
                break

    return {
        "title": title,
        "date": format_date(date_str),
        "content": "\n\n".join(content),
        "leaning": "far right"
    }

def format_date(raw_date):
    patterns = [
        "%Y-%m-%d",  # Their actual datetime format
        "%B %d, %Y",  # Fallback
        "%Y-%m-%dT%H:%M:%S%z"
    ]
    
    for pattern in patterns:
        try:
            return datetime.strptime(raw_date.strip()[:50], pattern).strftime("%Y-%m-%d %H:%M:%S")
        except:
            continue
    
    return raw_date.strip()[:50]  # Return raw date if all parsing fails