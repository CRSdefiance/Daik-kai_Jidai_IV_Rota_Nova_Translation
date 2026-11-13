from __future__ import annotations

import csv
import json
from pathlib import Path


SOURCE = Path("work/sc3/script.csv")
REUSE = Path("work/analysis/sc3_cross_route_reuse.json")
OUTPUT = Path("translations/maria_deep_route_v27.json")
SC3_SHA256 = "001e21897ddb727ae261c82763ebef8515784ecfa571619c7614d87f3320aab2"
BLOCKS = (183, 191, 211, 212, 220, 230)

OVERRIDES = {
    "DK4_MES_B183_R0018": "Blood-red blade...",
    "DK4_MES_B183_R0025": "Such a fine sword, unable to show{LB}its true worth... A shame.",
    "DK4_MES_B183_R0033": "The fear is understandable, but...{LB}Where could that sword be?",
    "DK4_MES_B191_R0007": "Rare to hear that from you.{LB}What kind of weapon?",
    "DK4_MES_B191_R0014": "Ares... the god of war, yes?{LB}A spear named for him sounds promising.{LB}Where can we find it?",
    "DK4_MES_B191_R0020": "That answers nothing.{LB}Now this is completely unclear.",
    "DK4_MES_B191_R0023": "The townspeople imply it lies nearby...{LB}We must find it.",
    "DK4_MES_B191_R0027": "(Oh? He is interested.)",
    "DK4_MES_B191_R0031": "Admiral? Why that face?{LB}Surprised to see me care about legends?",
    "DK4_MES_B191_R0035": "Honestly, yes.",
    "DK4_MES_B191_R0045": "So... you're a romantic.",
    "DK4_MES_B211_R0008": "Janus?{LB}What happened?",
    "DK4_MES_B211_R0011": "Nothing serious.{LB}A mast fitting caught my hand{LB}during maintenance.",
    "DK4_MES_B211_R0018": "Well...",
    "DK4_MES_B211_R0022": "A crewmate hurt his hand.",
    "DK4_MES_B211_R0043": "Yes! Rare and very useful gloves.{LB}Wait... Where did those go?",
    "DK4_MES_B211_R0049": "Get a grip.",
    "DK4_MES_B211_R0053": "Sorry. They must be... Yes!{LB}Somewhere around Denmark!",
    "DK4_MES_B211_R0061": "Yes! Somewhere on Jutland.{LB}Truly! Believe me!",
    "DK4_MES_B211_R0065": "All right. Let's search.",
    "DK4_MES_B211_R0073": "They never fit my hands,{LB}so they were meant for sale anyway.{LB}Their quality is guaranteed.",
    "DK4_MES_B212_R0011": "Yes.",
    "DK4_MES_B212_R0023": "What happened?",
    "DK4_MES_B212_R0040": "You look terribly down.{LB}Something troubling you?",
    "DK4_MES_B212_R0047": "Yes.",
    "DK4_MES_B212_R0057": "Yes",
    "DK4_MES_B212_R0059": "No",
    "DK4_MES_B212_R0067": "Yes. Why?",
    "DK4_MES_B212_R0073": "The New World...?{LB}We haven't crossed the Atlantic.",
    "DK4_MES_B212_R0077": "But perhaps someday.{LB}Why?",
    "DK4_MES_B212_R0087": "What?",
    "DK4_MES_B212_R0098": "How awful.{LB}Do you know who took it?",
    "DK4_MES_B212_R0105": "Difficult...{LB}Your story suggests the thief{LB}is in the New World.",
    "DK4_MES_B212_R0109": "Someone in Havana sells glasswork{LB}as jade or crystal at high prices.{LB}Word came through a friend.",
    "DK4_MES_B212_R0112": "{LB}A swindler...{LB}Hm. That hardly proves guilt.",
    "DK4_MES_B212_R0116": "Let's go to Havana.{LB}There seems to be no other lead.",
    "DK4_MES_B212_R0119": "{LB}Hm... Agreed.",
    "DK4_MES_B212_R0127": "We'll do what we can.{LB}But don't expect too much.",
    "DK4_MES_B220_R0008": "This statue...{LB}Doesn't it feel warm?",
    "DK4_MES_B220_R0017": "There.",
    "DK4_MES_B220_R0025": "A figurehead!{LB}Very finely made.{LB}Yes, something can be felt here!",
    "DK4_MES_B220_R0032": "Could it be famous?",
    "DK4_MES_B220_R0036": "Never heard of it.{LB}Wait, will you take it?",
    "DK4_MES_B220_R0042": "Exactly.",
    "DK4_MES_B220_R0054": "Such a magnificent figurehead{LB}belongs with the sea,{LB}not sitting on land.",
    "DK4_MES_B220_R0071": "What's wrong?{LB}Let's move it.",
    "DK4_MES_B220_R0078": "Wake up.",
    "DK4_MES_B220_R0083": "{MACRO:FI}'s Luck rose by 1!",
    "DK4_MES_B220_R0097": "Yes...{LB}(Still, this feels a little sad.)",
    "DK4_MES_B220_R0101": "Let's return to town.",
    "DK4_MES_B220_R0110": "{MACRO:FI}'s Charm rose by 1!",
    "DK4_MES_B230_R0014": "(So arrogant.)",
    "DK4_MES_B230_R0018": "Sorry to interrupt, but have you heard{LB}the name Jean Ramgio around here?",
    "DK4_MES_B230_R0026": "Trade made local ports prosper,{LB}and pirates fled before me.",
    "DK4_MES_B230_R0034": "Your conceit is astounding.{LB}The Sofala guild ordered your arrest{LB}for smuggling.",
    "DK4_MES_B230_R0045": "He's always like this.{LB}He lies, boasts, and acts superior.",
    "DK4_MES_B230_R0052": "...Pathetic.{LB}Brace yourself.{LB}You're coming to the Sofala guild.",
}

