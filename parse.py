from bs4 import BeautifulSoup
from datetime import datetime

SITE_SELECTORS = {
    "default": {
        "title": ["h1", "h2.article-title"],
        "date": ["time", "span.date"],
        "content": ["article", "div.article-body"]
    },
    "reuters.com": {
        "title": "h1",
        "date": "time",
        "content": "div.article-body__content"
    },
    "vox.com": {
        "title": "h1.c-page-title",
        "date": "time.c-byline__item",
        "content": "div.c-entry-content"
    },
    "techcrunch.com": {
        "title": "h1.article__title",
        "date": "time.datetime",
        "content": "div.article-content"
    }
    
}

def parse_news(html):
    soup = BeautifulSoup(html, "html.parser")
    domain = None
    for site in SITE_SELECTORS:
        if site in str(soup.find("html")):
            domain = site
            break
    
    selectors = SITE_SELECTORS.get(domain, SITE_SELECTORS["default"])
    
    # Extract title
    title = "Untitled"
    for selector in selectors["title"]:
        if title_elem := soup.select_one(selector):
            title = title_elem.get_text(strip=True)
            break
    
    # Extract date
    date = "N/A"
    for selector in selectors["date"]:
        if date_elem := soup.select_one(selector):
            date = date_elem.get("datetime") or date_elem.get_text(strip=True)
            break
    
    # Extract content
    content = []
    for selector in selectors["content"]:
        if content_container := soup.select_one(selector):
            paragraphs = content_container.find_all(["p", "h2", "h3"])
            content = [p.get_text(strip=True) for p in paragraphs if p.get_text(strip=True)]
            break
    
    return {
        "title": title,
        "date": format_date(date),
        "content": "\n\n".join(content),
        "source": domain
    }

def format_date(raw_date):
    try:
        return datetime.strptime(raw_date[:19], "%Y-%m-%dT%H:%M:%S").isoformat()
    except:
        return raw_date