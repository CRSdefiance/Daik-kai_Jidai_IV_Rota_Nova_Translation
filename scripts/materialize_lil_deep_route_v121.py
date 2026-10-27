from __future__ import annotations

import csv
import json

from scripts.materialize_lil_deep_route_v107 import ROOT, SC2_SHA256

LINES = {
    19: "Admiral, wandering this jungle blindly is risky.",
    20: "Admiral, we can't roam this jungle blindly.",
    21: "Admiral, roaming this jungle blindly is risky.",
    22: "Admiral, no way are we roaming this jungle blindly!",
    23: "Admiral, roaming this jungle blindly is risky.",
    24: "Admiral, walking this jungle with no map is dangerous!",
    25: "Admiral, roaming this jungle blindly is risky.",
    49: "Shall we go?",
    51: "Let's go, then.",
    53: "Come on! Let's go!",
    55: "Let's go, then.",
    57: "Let's go.",
    59: "Off we go.",
    63: "Ugh, so hot and humid!",
    84: "A cave out here...?",
    86: "Huh? There's a cave.",
    90: "Ugh, pitch dark! W-we have to go on...",
    93: "Ma'am?",
    99: "Grope ahead",
    101: "Light up",
    108: "The dark's scary, but so are strange creatures... Let's go on!",
    113: "Oh? This feels...",
    116: "Admiral! A giant snake! Someone's hurt!",
    127: "Whoa! A South Asian python! (Maybe?)",
    133: "Aah! A snake! Nooo!",
    141: "Some sailors are hurt.",
    147: "Phew... So tired... Where are we?",
    158: "...Not sure, but we seem near the ruins.",
    159: "...We seem near the ruins.",
    161: "Here? Um... Not sure, but aren't we near the ruins?",
    163: "Um...? Seems we're near the ruins.",
    165: "Oh!? Aren't we near the ruins now!?",
    167: "Where are we!? ...Hmm. Seems we're near the ruins.",
    168: "Here? Um... Huh? Not sure, but we seem to be near the ruins! Lucky!",
    170: "Hmm... Seems we're near the ruins.",
    176: "Let's light up, then.",
    180: "Aaah! What's going on?!",
    194: "Too many!",
    196: "Too many of them!",
    198: "Aaah! Admiral, this many isn't normal!",
    199: "Too many!",
    201: "Admiral! We can't go on while fighting so many bats!",
    202: "Aaah, bats! So creepy!",
    205: "Charge through! Everyone, run for the exit!",
    215: "The sailors seem tired.",
    228: "We did it, Admiral! Out of the jungle!",
    229: "Out of the jungle!",
    231: "Yes, Admiral! Out of the jungle!",
    232: "Phew, out of the jungle!",
    234: "Yes, Admiral! Out of the jungle!",
    235: "We did it! Out of the jungle!",
    236: "We did it, Admiral! We've made it out of the jungle!",
    249: "Admiral, the ruins!",
    251: "Admiral, the ruins!",
    253: "Admiral, ruins!",
    255: "Admiral, the ruins.",
    257: "Admiral, the ruins!",
    259: "Admiral, the ruins!",
    261: "Admiral, we're at the ruins.",
}
STATES = {0x02, 0x16, 0xCF, 0xD0, 0xD3, 0xD6, 0xFE}
EXCLUDED = {
    "DK4_MES_B324_R0037": "Packed jungle event 60 40 46 99 80 3F 63; identical SC0B333R0037/SC1B317R0037/SC3B292R0036. Preserve unchanged.",
    "DK4_MES_B324_R0143": "Packed snake aftermath 2B 63 20 46 94 80; identical SC1B317R0143/SC3B292R0141. Preserve unchanged.",
    "DK4_MES_B324_R0217": "Packed bat aftermath 2B 63 10 46 94 80; identical SC0B333R0200/SC1B317R0216/SC3B292R0215. Preserve unchanged.",
}


def main() -> None:
    with (ROOT / "work/sc2/script.csv").open(encoding="utf-8-sig", newline="") as stream:
        source = {r["id"]: r for r in csv.DictReader(stream)}
    expected = {i for i in source if "_B324_" in i}
    assert expected == {f"DK4_MES_B324_R{n:04d}" for n in LINES} | set(EXCLUDED)
    records = []
    for n, text in LINES.items():
        row_id = f"DK4_MES_B324_R{n:04d}"
        raw = bytes.fromhex(source[row_id]["source_hex"])
        assert "I" not in text and "F" not in text, row_id
        assert not any(m in raw for m in (b"FI", b"FA", b"FO")), row_id
        state = raw[0] in STATES
        records.append({"id": row_id, "english": (f"{{SPEAKER:{raw[0]:02X}}}" if state else "") + text + "{PAD}", "speaker": "Lil" if raw[0] == 2 else "Companion or system", "context": "Jungle map warning, humid heat, dark cave: feel ahead or light up; giant snake injuries, bat swarm, sailors' fatigue, jungle exit and ruins arrival.", "source_meaning": text, "source_japanese": raw[int(state):].decode("shift_jis", errors="replace"), "localization_note": "Natural English retains all companion variants, both cave branches, python uncertainty, injuries, bats and fatigue. Lil addressed as Ma'am in tiny Admiral line. Bare Japanese leads preserved as prose; native states and packed events unchanged.", "review": {g: True for g in ("source", "context", "localization", "naturalness", "formatting")}})
    batch = {"format": "dk4-ilnk-translation-batch-v1", "file_path": "/data/SC2.DK4", "source_file_sha256": SC2_SHA256, "encoder": "dialogue-fixed-v1", "dialogue_profile": "lil-story-deep-route-v121-live", "translation_policy": "natural-dialogue-v2", "target_locale": "en-US", "review_gates": ["source", "context", "localization", "naturalness", "formatting"], "scope": "Complete B324 jungle and cave branches.", "inventory": {"identified_records": len(expected), "translated_records": len(records), "blocks": {"324": len(records)}}, "excluded_records": EXCLUDED, "records": records}
    (ROOT / "translations/lil_deep_route_v121.json").write_text(json.dumps(batch, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"wrote Lil V121: {len(records)} records")


if __name__ == "__main__":
    main()
