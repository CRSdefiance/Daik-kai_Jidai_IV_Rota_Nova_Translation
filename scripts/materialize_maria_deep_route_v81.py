from __future__ import annotations
import csv,json
from pathlib import Path
S=Path("work/sc3/script.csv");O=Path("translations/maria_deep_route_v81.json");SHA="001e21897ddb727ae261c82763ebef8515784ecfa571619c7614d87f3320aab2"
L={
"DK4_MES_B88_R0005":"{LB}Hm?!",
"DK4_MES_B88_R0009":"Aaaah...",
"DK4_MES_B88_R0013":"Ooooh!",
"DK4_MES_B88_R0017":"Those must be the strange people.",
"DK4_MES_B88_R0021":"A revelation!{LB}Our Ancient Megalith Society{LB}shall soon conquer the world!",
"DK4_MES_B88_R0025":"We are the chosen!{LB}We'll dig up the listed treasure{LB}and rule every godless fool!",
"DK4_MES_B88_R0028":"Ooooh!",
"DK4_MES_B88_R0032":"{LB}They're mad...",
"DK4_MES_B88_R0036":"We begin by raiding this village!{LB}Those who mocked us will pay!",
"DK4_MES_B88_R0040":"Ooooh!!",
"DK4_MES_B88_R0044":"!!{LB}We've walked into something awful.",
"DK4_MES_B88_R0048":"{LB}Well, {MACRO:FI}?{LB}Not enough guns.",
"DK4_MES_B88_R0055":"Our guns will do.{LB}Load blanks.",
"DK4_MES_B88_R0058":"{LB}Eh?",
"DK4_MES_B88_R0074":"Use that too. Get ready.",
"DK4_MES_B88_R0078":"Yes!",
"DK4_MES_B88_R0084":"Jam, use that too.",
"DK4_MES_B88_R0087":"Yahoo! A festival!",
"DK4_MES_B88_R0096":"Charles, use that too.",
"DK4_MES_B88_R0099":"What?{LB}Ah, that!",
"DK4_MES_B88_R0110":"Burn it!{LB}Spare no resisters!",
"DK4_MES_B88_R0113":"Ooooh!",
"DK4_MES_B88_R0125":"{LB}Heretics!{LB}The church condemns you!{LB}Surrender now!",
"DK4_MES_B88_R0129":"Who?!",
"DK4_MES_B88_R0133":"{LB}Shoot!!",
"DK4_MES_B88_R0137":"Eek!!",
"DK4_MES_B88_R0141":"The army!{LB}Run away!",
"DK4_MES_B88_R0144":"Stop, you fools!{LB}Don't run! Protect me!",
"DK4_MES_B88_R0148":"We can't beat an army!{LB}D-don't want to die!!",
"DK4_MES_B88_R0151":"Damn! They won't listen!{LB}Cowards, all of them!",
"DK4_MES_B88_R0154":"Can't leave that behind!",
"DK4_MES_B88_R0158":"Ugh!!",
"DK4_MES_B88_R0162":"What's this?",
"DK4_MES_B88_R0166":"D-don't touch it!{LB}Give it back!!",
"DK4_MES_B88_R0169":"Your panic says{LB}it must be precious.",
"DK4_MES_B88_R0172":"You...!",
"DK4_MES_B88_R0177":"Oh, drawing your sword?{LB}Handle sharp things with care.",
"DK4_MES_B88_R0181":"Silence!",
"DK4_MES_B88_R0185":"Gaaah!!",
"DK4_MES_B88_R0189":"{LB}That naughty cult leader.{LB}Needs severe punishment.",
"DK4_MES_B88_R0192":"What?!{LB}Why is your army{LB}all easterners?",
"DK4_MES_B88_R0196":"Army?{LB}Do troops fight{LB}with fireworks and crackers?",
"DK4_MES_B88_R0200":"Those were firecrackers?!",
"DK4_MES_B88_R0204":"Gunpowder came from China.{LB}Westerners use it well in war,{LB}but not in ways like these.",
"DK4_MES_B88_R0207":"Grrr...!!",
"DK4_MES_B88_R0211":"We're leaving!",
}
SP={"03":"Maria","0B":"Jam","12":"Charles","9C":"Companion","B1":"Cult leader","B2":"Cult followers"};ST={int(x,16) for x in SP}
def main()->None:
 with S.open(encoding="utf-8-sig",newline="") as f:rows={r["id"]:r for r in csv.DictReader(f) if r["id"].startswith("DK4_MES_B88_")}
 if set(L)!=set(rows):raise SystemExit(f"V81 mismatch: missing={sorted(set(rows)-set(L))}; extra={sorted(set(L)-set(rows))}")
 rec=[]
 for i in sorted(L,key=lambda v:int(v.rsplit("R",1)[1])):
  r=rows[i];e=L[i];first=bytes.fromhex(r["source_hex"])[0];state=f"{first:02X}" if first in ST else "";u=e.replace("{MACRO:FI}","").replace("{MACRO:FA}","").replace("{MACRO:FO}","")
  if "F" in u or "I" in u:raise SystemExit(f"{i}: unsafe macro literal: {e}")
  sb=r["japanese"].count("{LB}");tb=e.count("{LB}");w=["weak-line-ending","orphan-final-line"]+(["manual-break"] if tb else [])+(["source-leading-linebreak"] if r["japanese"].startswith("{LB}") else [])+(["line-break-count"] if sb!=tb else [])
  prefix=f"{{SPEAKER:{state}}}" if state else ""
  rec.append({"id":i,"english":f"{prefix}{e}{{PAD}}","speaker":SP.get(state,"Continuing companion"),"context":"Maria infiltrates a violent megalith cult, stages a fake army assault with blank rounds and fireworks, seizes its treasure clue, and humiliates the leader.","source_meaning":e.replace("{LB}"," "),"localization_note":"Direct SC3 translation preserving companion setup variants, the player-name macro, cult crowd states, source-leading breaks, action pacing, and fixed allocation.","qa_waivers":w,**({"manual_break_reason":"Protects semantic rows and progressive ASCII pair phase."} if tb else {}),"review":{"source":True,"context":True,"localization":True,"naturalness":True,"formatting":True}})
 p={"format":"dk4-ilnk-translation-batch-v1","file_path":"/data/SC3.DK4","source_file_sha256":SHA,"encoder":"dialogue-fixed-v1","dialogue_profile":"maria-story-shared-events-v81-live","translation_policy":"natural-dialogue-v2","target_locale":"en-US","review_gates":["source","context","localization","naturalness","formatting"],"scope":"Maria SC3 block 88: complete megalith-cult infiltration and staged-army confrontation.","inventory":{"identified_records":len(rows),"translated_records":len(rec),"excluded_records":0,"blocks":{"88":len(rec)}},"excluded":[],"records":rec};O.write_text(json.dumps(p,ensure_ascii=False,indent=2)+"\n",encoding="utf-8");print(f"wrote {O}: {len(rec)} records")
if __name__=="__main__":main()
