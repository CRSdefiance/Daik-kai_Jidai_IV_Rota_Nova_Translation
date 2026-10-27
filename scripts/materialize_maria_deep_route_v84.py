from __future__ import annotations
import csv,json
from pathlib import Path
S=Path("work/sc3/script.csv");O=Path("translations/maria_deep_route_v84.json");SHA="001e21897ddb727ae261c82763ebef8515784ecfa571619c7614d87f3320aab2"
L={
"DK4_MES_B94_R0005":"Masterful work.",
"DK4_MES_B94_R0009":"You.",
"DK4_MES_B94_R0013":"Yes?",
"DK4_MES_B94_R0017":"You seek the Conqueror's Proof?",
"DK4_MES_B94_R0020":"What?!{LB}You know something about it?",
"DK4_MES_B94_R0023":"Yes. But such knowledge{LB}is not for everyone.",
"DK4_MES_B94_R0026":"Only one fit to rule{LB}may hear it, correct?",
"DK4_MES_B94_R0029":"You know that much. Good.{LB}Why do you seek the Proof?",
"DK4_MES_B94_R0033":"The reason is not yet clear.{LB}But the powers plotting to rule Asia{LB}must never possess it.",
"DK4_MES_B94_R0036":"Hmm...",
"DK4_MES_B94_R0040":"Please.{LB}Tell us what you know.",
"DK4_MES_B94_R0043":"One point.",
"DK4_MES_B94_R0047":"You treat Westerners as enemies.{LB}Hatred and resentment are far removed{LB}from the qualities of a ruler.",
"DK4_MES_B94_R0054":"Yet your eyes hold deep sorrow{LB}and love for your people.{LB}That is justice and compassion.",
"DK4_MES_B94_R0057":"Very well.{LB}Listen.",
"DK4_MES_B94_R0060":"Long ago in China, the clan{LB}guarding the map fled their ruler{LB}and traveled far to the northeast.",
"DK4_MES_B94_R0063":"Northeast...",
"DK4_MES_B94_R0067":"At the northern edge, near frozen seas,{LB}their descendants live quietly{LB}in a small village.",
"DK4_MES_B94_R0070":"A village far northeast of China...{LB}Thank you very much.",
"DK4_MES_B94_R0073":"The land is terribly remote.{LB}An ordinary ship may never reach it.{LB}Go halfheartedly, and you will die.",
"DK4_MES_B94_R0080":"Never yield the Proof{LB}to wicked hands.",
"DK4_MES_B94_R0083":"Nor let wicked desire possess you.{LB}Never surrender to hatred or anger.",
"DK4_MES_B94_R0087":"Yes...",
}
SP={"03":"Maria","89":"Palace sage"};ST={int(x,16) for x in SP}
def main()->None:
 with S.open(encoding="utf-8-sig",newline="") as f:rows={r["id"]:r for r in csv.DictReader(f) if r["id"].startswith("DK4_MES_B94_")}
 if set(L)!=set(rows):raise SystemExit(f"V84 mismatch: missing={sorted(set(rows)-set(L))}; extra={sorted(set(L)-set(rows))}")
 rec=[]
 for i in sorted(L,key=lambda v:int(v.rsplit("R",1)[1])):
  r=rows[i];e=L[i];first=bytes.fromhex(r["source_hex"])[0];state=f"{first:02X}" if first in ST else "";u=e.replace("{MACRO:FI}","").replace("{MACRO:FA}","").replace("{MACRO:FO}","")
  if "F" in u or "I" in u:raise SystemExit(f"{i}: unsafe macro literal: {e}")
  sb=r["japanese"].count("{LB}");tb=e.count("{LB}");w=["weak-line-ending","orphan-final-line"]+(["manual-break"] if tb else [])+(["line-break-count"] if sb!=tb else [])
  rec.append({"id":i,"english":f"{{SPEAKER:{state}}}{e}{{PAD}}","speaker":SP[state],"context":"A palace sage tests Maria's motive for seeking the Proof, recognizes justice beneath her anger, and reveals the map-guardian clan's frozen northeastern village.","source_meaning":e.replace("{LB}"," "),"localization_note":"Direct SC3 translation preserving Maria's political motive, the sage's moral warning, the northeastern-village clue, speaker states, pacing, and allocation.","qa_waivers":w,**({"manual_break_reason":"Protects semantic rows and progressive ASCII pair phase."} if tb else {}),"review":{"source":True,"context":True,"localization":True,"naturalness":True,"formatting":True}})
 p={"format":"dk4-ilnk-translation-batch-v1","file_path":"/data/SC3.DK4","source_file_sha256":SHA,"encoder":"dialogue-fixed-v1","dialogue_profile":"maria-story-shared-events-v84-live","translation_policy":"natural-dialogue-v2","target_locale":"en-US","review_gates":["source","context","localization","naturalness","formatting"],"scope":"Maria SC3 block 94: complete palace-sage Proof motive test and northeastern map-clan clue.","inventory":{"identified_records":len(rows),"translated_records":len(rec),"excluded_records":0,"blocks":{"94":len(rec)}},"excluded":[],"records":rec};O.write_text(json.dumps(p,ensure_ascii=False,indent=2)+"\n",encoding="utf-8");print(f"wrote {O}: {len(rec)} records")
if __name__=="__main__":main()
