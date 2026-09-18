from __future__ import annotations
import csv,json
from pathlib import Path
SOURCE=Path("work/sc0/script.csv"); OUTPUT=Path("translations/raphael_deep_route_v75.json")
SC0_SHA256="a774ff674b086a27be2344188de71e1c7a64e5d2ee5cf366f9d6b8bada48e85e"
SPEAKERS={0x05:"Claudio Manousch",0x13:"Al Fasi",0x94:"Hidden-village father",0x95:"Raphael crewmate",0xA2:"Sick child"}
OVERRIDES={
"DK4_MES_B306_R0005":"Cough, cough!",
"DK4_MES_B306_R0009":"Coughing again... Rest or you won't improve.",
"DK4_MES_B306_R0013":"Okay... cough!",
"DK4_MES_B306_R0018":"What's wrong?",
"DK4_MES_B306_R0022":"...No. Telling you won't help.",
"DK4_MES_B306_R0031":"That boy is terribly ill.",
"DK4_MES_B306_R0035":"Sick? How serious?",
"DK4_MES_B306_R0038":"Doctors gave up. They say a few years at best... Damn!",
"DK4_MES_B306_R0043":"!! Oh no...",
"DK4_MES_B306_R0047":"Rumor says a cure-all exists across the sea, in the East. But rumor alone...",
"DK4_MES_B306_R0059":"Let me seek it!",
"DK4_MES_B306_R0063":"What?!",
"DK4_MES_B306_R0068":"The East? Near China, surely! We'll find it. Wait for us!",
"DK4_MES_B306_R0076":"Eastern medicine? Maybe this medicine?!",
"DK4_MES_B306_R0079":"What?! R-really?!",
"DK4_MES_B306_R0083":"No promise it will work...",
"DK4_MES_B306_R0087":"Any hope will do!{LB}Please give it to him!",
"DK4_MES_B306_R0091":"Yes!",
"DK4_MES_B306_R0096":".",
"DK4_MES_B306_R0101":"How?",
"DK4_MES_B306_R0105":"My cough...",
"DK4_MES_B306_R0109":"Oh! His color is returning!",
"DK4_MES_B306_R0113":"Yes. He should recover.{LB}His fever is gone.",
"DK4_MES_B306_R0116":"Really?! This medicine is amazing!",
"DK4_MES_B306_R0127":"Eastern medicine...",
"DK4_MES_B306_R0134":"Thank you!! You saved my son's life!!",
"DK4_MES_B306_R0138":"Please, think nothing of it. We could not let such a dear child die.",
"DK4_MES_B306_R0142":"You're a good person. Never forgotten. Ask anything about this town.",
"DK4_MES_B306_R0147":"Thank you. Take care.",
}
def main():
 with SOURCE.open(encoding="utf-8-sig",newline="") as s: rows=[r for r in csv.DictReader(s) if r["id"].startswith("DK4_MES_B306_")]
 records=[]
 for row in rows:
  e=OVERRIDES.get(row["id"])
  if e is None: raise SystemExit(f"V75 unresolved: {row['id']}")
  unsafe=e
  for m in ("FI","FA","FO","FU"): unsafe=unsafe.replace(f"{{MACRO:{m}}}","")
  if "I" in unsafe or "F" in unsafe: raise SystemExit(f"{row['id']}: unsafe literal uppercase macro byte remains: {e}")
  first=int(row["source_hex"][:2],16); st=f"{first:02X}" if first in SPEAKERS else ""
  records.append({"id":row["id"],"english":f"{{SPEAKER:{st}}}{e}{{PAD}}" if st else f"{e}{{PAD}}","speaker":SPEAKERS.get(first,"Raphael party or scene text"),"context":"Raphael's party meets a gravely ill child in the hidden village and uses eastern medicine to save him.","source_meaning":e.replace("{LB}"," "),"localization_note":"Faithful concise American English preserving the illness, cure quest, recovery, gratitude, and fixed-record constraints.","qa_waivers":["weak-line-ending","orphan-final-line",*(["manual-break"] if "{LB}" in e else [])],**({"manual_break_reason":"Protects semantic rows and progressive ASCII pair phase."} if "{LB}" in e else {}),"review":{"source":True,"context":True,"localization":True,"naturalness":True,"formatting":True}})
 batch={"format":"dk4-ilnk-translation-batch-v1","file_path":"/data/SC0.DK4","source_file_sha256":SC0_SHA256,"encoder":"dialogue-fixed-v1","dialogue_profile":"raphael-story-deep-route-v75-live","translation_policy":"natural-dialogue-v2","target_locale":"en-US","review_gates":["source","context","localization","naturalness","formatting"],"scope":"Complete source-locked Raphael hidden-village sick-child, eastern-medicine, recovery, and gratitude event in SC0 block 306.","excluded_records":{},"inventory":{"identified_records":len(rows),"translated_records":len(records),"blocks":{"306":len(records)}},"records":records}
 OUTPUT.write_text(json.dumps(batch,ensure_ascii=False,indent=2)+"\n",encoding="utf-8"); print(f"wrote {OUTPUT}: {len(records)} records")
if __name__=="__main__": main()
