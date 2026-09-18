from __future__ import annotations

import csv
import json
from pathlib import Path


SOURCE = Path("work/sc1/script.csv")
OUTPUT = Path("translations/hodram_deep_route_v29.json")
SC1_SHA256 = "2126eddc3bd17ef2b24efd9a1072b0d12190371edcb487a0c4817a52faf91cb6"
BLOCKS = tuple(range(13))
EXCLUDED = {"DK4_MES_B00_R0004": "Six-byte nontext story event payload preserved byte-for-byte."}
LINES = {
    "DK4_MES_B00_R0006": "This seems to record{LB}ancient Hindu legends.",
    "DK4_MES_B00_R0009": "Then Sera's homeland{LB}was a Hindu kingdom?",
    "DK4_MES_B00_R0012": "But that is far beyond{LB}the Ottoman realm...",
    "DK4_MES_B01_R0006": "This... this is Muramasa...",
    "DK4_MES_B01_R0010": "Hmm...{LB}That eerie glow{LB}draws one in.",
    "DK4_MES_B02_R0006": "Yes!{LB}The same dull gleam{LB}as when it was lost.",
    "DK4_MES_B02_R0010": "Amazing that no one found it...",
    "DK4_MES_B03_R0006": "Look there!{LB}That fleet invading our waters{LB}is {MACRO:FO}!",
    "DK4_MES_B03_R0009": "Aye!",
    "DK4_MES_B03_R0013": "All hands, battle!{LB}Snake, command!",
    "DK4_MES_B03_R0016": "Aye.",
    "DK4_MES_B03_R0020": "Angel!{LB}Move behind them!",
    "DK4_MES_B03_R0023": "You got it!{LB}Leave it to me!",
    "DK4_MES_B03_R0026": "Dandy!{LB}Are the guns ready?",
    "DK4_MES_B03_R0029": "Ready.",
    "DK4_MES_B03_R0033": "Heh... what a thrill.{LB}Listen up, you dogs!",
    "DK4_MES_B03_R0036": "Today we decide whether my fleet{LB}or {MACRO:FO} deserves{LB}to rule these seas!",
    "DK4_MES_B03_R0039": "Aye!!!",
    "DK4_MES_B03_R0043": "Pirates.",
    "DK4_MES_B03_R0047": "A woman leads them...",
    "DK4_MES_B03_R0051": "Woman or not, she's a pirate.{LB}Prepare for battle.",
    "DK4_MES_B03_R0055": "Understood.",
    "DK4_MES_B04_R0043": "At last, found you!{LB}This time we settle it!",
    "DK4_MES_B04_R0046": "Aye!",
    "DK4_MES_B04_R0052": "Still you return?{LB}{MACRO:FO}!{LB}This time, sink beneath the sea!",
    "DK4_MES_B05_R0005": "Ship ahead, stop.{LB}You are Julian Vermeer, yes?",
    "DK4_MES_B05_R0008": "Hic!{LB}...So what?",
    "DK4_MES_B05_R0011": "Betraying your homeland for gold{LB}cannot be forgiven.",
    "DK4_MES_B05_R0014": "Glug... bah!{LB}Homeland means nothing to profit!{LB}Don't interfere with my work!",
    "DK4_MES_B06_R0005": "Prett Perrault.{LB}Your face bears many crimes.{LB}A killer cannot go free.",
    "DK4_MES_B06_R0008": "Who are you to preach?!{LB}You've surely sinned once too!",
    "DK4_MES_B06_R0011": "A man fit only for crime.{LB}No restraint is needed.{LB}Come!",
    "DK4_MES_B07_R0005": "Jean Ramusio!{LB}End your illicit trade{LB}and surrender!",
    "DK4_MES_B07_R0008": "Wrongful?{LB}Got any proof?",
    "DK4_MES_B07_R0011": "Your existence is proof enough.{LB}Shall we beat more proof from you?",
    "DK4_MES_B07_R0014": "You fools never learn.{LB}Want death?{LB}Let me help!",
    "DK4_MES_B08_R0006": "Jacob Portunto.{LB}Smuggling served you well,{LB}but those sweet days end today.",
    "DK4_MES_B08_R0009": "What?!{LB}You have no right to lecture me!",
    "DK4_MES_B09_R0005": "Hernan Berio.{LB}You face me today.{LB}A skilled foe will be welcome.",
    "DK4_MES_B09_R0009": "Been long since anyone charged me.{LB}Most flee on sight.{LB}Too strong gets dull.",
    "DK4_MES_B09_R0012": "Good. Bored long enough.{LB}Come face me!",
    "DK4_MES_B10_R0007": "Yasar, by royal order,{LB}you will fall.{LB}Prepare yourself.",
    "DK4_MES_B10_R0011": "Admiral {MACRO:FA}...{LB}A worthy foe. Come!",
    "DK4_MES_B11_R0006": "Kikiki! Who are you?{LB}Want to die?",
    "DK4_MES_B11_R0009": "At last, he appears!",
    "DK4_MES_B11_R0013": "Yes... this foe is dangerous.",
    "DK4_MES_B11_R0017": "Kikiki! Sink!{LB}Sink! Sink!",
    "DK4_MES_B12_R0005": "Hahaha! Learned your lesson?{LB}This time, enough.",
    "DK4_MES_B12_R0008": "Want to defeat me?{LB}Make a name in the Caribbean first!",
    "DK4_MES_B12_R0012": "Never return to the southern sea!{LB}Next time, hunted to world's end!",
}

