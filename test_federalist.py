# test_federalist.py
from scrape import scrape_page
from parse import parse_news

FEDERALIST_URL = "https://thefederalist.com/2024/04/03/mastercard-backtracks-after-getting-caught-using-ad-dollars-to-censor-conservatives/"

def test_federalist():
    print("=== Testing Federalist ===")
    html = scrape_page(FEDERALIST_URL)
    
    if not html:
        print("❌ Federalist scraping failed")
        return
        
    with open("debug_federalist.html", "w", encoding="utf-8") as f:
        f.write(html)
    
    article = parse_news(html)
    print(f"Title: {article.get('title', 'N/A')}")
    print(f"Date: {article.get('date', 'N/A')}")
    print(f"Content: {article.get('content', 'N/A')[:200]}...")

if __name__ == "__main__":
    test_federalist()