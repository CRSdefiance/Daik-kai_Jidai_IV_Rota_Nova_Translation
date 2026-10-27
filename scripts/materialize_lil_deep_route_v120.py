from __future__ import annotations

import csv
import json

from scripts.materialize_lil_deep_route_v107 import ROOT, SC2_SHA256

LINES = {
    20: "Admiral, no map? We'll get lost.",
    21: "Admiral, no map? We'll be lost.",
    22: "Admiral, no map? We'll get lost!",
    23: "Admiral, no map? We'll get lost.",
    24: "Admiral, no map? We'll get lost.",
    25: "Admiral, no map? We'll get lost.",
    26: "Admiral, get us a map!",
    27: "Admiral, no map? We'll get lost.",
    52: "Well, let's set out.",
    54: "Shall we go?",
    56: "Come on!",
    58: "Let's head out, then.",
    60: "Let's go, then!",
    62: "Come on! Off we go!",
    64: "Let's get going!",
    77: "Here comes fog.",
    79: "Here comes fog.",
    81: "So foggy.",
    83: "The fog's here.",
    85: "Such thick fog!",
    87: "Here comes fog.",
    89: "Such thick fog!",
    95: "Go on",
    97: "Wait",
    104: "Let's try going on.",
    117: "Seems it's a dead end.",
    119: "A dead end...",
    121: "Oh no. A dead end.",
    123: "A dead end...",
    125: "Seems it's a dead end.",
    127: "Oh no. A dead end.",
    129: "Well, well. A dead end.",
    135: "Push on",
    137: "Seek a path",
    144: "We're going on! We'll find a way!",
    157: "Let's try.",
    159: "Let's try it.",
    161: "This is crazy... But let's try it.",
    162: "Let's try.",
    164: "All right! Let's go on!",
    166: "That's reckless. But let's try, then.",
    167: "This is crazy... All right, let's go!",
    173: "The sailors seem tired.",
    178: "Let's find a way round, then.",
    190: "Admiral, another path!",
    192: "Admiral, another path!",
    194: "Admiral, look! Another path!",
    196: "Admiral, a path here!",
    198: "Admiral, a path here!",
    200: "Admiral, we can go this way!",
    202: "Admiral! Over here!",
    204: "There's a path over here!",
    212: "Can't see a thing... Let's wait for the fog to clear.",
    225: "That seems a better idea.",
    227: "Good idea.",
    229: "Good idea.",
    231: "Yes, let's do that.",
    233: "There's no other choice.",
    235: "Yes, let's do that.",
    237: "That's safer.",
    252: "One day passed.",
    256: "Ah, the fog's cleared! Everyone, let's go!",
    276: "We can see it!",
    278: "There it is!",
    280: "There it is!",
    282: "There it is?",
}
STATES = {0x02, 0xD0, 0xD3, 0xFE}
EXCLUDED = {
    "DK4_MES_B323_R0038": "Packed map event 05 60 41 46 8A 80 3E 63; identical SC0B332R0038/SC1B316R0038/SC3B291R0037. Preserve unchanged.",
    "DK4_MES_B323_R0066": "Packed fog event 21 46 91 80; identical SC1B316R0066/SC3B291R0065. Preserve unchanged.",
    "DK4_MES_B323_R0106": "Packed advance event 20 46 8E 80; identical SC1B316R0106/SC3B291R0105. Preserve unchanged.",
    "DK4_MES_B323_R0179": "Packed alternate path event 94 46 8C 80; identical SC1B316R0181/SC3B291R0180. Preserve unchanged.",
}


def main() -> None:
    with (ROOT / "work/sc2/script.csv").open(encoding="utf-8-sig", newline="") as stream:
        source = {r["id"]: r for r in csv.DictReader(stream)}
    expected = {i for i in source if "_B323_" in i}
    assert expected == {f"DK4_MES_B323_R{n:04d}" for n in LINES} | set(EXCLUDED)
    records = []
    for n, text in LINES.items():
        row_id = f"DK4_MES_B323_R{n:04d}"
        raw = bytes.fromhex(source[row_id]["source_hex"])
        assert "I" not in text and "F" not in text, row_id
        assert not any(m in raw for m in (b"FI", b"FA", b"FO")), row_id
        state = raw[0] in STATES
        records.append({"id": row_id, "english": (f"{{SPEAKER:{raw[0]:02X}}}" if state else "") + text + "{PAD}", "speaker": "Lil" if raw[0] == 2 else "Companion or system", "context": "Fog exploration: map requirement, advance/wait choices, dead end, force passage or alternate path, sailors' fatigue and one-day wait.", "source_meaning": text, "source_japanese": raw[int(state):].decode("shift_jis", errors="replace"), "localization_note": "Natural English preserves all companion variants, branch choices, fatigue and one-day wait. Japanese bare leads retained as text; native states and packed events preserved.", "review": {g: True for g in ("source", "context", "localization", "naturalness", "formatting")}})
    batch = {"format": "dk4-ilnk-translation-batch-v1", "file_path": "/data/SC2.DK4", "source_file_sha256": SC2_SHA256, "encoder": "dialogue-fixed-v1", "dialogue_profile": "lil-story-deep-route-v120-live", "translation_policy": "natural-dialogue-v2", "target_locale": "en-US", "review_gates": ["source", "context", "localization", "naturalness", "formatting"], "scope": "Complete B323 fog and dead-end branches.", "inventory": {"identified_records": len(expected), "translated_records": len(records), "blocks": {"323": len(records)}}, "excluded_records": EXCLUDED, "records": records}
    (ROOT / "translations/lil_deep_route_v120.json").write_text(json.dumps(batch, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"wrote Lil V120: {len(records)} records")


if __name__ == "__main__":
    main()
