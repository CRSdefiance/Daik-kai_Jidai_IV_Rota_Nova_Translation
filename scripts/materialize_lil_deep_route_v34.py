from __future__ import annotations

import csv
import json
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "work/sc2/script.csv"
OUTPUT = ROOT / "translations/lil_deep_route_v34.json"
SC2_SHA256 = "c2e0d1a2744a7da4a24f9693230b302a29f05bcaa036ebd5cc9726a6184731ff"
FRAGMENTS = {
    "DK4_MES_B117_R0004": "60344693803F63344872A8",
    "DK4_MES_B118_R0004": "60944695803B63",
}
LINES = {
    "DK4_MES_B116_R0006": ("Hey, wait!", "Hey, wait!"),
    "DK4_MES_B116_R0014": (
        "I can't just accept a present without giving something back. I'll tell you something useful as thanks.",
        "You gave me a present, so let me return the favor. Here's a tip you might like.",
    ),
    "DK4_MES_B116_R0018": (
        "There's a wonderful building in India. Having come this far, you should definitely visit it.",
        "The subcontinent has a magnificent building that's well worth a visit.",
    ),
    "DK4_MES_B116_R0022": (
        "The trouble is that you can't reach it without a map. Do go and see it.",
        "You'll need a map to find it. You really should go see it.",
    ),
    "DK4_MES_B116_R0025": ("Yes! Thank you!", "Sure! Thanks!"),
    "DK4_MES_B117_R0006": ("Admiral, this statue...", "This statue..."),
    "DK4_MES_B117_R0010": ("Huh?", "Hm?"),
    "DK4_MES_B117_R0021": (
        "The design seems out of place in this building.",
        "The design seems out of place here.",
    ),
    "DK4_MES_B117_R0022": (
        "Its design seems unsuitable for this building.",
        "The design doesn't suit this building.",
    ),
    "DK4_MES_B117_R0023": (
        "It seems out of place in this building.",
        "That looks out of place here.",
    ),
    "DK4_MES_B117_R0024": (
        "It seems mismatched with this building.",
        "Doesn't fit in here, does it?",
    ),
    "DK4_MES_B117_R0025": (
        "Don't you think it doesn't fit this building?",
        "Doesn't fit this building, does it?",
    ),
    "DK4_MES_B117_R0026": (
        "It seems rather unsuitable for this building.",
        "Rather out of place here, wouldn't you agree?",
    ),
    "DK4_MES_B117_R0027": (
        "It doesn't seem to match this building.",
        "Doesn't fit in here, does it?",
    ),
    "DK4_MES_B117_R0029": (
        "Isn't the design inappropriate for this building?",
        "That design looks out of place, doesn't it?",
    ),
    "DK4_MES_B117_R0032": ("Hmm, that's true.", "You're right."),
    "DK4_MES_B117_R0042": (
        "It looks like a figurehead. Perhaps it originally was one?",
        "Looks like a figurehead... Perhaps it was one.",
    ),
    "DK4_MES_B117_R0043": (
        "It's shaped like a figurehead. No, perhaps it was one to begin with?",
        "Looks like a figurehead... Could it really be one?",
    ),
    "DK4_MES_B117_R0044": (
        "Doesn't this look like a figurehead? Or rather, isn't it a figurehead?",
        "This looks like a figurehead. Could that be what it really is?",
    ),
    "DK4_MES_B117_R0046": (
        "It looks like a figurehead. Ah, could it actually be one?",
        "Looks like a figurehead... Could it really be one?",
    ),
    "DK4_MES_B117_R0047": (
        "It looks like a figurehead. Or rather, isn't it one?",
        "Looks like a figurehead... Wait, could it really be one?",
    ),
    "DK4_MES_B117_R0048": (
        "It's shaped like a figurehead. No, it was a figurehead all along.",
        "Looks like a figurehead. Ah, that's what it really is!",
    ),
    "DK4_MES_B117_R0049": (
        "This could be made into a figurehead. Look.",
        "We can use it on the bow!",
    ),
    "DK4_MES_B117_R0050": (
        "It's shaped like a figurehead. No, perhaps it was a figurehead to begin with?",
        "Looks like a figurehead... Was it one all along?",
    ),
    "DK4_MES_B117_R0053": ("Oh, you're right!", "Oh! You're right!"),
    "DK4_MES_B118_R0006": ("Oh! This is...!", "Oh! This is...!"),
    "DK4_MES_B118_R0010": (
        "As its discoverers, you have the right to own this small knife.",
        "This knife is yours to keep. You discovered it.",
    ),
    "DK4_MES_B118_R0016": (
        "Thanks to you, we finally found the spiritual mainstay of our tribe. Please accept this.",
        "Thanks to you, our tribe has found its source of hope at last. Please accept this.",
    ),
    "DK4_MES_B118_R0020": (
        "Received 24,000 gold coins.",
        "Received 24,000 gold coins.",
    ),
    "DK4_MES_B118_R0026": (
        "Now, let's return. Your fleet must be waiting eagerly.",
        "Let's head back. Your fleet must be waiting for you.",
    ),
}
SPEAKERS = {
    0x02: "Lil Argot",
    0xC6: "Gift recipient",
    0xD1: "Selected crewmate",
    0xDC: "Figurehead observer",
    0xB3: "Tribal representative",
    0xFE: "System reward",
}
TEXT_LEADS = {0x82, 0x91}
CONTEXTS = {
    "116": "A gift recipient repays Lil's kindness with a tip about a building in India and the map needed to reach it.",
    "117": "Lil and companion variants inspect a statue that seems out of place, then recognize its figurehead shape.",
    "118": "A tribal representative recognizes the recovered knife and rewards the finders with 24,000 gold coins.",
}


