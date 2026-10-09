"""Prepare clean-source officer duties, figurehead effects, gifts and Proofs of Conquest."""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from dk4tool.rom.nds import NdsImage
from dk4tool.script.common_message_table import common_message_entries

TEXT = {
    3120: ("An adjutant's duties include persuading disgruntled sailors and negotiating with other factions.", 'Both persuading discontented sailors and conducting negotiations with other factions are adjutant duties.'),
    3121: ("An adjutant's grasp of world geography can bring peace of mind on a voyage.", 'Having an adjutant with strong knowledge of world geography would make voyages reassuring.'),
    3124: ('A boarding chief you can rely on must be skilled with a sword and know how to fight.', 'A truly dependable boarding chief excels in swordsmanship and knows combat tactics.'),
    3125: ('A boarding chief you can rely on must be skilled with a sword and know how to fight.', 'A truly dependable boarding chief excels in swordsmanship and knows combat tactics.'),
    3126: ('Unseen luck also plays a major part in gunnery ability.', 'Invisible luck contributes greatly to gunnery ability as well.'),
    3136: ('Dress like a cook, and somehow you feel as though you could make delicious food.', 'Dressing like a cook mysteriously creates confidence that one can prepare tasty food; subjective feeling, not guaranteed ability.'),
    3137: ('Tending livestock is hard work. Even a little relief would be welcome.', 'Livestock care is demanding work; wishes to ease the labor even slightly.'),
    3152: ('Fit it to any ship, and the whole fleet benefits. They say it increases our discovery range.', 'Regardless of ship fitted, effect covers the entire fleet; reportedly widens the range within which discoveries are possible.'),
    3153: ('It should work on any ship. It seems to refresh the spirit and ease fatigue...', 'Expects effect on any ship; apparently purifies or refreshes the mind and relieves fatigue.'),
    3154: ('Hmm... Once this is installed, you cannot transfer it to another ship.', 'Warns that after installation the item cannot be moved to a different ship.'),
    3155: ("This seems useful in close combat. I'd fit it to a ship carrying plenty of sailors.", 'Recommends installation on a ship with many sailors; expects an effect in close-quarters combat.'),
    3156: ("Any ship should gain the heavens' protection. It seems this could prevent illness.", 'Expects heavenly protection on any ship; apparently prevents contracting disease.'),
    3157: ('A very useful tool for a surveyor.', 'Describes item as highly beneficial to a surveyor.'),
    3165: ('Arabian clothing looks quite mysterious to Europeans.', 'Arabian dress appears mysterious to Europeans; preserves the source cultural viewpoint.'),
    3166: ("Beautiful poetry. Around Mediterranean shores, romantic tales about ancient Greece's glory are well known.", 'Praises poetry and says ancient Greek splendor is well known in the Mediterranean as romantic tales.'),
    3171: ('In a tavern in an Indian Ocean town, I recall hearing of a woman learning to dance.', 'Recalls hearing at an Indian Ocean town tavern about a woman learning to dance; no town name invented.'),
    3172: ('I hear a fleet from the East once reached East Africa and explained that jade brings good luck.', 'Hearsay that an Eastern fleet arrived in East Africa in the past and conveyed that jade is auspicious.'),
    3175: ('Beautiful indeed... Westerners find its true worth hard to appreciate.', 'Acknowledges beauty and says Westerners have difficulty appreciating the item true merits.'),
    3176: ('An exquisite piece of craftsmanship. Carpets are very popular in East Asia too.', 'Praises elaborate workmanship and notes carpets are very popular in East Asia as well.'),
    3177: ('Made from fine silk, I see. People from the East would probably appreciate it too.', 'Recognizes high quality silk and expects Eastern people would enjoy it as well.'),
    3178: ('Pottery thrives in West Africa. They should recognize the value of this fine piece.', 'West Africa has active pottery production, so its people would likely understand this exceptional item value.'),
    3179: ("It seems hard to get Europe's latest tools in the New World.", 'Apparently difficult to acquire the newest European instruments or tools in the New World.'),
    3180: ('A beautiful feather. They say many women in the New World are very fond of animals.', 'Praises a feather and reports that many New World women love animals; retains hearsay.'),
    3181: ("The North Sea's Proof of Conquest.", 'Identifies the proof of the North Sea conqueror.'),
    3182: ("Here we have the Mediterranean's Proof of Conquest.", 'Identifies the proof of the Mediterranean conqueror.'),
    3183: ("Africa's Proof of Conquest.", 'Identifies the proof of the African conqueror.'),
    3185: ("Southeast Asia's Proof of Conquest.", 'Identifies the proof of the Southeast Asian conqueror.'),
    3186: ("East Asia's Proof of Conquest.", 'Identifies the proof of the East Asian conqueror.'),
    3187: ("The New World's Proof of Conquest.", 'Identifies the proof of the New World conqueror.'),
    3188: ("It marks the location of the North Sea's Proof of Conquest.", 'Says the location of the North Sea proof is marked on this item.'),
}


def main():
    clean = NdsImage.open('work/clean.nds')
    entries = common_message_entries(clean.read_file('/COMMON/MESFILE.DK4'),
                                     clean.read_file('/__arm9__.bin'))
    owners = {(entries[i].block, entries[i].record_index) for i in TEXT}
    selected = [e for e in entries if (e.block, e.record_index) in owners]
    assert {e.message_id for e in selected} == set(TEXT)
    rows = []
    for e in selected:
        english, meaning = TEXT[e.message_id]
        rows.append({
            'id': f'COMMON_MESSAGE_{e.message_id}', 'message_id': e.message_id,
            'block': e.block, 'record': e.record_index,
            'source_hex': e.text.hex().upper(), 'japanese': e.text.decode('cp932'),
            'previous_japanese': entries[e.message_id - 1].text.decode('cp932'),
            'next_japanese': entries[e.message_id + 1].text.decode('cp932'),
            'english': english.replace('I', 'Ｉ').replace('F', 'Ｆ') + '{PAD}',
            'source_meaning': meaning,
            'speaker': 'Older naturalist advising on trade goods, items and crew roles',
            'context': (f'Independent native message {e.message_id}, clean COMMON B35 '
                        f'R{e.record_index}; officer duties, figurehead effects, gifts and Proofs of Conquest. '
                        'All native selections in each selected source owner are included.'),
            'localization_note': ('Fresh clean-source American English preserves adjutant and boarding-chief '
                                  'duties, luck, subjective confidence from cook clothing, livestock workload, '
                                  'whole-fleet discovery range versus effects on any fitted ship, one-time '
                                  'installation restrictions, sailor counts, close combat, fatigue and disease '
                                  'uncertainty, cultural gift advice, remembered tavern hearsay, jade good luck '
                                  'and regional Proof identity versus a marked location. No invented town, '
                                  'guaranteed effect or recipient. One paragraph; safe full-width I/F. '
                                  'Exact-font previews await review.'),
            'review': {'source': True, 'context': True, 'localization': True,
                       'naturalness': True, 'formatting': False},
        })
    payload = {'format': 'dk4-common-entry-manuscript-v1',
               'translation_policy': 'natural-dialogue-v2', 'target_locale': 'en-US',
               'encoder': 'dialogue-fixed-v1',
               'review_gates': ['source', 'context', 'localization', 'naturalness', 'formatting'],
               'status': 'draft-awaiting-reblocking-and-formatting-review', 'records': rows}
    Path('translations/common_japanese_b35_manuscript_v1.json').write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(f'Prepared {len(rows)} clean-source native messages')


if __name__ == '__main__':
    main()
