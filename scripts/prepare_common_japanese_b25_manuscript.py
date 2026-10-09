"""Prepare clean-source white-whale, dolphin and sea-hazard reports."""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from dk4tool.rom.nds import NdsImage
from dk4tool.script.common_message_table import common_message_entries

TEXT = {
    2340: ("That's... the white whale we've heard about. I hear many ships have been attacked by it... Admiral, let's defeat it!", 'Identifies the rumored white whale, hearsay about many ships attacked, and urges the admiral to defeat it.'),
    2341: ("Ah! That's the white whale everyone's talking about! They say it's attacked lots of ships. How about we take it down?!", 'Rough surprised identification of the rumored white whale; reported attacks on many ships and a proposal to defeat it.'),
    2343: ("Wow, the white whale! It's famous! It's attacked lots of ships! Hey, let's beat it!", 'Youthful excitement at seeing the famous white whale; many ships attacked and eager proposal to defeat it.'),
    2344: ("That's the white whale we've heard about! They say countless ships have fallen prey to it. Shall we defeat it ourselves?", 'Formal older identification of the rumored white whale; reportedly countless ships fell prey and asks whether we should defeat it.'),
    2352: ("Ah! The white whale is getting away... Hm? Something's shining where it dived!", 'Notices the white whale escaping, then notices something shining at the spot where it submerged.'),
    2353: ("Oh, the white whale is getting away... What's that?! Something's gleaming where it dived!", 'Regret at the white whale escaping, then startled question and a gleaming object at its dive site.'),
    2354: ("Aw, the white whale got away... Huh?! Hey, something's glittering over there!", 'Youthful disappointment at the white whale escaping, then surprise and a shining object over there.'),
    2355: ("Aw, it got away... Oh? There's something shining where the white whale dived!", "Disappointed feminine voice at the escape, then noticing something shining at the white whale's dive site."),
    2367: ('Admiral, a pod of dolphins over there! May I record this in our voyage log?', 'Addresses the admiral, points out a group of dolphins and requests permission to record it in the voyage log.'),
    2368: ('Wow, a pod of dolphins over there! May I record the sighting in our voyage log?', 'Excited voice points out dolphins and requests permission to record the sighting in the voyage log.'),
    2374: ('Yes, you have my permission.', 'Authorizes recording the sighting, with a deliberate affirmative tone.'),
    2375: ('Yes. Record it in the log.', 'Informal affirmative and instruction to record the preceding sighting.'),
    2376: ('Yes, please write it down.', 'Polite affirmative and request to write down the preceding sighting.'),
    2391: ('The foam is swallowing the ship!', 'Reports foam swallowing the ship.'),
    2392: ('This foam is swallowing the ship!', 'Youthful alarm that this foam is swallowing the ship.'),
    2393: ('The foam is swallowing our ship!', 'Feminine alarm that the ship is being swallowed by foam.'),
    2394: ("The foam's swallowing our ship!", 'Rough alarm that the ship is being swallowed by foam.'),
    2395: ('The foam is swallowing the ship!', 'Older emphatic report of foam swallowing the ship.'),
    2397: ('Ugh... S-so cold...', 'Shivering, hesitant complaint of being cold.'),
    2398: ("Brrr... It's so cold!", 'Youthful shivering complaint of being cold.'),
    2399: ('Whoa! L-l-lightning!', 'Startled cry and stammered lightning warning.'),
    2400: ('Ah! Lightning!', 'Short gruff surprised lightning warning.'),
    2401: ('L-l-lightning!', 'Stammered lightning warning.'),
    2402: ('L-l-lightning!', 'Feminine stammered lightning warning.'),
    2410: ("We're in trouble! A whirlpool has caught us!", 'Alarm that we are being caught up in a whirlpool.'),
    2411: ("This is bad! We're being sucked into a whirlpool!", 'Older alarm that we are caught up in a whirlpool.'),
    2412: ('The whirlpool is eating our ship!', 'Youthful personification of the whirlpool as eating the ship.'),
    2413: ('Oh no! A hidden reef!', 'Regretful sudden warning of a submerged reef.'),
    2416: ('Trouble! A hidden reef!', 'Feminine alarm at a submerged reef.'),
    2417: ('This is bad! A hidden reef!', 'Older alarm at a submerged reef.'),
    2424: ("No! We can't turn in time!", 'Older warning that steering cannot be completed in time, not that the rudder is broken.'),
    2425: ('That was a tough opponent...', 'Reflects that the opponent was quite formidable; no invented outcome or identity.'),
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
            'context': (f'Independent native message {e.message_id}, clean COMMON B25 '
                        f'R{e.record_index}; white-whale encounters, dolphins and hazards at sea. '
                        'All native selections in each selected source owner are included.'),
            'localization_note': ('Fresh clean-source American English retains hearsay about whale attacks, '
                                  'countless ships versus many, proposals and questions, escape and dive-site '
                                  'discoveries, dolphin pods, log permission, foam swallowing ships, cold and '
                                  'stammered lightning warnings, whirlpools, hidden reefs, and inability to turn '
                                  'in time. The youthful whirlpool eating image is retained; no invented broken '
                                  'rudder or destroyed ships. One paragraph. Reserved I/F use safe full-width '
                                  'glyphs. Exact-font previews await review.'),
            'review': {'source': True, 'context': True, 'localization': True,
                       'naturalness': True, 'formatting': False},
        })
    payload = {'format': 'dk4-common-entry-manuscript-v1',
               'translation_policy': 'natural-dialogue-v2', 'target_locale': 'en-US',
               'encoder': 'dialogue-fixed-v1',
               'review_gates': ['source', 'context', 'localization', 'naturalness', 'formatting'],
               'status': 'draft-awaiting-reblocking-and-formatting-review', 'records': rows}
    Path('translations/common_japanese_b25_manuscript_v1.json').write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(f'Prepared {len(rows)} clean-source native messages')


if __name__ == '__main__':
    main()
