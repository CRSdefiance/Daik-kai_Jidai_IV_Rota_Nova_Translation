"""Restore the three native blizzard alerts replaced by placeholder fragments."""

import json
from pathlib import Path

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from dk4tool.script.common_message_table import common_message_entries

TEXT = {
    389: ('Admiral, a blizzard has started!',
          'A formal crew member tells the admiral that the weather has become a blizzard.'),
    390: ("Admiral, we've hit a blizzard!",
          'A casual crew member tells the admiral that the weather has become a blizzard, with a dismayed tone.'),
    391: ('Admiral, a blizzard!',
          'A blunt crew member alerts the admiral to a blizzard.'),
}


def main():
    clean = NdsImage.open('work/clean.nds')
    if sha(Path('work/clean.nds').read_bytes()) != 'f4f07c975cc293f5b2ba469747693d3dd37f2e6dfc408cf5910adf5e83d9177d':
        raise ValueError('Exact clean source is required')
    entries = common_message_entries(clean.read_file('/COMMON/MESFILE.DK4'), clean.read_file('/__arm9__.bin'))
    owners = {(entries[i].block, entries[i].record_index) for i in TEXT}
    selected = [e for e in entries if (e.block, e.record_index) in owners]
    if {e.message_id for e in selected} != set(TEXT) or owners != {(5, 30)}:
        raise ValueError('Complete blizzard owner changed')
    rows = []
    for entry in selected:
        english, meaning = TEXT[entry.message_id]
        rows.append({
            'id': f'COMMON_MESSAGE_{entry.message_id}', 'message_id': entry.message_id,
            'block': entry.block, 'record': entry.record_index,
            'source_hex': entry.text.hex().upper(), 'japanese': entry.text.decode('cp932'),
            'previous_japanese': entries[entry.message_id - 1].text.decode('cp932'),
            'next_japanese': entries[entry.message_id + 1].text.decode('cp932'),
            'english': english + '{PAD}', 'source_meaning': meaning,
            'speaker': 'Crew member selected by actor speech category',
            'context': 'Native blizzard warning table 02118980, selected at 02030B10 when r5 equals 3 through wrapper 02053F0C. All three selections in clean B5 R30 are included. Adjacent messages are storm and other blizzard variants; no story/letter/faction message belongs here.',
            'localization_note': 'Fresh Japanese-source English restores the weather warning and the explicit Admiral address. Formal, casual and blunt variants retain their tone. No ship damage, navigation advice or trapped-state claim is added. One logical paragraph; no manual alignment or line breaks.',
            'review': {'source': True, 'context': True, 'localization': True,
                       'naturalness': True, 'formatting': False},
        })
    payload = {'format': 'dk4-common-entry-manuscript-v1',
               'translation_policy': 'natural-dialogue-v2', 'target_locale': 'en-US',
               'encoder': 'dialogue-fixed-v1',
               'review_gates': ['source', 'context', 'localization', 'naturalness', 'formatting'],
               'status': 'draft-native-preview-and-repacking-review-pending', 'records': rows}
    Path('translations/common_blizzard_repair_manuscript_v2.json').write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print('Prepared three complete-owner, clean-source blizzard alerts.')


if __name__ == '__main__':
    main()
