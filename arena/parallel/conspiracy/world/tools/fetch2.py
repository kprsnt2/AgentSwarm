import sys, urllib.parse, urllib.request, json, io, re
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

def get(title, n=12000):
    u = ("https://en.wikipedia.org/w/api.php?action=query&format=json&prop=extracts"
         "&explaintext=1&redirects=1&titles=" + urllib.parse.quote(title))
    req = urllib.request.Request(u, headers={'User-Agent': 'research-agent/1.0'})
    d = json.load(urllib.request.urlopen(req, timeout=40))
    p = list(d['query']['pages'].values())[0]
    return (p.get('title'), p.get('extract', '(none)'))

if __name__ == '__main__':
    title = sys.argv[1]
    n = int(sys.argv[2]) if len(sys.argv) > 2 else 12000
    pat = sys.argv[3] if len(sys.argv) > 3 else None
    t, ex = get(title)
    print('###', t)
    if pat:
        lines = ex.splitlines()
        hits = [i for i, l in enumerate(lines) if re.search(pat, l, re.I)]
        shown = set()
        for i in hits:
            for j in range(max(0, i - 2), min(len(lines), i + 7)):
                if j not in shown:
                    print(f'{j+1:5d}| {lines[j]}')
                    shown.add(j)
    else:
        print(ex[:n])
