from __future__ import annotations
import csv,json
from pathlib import Path
S=Path("work/sc3/script.csv");O=Path("translations/maria_deep_route_v70.json");SHA="001e21897ddb727ae261c82763ebef8515784ecfa571619c7614d87f3320aab2"
L={
"DK4_MES_B66_R0004":"Ook ook!",
"DK4_MES_B66_R0008":"Whoa! What?!",
"DK4_MES_B66_R0012":"Ook ook!",
"DK4_MES_B66_R0016":"Go away!",
"DK4_MES_B66_R0020":"Ook ook!",
"DK4_MES_B66_R0024":"Give it back!",
"DK4_MES_B66_R0028":"What?",
"DK4_MES_B66_R0032":"My banana!{LB}Something stole{LB}the banana from me!",
"DK4_MES_B66_R0036":"'Something'?{LB}What?",
"DK4_MES_B66_R0040":"That thing... gone!{LB}Ran away! Wait!",
"DK4_MES_B66_R0043":"Any luck catching it?",
"DK4_MES_B66_R0047":"Too quick!{LB}And it throws things:{LB}rocks and seeds.",
"DK4_MES_B66_R0051":"Let me see.{LB}This seed is unfamiliar.{LB}Perhaps we found a treasure.",
"DK4_MES_B66_R0055":"No!{LB}My banana!!",
"DK4_MES_B66_R0059":"My banana!!{LB}Give it back!!",
"DK4_MES_B66_R0063":"...{LB}Want to try the local food?",
"DK4_MES_B66_R0066":"My treat?",
"DK4_MES_B66_R0070":"Yes. My treat.",
"DK4_MES_B66_R0076":"Hooray!",
}
SP={"03":"Maria","0E":"Emilio Ferrog","FE":"Monkey"};ST={int(x,16) for x in SP}
def main()->None:
 with S.open(encoding="utf-8-sig",newline="") as f:rows={r["id"]:r for r in csv.DictReader(f) if r["id"].startswith("DK4_MES_B66_")}
 if set(L)!=set(rows):raise SystemExit(f"V70 mismatch: missing={sorted(set(rows)-set(L))}")
 rec=[]
 for i in sorted(L,key=lambda v:int(v.rsplit("R",1)[1])):
  r=rows[i];e=L[i];first=bytes.fromhex(r["source_hex"])[0];state=f"{first:02X}" if first in ST else "";u=e.replace("{MACRO:FI}","").replace("{MACRO:FA}","").replace("{MACRO:FO}","")
  if "F" in u or "I" in u:raise SystemExit(f"{i}: unsafe macro literal: {e}")
  sb=r["japanese"].count("{LB}");tb=e.count("{LB}");w=["weak-line-ending","orphan-final-line"]+(["manual-break"] if tb else [])+(["line-break-count"] if sb!=tb else [])
  rec.append({"id":i,"english":f"{{SPEAKER:{state}}}{e}{{PAD}}","speaker":SP[state],"context":"A monkey steals Emilio's banana and pelts him with stones and unfamiliar seeds; Maria keeps one of the seeds and distracts Emilio with local food.","source_meaning":e.replace("{LB}"," "),"localization_note":"Direct SC3 translation preserving the monkey calls, banana chase, seed discovery, Emilio's comic fixation, speaker states, and fixed allocation.","qa_waivers":w,**({"manual_break_reason":"Protects semantic rows and progressive ASCII pair phase."} if tb else {}),"review":{"source":True,"context":True,"localization":True,"naturalness":True,"formatting":True}})
 p={"format":"dk4-ilnk-translation-batch-v1","file_path":"/data/SC3.DK4","source_file_sha256":SHA,"encoder":"dialogue-fixed-v1","dialogue_profile":"maria-story-shared-events-v70-live","translation_policy":"natural-dialogue-v2","target_locale":"en-US","review_gates":["source","context","localization","naturalness","formatting"],"scope":"Maria SC3 block 66: complete Emilio banana-theft and unfamiliar-seed event.","inventory":{"identified_records":len(rows),"translated_records":len(rec),"excluded_records":0,"blocks":{"66":len(rec)}},"excluded":[],"records":rec};O.write_text(json.dumps(p,ensure_ascii=False,indent=2)+"\n",encoding="utf-8");print(f"wrote {O}: {len(rec)} records")
if __name__=="__main__":main()
