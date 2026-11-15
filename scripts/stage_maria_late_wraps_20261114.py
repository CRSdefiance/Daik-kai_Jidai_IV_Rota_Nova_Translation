"""Review the flagged Maria shop, bargaining, and letter scenes."""

import argparse
from pathlib import Path
from types import FunctionType

from scripts import register_maria_midroute_wraps_20261114 as parent
from scripts import stage_maria_opening_wraps_20261114 as previous
from scripts.source_locked_derivation_v5118 import checked_text


base, sha, prior = previous.base, previous.sha, previous.prior
FILE, ARM, CLEAN, IlnkContainer = previous.FILE, previous.ARM, previous.CLEAN, previous.IlnkContainer
ROOT = Path('work/maria_late_wraps_20261114_v1')
CAPTURE = ROOT / 'maria_startup/capture_report.json'
RUNTIME = ROOT / 'maria_native_context.json'
REVIEW = parent.TRIAGE.with_name('maria_late_wraps_context_v1.json')
PROOF = ROOT / 'stored_and_native.json'
native, expanded, expand_bytes = previous.native, previous.expanded, previous.expand_bytes
initial_names = previous.initial_names

# Exact current body offsets with their unchanged source-aligned quote or signature.
EXTRA = {
    (169, 11): (77, b'200000 gold'),
    (169, 151): (891, b'50000 gold'),
    (169, 211): (1215, b'40000 gold'),
    (169, 256): (1405, b'30000 gold'),
    (174, 16): (217, b'300000 gold'),
    (174, 25): (471, b'200000 gold'),
    (174, 28): (561, b'50000.'),
    (174, 32): (575, b'150000 gold'),
    (187, 67): (1049, b'Janus Pasar'),
}

