import json
import re
from pathlib import Path

INDEX=Path(__file__).with_name("search_index.json")

def search(query,limit=20):
    if not INDEX.exists():
        return []
    docs=json.loads(INDEX.read_text(encoding="utf-8"))
    terms=[x.lower() for x in re.findall(r"\w+",query,flags=re.UNICODE) if len(x)>1]
    if not terms:
        return []
    scored=[]
    for d in docs:
        hay=(d.get("title","")+" "+d.get("text","")).lower()
        score=sum(hay.count(t) for t in terms)
        if score:
            pos=min((hay.find(t) for t in terms if hay.find(t)>=0),default=0)
            source=d.get("text","")
            snippet=source[max(0,pos-120):pos+400].replace("\n"," ")
            scored.append((score,d.get("url",""),d.get("title",""),snippet))
    scored.sort(reverse=True,key=lambda x:x[0])
    return [{"url":u,"title":t or u,"snippet":s} for _,u,t,s in scored[:limit]]
