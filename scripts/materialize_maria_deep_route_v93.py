from __future__ import annotations
import csv,json
from pathlib import Path
S=Path("work/sc3/script.csv");O=Path("translations/maria_deep_route_v93.json");SHA="001e21897ddb727ae261c82763ebef8515784ecfa571619c7614d87f3320aab2"
L={
"DK4_MES_B113_R0004":"Hardly any customers.",
"DK4_MES_B113_R0016":"Really...",
"DK4_MES_B113_R0023":"{LB}Very few.{LB}One man in back...",
"DK4_MES_B113_R0026":"Ho ho! The feast is over?{LB}Bring me more!",
"DK4_MES_B113_R0034":"{LB}Could he be monopolizing it?",
"DK4_MES_B113_R0037":"Heard that. This is no monopoly.{LB}Everything here was paid for.",
"DK4_MES_B113_R0040":"Enough was paid to eat, drink,{LB}and revel as much as desired!",
"DK4_MES_B113_R0044":"Vulgar...",
"DK4_MES_B113_R0048":"{LB}Rich or not,{LB}such behavior only debases him.",
"DK4_MES_B113_R0052":"Ho ho! This world belongs{LB}to those with money.",
"DK4_MES_B113_R0055":"Seeing value only in money...{LB}What a miserable life.",
"DK4_MES_B113_R0058":"Nonsense! How can one so rich{LB}be miserable? Money is everything!",
"DK4_MES_B113_R0062":"{LB}Words are wasted on him...",
"DK4_MES_B113_R0074":"Nothing gets through.",
"DK4_MES_B113_R0081":"A new face, perhaps?{LB}Shall the Nagalpur Company{LB}show you its power?",
"DK4_MES_B113_R0085":"So you are Nagalpur.{LB}The greedy company said to do anything{LB}for money.",
"DK4_MES_B113_R0089":"And you are {MACRO:FO}.{LB}You insulted me, so surely{LB}you possess the nerve and wealth.",
"DK4_MES_B113_R0092":"The value of money{LB}will soon be clear to you.{LB}Ho ho ho!",
"DK4_MES_B113_R0097":"A troublesome foe...",
"DK4_MES_B114_R0005":"Oh, {MACRO:FI}! Well?{LB}Everyone talks about you.",
"DK4_MES_B114_R0008":"Heh...{LB}More awful rumors?",
"DK4_MES_B114_R0011":"No! You are my hero.",
"DK4_MES_B114_R0014":"?",
"DK4_MES_B114_R0018":"You sail dangerous seas{LB}and stand equal to any man.{LB}Every woman here admires you.",
"DK4_MES_B114_R0021":"A-admires?",
"DK4_MES_B114_R0025":"Yes, our shining hope!{LB}Here, take this.{LB}Let me help you.",
"DK4_MES_B114_R0028":"Th-thanks.{LB}Gladly accepted.",
"DK4_MES_B114_R0031":"(Such warmth from a townsman...{LB}That has been rare.)",
"DK4_MES_B115_R0004":"The Everlasting Lotus Leaf{LB}and Kushan Platter{LB}relate to the Proof map.",
"DK4_MES_B115_R0007":"{LB}Leaf and plate...{LB}A hard pairing.",
"DK4_MES_B115_R0018":"Could Taoist magic solve it?{LB}Hah!",
"DK4_MES_B115_R0021":"{LB}Effort wasted.",
"DK4_MES_B115_R0028":"The leaf looks completely dry.{LB}Can it truly be unwithered?",
"DK4_MES_B115_R0032":"{LB}!!{LB}Try soaking it in water.",
"DK4_MES_B115_R0035":"So the platter holds water.{LB}Then the leaf floats atop it...",
"DK4_MES_B115_R0039":"{LB}The leaf drinks water!",
"DK4_MES_B115_R0043":"The veins formed a map!{LB}The great southern ocean's Proof map!",
"DK4_MES_B115_R0047":"{LB}Now only the Proof remains.",
}
EX={"DK4_MES_B115_R0041":"Raw four-byte event-control payload between the soaking animation and map reveal; not dialogue."}
SP={"03":"Maria","19":"Companion","1A":"Companion","26":"Nagalpur","C6":"Admirer"};ST={int(x,16) for x in SP}
C={113:"Maria meets Nagalpur and his money-centered worldview, beginning their rivalry.",114:"A female admirer praises Maria as an inspiration and gives her a gift.",115:"Maria's party combines the Everlasting Lotus Leaf and Kushan Platter to reveal the Indian Ocean Proof map."}
def main()->None:
 with S.open(encoding="utf-8-sig",newline="") as f:rows={r["id"]:r for r in csv.DictReader(f) if 113<=int(r["id"].split("_B",1)[1].split("_R",1)[0])<=115}
 if set(L)|set(EX)!=set(rows):raise SystemExit(f"V93 mismatch: missing={sorted(set(rows)-set(L)-set(EX))}; extra={sorted((set(L)|set(EX))-set(rows))}")
 rec=[]
 for i in sorted(L,key=lambda v:(int(v.split("_B",1)[1].split("_R",1)[0]),int(v.rsplit("R",1)[1]))):
  r=rows[i];e=L[i];first=bytes.fromhex(r["source_hex"])[0];state=f"{first:02X}" if first in ST else "";u=e.replace("{MACRO:FI}","").replace("{MACRO:FA}","").replace("{MACRO:FO}","")
  if "F" in u or "I" in u:raise SystemExit(f"{i}: unsafe macro literal: {e}")
  sb=r["japanese"].count("{LB}");tb=e.count("{LB}");w=["weak-line-ending","orphan-final-line"]+(["manual-break"] if tb else [])+(["source-leading-linebreak"] if r["japanese"].startswith("{LB}") else [])+(["line-break-count"] if sb!=tb else []);prefix=f"{{SPEAKER:{state}}}" if state else "";b=int(i.split("_B",1)[1].split("_R",1)[0])
  rec.append({"id":i,"english":f"{prefix}{e}{{PAD}}","speaker":SP.get(state,"Maria or Xien continuation"),"context":C[b],"source_meaning":e.replace("{LB}"," "),"localization_note":"Direct SC3 translation preserving speaker states, route macros, item names, rivalry and introspective tone, the verified raw control, and fixed allocation.","qa_waivers":w,**({"manual_break_reason":"Protects semantic rows and progressive ASCII pair phase."} if tb else {}),"review":{"source":True,"context":True,"localization":True,"naturalness":True,"formatting":True}})
 p={"format":"dk4-ilnk-translation-batch-v1","file_path":"/data/SC3.DK4","source_file_sha256":SHA,"encoder":"dialogue-fixed-v1","dialogue_profile":"maria-story-shared-events-v93-live","translation_policy":"natural-dialogue-v2","target_locale":"en-US","review_gates":["source","context","localization","naturalness","formatting"],"scope":"Maria SC3 blocks 113-115: Nagalpur encounter, female admirer gift, and Indian Ocean Proof-map item combination.","excluded_records":EX,"inventory":{"identified_records":len(rows),"translated_records":len(rec),"excluded_records":len(EX),"blocks":{"113":19,"114":9,"115":11}},"records":rec};O.write_text(json.dumps(p,ensure_ascii=False,indent=2)+"\n",encoding="utf-8");print(f"wrote {O}: {len(rec)} translations + {len(EX)} control")
if __name__=="__main__":main()