DECISIONS = {
    (153, 4): ("Lady", "Wasn't that fragrance lovely?",
        "The lady asks another woman whether she noticed the wonderful scent the person was wearing.",
        "The preceding person remains unspecified in English. Keep her elegant enthusiasm as the opening to a conversation about fashion.",
        ("that fragrance lovely?",)),
    (156, 17): ("Guildmaster", "Oh, yes. People will remember his work for generations.",
        "The admirer believes the artist will make a lasting name for himself.",
        "Keep his confidence before he recommends buying the work now. The other two buyers disagree about which artist is best.",
        ("remember his work", "for generations.",)),
    (159, 12): ("Owner", "Yes! Our customers won't settle for a flavor this mild. Sweet is what matters. Sweet!",
        "The owner insists that the light taste will not satisfy customers and repeats sweet with exaggerated emphasis.",
        "Keep the owner's certainty and the repeated word that drives the exchange. Her employee remains doubtful and later asks how to make it sweeter.",
        ("a flavor this mild.", "Sweet is what matters.",)),
    (160, 16): ("Shopkeeper", "Lots of people have a cough lately.",
        "The shopkeeper recalls seeing many people cough lately.",
        "Keep his observation in response to the other person's coughing, before the question about an outbreak.",
        ("have a cough lately.",)),
    (160, 23): ("Shopkeeper", "I heard there's a good remedy.",
        "The shopkeeper recalls hearing about a good medicine.",
        "The uncertain recollection works before he is asked what the medicine is called.",
        ("a good remedy.",)),
    (160, 29): ("Shopkeeper", "Forgot the name. It's got almonds.",
        "The shopkeeper forgot the name but heard that the remedy contains almonds.",
        "Keep his casual reminder about the ingredient, which the ill man repeats in surprise.",
        ("It's got almonds.",)),
    (163, 47): ("Sailor", "But what happened afterward?",
        "The sailor asks about what happened after the familiar part of the story.",
        "The question changes the focus after the other speaker says everyone knows the story.",
        ("what happened afterward?",)),
    (169, 11): ("Shady Man", "I've got a deal for you. 200,000 gold? Heeheehee!",
        "The vendor offers the item for 200,000 gold with a snicker.",
        "Keep the opening price exact and group its digits the same way as the counteroffers. Later halving assumes this opening price.",
        ("200,000 gold?",)),
    (169, 61): ("Shady Man", "Fine. 100,000 gold? Heeheehee!",
        "The vendor drops his asking price to 100,000 gold and snickers.",
        "Keep the price and his laugh. Carlo's private advice immediately remarks on the price being halved.",
        ("100,000 gold?",)),
    (169, 106): ("Shady Man", "How about 70,000 gold? Heeheehee!",
        "The vendor proposes 70,000 gold and snickers.",
        "Keep his second price reduction distinct before Fernando suggests trying once more.",
        ("70,000 gold?",)),
    (169, 151): ("Shady Man", "Greedier than you look. How about 50,000 gold? Heehee!",
        "The vendor says the buyer is greedier than expected and asks 50,000 gold.",
        "Keep his jibe and laugh at this stage of negotiation. Use the same thousands separator as the earlier bids.",
        ("50,000 gold?",)),
    (169, 196): ("Shady Man", "You're good at this. Here you go.",
        "The vendor compliments the buyer's bargaining skill and hands over the item.",
        "Keep this as a completed sale in the acceptance branch. The next counteroffer belongs to a different choice.",
        ("You're good at this.", "Here you go.",)),
    (169, 211): ("Shady Man", "40,000 gold... Heh.",
        "The vendor hesitates over a price of 40,000 gold and gives a short laugh.",
        "Keep the marked hesitation and brief laugh. Consistent digits distinguish this bid from the previous one.",
        ("40,000 gold...",)),
    (169, 256): ("Shady Man", "Please, just buy it. I'll take 30,000 gold.",
        "The vendor pleads for a sale and settles for 30,000 gold.",
        "Keep his change from swagger to pleading. The next private aside says the price is as low as it will go.",
        ("30,000 gold.",)),
    (169, 305): ("Shady Man", "Forget it! Someone else will buy it.",
        "The vendor breaks off negotiations because he will sell to someone else.",
        "Preserve his dismissive response after the player declines. Leave the sale prospective.",
        ("Someone else will buy it.",)),
    (170, 48): ("Alluring Woman", "May you find love with a celestial maiden, too.",
        "She wishes that the buyer can also find love with a celestial maiden.",
        "Keep the folkloric reference and the blessing after the purchase, using the parallel Lil exchange for continuity.",
        ("a celestial maiden, too.",)),
    (170, 92): ("Alluring Woman", "Hehe... Next time, I'd like to fall for a man like you.",
        "The woman laughs and says she would like to fall in love with a man like him next time.",
        "Keep her direct personal wish after she gives him the item. Her disappearance and Ian's uncertain conclusion come later.",
        ("I'd like to fall", "a man like you.",)),
    (173, 36): ("Stranger", "I see. Sorry for the trouble.",
        "The recovered stranger acknowledges what happened and apologizes for putting the other person to trouble.",
        "Keep the quiet courtesy after the explanation that he was carried from the harbor, before being advised to rest.",
        ("Sorry for the trouble.",)),
    (174, 16): ("Seller", "W-what? Of course not! I'll give you a good price, though. Say 300,000 gold.",
        "The seller balks at replacing the rope for free, promises a favorable price and asks 300,000 gold.",
        "Keep his sputter and ironic promise before Carlo intervenes. Write the price like the other bids.",
        ("300,000 gold.",)),
    (174, 22): ("Carlo", "Special or not, that's a ridiculous price for mast rope. I'd say 30,000 gold at most.",
        "Carlo says that even for a rare rope the price is absurd and puts it at no more than 30,000 gold.",
        "Preserve the difference between Carlo's initial valuation and the later bids. The seller immediately counters at 200,000.",
        ("a ridiculous price", "for mast rope.", "30,000 gold at most.",)),
    (174, 25): ("Seller", "W-wait! You won't find another like it anywhere. How about 200,000 gold?",
        "The seller protests that the rope is unique and asks 200,000 gold.",
        "Keep the seller's stammer and the new asking price after Carlo values the rope at 30,000.",
        ("another like it", "200,000 gold?",)),
    (174, 28): ("Carlo", "50,000",
        "Carlo counters with the bare amount of 50,000.",
        "Keep the five digits and no extra wording. The terse quote uses the same grouping as Carlo's later 75,000 offer.",
        ("50,000",)),
    (174, 32): ("Seller", "Hmm... 150,000 gold. Will that do?",
        "The seller counters with 150,000 gold and asks Carlo to accept it.",
        "Keep his bargaining concession and exact amount before Carlo offers 75,000.",
        ("150,000 gold.",)),
    (174, 84): ("Maria", "Yes... On second thought, we don't need to replace it yet.",
        "Maria agrees that there is no hurry to replace the rope after all.",
        "Keep the practical conclusion in the refusal branch before Carlo relays that decision.",
        ("On second thought,", "replace it yet.",)),
    (177, 34): ("Maria", "I'm glad they understood you. We're leaving soon. Get ready, please.",
        "Maria is pleased the locals understood his explanation and tells him to prepare because they will leave shortly.",
        "Move from her acknowledgment of the figurehead exchange to the departure order. He asks for a moment.",
        ("I'm glad they understood you.", "We're leaving soon.", "Get ready, please.",)),
    (179, 23): ("Cristina", "They don't look that unusual to me.",
        "Cristina doubts that the ceramic earrings are unusual.",
        "Keep her skeptical question implicit in her delivery before the vendor insists they are special.",
        ("that unusual to me.",)),
    (179, 27): ("Shady Man", None,
        "The vendor chuckles and claims the earrings are no ordinary earrings.",
        "Keep the existing sales-pitch wording. The chuckle and assertion directly answer Cristina's skepticism.",
        ("no ordinary earrings.",)),
    (179, 74): ("Shady Man", "9,000 gold. I'm practically giving them away. I won't take a coin less.",
        "The vendor demands 9,000 gold, calls it a bargain and refuses to reduce it at all.",
        "Preserve the amount and refusal after Maria says she will buy. He praises her judgment when he gives her the earrings.",
        ("9,000 gold.", "giving them away.", "I won't take a coin less.",)),
    (180, 24): ("Emilio", "Dunno... They say the Minotaur once lived here. That's all I know.",
        "Emilio does not know the location beyond the story that the Minotaur once lived on the island.",
        "Use his candid admission after Maria asks where to look. She treats it as a difficult lead.",
        ("the Minotaur", "That's all I know.",)),
    (181, 31): ("Cristina", "You think so? Then I'll have to get even stronger, just like her.",
        "Cristina responds to being compared to the woman pirate and resolves to get stronger in emulation of her.",
        "Keep Cristina's delight at the comparison before the old man suggests the pirate's sword.",
        ("You think so?", "get even stronger,", "just like her.",)),
    (182, 26): ("Yukihisa", "I have news of Muramasa. This legendary cursed blade is said to be the bane of Tokugawa, ruler of Japan. They seek to destroy every one of these fine swords.",
        "In a formal letter Yukihisa reports hearing of the famous accursed blade, said to be a bane to Japan's ruler Tokugawa. The blades are threatened with eradication.",
        "Preserve his slightly old-fashioned letter voice and the reported association. The next paragraph says one sword may have been hidden by a hostile clan.",
        ("I have news of Muramasa.", "legendary cursed blade", "the bane of Tokugawa,", "ruler of Japan.", "these fine swords.",)),
    (182, 32): ("Yukihisa", "I have no doubt this is the blade I have sought all these years. -- Yukihisa Genjo Shiraki",
        "He is sure this is the blade he has sought for years and signs the letter.",
        "Keep his certainty and use a separate signature line, supported by the blank and signature in the Japanese letter. The crew then remarks on his elaborate writing.",
        ("I have no doubt", "sought all these years.", "-- Yukihisa Genjo Shiraki",)),
    (183, 37): ("Al", "I couldn't learn where he hid it. Let's look if we get the chance.",
        "Al did not get as far as learning the hiding place and suggests looking when they can.",
        "Keep Al's practical response to Maria's question about where the sword ended up.",
        ("where he hid it.", "if we get the chance.",)),
    (184, 27): ("Cristina", "Oh! Where to? Look, they're carrying something!",
        "Cristina asks where the birds are going and suddenly sees that they are carrying something.",
        "Use the audible flap as the lead and keep the realization ahead of the following observation about direction.",
        ("Where to?", "they're carrying something!",)),
    (185, 57): ("Guildmaster", "Actually, I heard a rumor. Zhao Yun's legendary spear is supposed to be somewhere on the peninsula near here.",
        "The guildmaster has heard that the legendary spear Zhao Yun used is somewhere on a nearby peninsula.",
        "Let the legend turn into a local lead after the story of Changban. The guildmaster follows with the story of his own unsuccessful search.",
        ("Zhao Yun's legendary spear", "the peninsula near here.",)),
    (186, 44): ("Mysterious Old Man", "My family descends from that retainer. We've waited for the ruler of the seas...",
        "The man's family descends from the retainer and has waited for the ruler of the seas.",
        "Keep the link with the emperor's instructions before the man identifies Maria as the person he awaited.",
        ("from that retainer.", "the ruler of the seas...",)),
    (187, 67): ("Janus", "I'll write if I hear anything else. -- Janus Pasar",
        "Janus promises to write if he learns anything else, then signs the letter.",
        "Use the established Janus sign-off. Keep his signature separate as shown in the clean letter, before Maria speaks.",
        ("I'll write if I hear anything else.", "-- Janus Pasar",)),
    (187, 74): ("Maria", "A traitor's sword... Trust Janus to point out the sword itself did nothing wrong. How practical of him.",
        "Maria recognizes Janus's practical view that the sword itself bears no guilt for its owner's betrayal.",
        "Let her comment echo his letter and set up Manuel's own religious reservation without inventing beliefs for Janus.",
        ("A traitor's sword...", "did nothing wrong.", "How practical of him.",)),
    (188, 53): ("Maria", "A weapon named for a demon king... Thanks for the tip. I'll look for it.",
        "Maria repeats that the weapon bears a demon king's name, thanks the speaker and says she will look.",
        "Keep Iceland tentative in the preceding line and let her respond to the lead rather than identify a location as fact.",
        ("named for a demon king...", "Thanks for the tip.", "I'll look for it.",)),
    (193, 7): ("Lucia", "Welcome, Julian. Smooth as ever.",
        "Lucia greets Julian and jokes that he is as glib as ever.",
        "Keep her amused familiarity in response to his elaborate compliment, before he changes the subject.",
        ("Smooth as ever.",)),
    (193, 26): ("Julian", "Oh, sorry. Bit sudden, wasn't it? I just heard about some armor called the Empress Gown.",
        "Julian apologizes for the abrupt remark and explains it slipped out after hearing about the Empress Gown armor.",
        "Preserve his self-conscious correction and the complete item name so Lucia's next question reads clearly.",
        ("Bit sudden, wasn't it?", "the Empress Gown.",)),
    (197, 45): ("Julian", "Aw, so cold. Even that's part of your charm... Well, I'd better go. See you.",
        "Julian affectionately teases her cold manner, says that is part of her charm and takes his leave.",
        "Keep the affectionate teasing after her dry remark about his turning to stone. She returns his farewell.",
        ("part of your charm...", "I'd better go.",)),
}


