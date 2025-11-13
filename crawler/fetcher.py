import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

def fetch_links(url):
    """Fetch all valid links from the given URL."""
    try:
        resp = requests.get(url, timeout=5)
        if "text/html" not in resp.headers.get("Content-Type", ""):
            return []
        soup = BeautifulSoup(resp.text, "html.parser")
        links = set()
        for a in soup.find_all("a", href=True):
            link = urljoin(url, a['href'])
            if link.startswith("http"):
                links.add(link)
        return list(links)
    except Exception as e:
        # print("Fetch error:", e)  # Optional debug
        return []
