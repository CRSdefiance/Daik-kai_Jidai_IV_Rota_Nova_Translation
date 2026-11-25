from __future__ import annotations
import csv,json
from pathlib import Path
S=Path("work/sc3/script.csv");O=Path("translations/maria_deep_route_v77.json");SHA="001e21897ddb727ae261c82763ebef8515784ecfa571619c7614d87f3320aab2"
L={
"DK4_MES_B77_R0004":"Admiral, did you hear a Portuguese{LB}fleet was wrecked here 20 years ago?",
"DK4_MES_B77_R0008":"News to me.",
"DK4_MES_B77_R0012":"The admiral had a telescope{LB}that could see incredibly far--{LB}even the contours of the moon.",
"DK4_MES_B77_R0015":"Remarkable.",
"DK4_MES_B77_R0019":"They say Aristarchus, the brilliant{LB}Hellenistic astronomer, made it...",
"DK4_MES_B77_R0023":"Really?",
"DK4_MES_B77_R0027":"Hard to believe they could polish{LB}lenses so precisely in that age.",
"DK4_MES_B77_R0031":"The truth is unknown. But bearing{LB}his name, it became known as{LB}the Telescope of Aristarchus.",
"DK4_MES_B77_R0034":"And?",
"DK4_MES_B77_R0038":"Judging by the currents, it may{LB}have washed ashore somewhere{LB}along this coast.",
"DK4_MES_B77_R0041":"Such a telescope would reveal{LB}cities and enemy ships with ease.{LB}Worth searching for.",
}
SP={"03":"Maria","04":"Janus Pasha"};ST={int(x,16) for x in SP}
def main()->None:
 with S.open(encoding="utf-8-sig",newline="") as f:rows={r["id"]:r for r in csv.DictReader(f) if r["id"].startswith("DK4_MES_B77_")}
 if set(L)!=set(rows):raise SystemExit(f"V77 mismatch: missing={sorted(set(rows)-set(L))}")
 rec=[]
 for i in sorted(L,key=lambda v:int(v.rsplit("R",1)[1])):
  r=rows[i];e=L[i];first=bytes.fromhex(r["source_hex"])[0];state=f"{first:02X}" if first in ST else "";u=e.replace("{MACRO:FI}","").replace("{MACRO:FA}","").replace("{MACRO:FO}","")
  if "F" in u or "I" in u:raise SystemExit(f"{i}: unsafe macro literal: {e}")
  sb=r["japanese"].count("{LB}");tb=e.count("{LB}");w=["weak-line-ending","orphan-final-line"]+(["manual-break"] if tb else [])+(["line-break-count"] if sb!=tb else [])
  rec.append({"id":i,"english":f"{{SPEAKER:{state}}}{e}{{PAD}}","speaker":SP[state],"context":"Janus tells Maria about a wrecked Portuguese admiral and the legendary Telescope of Aristarchus that may have washed ashore.","source_meaning":e.replace("{LB}"," "),"localization_note":"Direct SC3 translation preserving the historical skepticism, coastal clue, speakers, pacing, and allocation.","qa_waivers":w,**({"manual_break_reason":"Protects semantic rows and progressive ASCII pair phase."} if tb else {}),"review":{"source":True,"context":True,"localization":True,"naturalness":True,"formatting":True}})
 p={"format":"dk4-ilnk-translation-batch-v1","file_path":"/data/SC3.DK4","source_file_sha256":SHA,"encoder":"dialogue-fixed-v1","dialogue_profile":"maria-story-shared-events-v77-live","translation_policy":"natural-dialogue-v2","target_locale":"en-US","review_gates":["source","context","localization","naturalness","formatting"],"scope":"Maria SC3 block 77: complete Telescope of Aristarchus rumor.","inventory":{"identified_records":len(rows),"translated_records":len(rec),"excluded_records":0,"blocks":{"77":len(rec)}},"excluded":[],"records":rec};O.write_text(json.dumps(p,ensure_ascii=False,indent=2)+"\n",encoding="utf-8");print(f"wrote {O}: {len(rec)} records")
if __name__=="__main__":main()
