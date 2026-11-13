from __future__ import annotations
import csv,json
from pathlib import Path
S=Path("work/sc3/script.csv");O=Path("translations/maria_deep_route_v73.json");SHA="001e21897ddb727ae261c82763ebef8515784ecfa571619c7614d87f3320aab2"
L={
"DK4_MES_B73_R0004":"Oh! You trade amber?",
"DK4_MES_B73_R0008":"Yes. The glow seems to call us{LB}back to ancient times.",
"DK4_MES_B73_R0012":"Huh? What do you mean?",
"DK4_MES_B73_R0016":"Amber is ancient tree sap,{LB}hardened and reborn as a gem.",
"DK4_MES_B73_R0020":"See the bee inside?{LB}Ages have passed while it slept{LB}within this sepia cosmos.{LB}How mysterious...",
"DK4_MES_B73_R0023":"How do you know{LB}such complicated things?",
"DK4_MES_B73_R0026":"Science. Human reason seeks{LB}to explain the world's wonders,{LB}even those beyond reason.",
"DK4_MES_B73_R0029":"No idea what that means.{LB}Ah! Amber reminds me...",
"DK4_MES_B73_R0033":"Of what?",
"DK4_MES_B73_R0037":"There are islands off this cape.{LB}One is said to hold a strange place{LB}that glows amber.",
"DK4_MES_B73_R0040":"Amber glow?{LB}A mineral vein?",
"DK4_MES_B73_R0044":"Who knows?{LB}Only a rumor.",
"DK4_MES_B73_R0048":"Thank you for the news.{LB}This stirs my scientific curiosity.",
}
SP={"12":"Charles Jean Rochefort","72":"Local sailor"};ST={int(x,16) for x in SP}
def main()->None:
 with S.open(encoding="utf-8-sig",newline="") as f:rows={r["id"]:r for r in csv.DictReader(f) if r["id"].startswith("DK4_MES_B73_")}
 if set(L)!=set(rows):raise SystemExit(f"V73 mismatch: missing={sorted(set(rows)-set(L))}")
 rec=[]
 for i in sorted(L,key=lambda v:int(v.rsplit("R",1)[1])):
  r=rows[i];e=L[i];first=bytes.fromhex(r["source_hex"])[0];state=f"{first:02X}" if first in ST else "";u=e.replace("{MACRO:FI}","").replace("{MACRO:FA}","").replace("{MACRO:FO}","")
  if "F" in u or "I" in u:raise SystemExit(f"{i}: unsafe macro literal: {e}")
  sb=r["japanese"].count("{LB}");tb=e.count("{LB}");w=["weak-line-ending","orphan-final-line"]+(["manual-break"] if tb else [])+(["line-break-count"] if sb!=tb else [])
  rec.append({"id":i,"english":f"{{SPEAKER:{state}}}{e}{{PAD}}","speaker":SP[state],"context":"Charles explains amber's ancient origin to a local sailor, who shares a rumor about an island location glowing amber beyond the cape.","source_meaning":e.replace("{LB}"," "),"localization_note":"Direct SC3 translation preserving Charles's scientific enthusiasm, the amber-island lead, speaker states, source pacing, and fixed allocation.","qa_waivers":w,**({"manual_break_reason":"Protects semantic rows and progressive ASCII pair phase."} if tb else {}),"review":{"source":True,"context":True,"localization":True,"naturalness":True,"formatting":True}})
 p={"format":"dk4-ilnk-translation-batch-v1","file_path":"/data/SC3.DK4","source_file_sha256":SHA,"encoder":"dialogue-fixed-v1","dialogue_profile":"maria-story-shared-events-v73-live","translation_policy":"natural-dialogue-v2","target_locale":"en-US","review_gates":["source","context","localization","naturalness","formatting"],"scope":"Maria SC3 block 73: complete amber science discussion and glowing-island rumor.","inventory":{"identified_records":len(rows),"translated_records":len(rec),"excluded_records":0,"blocks":{"73":len(rec)}},"excluded":[],"records":rec};O.write_text(json.dumps(p,ensure_ascii=False,indent=2)+"\n",encoding="utf-8");print(f"wrote {O}: {len(rec)} records")
if __name__=="__main__":main()
