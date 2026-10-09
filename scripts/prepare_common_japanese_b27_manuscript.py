"""Prepare clean-source crew, fleet, accounting and pirate reports."""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from dk4tool.rom.nds import NdsImage
from dk4tool.script.common_message_table import common_message_entries

TEXT = {
    2526: ("Admiral! We can't sail the ship if you dismiss every sailor!", 'Warns the admiral that dismissing every sailor prevents operating the ship.'),
    2527: ("Hey, if you dismiss all the sailors, the ship won't move!", 'Older warning that dismissing every sailor makes the ship inoperable.'),
    2530: ("I can't do my job without this.", 'Cannot perform the job without this item.'),
    2531: ('Oh... I need this to do my job.', 'Feminine realization that this item is necessary to do the job.'),
    2534: ("We've spotted %s's fleet! We're beginning our attack!", "Rough report of spotting the substituted party's fleet and moving to attack."),
    2535: ("%s's fleet sighted! Attack!", "Older report of spotting the substituted party's fleet and an order to attack."),
    2536: ("We found %s's fleet! Let's attack!", "Youthful report of finding the substituted party's fleet and proposing an attack."),
    2537: ("%s's fleet is attacking us!", "Reports the substituted party's fleet beginning an attack on us."),
    2545: ("We've defeated the %s / %s fleet! Victory is ours!", 'Rough report of defeating the paired-identifier fleet and winning; no invented sinking.'),
    2546: ("We've beaten the %s / %s fleet! We've won!", 'Older report of defeating the paired-identifier fleet and winning.'),
    2547: ('We beat the %s / %s fleet! We won!', 'Youthful report of defeating the paired-identifier fleet and winning.'),
    2548: ('The %s / %s fleet has fled!', 'Reports the paired-identifier fleet fleeing.'),
    2555: ('The %s / %s fleet has defeated us...', 'Feminine regretful report that the paired-identifier fleet defeated our side.'),
    2556: ('The %s / %s fleet beat us...', 'Rough regretful report of our side defeated by the paired-identifier fleet.'),
    2557: ('The %s / %s fleet defeated us...', 'Older regretful report of our side defeated by the paired-identifier fleet.'),
    2558: ('We lost to the %s / %s fleet...', 'Youthful disappointment about being defeated by the paired-identifier fleet.'),
    2564: ('The %s / %s fleet was stronger than we thought. Our fleet fled...', 'Youthful report of unexpectedly strong opponents and our own fleet fleeing.'),
    2565: ("I'm sorry. We incurred a loss of %s gold coins.", 'Formal apology for causing a loss of the substituted number of gold coins.'),
    2566: ("I'm sorry. We lost %s gold coins.", 'Informal apology for losing the substituted number of gold coins.'),
    2568: ('Sorry, we lost %s gold coins.', 'Rough apology for losing the substituted number of gold coins.'),
    2569: ("I'm sorry. We suffered a loss of %s gold coins.", 'Older apology for a loss of the substituted number of gold coins.'),
    2570: ('Sorry! I lost you %s gold coins...', 'Youthful apology for causing the listener to lose as many as the substituted number of gold coins.'),
    2571: ('We were able to earn %s gold coins.', 'Reports earnings of the substituted number of gold coins.'),
    2574: ('We made %s gold coins! Hehe!', 'Youthful delight at making the substituted amount of gold coins, followed by a laugh.'),
    2575: ("We don't have enough money to cover the loss, so it'll be added to next month's expenses.", "Insufficient current funds to settle the loss, so it carries into the following month's expense amount."),
    2576: ("We don't have enough money to cover the loss. It'll be carried over into next month's expenses.", "Informal report that available money cannot settle the loss, which carries into next month's expenses."),
    2614: ('We will now attack the town of %s.', 'Formal older announcement of beginning the attack on the substituted town.'),
    2615: ("At %s, we've spotted the pirate %s!", 'Reports sighting the named pirate at the substituted location; location first, pirate second.'),
    2616: ("At %s, we've found the pirate %s!", 'Reports finding the named pirate at the substituted location; location first, pirate second.'),
    2617: ('At %s, we spotted the pirate %s!', 'Rough report of sighting the named pirate; location first, pirate second.'),
    2618: ('At %s, we found the pirate %s!', 'Older report of finding the named pirate; location first, pirate second.'),
    2619: ("Hey, at %s, there's the pirate %s!", 'Youthful call for attention to the named pirate at the substituted location.'),
    2620: ("At %s, we've sighted the pirate %s!", 'Formal older report of sighting the pirate; location first, pirate second.'),
    2625: ("Ho ho ho! We've obtained information on the pirate %s.", 'Older laugh followed by a report of obtaining information on the named pirate.'),
    2626: ('We got information on the pirate %s!', 'Youthful enthusiastic report of obtaining information on the named pirate.'),
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
            'speaker': 'Crew sea-event voice variant or protagonist granting log permission',
            'context': (f'Independent native message {e.message_id}, clean COMMON B27 '
                        f'R{e.record_index}; crew, fleet, accounting and pirate reports. '
                        'All native selections in each selected source owner are included.'),
            'localization_note': ('Fresh clean-source American English retains all-sailor dismissal warnings, '
                                  'item necessity, attacks, victory versus defeat versus flight, apologies, '
                                  'gold-coin counts, earnings, and loss carryover into next month expenses. '
                                  'Pirate sightings keep location first and name second. Paired fleet labels '
                                  'use the established neutral slash in source order; their actual runtime '
                                  'types still need classification. No invented sinking or hierarchy. '
                                  'One paragraph; safe full-width I/F. Exact-font previews await review.'),
            'review': {'source': True, 'context': True, 'localization': True,
                       'naturalness': True, 'formatting': False},
        })
    payload = {'format': 'dk4-common-entry-manuscript-v1',
               'translation_policy': 'natural-dialogue-v2', 'target_locale': 'en-US',
               'encoder': 'dialogue-fixed-v1',
               'review_gates': ['source', 'context', 'localization', 'naturalness', 'formatting'],
               'status': 'draft-awaiting-reblocking-and-formatting-review', 'records': rows}
    Path('translations/common_japanese_b27_manuscript_v1.json').write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(f'Prepared {len(rows)} clean-source native messages')


if __name__ == '__main__':
    main()
