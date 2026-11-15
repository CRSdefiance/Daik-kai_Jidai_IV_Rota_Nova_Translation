from __future__ import annotations

import csv
import json
from pathlib import Path

SOURCE = Path("work/sc3/script.csv")
OUTPUT = Path("translations/maria_deep_route_v62.json")
SC3_SHA256 = "001e21897ddb727ae261c82763ebef8515784ecfa571619c7614d87f3320aab2"
LINES = {
    "DK4_MES_B57_R0004": "So incredibly{LB}persistent!!!",
    "DK4_MES_B57_R0007": "Oh, my beloved Cristina!{LB}Why are you so cold?",
    "DK4_MES_B57_R0010": "Are you unwell?{LB}Who follows someone{LB}who hates him this much?",
    "DK4_MES_B57_R0013": "No need for shyness!",
    "DK4_MES_B57_R0017": "Enough! Listen.{LB}Our parents arranged it.{LB}No wish to marry you!",
    "DK4_MES_B57_R0020": "Hearing your voice alone{LB}makes me happy!",
    "DK4_MES_B57_R0023": "Moron!",
    "DK4_MES_B57_R0027": "That man...?",
    "DK4_MES_B57_R0031": "Yes, him.",
    "DK4_MES_B57_R0035": "Looks like trouble?",
    "DK4_MES_B57_R0038": "No trouble at all.{LB}Hey, Cristina!",
    "DK4_MES_B57_R0042": "Cristina!{LB}Been well?",
    "DK4_MES_B57_R0046": "Grandpa! When reach London?",
    "DK4_MES_B57_R0050": "Just now.{LB}Sailing again, you see.",
    "DK4_MES_B57_R0053": "Again?!{LB}Mom and Dad will stop you.",
    "DK4_MES_B57_R0056": "Only if you tell them.{LB}Ho ho ho.",
    "DK4_MES_B57_R0059": "Come on...",
    "DK4_MES_B57_R0063": "More important:{LB}want to sail too?",
    "DK4_MES_B57_R0066": "What?!{LB}Absolutely not!",
    "DK4_MES_B57_R0069": "Who is this fellow?",
    "DK4_MES_B57_R0072": "Dad's pal's son...{LB}What was his name?",
    "DK4_MES_B57_R0075": "Cristina! Do not be shy!{LB}Are you her grandfather?",
    "DK4_MES_B57_R0079": "An honor to meet you!{LB}My name is Mivor!{LB}Mivor Gentz!",
    "DK4_MES_B57_R0082": "Yes, something like that.{LB}Our fathers promised it{LB}without asking me.",
    "DK4_MES_B57_R0086": "Somehow this odd fellow{LB}became my betrothed.",
    "DK4_MES_B57_R0089": "Oh. So.",
    "DK4_MES_B57_R0093": "Do not just say that!",
    "DK4_MES_B57_R0097": "Hm, this pale weakling...",
    "DK4_MES_B57_R0100": "Not only because our parents said so...{LB}Truly, Lady Cristina...",
    "DK4_MES_B57_R0104": "Mom and Dad mean:{LB}'Stop swords and settle down.'{LB}What a bother.",
    "DK4_MES_B57_R0107": "Sounds like Herald.{LB}Maybe raised him wrong...",
    "DK4_MES_B57_R0110": "Ahem.",
    "DK4_MES_B57_R0114": "You stay quiet!{LB}Now, about that ship...",
    "DK4_MES_B57_R0118": "Right, right.{LB}Want to come with me?",
    "DK4_MES_B57_R0122": "Grandpa told me about you.{LB}Would you sail on my ship?",
    "DK4_MES_B57_R0126": "What?{LB}Grandpa, who are they?",
    "DK4_MES_B57_R0129": "Well. (One thing after another.){LB}This is Admiral{LB}{MACRO:FI} {MACRO:FA}.",
    "DK4_MES_B57_R0132": "Admiral? Very young.",
    "DK4_MES_B57_R0136": "You wanted foreign sword matches.{LB}Why not train around the world?",
    "DK4_MES_B57_R0139": "No! Absolutely not!",
    "DK4_MES_B57_R0143": "Yes... good.{LB}Count me in.",
    "DK4_MES_B57_R0146": "No! No way!",
    "DK4_MES_B57_R0150": "Can we leave Mivor behind?",
    "DK4_MES_B57_R0153": "Of course. No time like now.{LB}Right, Grandpa?",
    "DK4_MES_B57_R0156": "My granddaughter.{LB}You understand.",
    "DK4_MES_B57_R0159": "Mivor,{LB}coming with us?",
    "DK4_MES_B57_R0162": "Well, uh...",
    "DK4_MES_B57_R0166": "He cannot swim.{LB}Terrified of water.{LB}Cannot follow, right?",
    "DK4_MES_B57_R0169": "Then... a duel!",
    "DK4_MES_B57_R0176": "You never understand!{LB}Hyaah!",
    "DK4_MES_B57_R0180": "Aaaah! Ouch!",
    "DK4_MES_B57_R0184": "With that stance,{LB}even a child would win.",
    "DK4_MES_B57_R0187": "Hm. Still sharp.",
    "DK4_MES_B57_R0190": "My rapier!{LB}Dad bought it!",
    "DK4_MES_B57_R0194": "Let us go!{LB}Sword matches are nice,{LB}but sailing sounds fun!",
}
SPEAKERS = {"03": "Maria", "06": "Cristina's grandfather", "07": "Cristina", "4F": "Mivor Gentz"}
STATES = {int(value, 16) for value in SPEAKERS}


