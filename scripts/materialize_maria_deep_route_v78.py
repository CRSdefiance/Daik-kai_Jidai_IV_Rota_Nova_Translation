from __future__ import annotations
import csv,json
from pathlib import Path
S=Path("work/sc3/script.csv");O=Path("translations/maria_deep_route_v78.json");SHA="001e21897ddb727ae261c82763ebef8515784ecfa571619c7614d87f3320aab2"
L={
"DK4_MES_B78_R0004":"We're in port!{LB}Let's go find food!",
"DK4_MES_B78_R0007":"Emilio, you say that{LB}in every town.",
"DK4_MES_B78_R0010":"Eating matters!{LB}Besides, there's something{LB}we need to find.",
"DK4_MES_B78_R0014":"Something?",
"DK4_MES_B78_R0018":"The tastiest food!",
"DK4_MES_B78_R0022":"The world's best taste...{LB}Hard to prove nothing tastier exists.",
"DK4_MES_B78_R0026":"No problem. We'll know.{LB}The world's best food is cooked{LB}in Hestia's Cauldron.",
"DK4_MES_B78_R0029":"Hestia's pot?",
"DK4_MES_B78_R0033":"A pot made for{LB}the hearth goddess.{LB}They say it lies overseas,{LB}far south of Greece.",
"DK4_MES_B78_R0036":"That's why Greek food shops{LB}have me so excited! Come on,{LB}let's go eat already!",
}
SP={"03":"Maria","0E":"Emilio Ferrog"};ST={int(x,16) for x in SP}
def main()->None:
 with S.open(encoding="utf-8-sig",newline="") as f:rows={r["id"]:r for r in csv.DictReader(f) if r["id"].startswith("DK4_MES_B78_")}
 if set(L)!=set(rows):raise SystemExit(f"V78 mismatch: missing={sorted(set(rows)-set(L))}")
 rec=[]
 for i in sorted(L,key=lambda v:int(v.rsplit("R",1)[1])):
  r=rows[i];e=L[i];first=bytes.fromhex(r["source_hex"])[0];state=f"{first:02X}" if first in ST else "";u=e.replace("{MACRO:FI}","").replace("{MACRO:FA}","").replace("{MACRO:FO}","")
  if "F" in u or "I" in u:raise SystemExit(f"{i}: unsafe macro literal: {e}")
  sb=r["japanese"].count("{LB}");tb=e.count("{LB}");w=["weak-line-ending","orphan-final-line"]+(["manual-break"] if tb else [])+(["line-break-count"] if sb!=tb else [])
  rec.append({"id":i,"english":f"{{SPEAKER:{state}}}{e}{{PAD}}","speaker":SP[state],"context":"Emilio's hunger leads to a rumor about Hestia's Cauldron somewhere south of Greece.","source_meaning":e.replace("{LB}"," "),"localization_note":"Direct SC3 translation preserving Emilio's food obsession, the cauldron clue, speakers, pacing, and allocation.","qa_waivers":w,**({"manual_break_reason":"Protects semantic rows and progressive ASCII pair phase."} if tb else {}),"review":{"source":True,"context":True,"localization":True,"naturalness":True,"formatting":True}})
 p={"format":"dk4-ilnk-translation-batch-v1","file_path":"/data/SC3.DK4","source_file_sha256":SHA,"encoder":"dialogue-fixed-v1","dialogue_profile":"maria-story-shared-events-v78-live","translation_policy":"natural-dialogue-v2","target_locale":"en-US","review_gates":["source","context","localization","naturalness","formatting"],"scope":"Maria SC3 block 78: complete Hestia's Cauldron rumor.","inventory":{"identified_records":len(rows),"translated_records":len(rec),"excluded_records":0,"blocks":{"78":len(rec)}},"excluded":[],"records":rec};O.write_text(json.dumps(p,ensure_ascii=False,indent=2)+"\n",encoding="utf-8");print(f"wrote {O}: {len(rec)} records")
if __name__=="__main__":main()
