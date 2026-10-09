"""Prepare clean-source map identification, Proof-location clues and item advice."""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from dk4tool.rom.nds import NdsImage
from dk4tool.script.common_message_table import common_message_entries

TEXT = {
    3201: ('An Indochinese kingdom, it seems.', 'Tentatively identifies what is depicted as an Indochinese kingdom.'),
    3202: ('Head north overland from Hangzhou.', 'Recommends traveling north by land from Hangzhou.'),
    3204: ('Begin your expedition from Osaka.', 'Recommends beginning exploration from Osaka.'),
    3205: ('A Caribbean island is shown here.', 'Identifies the island depicted as a Caribbean island.'),
    3207: ("It may show where the North Sea's Proof of Conquest lies. I can't make it out from this alone.", 'Possibly indicates the North Sea proof location, but this alone cannot be understood.'),
    3208: ("This must mark the Mediterranean's Proof of Conquest. But it cannot be deciphered on its own.", 'Confidently identifies a record of the Mediterranean proof location, but this alone is indecipherable.'),
    3209: ("This probably marks Africa's Proof of Conquest. But with only half, I can't make it out...", 'Likely records the African proof location, but only half is available and cannot be understood.'),
    3210: ('The Proof of Conquest in the Indian Ocean... I believe this records its location in some form.', 'Thinks it indicates the Indian Ocean proof location in some unspecified form; retains uncertainty.'),
    3211: ("This is probably needed to find Southeast Asia's Proof of Conquest.", 'Probably necessary to discover the Southeast Asian proof.'),
    3216: ("This probably marks Africa's Proof of Conquest. But with only half...", 'Likely records the African proof location, but only half is insufficient; unfinished thought preserved.'),
    3217: ("This seems linked to something showing where the Indian Ocean's Proof of Conquest lies.", 'Apparently related to an object indicating the Indian Ocean proof location; does not identify the object as a specific map.'),
    3226: ('Now this is a magic sword. Hmm... The longer I look at it, the more it draws me in.', 'Identifies a magical sword and feels increasingly captivated when looking at it; exact counterpart to 3081.'),
    3227: ('What a lovely mermaid figurine! Give it to the gunner.', 'Praises a beautiful mermaid statuette and recommends giving it to the gunner.'),
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
            'context': (f'Independent native message {e.message_id}, clean COMMON B36 '
                        f'R{e.record_index}; map identification, Proof-location clues and item advice. '
                        'All native selections in each selected source owner are included.'),
            'localization_note': ('Fresh clean-source American English preserves Indochina, Hangzhou, '
                                  'Osaka and the Caribbean; overland northward travel; uncertain versus '
                                  'confident regional Proof-location identification; insufficient half-documents '
                                  'and clues to other objects; magic-sword fascination and gunner assignment. '
                                  'No invented map completion or precise treasure location. The packed BGM '
                                  'and promotional owners are separate and require renderer classification. '
                                  'One paragraph; safe full-width I/F. Exact-font previews await review.'),
            'review': {'source': True, 'context': True, 'localization': True,
                       'naturalness': True, 'formatting': False},
        })
    payload = {'format': 'dk4-common-entry-manuscript-v1',
               'translation_policy': 'natural-dialogue-v2', 'target_locale': 'en-US',
               'encoder': 'dialogue-fixed-v1',
               'review_gates': ['source', 'context', 'localization', 'naturalness', 'formatting'],
               'status': 'draft-awaiting-reblocking-and-formatting-review', 'records': rows}
    Path('translations/common_japanese_b36_advice_manuscript_v1.json').write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(f'Prepared {len(rows)} clean-source native messages')


if __name__ == '__main__':
    main()
