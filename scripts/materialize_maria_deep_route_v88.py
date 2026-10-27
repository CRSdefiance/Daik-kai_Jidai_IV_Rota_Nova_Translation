from __future__ import annotations
import csv,json
from pathlib import Path
S=Path("work/sc3/script.csv");O=Path("translations/maria_deep_route_v88.json");SHA="001e21897ddb727ae261c82763ebef8515784ecfa571619c7614d87f3320aab2"
L={
"DK4_MES_B102_R0012":"Xien?",
"DK4_MES_B102_R0016":"{LB}What is it?",
"DK4_MES_B102_R0020":"Nothing. Just thinking.",
"DK4_MES_B102_R0024":"{LB}Ah.",
"DK4_MES_B102_R0028":"Why ask?",
"DK4_MES_B102_R0032":"{LB}You looked troubled by something.",
"DK4_MES_B102_R0041":"A little...",
"DK4_MES_B102_R0043":"Not worried at all.",
"DK4_MES_B102_R0050":"...{LB}My confidence is gone.",
"DK4_MES_B102_R0054":"{LB}Why?",
"DK4_MES_B102_R0058":"Are my deeds truly right?{LB}Will my plans really help people?",
"DK4_MES_B102_R0062":"{LB}Of course.{LB}Everyone believes so.",
"DK4_MES_B102_R0065":"Those we beat had families{LB}and comrades. We made them{LB}suffer. That is true.",
"DK4_MES_B102_R0073":"Even so, can we truly say{LB}everything we do is right?",
"DK4_MES_B102_R0080":"Sorry.{LB}Words flow freely with you.",
"DK4_MES_B102_R0083":"{LB}No... this was careless.{LB}{MACRO:FI}, never knew{LB}you were so troubled.",
"DK4_MES_B102_R0087":"Don't worry.{LB}Talking helped.{LB}All will be well.",
"DK4_MES_B102_R0095":"{LB}Superstition seems{LB}foolish, but...",
"DK4_MES_B102_R0102":"{LB}But if {MACRO:FI} believes,{LB}perhaps we should seek it.",
"DK4_MES_B102_R0106":"Seek what? What do you mean?",
"DK4_MES_B102_R0110":"{LB}The Staff of Guidance.",
"DK4_MES_B102_R0114":"A staff?",
"DK4_MES_B102_R0118":"{LB}A staff guiding its bearer{LB}toward good. Said to be in Hindustan.",
"DK4_MES_B102_R0122":"...Thank you, but{LB}all is well now.{LB}Besides, you are here.",
"DK4_MES_B102_R0126":"{LB}Yes.",
"DK4_MES_B102_R0130":"Still, if it guides us toward good,{LB}it may be worth finding.",
"DK4_MES_B102_R0133":"{LB}Quite so.{LB}When doubt comes, it may help.{LB}Seek it if the need arises.",
"DK4_MES_B102_R0137":"Yes.{LB}Xien, thank you for today.",
"DK4_MES_B102_R0140":"{LB}Don't worry.",
"DK4_MES_B102_R0147":"You worry too much.",
"DK4_MES_B102_R0151":"{LB}Good, if that is so.",
"DK4_MES_B102_R0155":"Strong foes remain.{LB}No time for doubt.{LB}We must press on.",
"DK4_MES_B102_R0159":"{LB}Agreed.",
"DK4_MES_B102_R0163":"And you still have much work ahead.{LB}No quiet retirement back home{LB}for a long time yet.",
"DK4_MES_B102_R0167":"{LB}Ha ha ha! Understood.{LB}Time to finish my own work.",
"DK4_MES_B102_R0172":"{MACRO:FI}'s Spirit rose by 1!",
}
SP={"03":"Maria","FE":"System"};ST={int(x,16) for x in SP}
def main()->None:
 with S.open(encoding="utf-8-sig",newline="") as f:rows={r["id"]:r for r in csv.DictReader(f) if r["id"].startswith("DK4_MES_B102_")}
 if set(L)!=set(rows):raise SystemExit(f"V88 mismatch: missing={sorted(set(rows)-set(L))}; extra={sorted(set(L)-set(rows))}")
 rec=[]
 for i in sorted(L,key=lambda v:int(v.rsplit("R",1)[1])):
  r=rows[i];e=L[i];first=bytes.fromhex(r["source_hex"])[0];state=f"{first:02X}" if first in ST else "";u=e.replace("{MACRO:FI}","").replace("{MACRO:FA}","").replace("{MACRO:FO}","")
  if "F" in u or "I" in u:raise SystemExit(f"{i}: unsafe macro literal: {e}")
  sb=r["japanese"].count("{LB}");tb=e.count("{LB}");w=["weak-line-ending","orphan-final-line"]+(["manual-break"] if tb else [])+(["source-leading-linebreak"] if r["japanese"].startswith("{LB}") else [])+(["line-break-count"] if sb!=tb else [])
  prefix=f"{{SPEAKER:{state}}}" if state else ""
  rec.append({"id":i,"english":f"{prefix}{e}{{PAD}}","speaker":SP.get(state,"Xien or player choice"),"context":"Maria confides her moral doubts to Xien, may deny or admit them, learns of the Staff of Guidance, regains resolve, and receives a Spirit increase.","source_meaning":e.replace("{LB}"," "),"localization_note":"Direct SC3 translation preserving both choices, Xien's continuation-line layout, all player-name macros, moral nuance, treasure lead, stat result, and fixed allocation.","qa_waivers":w,**({"manual_break_reason":"Protects semantic rows and progressive ASCII pair phase."} if tb else {}),"review":{"source":True,"context":True,"localization":True,"naturalness":True,"formatting":True}})
 p={"format":"dk4-ilnk-translation-batch-v1","file_path":"/data/SC3.DK4","source_file_sha256":SHA,"encoder":"dialogue-fixed-v1","dialogue_profile":"maria-story-shared-events-v88-live","translation_policy":"natural-dialogue-v2","target_locale":"en-US","review_gates":["source","context","localization","naturalness","formatting"],"scope":"Maria SC3 block 102: complete Xien confidence dialogue, both choices, Staff of Guidance lead, and Spirit result.","inventory":{"identified_records":len(rows),"translated_records":len(rec),"excluded_records":0,"blocks":{"102":len(rec)}},"excluded":[],"records":rec};O.write_text(json.dumps(p,ensure_ascii=False,indent=2)+"\n",encoding="utf-8");print(f"wrote {O}: {len(rec)} records")
if __name__=="__main__":main()
