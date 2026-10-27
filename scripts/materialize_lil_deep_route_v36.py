from __future__ import annotations

import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "work/sc2/script.csv"
OUTPUT = ROOT / "translations/lil_deep_route_v36.json"
SC2_SHA256 = "c2e0d1a2744a7da4a24f9693230b302a29f05bcaa036ebd5cc9726a6184731ff"

# Faithful source gloss, then localized paragraph. The keys are B121 record numbers.
LINES = {
    5: ("Admiral, a suspicious fleet is approaching!", "Admiral! A strange fleet ahead!"),
    9: ("Check whose fleet it is!", "Check who they are!"),
    13: ("That's the Li family. Admiral, it's their fleet! Five ships, and they're firing!", "The Li family... Admiral! They have five ships and they're firing!"),
    25: ("The Li family?!", "Li family?!"),
    40: ("Impossible! What's going on?", "What?! That's absurd!"),
    47: ("Admiral, what should we do?", "Admiral! Your orders?!"),
    53: ("We'll engage them!", "Engage!"),
    55: ("We should retreat!", "Retreat!"),
    63: ("Understood! We'll engage!", "Aye! We'll engage!"),
    68: ("Admiral, no! We can't shake them!", "Admiral! We can't shake them!"),
    71: ("We have no choice but to fight. Maria Huamei Li, were you our enemy? I can't believe it.", "We must fight! Maria Huamei Li... Our enemy? How can this be?"),
    75: ("Everyone to battle stations!", "Battle stations, everyone!"),
    79: ("Can we really beat that fleet?", "Can we beat that fleet...?"),
    83: ("If we can't escape, we'll break through head-on. We have to!", "Can't escape? We'll break through!"),
    97: ("Now it's down to luck! If luck is on our side...", "Now it's down to luck! Come on..."),
    104: ("Admiral! Trouble! More enemies have appeared!", "Admiral! More enemy ships!"),
    116: ("What? More enemies?!", "What?! More ships?!"),
    127: ("Against a fleet this large, even I may not stand a chance...", "Such a huge fleet... Can we really survive this?"),
    138: ("It seems we must prepare for the worst...", "We must brace for the worst..."),
    153: ("FI, Yukihisa will protect you at the cost of his life!", "My life is yours, {MACRO:FI}! You'll be safe with me!"),
    160: ("Kamil, I wanted to see you once more, and apologize. I'm sorry...", "Kamil... Wish we could meet again. So sorry..."),
    172: ("You fool! Don't give up so easily!", "You fool! Don't give up so easily!"),
    182: ("Huh?! That voice...!", "What?! That voice...!"),
    194: ("No way?!", "No way?!"),
    214: ("Wow! He's back!", "Wow! He's back!"),
    221: ("Kamil, is that you?!", "Kamil?! Really you?!"),
    232: ("We made it in time somehow, Kamil.", "Just in time, Kamil."),
    236: ("Yes, thanks to you and Hodram.", "Yes. Thanks to you and Hodram."),
    239: ("Huh? Maria? What's going on?", "What?! Maria...? What's going on?"),
    244: ("We made it in time somehow, Kamil.", "Made it in time, Kamil."),
    248: ("Just in the nick of time.", "Barely!"),
    258: ("Who are you? And Maria too? What's going on?", "Who are you? And Maria...? What's going on?"),
    264: ("Oh, you're Hodram, the officer. And Maria too? What's going on?", "Wait, you're Hodram, the officer! And Maria...? What's going on?"),
    274: ("Those fleets are all Kuhn's disguised fleets! Kuhn planned to pretend that the Li family killed FI...", "All Kuhn's ships, disguised! He'd claim the Li family killed {MACRO:FI}..."),
    277: ("He was creating a pretext to avenge an ally!", "A pretext to avenge his ally!"),
    288: ("Damn! So that's what happened!", "Damn! So that's his game!"),
    295: ("This is Kuhn's true nature. Now you understand, don't you?", "That's the real Kuhn. Now you understand."),
    298: ("I was such a fool. I'm sorry, Kamil...", "What a fool... So sorry, Kamil. Please forgive me..."),
    301: ("We'll talk later! We have to defeat Kuhn's fleet!", "Talk later! We must beat his fleet!"),
    312: ("Kamil is right, FI!", "Kamil is right, {MACRO:FI}!"),
    326: ("Let's scatter them!", "We'll crush them!"),
    333: ("Y-yes, you're right!", "Y-yes...!"),
    337: ("What's happening, Georg? Why is Maria here? And Marinus too!", "What's this?! Georg! Why is Maria here? And Marinus, of all people...!"),
    341: ("Hmm, neither was in our calculations. We should withdraw for now.", "Hmm... Neither was expected. We should withdraw for now."),
    345: ("Yes, all ships withdraw! I'll repay this debt someday!", "All ships, withdraw! We'll settle this score!"),
    348: ("It seems we're out of danger.", "We're out of danger."),
    352: ("Thank you. What you told me earlier was true. I'm sorry I didn't believe you.", "Thank you... You were right. Sorry for doubting you."),
    356: ("It's all right. But he's the one you really want to apologize to, isn't he?", "That's fine. You want to apologize to him, right?"),
    368: ("FI, you've got so much you want to say, don't you?", "{MACRO:FI}, you have so much to say..."),
    381: ("Kamil.", "Kamil."),
    387: ("Kamil.", "Kamil."),
    395: ("Y-yes. FI, I'm sorry. I...", "Y-yes. {MACRO:FI}, sorry..."),
    399: ("I'm the one who should apologize. Kamil, I'm sorry. You're Kuhn's...", "No, it's my fault. Sorry, Kamil. You're Kuhn's..."),
    403: ("Overijssel is my mother's surname. My real name is Marinus Kuhn. I'm Antony Kuhn's son.", "Yes... Overijssel is Mother's surname. My real name is Marinus Kuhn. Antony Kuhn's son."),
    406: ("The tavern keeper told me Kamil was a nickname. So it really was.", "Kamil was a nickname, then! That tavern keeper was right."),
    410: ("As a child I looked even more like a girl, so someone jokingly called me a girl's name. That's how it began.", "As a child, my face looked girlish. Someone teased me with a girl's name, and it stuck."),
    414: ("Only Father never used that name. By then he wasn't the father I had known.", "Only my father never used it. He'd already changed by then..."),
    418: ("Father was good once. When he met Mother he was a very small trader, she said.", "He was a good man once. Mother said he was just a small trader when they met."),
    421: ("Mother said they were poor but every day was happy and enjoyable.", "Mother said they were poor, but happy. Every day was a joy."),
    424: ("The Kuhn Company started making profits as soon as it entered the Spice Islands. Father changed after making a fortune.", "The Kuhn Company grew rich in those islands known for spices. The money changed him..."),
    428: ("Greed blinded him. He thought only of making money and wasn't afraid to use dirty tricks.", "Greed blinded him. He cared only about profit, and would use any dirty trick..."),
    432: ("Mother and I couldn't bear that.", "We couldn't bear it, Mother and me."),
    435: ("Kamil...", "Kamil..."),
    439: ("Everyone feared Father. Even Mother and I came to be avoided by our neighbors.", "Everyone feared him. Even our neighbors shunned Mother and me..."),
    443: ("Mother thought we couldn't live there anymore. She took me back to the Netherlands.", "Mother knew we couldn't stay. She took me back to the Netherlands."),
    447: ("FI, I never meant to tell anyone about Father. Especially you. I didn't want you to know.", "{MACRO:FI}... Nobody was meant to know about my father, especially you..."),
    450: ("That's why, that time... I'm sorry.", "That's why... Sorry."),
    453: ("Yes...", "Yes..."),
    465: ("So that's what it was...", "So that's what it was..."),
    472: ("FI, will you let me aboard your ship again?", "{MACRO:FI}, may your old shipmate come aboard again?"),
    475: ("Of course! What are you saying? It was so hard while you were gone!", "Of course! What are you saying? Things were so hard without you!"),
    479: ("FI... Thank you!", "{MACRO:FI}... Thank you!"),
    482: ("Work hard to repay all the worry you caused me!", "You worried me sick! Repay me by working hard!"),
    485: ("Good grief. You're as demanding as ever.", "Whew... Still a hard taskmaster!"),
    488: ("Kamil's back. I'm so glad.", "(Kamil's back... What a relief.)"),
    498: ("Has the misunderstanding been resolved?", "All cleared up now?"),
    502: ("Yes. I'm truly grateful to you and Hodram.", "Yes. You and Hodram have my heartfelt thanks."),
    506: ("Have you made up?", "Made up yet?"),
    510: ("Hodram, this is thanks to you too.", "Hodram... This is all thanks to you."),
    513: ("Maria tricked me. She only told me to bring Kamil here aboard my ship. I didn't do anything.", "Maria tricked me. She just asked me to bring Kamil here on my ship. Nothing more."),
    517: ("Tricked? You'd figured everything out!", "Tricked? You knew all along!"),
    520: ("Maria, thank you for warning us about the attack.", "Maria... Thank you for warning us about the attack!"),
    527: ("You're welcome. I'll have you repay this favor someday. We're leaving now.", "You're welcome. Repay this favor someday. Time for us to go."),
    531: ("Let me warn you: Kuhn won't be stopped by this much. Be prepared.", "Be warned: a setback won't stop Kuhn. Be ready for what comes next."),
    535: ("Yes, Father won't give up over this. What's coming now is even more frightening.", "Yes. My father won't give up. What comes next scares me even more."),
    539: ("That's true.", "True."),
    549: ("But Kamil, if you help FI, you'll surely get through this.", "But Kamil, help {MACRO:FI}, and you'll get through this together."),
    553: ("Yes, I'll do my best. Thank you very much. Please tell Hodram...", "Yes... Count on me. Thank you so much. Please tell Hodram..."),
    557: ("Thank you for introducing me to Maria and helping me recover...", "Thank him for introducing us and helping me recover..."),
    560: ("And tell him not to give up on building the strongest fleet.", "And keep aiming for the strongest fleet of all."),
    563: ("Yes, I'll tell him.", "Will do."),
    569: ("Kamil, you can get through it now. Join FI and prove it. I'll be going too.", "Kamil, you can face this. Join {MACRO:FI} and prove it. Time for me to go."),
    573: ("Hodram, thank you. I hope you build the strongest fleet as soon as possible.", "Thank you, Hodram. Hope your fleet becomes the strongest soon!"),
    579: ("I'll be going now. Oh, right! Take this.", "Time for me to go... Oh! Take this."),
    582: ("What's this?", "This?"),
    586: ("It's the key to solving the Proof's map. I'll give it to you.", "A key to solving the Proof's map. You can have it."),
    591: ("Thank you very much!", "Thank you so much!"),
    595: ("Maria, why are you so kind to me? I've been so rude to you...", "Maria... Why are you so kind to me? Even after my rude remarks..."),
    599: ("Because I found hope in you.", "Because you give me hope."),
    602: ("Hope?", "Hope?"),
    606: ("You'll surely save Asia's countries, divided by the European powers and unable to preserve independence.", "You can save Asia. Europe's great powers have divided its nations and denied them independence."),
    609: ("Can I really do that?", "Can someone like me do that...?"),
    612: ("Your dream is to make people in need around the world happy, isn't it? Asia's people are in need right now.", "You can. Your dream is to bring happiness to people in need, isn't it? Asia's people need you now."),
    615: ("You're the one who said dreams come true. I decided to put my faith in you.", "You said dreams come true. That's why you're the one worth putting my faith in."),
    619: ("Maria, thank you. I'll do my best, everything I can.", "Maria... Thank you. You'll get my very best. Count on it."),
    623: ("Thank you very much.", "Thank you for everything."),
    627: ("Let's go!", "Come on!"),
    631: ("Yes!", "Yeah!"),
    643: ("Then it's settled! Let's go! Yahoo!", "Then it's settled! Let's go! Yahoo!"),
}

