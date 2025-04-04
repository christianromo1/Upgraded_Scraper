# main.py (updated for CSV output)
import streamlit as st
import csv
import io
from datetime import datetime
from crawler import NewsCrawler

st.set_page_config(page_title="Right-Leaning News Scraper", layout="wide")
st.title("🇺🇸 Conservative News Scraper")

# Configuration
with st.sidebar:
    st.header("Settings")
    use_proxy = st.checkbox("Use Proxy Service", True)
    max_pages = st.slider("Max Pages to Crawl", 1, 100, 10)

# URL Input
start_urls = st.text_area("Enter Starting URLs (one per line):", height=100, value="\n".join([
    "https://www.dailywire.com/",
    "https://www.theamericanconservative.com/",
    "https://thepostmillennial.com/",
    "https://spectator.org/",
    "https://thefederalist.com/"
])).split("\n")

if st.button("🚀 Start Scraping"):
    if start_urls:
        with st.spinner(f"Scraping up to {max_pages} articles..."):
            crawler = NewsCrawler(
                start_urls=start_urls,
                max_pages=max_pages,
                use_proxy=use_proxy
            )
            results = crawler.run()
            
            st.session_state.results = results
            st.success(f"Successfully collected {len(results)} articles!")

            # Display results
            for idx, article in enumerate(results, 1):
                with st.expander(f"Article {idx}: {article.get('title', '')}"):
                    st.write(f"**Date:** {article.get('date', 'N/A')}")
                    st.write(f"**Leaning:** {article.get('leaning', 'far right')}")
                    st.write(article.get('content', ''))

# CSV Download
if "results" in st.session_state:
    csv_buffer = io.StringIO()
    csv_writer = csv.DictWriter(csv_buffer, fieldnames=['title', 'date', 'content', 'leaning'])
    csv_writer.writeheader()
    
    for article in st.session_state.results:
        csv_writer.writerow({
            'title': article.get('title', ''),
            'date': article.get('date', ''),
            'content': article.get('content', ''),
            'leaning': 'far right'
        })
    
    current_time = datetime.now().strftime("%Y%m%d_%H%M%S")
    st.download_button(
        label="📥 Download CSV",
        data=csv_buffer.getvalue(),
        file_name=f"conservative_news_{current_time}.csv",
        mime="text/csv"
    )