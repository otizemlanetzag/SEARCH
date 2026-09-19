import argparse
import gzip
import urllib.request
from .config import COMMON_CRAWL_INDEX, WET_LIMIT

BASE = "https://data.commoncrawl.org/"

def get_wet_paths(crawl):
    url = f"{BASE}crawl-data/{crawl}/wet.paths.gz"
    with urllib.request.urlopen(url, timeout=60) as r:
        manifest = gzip.decompress(r.read()).decode("utf-8", "replace")
    for line in manifest.splitlines():
        if line.strip():
            yield line.strip()

def download_wet(path):
    req = urllib.request.Request(BASE + path, headers={"User-Agent": "SEARCH/1.0"})
    with urllib.request.urlopen(req, timeout=300) as r:
        return gzip.decompress(r.read())

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--limit",type=int,default=WET_LIMIT)
    p.add_argument("--out",default="wet-data")
    args=p.parse_args()
    import os
    os.makedirs(args.out,exist_ok=True)
    for i,path in enumerate(get_wet_paths(COMMON_CRAWL_INDEX)):
        if i>=args.limit: break
        data=download_wet(path)
        with open(f"{args.out}/{i:05d}.wet","wb") as f: f.write(data)
        print(f"downloaded {i+1}: {path}")

if __name__=="__main__":
    main()
