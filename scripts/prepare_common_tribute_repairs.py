"""Restore tribute direction, monthly timing and coin units from Japanese."""

import json
from pathlib import Path

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from dk4tool.script.common_message_table import common_message_entries

TEXT = {
    76: ("This month's tribute is %s gold coins. Please accept it.", 'States this month\'s tribute amount in gold coins and politely asks the recipient to accept it.'),
    77: ("This month's tribute is %s gold coins. Please accept it...", 'States this month\'s tribute amount in gold coins and asks the recipient to accept it, with trailing hesitation.'),
    78: ("The tribute for this month is %s gold coins.", 'States this month\'s tribute amount in gold coins; no request follows.'),
    79: ("This month's tribute comes to %s gold coins.", 'States this month\'s tribute amount in gold coins in a conversational voice.'),
    80: ("Here's the tribute for this month: %s gold coins.", 'Casually announces this month\'s tribute amount in gold coins.'),
    81: ("This month's tribute is %s gold coins. Go on, please accept it.", 'An older, inviting voice states this month\'s tribute amount and urges the recipient to accept it.'),
    82: ("Please accept this month's tribute of %s gold coins.", 'Politely invites the recipient to accept this month\'s tribute, retaining the gold-coin amount.'),
    83: ("Towns under %s's exclusive contracts paid %s gold coins in tribute.", 'Reports accumulated tribute from towns under the first named party\'s exclusive contracts, followed by the gold-coin amount. The Japanese town noun is not singular-marked; the native caller accumulates up to ninety town contributions and announces once per beneficiary. The first argument is the contract holder and the second is money.'),
}


def main():
    path = Path('work/clean.nds')
    if sha(path.read_bytes()) != 'f4f07c975cc293f5b2ba469747693d3dd37f2e6dfc408cf5910adf5e83d9177d':
        raise ValueError('Exact clean source required')
    clean = NdsImage.open(path)
    entries = common_message_entries(clean.read_file('/COMMON/MESFILE.DK4'), clean.read_file('/__arm9__.bin'))
    owners = {(entries[i].block, entries[i].record_index) for i in TEXT}
    selected = [e for e in entries if (e.block, e.record_index) in owners]
    if {e.message_id for e in selected} != set(TEXT) or owners != {(0, n) for n in range(58, 63)}:
        raise ValueError('Complete tribute owners differ')
    rows = []
    for e in selected:
        english, meaning = TEXT[e.message_id]
        rows.append({'id': f'COMMON_MESSAGE_{e.message_id}', 'message_id': e.message_id,
                     'block': e.block, 'record': e.record_index,
                     'source_hex': e.text.hex().upper(), 'japanese': e.text.decode('cp932'),
                     'previous_japanese': entries[e.message_id - 1].text.decode('cp932'),
                     'next_japanese': entries[e.message_id + 1].text.decode('cp932'),
                     'english': english.replace('I', 'Ｉ').replace('F', 'Ｆ') + '{PAD}',
                     'source_meaning': meaning,
                     'speaker': 'Tribute report narrator' if e.message_id == 83 else 'Representative offering tribute',
                     'context': 'Complete native owners B0 R58-R62. For IDs 76-82, table 021189C0 is selected at 0202DE94; the preceding code subtracts tribute from the paying faction and credits the player before announcing it. お納めください means accept the offered tribute, not pay a bill. The separate two-argument town notice 83 shares R62: caller 020B25A8 reports an accumulated town total and passes the current player faction name before the amount. The player name editor allows eighteen bytes. Expanded window layout remains unapproved.',
                     'localization_note': 'Fresh natural American English restores receiving direction, monthly timing and gold-coin units. Retains each source variant\'s politeness, hesitation, neutral statement or older invitation. The packed town notice retains the exclusive-contract relationship and original name/amount argument order. No manual wrapping; runtime expansions await formatting review.',
                     'review': {'source': True, 'context': True, 'localization': True,
                                'naturalness': True, 'formatting': False}})
    payload = {'format': 'dk4-common-entry-manuscript-v1',
               'translation_policy': 'natural-dialogue-v2', 'target_locale': 'en-US',
               'encoder': 'dialogue-fixed-v1',
               'review_gates': ['source', 'context', 'localization', 'naturalness', 'formatting'],
               'status': 'draft-awaiting-native-runtime-substitution-layout-review', 'records': rows}
    Path('translations/common_tribute_repairs_manuscript_v2.json').write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print('Prepared eight complete-owner tribute messages; runtime formatting remains unapproved.')


if __name__ == '__main__':
    main()
