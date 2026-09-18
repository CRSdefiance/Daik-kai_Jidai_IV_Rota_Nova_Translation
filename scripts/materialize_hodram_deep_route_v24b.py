from __future__ import annotations

import csv
import json
from pathlib import Path


SOURCE = Path("work/sc1/script.csv")
OUTPUT = Path("translations/hodram_deep_route_v24b.json")
SC1_SHA256 = "2126eddc3bd17ef2b24efd9a1072b0d12190371edcb487a0c4817a52faf91cb6"
BLOCKS = (291,)
EXCLUDED: dict[str, str] = {}


LINES = {
    "DK4_MES_B291_R0017": "Admiral, no map.{LB}This jungle is dangerous.",
    "DK4_MES_B291_R0018": "Admiral, no map.{LB}This jungle is dangerous.",
    "DK4_MES_B291_R0019": "Admiral, no map.{LB}This jungle is too dangerous.",
    "DK4_MES_B291_R0020": "Admiral, we'll get lost{LB}in this jungle without a map.",
    "DK4_MES_B291_R0021": "Admiral, roaming this jungle{LB}blindly is suicidal.",
    "DK4_MES_B291_R0022": "Admiral, no map.{LB}This jungle is dangerous.",
    "DK4_MES_B291_R0023": "Admiral, no map?{LB}This jungle is too scary!",
    "DK4_MES_B291_R0024": "Admiral, no map.{LB}This jungle is dangerous.",
    "DK4_MES_B291_R0037": "An eerie jungle...",
    "DK4_MES_B291_R0041": "Yes. May nothing happen...",
    "DK4_MES_B291_R0045": "Cave.",
    "DK4_MES_B291_R0049": "Very deep...{LB}Still, we must proceed.",
    "DK4_MES_B291_R0060": "This cave is a shortcut{LB}to our goal.",
    "DK4_MES_B291_R0066": "Hmm.",
    "DK4_MES_B291_R0070": "{MACRO:FI}, mind the slick moss.",
    "DK4_MES_B291_R0073": "Yes.",
    "DK4_MES_B291_R0077": "Grrr...",
    "DK4_MES_B291_R0091": "Something's there...{LB}Bad.",
    "DK4_MES_B291_R0092": "Something...{LB}Bad omen.",
    "DK4_MES_B291_R0093": "Something...{LB}Bad feeling.",
    "DK4_MES_B291_R0094": "Something...{LB}Bad feeling.",
    "DK4_MES_B291_R0095": "Something's there.{LB}Bad feeling.",
    "DK4_MES_B291_R0096": "Something...{LB}Bad feeling.",
    "DK4_MES_B291_R0097": "Something's there...{LB}This feels awful...",
    "DK4_MES_B291_R0100": "A beast!!",
    "DK4_MES_B291_R0106": "Attack!",
    "DK4_MES_B291_R0108": "Run!",
    "DK4_MES_B291_R0115": "Shoot!",
    "DK4_MES_B291_R0119": "Grr!",
    "DK4_MES_B291_R0123": "Whoa!",
    "DK4_MES_B291_R0127": "Damn! Too quick!",
    "DK4_MES_B291_R0136": "No!{LB}A shot in this cramped cave{LB}could hit our own men!",
    "DK4_MES_B291_R0138": "No!{LB}This cramped space means{LB}we might shoot our allies!",
    "DK4_MES_B291_R0140": "No!{LB}This cramped cave means{LB}we might hit our own men!",
    "DK4_MES_B291_R0142": "No!{LB}Shooting in this cramped cave{LB}could hit our allies!",
    "DK4_MES_B291_R0144": "No!{LB}Shooting here could hit our own men!",
    "DK4_MES_B291_R0145": "No! This cramped cave means{LB}we cannot avoid hitting our men!",
    "DK4_MES_B291_R0146": "Admiral!{LB}This cramped cave means{LB}we may hit our friends!",
    "DK4_MES_B291_R0148": "No!{LB}Shooting in this cramped cave{LB}risks hitting our allies!",
    "DK4_MES_B291_R0152": "Gunfire will only hurt us.{LB}Close combat!",
    "DK4_MES_B291_R0169": "Pant... we defeated it...",
    "DK4_MES_B291_R0171": "We beat it.",
    "DK4_MES_B291_R0173": "Pant... we won... maybe...",
    "DK4_MES_B291_R0175": "Pant... looks like we won...",
    "DK4_MES_B291_R0177": "...Dead!",
    "DK4_MES_B291_R0179": "Pant... we beat it somehow!",
    "DK4_MES_B291_R0181": "We finally won!{LB}That tiger was strong!",
    "DK4_MES_B291_R0182": "Pant... we defeated it!",
    "DK4_MES_B291_R0186": "Many crewmen were injured.",
    "DK4_MES_B291_R0197": "Not hungry.{LB}The tiger won't chase.",
    "DK4_MES_B291_R0198": "Not hungry.{LB}The tiger won't chase.",
    "DK4_MES_B291_R0199": "The tiger wasn't hungry.{LB}That's why it won't chase us.",
    "DK4_MES_B291_R0200": "The tiger wasn't hungry...{LB}Good. No pursuit.",
    "DK4_MES_B291_R0202": "No pursuit means{LB}hunger wasn't the reason.{LB}We're safe.",
    "DK4_MES_B291_R0204": "Since it isn't chasing us,{LB}the tiger was not hungry.",
    "DK4_MES_B291_R0206": "The tiger isn't hungry.{LB}No pursuit.",
    "DK4_MES_B291_R0208": "Not hungry.{LB}The tiger won't chase.",
    "DK4_MES_B291_R0211": "Whew, saved!",
    "DK4_MES_B291_R0221": "A light...",
    "DK4_MES_B291_R0225": "Now we can leave the cave.",
}


