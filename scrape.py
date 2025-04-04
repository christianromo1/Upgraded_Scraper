# scrape.py
from selenium.webdriver import Remote
from selenium.webdriver.chromium.remote_connection import ChromiumRemoteConnection
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException, WebDriverException
import time
import random

AUTH = 'brd-customer-hl_b8d12720-zone-ai_scraper:ndjc6153la1o'
SBR_WEBDRIVER = f'https://{AUTH}@brd.superproxy.io:9515'

def scrape_page(url):
    """Scrape webpage while preserving Federalist compatibility"""
    driver = None
    try:
        # 1. Initialize connection
        print(f"🌐 Connecting to Bright Data ({'Federalist' if 'thefederalist' in url else 'Other'})")
        chrome_options = Options()
        
        # Configuration that works for all sites
        chrome_options.add_argument("--headless=new")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
        
        # 2. Initialize driver with retries
        max_retries = 3
        for attempt in range(max_retries):
            try:
                sbr_connection = ChromiumRemoteConnection(SBR_WEBDRIVER, 'goog', 'chrome')
                driver = Remote(sbr_connection, options=chrome_options)
                driver.set_page_load_timeout(45 if 'dailywire' in url else 30)  # Longer for Daily Wire
                break
            except WebDriverException as e:
                if attempt == max_retries - 1:
                    raise
                time.sleep(random.uniform(2, 5))
                continue

        # 3. Load page with site-specific strategies
        print(f"🔄 Navigating to: {url}")
        
        if 'dailywire' in url:
            chrome_options.add_argument("--disable-blink-features=AutomationControlled")
            driver.set_page_load_timeout(60)  # Extended timeout
            driver.get(url)
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight/3);")
            WebDriverWait(driver, 45).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "h1,h2,article"))
            )
        elif 'thepostmillennial' in url:
            chrome_options.add_argument("--disable-web-security")
            driver.set_page_load_timeout(40)

        # 4. Return HTML
        print(f"✅ Successfully scraped {url}")
        return driver.page_source
        
    except Exception as e:
        print(f"❌ Failed to scrape {url}: {str(e)}")
        return None
    finally:
        if driver:
            driver.quit()

def extract_links(html, base_url):
    """Safe link extraction that won't break existing flows"""
    if not html:
        return []
        
    from bs4 import BeautifulSoup
    from urllib.parse import urljoin
    import re
    
    soup = BeautifulSoup(html, "html.parser")
    links = set()
    
    for a in soup.find_all("a", href=True):
        try:
            full_url = urljoin(base_url, a["href"])
            if re.match(r"https?://", full_url):
                links.add(full_url)
        except:
            continue
            
    return list(links)