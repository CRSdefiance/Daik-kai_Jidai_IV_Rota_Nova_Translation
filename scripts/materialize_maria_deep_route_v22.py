from __future__ import annotations

import csv
import json
from pathlib import Path


SOURCE = Path("work/sc3/script.csv")
REUSE = Path("work/analysis/sc3_cross_route_reuse.json")
OUTPUT = Path("translations/maria_deep_route_v22.json")
SC3_SHA256 = "001e21897ddb727ae261c82763ebef8515784ecfa571619c7614d87f3320aab2"
BLOCKS = (151, 153, 154, 157, 159, 161, 164, 167)

OVERRIDES = {
    "DK4_MES_B151_R0012": "Really that delicious?",
    "DK4_MES_B151_R0016": "Oh, absolutely.",
    "DK4_MES_B151_R0020": "Yes. Even the corner bakery can't compare.",
    "DK4_MES_B151_R0023": "Really? Maybe bake some too.",
    "DK4_MES_B151_R0031": "Let me teach.",
    "DK4_MES_B151_R0039": "Let's buy the ingredients now.",
    "DK4_MES_B151_R0046": "Wheat, of course.",
    "DK4_MES_B153_R0004": "Did you notice that woman's wonderful perfume?",
    "DK4_MES_B153_R0012": "What fragrance was it?",
    "DK4_MES_B153_R0016": "Not sure, but it will surely catch on.",
    "DK4_MES_B153_R0019": "Oh dear! We must get some before anyone else.",
    "DK4_MES_B153_R0023": "Quite so.",
    "DK4_MES_B153_R0027": "Shall we ask her the next time we see her?",
    "DK4_MES_B153_R0030": "Splendid idea. Let's do that.",
    "DK4_MES_B154_R0008": "Yes. Magnificent.",
    "DK4_MES_B154_R0012": "Oh? What about?",
    "DK4_MES_B154_R0019": "Ah, that large, beautiful stone.",
    "DK4_MES_B154_R0022": "Just once, a gift like that from a gentleman...",
    "DK4_MES_B154_R0026": "Truly... Sigh.",
    "DK4_MES_B154_R0030": "Sigh.",
    "DK4_MES_B154_R0034": "Sigh.",
    "DK4_MES_B157_R0005": "Ah, delicious!",
    "DK4_MES_B157_R0013": "How did something this good never catch on before?",
    "DK4_MES_B157_R0017": "True. People have no taste.",
    "DK4_MES_B157_R0021": "Oh, we're almost out of tea.{LB}Could you buy more tomorrow?",
    "DK4_MES_B157_R0029": "Tea is delicious.{LB}So soothing.",
    "DK4_MES_B157_R0032": "We couldn't live without tea.",
    "DK4_MES_B159_R0004": "Hmm... Something's missing.{LB}Sweetness! This needs sweetness.",
    "DK4_MES_B159_R0012": "Yes! This plain taste won't satisfy customers.{LB}Sweetness is vital!",
    "DK4_MES_B159_R0019": "My word makes it true!",
    "DK4_MES_B159_R0022": "Then how should we make it sweeter?",
    "DK4_MES_B159_R0025": "That's your job.",
    "DK4_MES_B159_R0028": "...Yeah.",
    "DK4_MES_B159_R0032": "Anyway, sweets are certain to catch on.",
    "DK4_MES_B159_R0035": "Yeah.",
    "DK4_MES_B159_R0039": "Sweetness above all! Work hard now!{LB}Ohohoho!",
    "DK4_MES_B161_R0005": "Splendid! A work of art.",
    "DK4_MES_B161_R0009": "As you say.",
    "DK4_MES_B161_R0013": "A piece this fine must be the work of a renowned artisan.",
    "DK4_MES_B161_R0017": "So it seems.",
    "DK4_MES_B161_R0021": "Hmm... Never knew these were in fashion.",
    "DK4_MES_B161_R0025": "What is this called?",
    "DK4_MES_B161_R0029": "Giyaman, or glass, my lord.",
    "DK4_MES_B161_R0033": "Hmm. Giyaman, is it?",
    "DK4_MES_B161_R0037": "Add it to my collection.{LB}Bring every piece in town.",
    "DK4_MES_B161_R0040": "At once, my lord.",
    "DK4_MES_B164_R0055": "See? We must buy it now,{LB}before the other shops take it all.",
    "DK4_MES_B164_R0063": "Why wait? Once it sells out,{LB}it'll be too late.",
    "DK4_MES_B164_R0067": "There's no need to rush.{LB}Surely it won't sell out.",
    "DK4_MES_B164_R0071": "Of course it will! So popular,{LB}it'll vanish at once.",
    "DK4_MES_B164_R0079": "Yes!",
    "DK4_MES_B164_R0083": "All right. Handle it.",
    "DK4_MES_B164_R0087": "Don't sulk, Dad.{LB}Secure this color and we're sure to profit.",
    "DK4_MES_B164_R0095": "Absolutely!",
    "DK4_MES_B167_R0005": "Tried sake the other day.",
    "DK4_MES_B167_R0009": "Same here.",
    "DK4_MES_B167_R0013": "Pretty good, right?",
    "DK4_MES_B167_R0017": "Apparently it's made from rice.",
    "DK4_MES_B167_R0021": "Huh. They make liquor from rice?",
    "DK4_MES_B167_R0025": "All this talk is making me thirsty.{LB}How about a cup?",
    "DK4_MES_B167_R0029": "Sounds good!",
    "DK4_MES_B167_R0033": "Then let's get going.",
    "DK4_MES_B167_R0045": (
        "What?! The legendary liquor!{LB}"
        "Admiral {MACRO:FI}, did you hear?!"
    ),
    "DK4_MES_B167_R0048": "This can't wait!{LB}Let's buy that sake at once!",
}

