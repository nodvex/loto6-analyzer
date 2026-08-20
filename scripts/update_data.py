import argparse,json,time
from pathlib import Path
from datetime import datetime
from zoneinfo import ZoneInfo
from scraper_mizuho import range_page,current
from validate_data import validate
R=Path(__file__).resolve().parents[1];D=R/"data/loto6.json";M=R/"data/metadata.json"
def old():
    try:return json.loads(D.read_text())
    except:return []
def bootstrap():
    rows=[];a=1;empty=0
    while empty<2 and a<5000:
        print("fetch",a,a+19)
        try:p=range_page(a,a+19)
        except Exception as e:print(e);p=[]
        if p:rows+=p;empty=0
        else:empty+=1
        a+=20;time.sleep(.35)
    try:rows+=current()
    except Exception as e:print("current",e)
    rows=list({x["draw"]:x for x in rows}.values());rows.sort(key=lambda x:x["draw"]);validate(rows);return rows
def update(rows):
    by={x["draw"]:x for x in rows}
    for x in current():by[x["draw"]]=x
    if by:
        nxt=max(by)+1;a=((nxt-1)//20)*20+1
        try:
            for x in range_page(a,a+19):by[x["draw"]]=x
        except Exception as e:print("range fallback",e)
    z=[by[k] for k in sorted(by)];validate(z);return z
def main():
    p=argparse.ArgumentParser();p.add_argument("--bootstrap",action="store_true");a=p.parse_args();o=old();z=bootstrap() if a.bootstrap or not o else update(o)
    nt=json.dumps(z,ensure_ascii=False,indent=2)+"\n";ot=D.read_text() if D.exists() else "";changed=nt!=ot
    if changed:D.write_text(nt,encoding="utf-8")
    M.write_text(json.dumps({"updated_at":datetime.now(ZoneInfo("Asia/Tokyo")).isoformat(timespec="seconds"),"latest_draw":z[-1]["draw"],"count":len(z),"changed":changed,"source":"Mizuho Bank"},ensure_ascii=False,indent=2),encoding="utf-8")
    print("latest",z[-1]["draw"],"count",len(z),"changed",changed)
if __name__=="__main__":main()
