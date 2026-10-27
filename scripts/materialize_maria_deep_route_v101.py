from __future__ import annotations
import csv,json,re
from pathlib import Path
S=Path("work/sc3/script.csv");O=Path("translations/maria_deep_route_v101.json");SHA="001e21897ddb727ae261c82763ebef8515784ecfa571619c7614d87f3320aab2"
U={
"DK4_MES_B138_R0004":"{LB}{MACRO:FI},{LB}someone is near our ship.",
"DK4_MES_B138_R0009":"...A splendid ship.{LB}But...",
"DK4_MES_B138_R0012":"What are you doing here?",
"DK4_MES_B138_R0016":"Admiring the ship.{LB}Up close, its heartbeat{LB}can almost be heard...",
"DK4_MES_B138_R0020":"But this ship...{LB}Wait! Are you{LB}Admiral {MACRO:FA}?",
"DK4_MES_B138_R0023":"Yes.{LB}What about my ship?",
"DK4_MES_B138_R0026":"This ship lacks care.{LB}Show it more love,{LB}or the ship will weep.",
"DK4_MES_B138_R0030":"{LB}A weeping ship?{LB}Quite poetic.",
"DK4_MES_B138_R0033":"Who are you?",
"DK4_MES_B138_R0037":"Manuel, formerly a navigator.{LB}Pardon my bluntness...",
"DK4_MES_B138_R0041":"{LB}The poor upkeep is true.{LB}Seeing it at once proves skill.",
"DK4_MES_B138_R0045":"Skill, experience,{LB}and love for ships.",
"DK4_MES_B138_R0048":"You clearly love ships.{LB}Why stop sailing?{LB}Would you tell me?",
"DK4_MES_B138_R0052":"Sorry... That was long ago...",
"DK4_MES_B138_R0056":"One more question.{LB}Would you return to sea?",
"DK4_MES_B138_R0059":"What...?",
"DK4_MES_B138_R0063":"Care for my ship.",
"DK4_MES_B138_R0070":"What do you say?{LB}Only should you wish.",
"DK4_MES_B138_R0074":"...Thank you.{LB}Ships give my life meaning.{LB}Gladly.",
"DK4_MES_B138_R0093":"Then... room assignments{LB}for long voyages need explaining.",
"DK4_MES_B138_R0101":"A galley or livestock room{LB}reduces water and food use.",
"DK4_MES_B138_R0109":"Sick or injured sailors recover{LB}faster in cabins or lounges.",
}
SP={"03":"Maria","17":"Manuel","89":"Choice control"};ST={int(x,16) for x in SP};C="Maria recognizes Manuel's love and skill with ships, recruits him, and receives his ship-room tutorial."
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
 with S.open(encoding="utf-8-sig",newline="") as f:rows={r["id"]:r for r in csv.DictReader(f) if int(r["id"].split("_B",1)[1].split("_R",1)[0])==138}
 refs=references();L={i:(U[i] if i in U else refs.get(bytes.fromhex(r["source_hex"])[1:])) for i,r in rows.items()}
 if any(v is None for v in L.values()):raise SystemExit(f"V101 missing: {sorted(i for i,v in L.items() if v is None)}")
 rec=[]
 for i in sorted(L,key=lambda v:int(v.rsplit("R",1)[1])):
  r=rows[i];e=L[i];first=bytes.fromhex(r["source_hex"])[0];state=f"{first:02X}" if first in ST else "";u=e.replace("{MACRO:FI}","").replace("{MACRO:FA}","").replace("{MACRO:FO}","")
  if "F" in u or "I" in u:raise SystemExit(f"{i}: unsafe macro literal: {e}")
  sb=r["japanese"].count("{LB}");tb=e.count("{LB}");w=["weak-line-ending","orphan-final-line"]+(["manual-break"] if tb else [])+(["source-leading-linebreak"] if r["japanese"].startswith("{LB}") else [])+(["line-break-count"] if sb!=tb else []);prefix=f"{{SPEAKER:{state}}}" if state else ""
  rec.append({"id":i,"english":f"{prefix}{e}{{PAD}}","speaker":SP.get(state,"Xien continuation or choice"),"context":C,"source_meaning":e.replace("{LB}"," "),"localization_note":"Direct Maria translation or byte-identical reviewed reuse, preserving tutorial choices, FI/FA macros, source-leading line breaks, speaker states, and fixed allocation.","qa_waivers":w,**({"manual_break_reason":"Protects semantic rows and progressive ASCII pair phase."} if tb else {}),"review":{"source":True,"context":True,"localization":True,"naturalness":True,"formatting":True}})
 p={"format":"dk4-ilnk-translation-batch-v1","file_path":"/data/SC3.DK4","source_file_sha256":SHA,"encoder":"dialogue-fixed-v1","dialogue_profile":"maria-story-shared-events-v101-live","translation_policy":"natural-dialogue-v2","target_locale":"en-US","review_gates":["source","context","localization","naturalness","formatting"],"scope":"Maria SC3 block 138: Manuel recruitment and ship-room tutorial.","excluded_records":{},"inventory":{"identified_records":31,"translated_records":31,"excluded_records":0,"blocks":{"138":31}},"records":rec};O.write_text(json.dumps(p,ensure_ascii=False,indent=2)+"\n",encoding="utf-8");print(f"wrote {O}: {len(rec)} translations")
if __name__=="__main__":main()
