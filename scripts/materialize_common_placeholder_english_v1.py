from __future__ import annotations

import argparse
import hashlib
import json
import re
import textwrap
from pathlib import Path

from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.rom.nds import NdsImage

BASE_ROM = Path("out/raphael_natural_v2_pre_lil_hodram_unified_v1_accepted_rollback.nds")
CLEAN_COMMON = Path("work/files/COMMON/MESFILE.DK4")
RESTORE_BATCH = Path("translations/common_placeholder_source_restore_v1.json")
OUTPUT = Path("translations/common_placeholder_english_v1.json")
FILE_PATH = "/COMMON/MESFILE.DK4"


TEXT: dict[tuple[int, int], str | list[str]] = {
    # Fleet organization and tribute.
    (0, 55): "%s sailors idle.\nContinue?",
    (0, 57): "%s sailors unassigned.\n Continue?",
    (0, 61): "Monthly tribute:\n %s coins.",

    # Trade-good descriptions.
    (2, 8): "A lustrous yellow metal used\n for ornaments and jewelry.",
    (2, 9): "A pale, lustrous metal used\n for ornaments and jewelry.",
    (2, 16): "Cotton fiber used\n to make thread.",
    (2, 22): "Cotton dyed with\n figures, beasts, and flowers.",
    (3, 12): "Fungus grown on insects,\n prized as a tonic.",
    (3, 13): "Turmeric-root extract\n used as yellow dye.",
    (3, 14): "Fermented indigo-leaf dye\n with a vivid blue hue.",
    (3, 16): "Dark dye made by boiling\n betel-palm fruit.",
    (3, 17): "Yellow rhubarb-root dye.\nNative to China.",
    (3, 19): "Powder weapon firing bullets.\nSells well in war.",
    (3, 20): "Weapon firing large shot.\nSells well in war.",

    # Items, fleet results, and equipment prompts.
    (4, 1): "Azores wine, from the\nIslands of Hawks.",
    (4, 3): "A sword like Svartis,\nor Black Ice.",
    (4, 17): "Dismiss the captain and leave\nthe crew in charge?",
    (4, 22): "Make %s of %s\n the Admiral?",
    (4, 28): "A sense of peace fills you.",
    (4, 31): "A gentle melody moves\n %s and the others.",
    (4, 34): "Seized %s coins\n aboard.",
    (4, 36): "Seized ship:\n%s food, %s water.",
    (4, 38): "The nation awarded\n %s coins.",
    (4, 41): "Hot spring raised\n Experience.",
    (4, 44): "Splash!",
    (4, 47): ["Who will equip it?", "%s equipped %s."],
    (4, 48): ["%s removed.", "Equip which ship?"],
    (4, 49): "The Devil Statue broke!",
    (4, 50): "The Devil Statue will not come off.\n Force it off?",
    (4, 53): "%s removed\n %s.",
    (4, 57): ["%s dissolved.", "%s sank!"],

    # Diplomacy, letters, and ocean events.
    (5, 2): "%s got a letter.\n Relations rose %s.",
    (5, 3): "Got a letter\n from %s.",
    (5, 4): "%s proposes an alliance\n against %s. Accept?",
    (5, 5): "%s and %s formed an alliance\n against %s.",
    (5, 6): ["Offer refused.", "Pact with %s failed."],
    (5, 8): ["%s requests a truce.\n Accept?", "%s and %s made peace"],
    (5, 9): "%s accepted\n peace.",
    (5, 10): "%s rejected\n the truce offer!",
    (5, 11): ["%s declared war on %s!", "%s declared war on us!"],
    (5, 12): "%s joined\n you.",
    (5, 13): "%s rejected\n the merger offer.",
    (5, 14): "Lies reached\n %s.",
    (5, 15): "%s was lured.\nSuccess!",
    (5, 16): "Forgeries reached\n %s.",
    (5, 17): "%s and %s\n turned against each other.",
    (5, 19): "In %s, rumors\n spread of %s.",
    (5, 21): "%s's share\n fell.",
    (5, 22): ["In %s, %s bribed your broker!", "Bribe failed."],
    (5, 23): "%s ignored\n the merger offer.",
    (5, 24): "%s and %s\n formed an alliance.",
    (5, 25): ["Admiral, a storm!", "Storm, sir!"],
    (5, 26): "Admiral!\n A storm!",
    (5, 27): "Admiral, a storm!",
    (5, 28): "Admiral, a storm!",
    (5, 29): "This is bad!\n A storm!",
    (5, 31): "Blizzard, sir!",
    (5, 32): "Brrr!\n A-Admiral, a blizzard!",
    (5, 33): "Admiral, sailors\n have scurvy!",
    (5, 34): "This is bad!\n The sailors have scurvy!",
    (5, 36): "Admiral, sailors\n have scurvy!",
    (5, 37): "This is bad!\n The sailors caught scurvy!",
    (5, 38): "Admiral, sailors\n have scurvy!",
    (5, 39): "Admiral, rats are everywhere!\n They'll ruin our food!",
    (5, 40): "Rats!\nFood's at risk.",
    (5, 41): "Rats everywhere!\nFood is at risk...",
    (5, 42): "Eek!\n Admiral, rats are everywhere!\n Help!",
    (5, 43): "Admiral, rats are everywhere!\n Is the food safe?!",
    (5, 44): "Admiral, rats everywhere!\n Food's at risk!",
    (5, 46): "A storm!\n It was clear only moments ago...",
    (5, 47): "Admiral, a storm!\n Weather changed fast...",
    (5, 48): "Admiral, a storm!\n It was just sunny...",
    (5, 49): "Admiral, a storm!\n It was clear...",
    (5, 50): "A storm!\n Strange... It was clear.",
    (5, 51): "A storm!\nBut the weather was fine.",
    (5, 52): "A storm is coming!\n The sun was just out...",
    (5, 54): "Admiral, look up!",
    (5, 55): ["Admiral, look skyward!", "Fog forming... Poor visibility."],
    (5, 56): "Fog.",
    (5, 58): ["Fog is rolling in.", "Fog! I can't see well."],
    (5, 59): "Fog forming.\n Poor visibility...",
    (5, 60): "Aah!\n A m-monster!",
    (5, 61): "What?!\n A monster!",
    (5, 62): "Aah!\n A m-monster!",
    (5, 63): "Eek!\n A m-monster!",
    (5, 64): "Eeeeeek!\n A m-monster!",
    (5, 65): "Waaah!\n A m-monster!",
    (5, 66): ["W-what is this song?", "What song?"],
    (5, 67): ["Singing...?", "W-what song is this?"],
    (5, 68): "What...? I hear singing...",
    (5, 69): "Hm? What's that?\nS-someone's swimming!",
    (5, 70): "What's that...?\n Someone is swimming!",
    (5, 71): "What is it?\nSomeone's swimming!",
    (5, 72): "Oh...?\n Someone's swimming!",
    (5, 73): "What is that...?\n Someone's swimming!",
    (5, 74): "What is that...?\n Someone is swimming!",
    (5, 75): "What's that?\n Someone swims!",
    (5, 76): "What could that be...?\n Is someone swimming?!",
    (5, 77): "Oh! Is that the legendary\n mermaid?!",
    (5, 78): "Oh!\n The legendary mermaid?!",
    (5, 79): "Whoa!\n The legendary mermaid?!",
    (5, 80): "Is that\n a legendary mermaid?!",
    (5, 81): "Could that be the legendary\n mermaid?!",
    (5, 82): "Is that... a mermaid?",
    (5, 83): "I-is that a mermaid?",
    (5, 84): "A legendary mermaid?",
    (5, 85): "Admiral, look!\n Strange bubbles at sea!",
    (5, 86): "Sir!\n Odd bubbles!",
    (5, 87): "Admiral!\n Strange bubbles!",
    (5, 88): "Admiral, look there!\n Strange bubbles are rising!",
    (5, 89): "Admiral! Strange bubbles\n rising there!",

    # Strange bubbles, disease, sharks, and discipline.
    (6, 1): ["The rumored... Gulp!", "Rumored..."],
    (6, 2): "Gulp!\n Could that be...?",
    (6, 4): "Are those strange bubbles...?",
    (6, 9): "Those bubbles...\nThey sink ships.",
    (6, 12): "Danger! Evade! All hands ready!",
    (6, 15): ["Admiral! %s!", "Admiral! %s!"],
    (6, 16): "Admiral! %s!",
    (6, 17): ["Admiral! %s!", "Admiral! %s!"],
    (6, 18): "Admiral! It's %s!",
    (6, 19): "An epidemic!",
    (6, 20): "Admiral, disaster!\n An epidemic!",
    (6, 21): "Disaster! An epidemic!",
    (6, 22): "Admiral!\n An epidemic!",
    (6, 32): "Admiral, sharks!\n Be careful!",
    (6, 33): "Admiral, sharks!\n Be careful!",
    (6, 35): "Sharks, Admiral!\nBe careful!",
    (6, 36): "Admiral, sharks!\n Take care!",
    (6, 37): "Waaah, sharks!\n Be careful, Admiral!",
    (6, 53): "Silence! Defy the Admiral,\n face me!",

    # Mutiny, damage reports, supplies, enemy fleets, and route restrictions.
    (7, 4): "That trick won't fool us!",
    (7, 5): "Drag out the Admiral!\nGet 'em!",
    (7, 7): "Ouch! Stop that!",
    (7, 8): "Enough!\n You've made your point!",
    (7, 9): "Enough! Stop!",
    (7, 12): "Stop it already!\n Leave the poor Admiral alone!",
    (7, 13): "Enough!\n You've made your point!",
    (7, 14): "Understood.\n I'll cook!",
    (7, 15): "Got it!\n Leave it to IC!",
    (7, 16): "Understood. I'll do it!",
    (7, 18): "Got it! Leave the meals\n to me!",
    (7, 20): "Admiral, a leak!\n Flagship hull damaged!",
    (7, 21): "This ship is leaking!\n Is the hull damaged...?",
    (7, 23): "Admiral! The flagship's\nhull is leaking!",
    (7, 25): "Admiral! The flagship's\nhull is damaged.",
    (7, 26): "A leak aboard %s!\n The hull appears damaged!",
    (7, 27): "Admiral! %s is leaking!\n Is the hull damaged?",
    (7, 28): "Admiral! %s is leaking!\n Hull damaged.",
    (7, 29): "Admiral! A leak aboard %s!\n The hull appears damaged.",
    (7, 30): "Admiral! %s is leaking!\n Its hull seems damaged.",
    (7, 32): ["The fire is out!", "Flames are out!"],
    (7, 33): "Admiral, the fire is out!",
    (7, 34): "Admiral! I put out the fire!",
    (7, 35): "Fire extinguished!",
    (7, 36): "%s's fire\n is out!",
    (7, 37): "%s's fire\n is out!",
    (7, 38): "%s's fire\n is out!",
    (7, 39): "%s fire\n is out!",
    (7, 40): "%s's fire\n is out!",
    (7, 41): "%s's fire\n is out!",
    (7, 42): "%s's fire\n is out!",
    (7, 43): "%s's fire\n is out!",
    (7, 44): "No %s left!",
    (7, 45): "No %s\n remains!",
    (7, 46): "We've run out\n of %s!",
    (7, 47): "There is no %s\n left!",
    (7, 48): "%s has\n run out!",
    (7, 49): "We've run out\n of %s!",
    (7, 50): "Oh no!\n We've run out of %s!",
    (7, 51): "We've run out\n of %s!",
    (7, 53): "%s is gone...\n Stopping %s.",
    (7, 54): "No %s remains.\n We'll stop %s.",
    (7, 55): "We're out of %s.\n I'll stop %s.",
    (7, 56): "At %s: %s fleet spotted!\n Battle stations!",
    (7, 57): "At %s: %s fleet!\n Battle stations!",
    (7, 58): "At %s: %s fleet!\n Battle stations!",
    (7, 59): "At %s: %s fleet!\n Battle stations!",
    (7, 60): "At %s: %s fleet!\n Battle stations!",
    (7, 61): "At %s: %s fleet!\n Battle stations!",
    (7, 62): "At %s: %s fleet!\n Battle!",
    (7, 63): "At %s: %s fleet spotted!\n Battle stations!",
    (7, 64): "At %s: %s fleet!\n They're attacking!",
    (7, 65): "At %s: %s fleet!\n They're attacking!",
    (7, 66): "At %s: %s fleet!\n They're attacking!",
    (7, 67): "At %s: %s fleet!\n They're attacking!",
    (7, 68): "At %s: %s fleet!\n They're attacking!",
    (7, 69): "From %s: %s fleet attacks!",
    (7, 70): "At %s: %s fleet!\n They're attacking!",
    (7, 71): ["No surveyor.", "No surveyor."],
    (7, 72): ["No surveyor.", "No surveyor."],
    (7, 73): "No surveyor aboard.",
    (7, 75): "There is no route\n to that city.",
    (7, 76): "There is no route\n to that city.",
    (7, 77): "There is no route\n to that city.",
    (7, 78): "There is no route\n to that city.",
    (7, 79): "There is no route\n to that city.",
    (7, 80): "No route leads\n to that city.",
    (7, 81): "There is no route\n to that city.",
    (7, 82): "Order from\n Captain's cabin.",
    (7, 83): "Order in\n Captain's cabin.",
    (7, 84): "Order from the\nCaptain's cabin.",
    (7, 85): "Order in\n Captain's cabin.",

    # Square merchants, free samples, economic conditions, and regional history.
    (8, 8): [
        "Bulk trade? Try the trade house.",
        "Business? Fair. I wish a good opportunity would arise.",
    ],
    (8, 9): "Give the goods\n away free?",
    (8, 10): "Hand the goods\n out free?",
    (8, 11): "Give the goods\n as samples?",
    (8, 12): "Give the goods\n away free?",
    (8, 13): "Give townspeople\n the goods free?",
    (8, 14): "Give everyone\n the goods free?",
    (8, 15): "Give out the goods\n as free samples?",
    (8, 16): "Please take a free sample!\n No charge today!",
    (8, 17): "Everyone, please take one.\n They're free, so don't be shy.",
    (8, 18): "Come look and take one!\n Free samples for everyone!",
    (8, 19): "Please try one!\n It's a free sample!",
    (8, 20): "Try this!\n It's free, so take one!",
    (8, 21): "Try this! A free sample!\n It costs nothing today!",
    (8, 22): "Free samples here!\n Now is your chance to try one!",
    (8, 23): "Please take one.\n Free samples available now!",
    (8, 25): [
        "Look at this %s. It's surely the finest quality.",
        "See what this makes: superb flavor!",
        "Ladies, take a look! Discover the fashions and decor soon to captivate society.",
    ],
    (8, 26): "Mmm, that aroma and flavor!\n It melts away fatigue. Try it!",
    (8, 27): "This age overflows with inventions and industry. Hear my lecture or miss your chance to profit!",
    (8, 28): [
        "This cures every illness. Try it and see!",
        "Hmm... %s? Worth watching. Let's try selling it around %s.",
    ],
    (8, 29): "Business? Forget that.\n I just hope peace returns soon.",
    (8, 30): "Business? People are dying\n from disease, and you ask that?",
    (8, 31): "Business? Food comes first.\n People cannot live without eating.",
    (8, 32): "Business? Just look around!\n I can't stop smiling.",
    (8, 33): "Business? Don't ask.\n No one can trade like this.",
    (8, 34): "Business? The liner sank.\n Everyone suffers.",
    (8, 35): "England unites England, Scotland, and Wales. It will surely keep growing. Long live the Queen!",
    (8, 36): "After a long war, the Netherlands recently broke from Spain.",
    (8, 37): "The Hanseatic League once ruled European trade, but faded after routes to India and the New World opened.",
    (8, 38): "Sweden recently left the Kalmar Union with Denmark and Norway.",
    (8, 39): "Portugal? Until quite recently, it controlled nearly all the world's seas.",
    (8, 40): "Spain prospers, doesn't it? Other nations call it the empire where the sun never sets.",
    (8, 41): "Since the India route opened, Italian city-states like Genoa and Venice have lost their eastern trade.",
    (8, 42): "Since the Ottomans occupied Greece, many churches have been turned into mosques.",
    (8, 43): "Istanbul was once Constantinople, capital of the Eastern Roman and Byzantine empires.",
    (8, 44): "North African cities are Ottoman subjects. Even the Mediterranean pirates bow to the Sultan.",
    (8, 45): [
        "Everyone seeks West African trade rights because the region produces ivory and gold.",
        "Muslim powers once controlled trade in this region.",
    ],
    (8, 46): [
        "You're an infidel. I have nothing more to say to you.",
        "Do not blame others. Misfortune comes from deeds in a former life.",
    ],
    (8, 47): "Kingdoms here once submitted to Ming China, but today's Ming has lost its former glory.",
    (8, 48): "The Majapahit kingdom once ruled these seas, but fell under pressure from Muslim powers.",
    (8, 49): "The Ming once prospered, but eunuchs now dominate a government in disorder.",
    (8, 50): "Korea unified under its founder Yi Seong-gye about two centuries ago.",
    (8, 51): "The long age of warring states is finally ending.",
    (8, 52): "The Caribbean is a haven for pirates from across Europe.",

    # Tavern, shipyard, plots, and diplomacy commands.
    (9, 28): "I see. How stingy.",
    (10, 4): "I wish the war would end.\n Trade is difficult.",
    (10, 5): "Business has improved.\n Trade is easier now.",
    (10, 6): "Business has worsened.\n Trade is difficult.",
    (10, 7): "Thanks for popular goods!\n I'll write a referral.",
    (10, 21): ["Admiral, IC will help!", "Admiral, let me help repair!"],
    (10, 22): ["Admiral, I'll help!", "Admiral, let me help repair!"],
    (10, 30): "You really can't manage\n without me beside you!",
    (10, 31): "I worry about %s...\n May I stay?",
    (10, 32): "No. I will remain\nthe Admiral's aide.",
    (10, 37): "Change water-food\n supply ratio?",
    (11, 46): "%s, correct?\nChoose the opposing side.",
    (11, 47): "%s, right?\n Which faction opposes it?",
    (11, 48): "%s, right?\n Which opponent?",
    (11, 50): "%s, right?\n Which faction opposes it?",
    (11, 54): "Send them to which city?",
    (11, 58): "Oppose whom?",
    (11, 59): "Turn them on whom?",
    (11, 60): "Make them fight whom?",
    (11, 61): "Who should we set against them?",
    (11, 63): "Lure %s's fleet\n out to %s?",
    (11, 65): "Draw %s's fleet\n out to %s?",
    (11, 67): "Turn %s and %s\n against each other?",
    (11, 68): "Make %s and %s\n fight?",
    (11, 69): "Have %s and %s\n fight each other?",
    (11, 70): "Make %s and %s\n fight each other?",
    (11, 71): "Pit %s against %s?",
    (11, 72): "Make %s and %s\n quarrel?",
    (11, 73): "Set %s and %s\n against each other?",
    (11, 74): "In %s, spread rumors of %s?",
    (11, 75): "In %s, spread rumors of %s?",
    (12, 0): "In %s, spread rumors of %s?",
    (12, 3): "In %s, spread rumors of %s?",
    (12, 15): "Bribe which city's broker?",
    (13, 48): "Fine. I'll pay %s coins.",
    (13, 50): "Choose whom to %s.",
    (13, 51): "Who should we %s?",
    (13, 52): "Whom shall we %s?",
    (13, 54): "Choose our common enemy.",
    (13, 55): "Which common enemy?",
    (13, 56): "Who shall we oppose?",
    (14, 0): "Who should we fight?",
    (14, 7): "To %s, send %s's letter?",
    (14, 9): "To %s, send %s's letter?",
    (14, 23): "There is no common enemy.",
    (14, 24): "There is no common foe.",
    (14, 58): ["Just 1 coin.", "Sleep well!"],
    (14, 62): "In %s, someone cornered %s.",
    (14, 64): "Found information\n on %s.",
    (14, 65): "Found information\n on %s.",
    (15, 45): "IC will help\n refit!",
    (16, 13): ["Admiral, a village!", "A village!"],
}


