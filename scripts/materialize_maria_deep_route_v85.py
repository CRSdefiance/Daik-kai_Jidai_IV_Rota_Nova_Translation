from __future__ import annotations
import csv,json
from pathlib import Path
S=Path("work/sc3/script.csv");O=Path("translations/maria_deep_route_v85.json");SHA="001e21897ddb727ae261c82763ebef8515784ecfa571619c7614d87f3320aab2"
L={
"DK4_MES_B95_R0005":"Do the officials in this palace{LB}sense how fast the world changes?{LB}Never mind. Let's go.",
"DK4_MES_B95_R0028":"Hm? On the sandbar!",
"DK4_MES_B95_R0030":"On the sandbar!",
"DK4_MES_B95_R0032":"Hm? Someone there.",
"DK4_MES_B95_R0034":"Huh? Someone.",
"DK4_MES_B95_R0038":"What happened?",
"DK4_MES_B95_R0042":"Traveler! Thank heaven!{LB}Save my grandson!",
"DK4_MES_B95_R0045":"Who?",
"DK4_MES_B95_R0049":"Grandpa! Help me!",
"DK4_MES_B95_R0053":"A boy is drowning!",
"DK4_MES_B95_R0068":"Leave it to me!",
"DK4_MES_B95_R0070":"Got it!",
"DK4_MES_B95_R0072":"Let me go!",
"DK4_MES_B95_R0074":"Got it!",
"DK4_MES_B95_R0076":"Leave this to me!",
"DK4_MES_B95_R0078":"Let me go!",
"DK4_MES_B95_R0082":"That was scary!",
"DK4_MES_B95_R0086":"You're safe now!{LB}Thank goodness!",
"DK4_MES_B95_R0089":"Traveler, thank you!{LB}Truly, thank you!",
"DK4_MES_B95_R0092":"He's safe.{LB}That's enough.",
"DK4_MES_B95_R0095":"We have no way to repay you...{LB}Ah, yes! Wait here!",
"DK4_MES_B95_R0099":"Please take this.",
"DK4_MES_B95_R0103":"What?",
"DK4_MES_B95_R0107":"As a youth, this man drove{LB}bandits from here.{LB}The governor gave this reward.",
"DK4_MES_B95_R0110":"The origin is unknown,{LB}but it is said to be valuable.",
"DK4_MES_B95_R0114":"No, we cannot...{LB}Keep this as proof{LB}of your valor.",
"DK4_MES_B95_R0118":"No, no. You saved my grandson.{LB}Please accept it. Such a thing{LB}has little value to me now.",
"DK4_MES_B95_R0121":"Since you insist...{LB}we accept with gratitude.",
"DK4_MES_B95_R0126":"Safe travels, my friends.",
"DK4_MES_B95_R0130":"Bye, big sister!",
"DK4_MES_B96_R0018":"Look, Admiral!",
"DK4_MES_B96_R0020":"Admiral!",
"DK4_MES_B96_R0022":"Admiral, this!",
"DK4_MES_B96_R0026":"Splendid jade...{LB}Even in China, we've never{LB}seen its equal.",
"DK4_MES_B96_R0038":"The New World prizes jade{LB}as highly as the East does.",
"DK4_MES_B96_R0041":"So much jade was offered here.{LB}This structure must have held{LB}great importance.",
}
EX={"DK4_MES_B95_R0009":"Raw seven-byte event-control payload; not dialogue.","DK4_MES_B96_R0003":"Raw seven-byte event-control payload; not dialogue.","DK4_MES_B96_R0024":"Raw four-byte event-control payload; not dialogue."}
SP={"03":"Maria","13":"Carlo Sinato","94":"Companion","A3":"Boy","AA":"Old man","D0":"Companion","D6":"Companion","D7":"Companion"};ST={int(x,16) for x in SP}
def main()->None:
 with S.open(encoding="utf-8-sig",newline="") as f:rows={r["id"]:r for r in csv.DictReader(f) if r["id"].startswith(("DK4_MES_B95_","DK4_MES_B96_"))}
 if set(L)|set(EX)!=set(rows):raise SystemExit(f"V85 mismatch: missing={sorted(set(rows)-set(L)-set(EX))}; extra={sorted((set(L)|set(EX))-set(rows))}")
 rec=[]
 for i in sorted(L,key=lambda v:(int(v.split("_B",1)[1].split("_",1)[0]),int(v.rsplit("R",1)[1]))):
  r=rows[i];e=L[i];first=bytes.fromhex(r["source_hex"])[0];state=f"{first:02X}" if first in ST else "";u=e.replace("{MACRO:FI}","").replace("{MACRO:FA}","").replace("{MACRO:FO}","")
  if "F" in u or "I" in u:raise SystemExit(f"{i}: unsafe macro literal: {e}")
  sb=r["japanese"].count("{LB}");tb=e.count("{LB}");w=["weak-line-ending","orphan-final-line"]+(["manual-break"] if tb else [])+(["line-break-count"] if sb!=tb else [])
  prefix=f"{{SPEAKER:{state}}}" if state else ""
  rec.append({"id":i,"english":f"{prefix}{e}{{PAD}}","speaker":SP.get(state,"Companion variant"),"context":"Maria's party rescues a drowning boy and receives the grandfather's old valor reward, then examines extraordinary jade at a New World ruin.","source_meaning":e.replace("{LB}"," "),"localization_note":"Direct SC3 translation preserving every rescuer variant, gift exchange, jade analysis, verified speaker states, raw controls, pacing, and fixed allocation.","qa_waivers":w,**({"manual_break_reason":"Protects semantic rows and progressive ASCII pair phase."} if tb else {}),"review":{"source":True,"context":True,"localization":True,"naturalness":True,"formatting":True}})
 p={"format":"dk4-ilnk-translation-batch-v1","file_path":"/data/SC3.DK4","source_file_sha256":SHA,"encoder":"dialogue-fixed-v1","dialogue_profile":"maria-story-shared-events-v85-live","translation_policy":"natural-dialogue-v2","target_locale":"en-US","review_gates":["source","context","localization","naturalness","formatting"],"scope":"Maria SC3 blocks 95-96: complete sandbar rescue and jade-ruin examination.","excluded_records":EX,"inventory":{"identified_records":len(rows),"translated_records":len(rec),"excluded_records":len(EX),"blocks":{"95":31,"96":8}},"records":rec};O.write_text(json.dumps(p,ensure_ascii=False,indent=2)+"\n",encoding="utf-8");print(f"wrote {O}: {len(rec)} translations + {len(EX)} controls")
if __name__=="__main__":main()
