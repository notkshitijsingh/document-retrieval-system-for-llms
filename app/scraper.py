import threading
import time
from .models import DocumentModel
from .utils import encode_text

def start_scraper():
    def scrape_task():
        while True:
            news_articles = scrape_news_articles()  # Replace with actual scraping logic
            for article in news_articles:
                DocumentModel.add_document(article)
            time.sleep(3600)  # Scrape every hour

    thread = threading.Thread(target=scrape_task)
    thread.daemon = True
    thread.start()

def scrape_news_articles():
    # Replace this with your actual news scraping logic
    return ["Example article 1", "Example article 2"]
