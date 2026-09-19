import gzip, json, os, re, urllib.request
from .config import COMMON_CRAWL_INDEX

BASE = "https://data.commoncrawl.org/"
OUT = "search_engine/search_index.json"

def records(data):
    for block in re.split(br"(?=WARC/1\.[01]\r?\n)", data):
        if b"WARC-Type: conversion" not in block:
            continue
        sep = re.search(br"\r?\n\r?\n", block)
        if not sep:
            continue
        headers, body = block[:sep.start()], block[sep.end():]
        m = re.search(br"WARC-Target-URI:\s*(.+)", headers)
        if not m:
            continue
        url = m.group(1).decode("utf-8", "replace").strip()
        text = body.decode("utf-8", "replace").strip()
        if len(text) >= 80:
            yield {"url": url, "title": text.splitlines()[0][:180] or url, "text": text[:12000]}

def main():
    manifest = f"{BASE}crawl-data/{COMMON_CRAWL_INDEX}/wet.paths.gz"
    with urllib.request.urlopen(manifest, timeout=60) as r:
        paths = gzip.decompress(r.read()).decode("utf-8", "replace").splitlines()
    if not paths:
        raise RuntimeError("No WET files found")
    with urllib.request.urlopen(BASE + paths[0].strip(), timeout=600) as r:
        raw = gzip.decompress(r.read())
    docs = []
    for doc in records(raw):
        docs.append(doc)
        if len(docs) >= 20000:
            break
    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(docs, f, ensure_ascii=False, separators=(",", ":"))
    print(f"Built WET search index: {len(docs)} documents")

if __name__ == "__main__":
    main()