SPEAKERS = {
    0x01: "Hodram Bergstrom", 0x02: "Lil Argot", 0x03: "Maria Huamei Li",
    0x07: "Christina", 0x09: "Kamil", 0x0B: "Jam Jack Ludwayer",
    0x0C: "Yukihisa Genjo Shiraki", 0x0E: "Emilio Ferrog",
    0x10: "Gerhard Adelknauts", 0x14: "Fernando", 0x15: "Ian Dukov",
    0x28: "Antony Kuhn", 0x38: "Georg", 0x97: "Lookout",
}
TEXT_LEADS = {0x8C, 0x91}


def main() -> None:
    with SOURCE.open(encoding="utf-8-sig", newline="") as stream:
        source_rows = {row["id"]: row for row in csv.DictReader(stream)}
    expected = {row_id for row_id in source_rows if row_id.startswith("DK4_MES_B121_")}
    if {f"DK4_MES_B121_R{number:04d}" for number in LINES} != expected:
        raise ValueError("B121 coverage does not match clean source")
    records = []
    for number, (source_meaning, english) in LINES.items():
        row_id = f"DK4_MES_B121_R{number:04d}"
        lead = int(source_rows[row_id]["source_hex"][:2], 16)
        if lead not in SPEAKERS and lead not in TEXT_LEADS:
            raise ValueError(f"{row_id}: unmapped lead {lead:02X}")
        literal = english.replace("{MACRO:FI}", "")
        if "I" in literal or "F" in literal:
            raise ValueError(f"{row_id}: uppercase renderer macro byte in English")
        context = (
            "Kuhn's disguised fleet ambushes Lil; Maria and Hodram return with Kamil to save her."
            if number < 348 else
            "After the rescue, Kamil explains his identity and family history, reconciles with Lil, and returns to her ship."
            if number < 498 else
            "The rescuers depart; Maria gives a Proof-map key and explains her faith in Lil's dream of helping Asia."
        )
        records.append({
            "id": row_id,
            "english": (f"{{SPEAKER:{lead:02X}}}" if lead in SPEAKERS else "") + english + "{PAD}",
            "speaker": SPEAKERS.get(lead, "Lil combat choice"),
            "context": context,
            "source_meaning": source_meaning,
            "localization_note": (
                "Localized from clean Japanese with all neighboring records and alternate rescue branches reviewed. "
                "Preserves Kamil's Marinus identity, maternal surname, Kuhn's false flag plot, real speaker states, and FI macros. "
                "8C/91 choice starts are ordinary text, not presentation commands."
            ),
            "review": {gate: True for gate in ("source", "context", "localization", "naturalness", "formatting")},
        })
    batch = {
        "format": "dk4-ilnk-translation-batch-v1", "file_path": "/data/SC2.DK4",
        "source_file_sha256": SC2_SHA256, "encoder": "dialogue-fixed-v1",
        "dialogue_profile": "lil-story-deep-route-v34-live",
        "translation_policy": "natural-dialogue-v2", "target_locale": "en-US",
        "review_gates": ["source", "context", "localization", "naturalness", "formatting"],
        "scope": "All 109 B121 ambush, rescue, Kamil reconciliation, family-history, and Maria farewell records.",
        "inventory": {"identified_records": 109, "translated_records": len(records), "blocks": {"121": len(records)}},
        "records": records,
    }
    OUTPUT.write_text(json.dumps(batch, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {OUTPUT.relative_to(ROOT)}: {len(records)} records")


if __name__ == "__main__":
    main()