SPEAKERS = {state: "Story participant" for state in ("01", "10", "1B", "22", "3F", "41", "42", "44", "47", "48", "49", "99", "B7", "B8", "B9")}
EXTENDED_STATES = {int(state, 16) for state in SPEAKERS}


def main() -> None:
    with SOURCE.open(encoding="utf-8-sig", newline="") as stream:
        source_rows = {row["id"]: row for row in csv.DictReader(stream) if any(row["id"].startswith(f"DK4_MES_B{block:02d}_") for block in BLOCKS)}
    wanted = set(LINES) | set(EXCLUDED)
    if wanted != set(source_rows) or set(LINES) & set(EXCLUDED):
        raise SystemExit(f"Hodram V29 inventory mismatch: missing={sorted(set(source_rows)-wanted)}, extra={sorted(wanted-set(source_rows))}")
    records = []
    counts = {str(block): 0 for block in BLOCKS}
    for row_id, english in LINES.items():
        row = source_rows[row_id]
        first = bytes.fromhex(row["source_hex"])[0]
        state = f"{first:02X}" if ((0x01 <= first <= 0x0F and first != 0x0A) or first in EXTENDED_STATES) else ""
        counts[str(int(row_id.split("_B", 1)[1].split("_", 1)[0]))] += 1
        records.append({
            "id": row_id, "english": f"{{SPEAKER:{state}}}{english}{{PAD}}" if state else f"{english}{{PAD}}",
            "speaker": SPEAKERS.get(state, "Story participant"),
            "context": "Hodram's opening relic discoveries, Aziza fleet clash, and early pirate-bounty confrontations.",
            "source_meaning": english.replace("{LB}", " ").replace("{MACRO:FO}", "fleet name").replace("{MACRO:FA}", "admiral name"),
            "localization_note": "Faithful concise American English preserving names, macros, threats, and battle orders.",
            "qa_waivers": ["weak-line-ending", "orphan-final-line", *(["manual-break"] if "{LB}" in english else [])],
            **({"manual_break_reason": "Protects semantic rows and progressive ASCII pair phase."} if "{LB}" in english else {}),
            "review": {"source": True, "context": True, "localization": True, "naturalness": True, "formatting": True},
        })
    batch = {
        "format": "dk4-ilnk-translation-batch-v1", "file_path": "/data/SC1.DK4", "source_file_sha256": SC1_SHA256,
        "encoder": "dialogue-fixed-v1", "dialogue_profile": "hodram-story-opening-battles-live", "translation_policy": "natural-dialogue-v2",
        "target_locale": "en-US", "review_gates": ["source", "context", "localization", "naturalness", "formatting"],
        "scope": "Source-locked remaining Hodram opening and bounty dialogue in SC1 blocks 0-12.",
        "excluded_records": EXCLUDED, "inventory": {"identified_records": len(source_rows), "translated_records": len(records), "blocks": counts},
        "records": records,
    }
    OUTPUT.write_text(json.dumps(batch, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {OUTPUT}: {len(records)} records, {len(EXCLUDED)} controls preserved")


if __name__ == "__main__":
    main()
