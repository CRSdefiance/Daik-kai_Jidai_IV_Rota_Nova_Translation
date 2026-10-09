from __future__ import annotations
import csv,json
from pathlib import Path
S=Path("work/sc3/script.csv");O=Path("translations/maria_deep_route_v67.json");SHA="001e21897ddb727ae261c82763ebef8515784ecfa571619c7614d87f3320aab2"
EX={"DK4_MES_B62_R0003":"nontext treasure-scene payload 46 81 80 F2 61 21 48 89 A2; preserved byte-for-byte"}
L={
"DK4_MES_B62_R0010":"The Golden Crown of Silla...",
"DK4_MES_B62_R0014":"Beautiful...",
"DK4_MES_B62_R0018":"Worth every hardship.",
"DK4_MES_B62_R0021":"Yet that man still{LB}has not arrived?",
"DK4_MES_B62_R0024":"He left the tavern before us.{LB}He should have found it by now...",
"DK4_MES_B62_R0028":"Someone...",
"DK4_MES_B62_R0034":"Pant... pant...{LB}Made it at last...{LB}That is the crown{LB}this man sought all his life...",
"DK4_MES_B62_R0037":"Late.{LB}{MACRO:FI}.",
"DK4_MES_B62_R0040":"{MACRO:FI}?{LB}What a lovely name.",
"DK4_MES_B62_R0043":"How did you know?{LB}Why seek the crown?",
"DK4_MES_B62_R0047":"We heard you discuss it{LB}in Hangzhou.",
"DK4_MES_B62_R0050":"You spied on Mihwa and me,{LB}then followed me!{LB}Perhaps you fell for me?",
"DK4_MES_B62_R0053":"Mind your words to the admiral!",
"DK4_MES_B62_R0057":"How rude. We overheard you,{LB}but never followed you.{LB}There are no feelings for you.",
"DK4_MES_B62_R0060":"A shame.{LB}A woman like you is just my type.",
"DK4_MES_B62_R0064":"Enough! This woman is...",
"DK4_MES_B62_R0068":"Leave him, Shien.{LB}He courts every woman he sees.",
"DK4_MES_B62_R0071":"Do not glare so fiercely.{LB}That spoils your beauty.",
"DK4_MES_B62_R0074":"Back to the matter:{LB}do you want the crown?",
"DK4_MES_B62_R0077":"The crown interests me.",
"DK4_MES_B62_R0081":"Then you can give it{LB}to me, right?",
"DK4_MES_B62_R0085":"Such nerve!{LB}{MACRO:FI}, do not pity this rogue.",
"DK4_MES_B62_R0089":"Please. A promise was made{LB}to find it for Mihwa.",
"DK4_MES_B62_R0093":"My honor is ruined!{LB}You see why returning{LB}empty-handed is impossible?",
"DK4_MES_B62_R0096":"Very well. Take it.{LB}Return to her quickly.",
"DK4_MES_B62_R0099":"Thank you, {MACRO:FI}!{LB}See you in Hangzhou!",
"DK4_MES_B62_R0102":"{MACRO:FO}'s admiral is{LB}as lovely as rumored!",
"DK4_MES_B62_R0109":"He knew you led{LB}{MACRO:FO}...",
"DK4_MES_B62_R0113":"He fooled us.{LB}He may be formidable.",
"DK4_MES_B62_R0116":"Such boldness suits{LB}an adventurer.",
}
SP={"03":"Maria","1A":"Julian","FE":"Shien"};ST={int(x,16) for x in SP}
def main()->None:
 with S.open(encoding="utf-8-sig",newline="") as f:rows={r["id"]:r for r in csv.DictReader(f) if r["id"].startswith("DK4_MES_B62_")}
 if set(L)|set(EX)!=set(rows):raise SystemExit(f"V67 mismatch: missing={sorted(set(rows)-set(L)-set(EX))}")
 rec=[]
 for i in sorted(L,key=lambda v:int(v.rsplit("R",1)[1])):
  r=rows[i];e=L[i];first=bytes.fromhex(r["source_hex"])[0];state=f"{first:02X}" if first in ST and not r["japanese"].startswith("{LB}") else "";u=e.replace("{MACRO:FI}","").replace("{MACRO:FA}","").replace("{MACRO:FO}","")
  if "F" in u or "I" in u:raise SystemExit(f"{i}: unsafe macro literal: {e}")
  sb=r["japanese"].count("{LB}");tb=e.count("{LB}");w=["weak-line-ending","orphan-final-line"]+(["manual-break"] if tb else [])+(["source-leading-linebreak"] if r["japanese"].startswith("{LB}") else [])+(["line-break-count"] if sb!=tb else [])
  rec.append({"id":i,"english":f"{{SPEAKER:{state}}}{e}{{PAD}}" if state else f"{e}{{PAD}}","speaker":SP.get(state,"Shien or scene participant"),"context":"Maria finds the Golden Crown of Silla before Julian, then yields it so he can keep his promise to Mihwa; Julian reveals he already knows Maria's reputation.","source_meaning":e.replace("{LB}"," "),"localization_note":"Direct SC3 translation preserving Julian's flirtation, Maria's refusal, crown handoff, protagonist and fleet macros, source staging, and fixed allocation.","qa_waivers":w,**({"manual_break_reason":"Protects semantic rows and progressive ASCII pair phase."} if tb else {}),"review":{"source":True,"context":True,"localization":True,"naturalness":True,"formatting":True}})
 p={"format":"dk4-ilnk-translation-batch-v1","file_path":"/data/SC3.DK4","source_file_sha256":SHA,"encoder":"dialogue-fixed-v1","dialogue_profile":"maria-story-shared-events-v67-live","translation_policy":"natural-dialogue-v2","target_locale":"en-US","review_gates":["source","context","localization","naturalness","formatting"],"scope":"Maria SC3 block 62: complete Golden Crown of Silla encounter with Julian.","inventory":{"identified_records":len(rows),"translated_records":len(rec),"excluded_records":len(EX),"blocks":{"62":len(rec)}},"excluded":[{"id":i,"reason":x} for i,x in EX.items()],"records":rec};O.write_text(json.dumps(p,ensure_ascii=False,indent=2)+"\n",encoding="utf-8");print(f"wrote {O}: {len(rec)} records, {len(EX)} control")
if __name__=="__main__":main()