pair_source = checked_text(previous.get_source, {
    'extras = {712} if block == 87 else set()': 'extras = set()',
    """            if en['offset'] not in leads:
                continue
            lead = leads[en['offset']]
            assert en['raw_hex'][2:] == lead['stored_body_hex'] and en['selector'] == lead['source_selector']""":
        """            linked = EXTRA.get((block, ja['record_index']))
            if linked is None:
                if en['offset'] not in leads:
                    continue
                lead = leads[en['offset']]
                assert en['raw_hex'][2:] == lead['stored_body_hex'] and en['selector'] == lead['source_selector']
            else:
                offset, anchor = linked
                assert en['offset'] == offset and offset not in leads
                assert anchor in bytes.fromhex(en['raw_hex'])[1:]""",
})
env = previous.get_exchanges.__globals__ | globals()
exec(compile(pair_source, __file__ + '::original-Maria-commands-and-linked-quotes', 'exec'), env)
get_exchanges = env['get_exchanges']

compile_rows = FunctionType(previous.compile_rows.__code__, previous.compile_rows.__globals__ | globals()
                            | {'previous': initial_names})
bind_runtime = FunctionType(previous.bind_runtime.__code__, previous.bind_runtime.__globals__ | globals())
main = FunctionType(previous.main.__code__, previous.main.__globals__ | globals())


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--preview', action='store_true')
    main(parser.parse_args().preview)

