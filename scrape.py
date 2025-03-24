from selenium.webdriver import Remote
from selenium.webdriver.chromium.remote_connection import ChromiumRemoteConnection
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import re

AUTH = 'brd-customer-hl_b8d12720-zone-ai_scraper:ndjc6153la1o'
SBR_WEBDRIVER = f'https://{AUTH}@brd.superproxy.io:9515'  # Use HTTPS endpoint

def scrape_page(url):
    try:
        print("🌐 Connecting to Scraping Browser...")
        
        # Create connection using Bright Data's recommended format
        sbr_connection = ChromiumRemoteConnection(SBR_WEBDRIVER, 'goog', 'chrome')
        
        # Configure Chrome options
        chrome_options = Options()
        chrome_options.add_argument("--headless=new")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        
        driver = Remote(sbr_connection, options=chrome_options)
        
        print(f"🔄 Navigating to: {url}")
        driver.get(url)
        html = driver.page_source
        print(f"✅ Successfully scraped {url}")
        
        return html
        
    except Exception as e:
        print(f"❌ Error scraping {url}: {str(e)}")
        return None
    finally:
        if 'driver' in locals():
            driver.quit()

def extract_links(html, base_url):
    soup = BeautifulSoup(html, "html.parser")
    links = set()
    
    for a in soup.find_all("a", href=True):
        href = a["href"]
        full_url = urljoin(base_url, href)
        if re.match(r"https?://", full_url):
            links.add(full_url)
    
    return list(links)