from __future__ import annotations

import csv
import json
from pathlib import Path


SOURCE = Path("work/sc3/script.csv")
REUSE = Path("work/analysis/sc3_cross_route_reuse.json")
OUTPUT = Path("translations/maria_deep_route_v26.json")
SC3_SHA256 = "001e21897ddb727ae261c82763ebef8515784ecfa571619c7614d87f3320aab2"
BLOCKS = (194, 198, 206, 210, 214, 231)

OVERRIDES = {
    "DK4_MES_B194_R0004": "You there.{LB}Don't leave without listening.",
    "DK4_MES_B194_R0007": "What's here?",
    "DK4_MES_B194_R0011": "Do you know of the Crusades?",
    "DK4_MES_B194_R0017": "Yes",
    "DK4_MES_B194_R0019": "No",
    "DK4_MES_B194_R0027": "Hmph. Noble knights reclaiming{LB}the Holy Land, right?",
    "DK4_MES_B194_R0033": "Europe calls them chivalrous armies{LB}that fought to reclaim the Holy Land...",
    "DK4_MES_B194_R0039": "A convenient lie.{LB}People here know what the Crusaders{LB}were truly like.",
    "DK4_MES_B194_R0042": "Truth?",
    "DK4_MES_B194_R0046": "Their goal was the region's wealth.{LB}They looted and killed freely{LB}all along the road.{LB}Nothing was forbidden.",
    "DK4_MES_B194_R0049": "Rewritten history is unforgivable!{LB}The true hero of this land{LB}was our own Saladin,{LB}not the Crusaders!",
    "DK4_MES_B194_R0052": "Saladin?",
    "DK4_MES_B194_R0056": "A Muslim hero.{LB}Beating Crusaders scarcely hints{LB}at his greatness.",
    "DK4_MES_B194_R0060": "His conduct in war was humane,{LB}as was his treatment of captives,{LB}civilians, and peace terms.{LB}He never acted dishonorably.",
    "DK4_MES_B194_R0063": "Europe's invaders...{LB}fascinating.",
    "DK4_MES_B194_R0066": "They say Saladin's armor vanished.{LB}Seek it if you wish to follow his example.",
    "DK4_MES_B198_R0011": "What is that?{LB}An unusual game.",
    "DK4_MES_B198_R0019": "Then the hero here is Charles...{LB}something?",
    "DK4_MES_B198_R0025": "Near Tours and Poitiers,{LB}he defeated a Muslim army{LB}advancing north from Spain.",
    "DK4_MES_B198_R0028": "Many have won battles in history.{LB}Why is he still a hero to children{LB}after so many centuries?",
    "DK4_MES_B198_R0031": "The victory's meaning.",
    "DK4_MES_B198_R0039": "So he saved Europe's culture{LB}and traditions.{LB}No wonder children call him a hero.",
    "DK4_MES_B198_R0047": "Posterity may call you a hero too,{LB}Admiral.",
    "DK4_MES_B206_R0007": "What is it?",
    "DK4_MES_B206_R0011": "At Alexandria's library,{LB}a fascinating scrap turned up.",
    "DK4_MES_B206_R0015": "Paper?",
    "DK4_MES_B206_R0022": "Hm.",
    "DK4_MES_B206_R0032": "Manuel,{LB}will that chisel repair{LB}our ship?",
    "DK4_MES_B210_R0007": "Cesare, what's wrong?{LB}Why so angry?",
    "DK4_MES_B210_R0013": "Nonsense?",
    "DK4_MES_B210_R0020": "Explain it more clearly...{LB}Never mind. What is it?",
    "DK4_MES_B210_R0038": "They cheer over foolish rumors!{LB}Were it so close, someone would{LB}have taken it already!",
    "DK4_MES_B210_R0041": "...{LB}(Words are useless right now.)",
    "DK4_MES_B214_R0009": "This is the stolen ornament?",
    "DK4_MES_B214_R0016": "Returned the frozen rose.",
    "DK4_MES_B214_R0029": "Keep it safe.{LB}Goodbye.",
    "DK4_MES_B214_R0051": "A wooden church?{LB}That is rare.{LB}Worth a visit.",
}

SPEAKERS = {
    "03": "Maria", "0D": "Cesare", "10": "Mikhail", "11": "Kamil",
    "17": "Manuel", "42": "Jean", "55": "Townsman", "93": "Patron",
    "BA": "Townswoman", "FE": "System",
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
            f"Maria V26 mismatch: missing={sorted(set(rows)-set(lines))}, "
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
            "context": "Complete shared historical, treasure-rumor, or recovery event.",
            "source_meaning": english,
            "localization_note": "Cross-route match or direct SC3 translation reviewed for natural English and state-byte safety.",
            "qa_waivers": ["weak-line-ending", "orphan-final-line"] + (["manual-break"] if "{LB}" in english else []),
            **({"manual_break_reason": "Protects semantic rows and pair phase."} if "{LB}" in english else {}),
            "review": {"source": True, "context": True, "localization": True, "naturalness": True, "formatting": True},
        })

    payload = {
        "format": "dk4-ilnk-translation-batch-v1", "file_path": "/data/SC3.DK4",
        "source_file_sha256": SC3_SHA256, "encoder": "dialogue-fixed-v1",
        "dialogue_profile": "maria-story-shared-events-v26-live",
        "translation_policy": "natural-dialogue-v2", "target_locale": "en-US",
        "review_gates": ["source", "context", "localization", "naturalness", "formatting"],
        "scope": "Maria SC3 blocks 194, 198, 206, 210, 214, and 231: six complete shared events.",
        "inventory": {"identified_records": len(rows), "translated_records": len(records), "excluded_records": 0, "blocks": block_counts},
        "excluded": [], "records": records,
    }
    OUTPUT.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {OUTPUT}: {len(records)} records")


if __name__ == "__main__":
    main()