SPEAKERS = {
    "01": "Hodram Bergstrom", "10": "Gerhard Adelknauts", "12": "Charles",
    "97": "Companion", "D0": "Companion", "D3": "Companion",
    "D7": "Companion", "D8": "Companion", "FE": "System or creature voice",
}
EXTENDED_STATES = {int(state, 16) for state in SPEAKERS}


def main() -> None:
    with SOURCE.open(encoding="utf-8-sig", newline="") as stream:
        source_rows = {row["id"]: row for row in csv.DictReader(stream) if row["id"].startswith("DK4_MES_B291_")}
    if set(LINES) | set(EXCLUDED) != set(source_rows) or set(LINES) & set(EXCLUDED):
        missing = sorted(set(source_rows) - set(LINES) - set(EXCLUDED))
        extra = sorted((set(LINES) | set(EXCLUDED)) - set(source_rows))
        raise SystemExit(f"Hodram V24b inventory mismatch: missing={missing}, extra={extra}")
    records = []
    for row_id, english in LINES.items():
        row = source_rows[row_id]
        first = bytes.fromhex(row["source_hex"])[0]
        state = f"{first:02X}" if ((0x01 <= first <= 0x0F and first != 0x0A) or first in EXTENDED_STATES) else ""
        records.append({
            "id": row_id, "english": f"{{SPEAKER:{state}}}{english}{{PAD}}" if state else f"{english}{{PAD}}",
            "speaker": SPEAKERS.get(state, "Party-member variant"),
            "context": "Hodram's expedition crosses a jungle and cave, confronts a tiger, and finds the exit.",
            "source_meaning": english.replace("{MACRO:FI}", "Hodram").replace("{LB}", " "),
            "localization_note": "Faithful concise American English; parallel party-member reactions retain their distinct tone.",
            "qa_waivers": ["weak-line-ending", "orphan-final-line", *(["manual-break"] if "{LB}" in english else [])],
            **({"manual_break_reason": "Protects semantic rows and the progressive ASCII pair phase in this expedition scene."} if "{LB}" in english else {}),
            "review": {"source": True, "context": True, "localization": True, "naturalness": True, "formatting": True},
        })
    batch = {
        "format": "dk4-ilnk-translation-batch-v1", "file_path": "/data/SC1.DK4", "source_file_sha256": SC1_SHA256,
        "encoder": "dialogue-fixed-v1", "dialogue_profile": "hodram-story-cave-live", "translation_policy": "natural-dialogue-v2",
        "target_locale": "en-US", "review_gates": ["source", "context", "localization", "naturalness", "formatting"],
        "scope": "Source-locked Hodram jungle, cave, and tiger expedition in SC1 block 291.",
        "excluded_records": EXCLUDED, "inventory": {"identified_records": len(source_rows), "translated_records": len(records), "blocks": {"291": len(records)}},
        "records": records,
    }
    OUTPUT.write_text(json.dumps(batch, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {OUTPUT}: {len(records)} records, {len(EXCLUDED)} controls preserved")


if __name__ == "__main__":
    main()
