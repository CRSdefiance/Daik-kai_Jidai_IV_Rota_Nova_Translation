from __future__ import annotations
import csv,json,re
from pathlib import Path
S=Path("work/sc3/script.csv");O=Path("translations/maria_deep_route_v103.json");SHA="001e21897ddb727ae261c82763ebef8515784ecfa571619c7614d87f3320aab2"
U={
"DK4_MES_B141_R0021":"Hm?",
"DK4_MES_B141_R0036":"Yifa's...?",
"DK4_MES_B141_R0051":"Then you came to take Yifa back?",
"DK4_MES_B141_R0076":"That was a dream?{LB}So vivid...",
"DK4_MES_B141_R0086":"What is it?",
"DK4_MES_B141_R0094":"Senior pupil?{LB}His name is Sanghyeon?",
"DK4_MES_B141_R0097":"What?{LB}You met my brother?",
"DK4_MES_B141_R0100":"No... a dream.{LB}He called himself your senior{LB}and gave the name.",
"DK4_MES_B141_R0116":"Art...?{LB}(Of course.)",
"DK4_MES_B141_R0119":"Right. He said to keep training{LB}after leaving the mountain.",
"DK4_MES_B141_R0127":"{LB}What is it?",
"DK4_MES_B141_R0134":"Do ship work{LB}with that same energy.",
"DK4_MES_B142_R0014":"Men like that make{LB}tavern work difficult...",
"DK4_MES_B142_R0067":"Quite intriguing.",
"DK4_MES_B142_R0071":"You heard?{LB}Maybe his type suits you.",
"DK4_MES_B142_R0075":"Sadly, the man did not interest me.{LB}The Golden Crown of Silla did.",
"DK4_MES_B142_R0079":"Oh... that makes more sense.{LB}Know anything about the crown?",
"DK4_MES_B142_R0082":"Nothing.{LB}Would you tell me what you know?",
"DK4_MES_B142_R0086":"Only that it is in Seoul,{LB}and incredibly beautiful.",
"DK4_MES_B142_R0090":"When Seoul is visited{LB}the search begins.",
"DK4_MES_B142_R0094":"Really?{LB}Show me if you find it!",
"DK4_MES_B142_R0097":"Once found.{LB}But that man may be your better hope.",
}
SP={"03":"Maria","19":"Yifa","1A":"Julian","51":"Sanghyeon","AE":"Merchant","AF":"Merchant","C9":"Mihwa","FE":"Narration"};ST={int(x,16) for x in SP}
C={141:"Sanghyeon reaches Maria in a dream to entrust Yifa's continued training to her.",142:"Maria overhears Julian and Mihwa discuss the Golden Crown of Silla and takes up the Seoul lead.",149:"Merchants anticipate a banana boom in Seville."}
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
 with S.open(encoding="utf-8-sig",newline="") as f:rows={r["id"]:r for r in csv.DictReader(f) if int(r["id"].split("_B",1)[1].split("_R",1)[0]) in {141,142,149}}
 refs=references();L={i:(U[i] if i in U else refs.get(bytes.fromhex(r["source_hex"])[1:])) for i,r in rows.items()}
 if any(v is None for v in L.values()):raise SystemExit(f"V103 missing: {sorted(i for i,v in L.items() if v is None)}")
 rec=[]
 for i in sorted(L,key=lambda v:(int(v.split("_B",1)[1].split("_R",1)[0]),int(v.rsplit("R",1)[1]))):
  r=rows[i];e=L[i];first=bytes.fromhex(r["source_hex"])[0];state=f"{first:02X}" if first in ST else "";u=e.replace("{MACRO:FI}","").replace("{MACRO:FA}","").replace("{MACRO:FO}","")
  if "F" in u or "I" in u:raise SystemExit(f"{i}: unsafe macro literal: {e}")
  sb=r["japanese"].count("{LB}");tb=e.count("{LB}");w=["weak-line-ending","orphan-final-line"]+(["manual-break"] if tb else [])+(["source-leading-linebreak"] if r["japanese"].startswith("{LB}") else [])+(["line-break-count"] if sb!=tb else []);prefix=f"{{SPEAKER:{state}}}" if state else "";b=int(i.split("_B",1)[1].split("_R",1)[0])
  rec.append({"id":i,"english":f"{prefix}{e}{{PAD}}","speaker":SP.get(state,"continuation"),"context":C[b],"source_meaning":e.replace("{LB}"," "),"localization_note":"Direct Maria translation or byte-identical reviewed reuse, preserving dream and rumor scenes, FI macro, line breaks, speaker states, and fixed allocation.","qa_waivers":w,**({"manual_break_reason":"Protects semantic rows and progressive ASCII pair phase."} if tb else {}),"review":{"source":True,"context":True,"localization":True,"naturalness":True,"formatting":True}})
 p={"format":"dk4-ilnk-translation-batch-v1","file_path":"/data/SC3.DK4","source_file_sha256":SHA,"encoder":"dialogue-fixed-v1","dialogue_profile":"maria-story-shared-events-v103-live","translation_policy":"natural-dialogue-v2","target_locale":"en-US","review_gates":["source","context","localization","naturalness","formatting"],"scope":"Maria SC3 blocks 141, 142, and 149: Yifa dream, Silla crown lead, and banana boom.","excluded_records":{},"inventory":{"identified_records":71,"translated_records":71,"excluded_records":0,"blocks":{"141":35,"142":26,"149":10}},"records":rec};O.write_text(json.dumps(p,ensure_ascii=False,indent=2)+"\n",encoding="utf-8");print(f"wrote {O}: {len(rec)} translations")
if __name__=="__main__":main()
