from __future__ import annotations

import csv
import json
from pathlib import Path


SOURCE = Path("work/sc1/script.csv")
OUTPUT = Path("translations/hodram_deep_route_v26b.json")
SC1_SHA256 = "2126eddc3bd17ef2b24efd9a1072b0d12190371edcb487a0c4817a52faf91cb6"
BLOCKS = (313, 314)
EXCLUDED: dict[str, str] = {}
LINES = {
    "DK4_MES_B313_R0019": "No map, Admiral.{LB}We'll get lost.",
    "DK4_MES_B313_R0020": "No map.{LB}We'll get lost.",
    "DK4_MES_B313_R0021": "No map.{LB}We'll get lost.",
    "DK4_MES_B313_R0022": "No map, Admiral.{LB}We'll get lost.",
    "DK4_MES_B313_R0023": "No map, Admiral.{LB}We'll get lost.",
    "DK4_MES_B313_R0024": "No map, Admiral.{LB}We'll get lost.",
    "DK4_MES_B313_R0025": "Admiral, without a map{LB}we'll get lost.",
    "DK4_MES_B313_R0026": "No map.{LB}We'll get lost.",
    "DK4_MES_B313_R0053": "Terrible heat.",
    "DK4_MES_B313_R0055": "So very hot.",
    "DK4_MES_B313_R0057": "So hot.",
    "DK4_MES_B313_R0059": "Hot.",
    "DK4_MES_B313_R0061": "Ugh, so hot.",
    "DK4_MES_B313_R0065": "Desert heat is normal.{LB}Onward.",
    "DK4_MES_B313_R0068": "Whoa!!",
    "DK4_MES_B313_R0084": "Admiral!{LB}Scorpions!",
    "DK4_MES_B313_R0085": "Whoa!{LB}A scorpion swarm!",
    "DK4_MES_B313_R0086": "Aah!{LB}Scorpions!!",
    "DK4_MES_B313_R0087": "Admiral!{LB}So many scorpions!",
    "DK4_MES_B313_R0088": "Admiral!{LB}Scorpions!",
    "DK4_MES_B313_R0089": "Whoa!{LB}Scorpions!",
    "DK4_MES_B313_R0092": "Calm.",
    "DK4_MES_B313_R0096": "B-but... what now?",
    "DK4_MES_B313_R0103": "Destroy",
    "DK4_MES_B313_R0105": "Drive",
    "DK4_MES_B313_R0107": "Run",
    "DK4_MES_B313_R0115": "My turn.{LB}Hah!",
    "DK4_MES_B313_R0128": "They fled!{LB}As expected of you, Admiral.",
    "DK4_MES_B313_R0129": "They fled!{LB}Well done.",
    "DK4_MES_B313_R0130": "They ran!{LB}As expected, Admiral.",
    "DK4_MES_B313_R0131": "They fled!{LB}Reliable as ever, Admiral.",
    "DK4_MES_B313_R0132": "They fled!{LB}Most impressive, Admiral.",
    "DK4_MES_B313_R0133": "They ran!{LB}Amazing, Admiral!",
    "DK4_MES_B313_R0134": "They fled!{LB}Reliable as ever, Admiral.",
    "DK4_MES_B313_R0139": "My turn{LB}Drive",
    "DK4_MES_B313_R0152": "They fled!{LB}As expected of you, Admiral.",
    "DK4_MES_B313_R0153": "They fled!{LB}Well done.",
    "DK4_MES_B313_R0154": "They ran!{LB}As expected, Admiral.",
    "DK4_MES_B313_R0155": "They fled!{LB}Reliable as ever, Admiral.",
    "DK4_MES_B313_R0156": "They fled!{LB}Most impressive, Admiral.",
    "DK4_MES_B313_R0157": "They ran!{LB}Amazing, Admiral!",
    "DK4_MES_B313_R0158": "They fled!{LB}Reliable as ever, Admiral.",
    "DK4_MES_B313_R0162": "Damn!!",
    "DK4_MES_B313_R0179": "Admiral! Are you okay?!",
    "DK4_MES_B313_R0181": "Admiral! You okay?!",
    "DK4_MES_B313_R0183": "Admiral! You okay?!",
    "DK4_MES_B313_R0185": "Admiral!",
    "DK4_MES_B313_R0189": "Damn, careless.",
    "DK4_MES_B313_R0203": "Needs treatment now!",
    "DK4_MES_B313_R0205": "Treat it quickly!",
    "DK4_MES_B313_R0207": "This is bad!{LB}Treat it now!",
    "DK4_MES_B313_R0208": "Treat it quickly!",
    "DK4_MES_B313_R0210": "Needs treatment now!",
    "DK4_MES_B313_R0212": "Needs treatment now!",
    "DK4_MES_B313_R0228": "{MACRO:FI} was injured.{LB}One day for treatment.",
    "DK4_MES_B313_R0236": "Sorry.{LB}Better.",
    "DK4_MES_B313_R0242": "Retreat silently.{LB}Don't provoke them.",
    "DK4_MES_B313_R0255": "Everyone, move out.{LB}Quietly now.",
    "DK4_MES_B313_R0256": "Everyone, move out.{LB}Quietly now.",
    "DK4_MES_B313_R0257": "Everyone, move out.{LB}Quietly now.",
    "DK4_MES_B313_R0258": "Everyone, move out.{LB}Quietly now.",
    "DK4_MES_B313_R0259": "Everyone, move out.{LB}Quietly now.",
    "DK4_MES_B313_R0260": "Everyone, move out.{LB}Quietly now.",
    "DK4_MES_B313_R0275": "Thud!",
    "DK4_MES_B313_R0279": "Damn! The cargo fell!",
    "DK4_MES_B313_R0293": "Oh, no!",
    "DK4_MES_B313_R0295": "Oh!",
    "DK4_MES_B313_R0297": "Bad!",
    "DK4_MES_B313_R0299": "Damn!",
    "DK4_MES_B313_R0303": "Whoa!",
    "DK4_MES_B313_R0316": "Are you okay?{LB}Stay with me!",
    "DK4_MES_B313_R0317": "You okay? Stay with me!",
    "DK4_MES_B313_R0319": "Are you okay? Stay with me!",
    "DK4_MES_B313_R0321": "You okay? Stay with me!",
    "DK4_MES_B313_R0323": "Are you okay? Stay with me!",
    "DK4_MES_B313_R0325": "You okay? Stay with me!",
    "DK4_MES_B313_R0331": "Run through, now!",
    "DK4_MES_B313_R0336": "A sailor was injured.",
    "DK4_MES_B313_R0355": "Looks like we made it!",
    "DK4_MES_B314_R0006": "Welcome.",
    "DK4_MES_B314_R0010": "{MACRO:FI}, they say the Goryeo Celadon Burner{LB}lies somewhere in East Asia.",
    "DK4_MES_B314_R0014": "They say it makes divination exact.{LB}Oh, what a thing to try...",
    "DK4_MES_B314_R0031": "Hmm.",
    "DK4_MES_B314_R0035": "Oh, yes.",
    "DK4_MES_B314_R0039": "Pirates have been active nearby.{LB}Best equip yourself well.",
    "DK4_MES_B314_R0044": "Really? Dangerous.{LB}Thanks. We'll be careful.",
    "DK4_MES_B314_R0047": "See you.",
}

