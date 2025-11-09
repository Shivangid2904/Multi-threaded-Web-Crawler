import threading
import time
from urllib.parse import urlparse
from .database import init_db, get_visited_urls
from .worker import CrawlerThread

def start_crawler(start_url, max_threads=5, max_depth=2):
    init_db()
    visited = get_visited_urls()
    queue = [(start_url, 0)]
    base_domain = urlparse(start_url).netloc

    while queue:
        threads = []
        while queue and len(threads) < max_threads:
            url, depth = queue.pop(0)
            if depth < max_depth:
                thread = CrawlerThread(url, visited, queue, base_domain)
                thread.start()
                threads.append(thread)

        for thread in threads:
            thread.join()

        time.sleep(1)

    print("\n✅ Crawling completed!")
    print(f"Total URLs visited: {len(visited)}")

if __name__ == "__main__":
    start_crawler("https://example.com")
