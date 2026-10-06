import sys,io
sys.stdout=io.TextIOWrapper(sys.stdout.buffer,encoding='utf-8',errors='replace')
import urllib.parse,urllib.request,json,re
want=sys.argv[1]
titles=sys.argv[2].split('|')
u="https://en.wikipedia.org/w/api.php?action=query&format=json&prop=extracts&explaintext=1&redirects=1&titles="+urllib.parse.quote('|'.join(titles))
req=urllib.request.Request(u,headers={'User-Agent':'research-agent/1.0'})
d=json.load(urllib.request.urlopen(req,timeout=40))
for p in d['query']['pages'].values():
    txt=p.get('extract','')
    print("\n"+("="*20)+" "+p.get('title','?')+" "+("="*20))
    for line in txt.split('\n'):
        if re.search(want,line,re.I): print(line)
