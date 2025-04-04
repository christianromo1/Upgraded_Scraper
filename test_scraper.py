# test_scraper.py
import os
from scrape import scrape_page
from parse import parse_news

TEST_URLS = [
    'https://www.dailywire.com/news/senate-confirms-dr-oz-as-head-of-medicare-and-medicaid-services',
    'https://www.theamericanconservative.com/how-to-solve-the-immigration-crisis/',
    'https://thepostmillennial.com/breaking-pro-life-activist-savannah-craven-beaten-and-bloodied-by-abortion-supporter-during-nyc-street-interview'
]

def test_scraping():
    # Create debug directory
    os.makedirs("debug_html", exist_ok=True)
    
    for url in TEST_URLS:
        print(f"\n=== Testing: {url} ===")
        
        try:
            # 1. Scrape page
            html = scrape_page(url)
            if not html:
                print("❌ Failed to get HTML")
                continue
                
            # 2. Save debug file
            filename = url.split('/')[-1].split('?')[0][:50] + ".html"
            with open(f"debug_html/{filename}", "w", encoding="utf-8") as f:
                f.write(html)
            
            # 3. Parse and print results
            article = parse_news(html)
            if not article:
                print("❌ Failed to parse HTML")
                continue
                
            print(f"✅ Title: {article.get('title', 'N/A')}")
            print(f"📅 Date: {article.get('date', 'N/A')}")
            print(f"📝 Content Preview: {article.get('content', '')[:200]}...")
            
        except Exception as e:
            print(f"🔥 Critical error: {str(e)}")

if __name__ == "__main__":
    test_scraping()