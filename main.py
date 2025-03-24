import streamlit as st
import asyncio
import json
from crawler import NewsCrawler

st.set_page_config(page_title="News Crawler", layout="wide")
st.title("🌐 AI News Crawler")

# Configuration
with st.sidebar:
    st.header("Settings")
    use_proxy = st.checkbox("Use Proxy Service", False)
    use_cache = st.checkbox("Use Google Cache", True)
    max_pages = st.slider("Max Pages to Crawl", 1, 100, 10)

# URL Input
start_urls = st.text_area("Enter Starting URLs (one per line):", height=100).split("\n")
start_urls = [url.strip() for url in start_urls if url.strip()]

if st.button("🚀 Start Crawling"):
    if start_urls:
        with st.spinner(f"Crawling up to {max_pages} pages..."):
            crawler = NewsCrawler(
                start_urls=start_urls,
                max_pages=max_pages,
                use_proxy=use_proxy,  # Now properly passed
                use_cache=use_cache   # Optional future use
            )
            results = crawler.run()
            
            st.session_state.results = results
            st.success(f"Found {len(results)} articles!")

# Download JSON
if "results" in st.session_state:
    json_data = json.dumps(st.session_state.results, indent=2)
    st.download_button(
        label="💾 Download JSON",
        data=json_data,
        file_name="news_articles.json",
        mime="application/json"
    )