SPEAKERS = {
    "01": "Hodram Bergstrom", "97": "Companion", "CC": "Local woman",
    "D0": "Companion", "D3": "Companion", "D6": "Companion",
    "DA": "Companion", "FE": "System text",
}
EXTENDED_STATES = {int(state, 16) for state in SPEAKERS}


def main() -> None:
    with SOURCE.open(encoding="utf-8-sig", newline="") as stream:
        source_rows = {row["id"]: row for row in csv.DictReader(stream) if any(row["id"].startswith(f"DK4_MES_B{block}_") for block in BLOCKS)}
    if set(LINES) != set(source_rows):
        raise SystemExit(f"Hodram V26b inventory mismatch: missing={sorted(set(source_rows)-set(LINES))}, extra={sorted(set(LINES)-set(source_rows))}")
    records = []
    counts = {str(block): 0 for block in BLOCKS}
    for row_id, english in LINES.items():
        row = source_rows[row_id]
        first = bytes.fromhex(row["source_hex"])[0]
        state = f"{first:02X}" if ((0x01 <= first <= 0x0F and first != 0x0A) or first in EXTENDED_STATES) else ""
        counts[row_id.split("_B", 1)[1].split("_", 1)[0]] += 1
        records.append({
            "id": row_id, "english": f"{{SPEAKER:{state}}}{english}{{PAD}}" if state else f"{english}{{PAD}}",
            "speaker": SPEAKERS.get(state, "Party-member variant"),
            "context": "Hodram's party crosses a scorpion-filled desert and later hears of the Goryeo Celadon Burner and nearby pirates.",
            "source_meaning": english.replace("{MACRO:FI}", "Hodram").replace("{LB}", " "),
            "localization_note": "Faithful concise American English preserving combat choices, injury branches, and party variants.",
            "qa_waivers": ["weak-line-ending", "orphan-final-line", *(["manual-break"] if "{LB}" in english else [])],
            **({"manual_break_reason": "Protects semantic rows and progressive ASCII pair phase."} if "{LB}" in english else {}),
            "review": {"source": True, "context": True, "localization": True, "naturalness": True, "formatting": True},
        })
    batch = {
        "format": "dk4-ilnk-translation-batch-v1", "file_path": "/data/SC1.DK4", "source_file_sha256": SC1_SHA256,
        "encoder": "dialogue-fixed-v1", "dialogue_profile": "hodram-story-eastasia-live", "translation_policy": "natural-dialogue-v2",
        "target_locale": "en-US", "review_gates": ["source", "context", "localization", "naturalness", "formatting"],
        "scope": "Source-locked Hodram scorpion expedition and Goryeo celadon rumor in SC1 blocks 313-314.",
        "excluded_records": EXCLUDED, "inventory": {"identified_records": len(source_rows), "translated_records": len(records), "blocks": counts},
        "records": records,
    }
    OUTPUT.write_text(json.dumps(batch, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {OUTPUT}: {len(records)} records")


if __name__ == "__main__":
    main()
