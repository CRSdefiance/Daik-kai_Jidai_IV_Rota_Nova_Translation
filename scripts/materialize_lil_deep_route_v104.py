from __future__ import annotations

import csv
import json
from pathlib import Path

from scripts.materialize_lil_deep_route_v101 import SC2_SHA256

ROOT = Path(__file__).resolve().parents[1]
LINES = {
    (239, 5): "Welcome!",
    (239, 9): "Hey, dear! Customers!",
    (239, 12): "Yes...",
    (239, 16): "Crying forever won't help. Give it up already.",
    (239, 24): "What's wrong?",
    (239, 27): "Oh, nothing you need worry about. Just enjoy your drink.",
    (239, 40): "You look so sad. What's troubling you?",
    (239, 43): "Um... You sail to towns all over the world, right?",
    (239, 47): "Yes, we do.",
    (239, 51): "Ever been to the New World?",
    (239, 57): "Yes",
    (239, 59): "No",
    (239, 67): "Yes. But why?",
    (239, 73): "The New World? We haven't sailed that far yet...",
    (239, 77): "But we will someday! Why do you ask?",
    (239, 83): "Well... Someone stole a treasure dear to me.",
    (239, 87): "Treasure?",
    (239, 91): "Maybe it's not worth much, but Papa gave it to me for my birthday. He knows how much roses mean to me.",
    (239, 94): "Like a real rose frozen in ice. A lovely glass ornament... So dear to me.",
    (239, 98): "Who stole it?",
    (239, 102): "No idea.",
    (239, 106): "Then we can't find the thief... So why did you ask about the New World?",
    (239, 110): "A friend's acquaintance heard of a Havana swindler who sells glass as costly jade or crystal.",
    (239, 113): "A swindler? Hmm. Hard to say whether he's your thief...",
    (239, 117): "But she's in trouble. Maybe he's not involved, but let's go to Havana anyway.",
    (239, 121): "We might learn something there.",
    (239, 125): "Yes. That's the only lead we've got.",
    (239, 129): "He might sell it soon if he's the thief. Let's hurry!",
    (239, 133): "Oh, thank you!",
    (239, 137): "Wait for us! We'll find it!",
    (240, 6): "Sir, you must settle up today. Do you even remember how much you've put on your tab?",
    (240, 9): "Told you, next time for sure! Ever known me to skip a bill?",
    (240, 13): "Never known you to pay one.",
    (240, 17): "Tch! All right. Take this for the drinks.",
    (240, 21): "What's this?",
    (240, 25): "Amethyst piece.",
    (240, 29): "Oh! Looks expensive! Are you sure?",
    (240, 33): "Worth quite a bit, but call it interest. Keep the change! Hahaha!",
    (240, 36): "Hold it right there!",
    (240, 41): "Huh? Who are you?",
    (240, 44): "You won't get away with selling a fake!",
    (240, 47): "W-what?! Stay out of this! Get lost, brat!",
    (240, 51): "Don't let him fool you, sir! That thing is made of glass!",
    (240, 55): "What? G-glass?!",
    (240, 59): "W-what are you saying?! This is genuine...",
    (240, 62): "Still playing innocent? The real owner sent me! You can't fool me!",
    (240, 65): "Tch! The game's up! Time to leave! Urgh!",
    (240, 69): "You... Been patient since you're a customer. But that's enough!",
    (240, 73): "Move, old man, unless you want to get hurt!",
    (240, 76): "Dealing with rough sailors every day takes muscle! You think you're a match for me?",
    (240, 79): "Urgh!!",
    (240, 83): "How dare you pull that filth in my tavern!",
    (240, 86): "Gah!",
    (240, 90): "Eek! H-have mercy!",
    (240, 102): "Wow... strong.",
    (240, 109): "D-damn! You'll pay for this!",
    (240, 112): "Hey! Stop! Tch, he got away.",
    (240, 115): "Thanks, you two! He nearly fooled me completely. You came looking for this, right?",
    (240, 120): "Take it to its owner. He's bound to be up to other crimes too. Next time, he'll go straight to the governor!",
    (241, 6): "Oh, welcome!",
    (241, 10): "Look! We got it back!",
    (241, 14): "Oh! You found it! Thank you so much!",
    (241, 18): "Returned the frozen rose.",
    (241, 27): "Thought it was gone for good... But you found it! Thanks to you!",
    (241, 31): "No trouble. Bye!",
    (241, 41): "Oh, wait!",
    (241, 45): "You explore places all over the world, right?",
    (241, 48): "There's a wooden church outside town, rare in Europe. Why not visit it?",
    (241, 53): "Sounds fun! We'll go!",
    (241, 61): "Thank you so much! Come again!",
    (242, 6): "Boss!",
    (242, 10): "What's up?",
    (242, 14): "Look! What a fine figurehead!",
    (242, 17): "Well done finding it.",
    (242, 21): "Oh, Padre!",
    (242, 25): "Such a stately figure. Any story behind it?",
    (242, 28): "No particular story. But...",
    (242, 31): "But?",
    (242, 35): "Only someone the statue itself favors can take it away.",
    (242, 39): "Several people have tried. Most leave empty-handed, with injuries to show for it.",
    (242, 43): "And when its owner dies, the statue somehow returns to this church.",
    (242, 47): "Oh! How mysterious.",
    (242, 50): "Would you like to try?",
    (242, 54): "Ha! No thanks! Don't want anything that strange! Right, Admiral?",
    (242, 58): "Hmm...",
    (242, 62): "Surely not, Boss!",
    (242, 68): "Try it",
    (242, 70): "Leave it",
    (242, 77): "Come on! Lend a hand!",
    (242, 81): "No! Leave it alone!",
    (242, 85): "Leave it to us. You can head back first.",
    (242, 88): "All right! Let me help! Happy now? Honestly!",
    (242, 92): "Heave! Heave! Heave!",
    (242, 111): "Aah!",
    (242, 123): "Run for it!",
    (242, 130): "Seems you were not worthy of it.",
    (242, 134): "Ow, ow...",
    (242, 140): "The statue seems to have accepted you.",
    (242, 143): "Just good luck.",
    (242, 147): "No need for such modesty.",
    (242, 151): "No, really. Just good luck.",
    (242, 156): "Either way, all is well. May God grant you his protection.",
    (242, 161): "{MACRO:FI}'s Spirit rose by 1!",
    (242, 172): "A wise choice.",
    (242, 176): "Yes! Had me worried you were going to take it!",
    (242, 180): "May God grant you his protection.",
    (243, 6): "Oh, you've come back!",
    (243, 10): "Ever seen golden sand?",
    (243, 14): "Gold?",
    (243, 18): "A New World sailor told me of a river there with golden sand flowing through it.",
    (243, 22): "Just picturing it... Doesn't it sound romantic?",
    (244, 7): "Oh, {MACRO:FI}!",
    (244, 11): "Do you like ancient cultures too? There are ruins here.",
    (244, 14): "Didn't know? They're close by. On that hill you can see from here.",
    (245, 7): "Been to the pyramids yet?",
    (245, 11): "No.",
    (245, 15): "You must see them while you're here! Let me show you the way. Go on!",
    (245, 18): "Yes. Thanks!",
    (246, 6): "Welcome, {MACRO:FI}! Lovely weather today.",
    (246, 10): "Oh, have you visited the ruins near town? Some say they were King Solomon's treasury.",
    (246, 13): "Hmm.",
    (246, 17): "Perfect weather for a picnic! Why not take a little trip?",
    (247, 5): "Got a job for you.",
    (247, 9): "The village of Lebaque lies far east across the ocean. Send an expedition there to investigate it for me.",
    (247, 12): "A survey?",
    (247, 20): "East across the ocean south of Asia... South of Southeast Asia?! That's so far!",
    (247, 24): "That's why we're asking you.",
    (247, 28): "The survey will cost money, so bring a little extra.",
    (248, 12): "Um... Lebaque village was south of Southeast Asia, right?",
    (248, 18): "How's the Lebaque survey? Across the ocean south of Asia, far east of here.",
    (249, 5): "Thanks! Your expenses and reward. Take them.",
    (249, 9): "Received 42,000 gold coins.",
    (249, 33): "Share in Sofala rose a little!",
    (249, 51): "Have you visited the ruins near town?",
    (249, 54): "Legend says they were King Solomon's treasury. Why not visit?",
}
BARE = {(239, 57), (239, 59), (242, 68), (242, 70)}
EXCLUDED = {"DK4_MES_B242_R0097": "Packed two-byte figurehead challenge control (94 40), identical to SC0 B254 R0104, SC1 B243 R0100 and SC3 B215 R0099; preserved unchanged."}
SPEAKERS = {0x02: "Lil", 0x06: "Gerald", 0x09: "Kamil", 0x43: "Swindler", 0x5C: "Tavern keeper", 0x8B: "Priest", 0x93: "Guild master", 0xBA: "Francesca", 0xBC: "Tavern woman", 0xC1: "Tavern woman", 0xC3: "Tavern woman", 0xC4: "Tavern woman", 0xFE: "System"}
CONTEXT = {239: "Francesca's stolen Frozen Rose and both New World visit choices.", 240: "Havana glass swindler confrontation and the tavern keeper's rescue.", 241: "Frozen Rose returned; wooden church discovery clue.", 242: "Supernatural figurehead challenge, all choices, failure and success branches and Spirit reward.", 243: "New World golden river clue.", 244: "Hilltop ancient ruins clue.", 245: "Pyramid directions.", 246: "Solomon's treasury ruins clue.", 247: "Guild survey request for Lebaque village.", 248: "Lebaque survey reminder variants.", 249: "Survey reward, Sofala share gain and ruins clue."}


