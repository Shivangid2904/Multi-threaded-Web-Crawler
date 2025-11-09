Multi-Threaded Web Crawler

A Python-based multi-threaded web crawler that efficiently fetches and stores URLs while supporting resume functionality. It uses threading for parallel crawling and SQLite for persistence.

🚀 Features

Multi-threaded crawling for faster performance

Resume from last crawl using SQLite database

Simple, modular design (easy to extend)

Graceful handling of invalid or duplicate URLs

🧠 How It Works

Fetches the starting URL and extracts all valid links.

Each thread handles a subset of URLs concurrently.

Visited links are stored in a local database to avoid repetition.

Crawl can resume later using saved data.

⚙️ Usage
pip install -r requirements.txt
python run.py https://example.com

📂 Project Structure
crawler/
├── main.py        # Entry point
├── worker.py      # Thread logic
├── database.py    # SQLite operations
├── fetcher.py     # Fetch & parse links
└── utils.py       # Helper functions