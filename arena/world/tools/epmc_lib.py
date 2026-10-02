"""Europe PMC REST helper (stdlib only): search + open-access full text."""
import json, re, sys, urllib.parse, urllib.request

BASE = "https://www.ebi.ac.uk/europepmc/webservices/rest"

def _get(url):
    req = urllib.request.Request(url, headers={"User-Agent": "research-agent/1.0"})
    with urllib.request.urlopen(req, timeout=120) as r:
        return r.read().decode("utf-8", "replace")

def search(q, n=5, fmt="json"):
    url = f"{BASE}/search?query={urllib.parse.quote(q)}&format={fmt}&pageSize={n}"
    return json.loads(_get(url))

def show(q, n=5):
    d = search(q, n)
    print(f"# QUERY {q}  hitCount={d.get('hitCount')}")
    for r in d.get("resultList", {}).get("result", []):
        print(f"\n=== {r.get('id')} | pmcid={r.get('pmcid')} | {r.get('journalTitle')} {r.get('pubYear')}")
        print(f"TITLE: {r.get('title')}")
        print(f"AUTH:  {r.get('authorString','')[:200]}")
        print(f"DOI:   {r.get('doi')}")
        print(f"ABSTRACT: {(r.get('abstractText') or '')[:2500]}")

def fulltext(pmcid, maxchars=60000):
    xml = _get(f"{BASE}/{pmcid}/fullTextXML")
    return xml

if __name__ == "__main__":
    show(sys.argv[1], int(sys.argv[2]) if len(sys.argv) > 2 else 5)
