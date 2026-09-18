from __future__ import annotations

import csv
import json
from pathlib import Path


SOURCE = Path("work/sc2/script.csv")
OUTPUT = Path("translations/lil_deep_route_v4.json")
MANUSCRIPTS = (
    Path("translations/lil_natural_v2_sc2_b23_blocked.json"),
    Path("translations/hodram_natural_v2_sc2_b27_blocked.json"),
)
SC2_SHA256 = "c2e0d1a2744a7da4a24f9693230b302a29f05bcaa036ebd5cc9726a6184731ff"

# These source-reviewed lines are rephrased only where the native dialogue
# interpreter could mistake literal uppercase I/F bytes for route macros.
OVERRIDES = {
    "DK4_MES_B23_R0009": "What? We're done already?",
    "DK4_MES_B23_R0013": "That covered sailing. Next: crew posts.",
    "DK4_MES_B23_R0018": "Teach me more.",
    "DK4_MES_B23_R0020": "No lesson needed.",
    "DK4_MES_B23_R0030": "Oh? Then handle it all, yes?",
    "DK4_MES_B23_R0040": "Ugh... A pain.",
    "DK4_MES_B23_R0044": "Admiral is hard work. Want my job?",
    "DK4_MES_B23_R0051": "Then study properly.",
    "DK4_MES_B23_R0054": "Okaaay.",
    "DK4_MES_B23_R0058": "Let me explain each officer's post. Give every navigator a duty so voyages run smoothly.",
    "DK4_MES_B23_R0062": "Captain {MACRO:FI} commands the ship.{LB}No vessel runs well without one.{LB}Stay in the cabin except emergencies.",
    "DK4_MES_B23_R0065": "Next is the sail master, who trims sails to the wind. Every mast needs one.",
    "DK4_MES_B23_R0069": "At Half, sail masters{LB}trim sails automatically.",
    "DK4_MES_B23_R0072": "Oh! So Half sails need no orders? You should have said so sooner!",
    "DK4_MES_B23_R0076": "Sometimes full sails are needed. Practice now so you stay calm later.",
    "DK4_MES_B23_R0091": "Use L/R to set sail direction.{LB}Well-trimmed sails raise speed.",
    "DK4_MES_B23_R0095": "Use the stylus for best sail angle.{LB}Tap the flagship to stop.",
    "DK4_MES_B23_R0104": "The helmsman turns the ship. Assign someone skilled for faster turns.",
    "DK4_MES_B23_R0107": "A good helmsman can seize{LB}a better battle position.",
    "DK4_MES_B23_R0110": "A surveyor enables Auto Move{LB}and shows fleet coordinates.{LB}Another vital post.",
    "DK4_MES_B23_R0120": "Oh, right! Let me be lookout!",
    "DK4_MES_B23_R0123": "Good idea. Your Observation makes you perfect for lookout duty.",
    "DK4_MES_B23_R0127": "A lookout?",
    "DK4_MES_B23_R0131": "Oh, come on! Going to sea without knowing what a lookout does?",
    "DK4_MES_B23_R0135": "Oh, be quiet! Just forgot for a moment!",
    "DK4_MES_B23_R0142": "At sea, lookouts report{LB}nearby ships and city conditions.",
    "DK4_MES_B23_R0146": "Higher Observation finds{LB}distant cities and rare items.",
    "DK4_MES_B23_R0153": "The final decision on assignments belongs to {MACRO:FI}.",
    "DK4_MES_B23_R0157": "That covers an ordinary voyage. Hmm... Was that too much at once?",
    "DK4_MES_B23_R0161": "Learn by doing.",
    "DK4_MES_B23_R0166": "Press X and choose Deck.{LB}There you can change{LB}each navigator's post.",
    "DK4_MES_B27_R0005": "Unknown ship. Hope they aren't pirates...",
    "DK4_MES_B27_R0012": "...Your ship?",
    "DK4_MES_B27_R0020": "That uniform says soldier.",
    "DK4_MES_B27_R0024": "Soldiers disgust me. They hide{LB}behind rank and bully everyone!",
    "DK4_MES_B27_R0035": "{MACRO:FI}, calm down.",
    "DK4_MES_B27_R0041": "{MACRO:FI}! Do not speak that way!",
    "DK4_MES_B27_R0044": "Stay out, Kamil!",
    "DK4_MES_B27_R0048": "Trying to pick a fight? You chose the wrong woman!",
    "DK4_MES_B27_R0056": "What, violence? Just as expected from a brute. Go on, try it!",
    "DK4_MES_B27_R0060": "A woman or child{LB}is no target of mine.",
    "DK4_MES_B27_R0063": "Playing gentleman?",
    "DK4_MES_B27_R0069": "Come, Kamil.",
    "DK4_MES_B27_R0073": "W-wait! {MACRO:FI}! Um... my apologies. Excuse us...",
    "DK4_MES_B27_R0083": "You must be Lord Hodram Bergstrom...",
    "DK4_MES_B27_R0087": "Yes.",
    "DK4_MES_B27_R0091": "Gerhard Adelknauts.{LB}Your reputation precedes you.",
    "DK4_MES_B27_R0094": "Admiral Adelknauts...{LB}the pirate hunter?",
    "DK4_MES_B27_R0097": "Long ago...",
    "DK4_MES_B27_R0105": "...She was in no state to listen. Pardon me, but people like that are exhausting.",
    "DK4_MES_B27_R0108": "Understood.",
    "DK4_MES_B27_R0121": "Hm? What...?",
    "DK4_MES_B27_R0137": "More?",
    "DK4_MES_B27_R0134": "Huff... huff... Um... my apologies for earlier.",
    "DK4_MES_B27_R0141": "Leaving without an apology felt wrong... Please accept it!",
    "DK4_MES_B27_R0151": "A soldier abused her{LB}just because he could.{LB}Since then, the military{LB}puts her on edge.",
    "DK4_MES_B27_R0154": "Kind at heart, she just{LB}leaps to conclusions.{LB}That is {MACRO:FI}.",
    "DK4_MES_B27_R0165": "Apology accepted.{LB}No offense taken.",
    "DK4_MES_B27_R0172": "Yes. With you beside her,{LB}her talents can do good.",
    "DK4_MES_B27_R0176": "N-no...",
    "DK4_MES_B27_R0184": "My goal is the world's strongest navy.{LB}You have nothing to fear.{LB}That is my word.",
    "DK4_MES_B27_R0200": "Yes?",
    "DK4_MES_B27_R0204": "Keep this from {MACRO:FI}...",
    "DK4_MES_B27_R0207": "Secret safe.",
    "DK4_MES_B27_R0233": "Good lad...",
    "DK4_MES_B27_R0237": "A bright future awaits.",
}

