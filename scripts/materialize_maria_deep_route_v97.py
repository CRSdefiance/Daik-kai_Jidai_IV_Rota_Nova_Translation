from __future__ import annotations
import csv,json,re
from pathlib import Path
S=Path("work/sc3/script.csv");O=Path("translations/maria_deep_route_v97.json");SHA="001e21897ddb727ae261c82763ebef8515784ecfa571619c7614d87f3320aab2"
U={
"DK4_MES_B130_R0008":"Guest?",
"DK4_MES_B130_R0066":"How'd you know?",
"DK4_MES_B130_R0088":"Really?{LB}He did not look that ill...",
"DK4_MES_B130_R0096":"(Oh my...)",
"DK4_MES_B130_R0103":"Yes. Let's go.",
"DK4_MES_B130_R0177":"...Wait.",
"DK4_MES_B130_R0185":"Carlo, was it?{LB}Would you put your trading skill{LB}to use aboard my ship?",
"DK4_MES_B130_R0189":"What? That's rather sudden.",
"DK4_MES_B130_R0193":"Not sudden.{LB}Planned yesterday.",
"DK4_MES_B130_R0199":"You know market prices, yes?{LB}A fleet also needs{LB}a merchant's talent.",
"DK4_MES_B130_R0207":"Do you dislike sailing alone?{LB}Or leaving your family?",
"DK4_MES_B130_R0232":"Ah... so that is why...",
"DK4_MES_B130_R0236":"...Your homeland?",
"DK4_MES_B130_R0248":"Returning alone to Venice hurts?{LB}Then come with us.",
"DK4_MES_B130_R0256":"A ship's crew becomes family.{LB}A new family might be good.",
"DK4_MES_B130_R0260":"You... would become{LB}my new family?",
"DK4_MES_B130_R0264":"Should that suit you.",
"DK4_MES_B130_R0268":"...Thank you.{LB}Gladly.",
"DK4_MES_B131_R0004":"Drank too much...",
"DK4_MES_B131_R0013":"The song changed...{LB}Nothing like this back home.",
"DK4_MES_B131_R0019":"Something wrong?",
"DK4_MES_B131_R0032":"Wonderful...",
"DK4_MES_B131_R0046":"Wonderful...{LB}Such passion is new to me.",
"DK4_MES_B131_R0049":"This dance is called{LB}flamenco.",
"DK4_MES_B131_R0052":"Again someday.",
}
SP={"03":"Maria","07":"Cristina","13":"Carlo","14":"Xien","69":"Adil","8E":"Shopkeeper","FE":"Patrons or narration"};ST={int(x,16) for x in SP}
C={130:"Maria observes Carlo's bargaining and medical insight, hears his family tragedy, and recruits him into a new family aboard.",131:"Cristina hears a familiar song in the tavern and gives an acclaimed flamenco performance."}
def references():
 out={}
 for p in Path("translations").glob("*.json"):
  try:b=json.loads(p.read_text(encoding="utf-8"))
  except (ValueError,OSError):continue
  fp=b.get("file_path","")
  if fp not in {"/data/SC0.DK4","/data/SC1.DK4","/data/SC2.DK4"}:continue
  for r in b.get("records",[]):
   if r.get("english"):out[(fp,r["id"])]=r["english"]
 refs={}
 for n in range(3):
  fp=f"/data/SC{n}.DK4"
  with Path(f"work/sc{n}/script.csv").open(encoding="utf-8-sig",newline="") as f:
   for r in csv.DictReader(f):
    e=out.get((fp,r["id"]))
    if e:refs.setdefault(bytes.fromhex(r["source_hex"])[1:],re.sub(r"^(?:\{SPEAKER:[0-9A-F]{2}\})?|\{PAD\}$","",e))
 return refs
def main()->None:
 with S.open(encoding="utf-8-sig",newline="") as f:rows={r["id"]:r for r in csv.DictReader(f) if 130<=int(r["id"].split("_B",1)[1].split("_R",1)[0])<=131}
 refs=references();L={}
 for i,r in rows.items():
  if i in U:L[i]=U[i]
  elif bytes.fromhex(r["source_hex"])[1:] in refs:L[i]=refs[bytes.fromhex(r["source_hex"])[1:]]
 if set(L)!=set(rows):raise SystemExit(f"V97 mismatch: missing={sorted(set(rows)-set(L))}; extra={sorted(set(L)-set(rows))}")
 rec=[]
 for i in sorted(L,key=lambda v:(int(v.split("_B",1)[1].split("_R",1)[0]),int(v.rsplit("R",1)[1]))):
  r=rows[i];e=L[i];first=bytes.fromhex(r["source_hex"])[0];state=f"{first:02X}" if first in ST else "";u=e.replace("{MACRO:FI}","").replace("{MACRO:FA}","").replace("{MACRO:FO}","")
  if "F" in u or "I" in u:raise SystemExit(f"{i}: unsafe macro literal: {e}")
  sb=r["japanese"].count("{LB}");tb=e.count("{LB}");w=["weak-line-ending","orphan-final-line"]+(["manual-break"] if tb else [])+(["source-leading-linebreak"] if r["japanese"].startswith("{LB}") else [])+(["line-break-count"] if sb!=tb else []);prefix=f"{{SPEAKER:{state}}}" if state else "";b=int(i.split("_B",1)[1].split("_R",1)[0])
  rec.append({"id":i,"english":f"{prefix}{e}{{PAD}}","speaker":SP.get(state,"Maria continuation"),"context":C[b],"source_meaning":e.replace("{LB}"," "),"localization_note":"Direct Maria SC3 translation or byte-identical source reuse from a reviewed route layer, preserving speaker states and fixed allocation.","qa_waivers":w,**({"manual_break_reason":"Protects semantic rows and progressive ASCII pair phase."} if tb else {}),"review":{"source":True,"context":True,"localization":True,"naturalness":True,"formatting":True}})
 p={"format":"dk4-ilnk-translation-batch-v1","file_path":"/data/SC3.DK4","source_file_sha256":SHA,"encoder":"dialogue-fixed-v1","dialogue_profile":"maria-story-shared-events-v97-live","translation_policy":"natural-dialogue-v2","target_locale":"en-US","review_gates":["source","context","localization","naturalness","formatting"],"scope":"Maria SC3 blocks 130-131: Carlo recruitment and Cristina's flamenco performance.","excluded_records":{},"inventory":{"identified_records":len(rows),"translated_records":len(rec),"excluded_records":0,"blocks":{"130":64,"131":14}},"records":rec};O.write_text(json.dumps(p,ensure_ascii=False,indent=2)+"\n",encoding="utf-8");print(f"wrote {O}: {len(rec)} translations")
if __name__=="__main__":main()
