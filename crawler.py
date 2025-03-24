# crawler.py (updated)
import time
import random
from scrape import scrape_page, extract_links
from parse import parse_news

class NewsCrawler:
    def __init__(self, start_urls, max_pages=10, use_proxy=False, use_cache=False):
        self.start_urls = start_urls
        self.max_pages = max_pages
        self.use_proxy = use_proxy  # Now properly handled
        self.use_cache = use_cache  # For future compatibility
        self.visited = set()
        self.results = []

    def _crawl(self, url):
        if url in self.visited or len(self.results) >= self.max_pages:
            return

        self.visited.add(url)
        print(f"\n🔍 Crawling: {url}")
        
        # Add random delay (2-5 seconds)
        time.sleep(random.uniform(2, 5))
        
        html = scrape_page(url)  # Proxy handled in scrape.py
        if not html:
            return

        article = parse_news(html)
        if article:
            self.results.append(article)
            print(f"✅ Found: {article['title'][:50]}...")

        links = extract_links(html, url)
        for link in links:
            if len(self.results) < self.max_pages:
                self._crawl(link)

    def run(self):
        for url in self.start_urls:
            self._crawl(url)
        return self.results