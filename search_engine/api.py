from fastapi import FastAPI, Query
from fastapi.responses import HTMLResponse
from .db import search

app=FastAPI(title="SEARCH — Common Crawl")

HTML="""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Sandstorm Search</title>
<style>
body{margin:0;background:#F5F2EB;color:#3E2723;font-family:system-ui,sans-serif}
main{max-width:900px;margin:8vh auto;padding:24px}
h1{font-size:42px}
form{display:flex;gap:10px}input{flex:1;padding:15px;border:1px solid #C2A67D;border-radius:12px;background:#EFEAE0;font-size:18px}
button{padding:15px 22px;border:0;border-radius:12px;background:#D2B48C;color:#3E2723;font-weight:700}
.result{margin-top:24px;padding:18px;background:#EFEAE0;border:1px solid #C2A67D;border-radius:12px}
a{color:#5d4037}.url{font-size:13px}
</style></head><body><main><h1>Sandstorm Search</h1>
<form action="/search"><input name="q" autofocus placeholder="Search the Common Crawl index"><button>Search</button></form>
<div id="results"></div>
<script>
const p=new URLSearchParams(location.search),q=p.get("q");
if(q) fetch("/api/search?q="+encodeURIComponent(q)).then(r=>r.json()).then(x=>{
 document.querySelector("#results").innerHTML=x.results.map(r=>'<div class="result"><a href="'+r.url+'" target="_blank"><h2>'+r.title+'</h2></a><div class="url">'+r.url+'</div><p>'+r.snippet+'</p></div>').join('')||'<p>No results.</p>';
});
</script></main></body></html>"""

@app.get("/",response_class=HTMLResponse)
@app.get("/search",response_class=HTMLResponse)
def home(): return HTML

@app.get("/api/search")
def api_search(q: str=Query(min_length=1), limit:int=20):
    return {"query":q,"results":search(q,limit)}
