from urllib.parse import urlparse

def is_same_domain(url, base_domain):
    try:
        return urlparse(url).netloc == base_domain
    except Exception:
        return False
