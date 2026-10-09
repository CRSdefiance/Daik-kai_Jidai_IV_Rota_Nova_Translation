"""Prepare complete native treasure-map clues and adjacent artifact rumors."""
import json
from pathlib import Path

from dk4tool.rom.nds import NdsImage
from dk4tool.script.common_message_table import common_message_entries

LOCATIONS = {
    '新大陸': ('the New World', 'New World'),
    '北海': ('the North Sea', 'North Sea'),
    '地中海': ('the Mediterranean', 'Mediterranean'),
    'アフリカ': ('Africa', 'Africa'),
    'インド洋': ('the Indian Ocean', 'Indian Ocean'),
    '東南アジア': ('Southeast Asia', 'Southeast Asia'),
    '東アジア': ('East Asia', 'East Asia'),
}
REGION_TEXT = {
    '新大陸': 'The hidden treasure lies in New World waters.',
    '北海': 'The North Sea holds the hidden treasure.',
    '地中海': 'The waters of the Mediterranean hold the hidden treasure.',
    'アフリカ': 'African waters hold the hidden treasure.',
    'インド洋': 'The Indian Ocean holds the hidden treasure.',
    '東南アジア': 'Southeast Asian seas hold the hidden treasure.',
    '東アジア': 'East Asian waters hold the hidden treasure.',
}
DIRECTIONS = {
    'そのやや北にて': ('A little north of there.', 'Slightly north of the previously indicated region.'),
    'その中央にて': ('At its center.', 'At the center of the previously indicated region.'),
    'はるか北東へ向い': ('Head far northeast.', 'Travel far to the northeast.'),
    'はるか北西へ向い': ('Head far northwest.', 'Travel far to the northwest.'),
    'その北西にて': ('To its northwest.', 'Northwest of the previously indicated region.'),
    'はるか北へ向い': ('Head far north.', 'Travel far north.'),
    'はるか西へ向い': ('Head far west.', 'Travel far west.'),
    'そのやや南にて': ('A little south of there.', 'Slightly south of the previously indicated region.'),
    'その南東にて': ('To its southeast.', 'Southeast of the previously indicated region.'),
    'その西にて': ('To its west.', 'West of the previously indicated region.'),
    'その真南にて': ('Due south of there.', 'Directly south, retaining the precise due-south direction.'),
    'そのやや西にて': ('A little west of there.', 'Slightly west of the previously indicated region.'),
    'はるか南へ向い': ('Head far south.', 'Travel far south.'),
    'その北東にて': ('To its northeast.', 'Northeast of the previously indicated region.'),
}
TEXT = {
    3607: ('Seek the spot marked X.', 'Imperative: explore the location marked with an X.'),
    3648: ("It is a warrior's talisman, granting a lion's might to defeat powerful foes.", 'A warrior\'s protective talisman that grants the strength of a lion to overcome powerful enemies.'),
    3649: ('It is a weapon against evil. In ancient times, it was used in rites to drive away demons.', 'An evil-banishing weapon used in demon-exorcising rituals in ancient times.'),
    3650: ("It is the serpent god's mask. They say the serpent's magic protects warriors.", 'The mask of a serpent deity, said to protect warriors through the serpent\'s magic.'),
    3651: ("It is a magic marksman's treasure. They say whoever carries it never misses a shot.", 'The treasure of a marksman who uses magical bullets. It is said that the bearer never misses their aim; preserve the reported claim.'),
    3652: ('This treasure strengthens the mind. They say someone amassed a vast fortune with its help.', 'A treasure that increases mental or inner strength; someone is said to have accumulated immense wealth through it.'),
    3653: ('It is a fearsome weapon. Legend says it can cut things without touching them.', 'A frightening weapon traditionally said to sever objects without contact.'),
    3654: ('A symbol of destruction, its magic sank all opposing ships.', 'A symbol of destruction whose magic sank all opposing ships; preserve the past-tense claim in the inscription.'),
    3655: ('This oddly shaped horn has the power to ward off every disease.', 'A horn of unusual shape possessing the power to repel every illness.'),
    3656: ("This royal shield wards off misfortune through the goddess's blessing.", 'A royal shield with a goddess\'s protection and the power to avert disasters or misfortune.'),
    3657: ('A great red spear, this weapon has the power to drive evil away.', 'An evil-banishing weapon, specifically a large red spear with the power to repel evil.'),
    3658: ("It's said to be a strange jewel colored like blazing flames.", 'Apparently a mysterious jewel whose color resembles burning flames.'),
    3659: ('They say this dagger is ancient and bears an inscription. I doubt anyone can still read it.', 'Said to be a very ancient dagger with an inscription. The speaker doubts that anyone can read it in the present day; this is uncertainty rather than a proven unreadable language.'),
    3660: ("I hear priests used this stone mask long ago; it's carved with an eerie serpent pattern.", 'Reportedly a stone mask used by ancient priests and engraved with an unsettling serpent design.'),
    3661: ("It's a crimson crystal. Look through it, and a star-shaped pattern is said to appear inside.", 'A crimson crystal in which a star-shaped design reportedly appears when viewed through the crystal.'),
    3662: ("It's said to be a strange crystal containing a diamond. A jewel that eats jewels, they call it.", 'Reportedly a mysterious crystal containing a diamond, nicknamed a jewel that consumes jewels.'),
    3663: ('They say the blade is remarkably sharp. Whether true or not, it can cut things without making contact.', 'Apparently a very sharp sword; whether true or false, it is said to sever things without contact. Preserve the speaker\'s doubt.'),
    3664: ("They say it's a siren statue once used as a figurehead. I can't believe anyone would use a witch who causes shipwrecks!", 'Reportedly a siren statue used as a ship\'s figurehead. The speaker is incredulous at using an image of a witch that causes maritime disasters.'),
    3665: ("They say it's a twisted horn. Some say it's a dragon's. Rumor claims it can make medicine effective against every illness.", 'Reportedly a twisted horn, with some saying it belongs to a dragon and rumors claiming it can be made into medicine effective against every illness.'),
    3666: ("It's said to be a great king's shield, bearing a goddess's image. Sailors call it their finest talisman.", 'Apparently the shield of a great king, reportedly bearing a goddess\'s image and said to be the best protective charm for sailors.'),
    3667: ("I hear it's an enormous spear capable of driving evil away.", 'Reportedly an exceptionally large spear with the power to repel evil.'),
}


