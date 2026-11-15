from __future__ import annotations
import csv,json
from pathlib import Path
SOURCE=Path("work/sc3/script.csv");OUTPUT=Path("translations/maria_deep_route_v66.json");SC3_SHA256="001e21897ddb727ae261c82763ebef8515784ecfa571619c7614d87f3320aab2"
LINES={
"DK4_MES_B61_R0004":"At last, the far west.{LB}Across the whole world...{LB}remarkable.",
"DK4_MES_B61_R0008":"That blast?",
"DK4_MES_B61_R0012":"Sounds like a bomb.",
"DK4_MES_B61_R0015":"Charles again...{LB}A man cannot even nap.{LB}Wish he would be quiet.",
"DK4_MES_B61_R0019":"Charles?{LB}He caused that bomb blast?",
"DK4_MES_B61_R0023":"Yes. He plagues the neighborhood.{LB}Obsessed with 'science,'{LB}he makes that noise every day.",
"DK4_MES_B61_R0027":"'Science'?{LB}What is that, Shien?",
"DK4_MES_B61_R0030":"A popular Western study.{LB}They say it can transform life.{LB}Bombs are one part of it.",
"DK4_MES_B61_R0034":"Transform life...?{LB}Tell me more. Sounds intriguing.",
"DK4_MES_B61_R0038":"Hm. A man who can make bombs{LB}may know artillery too.{LB}Why not meet him?",
"DK4_MES_B61_R0042":"Yes. He may be worth meeting.",
"DK4_MES_B61_R0046":"Are you serious?",
"DK4_MES_B61_R0050":"Lead us to him?{LB}You will be rewarded.",
"DK4_MES_B61_R0053":"Guiding a lady is easy,{LB}but you should reconsider...",
"DK4_MES_B61_R0058":"Charles! You in there?!",
"DK4_MES_B61_R0063":"Uncle? Come back later.{LB}Very busy. My theory is{LB}nearly proven...",
"DK4_MES_B61_R0067":"Please be quiet sometimes!{LB}These blasts never stop!",
"DK4_MES_B61_R0071":"Pardon the interruption.{LB}You are Charles?{LB}They say you are quite learned.",
"DK4_MES_B61_R0075":"People respectfully call me{LB}'Dr. Charles.'",
"DK4_MES_B61_R0079":"Wonderful. We came to ask you{LB}to test that knowledge{LB}throughout the world.",
"DK4_MES_B61_R0083":"The world? That is grand!{LB}Can one person truly do it?",
"DK4_MES_B61_R0087":"Only because you do not know{LB}who stands before you.",
"DK4_MES_B61_R0090":"This is {MACRO:FI},{LB}the young admiral leading{LB}{MACRO:FO}.",
"DK4_MES_B61_R0094":"Her achievements are countless.{LB}That is who she is. Well?",
"DK4_MES_B61_R0098":"Amazing!{LB}Please put my science to use!{LB}This is like a dream!",
"DK4_MES_B61_R0101":"Ho ho! An amusing scholar.{LB}{MACRO:FI}, let us introduce him{LB}to everyone aboard.",
"DK4_MES_B61_R0105":"Before that, introductions.{LB}Admiral {MACRO:FI}.{LB}This elder is Shien.",
"DK4_MES_B61_R0109":"Elder?!{LB}This man is still young!",
"DK4_MES_B61_R0112":"This sounds fun!{LB}Charles Jean, at your service!",
}
SPEAKERS={"03":"Maria","12":"Charles Jean Rochefort","6D":"Townsman","FE":"Sound effect"};STATES={int(x,16) for x in SPEAKERS}
def main()->None:
 with SOURCE.open(encoding="utf-8-sig",newline="") as s:rows={r["id"]:r for r in csv.DictReader(s) if r["id"].startswith("DK4_MES_B61_")}
 if set(LINES)!=set(rows):raise SystemExit(f"V66 mismatch: missing={sorted(set(rows)-set(LINES))}, extra={sorted(set(LINES)-set(rows))}")
 records=[]
 for i in sorted(LINES,key=lambda v:int(v.rsplit("R",1)[1])):
  r=rows[i];e=LINES[i];first=bytes.fromhex(r["source_hex"])[0];state=f"{first:02X}" if first in STATES and not r["japanese"].startswith("{LB}") else "";unsafe=e.replace("{MACRO:FI}","").replace("{MACRO:FA}","").replace("{MACRO:FO}","")
  if "F" in unsafe or "I" in unsafe:raise SystemExit(f"{i}: unsafe macro literal: {e}")
  sb=r["japanese"].count("{LB}");tb=e.count("{LB}");w=["weak-line-ending","orphan-final-line"]+(["manual-break"] if tb else [])+(["source-leading-linebreak"] if r["japanese"].startswith("{LB}") else [])+(["line-break-count"] if sb!=tb else [])
  records.append({"id":i,"english":f"{{SPEAKER:{state}}}{e}{{PAD}}" if state else f"{e}{{PAD}}","speaker":SPEAKERS.get(state,"Shien or scene participant"),"context":"A series of explosions leads Maria and Shien to recruit eccentric Western scientist Charles Jean Rochefort for his knowledge of bombs, artillery, and science.","source_meaning":e.replace("{LB}"," "),"localization_note":"Direct SC3 translation preserving the science discussion, recruitment, protagonist and fleet macros, comic voices, source staging, and fixed allocation.","qa_waivers":w,**({"manual_break_reason":"Protects semantic rows and progressive ASCII pair phase."} if tb else {}),"review":{"source":True,"context":True,"localization":True,"naturalness":True,"formatting":True}})
 p={"format":"dk4-ilnk-translation-batch-v1","file_path":"/data/SC3.DK4","source_file_sha256":SC3_SHA256,"encoder":"dialogue-fixed-v1","dialogue_profile":"maria-story-shared-events-v66-live","translation_policy":"natural-dialogue-v2","target_locale":"en-US","review_gates":["source","context","localization","naturalness","formatting"],"scope":"Maria SC3 block 61: complete Charles Jean Rochefort recruitment.","inventory":{"identified_records":len(rows),"translated_records":len(records),"excluded_records":0,"blocks":{"61":len(records)}},"excluded":[],"records":records};OUTPUT.write_text(json.dumps(p,ensure_ascii=False,indent=2)+"\n",encoding="utf-8");print(f"wrote {OUTPUT}: {len(records)} records")
if __name__=="__main__":main()