PACKED_MARKERS: dict[tuple[int, int], list[str]] = {
    (4, 47): ["%sが"],
    (4, 48): ["どの船に"],
    (4, 57): ["%sが沈没"],
    (5, 6): ["%sとの協定は"],
    (5, 8): ["%sと"],
    (5, 11): ["%sが\n宣戦を布告してきました"],
    (5, 22): ["買収は失敗しました"],
    (5, 25): ["提督、嵐だよ"],
    (5, 55): ["霧が出てきましたね"],
    (5, 58): ["キリだあ"],
    (5, 66): ["この歌はなんだ"],
    (5, 67): ["な、なに、この歌は"],
    (6, 1): ["あれが噂の"],
    (6, 15): ["提督！　%sだよっ"],
    (6, 17): ["ていとくー"],
    (7, 32): ["もう火は消えたぜ"],
    (7, 71): ["測量士がおりません"],
    (7, 72): ["測量士がいませんわ"],
    (8, 8): ["景気？"],
    (8, 25): ["さあ、こいつを使って", "さあさあ、そこの奥方"],
    (8, 28): ["へえ…"],
    (8, 45): ["昔は、このあたり"],
    (8, 46): ["自分の不幸を"],
    (10, 21): ["提督、修理なら私にも"],
    (10, 22): ["提督、修理ならわしも"],
    (14, 58): ["はい、お休みなさい"],
    (16, 13): ["提督、村です"],
}

