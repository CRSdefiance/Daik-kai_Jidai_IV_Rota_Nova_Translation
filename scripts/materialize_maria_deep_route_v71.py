from __future__ import annotations
import csv,json
from pathlib import Path
S=Path("work/sc3/script.csv");O=Path("translations/maria_deep_route_v71.json");SHA="001e21897ddb727ae261c82763ebef8515784ecfa571619c7614d87f3320aab2"
L={
"DK4_MES_B68_R0004":"!{LB}Here...",
"DK4_MES_B68_R0007":"What is it, Gerhard?",
"DK4_MES_B68_R0011":"No.{LB}Just old memories...",
"DK4_MES_B68_R0014":"Old?",
"DK4_MES_B68_R0018":"During a battle with pirates here,{LB}my sword was lost.",
"DK4_MES_B68_R0021":"A sword?",
"DK4_MES_B68_R0025":"An old Katzbalger.{LB}Plain to look at, but superb{LB}in the hand. My companion{LB}for many years.",
"DK4_MES_B68_R0028":"What a shame.{LB}Was it never found?",
"DK4_MES_B68_R0031":"Nowhere.{LB}A local fisherman likely found it{LB}and sold it for a pittance.",
"DK4_MES_B68_R0034":"Perhaps someone with a good eye{LB}found and treasured it.",
"DK4_MES_B68_R0037":"A blade like that is rare.{LB}Knowing someone worthy uses it{LB}would ease my mind...",
}
SP={"03":"Maria","10":"Gerhard Adernkatz"};ST={int(x,16) for x in SP}
def main()->None:
 with S.open(encoding="utf-8-sig",newline="") as f:rows={r["id"]:r for r in csv.DictReader(f) if r["id"].startswith("DK4_MES_B68_")}
 if set(L)!=set(rows):raise SystemExit(f"V71 mismatch: missing={sorted(set(rows)-set(L))}")
 rec=[]
 for i in sorted(L,key=lambda v:int(v.rsplit("R",1)[1])):
  r=rows[i];e=L[i];first=bytes.fromhex(r["source_hex"])[0];state=f"{first:02X}" if first in ST else "";u=e.replace("{MACRO:FI}","").replace("{MACRO:FA}","").replace("{MACRO:FO}","")
  if "F" in u or "I" in u:raise SystemExit(f"{i}: unsafe macro literal: {e}")
  sb=r["japanese"].count("{LB}");tb=e.count("{LB}");w=["weak-line-ending","orphan-final-line"]+(["manual-break"] if tb else [])+(["line-break-count"] if sb!=tb else [])
  rec.append({"id":i,"english":f"{{SPEAKER:{state}}}{e}{{PAD}}","speaker":SP[state],"context":"Gerhard remembers losing his treasured Katzbalger during a pirate battle and hopes a worthy owner found the blade.","source_meaning":e.replace("{LB}"," "),"localization_note":"Direct SC3 translation preserving Gerhard's restrained nostalgia, the Katzbalger identification, speaker states, source pacing, and fixed allocation.","qa_waivers":w,**({"manual_break_reason":"Protects semantic rows and progressive ASCII pair phase."} if tb else {}),"review":{"source":True,"context":True,"localization":True,"naturalness":True,"formatting":True}})
 p={"format":"dk4-ilnk-translation-batch-v1","file_path":"/data/SC3.DK4","source_file_sha256":SHA,"encoder":"dialogue-fixed-v1","dialogue_profile":"maria-story-shared-events-v71-live","translation_policy":"natural-dialogue-v2","target_locale":"en-US","review_gates":["source","context","localization","naturalness","formatting"],"scope":"Maria SC3 block 68: complete Gerhard lost-Katzbalger reminiscence.","inventory":{"identified_records":len(rows),"translated_records":len(rec),"excluded_records":0,"blocks":{"68":len(rec)}},"excluded":[],"records":rec};O.write_text(json.dumps(p,ensure_ascii=False,indent=2)+"\n",encoding="utf-8");print(f"wrote {O}: {len(rec)} records")
if __name__=="__main__":main()
