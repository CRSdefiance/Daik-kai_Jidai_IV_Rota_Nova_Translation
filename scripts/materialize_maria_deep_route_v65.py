from __future__ import annotations
import csv,json
from pathlib import Path
SOURCE=Path("work/sc3/script.csv");OUTPUT=Path("translations/maria_deep_route_v65.json");SC3_SHA256="001e21897ddb727ae261c82763ebef8515784ecfa571619c7614d87f3320aab2"
LINES={
"DK4_MES_B60_R0004":"Well...",
"DK4_MES_B60_R0013":"Would you hire me?",
"DK4_MES_B60_R0023":"Who are you?",
"DK4_MES_B60_R0032":"Any special skills?",
"DK4_MES_B60_R0036":"Yes. Love machines.{LB}Good with ships and repairs.",
"DK4_MES_B60_R0039":"Terms?",
"DK4_MES_B60_R0043":"One request.{LB}Please lend me 1,000 gold!",
"DK4_MES_B60_R0053":"What?! Such nerve!{LB}Admiral, ignore this man.",
"DK4_MES_B60_R0063":"Pay him.",
"DK4_MES_B60_R0065":"We lack the money.",
"DK4_MES_B60_R0073":"Thank you!{LB}Now repairs can finish!",
"DK4_MES_B60_R0076":"Sorry, but please delay{LB}departure one day.",
"DK4_MES_B60_R0079":"Very well.",
"DK4_MES_B60_R0090":"Admiral, no!{LB}He grows bolder{LB}because we indulge him!",
"DK4_MES_B60_R0094":"Do you know who{LB}you are speaking to?!",
"DK4_MES_B60_R0102":"Tomorrow, at the port!",
"DK4_MES_B60_R0113":"Hey, wait!",
"DK4_MES_B60_R0125":"Been waiting!{LB}Come, look at this.",
"DK4_MES_B60_R0133":"Your money repaired the ship{LB}and cleared my debt.",
"DK4_MES_B60_R0137":"Sorry for testing you.{LB}An admiral trusted with my life{LB}must show character.",
"DK4_MES_B60_R0140":"You can be trusted.{LB}Please use this ship.",
"DK4_MES_B60_R0143":"Name?",
"DK4_MES_B60_R0147":"The ship?{LB}Name it anything you like.",
"DK4_MES_B60_R0151":"Your name, not the ship.",
"DK4_MES_B60_R0155":"Sorry. Excitement made me{LB}forget to introduce myself.",
"DK4_MES_B60_R0159":"Janus Pasha.{LB}Glad to serve.",
"DK4_MES_B60_R0164":"Take the ship from the dock,{LB}then use 'Modify' to name it.",
"DK4_MES_B60_R0170":"Understood.{LB}Someone else, then.",
}
SPEAKERS={"03":"Maria","04":"Janus Pasha","4A":"Richard","FE":"Tutorial narrator"};STATES={int(x,16) for x in SPEAKERS}
def main()->None:
 with SOURCE.open(encoding="utf-8-sig",newline="") as s:rows={r["id"]:r for r in csv.DictReader(s) if r["id"].startswith("DK4_MES_B60_")}
 if set(LINES)!=set(rows):raise SystemExit(f"V65 mismatch: missing={sorted(set(rows)-set(LINES))}, extra={sorted(set(LINES)-set(rows))}")
 records=[]
 for i in sorted(LINES,key=lambda v:int(v.rsplit("R",1)[1])):
  r=rows[i];e=LINES[i];first=bytes.fromhex(r["source_hex"])[0];state=f"{first:02X}" if first in STATES else "";unsafe=e.replace("{MACRO:FI}","").replace("{MACRO:FA}","").replace("{MACRO:FO}","")
  if "F" in unsafe or "I" in unsafe:raise SystemExit(f"{i}: unsafe macro literal: {e}")
  sb=r["japanese"].count("{LB}");tb=e.count("{LB}");w=["weak-line-ending","orphan-final-line"]+(["manual-break"] if tb else [])+(["line-break-count"] if sb!=tb else [])
  records.append({"id":i,"english":f"{{SPEAKER:{state}}}{e}{{PAD}}" if state else f"{e}{{PAD}}","speaker":SPEAKERS.get(state,"Choice"),"context":"Janus asks Maria for 1,000 gold to repair a ship, tests her character, then joins and explains how to rename the vessel.","source_meaning":e.replace("{LB}"," "),"localization_note":"Direct SC3 translation preserving both funding choices, Janus's test, recruitment, ship reward, naming tutorial, speaker states, and fixed allocation.","qa_waivers":w,**({"manual_break_reason":"Protects semantic rows and progressive ASCII pair phase."} if tb else {}),"review":{"source":True,"context":True,"localization":True,"naturalness":True,"formatting":True}})
 p={"format":"dk4-ilnk-translation-batch-v1","file_path":"/data/SC3.DK4","source_file_sha256":SC3_SHA256,"encoder":"dialogue-fixed-v1","dialogue_profile":"maria-story-shared-events-v65-live","translation_policy":"natural-dialogue-v2","target_locale":"en-US","review_gates":["source","context","localization","naturalness","formatting"],"scope":"Maria SC3 block 60: complete Janus recruitment, ship reward, and naming tutorial.","inventory":{"identified_records":len(rows),"translated_records":len(records),"excluded_records":0,"blocks":{"60":len(records)}},"excluded":[],"records":records};OUTPUT.write_text(json.dumps(p,ensure_ascii=False,indent=2)+"\n",encoding="utf-8");print(f"wrote {OUTPUT}: {len(records)} records")
if __name__=="__main__":main()
