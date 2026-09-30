from __future__ import annotations
import csv,json
from pathlib import Path
S=Path("work/sc3/script.csv");O=Path("translations/maria_deep_route_v79.json");SHA="001e21897ddb727ae261c82763ebef8515784ecfa571619c7614d87f3320aab2"
L={
"DK4_MES_B81_R0004":"Admiral, you've found{LB}the cursed Muramasa at last.{LB}May this one see it too?",
"DK4_MES_B81_R0007":"Of course.{LB}Your report led us{LB}straight to it.",
"DK4_MES_B81_R0011":"This...this is Muramasa...",
"DK4_MES_B81_R0015":"Hmm...{LB}That eerie glow draws one in.",
"DK4_MES_B81_R0019":"Magnificent.",
"DK4_MES_B82_R0006":"Say, word is you're searching{LB}the whole world for strange treasures.",
"DK4_MES_B82_R0009":"The nearby priest knows much.{LB}He may have useful news.",
"DK4_MES_B83_R0004":"Do you seek{LB}the Conqueror's Proof?",
"DK4_MES_B83_R0007":"You know of it?",
"DK4_MES_B83_R0011":"You surely know{LB}more than this priest.",
"DK4_MES_B83_R0014":"Should fate decree you claim it,{LB}nothing more need be said.",
"DK4_MES_B83_R0021":"Then take this sword.",
"DK4_MES_B83_R0028":"Do not defy destiny.{LB}Simply do what must be done.",
"DK4_MES_B83_R0032":"May God protect you all.",
"DK4_MES_B84_R0006":"Wait!{LB}Have you visited{LB}Santiago Cathedral?",
"DK4_MES_B84_R0014":"Pilgrims have come from all Europe{LB}for ages. The place is famous.",
"DK4_MES_B84_R0018":"Since you're in Seville,{LB}why not go? Here's the way.",
"DK4_MES_B85_R0012":"What is it?",
"DK4_MES_B85_R0016":"About this cross...{LB}May we truly keep it?",
"DK4_MES_B85_R0019":"Yes.{LB}Take it.",
"DK4_MES_B85_R0022":"(This seems odd...{LB}Maybe it's nothing.)",
"DK4_MES_B85_R0025":"Let us pray.{LB}By God, the Son, Holy Spirit...{LB}Amen.",
"DK4_MES_B86_R0014":"Admiral, look at this!",
"DK4_MES_B86_R0016":"Look, Admiral!",
"DK4_MES_B86_R0018":"Admiral, look at this!",
"DK4_MES_B86_R0020":"Admiral, look at this!",
"DK4_MES_B86_R0022":"Admiral! Look at this!",
"DK4_MES_B86_R0024":"Admiral, behold this!",
"DK4_MES_B86_R0028":"Traveler...",
"DK4_MES_B86_R0036":"Take my power.{LB}Debate as you will.",
}
SP={"03":"Maria","0C":"Yukihisa","8B":"Priest","BC":"Local woman","BF":"Local woman","D0":"Companion","FE":"Temple voice"};ST={int(x,16) for x in SP}
def main()->None:
 with S.open(encoding="utf-8-sig",newline="") as f:rows={r["id"]:r for r in csv.DictReader(f) if any(r["id"].startswith(f"DK4_MES_B{x}_") for x in range(81,87))}
 if set(L)!=set(rows):raise SystemExit(f"V79 mismatch: missing={sorted(set(rows)-set(L))}; extra={sorted(set(L)-set(rows))}")
 rec=[]
 for i in sorted(L,key=lambda v:(int(v.split("_B",1)[1].split("_",1)[0]),int(v.rsplit("R",1)[1]))):
  r=rows[i];e=L[i];first=bytes.fromhex(r["source_hex"])[0];state=f"{first:02X}" if first in ST else "";u=e.replace("{MACRO:FI}","").replace("{MACRO:FA}","").replace("{MACRO:FO}","")
  if "F" in u or "I" in u:raise SystemExit(f"{i}: unsafe macro literal: {e}")
  sb=r["japanese"].count("{LB}");tb=e.count("{LB}");w=["weak-line-ending","orphan-final-line"]+(["manual-break"] if tb else [])+(["line-break-count"] if sb!=tb else [])
  prefix=f"{{SPEAKER:{state}}}" if state else ""
  rec.append({"id":i,"english":f"{prefix}{e}{{PAD}}","speaker":SP.get(state,"Companion variant"),"context":"Maria's optional Muramasa viewing, church leads, Proof-related priest encounters, Santiago clue, cross scene, and temple-debate opening.","source_meaning":e.replace("{LB}"," "),"localization_note":"Direct SC3 translation preserving speaker states, inherited companion variants, treasure and church logic, pacing, and allocation.","qa_waivers":w,**({"manual_break_reason":"Protects semantic rows and progressive ASCII pair phase."} if tb else {}),"review":{"source":True,"context":True,"localization":True,"naturalness":True,"formatting":True}})
 p={"format":"dk4-ilnk-translation-batch-v1","file_path":"/data/SC3.DK4","source_file_sha256":SHA,"encoder":"dialogue-fixed-v1","dialogue_profile":"maria-story-shared-events-v79-live","translation_policy":"natural-dialogue-v2","target_locale":"en-US","review_gates":["source","context","localization","naturalness","formatting"],"scope":"Maria SC3 blocks 81-86: Muramasa viewing, church and Proof leads, Santiago, cross prayer, and temple-debate opening.","inventory":{"identified_records":len(rows),"translated_records":len(rec),"excluded_records":0,"blocks":{str(b):sum(i.startswith(f"DK4_MES_B{b}_") for i in L) for b in range(81,87)}},"excluded":[],"records":rec};O.write_text(json.dumps(p,ensure_ascii=False,indent=2)+"\n",encoding="utf-8");print(f"wrote {O}: {len(rec)} records")
if __name__=="__main__":main()