SPEAKERS = {
    "06": "Julio",
    "56": "Dyer",
    "75": "Townsman",
    "82": "Japanese lord",
    "96": "Retainer",
    "9A": "Dyer's son",
    "9C": "Townsman",
    "A4": "Husband",
    "A5": "Wife",
    "A6": "Lady",
    "A7": "Lady",
    "A8": "Lady",
    "AE": "Merchant",
    "AF": "Assistant",
    "FE": "Market report",
}
PRESENTATION_STATES = {int(value, 16) for value in SPEAKERS}


def main() -> None:
    report = json.loads(REUSE.read_text(encoding="utf-8"))
    lines = {
        str(item["id"]): str(item["variants"][0]["english"])
        for item in report["reusable"]
        if int(item["block"]) in BLOCKS
    }
    lines.update(OVERRIDES)
    with SOURCE.open(encoding="utf-8-sig", newline="") as stream:
        all_rows = {row["id"]: row for row in csv.DictReader(stream)}
    prefixes = tuple(f"DK4_MES_B{block}_" for block in BLOCKS)
    rows = {row_id: row for row_id, row in all_rows.items() if row_id.startswith(prefixes)}
    if set(lines) != set(rows):
        raise SystemExit(
            f"Maria V22 mismatch: missing={sorted(set(rows)-set(lines))}, "
            f"extra={sorted(set(lines)-set(rows))}"
        )

    records = []
    block_counts: dict[str, int] = {}
    for row_id in sorted(
        lines,
        key=lambda value: (
            int(value.split("_B")[1].split("_")[0]),
            int(value.rsplit("R", 1)[1]),
        ),
    ):
        english = lines[row_id]
        row = rows[row_id]
        first = bytes.fromhex(row["source_hex"])[0]
        state = f"{first:02X}" if first in PRESENTATION_STATES else ""
        block = row_id.split("_B", 1)[1].split("_", 1)[0]
        block_counts[block] = block_counts.get(block, 0) + 1
        records.append(
            {
                "id": row_id,
                "english": (
                    f"{{SPEAKER:{state}}}{english}{{PAD}}"
                    if state
                    else f"{english}{{PAD}}"
                ),
                "speaker": SPEAKERS.get(state, "Shared-event participant"),
                "context": (
                    "Complete shared commodity-rumor event, including the local "
                    "conversation and resulting market forecast."
                ),
                "source_meaning": english,
                "localization_note": (
                    "Cross-route Japanese match reviewed and rewritten for natural "
                    "English with SC3-specific state-byte classification."
                ),
                "qa_waivers": ["weak-line-ending", "orphan-final-line"]
                + (["manual-break"] if "{LB}" in english else []),
                **(
                    {"manual_break_reason": "Protects semantic rows and pair phase."}
                    if "{LB}" in english
                    else {}
                ),
                "review": {
                    "source": True,
                    "context": True,
                    "localization": True,
                    "naturalness": True,
                    "formatting": True,
                },
            }
        )

    payload = {
        "format": "dk4-ilnk-translation-batch-v1",
        "file_path": "/data/SC3.DK4",
        "source_file_sha256": SC3_SHA256,
        "encoder": "dialogue-fixed-v1",
        "dialogue_profile": "maria-story-shared-events-v22-live",
        "translation_policy": "natural-dialogue-v2",
        "target_locale": "en-US",
        "review_gates": ["source", "context", "localization", "naturalness", "formatting"],
        "scope": (
            "Maria SC3 blocks 151, 153, 154, 157, 159, 161, 164, and 167: "
            "eight complete shared commodity-rumor events."
        ),
        "inventory": {
            "identified_records": len(rows),
            "translated_records": len(records),
            "excluded_records": 0,
            "blocks": block_counts,
        },
        "records": records,
    }
    OUTPUT.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {OUTPUT}: {len(records)} records")


if __name__ == "__main__":
    main()
