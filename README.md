# SEARCH — Common Crawl WET Search Engine

A minimal search engine that builds a local full-text index from Common Crawl WET files.

## Architecture

- **Downloader**: fetches Common Crawl WET records.
- **Indexer**: extracts plain text and creates a SQLite FTS5 index.
- **Search API**: FastAPI endpoint for full-text queries.
- **Web UI**: lightweight sand-colored search page.
- **No external search engine required**: results come from the local WET index.

## Quick start

```bash
pip install -r requirements.txt
python -m search_engine.download_wet --limit 100
python -m search_engine.index_wet
uvicorn search_engine.api:app --host 0.0.0.0 --port 8000
```

Open `http://localhost:8000`.

## Common Crawl

Set `COMMON_CRAWL_INDEX` to a Common Crawl index, for example:

```text
CC-MAIN-2026-30
```

The WET files contain extracted text. The indexer stores document URL, title, and searchable text locally.

## License

GNU GPL v3.0