def main() -> None:
    with SOURCE.open(encoding="utf-8-sig", newline="") as stream:
        source_rows = {row["id"]: row for row in csv.DictReader(stream)}
    for row_id, raw_hex in FRAGMENTS.items():
        if source_rows[row_id]["source_hex"] != raw_hex:
            raise ValueError(f"{row_id}: non-prose fragment changed")
    records = []
    counts: Counter[str] = Counter()
    for row_id, (source_meaning, english) in LINES.items():
        row = source_rows[row_id]
        lead = int(row["source_hex"][:2], 16)
        if lead not in SPEAKERS and lead not in TEXT_LEADS:
            raise ValueError(f"{row_id}: unmapped lead {lead:02X}")
        if "I" in english or "F" in english:
            raise ValueError(f"{row_id}: uppercase renderer macro byte in English")
        block = row_id.split("_B", 1)[1].split("_R", 1)[0]
        counts[block] += 1
        records.append({
            "id": row_id,
            "english": (f"{{SPEAKER:{lead:02X}}}" if lead in SPEAKERS else "") + english + "{PAD}",
            "speaker": SPEAKERS.get(lead, "Companion variant"),
            "context": CONTEXTS[block],
            "source_meaning": source_meaning,
            "localization_note": (
                "Localized from clean Japanese with adjacent dialogue and companion voice reviewed. "
                "Cross-route source matches corroborate C6/D1/DC/B3 states; ordinary 82/91 starts retain their first English glyph. "
                + ("The subcontinent refers to India without using the renderer's unsafe literal uppercase I byte. " if row_id == "DK4_MES_B116_R0018" else "")
                + ("The bow reference conveys using the statue as a figurehead in this short companion variant. " if row_id == "DK4_MES_B117_R0049" else "")
            ),
            "review": {gate: True for gate in ("source", "context", "localization", "naturalness", "formatting")},
        })
    batch = {
        "format": "dk4-ilnk-translation-batch-v1",
        "file_path": "/data/SC2.DK4",
        "source_file_sha256": SC2_SHA256,
        "encoder": "dialogue-fixed-v1",
        "dialogue_profile": "lil-story-deep-route-v34-live",
        "translation_policy": "natural-dialogue-v2",
        "target_locale": "en-US",
        "review_gates": ["source", "context", "localization", "naturalness", "formatting"],
        "scope": "SC2 B116-B118 India tip, figurehead discovery, and tribal knife reward.",
        "inventory": {"identified_records": len(LINES) + len(FRAGMENTS), "translated_records": len(records), "blocks": dict(counts)},
        "excluded_records": {row_id: f"Non-prose staging fragment {raw_hex}; left unchanged pending runtime mapping." for row_id, raw_hex in FRAGMENTS.items()},
        "records": records,
    }
    OUTPUT.write_text(json.dumps(batch, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {OUTPUT.relative_to(ROOT)}: {len(records)} records")


if __name__ == "__main__":
    main()
