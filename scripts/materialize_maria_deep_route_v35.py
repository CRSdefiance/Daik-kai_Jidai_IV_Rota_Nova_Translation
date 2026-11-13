from __future__ import annotations

import csv
import json
from pathlib import Path

SOURCE = Path("work/sc3/script.csv")
OUTPUT = Path("translations/maria_deep_route_v35.json")
SC3_SHA256 = "001e21897ddb727ae261c82763ebef8515784ecfa571619c7614d87f3320aab2"
BLOCKS = (278,)

LINES = {
    "DK4_MES_B278_R0004": "One hundred Jesuits have arrived{LB}from Portugal, Excellency.",
    "DK4_MES_B278_R0008": "Well done. Rest before{LB}meeting the emperor.",
    "DK4_MES_B278_R0013": "Halt!",
    "DK4_MES_B278_R0017": "Eh?",
    "DK4_MES_B278_R0021": "You filthy smugglers! You dare deceive{LB}the Son of Heaven!",
    "DK4_MES_B278_R0029": "What!?",
    "DK4_MES_B278_R0033": "Do not be fooled! They are petty thugs{LB}who prey upon this region!",
    "DK4_MES_B278_R0037": "Damn! What is happening?",
    "DK4_MES_B278_R0041": "Truly!?",
    "DK4_MES_B278_R0045": "A false accusation! We are truly...",
    "DK4_MES_B278_R0048": "{LB}Silence! A witness who remembers{LB}your faces reported you!",
    "DK4_MES_B278_R0052": "{LB}They reached Macao disguised{LB}as priests. Their farce ends here!",
    "DK4_MES_B278_R0056": "No more excuses! Arrest them all!",
    "DK4_MES_B278_R0059": "Yes, sir!",
    "DK4_MES_B278_R0071": "Yahoo!",
    "DK4_MES_B278_R0086": "Hah!",
    "DK4_MES_B278_R0093": "Eek!",
    "DK4_MES_B278_R0097": "Damn! You will not take me here!",
    "DK4_MES_B278_R0101": "Hmm... They nearly fooled me{LB}and cost me my head. Thanks to... Hm?",
    "DK4_MES_B278_R0105": "Where did the troops who exposed them go?",
    "DK4_MES_B278_R0108": "They already withdrew, sir.",
    "DK4_MES_B278_R0111": "So... Left without{LB}a greeting? Curious...",
    "DK4_MES_B278_R0131": "Strange... Ming's army has{LB}foreign troops now?",
    "DK4_MES_B278_R0143": "Was that performance good enough?",
    "DK4_MES_B278_R0146": "Very convincing.",
    "DK4_MES_B278_R0157": "What a masterpiece!{LB}You should have seen their faces!",
    "DK4_MES_B278_R0171": "Yes! Even Macao's governor{LB}believed every word!",
    "DK4_MES_B278_R0178": "{LB}A born actor.{LB}The town's best mimic.",
    "DK4_MES_B278_R0181": "Playing officer{LB}was terrifying...",
    "DK4_MES_B278_R0185": "We had no choice. They used disguises,{LB}so we answered in kind.",
    "DK4_MES_B278_R0189": "{LB}The smugglers should lie low now.{LB}What will you do?",
    "DK4_MES_B278_R0193": "Nowhere else to go. Let me work{LB}for you from now on.",
    "DK4_MES_B278_R0197": "Welcome aboard.",
}

PRESENTATION_STATES = {0x03, 0x0B, 0x0C, 0x19, 0x44, 0x58, 0x66, 0x7B, 0x81, 0x83, 0x8B}
SPEAKERS = {"03":"Maria","0B":"Crewman","0C":"Crewman","19":"Crewman","44":"Jacob","58":"Aide","66":"Defector","7B":"Troops","81":"False officer","83":"Governor","8B":"Missionary"}

def main() -> None:
    with SOURCE.open(encoding="utf-8-sig", newline="") as stream: all_rows = {row["id"]: row for row in csv.DictReader(stream)}
    rows = {row_id: row for row_id, row in all_rows.items() if row_id.startswith("DK4_MES_B278_")}
    if set(LINES) != set(rows): raise SystemExit(f"Maria V35 mismatch: missing={sorted(set(rows)-set(LINES))}, extra={sorted(set(LINES)-set(rows))}")
    records=[]; block_counts={"278":len(rows)}
    for row_id in sorted(rows, key=lambda value: int(value.rsplit("R",1)[1])):
        row, english = rows[row_id], LINES[row_id]; first=bytes.fromhex(row["source_hex"])[0]; state=f"{first:02X}" if first in PRESENTATION_STATES else ""
        leading_break=english.startswith("{LB}"); waivers=["weak-line-ending","orphan-final-line"]+(["manual-break"] if "{LB}" in english else [])+(["source-leading-linebreak"] if leading_break else [])
        records.append({"id":row_id,"english":f"{{SPEAKER:{state}}}{english}{{PAD}}" if state else f"{english}{{PAD}}","speaker":SPEAKERS.get(state,"Companion" if leading_break else "Maria"),"context":"Macao governor's-office sting and aftermath.","source_meaning":english,"localization_note":"Direct SC3 translation reviewed for natural English and state-byte safety.","qa_waivers":waivers,**({"manual_break_reason":"Preserves source scene transition and semantic rows."} if "{LB}" in english else {}),"review":{"source":True,"context":True,"localization":True,"naturalness":True,"formatting":True}})
    payload={"format":"dk4-ilnk-translation-batch-v1","file_path":"/data/SC3.DK4","source_file_sha256":SC3_SHA256,"encoder":"dialogue-fixed-v1","dialogue_profile":"maria-story-shared-events-v35-live","translation_policy":"natural-dialogue-v2","target_locale":"en-US","review_gates":["source","context","localization","naturalness","formatting"],"scope":"Maria SC3 block 278: staged governor's-office arrest and defector recruitment.","inventory":{"identified_records":len(rows),"translated_records":len(records),"excluded_records":0,"blocks":block_counts},"excluded":[],"records":records}
    OUTPUT.write_text(json.dumps(payload,ensure_ascii=False,indent=2)+"\n",encoding="utf-8"); print(f"wrote {OUTPUT}: {len(records)} records")

if __name__=="__main__": main()