def main() -> None:
    with (ROOT / "work/sc2/script.csv").open(encoding="utf-8-sig", newline="") as stream:
        source = {row["id"]: row for row in csv.DictReader(stream)}
    expected = {i for i in source if 239 <= int(i.split("_B")[1].split("_")[0]) <= 249}
    assert expected == {f"DK4_MES_B{b}_R{n:04d}" for b, n in LINES} | set(EXCLUDED)
    assert source["DK4_MES_B242_R0097"]["source_hex"].lower() == "9440"
    records = []
    for (b, n), text in LINES.items():
        row_id = f"DK4_MES_B{b}_R{n:04d}"
        raw = bytes.fromhex(source[row_id]["source_hex"])
        state = None if (b, n) in BARE else raw[0]
        assert state is None or state in SPEAKERS
        prose = text
        for macro in ("FI", "FA", "FO"):
            assert raw.count(macro.encode()) == text.count(f"{{MACRO:{macro}}}")
            prose = prose.replace(f"{{MACRO:{macro}}}", "")
        assert "I" not in prose and "F" not in prose, row_id
        records.append({"id": row_id, "english": ("" if state is None else f"{{SPEAKER:{state:02X}}}") + text + "{PAD}", "speaker": SPEAKERS.get(state, "Bare choice"), "context": CONTEXT[b], "source_meaning": text, "source_japanese": raw[int(state is not None):].decode("shift_jis", errors="replace"), "localization_note": "Source-reviewed natural English preserves all choices, rewards, locations and macros. Epithets and phrasing avoid literal capital F/I renderer control bytes.", "review": {g: True for g in ("source", "context", "localization", "naturalness", "formatting")}})
    batch = {"format": "dk4-ilnk-translation-batch-v1", "file_path": "/data/SC2.DK4", "source_file_sha256": SC2_SHA256, "encoder": "dialogue-fixed-v1", "dialogue_profile": "lil-story-deep-route-v104-live", "translation_policy": "natural-dialogue-v2", "target_locale": "en-US", "review_gates": ["source", "context", "localization", "naturalness", "formatting"], "scope": "All B239-B249 rose, figurehead, ruin and survey events.", "inventory": {"identified_records": len(expected), "translated_records": len(records), "blocks": {str(b): sum(bb == b for bb, _ in LINES) for b in CONTEXT}}, "excluded_records": EXCLUDED, "records": records}
    (ROOT / "translations/lil_deep_route_v104.json").write_text(json.dumps(batch, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"wrote Lil V104: {len(records)} records, {len(EXCLUDED)} exclusions")


if __name__ == "__main__":
    main()