# Runtime screenshots show that the Inn renders these source indents literally.
# Preserve its two-byte first entry and unindented alternate entry instead of
# applying the general two-byte guard to both packed starts.
PACKED_ENTRY_PREFIXES: dict[tuple[int, int], list[int]] = {
    (14, 58): [2, 0],
}


def _sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _guarded(text: str) -> bytes:
    lines: list[str] = []
    for authored_line in text.split("\n"):
        lines.extend(
            textwrap.wrap(
                authored_line.strip(),
                width=29,
                break_long_words=False,
                break_on_hyphens=False,
            )
            or [""]
        )
    return b"\n".join(("  " + line).encode("ascii") for line in lines)


def _fit(text: str, source: bytes, record_id: str) -> bytes:
    encoded = _guarded(text)
    if len(encoded) > len(source):
        raise ValueError(
            f"{record_id}: translation needs {len(encoded)} bytes, allocation is {len(source)}"
        )
    if len(re.findall(rb"%[-+0-9.*]*[sd]", encoded)) != len(
        re.findall(rb"%[-+0-9.*]*[sd]", source)
    ):
        raise ValueError(f"{record_id}: printf macro count changed")
    return encoded.ljust(len(source), b" ")


def _fit_packed(
    english: list[str], markers: list[str], source: bytes, record_id: str,
    prefixes: list[int] | None = None,
) -> bytes:
    starts = [0]
    cursor = 1
    for marker in markers:
        position = source.find(marker.encode("cp932"), cursor)
        if position < 0:
            raise ValueError(f"{record_id}: packed marker not found: {marker}")
        starts.append(position)
        cursor = position + 1
    if len(starts) != len(english):
        raise ValueError(f"{record_id}: packed segment count mismatch")
    output = bytearray()
    for index, text in enumerate(english):
        end = starts[index + 1] if index + 1 < len(starts) else len(source)
        segment = source[starts[index] : end]
        if prefixes is None:
            output.extend(_fit(text, segment, f"{record_id}[{index}]"))
            continue
        if len(prefixes) != len(english):
            raise ValueError(f"{record_id}: packed prefix count mismatch")
        encoded = b" " * prefixes[index] + text.encode("ascii")
        if len(encoded) > len(segment):
            raise ValueError(
                f"{record_id}[{index}]: translation needs {len(encoded)} bytes, "
                f"allocation is {len(segment)}"
            )
        if len(re.findall(rb"%[-+0-9.*]*[sd]", encoded)) != len(
            re.findall(rb"%[-+0-9.*]*[sd]", segment)
        ):
            raise ValueError(f"{record_id}[{index}]: printf macro count changed")
        output.extend(encoded.ljust(len(segment), b" "))
    return bytes(output)


