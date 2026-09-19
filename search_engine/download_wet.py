import argparse
import gzip
import io
import json
import urllib.request
from .config import COMMON_CRAWL_INDEX, WET_LIMIT

BASE = "https://data.commoncrawl.org/"

def get_wet_paths(index_name):
    url=f"https://index.commoncrawl.org/{index_name}-index?url=*&output=json&filter=status:200"
    with urllib.request.urlopen(url, timeout=60) as r:
        for line in r:
            try:
                obj=json.loads(line)
            except json.JSONDecodeError:
                continue
            path=obj.get("filename")
            offset=int(obj.get("offset",0))
            length=int(obj.get("length",0))
            if path:
                yield path,offset,length

def download_record(path, offset, length):
    req=urllib.request.Request(
        BASE+path,
        headers={"Range":f"bytes={offset}-{offset+length-1}"}
    )
    with urllib.request.urlopen(req, timeout=120) as r:
        return gzip.GzipFile(fileobj=io.BytesIO(r.read())).read()

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--limit",type=int,default=WET_LIMIT)
    p.add_argument("--out",default="wet-data")
    args=p.parse_args()
    import os
    os.makedirs(args.out,exist_ok=True)
    for i,(path,offset,length) in enumerate(get_wet_paths(COMMON_CRAWL_INDEX)):
        if i>=args.limit: break
        data=download_record(path,offset,length)
        with open(f"{args.out}/{i:05d}.wet","wb") as f: f.write(data)
        print(f"downloaded {i+1}: {path}")
if __name__=="__main__":
    main()
