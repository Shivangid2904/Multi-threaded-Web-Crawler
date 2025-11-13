import threading
import time
from .database import init_db, get_visited_urls, enqueue_url, dequeue_url, get_queue_count
from .worker import CrawlerThread

def start_crawler(start_url, max_threads=5, max_depth=2):
    init_db()
    visited = get_visited_urls()
    base_domain = start_url.split("//")[-1].split("/")[0]

    # Seed the queue
    enqueue_url(start_url, 0)

    pause_event = threading.Event()
    pause_event.set()  # Initially running

    def crawl_worker():
        while True:
            pause_event.wait()  # Respect pause
            url, depth = dequeue_url()
            if url is None:
                break
            crawler = CrawlerThread(url, depth, visited, base_domain, max_depth, pause_event)
            crawler.run()

    # Start threads
    threads = []
    for _ in range(max_threads):
        t = threading.Thread(target=crawl_worker)
        t.start()
        threads.append(t)

    # Status printer
    def status_printer():
        while any(t.is_alive() for t in threads):
            print(f"[Status] Threads: {max_threads} | Visited: {len(visited)} | Queued: {get_queue_count()} | Domain: {base_domain}")
            time.sleep(2)

    status_thread = threading.Thread(target=status_printer, daemon=True)
    status_thread.start()

    # Pause/resume input
    try:
        while any(t.is_alive() for t in threads):
            cmd = input("⏸️ Pause requested... Press Enter to resume or type 'exit' to stop.\n>>> ").strip().lower()
            if cmd == "exit":
                print("🛑 Stopping crawler...")
                break
            else:
                pause_event.set()
                print("▶️ Resuming crawl...")
    except KeyboardInterrupt:
        print("\n🛑 Keyboard interrupt detected. Stopping crawler...")

    for t in threads:
        t.join()
    print("🚪 Crawler exited cleanly.")