def materialize(base_rom: Path, clean_common: Path) -> dict[str, object]:
    accepted = NdsImage.open(base_rom).read_file(FILE_PATH)
    clean = clean_common.read_bytes()
    clean_blocks = [block.split(b"\0") for block in IlnkContainer.parse(clean).blocks]
    restore = json.loads(RESTORE_BATCH.read_text(encoding="utf-8"))
    expected = {
        (int(record["id"][9:11]), int(record["id"][13:17]))
        for record in restore["records"]
    }
    if set(TEXT) != expected:
        missing = sorted(expected - set(TEXT))
        extra = sorted(set(TEXT) - expected)
        raise ValueError(f"translation coverage mismatch; missing={missing}, extra={extra}")

    records: list[dict[str, object]] = []
    for (block, index), english in sorted(TEXT.items()):
        source = clean_blocks[block][index]
        record_id = f"DK4_MES_B{block:02d}_R{index:04d}"
        if isinstance(english, list):
            replacement = _fit_packed(
                english,
                PACKED_MARKERS[(block, index)],
                source,
                record_id,
                PACKED_ENTRY_PREFIXES.get((block, index)),
            )
            display = " / ".join(english)
            structure = "packed-multiple-entry"
            entry_offsets = [0]
            cursor = 1
            for marker in PACKED_MARKERS[(block, index)]:
                position = source.find(marker.encode("cp932"), cursor)
                if position < 0:
                    raise ValueError(f"{record_id}: packed marker not found: {marker}")
                entry_offsets.append(position)
                cursor = position + 1
        else:
            replacement = _fit(english, source, record_id)
            display = english
            structure = "single-entry"
            entry_offsets = [0]
        record = {
                "id": record_id,
                "english": display,
                "replacement_hex": replacement.hex().upper(),
                "status": "translated",
                "context": f"Shared gameplay block {block}, record {index}.",
                "notes": (
                    "Translated from the clean Japanese source. Two-byte ASCII entry guards, printf "
                    "macros, fixed allocation length, and any mapped packed entry offsets are preserved."
                ),
                "structure": structure,
                "entry_offsets": entry_offsets,
            }
        if (block, index) in PACKED_ENTRY_PREFIXES:
            record["ascii_guard_exemption"] = (
                "Runtime Inn screenshots prove that the source entry indents are "
                "rendered literally; preserve the original per-entry layout."
            )
            record["notes"] = (
                "Translated from the clean Japanese source. Runtime-proven Inn "
                "indentation and the packed alternate entry offset are preserved."
            )
        records.append(record)

    return {
        "format": "dk4-ilnk-translation-batch-v1",
        "content_type": "ilnk-fixed-source-translation-v1",
        "file_path": FILE_PATH,
        "source_file_sha256": _sha256(accepted),
        "target_locale": "en-US",
        "ascii_guard_policy": "two-byte-entry-and-line-v1",
        "scope": "Complete English replacement for every source-restored generic COMMON record",
        "records": records,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--base", type=Path, default=BASE_ROM)
    parser.add_argument("--clean-common", type=Path, default=CLEAN_COMMON)
    parser.add_argument("--out", type=Path, default=OUTPUT)
    args = parser.parse_args()
    batch = materialize(args.base, args.clean_common)
    args.out.write_text(json.dumps(batch, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {len(batch['records'])} English records to {args.out}")


if __name__ == "__main__":
    main()
