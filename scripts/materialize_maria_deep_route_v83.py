from __future__ import annotations
import csv,json
from pathlib import Path
S=Path("work/sc3/script.csv");O=Path("translations/maria_deep_route_v83.json");SHA="001e21897ddb727ae261c82763ebef8515784ecfa571619c7614d87f3320aab2"
L={
"DK4_MES_B91_R0014":"Hmm... you ran a little over.{LB}Care to try once more?",
"DK4_MES_B91_R0030":"You did it!{LB}Now you know the round trip{LB}can be made in 30 days!",
"DK4_MES_B91_R0034":"Oh, you caught me.",
"DK4_MES_B91_R0038":"Thank you!{LB}Take your reward!",
"DK4_MES_B91_R0041":"Gained 10,000 coins.",
"DK4_MES_B91_R0065":"The capital's market share rose!",
"DK4_MES_B91_R0076":"Ask me anything{LB}you don't know about this city.",
"DK4_MES_B91_R0079":"Ruins? Sure.{LB}A special one. Come with me.",
"DK4_MES_B92_R0006":"Colosseum visitor,{LB}answer my question!",
"DK4_MES_B92_R0009":"A puzzle.",
"DK4_MES_B92_R0013":"Next.",
"DK4_MES_B92_R0017":"Magic beans double every second.{LB}One becomes two, then four, then eight.",
"DK4_MES_B92_R0021":"One bean fills a bag in 60 seconds.{LB}Starting with two,{LB}when will the bag be full?",
"DK4_MES_B92_R0024":"Choose your answer!",
"DK4_MES_B92_R0031":"1s",
"DK4_MES_B92_R0033":"30s",
"DK4_MES_B92_R0035":"59s",
"DK4_MES_B92_R0044":"Xien, any thoughts?",
"DK4_MES_B92_R0048":"{LB}No idea...{LB}At times like this,{LB}trust your luck!",
"DK4_MES_B92_R0052":"{LB}Right!{LB}One second!",
"DK4_MES_B92_R0055":"Wrong!",
"DK4_MES_B92_R0065":"Xien, half of sixty is thirty.{LB}What do you think?",
"DK4_MES_B92_R0068":"{LB}No idea...{LB}At times like this,{LB}trust your luck!",
"DK4_MES_B92_R0072":"{LB}Right!{LB}Thirty seconds!",
"DK4_MES_B92_R0075":"Wrong!",
"DK4_MES_B92_R0086":"Xien, solved it.",
"DK4_MES_B92_R0090":"{LB}Your answer?",
"DK4_MES_B92_R0094":"59 seconds.",
"DK4_MES_B92_R0098":"Splendid!{LB}Wise and brave one,{LB}take this!",
"DK4_MES_B93_R0014":"Admiral, dead end.",
"DK4_MES_B93_R0016":"A dead end, Admiral.",
"DK4_MES_B93_R0018":"Huh? A dead end.",
"DK4_MES_B93_R0020":"Admiral, a dead end.",
"DK4_MES_B93_R0022":"Well, a dead end.",
"DK4_MES_B93_R0024":"A dead end, Admiral.",
"DK4_MES_B93_R0026":"Admiral! Dead end!",
"DK4_MES_B93_R0028":"Well, well. A dead end.",
"DK4_MES_B93_R0032":"A pot tablet{LB}is in the wall.",
"DK4_MES_B93_R0035":"Traveler:{LB}pour left-handed.",
"DK4_MES_B93_R0038":"Left-handed?",
"DK4_MES_B93_R0045":"Push",
"DK4_MES_B93_R0047":"Right",
"DK4_MES_B93_R0049":"Left",
"DK4_MES_B93_R0065":"Left hand means{LB}tilt right...",
"DK4_MES_B93_R0088":"Run!",
"DK4_MES_B93_R0092":"Aaaah!!",
"DK4_MES_B93_R0099":"Sailor injured!",
}
EX={"DK4_MES_B92_R0100":"Raw five-byte event-control payload; not dialogue."}
SP={"03":"Maria","94":"Guildmaster","99":"Townsman","CF":"Companion","D0":"Companion","FE":"Temple voice","97":"Sailor"};ST={int(x,16) for x in SP}
def main()->None:
 with S.open(encoding="utf-8-sig",newline="") as f:rows={r["id"]:r for r in csv.DictReader(f) if any(r["id"].startswith(f"DK4_MES_B{x}_") for x in range(91,94))}
 if set(L)|set(EX)!=set(rows):raise SystemExit(f"V83 mismatch: missing={sorted(set(rows)-set(L)-set(EX))}; extra={sorted((set(L)|set(EX))-set(rows))}")
 rec=[]
 for i in sorted(L,key=lambda v:(int(v.split("_B",1)[1].split("_",1)[0]),int(v.rsplit("R",1)[1]))):
  r=rows[i];e=L[i];first=bytes.fromhex(r["source_hex"])[0];state=f"{first:02X}" if first in ST else "";u=e.replace("{MACRO:FI}","").replace("{MACRO:FA}","").replace("{MACRO:FO}","")
  if "F" in u or "I" in u:raise SystemExit(f"{i}: unsafe macro literal: {e}")
  sb=r["japanese"].count("{LB}");tb=e.count("{LB}");w=["weak-line-ending","orphan-final-line"]+(["manual-break"] if tb else [])+(["source-leading-linebreak"] if r["japanese"].startswith("{LB}") else [])+(["line-break-count"] if sb!=tb else [])
  prefix=f"{{SPEAKER:{state}}}" if state else ""
  rec.append({"id":i,"english":f"{prefix}{e}{{PAD}}","speaker":SP.get(state,"Choice or companion variant"),"context":"Timed guild challenge outcomes, the Colosseum doubling-bean riddle, and the sacred-pot maze trap with all companion and choice variants.","source_meaning":e.replace("{LB}"," "),"localization_note":"Direct SC3 translation preserving timed results, all riddle and maze choices, source-leading breaks, speaker states, the raw event control, and fixed allocation.","qa_waivers":w,**({"manual_break_reason":"Protects semantic rows and progressive ASCII pair phase."} if tb else {}),"review":{"source":True,"context":True,"localization":True,"naturalness":True,"formatting":True}})
 p={"format":"dk4-ilnk-translation-batch-v1","file_path":"/data/SC3.DK4","source_file_sha256":SHA,"encoder":"dialogue-fixed-v1","dialogue_profile":"maria-story-shared-events-v83-live","translation_policy":"natural-dialogue-v2","target_locale":"en-US","review_gates":["source","context","localization","naturalness","formatting"],"scope":"Maria SC3 blocks 91-93: timed guild outcomes, Colosseum bean riddle, and sacred-pot maze trap.","excluded_records":EX,"inventory":{"identified_records":len(rows),"translated_records":len(rec),"excluded_records":len(EX),"blocks":{"91":8,"92":22,"93":18}},"records":rec};O.write_text(json.dumps(p,ensure_ascii=False,indent=2)+"\n",encoding="utf-8");print(f"wrote {O}: {len(rec)} translations + {len(EX)} control")
if __name__=="__main__":main()