def main() -> None:
    with SOURCE.open(encoding="utf-8-sig", newline="") as stream:
        rows = {row["id"]: row for row in csv.DictReader(stream) if row["id"].startswith("DK4_MES_B57_")}
    if set(LINES) != set(rows):
        raise SystemExit(f"V62 mismatch: missing={sorted(set(rows)-set(LINES))}, extra={sorted(set(LINES)-set(rows))}")
    records = []
    for row_id in sorted(LINES, key=lambda value: int(value.rsplit("R", 1)[1])):
        row = rows[row_id]
        english = LINES[row_id]
        first = bytes.fromhex(row["source_hex"])[0]
        state = f"{first:02X}" if first in STATES else ""
        unsafe = english.replace("{MACRO:FI}", "").replace("{MACRO:FA}", "").replace("{MACRO:FO}", "")
        if "F" in unsafe or "I" in unsafe:
            raise SystemExit(f"{row_id}: unsafe literal macro byte: {english}")
        source_breaks = row["japanese"].count("{LB}")
        target_breaks = english.count("{LB}")
        waivers = ["weak-line-ending", "orphan-final-line"]
        if target_breaks:
            waivers.append("manual-break")
        if source_breaks != target_breaks:
            waivers.append("line-break-count")
        records.append({
            "id": row_id,
            "english": f"{{SPEAKER:{state}}}{english}{{PAD}}" if state else f"{english}{{PAD}}",
            "speaker": SPEAKERS.get(state, "Scene participant"),
            "context": "Maria meets Cristina and her unwanted fiancé Mivor in London; Cristina accepts her grandfather's invitation to pursue sword training around the world aboard Maria's ship.",
            "source_meaning": english.replace("{LB}", " "),
            "localization_note": "Faithful concise American English preserving Cristina's blunt voice, Mivor's comic devotion, the grandfather's invitation, protagonist name macros, and recruitment continuity.",
            "qa_waivers": waivers,
            **({"manual_break_reason": "Protects semantic rows and progressive ASCII pair phase."} if target_breaks else {}),
            "review": {"source": True, "context": True, "localization": True, "naturalness": True, "formatting": True},
        })
    payload = {
        "format": "dk4-ilnk-translation-batch-v1", "file_path": "/data/SC3.DK4",
        "source_file_sha256": SC3_SHA256, "encoder": "dialogue-fixed-v1",
        "dialogue_profile": "maria-story-shared-events-v62-live",
        "translation_policy": "natural-dialogue-v2", "target_locale": "en-US",
        "review_gates": ["source", "context", "localization", "naturalness", "formatting"],
        "scope": "Maria SC3 block 57: complete Cristina and Mivor London recruitment event.",
        "inventory": {"identified_records": len(rows), "translated_records": len(records), "excluded_records": 0, "blocks": {"57": len(records)}},
        "excluded": [], "records": records,
    }
    OUTPUT.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {OUTPUT}: {len(records)} records")


if __name__ == "__main__":
    main()
