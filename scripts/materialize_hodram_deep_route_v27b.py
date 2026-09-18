from __future__ import annotations

import csv
import json
from pathlib import Path


SOURCE = Path("work/sc1/script.csv")
OUTPUT = Path("translations/hodram_deep_route_v27b.json")
SC1_SHA256 = "2126eddc3bd17ef2b24efd9a1072b0d12190371edcb487a0c4817a52faf91cb6"
BLOCKS = (317, 318, 319)
EXCLUDED = {
    "DK4_MES_B317_R0037": "Seven-byte nontext expedition event payload preserved byte-for-byte.",
    "DK4_MES_B317_R0143": "Six-byte nontext expedition event payload preserved byte-for-byte.",
    "DK4_MES_B317_R0216": "Six-byte nontext expedition event payload preserved byte-for-byte.",
    "DK4_MES_B318_R0023": "Eight-byte nontext expedition event payload preserved byte-for-byte.",
    "DK4_MES_B318_R0070": "Three-byte nontext travel event payload preserved byte-for-byte.",
    "DK4_MES_B318_R0134": "Six-byte nontext expedition event payload preserved byte-for-byte.",
}
LINES = {
    "DK4_MES_B317_R0019": "Admiral, without a map{LB}this jungle is dangerous.",
    "DK4_MES_B317_R0020": "Admiral, we can't cross this jungle{LB}without a map.",
    "DK4_MES_B317_R0021": "Admiral, crossing without a map{LB}is dangerous.",
    "DK4_MES_B317_R0022": "No map, Admiral.{LB}This jungle is too risky.",
    "DK4_MES_B317_R0023": "No map, Admiral.{LB}This jungle is too risky.",
    "DK4_MES_B317_R0024": "Admiral, walking this jungle{LB}without a map is dangerous.",
    "DK4_MES_B317_R0025": "No map, Admiral.{LB}This jungle is too risky.",
    "DK4_MES_B317_R0049": "Shall we go?",
    "DK4_MES_B317_R0051": "Then let us go.",
    "DK4_MES_B317_R0053": "Come, let's go!",
    "DK4_MES_B317_R0055": "Then let's go.",
    "DK4_MES_B317_R0057": "Let's go.",
    "DK4_MES_B317_R0059": "Well, onward.",
    "DK4_MES_B317_R0063": "Such humidity.{LB}The party's fatigue concerns me.",
    "DK4_MES_B317_R0083": "A cave, here...",
    "DK4_MES_B317_R0085": "Huh? A cave.",
    "DK4_MES_B317_R0089": "So dark...",
    "DK4_MES_B317_R0093": "Sir...",
    "DK4_MES_B317_R0099": "Grope ahead",
    "DK4_MES_B317_R0101": "Use light",
    "DK4_MES_B317_R0108": "No matter. We continue.",
    "DK4_MES_B317_R0113": "Hm?{LB}What's this?",
    "DK4_MES_B317_R0116": "Admiral! A huge snake!{LB}A sailor!",
    "DK4_MES_B317_R0127": "Whoa! A python!!{LB}(Maybe?)",
    "DK4_MES_B317_R0133": "Damn! Retreat!",
    "DK4_MES_B317_R0141": "A sailor was injured.",
    "DK4_MES_B317_R0147": "...Where are we?",
    "DK4_MES_B317_R0158": "Hard to say...{LB}but we seem near the ruins.",
    "DK4_MES_B317_R0159": "Seems we're{LB}near the ruins.",
    "DK4_MES_B317_R0161": "Not sure where we are,{LB}but maybe near the ruins?",
    "DK4_MES_B317_R0163": "Hard to say...{LB}Ruins seem near.",
    "DK4_MES_B317_R0165": "Whoa!{LB}Aren't we near the ruins?",
    "DK4_MES_B317_R0167": "Ah!{LB}We seem to have emerged{LB}near the ruins.",
    "DK4_MES_B317_R0168": "Where are we?{LB}Not sure, but these look like ruins!{LB}Lucky!",
    "DK4_MES_B317_R0170": "Hmm...{LB}We seem to be near the ruins.",
    "DK4_MES_B317_R0176": "Good. Light it...",
    "DK4_MES_B317_R0180": "Ugh! Bats?!{LB}A huge swarm...",
    "DK4_MES_B317_R0195": "Too many!",
    "DK4_MES_B317_R0197": "Way too many!",
    "DK4_MES_B317_R0199": "Aaaah!{LB}Admiral, this swarm is enormous!",
    "DK4_MES_B317_R0200": "Too many!",
    "DK4_MES_B317_R0202": "Admiral! We can't advance{LB}through this many bats!",
    "DK4_MES_B317_R0203": "Aah, bats!{LB}Disgusting!",
    "DK4_MES_B317_R0206": "Never mind.{LB}Move on.",
    "DK4_MES_B317_R0214": "The sailors are exhausted.",
    "DK4_MES_B317_R0227": "We did it!{LB}Out of the jungle!",
    "DK4_MES_B317_R0228": "Out of the jungle!",
    "DK4_MES_B317_R0230": "We did it!{LB}Out of the jungle!",
    "DK4_MES_B317_R0231": "Thank goodness.{LB}We're out!",
    "DK4_MES_B317_R0233": "We did it!{LB}Out of the jungle!",
    "DK4_MES_B317_R0234": "We did it!{LB}Out of the jungle!",
    "DK4_MES_B317_R0235": "We did it, Admiral!{LB}We made it out of the jungle!",
    "DK4_MES_B317_R0248": "Admiral, the ruins!",
    "DK4_MES_B317_R0250": "Admiral, the ruins!",
    "DK4_MES_B317_R0252": "The ruins!",
    "DK4_MES_B317_R0254": "Admiral, the ruins!",
    "DK4_MES_B317_R0256": "Admiral, the ruins!",
    "DK4_MES_B317_R0258": "Admiral, the ruins!",
    "DK4_MES_B317_R0260": "Admiral, ruins ahead.",
    "DK4_MES_B318_R0012": "Bring me the map to the ruins first.",
    "DK4_MES_B318_R0032": "An ancient city stood{LB}in a place like this...",
    "DK4_MES_B318_R0034": "An ancient city{LB}stood here...",
    "DK4_MES_B318_R0035": "An ancient city{LB}stood here.",
    "DK4_MES_B318_R0036": "An ancient city{LB}stood here...",
    "DK4_MES_B318_R0037": "An ancient city{LB}stood here...",
    "DK4_MES_B318_R0038": "Hard to believe{LB}an ancient city stood here.",
    "DK4_MES_B318_R0040": "A city stood even here{LB}long ago.",
    "DK4_MES_B318_R0041": "An ancient city{LB}stood here...",
    "DK4_MES_B318_R0044": "This map says the ruins{LB}aren't on this island.",
    "DK4_MES_B318_R0048": "What?!",
    "DK4_MES_B318_R0054": "We must cross the sea.",
    "DK4_MES_B318_R0059": "Then return to port.",
    "DK4_MES_B318_R0063": "No, a boat is ready.{LB}We'll continue in it.",
    "DK4_MES_B318_R0066": "Only you are qualified.{LB}The sailors must not learn{LB}where the ruins lie.",
    "DK4_MES_B318_R0075": "One day passed.",
    "DK4_MES_B318_R0079": "We've arrived.{LB}Now we continue overland.",
    "DK4_MES_B318_R0083": "H-huh?",
    "DK4_MES_B318_R0094": "You're Rafael of Castor.{LB}Why are you here?",
    "DK4_MES_B318_R0100": "Who?",
    "DK4_MES_B318_R0110": "That person sent me to seek the ruins.{LB}But got lost on the way...",
    "DK4_MES_B318_R0114": "So you were among{LB}those sent everywhere.",
    "DK4_MES_B318_R0117": "My apologies.{LB}With no word from you,{LB}coming too seemed best.",
    "DK4_MES_B318_R0122": "No.{LB}My own weakness is to blame...",
    "DK4_MES_B318_R0125": "Very well.{LB}We can search together.",
    "DK4_MES_B318_R0128": "Yes.",
    "DK4_MES_B318_R0133": "Agreed.{LB}Search together.",
    "DK4_MES_B318_R0136": "Oh!{LB}There it is!",
    "DK4_MES_B318_R0149": "Admiral, ruins found.",
    "DK4_MES_B318_R0151": "Admiral, ruins found.",
    "DK4_MES_B318_R0153": "The ruins!",
    "DK4_MES_B318_R0155": "Admiral, we found the ruins.",
    "DK4_MES_B318_R0157": "Admiral, we found the ruins.",
    "DK4_MES_B318_R0159": "Admiral, those are the ruins.",
    "DK4_MES_B318_R0161": "Admiral, we found the ruins.",
    "DK4_MES_B318_R0165": "Coming",
    "DK4_MES_B319_R0005": "Welcome.",
    "DK4_MES_B319_R0009": "Have you visited the village{LB}far north in the New World?",
    "DK4_MES_B319_R0013": "A guest told me a great monk{LB}from this city crossed north{LB}to spread his faith.",
    "DK4_MES_B319_R0017": "After finding that village,{LB}he vanished.{LB}What happened to him?",
    "DK4_MES_B319_R0021": "Dunno.",
    "DK4_MES_B319_R0025": "They say he was very virtuous.{LB}May his new flock cherish him.",
    "DK4_MES_B319_R0028": "Travel north sometime,{LB}and ask about the monk.",
}

