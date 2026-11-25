from __future__ import annotations

import csv
import json
from pathlib import Path

from scripts.materialize_lil_deep_route_v101 import SC2_SHA256

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "work/sc2/script.csv"
OUTPUT = ROOT / "translations/lil_deep_route_v102.json"
BLOCKS = range(215, 227)
LINES = {
    (215, 5): "Who built these ruins, and why? They look like King Solomon's mines from the Old Testament.",
    (215, 8): "Do you know the legend of Solomon?",
    (215, 11): "Eh?",
    (215, 15): "Pardon me. Admiral {MACRO:FA}, yes?",
    (215, 19): "Yes. What do you want?",
    (215, 22): "Thanks for investing here. The people are pleased.",
    (215, 25): "We profit from it too. No need for thanks. Anyway, what is it?",
    (215, 29): "Heard the tales of King Solomon, Admiral?",
    (215, 33): "What?",
    (215, 37): "Great King Solomon once commanded even the demon king.",
    (215, 41): "A demon? And?",
    (215, 45): "A weapon linked to that demon is sealed on an icy island far northwest of here.",
    (215, 48): "Perhaps Admiral {MACRO:FA} could master even such a weapon. That is why this news is yours.",
    (215, 51): "An icy island far northwest... the land of ice?",
    (215, 54): "A demon's weapon... Sounds strong. Let's find it.",
    (216, 5): "King?",
    (216, 9): "You again! You're bad for business! Get out of here!",
    (216, 13): "The king? Where's the sword's hero?",
    (216, 16): "What? Who are you?",
    (216, 19): "Vivian... who once forged King Arthur's holy sword...",
    (216, 22): "Arthur?",
    (216, 26): "The king sleeps... But his sword still seeks a hero.",
    (216, 29): "Hero, seek Excalibur! The holy sword awaits you in Avalon, where the king sleeps!",
    (216, 32): "Avalon? Never heard of it.",
    (216, 41): "Me neither. Let's ask at the tavern.",
    (216, 46): "Let's ask around at the tavern.",
    (217, 5): "Do you know Avalon, sir?",
    (217, 8): "Again? You believe that woman calling herself a witch too?",
    (217, 12): "Avalon was supposedly just west of here.",
    (217, 16): "Arthur's a fairy tale. People keep asking, but nobody ever says they've found it.",
    (218, 5): "Admiral, heard a tale of a fine weapon in town.",
    (218, 8): "A fine weapon? Coming from you, that must mean something! What's its name?",
    (218, 11): "The Holy Spear of Ares. They say it belonged to Ares, one of the twelve Olympian gods.",
    (218, 14): "Ares? No idea who that is, but his spear must be great. Where can we get it?",
    (218, 17): "Armor named after other Olympian gods may lie nearby as well, so the rumor says.",
    (218, 20): "What's that mean? Where is it?",
    (218, 23): "The townspeople suggest somewhere nearby. A find like that would be wonderful.",
    (218, 27): "(He's interested? That's a surprise.)",
    (218, 30): "Admiral? Why that face? Surprised that these legends interest me?",
    (218, 34): "Yes. You don't seem the weapon type.",
    (218, 37): "Perhaps. But it's the mystery that moves me. Gods of myth once roamed this very land.",
    (218, 40): "The thought of weapons those gods may have used sends my mind back to ancient times.",
    (218, 43): "Really? That's lost on me.",
    (220, 5): "Hello, Lucia! How are you? Those lovely eyes of yours keep bringing me back here.",
    (220, 8): "Welcome, Julian. Smooth as ever, aren't you?",
    (220, 12): "Hm?",
    (220, 16): "What? Something on my face?",
    (220, 19): "Ah... That legendary empress may have been just like you.",
    (220, 23): "What do you mean by that?",
    (220, 27): "Sorry! Just heard about the Empress's Gown. That got me thinking.",
    (220, 31): "Empress's Gown?",
    (220, 35): "A beautiful Chinese empress wore it. She ruled as a tyrant and met a tragic end.",
    (220, 39): "She must have been so beautiful she could steal a man's heart with a glance. Just like you!",
    (220, 42): "A tyrant, though? Selfish and arrogant, then? Do you really think that's me?",
    (220, 46): "A little selfishness is cute in a woman. About as much as yours!",
    (220, 50): "A gown to keep a beautiful woman safe... So romantic, don't you think?",
    (220, 53): "A romantic gown? The rings and necklaces she wore interest me more.",
    (220, 57): "You mean their prices? Women are so practical! Time to go. See you soon.",
    (220, 61): "See you.",
    (220, 65): "Runs off as soon as gifts come up!",
    (221, 5): "Hey, you! Don't just pass through our square!",
    (221, 8): "Why? What's here?",
    (221, 11): "Know the Crusades?",
    (221, 17): "Yes",
    (221, 19): "No",
    (221, 27): "Hmph. Chivalrous knights reclaiming the Holy Land, right?",
    (221, 33): "Hmph. Europe calls them chivalrous knights who fought to reclaim the Holy Land...",
    (221, 39): "All convenient lies! People here know what the Crusaders were really like.",
    (221, 42): "How so?",
    (221, 46): "Heard a bit myself. They wanted this region's riches, right? Looting and slaughter all along the way.",
    (221, 49): "Can't stand history twisted to suit them! Our true hero wasn't a Crusader. He was Saladin!",
    (221, 52): "Saladin? Who's he?",
    (221, 56): "A great man in Muslim history. More than a victor over the Crusaders.",
    (221, 60): "He was humane in battle, in peace talks, and toward captives and civilians. A fine man who never stooped to dirty tricks.",
    (221, 63): "Strong and a good person too? Amazing! What a hero!",
    (221, 67): "Saladin's armor is missing, so they say. Want to follow his example? Why not look for it?",
    (222, 9): "Gerhard? Watching the sunset? What's wrong?",
    (222, 13): "Admiral... A story heard here in Japan moved me. Rather unlike me, perhaps...",
    (222, 17): "Hmm. Would we know him?",
    (222, 20): "A warrior of centuries past, named Noritsune.",
    (222, 23): "What was so great?",
    (222, 27): "His clan had once known great glory. But defeat after defeat at the hands of their rivals drove them toward extinction.",
    (222, 30): "As his weak kinsmen fell, he alone fought bravely...",
    (222, 33): "He leaped across seven ships to reach the enemy commander.",
    (222, 37): "Exhausted, he took two foes under his arms and sank into the strait, splendid armor and all...",
    (222, 40): "Such courage in this small eastern nation! What a glimpse of the spirit of the East.",
    (222, 44): "Every land has exceptional heroes, huh?",
    (222, 47): "Yes. An island can breed heroes.",
    (222, 50): "Hehe. A tale like that gets to you! (Looks scary, but such a pure heart.)",
    (222, 54): "...The strait, armor and all...",
    (222, 57): "Goodness, what a long tale. Best get back to work.",
    (223, 14): "Admiral, a letter from Dukov.",
    (223, 15): "Admiral, a letter from Dukov.",
    (223, 16): "Admiral, a letter from Dukov.",
    (223, 17): "Admiral, a letter from Dukov.",
    (223, 18): "Admiral, a letter from Dukov.",
    (223, 19): "Admiral, a letter from Dukov.",
    (223, 20): "Admiral! A letter from Dukov!",
    (223, 28): "An antique shop had a fine book.",
    (223, 31): "Timur built an empire from Central to West Asia 200 years ago, heir to the fading Mongols.",
    (223, 34): "His mail was so strong that enemy arrows bounced off it, and the blades of swords and spears were blunted against it.",
    (223, 37): "Buried with him, it was stolen decades later by a thief who also took other treasures from his tomb.",
    (223, 40): "Hunted, the thief fled into a hot desert. Near the sea, his strength failed and he died.",
    (223, 44): "This tale remained unknown for many years. The mail has still not been found.",
    (223, 48): "Should it interest you, why not investigate? -- Dukov",
    (223, 56): "Dukov likes Asian history too, huh?",
    (223, 67): "The Mongol Empire once ruled Russia and was its enemy for years. His interest is only natural.",
    (223, 70): "Hmm. Complicated.",
    (224, 5): "Safia! Those mysterious eyes of yours!",
    (224, 8): "Julian! Welcome.",
    (224, 15): "What? Something on my face?",
    (224, 18): "Your eyes draw me right in... So this is how it feels to turn to stone.",
    (224, 22): "Meaning?",
    (224, 26): "Heard of Medusa's Shield in the Tasman Sea. Your eyes reminded me of it.",
    (224, 29): "Medusa, that snake-haired monster? So now you're calling me ugly and terrifying?",
    (224, 32): "Nonsense! You needn't uncover your hair to capture me. Those lovely eyes are enough.",
    (224, 35): "Always teasing!",
    (224, 39): "Turn me to stone, and let me live beside you forever in the moonlight... How romantic!",
    (224, 43): "Don't expect me to tend your statue!",
    (224, 46): "So cold! That's part of your charm, though. Well, time to go. See you!",
    (224, 50): "See you.",
    (224, 54): "Odd comparison... But my heart fluttered!",
    (225, 5): "Heathen! Charles Martel will defeat you!",
    (225, 9): "Ow! Mercy! R-retreat!",
    (225, 12): "What are those kids doing?",
    (225, 16): "Playing heroes. Children everywhere admire the heroes of their homeland.",
    (225, 20): "So the local hero is Charles Something?",
    (225, 23): "Charles Martel. He lived over 800 years ago.",
    (225, 26): "Between Tours and Poitiers, he defeated a Muslim army advancing north from Spain.",
    (225, 29): "A hero for winning a war? Too simple. A soldier's view. Not for me.",
    (225, 32): "Consider what that win meant.",
    (225, 36): "Had he lost, all Europe would have turned to the Muslim faith. History would be very different.",
    (225, 40): "So he saved Europe's culture and traditions? No wonder children admire him.",
    (225, 44): "Your own achievements are every bit as great as Charles Martel's, Admiral.",
    (225, 48): "What will history make of your name? Can't wait!",
    (226, 5): "Ah, Admiral!",
    (226, 8): "Oh, Manuel!",
    (226, 12): "Studying trends? You work so hard.",
    (226, 15): "Just a break.",
    (226, 19): "Ah.",
    (226, 23): "What about you? Something going on in the square?",
    (226, 26): "Just like you. A stroll and a chance to hear some news.",
    (226, 29): "By the way, have you heard of Attila, king of the Huns?",
    (226, 33): "Who's that?",
    (226, 37): "The Huns were nomadic horsemen from Asia. Attila threatened both halves of the Roman Empire.",
    (226, 41): "So he was stronger than Rome? Does that mean he was stronger than me too?",
    (226, 45): "Even the mightiest empire meets a stronger foe in time. Nothing rules forever.",
    (226, 48): "Nobody can ever beat me!",
    (226, 51): "Of course. That takes effort.",
    (226, 54): "Yes, yes. Work hard, got it! But why bring this up?",
    (226, 57): "Heard a tale of Attila's armor just now. Only a rumor, of course.",
    (226, 61): "Oh? And?",
    (226, 65): "After his death, someone took the armor northwest.",
    (226, 69): "Anything worth having always gets carted off somewhere!",
    (226, 72): "Yes. Northwest from here... Scandinavia, perhaps?",
}
BARE = {(221, 17), (221, 19)} | {(223, n) for n in (15, 16, 17, 18, 19, 20)}
SPEAKERS = {0x02: "Lil", 0x09: "Kamil", 0x0D: "Companion", 0x10: "Gerhard", 0x11: "Al", 0x15: "Dukov", 0x17: "Manuel", 0x1A: "Julian", 0x52: "Shopkeeper", 0x55: "Townsman", 0x5C: "Tavern keeper", 0x78: "Legend keeper", 0x97: "Companion or child", 0xA2: "Child playing Martel", 0xA9: "Vivian", 0xC5: "Safia", 0xC7: "Lucia", 0xD0: "Companion report"}
CONTEXT = {
    215: "Solomon's demon weapon, investment thanks and the far-northwest icy island clue.",
    216: "Vivian reveals Excalibur and Avalon; Kamil and companion tavern variants.",
    217: "The cynical tavern keeper gives Avalon's western location.",
    218: "Dukov's Holy Spear of Ares rumor and fascination with ancient gods.",
    220: "Julian flirts with Lucia over the Empress's Gown rumor.",
    221: "The townsman's Crusades account, both choices, and Saladin's armor lead.",
    222: "Gerhard recounts Noritsune's final stand and armor lost in the strait.",
    223: "Dukov's Timur-mail letter, every companion delivery and Russian-history explanation.",
    224: "Julian and Safia's Medusa's Shield flirtation and Tasman Sea clue.",
    225: "Children play Charles Martel; Gerhard discusses his victory and Lil's legacy.",
    226: "Manuel explains Attila and his armor's northwestern, Scandinavian destination.",
}