def main():
    clean = NdsImage.open('work/clean.nds')
    entries = common_message_entries(clean.read_file('/COMMON/MESFILE.DK4'),
                                     clean.read_file('/__arm9__.bin'))
    for i in range(3608, 3628):
        source = entries[i].text.decode('cp932')
        for japanese, (english, gloss) in LOCATIONS.items():
            if source == f'秘宝が眠るは{japanese}の海域なり':
                TEXT[i] = (REGION_TEXT[japanese],
                           f'The secret treasure lies in the {gloss} sea region.')
                break
            if source == f'秘宝を得たくば{japanese}より出で' or source == f'秘宝を得たくば{japanese}の海より出で':
                TEXT[i] = (f'Depart from {english} if you seek the treasure.',
                           f'To obtain the secret treasure, depart from the {gloss} sea region; a point of departure, not a claim that the treasure lies there.')
                break
        else:
            raise ValueError(f'Unreviewed region clue {i}: {source}')
    for i in range(3628, 3648):
        TEXT[i] = DIRECTIONS[entries[i].text.decode('cp932')]
    assert set(TEXT) == set(range(3607, 3668))
    owners = {(entries[i].block, entries[i].record_index) for i in TEXT}
    selected = [e for e in entries if (e.block, e.record_index) in owners]
    assert {e.message_id for e in selected} == set(TEXT)
    rows = []
    for e in selected:
        english, meaning = TEXT[e.message_id]
        inscription = e.message_id < 3658
        rows.append({
            'id': f'COMMON_MESSAGE_{e.message_id}', 'message_id': e.message_id,
            'block': e.block, 'record': e.record_index,
            'source_hex': e.text.hex().upper(), 'japanese': e.text.decode('cp932'),
            'previous_japanese': entries[e.message_id - 1].text.decode('cp932'),
            'next_japanese': entries[e.message_id + 1].text.decode('cp932') if e.message_id + 1 < len(entries) else '',
            'english': english.replace('I', 'Ｉ').replace('F', 'Ｆ') + '{PAD}',
            'source_meaning': meaning,
            'speaker': 'Treasure-map inscription' if inscription else 'Unnamed artifact rumor informant',
            'context': (f'Native message {e.message_id}, clean B39 R{e.record_index}. '
                        'ARM9 0x10338C/0x1033E4/0x10342C/0x10346C select the map inscription, '
                        'sea-region clue, relative direction and X instruction through the native '
                        'accessor using tables at 0x12F6FC/0x12F724/0x12F774/0x12F660. '
                        'Adjacent final ten messages are casual artifact rumors; their speaker '
                        'identity is not inferred. Every native neighbor in each owner is included.'),
            'localization_note': ('Fresh clean-source American English retains named sea regions, '
                                  'departure versus destination, slightly/far/due directions, all '
                                  'artifact properties and explicit legend/hearsay/doubt. Map directions '
                                  'remain independently selected fragments with their source reference. '
                                  'No invented artifact names, certainty or speaker identity. One '
                                  'paragraph per native ID; safe full-width I/F. Previews await review.'),
            'review': {'source': True, 'context': True, 'localization': True,
                       'naturalness': True, 'formatting': False},
        })
    payload = {'format': 'dk4-common-entry-manuscript-v1',
               'translation_policy': 'natural-dialogue-v2', 'target_locale': 'en-US',
               'encoder': 'dialogue-fixed-v1',
               'review_gates': ['source', 'context', 'localization', 'naturalness', 'formatting'],
               'status': 'draft-awaiting-reblocking-and-formatting-review', 'records': rows}
    Path('translations/common_b39_treasure_clues_manuscript_v2.json').write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(f'Prepared {len(rows)} complete-owner treasure clues and artifact rumors')


if __name__ == '__main__':
    main()
