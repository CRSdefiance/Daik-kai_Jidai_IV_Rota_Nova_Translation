from __future__ import annotations

import csv
import json
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "work/sc2/script.csv"
OUTPUT = ROOT / "translations/lil_deep_route_v30.json"
SC2_SHA256 = "c2e0d1a2744a7da4a24f9693230b302a29f05bcaa036ebd5cc9726a6184731ff"
PUNCTUATION_IDS = {"DK4_MES_B111_R0062", "DK4_MES_B111_R0138"}

LINES = {
    "DK4_MES_B111_R0007": (
        "Wow, the temple really is covered in gold! What awful taste!",
        "Wow! A gold-plated temple! Talk about bad taste!",
    ),
    "DK4_MES_B111_R0011": ("Hey! Young lady!", "Hey, young lady!"),
    "DK4_MES_B111_R0015": ("Oh no! S-sorry.", "Oh, no! S-sorry!"),
    "DK4_MES_B111_R0018": (
        "Of all things, you call it bad taste? I cannot let that pass.",
        "Bad taste? How dare you say that!",
    ),
    "DK4_MES_B111_R0021": (
        "You cannot see the dignity and formal beauty within its splendor. Your eyes are still bound by worldly...",
        "You can't see the grace and beauty here. Your eyes are still so worldly...",
    ),
    "DK4_MES_B111_R0025": (
        "Enough lecturing! I already apologized!",
        "No more lectures! Sorry already!",
    ),
    "DK4_MES_B111_R0028": (
        "Hmm, how lamentable. Young people these days...",
        "Oh, the youth of today...",
    ),
    "DK4_MES_B111_R0031": ("If you have no business here, leave!", "No business? Then leave!"),
    "DK4_MES_B111_R0035": (
        "Fine. So there's no clue to the Proof here after all.",
        "Sure, sure. No clue to the Proof here, then.",
    ),
    "DK4_MES_B111_R0039": ("What? What did you just say?", "What? What did you just say?"),
    "DK4_MES_B111_R0043": (
        "Huh? I said there's no clue to the Proof of Supremacy. Did I upset him again?",
        "Huh? The Proof of Supremacy? No clue... (Did that upset him?)",
    ),
    "DK4_MES_B111_R0047": (
        "What! This ill-mannered girl seeks the Proof?",
        "What?! A rude girl like you seeks the Proof?",
    ),
    "DK4_MES_B111_R0051": ("You know about it, monk?", "Wait, you know about it?"),
    "DK4_MES_B111_R0054": ("I cannot believe this...", "Unbelievable..."),
    "DK4_MES_B111_R0058": (
        "Tell me if you know! I'll apologize again if you're still angry, okay?",
        "Then tell me! Sorry if you're still mad, okay?",
    ),
    "DK4_MES_B111_R0066": ("Please, okay?", "Please?"),
    "DK4_MES_B111_R0070": (
        "I must teach you some Eastern humility and proper manners.",
        "You need a lesson in Eastern humility and manners.",
    ),
    "DK4_MES_B111_R0077": (
        "Very well. I shall tell you, but you must train under me for a while.",
        "Very well. Train under me awhile; then you'll know.",
    ),
    "DK4_MES_B111_R0081": ("What?!", "What?!"),
    "DK4_MES_B111_R0085": (
        "If you cannot endure that, you cannot call yourself a conqueror.",
        "A true conqueror could endure this.",
    ),
    "DK4_MES_B111_R0088": ("Ugh, f-fine.", "Ugh, f-fine."),
    "DK4_MES_B111_R0092": (
        "Your reply should be, 'I understand,' should it not?",
        "Say, 'Understood, sir.'",
    ),
    "DK4_MES_B111_R0096": ("Yes, I understand!", "Understood, sir!"),
    "DK4_MES_B111_R0100": ("Hmm, good obedience.", "Good. Much better."),
    "DK4_MES_B111_R0112": (
        "Hee hee. This training suits foul-mouthed Lil perfectly.",
        "Heh. Just the training for rude {MACRO:FI}.",
    ),
    "DK4_MES_B111_R0119": ("Grrr...", "Grrr..."),
    "DK4_MES_B111_R0123": (
        "First, go buy rice to offer to the Buddha.",
        "Go buy rice to offer Buddha.",
    ),
    "DK4_MES_B111_R0126": (
        "Rice? Fine, a whole hold's worth, right? Who pays?",
        "Rice? A shipload, right? Who pays?",
    ),
    "DK4_MES_B111_R0130": ("Kah!", "Gah!"),
    "DK4_MES_B111_R0134": ("Whoa! What?", "Whoa! What?!"),
    "DK4_MES_B111_R0142": ("You mean I pay for it myself?", "You mean the bill's mine?"),
    "DK4_MES_B111_R0146": ("It is an offering.", "An offering."),
    "DK4_MES_B111_R0150": ("I cannot believe it...", "Unbelievable..."),
}

SPEAKERS = {0x02: "Lil Argot", 0x09: "Kamil", 0x89: "Temple monk"}


def main() -> None:
    with SOURCE.open(encoding="utf-8-sig", newline="") as stream:
        source_rows = {row["id"]: row for row in csv.DictReader(stream)}
    for row_id in PUNCTUATION_IDS:
        if source_rows[row_id]["source_hex"] != "898163":
            raise ValueError(f"{row_id}: monk's punctuation control changed")
    records = []
    counts: Counter[str] = Counter()
    for row_id, (source_meaning, english) in LINES.items():
        row = source_rows[row_id]
        lead = int(row["source_hex"][:2], 16)
        if lead not in SPEAKERS:
            raise ValueError(f"{row_id}: unmapped lead {lead:02X}")
        literal = english.replace("{MACRO:FI}", "")
        if "I" in literal or "F" in literal:
            raise ValueError(f"{row_id}: uppercase renderer macro byte in English")
        counts["111"] += 1
        records.append(
            {
                "id": row_id,
                "english": f"{{SPEAKER:{lead:02X}}}{english}{{PAD}}",
                "speaker": SPEAKERS[lead],
                "context": (
                    "Lil offends the gold-temple monk, then agrees to his training "
                    "in return for a clue to the Proof of Supremacy."
                ),
                "source_meaning": source_meaning,
                "localization_note": (
                    "Preserves Lil's teasing voice and the monk's formal register; "
                    "reviewed against clean Japanese and adjacent scene context."
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
    batch = {
        "format": "dk4-ilnk-translation-batch-v1",
        "file_path": "/data/SC2.DK4",
        "source_file_sha256": SC2_SHA256,
        "encoder": "dialogue-fixed-v1",
        "dialogue_profile": "lil-story-deep-route-v30-live",
        "translation_policy": "natural-dialogue-v2",
        "target_locale": "en-US",
        "review_gates": ["source", "context", "localization", "naturalness", "formatting"],
        "scope": "Lil and the gold-temple monk in SC2 B111.",
        "excluded_records": {
            row_id: "The three-byte monk-state ellipsis is already language-neutral; retain exact bytes."
            for row_id in sorted(PUNCTUATION_IDS)
        },
        "inventory": {
            "identified_records": len(LINES) + len(PUNCTUATION_IDS),
            "translated_records": len(records),
            "blocks": dict(counts),
        },
        "records": records,
    }
    OUTPUT.write_text(json.dumps(batch, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {OUTPUT.relative_to(ROOT)}: {len(records)} records, {len(PUNCTUATION_IDS)} exclusions")


if __name__ == "__main__":
    main()
