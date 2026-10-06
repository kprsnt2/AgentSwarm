import sys,urllib.parse,urllib.request,json
t=sys.argv[1]; n=int(sys.argv[2]) if len(sys.argv)>2 else 7000
u="https://en.wikipedia.org/w/api.php?action=query&format=json&prop=extracts&explaintext=1&redirects=1&titles="+urllib.parse.quote(t)
req=urllib.request.Request(u,headers={'User-Agent':'research-agent/1.0'})
d=json.load(urllib.request.urlopen(req,timeout=30))
p=list(d['query']['pages'].values())[0]
print("###",p.get('title')); print(p.get('extract','(none)')[:n])
