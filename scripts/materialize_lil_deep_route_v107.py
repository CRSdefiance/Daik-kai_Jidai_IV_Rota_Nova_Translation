from __future__ import annotations

import csv
import json
from pathlib import Path

from scripts.materialize_lil_deep_route_v101 import SC2_SHA256

ROOT = Path(__file__).resolve().parents[1]
LINES = {
    (283, 21): "Admiral, we'll get lost without a map.",
    (283, 22): "Admiral, we need a map or we'll get lost.",
    (283, 23): "Admiral, we'll get lost without a map!",
    (283, 24): "Admiral, no map means getting lost.",
    (283, 25): "Admiral, we'll lose our way without a map.",
    (283, 26): "Admiral, we need a map! We'll get lost!",
    (283, 27): "Admiral, we risk getting lost without a map.",
    (283, 49): "What a dense forest. Let's proceed carefully.",
    (283, 50): "This forest is dense. We must take care.",
    (283, 51): "So dark... This feels a bit creepy.",
    (283, 52): "Such a dense forest. Hope we don't get lost.",
    (283, 53): "This forest gives me a bad feeling.",
    (283, 55): "Careful now. Let's watch our step.",
    (283, 57): "Hope we find something nice!",
    (283, 59): "A dense forest indeed. Hope nothing jumps out at us...",
    (283, 62): "Come on, let's go!",
    (283, 79): "A-Admiral, behind you...",
    (283, 81): "Admiral, don't move! Behind you...",
    (283, 82): "A-Admiral, behind you...",
    (283, 84): "Eek... B-behind you...",
    (283, 86): "Hm! Admiral, behind you...",
    (283, 88): "Whoa... B-behind you...",
    (283, 96): "Look out!",
    (283, 103): "Battle",
    (283, 105): "Play dead",
    (283, 107): "Other",
    (283, 118): "Shoot it!",
    (283, 136): "Oh, it's running away!",
    (283, 138): "The bear ran away!",
    (283, 140): "Oh, it's running away!",
    (283, 142): "Oh! Off it goes!",
    (283, 144): "Hooray, it's gone!",
    (283, 148): "Some sailors suffered minor injuries.",
    (283, 161): "A-Admiral... That bear shows no sign of leaving.",
    (283, 163): "Admiral... That bear isn't about to leave.",
    (283, 165): "No good. That bear won't budge!",
    (283, 166): "A-Admiral... No good. This bear isn't moving.",
    (283, 167): "A-Admiral... No good. That damn bear won't leave.",
    (283, 168): "This won't do. The bear shows no sign of leaving.",
    (283, 170): "A-Admiral... Mr. Bear doesn't want to go home.",
    (283, 171): "Hmm... That bear seems intent on staying put.",
    (283, 175): "Shh! Stay still!",
    (283, 196): "Phew... Has it finally given up?",
    (283, 198): "Phew... The bear finally gave up.",
    (283, 200): "Phew... The damn thing finally gave up.",
    (283, 202): "Zzz...",
    (283, 214): "Huh? Where's Emilio?",
    (283, 218): "Zzz...",
    (283, 222): "We said to play dead, and he really fell asleep... Unbelievable.",
    (283, 232): "One day passed.",
    (283, 239): "Scare it off",
    (283, 241): "Run away",
    (283, 256): "We tried scaring it, but it won't run!",
    (283, 258): "Even our threats won't scare it off...",
    (283, 260): "What's with this thing?! We threatened it, but it won't run!",
    (283, 261): "Such a bold beast! Our threats won't scare it off!",
    (283, 262): "Whoa! This bear has guts! Won't run!",
    (283, 263): "Hey! We threatened it, but it won't run! What's going on?!",
    (283, 265): "Huh? We scared it, but it won't leave!",
    (283, 266): "Our threats won't scare it off... A bold beast indeed.",
    (283, 277): "This is bad, Admiral! Could it be a man-eater?! Provoke it and we'll be in danger!",
    (283, 288): "Admiral, look out! Damn... Our men were attacked! We must flee before it gets us too!",
    (283, 289): "Look out! Oh no... Our men were attacked! Let's flee! We're in danger!",
    (283, 290): "Admiral, look out! Our men were attacked! Give up and run!",
    (283, 292): "Admiral, look out! Our men are under attack! We'd better run now!",
    (283, 294): "Look out!! Damn, are some of our men hurt?! We'd better run!",
    (283, 296): "Look out! Admiral, we'd better run!!",
    (283, 297): "Look out! Let's run!!",
    (283, 299): "This is bad. Admiral, we'd better run!",
    (283, 304): "The sailors are much more fatigued. Some appear to be injured.",
    (283, 312): "Run!!",
    (283, 328): "We somehow managed to escape...",
    (283, 330): "Phew... We managed to escape...",
    (283, 332): "Pant... pant... Looks like we're safe...",
    (283, 333): "Looks like we're safe...",
    (283, 335): "Phew... Did we lose it?",
    (283, 336): "Pant... pant... That was so scary...",
    (283, 337): "Oh, out of breath... Everyone seems safe. Thank goodness.",
    (283, 351): "Admiral, we're out of the forest! We've reached the ruins.",
    (283, 352): "Admiral, we're out of the forest. So these are the ruins...",
    (283, 353): "At last, we're out of the forest... Oh! Admiral, are these the ruins?",
    (283, 355): "At last, we're out of the forest. So these... are the ruins.",
    (283, 356): "Oh! Admiral! We're out of the forest!! Yes, those are the ruins!",
    (283, 357): "Ah, we're out of the forest. Hmm... Could those be the ruins?",
    (283, 359): "Hooray, we're out of the forest! Lots of strange stones over there... Are those the ruins?",
    (283, 361): "Admiral, we're out of the forest. Oh... So these are the ruins...",
    (284, 6): "There you are! You're {MACRO:FA}, right? London's guild is looking for you.",
    (285, 5): "Glad you came. Got a little job for you.",
    (285, 9): "Deliver 200 barrels of wine to this town's market. That's two cargo holds' worth.",
    (285, 13): "They've had several big orders lately and can't keep up. Collect your reward at the market.",
    (286, 13): "Oh, right. We must deliver two holds of wine to London's market.",
    (286, 18): "Come on, hurry and deliver the wine to the market.",
    (287, 5): "Oh, you've brought the goods?",
    (287, 9): "Thanks. Here's your reward.",
    (287, 13): "Received 8,000 gold coins.",
    (287, 41): "Share in London rose a little!",
    (287, 52): "Does wine sell well here?",
    (287, 55): "Some odd folks have been holding what looks like a festival around the ruins. They buy heaps of wine.",
    (287, 58): "Where are those ruins?",
    (287, 62): "A little way from town. With a map, you should get there easily.",
    (287, 73): "They bought every map in town. Heard Amsterdam still has some, though...",
    (287, 78): "A map? This one?",
    (287, 83): "Yes, that's it! Don't tell me you're one of them, miss...",
    (287, 86): "Of course you aren't! Ha ha ha!",
}
LINES.update({
    (283, 22): "No map? We'll get lost.",
    (283, 23): "Admiral, no map? We'll get lost!",
    (283, 25): "Admiral, no map means getting lost.",
    (283, 27): "We'll get lost without a map.",
    (283, 49): "A dense forest. Let's be careful.",
    (283, 50): "A dense forest. We must take care.",
    (283, 51): "So dark... feels creepy.",
    (283, 52): "A dense forest. Hope we don't get lost!",
    (283, 53): "This forest feels wrong.",
    (283, 55): "Careful. Watch your step.",
    (283, 59): "A dense forest. Hope nothing jumps out...",
    (283, 62): "Let's go!",
    (283, 79): "B-behind you!",
    (283, 82): "B-behind you!",
    (283, 86): "Hm! Behind you!",
    (283, 88): "Whoa... Behind you!",
    (283, 148): "Sailors slightly injured.",
    (283, 167): "Admiral... No good. That damn bear won't leave.",
    (283, 170): "Admiral... Mr. Bear doesn't want to go home.",
    (283, 196): "Phew... it gave up.",
    (283, 198): "Phew... it gave up.",
    (283, 200): "Phew... it finally gave up.",
    (283, 222): "We said play dead. He's asleep... Unbelievable.",
    (283, 256): "Our threats won't scare it!",
    (283, 258): "Threats won't scare it!",
    (283, 260): "What's with it?! Threats won't scare it!",
    (283, 261): "So bold! Threats won't scare it!",
    (283, 265): "Huh? Our threats won't scare it!",
    (283, 266): "Threats won't scare it. A bold beast!",
    (283, 288): "Admiral, look out! Damn... Our men were attacked! Run before it gets us too!",
    (283, 299): "Bad news. Admiral, we'd better run!",
    (283, 304): "Sailors are much more fatigued. Some are injured.",
    (283, 328): "We somehow escaped...",
    (283, 332): "Pant... Looks like we're safe.",
    (283, 333): "Seems we're safe...",
    (283, 335): "Phew... We lost it?",
    (283, 336): "Pant... That was so scary...",
    (283, 337): "Out of breath... All safe. Thank goodness.",
    (283, 351): "Out of the forest! The ruins, Admiral!",
    (283, 352): "We're out! Are these the ruins?",
    (283, 353): "Out of the forest at last! Oh! Admiral, are these the ruins?",
    (283, 355): "Out of the forest at last. The ruins...",
    (283, 356): "Admiral! Out of the forest!! Yes, those are the ruins!",
    (283, 357): "Ah, out of the forest. Hmm... Are those the ruins?",
    (283, 359): "Hooray, out of the forest! Lots of strange stones there... Are those the ruins?",
    (283, 361): "We're out! Oh... These are the ruins.",
    (285, 13): "Big orders lately, and they can't keep up. Collect your reward at the market.",
    (286, 13): "Oh, right. Two holds of wine for London's market.",
    (286, 18): "Come on, deliver the wine to the market!",
    (287, 9): "Thanks. Your reward.",
    (287, 55): "Some odd folks hold what looks like a festival around the ruins. They buy heaps of wine.",
    (287, 83): "Yes, that's it! Are you one of them, miss...?",
})
STATES = {0x02, 0x0E, 0x16, 0x68, 0x71, 0x93, 0xD0, 0xD3, 0xD7, 0xD8, 0xFE}
EXCLUDED = {"DK4_MES_B283_R0038": "Packed forest event 05 60 40 46 8A 80 3E 63; identical SC0 B293 R0038, SC1 B290 R0038 and SC3 B252 R0037; preserve unchanged."}


