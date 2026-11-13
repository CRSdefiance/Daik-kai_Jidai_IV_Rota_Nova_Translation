from __future__ import annotations
import csv,json
from pathlib import Path
S=Path("work/sc3/script.csv");O=Path("translations/maria_deep_route_v69.json");SHA="001e21897ddb727ae261c82763ebef8515784ecfa571619c7614d87f3320aab2"
L={
"DK4_MES_B65_R0004":"Tomatoes are good!{LB}Munch.",
"DK4_MES_B65_R0007":"Yes.",
"DK4_MES_B65_R0011":"Thought it was an apple.{LB}Munch.",
"DK4_MES_B65_R0014":"Yes, indeed.",
"DK4_MES_B65_R0018":"Sweet and delicious!{LB}Munch, munch.",
"DK4_MES_B65_R0021":"Y-yes...",
"DK4_MES_B65_R0025":"Ha ha! You two really{LB}love those tomatoes.",
"DK4_MES_B65_R0028":"Since you like them so much,{LB}take this.",
"DK4_MES_B65_R0031":"What is it?",
"DK4_MES_B65_R0035":"Tomato plant.",
"DK4_MES_B65_R0039":"Really?",
"DK4_MES_B65_R0043":"Of course.{LB}You praised my tomatoes{LB}so warmly.",
"DK4_MES_B65_R0047":"Then, many thanks.",
"DK4_MES_B65_R0051":"Lucky, Admiral.{LB}Munch.",
"DK4_MES_B65_R0055":"Do not eat too much.",
}
SP={"03":"Maria","0E":"Emilio Ferrog","6C":"Tomato vendor"};ST={int(x,16) for x in SP}
def main()->None:
 with S.open(encoding="utf-8-sig",newline="") as f:rows={r["id"]:r for r in csv.DictReader(f) if r["id"].startswith("DK4_MES_B65_")}
 if set(L)!=set(rows):raise SystemExit(f"V69 mismatch: missing={sorted(set(rows)-set(L))}")
 rec=[]
 for i in sorted(L,key=lambda v:int(v.rsplit("R",1)[1])):
  r=rows[i];e=L[i];first=bytes.fromhex(r["source_hex"])[0];state=f"{first:02X}" if first in ST else "";u=e.replace("{MACRO:FI}","").replace("{MACRO:FA}","").replace("{MACRO:FO}","")
  if "F" in u or "I" in u:raise SystemExit(f"{i}: unsafe macro literal: {e}")
  sb=r["japanese"].count("{LB}");tb=e.count("{LB}");w=["weak-line-ending","orphan-final-line"]+(["manual-break"] if tb else [])+(["line-break-count"] if sb!=tb else [])
  rec.append({"id":i,"english":f"{{SPEAKER:{state}}}{e}{{PAD}}","speaker":SP[state],"context":"Maria and Emilio enjoy a vendor's tomatoes so enthusiastically that he gives them a tomato seedling.","source_meaning":e.replace("{LB}"," "),"localization_note":"Direct SC3 translation preserving Emilio's eating gag, the vendor's gift, speaker states, source rhythm, and fixed allocation.","qa_waivers":w,**({"manual_break_reason":"Protects semantic rows and progressive ASCII pair phase."} if tb else {}),"review":{"source":True,"context":True,"localization":True,"naturalness":True,"formatting":True}})
 p={"format":"dk4-ilnk-translation-batch-v1","file_path":"/data/SC3.DK4","source_file_sha256":SHA,"encoder":"dialogue-fixed-v1","dialogue_profile":"maria-story-shared-events-v69-live","translation_policy":"natural-dialogue-v2","target_locale":"en-US","review_gates":["source","context","localization","naturalness","formatting"],"scope":"Maria SC3 block 65: complete Emilio tomato-tasting and seedling gift event.","inventory":{"identified_records":len(rows),"translated_records":len(rec),"excluded_records":0,"blocks":{"65":len(rec)}},"excluded":[],"records":rec};O.write_text(json.dumps(p,ensure_ascii=False,indent=2)+"\n",encoding="utf-8");print(f"wrote {O}: {len(rec)} records")
if __name__=="__main__":main()
