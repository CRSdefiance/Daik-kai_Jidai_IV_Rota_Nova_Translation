from __future__ import annotations

import csv
import json

from scripts.materialize_lil_deep_route_v107 import ROOT, SC2_SHA256

LINES = {
    (293, 12): "Got a map? Even for you, no going on without one. Sorry!",
    (293, 25): "Good, you brought a map.",
    (293, 46): "Admiral, we can't go on without a map.",
    (293, 47): "Admiral, we need a map to go on.",
    (293, 48): "We can't go on without a map!",
    (293, 50): "Without a map, we can't go on.",
    (293, 51): "Hey, we need a map to go on.",
    (293, 52): "We need a map to go on.",
    (293, 54): "Admiral, we need a map!",
    (293, 56): "Admiral, we can't go on without a map.",
    (293, 69): "Phew... At the top!",
    (293, 72): "We part here. Take care.",
    (293, 75): "These ruins must hold a Proof of Conqueror clue.",
    (293, 86): "Huh? Why?",
    (293, 93): "Just a feeling. That's what my gut says.",
    (293, 104): "Let's be careful. A little fear is healthy here.",
    (293, 111): "Huh? Can't see ahead...",
    (293, 128): "Admiral, fog! Take care!",
    (293, 129): "Looks like fog. Let's take care.",
    (293, 130): "Thick fog! Can't see a thing around us.",
    (293, 131): "Such thick fog! Can't tell where anyone is!",
    (293, 133): "Damn... Can't see in this fog.",
    (293, 134): "Admiral, fog. Watch your step.",
    (293, 135): "Such thick fog! Can't see a thing!",
    (293, 136): "Mist...",
    (293, 142): "Thick fog! Everything vanished so fast. {MACRO:FI}, are you all right?",
    (293, 149): "Who's in my way?! Oh... Bumped into a tree. Oww!",
    (293, 170): "What now, Admiral?",
    (293, 172): "What now?",
    (293, 174): "What now, Admiral?",
    (293, 176): "What now, Admiral?",
    (293, 178): "What now, Admiral?",
    (293, 180): "What now, Admiral?",
    (293, 186): "What now, {MACRO:FI}?",
    (293, 193): "Hmm...",
    (293, 199): "Wait",
    (293, 201): "Hurry on",
    (293, 223): "Wait here?",
    (293, 225): "So we wait here...?",
    (293, 227): "We're waiting here?",
    (293, 229): "Wait here, you mean?",
    (293, 231): "We're waiting?",
    (293, 233): "Wait, then?",
    (293, 235): "What? We're waiting? But my belly's empty!",
    (293, 236): "Ah, so we wait here.",
    (293, 242): "What, in this fog?",
    (293, 249): "We can't move in this fog! We'd get separated for sure. Don't worry, it'll clear!",
    (293, 267): "Ah, good call, Admiral!",
    (293, 268): "Good call, Admiral.",
    (293, 269): "Oh, right. Good thinking!",
    (293, 270): "Oh, right. Clever, Admiral!",
    (293, 271): "Now we get it. Good thinking!",
    (293, 272): "Of course. Good call.",
    (293, 274): "Oh! You're smart, Admiral!",
    (293, 275): "Ah, that's your plan. Good call!",
    (293, 278): "Yep.",
    (293, 284): "True. Good call... for you, {MACRO:FI}!",
    (293, 288): "All my calls are good!",
    (293, 300): "One day passed.",
    (293, 304): "Hooray, the fog's clearing! Everyone, let's go!",
    (293, 325): "Are you serious?",
    (293, 327): "Will that be safe?",
    (293, 329): "Through this fog?! Will we be safe?",
    (293, 330): "Hey, you mean it?",
    (293, 332): "Going on, really?",
    (293, 334): "R-really? Will we be safe...?",
    (293, 336): "Safe...?",
    (293, 342): "Through this fog? Will we be safe?",
    (293, 348): "We'll be fine! Let's go!",
    (293, 359): "W-wait!",
    (293, 367): "Everyone with me?",
    (293, 383): "Seems some of us got separated...",
    (293, 384): "Seems some of us got separated.",
    (293, 385): "Couldn't see... Some of us got separated.",
    (293, 386): "Some are missing... Must've got separated...",
    (293, 387): "Some got separated. Can't be helped in this fog...",
    (293, 388): "Some of us got separated, it seems.",
    (293, 389): "Um... Some are missing. Must've lost us in the fog...",
    (293, 391): "Hmm... Some of us got separated in the fog.",
    (293, 396): "Couldn't see in the fog. Some of us got separated.",
    (293, 403): "Some sailors lost!",
    (293, 415): "Oh, here?!",
    (293, 427): "Seems we're here!",
    (294, 5): "Huh? Says there's a dead end ahead.",
    (294, 8): "Sorry. A recent rockfall blocked the road to those ruins.",
    (294, 18): "Can't get to the ruins?",
    (294, 24): "So we can't reach the ruins?",
    (294, 31): "Hmm, not for a while, no.",
    (294, 35): "How long...?",
    (294, 39): "Who knows? No one goes out there. Could be ten years, or twenty...",
    (294, 51): "{MACRO:FI}, what now? We can't wait so long!",
    (294, 57): "You insist? There's a risky way: climb the cliff.",
    (294, 61): "Cliff?",
    (294, 65): "Even locals rarely dare try it.",
    (294, 69): "Then watch me climb it!",
    (294, 76): "All right, let me guide you there. Meet here, and bring a map.",
    (294, 80): "A map?",
    (294, 84): "Yes, a hidden Christian village. Don't know the path beyond the cliff. Try a Mediterranean town for a map.",
}
STATES = {0x02, 0x09, 0x14, 0x94, 0xD0, 0xD3, 0xFE}
EXCLUDED = {
    "DK4_MES_B293_R0029": "Packed guide event 46 8D 80 80 43, identical SC0 B305 R0029 and SC3 B264 R0028; preserve unchanged.",
    "DK4_MES_B293_R0109": "Packed fog event 60 46 9F 80, no Japanese prose, native event byte family; preserve unchanged.",
}


