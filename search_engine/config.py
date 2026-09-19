import os

COMMON_CRAWL_INDEX = os.getenv("COMMON_CRAWL_INDEX", "CC-MAIN-2026-34")
WET_LIMIT = int(os.getenv("WET_LIMIT", "2"))
DB_PATH = os.getenv("SEARCH_DB", "search.db")