def main() -> None:
    with (ROOT / "work/sc2/script.csv").open(encoding="utf-8-sig", newline="") as stream:
        source = {row["id"]: row for row in csv.DictReader(stream)}
    expected = {i for i in source if 283 <= int(i.split("_B")[1].split("_")[0]) <= 287}
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
        records.append({"id": row_id, "english": (f"{{SPEAKER:{raw[0]:02X}}}" if has_state else "") + text + "{PAD}", "speaker": "Lil" if raw[0] == 2 else "System" if raw[0] == 0xFE else "Companion or NPC" if has_state else "Variant dialogue or choice", "context": "Complete forest bear encounter, all choices and companion variants; London wine delivery and ruin-map lead.", "source_meaning": text, "source_japanese": raw[1 if has_state else 0:].decode("shift_jis", errors="replace"), "localization_note": "Source-reviewed natural English retains all branch actions, injuries, one-day delay, 200-barrel/two-hold delivery, 8,000-gold reward and Amsterdam map lead. Bare variants retain their first English glyph.", "review": {g: True for g in ("source", "context", "localization", "naturalness", "formatting")}})
    batch = {"format": "dk4-ilnk-translation-batch-v1", "file_path": "/data/SC2.DK4", "source_file_sha256": SC2_SHA256, "encoder": "dialogue-fixed-v1", "dialogue_profile": "lil-story-deep-route-v107-live", "translation_policy": "natural-dialogue-v2", "target_locale": "en-US", "review_gates": ["source", "context", "localization", "naturalness", "formatting"], "scope": "Complete B283-B287 forest and London delivery scenes.", "inventory": {"identified_records": len(expected), "translated_records": len(records), "blocks": {str(b): sum(bb == b for bb, _ in LINES) for b in range(283, 288)}}, "excluded_records": EXCLUDED, "records": records}
    (ROOT / "translations/lil_deep_route_v107.json").write_text(json.dumps(batch, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"wrote Lil V107: {len(records)} records")


if __name__ == "__main__":
    main()
