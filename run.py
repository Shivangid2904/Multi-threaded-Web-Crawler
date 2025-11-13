from crawler.main import start_crawler

if __name__ == "__main__":
    start_crawler("http://github.com", max_threads=5, max_depth=2)