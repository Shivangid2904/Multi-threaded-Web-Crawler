import threading
from .fetcher import fetch_links
from .database import save_url, enqueue_url
from .utils import is_same_domain

class CrawlerThread(threading.Thread):
    def __init__(self, url, depth, visited, base_domain, max_depth, pause_event):
        super().__init__()
        self.url = url
        self.depth = depth
        self.visited = visited
        self.base_domain = base_domain
        self.max_depth = max_depth
        self.pause_event = pause_event

    def run(self):
        if self.url in self.visited:
            return

        print(f"Crawling (depth {self.depth}): {self.url}")
        self.visited.add(self.url)
        save_url(self.url)

        if self.depth >= self.max_depth:
            return

        # Respect pause
        self.pause_event.wait()

        links = fetch_links(self.url)
        for link in links:
            if is_same_domain(link, self.base_domain) and link not in self.visited:
                enqueue_url(link, self.depth + 1)
