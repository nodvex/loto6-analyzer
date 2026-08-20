import re,time,requests
from bs4 import BeautifulSoup
BASE="https://www.mizuhobank.co.jp/takarakuji/check/loto"
H={"User-Agent":"Mozilla/5.0 Loto6Analyzer/1.0"}
def get(url):
    for i in range(3):
        try:
            r=requests.get(url,headers=H,timeout=20);r.raise_for_status();return r.text
        except Exception:
            if i==2:raise
            time.sleep(2*(i+1))
def datejp(s):
    y,m,d=map(int,re.search(r"(\d{4})年\s*(\d+)月\s*(\d+)日",s).groups());return f"{y:04d}-{m:02d}-{d:02d}"
def parse(html):
    t=BeautifulSoup(html,"html.parser").get_text(" ",strip=True);ms=list(re.finditer(r"第\s*(\d+)\s*回",t));out=[]
    for i,m in enumerate(ms):
        c=t[m.start():(ms[i+1].start() if i+1<len(ms) else m.start()+1200)]
        dm=re.search(r"\d{4}年\s*\d+月\s*\d+日",c)
        if not dm:continue
        vals=[]
        for x in re.findall(r"(?<!\d)(\d{1,2})(?!\d)",c[dm.end():]):
            v=int(x)
            if 1<=v<=43:vals.append(v)
            if len(vals)==7:break
        if len(vals)==7 and len(set(vals[:6]))==6 and vals[6] not in vals[:6]:
            out.append({"draw":int(m.group(1)),"date":datejp(dm.group()),"numbers":sorted(vals[:6]),"bonus":vals[6]})
    return list({x["draw"]:x for x in out}.values())
def range_page(a,b):
    u=f"{BASE}/backnumber/detail.html?fromto={a}_{b}&type=loto6";x=parse(get(u))
    if not x and a<=640:x=parse(get(f"{BASE}/backnumber/loto6{a:04d}.html"))
    return x
def current():return parse(get(f"{BASE}/loto6/index.html"))
