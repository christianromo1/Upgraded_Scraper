# crawler.py
from urllib.parse import urljoin  # <-- Add this import
from bs4 import BeautifulSoup  # <-- Add this import
from scrape import scrape_page
from parse import parse_news
import re
import time
import random

class NewsCrawler:
    def _crawl(self, url):
        if "dailywire.com" in url:
            print(f"⏭️ Skipping Daily Wire (temp): {url}")
            return
        
    def __init__(self, start_urls, max_pages=10, use_proxy=True):
        self.start_urls = start_urls
        self.max_pages = max_pages
        self.use_proxy = use_proxy
        self.visited = set()
        self.results = []
        self.article_pattern = re.compile(
            r'/article/|/news/|/blog/|/opinion/|/\d{4}/\d{2}/\d{2}/'
        )

    def _crawl(self, url):
        if url in self.visited or len(self.results) >= self.max_pages:
            return

        self.visited.add(url)
        print(f"\n🔍 Crawling: {url}")
        
        try:
            html = scrape_page(url)
            if not html:
                return

            article = parse_news(html)
            if article['title'] != "No Title Found":
                self.results.append(article)
                print(f"✅ Found: {article['title'][:60]}...")

            # Add delay between requests
            time.sleep(random.uniform(1, 3))
            
            # Continue crawling with proper HTML parsing
            soup = BeautifulSoup(html, "html.parser")
            for link in soup.find_all('a', href=True):
                full_url = urljoin(url, link['href'])
                if self.article_pattern.search(full_url):
                    self._crawl(full_url)

        except Exception as e:
            print(f"⚠️ Error: {str(e)}")

    def run(self):
        for url in self.start_urls:
            self._crawl(url)
        return self.results