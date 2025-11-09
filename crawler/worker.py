import threading
from .fetcher import fetch_links
from .database import save_url

class CrawlerThread(threading.Thread):
    def __init__(self, url, visited, queue, base_domain):
        super().__init__()
        self.url = url
        self.visited = visited
        self.queue = queue
        self.base_domain = base_domain

    def run(self):
        if self.url in self.visited:
            return
        print(f"Crawling: {self.url}")
        self.visited.add(self.url)
        save_url(self.url)

        links = fetch_links(self.url)
        for link in links:
            if link not in self.visited:
                self.queue.append(link)
