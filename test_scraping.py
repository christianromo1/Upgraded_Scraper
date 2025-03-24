# test_scraping.py
from scrape import scrape_page

html = scrape_page("https://www.reuters.com/technology")
if html:
    print(f"Scraped content length: {len(html)} characters")
else:
    print("Scraping failed")