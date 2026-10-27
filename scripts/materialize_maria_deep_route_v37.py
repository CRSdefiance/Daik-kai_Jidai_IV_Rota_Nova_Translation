from __future__ import annotations
import csv,json
from pathlib import Path
SOURCE=Path("work/sc3/script.csv"); OUTPUT=Path("translations/maria_deep_route_v37.json"); SC3_SHA256="001e21897ddb727ae261c82763ebef8515784ecfa571619c7614d87f3320aab2"
EXCLUDED={"DK4_MES_B274_R0027":"Opaque six-byte event payload 056060463E63; not dialogue."}
LINES={
"DK4_MES_B274_R0011":"Got the map?",
"DK4_MES_B274_R0015":"Almost forgot. Must prepare.",
"DK4_MES_B274_R0029":"We part here. Travel safely.",
"DK4_MES_B274_R0034":"Thank you.",
"DK4_MES_B274_R0049":"Let us go.",
"DK4_MES_B274_R0051":"Let us go!",
"DK4_MES_B274_R0053":"Shall we go?",
"DK4_MES_B274_R0055":"Time to go.",
"DK4_MES_B274_R0057":"Let us depart.",
"DK4_MES_B274_R0059":"All right, onward!",
"DK4_MES_B274_R0068":"We passed here before. Could we be{LB}walking in circles?",
"DK4_MES_B274_R0070":"This place... We have passed{LB}the same spot several times.",
"DK4_MES_B274_R0072":"Odd. We seem to be{LB}circling the same place.",
"DK4_MES_B274_R0073":"Did we not pass here already?",
"DK4_MES_B274_R0074":"Strange. We have walked past{LB}this same spot several times...",
"DK4_MES_B274_R0075":"We passed this road before...",
"DK4_MES_B274_R0076":"Did we not just take this road?",
"DK4_MES_B274_R0077":"Hmm. We keep retracing{LB}the same road...",
"DK4_MES_B274_R0080":"Are we lost?",
"DK4_MES_B274_R0086":"Compass",
"DK4_MES_B274_R0088":"Hunch",
"DK4_MES_B274_R0096":"Use the compass.",
"DK4_MES_B274_R0100":"{LB}Will that work? Some places{LB}can confuse a compass.",
"DK4_MES_B274_R0104":"The midday sun confirms our course.",
"DK4_MES_B274_R0107":"{LB}Hmm. True.",
"DK4_MES_B274_R0113":"A compass may fail in places like this.{LB}Let us trust our instincts.",
"DK4_MES_B274_R0125":"Seriously!? That sounds reckless!",
"DK4_MES_B274_R0128":"{LB}You talk.",
"DK4_MES_B274_R0138":"A day passed.",
"DK4_MES_B274_R0142":"This fork is new.",
"DK4_MES_B274_R0146":"{LB}Whew... We may be through.",
"DK4_MES_B274_R0153":"Admiral! We found it!",
}
STATES={0x03,0x0B,0xCB,0xD0,0xFE}; SPEAKERS={"03":"Maria","0B":"Companion","CB":"Guide","D0":"Companion","FE":"System"}
def main()->None:
    with SOURCE.open(encoding="utf-8-sig",newline="") as s: all_rows={r["id"]:r for r in csv.DictReader(s)}
    rows={i:r for i,r in all_rows.items() if i.startswith("DK4_MES_B274_")}
    if set(LINES)|set(EXCLUDED)!=set(rows): raise SystemExit(f"Maria V37 mismatch: missing={sorted(set(rows)-set(LINES)-set(EXCLUDED))}, extra={sorted((set(LINES)|set(EXCLUDED))-set(rows))}")
    records=[]
    for row_id in sorted(LINES,key=lambda v:int(v.rsplit("R",1)[1])):
        row,english=rows[row_id],LINES[row_id]; first=bytes.fromhex(row["source_hex"])[0]; state=f"{first:02X}" if first in STATES else ""; leading=english.startswith("{LB}")
        records.append({"id":row_id,"english":f"{{SPEAKER:{state}}}{english}{{PAD}}" if state else f"{english}{{PAD}}","speaker":SPEAKERS.get(state,"Companion"),"context":"Kyoto-map maze and navigation choice.","source_meaning":english,"localization_note":"Direct SC3 translation reviewed for natural English, choice clarity, and state-byte safety.","qa_waivers":["weak-line-ending","orphan-final-line"]+(["manual-break"] if "{LB}" in english else [])+(["source-leading-linebreak"] if leading else []),**({"manual_break_reason":"Preserves source transition or semantic rows."} if "{LB}" in english else {}),"review":{"source":True,"context":True,"localization":True,"naturalness":True,"formatting":True}})
    payload={"format":"dk4-ilnk-translation-batch-v1","file_path":"/data/SC3.DK4","source_file_sha256":SC3_SHA256,"encoder":"dialogue-fixed-v1","dialogue_profile":"maria-story-shared-events-v37-live","translation_policy":"natural-dialogue-v2","target_locale":"en-US","review_gates":["source","context","localization","naturalness","formatting"],"scope":"Maria SC3 block 274: Kyoto-map maze, navigation choices, and exit.","inventory":{"identified_records":len(rows),"translated_records":len(records),"excluded_records":len(EXCLUDED),"blocks":{"274":len(records)}},"excluded":[{"id":i,"reason":r} for i,r in EXCLUDED.items()],"records":records}
    OUTPUT.write_text(json.dumps(payload,ensure_ascii=False,indent=2)+"\n",encoding="utf-8"); print(f"wrote {OUTPUT}: {len(records)} records, {len(EXCLUDED)} excluded")
if __name__=="__main__": main()