def main() -> None:
    with (ROOT / "work/sc2/script.csv").open(encoding="utf-8-sig", newline="") as stream:
        source = {row["id"]: row for row in csv.DictReader(stream)}
    expected = {i for i in source if 293 <= int(i.split("_B")[1].split("_")[0]) <= 294}
    assert expected == {f"DK4_MES_B{b}_R{n:04d}" for b, n in LINES} | set(EXCLUDED)
    records = []
    for (b, n), text in LINES.items():
        row_id = f"DK4_MES_B{b}_R{n:04d}"
        raw = bytes.fromhex(source[row_id]["source_hex"])
        has_state = raw[0] in STATES
        prose = text
        for macro in ("FI", "FA", "FO"):
            assert raw.count(macro.encode()) == text.count(f"{{MACRO:{macro}}}"), row_id
            prose = prose.replace(f"{{MACRO:{macro}}}", "")
        assert "I" not in prose and "F" not in prose, row_id
        records.append({"id": row_id, "english": (f"{{SPEAKER:{raw[0]:02X}}}" if has_state else "") + text + "{PAD}", "speaker": {2: "Lil", 9: "Kamil", 0x94: "Guide", 0xFE: "System"}.get(raw[0], "Companion variant"), "context": "Complete cliff guide and fog encounter, all companion variants, Wait/Hurry choices and outcomes, rockfall and Christian village map directions.", "source_meaning": text, "source_japanese": raw[1 if has_state else 0:].decode("shift_jis", errors="replace"), "localization_note": "Source-reviewed natural English preserves all choices, one-day waiting, lost sailors on the hurry branch, Proof clue, ten/twenty-year closure estimate, dangerous cliff and Mediterranean map lead.", "review": {g: True for g in ("source", "context", "localization", "naturalness", "formatting")}})
    batch = {"format": "dk4-ilnk-translation-batch-v1", "file_path": "/data/SC2.DK4", "source_file_sha256": SC2_SHA256, "encoder": "dialogue-fixed-v1", "dialogue_profile": "lil-story-deep-route-v110-live", "translation_policy": "natural-dialogue-v2", "target_locale": "en-US", "review_gates": ["source", "context", "localization", "naturalness", "formatting"], "scope": "Complete B293-B294 cliff and fog scenes.", "inventory": {"identified_records": len(expected), "translated_records": len(records), "blocks": {str(b): sum(bb == b for bb, _ in LINES) for b in (293, 294)}}, "excluded_records": EXCLUDED, "records": records}
    (ROOT / "translations/lil_deep_route_v110.json").write_text(json.dumps(batch, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"wrote Lil V110: {len(records)} records")


if __name__ == "__main__":
    main()
