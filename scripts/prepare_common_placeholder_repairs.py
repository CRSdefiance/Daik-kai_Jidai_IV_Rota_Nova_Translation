"""Restore every remaining instance of the generic COMMON placeholder in V141."""

import json
from pathlib import Path

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from dk4tool.script.common_message_table import common_message_entries

TEXT = {
    344: ('The Age of Discovery brought immense change to the world from the Middle Ages into the early modern era...',
          'The Age of Discovery brought great transformations to the world from the medieval to early modern period; the narration continues into the next message about its legends being passed down.', 'Ending narrator'),
    396: ('Admiral, this is serious! It looks like our sailors have scurvy!',
          'Urgently addresses the admiral: the sailors appear to have contracted scurvy.', 'Crew member'),
    397: ('Admiral, it looks like the sailors have scurvy!',
          'Addresses the admiral and reports that the sailors apparently have scurvy.', 'Crew member'),
    416: ('Admiral, please look at the sky!', 'Politely asks the admiral to look at the sky.', 'Crew member'),
    417: ('Admiral, look at the sky!', 'Asks the admiral to look at the sky.', 'Crew member'),
    418: ('Admiral, look at the sky!', 'Asks the admiral to look at the sky; identical Japanese to the preceding variant.', 'Crew member'),
    419: ('Admiral, take a look at the sky!', 'Casually asks the admiral to look at the sky.', 'Crew member'),
    424: ("Fog's starting to roll in...", 'Fog is starting to appear; preserve the trailing hesitation.', 'Crew member'),
    425: ('Fog... Visibility will be poor.', 'Notes the fog and warns that visibility will become poor.', 'Crew member'),
    426: ('Damn, fog is rolling in.', 'Roughly complains that fog has appeared; the curse localizes the coarse emphasis.', 'Crew member'),
}


def main():
    path = Path('work/clean.nds')
    if sha(path.read_bytes()) != 'f4f07c975cc293f5b2ba469747693d3dd37f2e6dfc408cf5910adf5e83d9177d':
        raise ValueError('Exact clean source required')
    clean = NdsImage.open(path)
    entries = common_message_entries(clean.read_file('/COMMON/MESFILE.DK4'), clean.read_file('/__arm9__.bin'))
    owners = {(entries[i].block, entries[i].record_index) for i in TEXT}
    selected = [e for e in entries if (e.block, e.record_index) in owners]
    if {e.message_id for e in selected} != set(TEXT) or owners != {(5, 0), (5, 35), (5, 53), (5, 57)}:
        raise ValueError('Complete placeholder owners differ')
    rows = []
    for e in selected:
        english, meaning, speaker = TEXT[e.message_id]
        rows.append({'id': f'COMMON_MESSAGE_{e.message_id}', 'message_id': e.message_id,
                     'block': e.block, 'record': e.record_index,
                     'source_hex': e.text.hex().upper(), 'japanese': e.text.decode('cp932'),
                     'previous_japanese': entries[e.message_id - 1].text.decode('cp932'),
                     'next_japanese': entries[e.message_id + 1].text.decode('cp932'),
                     'english': english.replace('I', 'Ｉ').replace('F', 'Ｆ') + '{PAD}',
                     'source_meaning': meaning, 'speaker': speaker,
                     'context': 'Complete native owner restored from Japanese after a generic story/letter/faction placeholder was split across unrelated native selections. Ending narration 344 continues into 345, whose full existing text remains unchanged. Other records are crew-category warning variants; no named speaker or unsupported weather phenomenon is inferred.',
                     'localization_note': 'Natural American English preserves the historical periods, urgent versus neutral scurvy reports and their uncertainty, explicit sky rather than a guessed phenomenon, and fog/visibility/coarse emphasis. Identical Japanese retains identical English. One paragraph per native ID; formatter owns wrapping. Safe full-width I/F preserve the established shared renderer convention.',
                     'review': {'source': True, 'context': True, 'localization': True,
                                'naturalness': True, 'formatting': False}})
    payload = {'format': 'dk4-common-entry-manuscript-v1',
               'translation_policy': 'natural-dialogue-v2', 'target_locale': 'en-US',
               'encoder': 'dialogue-fixed-v1',
               'review_gates': ['source', 'context', 'localization', 'naturalness', 'formatting'],
               'status': 'draft-awaiting-native-previews-and-repacking-review', 'records': rows}
    Path('translations/common_placeholder_repairs_manuscript_v2.json').write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print('Prepared ten faithful native messages across four complete placeholder owners.')


if __name__ == '__main__':
    main()
