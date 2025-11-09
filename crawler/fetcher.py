import requests
from bs4 import BeautifulSoup

def fetch_links(url):
    try:
        response = requests.get(url, timeout=5)
        if "text/html" not in response.headers.get("Content-Type", ""):
            return []
        soup = BeautifulSoup(response.text, "html.parser")
        links = set()
        for a in soup.find_all("a", href=True):
            link = a["href"]
            if link.startswith("http"):
                links.add(link)
        return list(links)
    except Exception:
        return []