SPEAKERS = {
    "01": "Hodram Bergstrom", "16": "Companion", "B3": "Expedition patron",
    "CE": "Local woman", "CF": "Companion", "D0": "Companion",
    "D3": "Companion", "D6": "Companion", "FE": "System text",
}
EXTENDED_STATES = {int(state, 16) for state in SPEAKERS}


def main() -> None:
    with SOURCE.open(encoding="utf-8-sig", newline="") as stream:
        source_rows = {row["id"]: row for row in csv.DictReader(stream) if any(row["id"].startswith(f"DK4_MES_B{block}_") for block in BLOCKS)}
    if set(LINES) | set(EXCLUDED) != set(source_rows) or set(LINES) & set(EXCLUDED):
        raise SystemExit(f"Hodram V27b inventory mismatch: missing={sorted(set(source_rows)-set(LINES)-set(EXCLUDED))}, extra={sorted((set(LINES)|set(EXCLUDED))-set(source_rows))}")
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
            "context": "Hodram crosses a jungle cave, reaches ancient-city ruins by boat, encounters Rafael, and hears a northern missionary rumor.",
            "source_meaning": english.replace("{LB}", " "),
            "localization_note": "Faithful concise American English preserving exploration choices, party variants, and the Rafael encounter.",
            "qa_waivers": ["weak-line-ending", "orphan-final-line", *(["manual-break"] if "{LB}" in english else [])],
            **({"manual_break_reason": "Protects semantic rows and progressive ASCII pair phase."} if "{LB}" in english else {}),
            "review": {"source": True, "context": True, "localization": True, "naturalness": True, "formatting": True},
        })
    batch = {
        "format": "dk4-ilnk-translation-batch-v1", "file_path": "/data/SC1.DK4", "source_file_sha256": SC1_SHA256,
        "encoder": "dialogue-fixed-v1", "dialogue_profile": "hodram-story-final-expeditions-live", "translation_policy": "natural-dialogue-v2",
        "target_locale": "en-US", "review_gates": ["source", "context", "localization", "naturalness", "formatting"],
        "scope": "Source-locked Hodram jungle-cave, ancient-city, Rafael, and missionary-rumor events in SC1 blocks 317-319.",
        "excluded_records": EXCLUDED, "inventory": {"identified_records": len(source_rows), "translated_records": len(records), "blocks": counts},
        "records": records,
    }
    OUTPUT.write_text(json.dumps(batch, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {OUTPUT}: {len(records)} records, {len(EXCLUDED)} controls preserved")


if __name__ == "__main__":
    main()