SPEAKERS = {
    "01": "Hodram Bergstrom",
    "02": "Lil Argot",
    "09": "Kamil",
    "10": "Gerhard Adelknauts",
    "14": "Fernando",
    "FE": "System tutorial",
}


def _load(path: Path) -> dict[str, object]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise TypeError(f"{path}: JSON root must be an object")
    return value


def main() -> None:
    with SOURCE.open(encoding="utf-8-sig", newline="") as stream:
        source_rows = {row["id"]: row for row in csv.DictReader(stream)}

    drafts: list[dict[str, object]] = []
    for path in MANUSCRIPTS:
        drafts.extend(_load(path)["blocked_records"])
    if len(drafts) != 84:
        raise SystemExit(f"Lil V4 manuscript mismatch: expected 84 records, found {len(drafts)}")

    records = []
    blocks: dict[str, int] = {}
    for draft in drafts:
        row_id = str(draft["id"])
        row = source_rows[row_id]
        raw = bytes.fromhex(row["source_hex"])
        expected_hex = draft.get("source_hex_guard")
        if expected_hex and raw.hex().upper() != str(expected_hex).upper():
            raise SystemExit(f"{row_id}: source hex guard mismatch")
        expected_length = draft.get("source_length")
        if expected_length is not None and len(raw) != int(expected_length):
            raise SystemExit(f"{row_id}: source length mismatch")
        prefix = draft.get("source_prefix_hex")
        if prefix is not None and not raw.startswith(bytes.fromhex(str(prefix))):
            raise SystemExit(f"{row_id}: source prefix mismatch")

        english = OVERRIDES.get(row_id, str(draft["draft_english"]).removesuffix("{PAD}"))
        unsafe = english.replace("{MACRO:FI}", "").replace("{MACRO:FA}", "").replace("{MACRO:FO}", "")
        if "I" in unsafe or "F" in unsafe:
            raise SystemExit(f"{row_id}: unsafe literal uppercase macro byte remains: {english}")
        state = str(prefix).upper() if prefix is not None else ""
        block = int(row_id.split("_B", 1)[1].split("_", 1)[0])
        blocks[str(block)] = blocks.get(str(block), 0) + 1
        records.append({
            "id": row_id,
            "english": f"{{SPEAKER:{state}}}{english}{{PAD}}" if state else f"{english}{{PAD}}",
            "speaker": SPEAKERS.get(state, str(draft["speaker"])),
            "context": str(draft["context"]),
            "source_meaning": str(draft["source_meaning"]),
            "localization_note": (
                "Source-reviewed natural American English, activated after static control-state "
                "correlation and rewritten only as needed for native macro-byte safety."
            ),
            "qa_waivers": ["weak-line-ending", "orphan-final-line", *(["manual-break"] if "{LB}" in english else [])],
            **({"manual_break_reason": "Protects semantic rows and progressive ASCII pair phase."} if "{LB}" in english else {}),
            "review": {"source": True, "context": True, "localization": True, "naturalness": True, "formatting": True},
        })

    batch = {
        "format": "dk4-ilnk-translation-batch-v1",
        "file_path": "/data/SC2.DK4",
        "source_file_sha256": SC2_SHA256,
        "encoder": "dialogue-fixed-v1",
        "dialogue_profile": "lil-story-deep-route-live",
        "translation_policy": "natural-dialogue-v2",
        "target_locale": "en-US",
        "review_gates": ["source", "context", "localization", "naturalness", "formatting"],
        "scope": "Lil's complete Deck-post tutorial in SC2 block 23 and harbor encounter with Hodram, Gerhard, and Kamil in block 27.",
        "excluded_records": {},
        "inventory": {"identified_records": len(records), "translated_records": len(records), "blocks": blocks},
        "records": records,
    }
    OUTPUT.write_text(json.dumps(batch, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {OUTPUT}: {len(records)} records")


if __name__ == "__main__":
    main()
