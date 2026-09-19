import os

COMMON_CRAWL_INDEX = os.getenv("COMMON_CRAWL_INDEX", "CC-MAIN-2026-30")
WET_LIMIT = int(os.getenv("WET_LIMIT", "100"))
DB_PATH = os.getenv("SEARCH_DB", "search.db")
