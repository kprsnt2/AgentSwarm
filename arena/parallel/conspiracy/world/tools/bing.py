import sys,urllib.parse,urllib.request,re,html,random
UA="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
q=sys.argv[1]
u="https://www.bing.com/search?q="+urllib.parse.quote(q)+"&setlang=en&count=10"
req=urllib.request.Request(u,headers={'User-Agent':UA,'Accept-Language':'en-US,en;q=0.9','Accept':'text/html'})
t=urllib.request.urlopen(req,timeout=30).read().decode('utf-8','ignore')
blocks=re.split(r'class="b_algo"',t)[1:]
clean=lambda s: html.unescape(re.sub(r'<[^>]+>','',s)).strip()
print("QUERY:",q,"| blocks:",len(blocks))
for i,b in enumerate(blocks[:7]):
    m=re.search(r'<h2[^>]*>\s*<a[^>]*href="([^"]+)"[^>]*>(.*?)</a>',b,re.S)
    if not m: continue
    sn=re.search(r'<p[^>]*>(.*?)</p>',b,re.S)
    print(f"[{i+1}] {clean(m.group(2))}\n    {m.group(1)[:150]}\n    {(clean(sn.group(1)) if sn else '')[:330]}\n")
