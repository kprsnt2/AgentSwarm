import sys,urllib.parse,urllib.request,re,html,time,random,http.cookiejar
cj=http.cookiejar.CookieJar()
op=urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))
q=urllib.parse.quote(sys.argv[1])
for a in range(5):
    try:
        req=urllib.request.Request(f"https://lite.duckduckgo.com/lite/?q={q}",
            headers={'User-Agent':f'Mozilla/5.0 ({random.choice(["X11; Linux x86_64","Windows NT 10.0; Win64; x64","Macintosh; Intel Mac OS X 10_15"])}) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/1{random.randint(20,39)}.0 Safari/537.36','Accept':'text/html','Accept-Language':'en-US,en;q=0.9'})
        t=op.open(req,timeout=30).read().decode('utf-8','ignore')
        links=re.findall(r'class="result-link"[^>]*href="([^"]+)"[^>]*>(.*?)</a>',t,re.S)
        snips=re.findall(r'class="result-snippet">(.*?)(?:<|$)',t,re.S)
        if links:
            clean=lambda s: html.unescape(re.sub(r'<[^>]+>','',s)).strip()
            print("QUERY:",sys.argv[1])
            for i,(url,ti) in enumerate(links[:6]):
                print(f"[{i+1}] {clean(ti)}\n    {url[:160]}\n    {(clean(snips[i]) if i<len(snips) else '')[:340]}\n")
            sys.exit(0)
        time.sleep(4+a*3)
    except Exception as e:
        print("err",e,file=sys.stderr); time.sleep(4)
print("DDG BLOCKED")
