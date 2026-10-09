"""Prepare clean-source expedition discoveries and hazard reports."""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from dk4tool.rom.nds import NdsImage
from dk4tool.script.common_message_table import common_message_entries

TEXT = {
    2263: ("Wild beasts attacked the expedition!", "Older emphatic report that beasts attacked the expedition."),
    2264: ("Admiral, disease is spreading across the ship! It seems the expedition caught it when they were attacked by wild beasts!", "Reports disease spreading throughout the ship; apparently the expedition contracted it in the beast attack."),
    2265: ("Admiral, disease is spreading all over the ship! The expedition apparently caught it in the attack by wild beasts!", "Informal alarm about widespread disease; apparently contracted by the expedition when attacked by beasts."),
    2266: ("Disease is spreading throughout our ship! It seems our expedition was infected when wild beasts attacked!", "Older alarm about disease throughout the ship; retains uncertainty about the expedition contracting it in the attack."),
    2275: ("It looks like the expedition has found a hot spring!", "Apparently the expedition discovered a hot spring."),
    2276: ("Admiral, it appears the expedition found a hot spring!", "Formal report to the admiral of an apparent hot spring discovery."),
    2281: ("The expedition found a hot spring, they say!", "Youthful hearsay that the expedition found a hot spring."),
    2282: ("Admiral, this feels wonderful. Hot springs soothe weary travelers.", "Addresses the admiral, praises how good it feels and says hot springs relieve travel fatigue."),
    2288: ("The expedition seems to have found an oasis! Let's go!", "Apparent oasis discovery and invitation to visit."),
    2289: ("The expedition appears to have found an oasis! Let's hurry!", "Formal report of an apparent oasis discovery and urging haste."),
    2290: ("Admiral! The expedition discovered an oasis! Let's hurry over!", "Youthful excited report of the oasis discovery, addressing the admiral and urging a quick visit."),
    2291: ("It looks like the expedition found an oasis! Come on, let's go!", "Rough informal report of an apparent oasis discovery and urging a quick visit."),
    2299: ("I never thought we'd find an oasis here. Ah, I feel refreshed!", "Older voice did not expect an oasis here and feels restored; localizes the idiom about washing one's life."),
    2300: ("An oasis in a place like this! I'm so happy!", "Youthful wonder and delight at finding an oasis in such a place."),
    2311: ("Admiral, we're in trouble! They say a bottomless bog has trapped our expedition!", "Alarm to the admiral with hearsay that the expedition is trapped in a bottomless bog."),
    2312: ("Admiral, we're in trouble! It seems a bottomless bog has trapped our expedition!", "Rough alarm to the admiral; apparent report of the expedition trapped in a bottomless bog."),
    2313: ("Trouble! It seems the expedition is stuck in a bottomless bog!", "Older alarm with uncertainty that the expedition is trapped in a bottomless bog."),
    2314: ("Oh no! A bottomless bog has trapped the expedition!", "Youthful alarm directly reports the expedition trapped in a bottomless bog."),
    2326: ("Admiral, the expedition found it! It's %s's Proof of Conqueror, %s!", "Excited report that the expedition found the named Proof of Conqueror; region first, artifact second."),
    2327: ("Admiral, the expedition's discovery is %s's Proof of Conqueror, %s, isn't it?!", "Rough confirmation question identifying what the expedition found; region first, artifact second."),
    2329: ("Admiral, what the expedition found is the Proof of Conqueror for %s: %s, right?", "Youthful confirmation question about the expedition's discovery; region first, artifact second."),
    2330: ("Admiral, our expedition discovered this. It appears to be %s's Proof of Conqueror, %s.", "Formal older report of the expedition's discovery, cautiously identifying the region's named Proof."),
    2334: ("Admiral, trouble! A shark has torn %s to pieces!", "Alarm to the admiral that a shark tore the substituted figurehead apart; item slot lookup is mapped in the shark argument note."),
    2335: ("A shark tore %s to pieces!", "Older emphatic report that a shark tore the substituted figurehead apart."),
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
            'speaker': 'Crew expedition report voice variant',
            'context': (f'Independent native message {e.message_id}, clean COMMON B24 '
                        f'R{e.record_index}; expedition hazards, discoveries and recovery. '
                        'All native selections in each selected source owner are included.'),
            'localization_note': ('Fresh clean-source American English retains reports versus '
                                  'hearsay, beast attacks and disease, travel fatigue, urgency, '
                                  'oasis delight, bog entrapment and the named Proof of Conqueror. '
                                  'Region and artifact remain in original printf order. The shark '
                                  'argument is a figurehead item selected by the clean ARM9 caller, '
                                  'not an inferred bodily injury. No authored line breaks. Reserved '
                                  'I/F use safe full-width glyphs. Exact-font previews await review.'),
            'review': {'source': True, 'context': True, 'localization': True,
                       'naturalness': True, 'formatting': False},
        })
    payload = {'format': 'dk4-common-entry-manuscript-v1',
               'translation_policy': 'natural-dialogue-v2', 'target_locale': 'en-US',
               'encoder': 'dialogue-fixed-v1',
               'review_gates': ['source', 'context', 'localization', 'naturalness', 'formatting'],
               'status': 'draft-awaiting-reblocking-and-formatting-review', 'records': rows}
    Path('translations/common_japanese_b24_manuscript_v1.json').write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(f'Prepared {len(rows)} clean-source native messages')


if __name__ == '__main__':
    main()
