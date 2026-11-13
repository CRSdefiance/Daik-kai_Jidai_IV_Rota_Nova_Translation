"""Prepare complete clean-source Grand Race help; presentation remains pending."""
import argparse
import hashlib
import json
import struct
from pathlib import Path

from dk4tool.rom.nds import NdsImage

# Gloss precedes localization. Offsets identify paired title/body descriptors.
PAGES = [
    (0x1152AC, 'Time Limit',
     'A time limit applies. Anyone not finishing within it is disqualified and gets no prize. If nobody finishes before the limit, the race is a no-game.',
     'A race has a time limit. Players who fail to reach the finish before time runs out are disqualified and receive no prize money. If no one finishes in time, the race is void.'),
    (0x1152B4, 'Your Ship',
     'Use the flagship from your own fleet. Choose save data recording the desired flagship. Only the flagship basic performance affects racing; equipment, recruited sailing personnel and item effects do not apply.',
     "You race with your fleet's flagship. Select the save data containing the flagship you want to use. Only the flagship's basic performance affects the race. Equipment, crew members and items have no effect."),
    (0x1152BC, 'Supplies',
     'Food is consumed during racing. The number beside the barrel at upper left of the lower screen gives food quantity. At zero food, ship speed drops. Replenish food at supply points.',
     'Food is consumed during a race. The number beside the barrel icon at the upper left of the lower screen shows how much food remains. When food reaches zero, your ship slows down. Replenish food at supply points.'),
    (0x1152C4, 'Map',
     'The race map shows positions of ships, finish, checkpoints and supply points. Player ships are red, blue, yellow, green in join order. Finish has G, checkpoints red circles, supply points light blue circles. Passed checkpoints vanish from your map.',
     "During a race, the map shows ships, the finish, checkpoints and supply points. Ships are colored red, blue, yellow and green in player join order. The finish is marked G, checkpoints are red circles, and supply points are light blue circles. Checkpoints you've passed disappear from your map."),
    (0x1152CC, 'About the Race',
     'Grand Race is competitive racing through Nintendo DS wireless communications, for up to four players. One player hosts the race; the others join that hosted race.',
     'Grand Race is a competitive race using DS Wireless Communications. Up to four people can play. One player hosts the race, and the others join it.'),
    (0x1152D4, 'Race Area',
     'Four sea regions serve as race stages. The host chooses the sea region. Leaving the racing region is impossible. Its boundaries appear as red lines.',
     'There are four sea regions to race in. The host chooses the region. You cannot leave the race area; its boundaries are marked by red lines.'),
    (0x1152DC, 'Basic Rules',
     'Control by touch screen, not directional pad. Pass seven checkpoints and finish first to win. Any checkpoint order is permitted, but all must be passed before finishing. Race lasts until everybody finishes.',
     "Control the race with the Touch Screen; the D-pad cannot be used. Pass all seven checkpoints and reach the finish first to win. You can pass the checkpoints in any order, but you cannot finish until you've passed them all. The race continues until everyone finishes."),
    (0x1152EC, 'Prizes',
     'Participants receive prize money according to their placing. The prize is reflected in the money held in their save data.',
     'Participants receive prize money according to their finishing position. The prize is added to the money in their save data.'),
    (0x1152FC, 'Stopping a Race',
     'One player cannot alone leave an ongoing race. To interrupt, turn off the Nintendo DS. If any one player powers off, the race is interrupted for everyone.',
     'A player cannot leave a race alone while it is underway. To stop playing, turn off your Nintendo DS. If one player turns off their system, the race stops for everyone.'),
]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--reviewed', action='store_true')
    args = parser.parse_args()
    clean = NdsImage.open('work/clean.nds')
    candidate = NdsImage.open('out/all_routes_combined_v133_candidate.nds')
    source = clean.read_file('/__arm9__.bin')
    current = candidate.read_file('/__arm9__.bin')
    reviewed = {}
    if args.reviewed:
        reviewed = {r['id']: r for r in json.loads(Path('work/qa/grand_race_help/report.json').read_text(encoding='utf-8'))['entries']}
    rows = []
    for descriptor, title, gloss, english in PAGES:
        if source[descriptor:descriptor + 8] != current[descriptor:descriptor + 8]:
            raise ValueError('Race help descriptor differs')
        title_pointer, body_pointer = struct.unpack_from('<II', source, descriptor)
        title_offset, offset = title_pointer - 0x02000000, body_pointer - 0x02000000
        japanese_title = source[title_offset:].split(b'\0', 1)[0].decode('cp932')
        raw = source[offset:].split(b'\0', 1)[0]
        raw.decode('cp932')
        if current[offset:offset + len(raw) + 1] != raw + b'\0':
            raise ValueError('Current body is not the unchanged clean source')
        rows.append({'id': f'DK4_GRAND_RACE_HELP_{offset:06X}',
                     'component': '/__arm9__.bin', 'source_offset': offset,
                     'source_hex': (raw + b'\0').hex().upper(),
                     'japanese': raw.decode('cp932'), 'source_meaning': gloss,
                     'english': english, 'speaker': 'Grand Race help system',
                     'context': f'Clean native help descriptor at {descriptor:#x}, title {japanese_title}. The group table at 0x115334 selects all nine pages through initial draw, direct page selection and previous/next navigation. Body cursor is (0, 12), drawn by 0x020D5404 through context 0x020D5160. Native startup sets 6/12-pixel font metrics; the widget is 252 by 108 pixels. Complete protected-break formatting, exact-font previews and byte-packed allocation are verified in research; integrated build enforcement and runtime remain pending.',
                     'localization_note': 'Natural American English retains every mechanic, count, condition, visual marker and multiplayer consequence. Host/join localizes parent/child connection roles. Grand Race and Map match existing UI terms. One logical paragraph, with no authored alignment or legacy Japanese wrapping.',
                     'review': {'source': True, 'context': True, 'localization': True,
                                'naturalness': True, 'formatting': args.reviewed},
                     'descriptor_offset': descriptor, 'title_offset': title_offset,
                     'draft_english_title': title, 'source_slot_minimum_bytes': len(raw) + 1,
                     'draft_ascii_bytes_including_nul': len(english.encode('ascii')) + 1})
    assert len(rows) == 9
    if args.reviewed:
        from dk4tool.dialogue.grand_race_help import format_page

        for row in rows:
            _, encoded, lines, _ = format_page(row['english'])
            previous = reviewed[row['id']]
            if previous['english'] != row['english'] or bytes.fromhex(previous['encoded_hex']) != encoded or previous['visible_lines'] != lines:
                raise ValueError('Reviewed preview does not match complete current prose')
    payload = {'format': 'dk4-arm9-text-manuscript-v1', 'translation_policy': 'natural-dialogue-v2',
               'target_locale': 'en-US', 'status': 'reviewed-awaiting-integration-and-runtime' if args.reviewed else 'source-reviewed-draft-awaiting-page-renderer-and-formatting',
               'source_arm9_sha256': hashlib.sha256(source).hexdigest(),
               'review_gates': ['source', 'context', 'localization', 'naturalness', 'formatting'],
               'records': rows,
               'integration_blockers': ['Complete page formatting and shared byte-packed allocation are verified in research; build-time revalidation and integrated release registration remain pending.',
                                       'Use the traced native page context and accepted pair-phase-safe protected breaks, not old Japanese wrapping.',
                                       'Full formatted bodies use 1,794 of the original 1,796 shared bytes. Title slot padding must be source-locked before integration.',
                                       'No batch/profile registered; runtime checks remain pending.']}
    Path('translations/grand_race_rules_manuscript_v2.json').write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(json.dumps({'source_reviewed_complete_pages': len(rows),
                      'requires_allocation_work': [r['id'] for r in rows
                                                  if r['draft_ascii_bytes_including_nul'] > r['source_slot_minimum_bytes']],
                      'formatting_reviewed': args.reviewed}, indent=2))


if __name__ == '__main__':
    main()
