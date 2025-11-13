from urllib.parse import urlparse

def is_same_domain(url, base_domain):
    """Check if the given URL belongs to the same domain (including subdomains)."""
    try:
        netloc = urlparse(url).netloc
        return netloc == base_domain or netloc.endswith("." + base_domain)
    except Exception:
        return False
