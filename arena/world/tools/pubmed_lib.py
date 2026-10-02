"""PubMed retrieval harness (stdlib only, no third-party deps)."""
import json, re, sys, urllib.parse, urllib.request

EP = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/{}.fcgi"

def _get(url):
    req = urllib.request.Request(url, headers={"User-Agent": "research-agent/1.0"})
    with urllib.request.urlopen(req, timeout=90) as r:
        return r.read().decode("utf-8", "replace")

def search(term, retmax=6, mindate=None, maxdate=None):
    q = urllib.parse.quote(term)
    md = f"&mindate={mindate}" if mindate else ""
    mx = f"&maxdate={maxdate}" if maxdate else ""
    url = f"{EP.format('esearch')}?db=pubmed&term={q}&retmode=json&retmax={retmax}{md}{mx}"
    d = json.loads(_get(url))["esearchresult"]
    return d.get("count"), d.get("idlist", [])

def _tag(s, t):
    m = re.search(rf"<{t}[^>]*>(.*?)</{t}>", s, re.S)
    return _strip(m.group(1)) if m else ""

def _strip(s):
    s = re.sub(r"<[^>]+>", "", s or "")
    return re.sub(r"\s+", " ", s).strip()

def records(pmids):
    xml = _get(f"{EP.format('efetch')}?db=pubmed&id={','.join(pmids)}&retmode=xml&rettype=abstract")
    out = []
    for chunk in re.split(r"<PubmedArticle>", xml)[1:]:
        pmid = _tag(chunk, "PMID")
        title = _strip(_tag(chunk, "ArticleTitle"))
        journal = _tag(chunk, "Title") or _tag(chunk, "ISOAbbreviation")
        yr = _tag(chunk, "PubDate") or _tag(chunk, "Year")
        labs = re.findall(r"<AbstractText[^>]*Label=\"(.*?)\"[^>]*>(.*?)</AbstractText>", chunk, re.S)
        plain = re.findall(r"<AbstractText(?![^>]*Label)[^>]*>(.*?)</AbstractText>", chunk, re.S)
        if labs:
            body = "\n".join(f"{l}: {_strip(p)}" for l, p in labs)
        else:
            body = "\n".join(_strip(p) for p in plain)
        doi = _tag(chunk, "ArticleId")  # first ArticleId
        dois = re.findall(r'ELocationID EIdType="pii".*?>(.*?)<', chunk, re.S)
        out.append(dict(pmid=pmid, title=title, journal=journal, year=yr, abstract=body))
    return out

def show(term, n=5, mindate=None):
    cnt, ids = search(term, n, mindate)
    print(f"# QUERY: {term}\n# HITS: {cnt}")
    for r in records(ids):
        print(f"\n=== PMID {r['pmid']} | {r['journal']} | {r['year']}\n{r['title']}\n{r['abstract'][:4000]}")

if __name__ == "__main__":
    show(sys.argv[1], int(sys.argv[2]) if len(sys.argv) > 2 else 5,
         sys.argv[3] if len(sys.argv) > 3 else None)