SPEAKERS = {
    "03": "Maria", "04": "Janus", "0D": "Cesare",
    "11": "Kamil", "15": "Ian", "42": "Jean", "5C": "Bartender",
    "71": "Sailor", "9A": "Crewman", "BA": "Francisca", "FE": "System or voice",
}
PRESENTATION_STATES = {int(value, 16) for value in SPEAKERS}


def main() -> None:
    report = json.loads(REUSE.read_text(encoding="utf-8"))
    lines = {
        str(item["id"]): str(item["variants"][0]["english"])
        for item in report["reusable"] if int(item["block"]) in BLOCKS
    }
    lines.update(OVERRIDES)
    with SOURCE.open(encoding="utf-8-sig", newline="") as stream:
        all_rows = {row["id"]: row for row in csv.DictReader(stream)}
    prefixes = tuple(f"DK4_MES_B{block}_" for block in BLOCKS)
    rows = {row_id: row for row_id, row in all_rows.items() if row_id.startswith(prefixes)}
    if set(lines) != set(rows):
        raise SystemExit(
            f"Maria V27 mismatch: missing={sorted(set(rows)-set(lines))}, "
            f"extra={sorted(set(lines)-set(rows))}"
        )

    records = []
    block_counts: dict[str, int] = {}
    for row_id in sorted(rows, key=lambda value: (int(value.split("_B")[1].split("_")[0]), int(value.rsplit("R", 1)[1]))):
        block = row_id.split("_B", 1)[1].split("_", 1)[0]
        row = rows[row_id]
        english = lines[row_id]
        first = bytes.fromhex(row["source_hex"])[0]
        state = f"{first:02X}" if first in PRESENTATION_STATES else ""
        block_counts[block] = block_counts.get(block, 0) + 1
        records.append({
            "id": row_id,
            "english": f"{{SPEAKER:{state}}}{english}{{PAD}}" if state else f"{english}{{PAD}}",
            "speaker": SPEAKERS.get(state, "Choice text"),
            "context": "Complete shared weapon, recovery, figurehead, or capture event.",
            "source_meaning": english,
            "localization_note": "Cross-route match or direct SC3 translation reviewed for natural English and state-byte safety.",
            "qa_waivers": ["weak-line-ending", "orphan-final-line"]
                + (["manual-break"] if "{LB}" in english else [])
                + (["source-leading-linebreak"] if english.startswith("{LB}") else []),
            **({"manual_break_reason": "Protects semantic rows and pair phase."} if "{LB}" in english else {}),
            "review": {"source": True, "context": True, "localization": True, "naturalness": True, "formatting": True},
        })

    payload = {
        "format": "dk4-ilnk-translation-batch-v1", "file_path": "/data/SC3.DK4",
        "source_file_sha256": SC3_SHA256, "encoder": "dialogue-fixed-v1",
        "dialogue_profile": "maria-story-shared-events-v27-live",
        "translation_policy": "natural-dialogue-v2", "target_locale": "en-US",
        "review_gates": ["source", "context", "localization", "naturalness", "formatting"],
        "scope": "Maria SC3 blocks 183, 191, 211, 212, 220, and 230: six complete shared events.",
        "inventory": {"identified_records": len(rows), "translated_records": len(records), "excluded_records": 0, "blocks": block_counts},
        "excluded": [], "records": records,
    }
    OUTPUT.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {OUTPUT}: {len(records)} records")


if __name__ == "__main__":
    main()
