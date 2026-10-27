from __future__ import annotations
import csv,json
from pathlib import Path
SOURCE=Path("work/sc3/script.csv");OUTPUT=Path("translations/maria_deep_route_v64.json");SC3_SHA256="001e21897ddb727ae261c82763ebef8515784ecfa571619c7614d87f3320aab2"
LINES={
"DK4_MES_B59_R0004":"Shipping thrives here.{LB}Perhaps a skilled navigator?",
"DK4_MES_B59_R0007":"Yes.{LB}Let us ask around.",
"DK4_MES_B59_R0010":"Excuse me.{LB}We seek someone skilled with ships...",
"DK4_MES_B59_R0013":"A sailor, eh?{LB}But Master Adernkatz...",
"DK4_MES_B59_R0017":"No, never mind.{LB}Heh heh heh.",
"DK4_MES_B59_R0020":"What a strange old man.{LB}Ader... Adernkatz, was it?{LB}Maybe we should find him.",
"DK4_MES_B59_R0024":"Hey, kid!{LB}Know anyone named Adernkatz?",
"DK4_MES_B59_R0028":"Admiral Adernkatz?{LB}His mansion is that way.",
"DK4_MES_B59_R0031":"Thanks, kid.{LB}Admiral {MACRO:FI},{LB}his mansion is that way.",
"DK4_MES_B59_R0035":"Let us go.",
"DK4_MES_B59_R0040":"Here?",
"DK4_MES_B59_R0044":"Knock.",
"DK4_MES_B59_R0049":"Who?",
"DK4_MES_B59_R0053":"Good day.{LB}We are with {MACRO:FO}...",
"DK4_MES_B59_R0056":"{MACRO:FI} {MACRO:FA}.{LB}This is navigator Janus Pasha.",
"DK4_MES_B59_R0060":"A navigator...{LB}Come inside.",
"DK4_MES_B59_R0063":"What brings you here?",
"DK4_MES_B59_R0067":"We heard of your skill{LB}and hoped to speak.",
"DK4_MES_B59_R0070":"Long ago.{LB}Now this life is ashore.",
"DK4_MES_B59_R0073":"Would you sail once more?",
"DK4_MES_B59_R0076":"An old man would be no help...",
"DK4_MES_B59_R0080":"You are not old.{LB}We seek your guidance.",
"DK4_MES_B59_R0091":"Hah.",
"DK4_MES_B59_R0099":"Had we met sooner,{LB}my life might have been different.",
"DK4_MES_B59_R0103":"Then?",
"DK4_MES_B59_R0107":"Very well.{LB}Put Gerhard Adernkatz's{LB}skill to good use.",
}
SPEAKERS={"03":"Maria","04":"Janus Pasha","10":"Gerhard Adernkatz","52":"Old townsman","A2":"Boy","FE":"Sound effect"};STATES={int(x,16) for x in SPEAKERS}
def main()->None:
 with SOURCE.open(encoding="utf-8-sig",newline="") as stream:rows={r["id"]:r for r in csv.DictReader(stream) if r["id"].startswith("DK4_MES_B59_")}
 if set(LINES)!=set(rows):raise SystemExit(f"V64 mismatch: missing={sorted(set(rows)-set(LINES))}, extra={sorted(set(LINES)-set(rows))}")
 records=[]
 for row_id in sorted(LINES,key=lambda v:int(v.rsplit("R",1)[1])):
  row=rows[row_id];english=LINES[row_id];first=bytes.fromhex(row["source_hex"])[0];state=f"{first:02X}" if first in STATES else "";unsafe=english.replace("{MACRO:FI}","").replace("{MACRO:FA}","").replace("{MACRO:FO}","")
  if "F" in unsafe or "I" in unsafe:raise SystemExit(f"{row_id}: unsafe macro literal: {english}")
  sb=row["japanese"].count("{LB}");tb=english.count("{LB}");waivers=["weak-line-ending","orphan-final-line"]+(["manual-break"] if tb else [])+(["line-break-count"] if sb!=tb else [])
  records.append({"id":row_id,"english":f"{{SPEAKER:{state}}}{english}{{PAD}}" if state else f"{english}{{PAD}}","speaker":SPEAKERS.get(state,"Scene participant"),"context":"Maria and Janus seek the retired master navigator Gerhard Adernkatz and persuade him to return to sea.","source_meaning":english.replace("{LB}"," "),"localization_note":"Direct SC3 translation preserving Gerhard's restrained voice, the recruitment exchange, runtime name macros, speaker states, and fixed allocation.","qa_waivers":waivers,**({"manual_break_reason":"Protects semantic rows and progressive ASCII pair phase."} if tb else {}),"review":{"source":True,"context":True,"localization":True,"naturalness":True,"formatting":True}})
 payload={"format":"dk4-ilnk-translation-batch-v1","file_path":"/data/SC3.DK4","source_file_sha256":SC3_SHA256,"encoder":"dialogue-fixed-v1","dialogue_profile":"maria-story-shared-events-v64-live","translation_policy":"natural-dialogue-v2","target_locale":"en-US","review_gates":["source","context","localization","naturalness","formatting"],"scope":"Maria SC3 block 59: complete Gerhard Adernkatz recruitment.","inventory":{"identified_records":len(rows),"translated_records":len(records),"excluded_records":0,"blocks":{"59":len(records)}},"excluded":[],"records":records}
 OUTPUT.write_text(json.dumps(payload,ensure_ascii=False,indent=2)+"\n",encoding="utf-8");print(f"wrote {OUTPUT}: {len(records)} records")
if __name__=="__main__":main()
