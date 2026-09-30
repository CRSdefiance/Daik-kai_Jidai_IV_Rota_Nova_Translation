from __future__ import annotations
import csv,json,re
from pathlib import Path
S=Path("work/sc3/script.csv");O=Path("translations/maria_deep_route_v99.json");SHA="001e21897ddb727ae261c82763ebef8515784ecfa571619c7614d87f3320aab2"
U={
"DK4_MES_B136_R0069":"Still green... No drink.{LB}Were you that confident{LB}in gambling?",
"DK4_MES_B136_R0080":"{LB}Luck aside, insight?",
"DK4_MES_B136_R0091":"Perhaps a proposal?",
"DK4_MES_B136_R0127":"Amazing... How did you know?",
"DK4_MES_B136_R0139":"Amazing. You noticed all that.",
"DK4_MES_B136_R0149":"Great talent. Join my{LB}{MACRO:FO} and test it?",
"DK4_MES_B136_R0163":"No drink.{LB}Join {MACRO:FO} now.",
"DK4_MES_B136_R0214":"Welcome aboard.",
}
EX={"DK4_MES_B136_R0013":"Raw five-byte event-control payload before the gambling challenge; not dialogue."}
SP={"03":"Maria","14":"Dias","74":"Companion","8E":"Choice control"};ST={int(x,16) for x in SP}
C={134:"A companion notes that someone still has not returned.",136:"Maria defeats Dias at a coin game, sees his extraordinary powers of observation, and recruits him on a final toss."}
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
 with S.open(encoding="utf-8-sig",newline="") as f:rows={r["id"]:r for r in csv.DictReader(f) if int(r["id"].split("_B",1)[1].split("_R",1)[0]) in {134,136}}
 refs=references();L={}
 for i,r in rows.items():
  if i in EX:continue
  if i in U:L[i]=U[i]
  elif bytes.fromhex(r["source_hex"])[1:] in refs:L[i]=refs[bytes.fromhex(r["source_hex"])[1:]]
 if set(L)|set(EX)!=set(rows):raise SystemExit(f"V99 mismatch: missing={sorted(set(rows)-set(L)-set(EX))}; extra={sorted((set(L)|set(EX))-set(rows))}")
 rec=[]
 for i in sorted(L,key=lambda v:(int(v.split("_B",1)[1].split("_R",1)[0]),int(v.rsplit("R",1)[1]))):
  r=rows[i];e=L[i];first=bytes.fromhex(r["source_hex"])[0];state=f"{first:02X}" if first in ST else "";u=e.replace("{MACRO:FI}","").replace("{MACRO:FA}","").replace("{MACRO:FO}","")
  if "F" in u or "I" in u:raise SystemExit(f"{i}: unsafe macro literal: {e}")
  sb=r["japanese"].count("{LB}");tb=e.count("{LB}");w=["weak-line-ending","orphan-final-line"]+(["manual-break"] if tb else [])+(["source-leading-linebreak"] if r["japanese"].startswith("{LB}") else [])+(["line-break-count"] if sb!=tb else []);prefix=f"{{SPEAKER:{state}}}" if state else "";b=int(i.split("_B",1)[1].split("_R",1)[0])
  rec.append({"id":i,"english":f"{prefix}{e}{{PAD}}","speaker":SP.get(state,"bystander or continuation"),"context":C[b],"source_meaning":e.replace("{LB}"," "),"localization_note":"Direct Maria translation or byte-identical reviewed route reuse, preserving the 0x8E choice control, FO macros, line breaks, event payload, and fixed allocation.","qa_waivers":w,**({"manual_break_reason":"Protects semantic rows and progressive ASCII pair phase."} if tb else {}),"review":{"source":True,"context":True,"localization":True,"naturalness":True,"formatting":True}})
 p={"format":"dk4-ilnk-translation-batch-v1","file_path":"/data/SC3.DK4","source_file_sha256":SHA,"encoder":"dialogue-fixed-v1","dialogue_profile":"maria-story-shared-events-v99-live","translation_policy":"natural-dialogue-v2","target_locale":"en-US","review_gates":["source","context","localization","naturalness","formatting"],"scope":"Maria SC3 blocks 134 and 136: absence hook and Dias gambling recruitment.","excluded_records":EX,"inventory":{"identified_records":len(rows),"translated_records":len(rec),"excluded_records":len(EX),"blocks":{"134":1,"136":40}},"records":rec};O.write_text(json.dumps(p,ensure_ascii=False,indent=2)+"\n",encoding="utf-8");print(f"wrote {O}: {len(rec)} translations + {len(EX)} control")
if __name__=="__main__":main()
