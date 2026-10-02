"""Crossref API lookup (stdlib only)."""
import json, re, sys, urllib.parse, urllib.request

def _get(url):
    req = urllib.request.Request(url, headers={"User-Agent": "research-agent/1.0 (mailto:a@b.c)"})
    with urllib.request.urlopen(req, timeout=90) as r:
        return r.read().decode("utf-8", "replace")

def q(title, rows=3):
    url = "https://api.crossref.org/works?query.bibliographic=" + urllib.parse.quote(title) + f"&rows={rows}"
    d = json.loads(_get(url))["message"]["items"]
    out = []
    for it in d:
        ti = (it.get("title") or [""])[0]
        yr = it.get("issued", {}).get("date-parts", [[None]])[0][0]
        cont = (it.get("container-title") or [""])[0]
        auth = ", ".join(f"{a.get('family','')} {a.get('given','')[:1]}" for a in (it.get("author") or [])[:4])
        doi = it.get("DOI", "")
        out.append(dict(title=ti, year=yr, journal=cont, authors=auth, doi=doi,
                        type=it.get("type", ""), cited=it.get("is-referenced-by-count", 0)))
    return out

if __name__ == "__main__":
    for t in sys.argv[1:]:
        print(f"\n### {t}")
        for r in q(t):
            print(f"  [{r['year']}] {r['authors']} — \"{r['title']}\" {r['journal']} "
                  f"doi:{r['doi']} (cited {r['cited']})")
