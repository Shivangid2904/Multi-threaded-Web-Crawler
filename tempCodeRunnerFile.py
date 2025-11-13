from crawler.main import start_crawler

if __name__ == "__main__":
    start_crawler("https://example.com", max_threads=3, max_depth=2)
