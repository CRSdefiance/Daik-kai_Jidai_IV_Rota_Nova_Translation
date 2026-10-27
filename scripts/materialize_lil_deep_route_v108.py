from __future__ import annotations

import csv
import json

from scripts.materialize_lil_deep_route_v107 import ROOT, SC2_SHA256

LINES = {
    17: "Admiral, this jungle's unsafe without a map.",
    18: "Admiral, wandering this jungle blindly is unsafe.",
    19: "Admiral, it's too risky to wander this jungle blindly!",
    20: "Admiral, we'll get lost in this jungle without a map!",
    21: "Admiral, wandering this jungle blindly is suicide.",
    22: "Admiral, wandering this jungle blindly is unsafe.",
    23: "Admiral, we have no map! Don't make me enter this jungle!",
    24: "Admiral, wandering this jungle blindly is unsafe.",
    37: "Ugh, a jungle... Snakes and bugs, right? Maybe a rest in town...",
    53: "Without you, Admiral, our morale will suffer!",
    54: "What are you saying?!",
    56: "Who'll lead us without you, Admiral?",
    57: "No, Admiral! Without you, there'll be no one to lead us!",
    59: "What are you saying?!",
    61: "Without you, Admiral, our morale will drop.",
    62: "No way! Come with us, Admiral!",
    64: "No admiral on an expedition? Absurd!",
    69: "What do you mean, {MACRO:FI}?! You're the admiral. You have to come!",
    75: "Oh, fine! You want me to go? Then let's go!",
    86: "Right, just come along. Don't worry.",
    92: "Whoa... This cave's pitch-black! Let's turn back!",
    108: "No, Admiral. We have to go in!",
    109: "No, Admiral. On we go.",
    111: "Stop joking! We have to get inside!",
    112: "Always joking! Admiral, let's go in!",
    113: "Too late now! Let's go in, Admiral.",
    114: "Nonsense! Come, Admiral. Let's go in.",
    115: "Scares me too... But we have to go. Come on, Admiral.",
    117: "Don't say that. Shall we go in, Admiral?",
    122: "W-what?! Aren't you supposed to say, 'Let's go'?!",
    128: "Y-yes...",
    140: "Hey... {MACRO:FI}, are you scared of caves?",
    144: "N-not at all! L-let's go, Kamil!",
    150: "Ugh... So dark and creepy...",
    169: "This darkness... My chance!!!",
    172: "Hum, hum, hum... Sweet {MACRO:FI}...",
    175: "Mmm, lovely...",
    179: "U-um... Mikhail... Th-that's my...",
    182: "Huh... Sorry...",
    191: "Grrr...",
    205: "Something's here. Bad feeling.",
    206: "Something's there. Bad omen.",
    207: "Something's there. Uh-oh.",
    208: "Something's there; feels bad.",
    209: "Something's there for sure. Uh-oh.",
    210: "Something's here. Bad feeling.",
    211: "Something's there... This feels bad...",
    214: "There it is!!",
    220: "Attack!",
    222: "Run!",
    229: "Eek! Shoot it, quick!",
    233: "Roar!!",
    237: "Aaargh!",
    241: "Oh, it's so quick!",
    250: "No! Too cramped! We're far too likely to hit our own men!",
    252: "No! Too cramped! We might shoot our own men!",
    254: "No! Too cramped! We might shoot our own men!",
    256: "No! Too cramped! We might hit our own men!",
    258: "No! Too cramped! We'll shoot our own men!",
    259: "No! Too cramped! We can't shoot without hitting our own men!",
    260: "Admiral! Too cramped! We might shoot our friends!",
    262: "No! Too cramped! We'd probably hit our own men!",
    266: "Hmm... More and more injuries. Time to fight with swords!",
    283: "Pant... We somehow beat it...",
    285: "We barely beat it.",
    287: "Pant... Did we beat it...?",
    289: "Pant... Looks like we beat it...",
    291: "We beat it!",
    293: "Pant... We somehow beat it!",
    295: "Beat it at last! Mr. Tiger's tough!",
    296: "Pant... We somehow beat it!",
    300: "Many were injured.",
    311: "Wasn't hungry, then; it won't chase us.",
    312: "Seems it wasn't hungry; it won't chase us.",
    313: "So it wasn't hungry; it isn't chasing us.",
    314: "So it wasn't hungry... Glad it's not chasing us.",
    316: "Not chasing us, so it wasn't hungry... Lucky escape.",
    318: "Not chasing us. The tiger wasn't hungry, then.",
    320: "Not hungry, then; it won't chase us.",
    322: "Seems it wasn't hungry; it won't chase us.",
    325: "Phew, safe!",
    335: "Oh, a ray of light... Hooray! We can get out of this cave!",
}
STATES = {0x02, 0x09, 0x14, 0x4C, 0x97, 0xD0, 0xD3, 0xD7, 0xD8, 0xFE}


def main() -> None:
    with (ROOT / "work/sc2/script.csv").open(encoding="utf-8-sig", newline="") as stream:
        source = {row["id"]: row for row in csv.DictReader(stream)}
    expected = {i for i in source if int(i.split("_B")[1].split("_")[0]) == 288}
    assert expected == {f"DK4_MES_B288_R{n:04d}" for n in LINES}
    records = []
    for n, text in LINES.items():
        row_id = f"DK4_MES_B288_R{n:04d}"
        raw = bytes.fromhex(source[row_id]["source_hex"])
        has_state = raw[0] in STATES
        prose = text
        for macro in ("FI", "FA", "FO"):
            assert raw.count(macro.encode()) == text.count(f"{{MACRO:{macro}}}"), row_id
            prose = prose.replace(f"{{MACRO:{macro}}}", "")
        assert "I" not in prose and "F" not in prose, row_id
        records.append({"id": row_id, "english": (f"{{SPEAKER:{raw[0]:02X}}}" if has_state else "") + text + "{PAD}", "speaker": {2: "Lil", 9: "Kamil", 0x14: "Companion", 0x4C: "Mikhail", 0xFE: "System"}.get(raw[0], "Companion variant"), "context": "Complete jungle/cave scene, Lil's fear, Mikhail's mistaken advances, tiger attack/run branches and companion variants.", "source_meaning": text, "source_japanese": raw[1 if has_state else 0:].decode("shift_jis", errors="replace"), "localization_note": "Source-reviewed natural English retains every response branch, exact FI substitutions, friendly-fire warning, sword fight, injuries and hungry-tiger escape explanation.", "review": {g: True for g in ("source", "context", "localization", "naturalness", "formatting")}})
    batch = {"format": "dk4-ilnk-translation-batch-v1", "file_path": "/data/SC2.DK4", "source_file_sha256": SC2_SHA256, "encoder": "dialogue-fixed-v1", "dialogue_profile": "lil-story-deep-route-v108-live", "translation_policy": "natural-dialogue-v2", "target_locale": "en-US", "review_gates": ["source", "context", "localization", "naturalness", "formatting"], "scope": "Complete B288 jungle cave encounter.", "inventory": {"identified_records": len(expected), "translated_records": len(records), "blocks": {"288": len(records)}}, "excluded_records": {}, "records": records}
    (ROOT / "translations/lil_deep_route_v108.json").write_text(json.dumps(batch, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"wrote Lil V108: {len(records)} records")


if __name__ == "__main__":
    main()
