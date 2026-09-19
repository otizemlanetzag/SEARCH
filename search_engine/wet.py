import gzip
import io
import re
from typing import Iterator

def iter_wet_records(raw: bytes) -> Iterator[tuple[str,str,str]]:
    # WARC/WET records are separated by WARC headers. We only index
    # conversion records containing the extracted plain text.
    for block in re.split(br"(?=WARC/1\.[01]\r?\n)", raw):
        if b"WARC-Type: conversion" not in block:
            continue
        sep = re.search(br"\r?\n\r?\n", block)
        if not sep:
            continue
        headers, body = block[:sep.start()], block[sep.end():]
        m = re.search(br"WARC-Target-URI:\s*(.+)", headers)
        if not m:
            continue
        url = m.group(1).decode("utf-8","replace").strip()
        text = body.decode("utf-8","replace").strip()
        title = text.splitlines()[0][:200] if text else url
        yield url, title, text