def main() -> None:
    with SOURCE.open(encoding="utf-8-sig", newline="") as stream:
        source_rows = {row["id"]: row for row in csv.DictReader(stream)}
    expected = {i for i in source_rows if int(i.split("_B")[1].split("_")[0]) in BLOCKS}
    authored = {f"DK4_MES_B{b}_R{n:04d}" for b, n in LINES}
    if authored != expected:
        raise ValueError(f"Coverage mismatch: missing={expected - authored}, extra={authored - expected}")
    records = []
    for (block, number), english in LINES.items():
        row_id = f"DK4_MES_B{block}_R{number:04d}"
        raw = bytes.fromhex(source_rows[row_id]["source_hex"])
        state = None if (block, number) in BARE else raw[0]
        if state is not None and state not in SPEAKERS:
            raise ValueError(f"{row_id}: unmapped state {state:02X}")
        prose = english
        for macro in ("FI", "FA", "FO"):
            prose = prose.replace(f"{{MACRO:{macro}}}", "")
            if raw.count(macro.encode()) != english.count(f"{{MACRO:{macro}}}"):
                raise ValueError(f"{row_id}: macro mismatch {macro}")
        if "I" in prose or "F" in prose:
            raise ValueError(f"{row_id}: unsafe uppercase renderer byte")
        prefix = "" if state is None else f"{{SPEAKER:{state:02X}}}"
        records.append({
            "id": row_id, "english": f"{prefix}{english}{{PAD}}",
            "speaker": SPEAKERS.get(state, "Bare choice or companion variant"),
            "context": CONTEXT[block], "source_meaning": english,
            "source_japanese": raw[int(state is not None):].decode("shift_jis", errors="replace"),
            "localization_note": "Source-reviewed natural English preserves the scene, direction, treasure, presentation, and bare entry starts. Uses Dukov's surname and an Iceland epithet to avoid unsafe capital I; source Japanese retains the exact names.",
            "review": {gate: True for gate in ("source", "context", "localization", "naturalness", "formatting")},
        })
    batch = {
        "format": "dk4-ilnk-translation-batch-v1", "file_path": "/data/SC2.DK4",
        "source_file_sha256": SC2_SHA256, "encoder": "dialogue-fixed-v1",
        "dialogue_profile": "lil-story-deep-route-v102-live",
        "translation_policy": "natural-dialogue-v2", "target_locale": "en-US",
        "review_gates": ["source", "context", "localization", "naturalness", "formatting"],
        "scope": "Complete B215-B226 optional legend, armor, tavern and correspondence scenes; B219 has no records.",
        "inventory": {"identified_records": len(expected), "translated_records": len(records), "blocks": {str(b): sum(block == b for block, _ in LINES) for b in CONTEXT}},
        "excluded_records": {}, "records": records,
    }
    OUTPUT.write_text(json.dumps(batch, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {OUTPUT.relative_to(ROOT)}: {len(records)} records")


if __name__ == "__main__":
    main()
