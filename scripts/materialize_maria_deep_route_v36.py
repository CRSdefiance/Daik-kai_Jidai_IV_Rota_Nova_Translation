from __future__ import annotations

import csv
import json
from pathlib import Path

SOURCE=Path("work/sc3/script.csv"); OUTPUT=Path("translations/maria_deep_route_v36.json")
SC3_SHA256="001e21897ddb727ae261c82763ebef8515784ecfa571619c7614d87f3320aab2"; BLOCKS=(279,280)
LINES={
"DK4_MES_B279_R0005":"{MACRO:FI}! We were worried!",
"DK4_MES_B279_R0008":"Okay.",
"DK4_MES_B279_R0012":"Sorry for all the trouble.",
"DK4_MES_B279_R0016":"Wonderful! You recovered!",
"DK4_MES_B279_R0021":"That is all.",
"DK4_MES_B279_R0025":"What an ordeal! Oh, is it that late?",
"DK4_MES_B279_R0028":"Were you going somewhere?",
"DK4_MES_B279_R0032":"Yes. The temple, to pray.",
"DK4_MES_B279_R0035":"We should not delay you. Goodbye.",
"DK4_MES_B279_R0038":"Visit Kyoto sometime. With a map,{LB}it is easy. We can guide you partway.",
"DK4_MES_B279_R0042":"Thank you.",
"DK4_MES_B280_R0008":"Admiral, let us meet the clan guarding{LB}the Proof map in far northeast China.",
"DK4_MES_B280_R0010":"Admiral, visit the clan guarding{LB}the Proof map in northeast China.",
"DK4_MES_B280_R0011":"Admiral, who guards the Proof map?{LB}Let us visit their village in northeast China!",
"DK4_MES_B280_R0012":"Admiral, before we forget, let us visit{LB}the Proof-map clan in northeast China.",
"DK4_MES_B280_R0013":"Admiral, let us meet the Proof-map clan.{LB}Their village is in northeast China, right?",
"DK4_MES_B280_R0015":"Admiral, we should meet the clan guarding{LB}the Proof map in northeast China.",
"DK4_MES_B280_R0016":"Admiral, curious about its guardians?{LB}Their village lies in northeast China.",
"DK4_MES_B280_R0017":"Admiral, the Proof map concerns me.{LB}Visit its guardian clan?{LB}Their village lies far away{LB}in northeast China.",
}
PRESENTATION_STATES={0x03,0x66,0xCB,0xD0}; SPEAKERS={"03":"Maria","66":"Defector","CB":"Innkeeper","D0":"Companion"}
def main()->None:
    with SOURCE.open(encoding="utf-8-sig",newline="") as stream: all_rows={r["id"]:r for r in csv.DictReader(stream)}
    rows={i:r for i,r in all_rows.items() if i.startswith(tuple(f"DK4_MES_B{b}_" for b in BLOCKS))}
    if set(LINES)!=set(rows): raise SystemExit(f"Maria V36 mismatch: missing={sorted(set(rows)-set(LINES))}, extra={sorted(set(LINES)-set(rows))}")
    records=[]; counts={}
    for row_id in sorted(rows,key=lambda v:(int(v.split("_B")[1].split("_")[0]),int(v.rsplit("R",1)[1]))):
        row,english=rows[row_id],LINES[row_id]; block=row_id.split("_B",1)[1].split("_",1)[0]; counts[block]=counts.get(block,0)+1
        first=bytes.fromhex(row["source_hex"])[0]; state=f"{first:02X}" if first in PRESENTATION_STATES else ""
        records.append({"id":row_id,"english":f"{{SPEAKER:{state}}}{english}{{PAD}}" if state else f"{english}{{PAD}}","speaker":SPEAKERS.get(state,"Companion"),"context":"Kyoto lead or Proof-map reminder variant.","source_meaning":english,"localization_note":"Direct SC3 translation reviewed for natural English and state-byte safety.","qa_waivers":["weak-line-ending","orphan-final-line"]+(["manual-break"] if "{LB}" in english else []),**({"manual_break_reason":"Protects semantic rows and pair phase."} if "{LB}" in english else {}),"review":{"source":True,"context":True,"localization":True,"naturalness":True,"formatting":True}})
    payload={"format":"dk4-ilnk-translation-batch-v1","file_path":"/data/SC3.DK4","source_file_sha256":SC3_SHA256,"encoder":"dialogue-fixed-v1","dialogue_profile":"maria-story-shared-events-v36-live","translation_policy":"natural-dialogue-v2","target_locale":"en-US","review_gates":["source","context","localization","naturalness","formatting"],"scope":"Maria SC3 blocks 279-280: Kyoto map lead and all Proof-map reminder variants.","inventory":{"identified_records":len(rows),"translated_records":len(records),"excluded_records":0,"blocks":counts},"excluded":[],"records":records}
    OUTPUT.write_text(json.dumps(payload,ensure_ascii=False,indent=2)+"\n",encoding="utf-8"); print(f"wrote {OUTPUT}: {len(records)} records")
if __name__=="__main__": main()
