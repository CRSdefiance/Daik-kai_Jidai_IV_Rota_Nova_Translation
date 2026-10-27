"""Review complete race menu/wireless source; keep unproven layout gates open."""

import hashlib
import json
import struct
from pathlib import Path

from dk4tool.rom.nds import NdsImage

BASE = 0x02000000
CANDIDATE = Path('out/all_routes_combined_v134_candidate.nds')
CANDIDATE_SHA = '6af0f04f94538daa6cab58062c62e9dff578041da1f0b9ccf84b0b2fedcada9f'
CANONICAL = Path('out/raphael_natural_v2_accepted_base.nds')
CANONICAL_SHA = '3cb827e4c52ab2086fb5a626835d72192085a958581279d3c79b0200bbf405fe'
CLEAN_ARM9_SHA = '0d1541022ef95afe02ad7a1a381a1fc3e5e74442a5f0408f436d68a5d306d731'

# Complete meanings precede the localized text. Multiple offsets form one
# sentence/paragraph; they are not independently translated allocation slots.
MESSAGES = [
    ('place_1', (0x16AFE4,), 'First place.', '1st Place', 'Race finishing position; source uses the ordinal kanji for first.'),
    ('place_2', (0x16AFD4,), 'Second place.', '2nd Place', 'Race finishing position; source uses the ordinal kanji for second.'),
    ('place_3', (0x16AFEC,), 'Third place.', '3rd Place', 'Race finishing position; source uses the ordinal kanji for third.'),
    ('place_4', (0x16AFFC,), 'Fourth place.', '4th Place', 'Race finishing position; source uses the ordinal kanji for fourth.'),
    ('number_1', (0x16B014,), 'Player 1.', '1P', 'Short wireless player identifier; preserve established P numbering.'),
    ('number_2', (0x16B004,), 'Player 2.', '2P', 'Short wireless player identifier; preserve established P numbering.'),
    ('number_3', (0x16AFDC,), 'Player 3.', '3P', 'Short wireless player identifier; preserve established P numbering.'),
    ('number_4', (0x16AFF4,), 'Player 4.', '4P', 'Short wireless player identifier; preserve established P numbering.'),
    ('limits', (0x13799C,), 'Restrictions applying to the race.', 'Race Limits', 'Rules category containing time limit and stopping a race.'),
    ('basic_rules', (0x1379D8,), 'Basic rules.', 'Basic Rules', 'Rules category containing ship, basic rules, area and prizes.'),
    ('map_supplies', (0x137A38,), 'Route map and replenishment.', 'Map & Supplies', 'Rules category containing map and food replenishment.'),
    ('read_rules', (0x137A58,), 'Read the rules.', 'Read the Rules', 'Second entry in the main race menu.'),
    ('about', (0x137AB8,), 'About the race.', 'About the Race', 'First race-help category.'),
    ('start', (0x137AF8,), 'Start the race.', 'Start Race', 'First entry in the main race menu.'),
    ('north_sea', (0x16B00C,), 'The North Sea.', 'North Sea', 'One of four sea regions selected by the host.'),
    ('mediterranean', (0x16B024,), 'The Mediterranean.', 'Mediterranean', 'One of four sea regions selected by the host.'),
    ('join', (0x16B04C,), 'Become a joining device/player.', 'Join', 'Wireless role choice; child means joining device, not a family relationship.'),
    ('host', (0x16B058,), 'Become the hosting device/player.', 'Host', 'Wireless role choice; parent means host, not a family relationship.'),
    ('east_asia', (0x16B064,), 'East Asia.', 'East Asia', 'One of four sea regions selected by the host.'),
    ('southeast_asia', (0x16B070,), 'Southeast Asia.', 'Southeast Asia', 'One of four sea regions selected by the host.'),
    ('prize_500', (0x16B14C,), 'Obtained prize money of 500.', 'You won 500 in prize money.', 'Race result prize notification; no invented currency unit.'),
    ('wait', (0x16B15C,), 'Please wait.', 'Please wait.', 'Wireless waiting notification.'),
    ('results', (0x16B17C,), 'These are the race results.', 'Race Results', 'Results screen heading.'),
    ('prize_5000', (0x16B1AC,), 'Obtained prize money of 5000.', 'You won 5,000 in prize money.', 'Race result prize notification; no invented currency unit.'),
    ('player_1', (0x16B1C0,), 'You are player 1.', 'You are Player 1.', 'Wireless assigned player number.'),
    ('prize_2000', (0x16B1D4,), 'Obtained prize money of 2000.', 'You won 2,000 in prize money.', 'Race result prize notification; no invented currency unit.'),
    ('player_2', (0x16B1E8,), 'You are player 2.', 'You are Player 2.', 'Wireless assigned player number.'),
    ('player_3', (0x16B1FC,), 'You are player 3.', 'You are Player 3.', 'Wireless assigned player number.'),
    ('prize_1000', (0x16B210,), 'Obtained prize money of 1000.', 'You won 1,000 in prize money.', 'Race result prize notification; no invented currency unit.'),
    ('player_4', (0x16B224,), 'You are player 4.', 'You are Player 4.', 'Wireless assigned player number.'),
    ('search', (0x16B274,), 'Searching for a hosting device.', 'Searching for a host...', 'Joining-device host search status.'),
    ('continue', (0x16B2B4, 0x16B2D0), 'Touch the lower screen or press the A Button.', 'Touch the lower screen or press the A Button.', 'Two consecutive instruction widgets after the race results.'),
    ('confirm_players', (0x16B308, 0x16B368), 'When all members appear, select Confirm on the lower screen.', 'When all players are displayed, select Confirm on the lower screen.', 'Host waiting room; confirmation is conditional on the complete player list.'),
    ('host_selecting', (0x16B328, 0x16B348), 'The host is choosing the stage; wait until it is decided.', 'The host is choosing the race area. Please wait until the selection is confirmed.', 'Joining players wait for the host to choose the sea region.'),
    ('choose_area', (0x16B388,), 'Choose the sea region in which to play.', 'Choose a sea region to race in.', 'Host race-area selection prompt.'),
    ('wait_players', (0x16B3EC,), 'Waiting for participating players.', 'Waiting for players to join...', 'Host waiting-room status.'),
    ('roles', (0x16B434, 0x16B458, 0x16B24C, 0x16B3C8), 'Decide wireless host and joining roles. Exactly one member must choose Host; all the others must choose Join.', 'Choose your roles for wireless play. Exactly one player must select Host. Everyone else must select Join.', 'Four ordered role instructions; the middle two fragments form one sentence.'),
    ('over', (0x16B8D4,), 'The race has ended.', 'Race Over', 'Race termination notification.'),
    ('error', (0x16B8EC,), 'A communication error occurred.', 'A communication error occurred.', 'Wireless error notification.'),
    ('disconnected', (0x16B908,), 'Communication was disconnected.', 'The connection was lost.', 'Wireless disconnect notification.'),
    ('full', (0x16B91C,), 'Cannot join because there are too many participants.', "The race is full. You can't join.", 'Join failure retaining the capacity cause.'),
    ('return_menu', (0x16B93C, 0x16B954, 0x16B968), 'Touch the lower screen or press the A Button to return to the menu screen.', 'Touch the lower screen or press the A Button to return to the menu.', 'Three consecutive error-screen instruction widgets forming one sentence.'),
    ('title', (0x16B980,), 'Grand sailing race.', 'Grand Race', 'Established English feature name.'),
    ('join_area', (0x16B990,), 'Joining device: stage decision.', 'Join: Waiting for Race Area', 'Joining-device area-decision screen; its full body says the host is choosing the region.'),
    ('join_search', (0x16B9A4,), 'Joining device: search for a hosting device.', 'Join: Find a Host', 'Joining-device screen heading.'),
    ('wait_registration', (0x16B9B4,), 'Wait until participation registration closes.', 'Please wait until registration closes.', 'Joining players wait for entry to close; distinct from generic waiting.'),
    ('host_open', (0x16B9F4,), 'Hosting device: accepting participation.', 'Host: Accepting Players', 'Host waiting-room heading.'),
    ('host_area', (0x16B9E0,), 'Hosting device: stage selection.', 'Host: Choose a Race Area', 'Host area-selection screen heading; the source includes an ideographic space.'),
    ('host_starting', (0x16BA08,), 'Hosting device: proceeding into the game.', 'Host: Starting the Race', 'Host transition heading after the waiting room; game refers to the race.'),
    ('choose_role', (0x16BA28,), 'Select hosting or joining role.', 'Choose Host or Join', 'Wireless role-selection screen heading; avoid literal family wording.'),
    ('empty_player', (0x16BA34,), 'Waiting for participation.', 'Waiting for a player', 'Unoccupied player slot fallback selected by the player-information widget.'),
]


def main():
    for path, expected in ((CANDIDATE, CANDIDATE_SHA), (CANONICAL, CANONICAL_SHA)):
        if hashlib.sha256(path.read_bytes()).hexdigest() != expected:
            raise ValueError(f'Pinned ROM differs: {path}')
    clean = NdsImage.open('work/clean.nds').read_file('/__arm9__.bin')
    canonical = NdsImage.open(CANONICAL).read_file('/__arm9__.bin')
    current = NdsImage.open(CANDIDATE).read_file('/__arm9__.bin')
    if hashlib.sha256(clean).hexdigest() != CLEAN_ARM9_SHA:
        raise ValueError('Clean Japanese ARM9 differs')
    covered = [offset for _, offsets, *_ in MESSAGES for offset in offsets]
    if len(covered) != 59 or len(covered) != len(set(covered)):
        raise ValueError('Manuscript must cover the 59 reviewed source parts once')
    reference_map = {}
    for p in range(0, len(clean) - 3, 4):
        reference_map.setdefault(struct.unpack_from('<I', clean, p)[0] - BASE, []).append(p)
    records = []
    for name, offsets, gloss, english, context in MESSAGES:
        parts = []
        for offset in offsets:
            raw = clean[offset:clean.index(b'\0', offset) + 1]
            japanese = raw[:-1].decode('cp932')
            if japanese.encode('cp932') + b'\0' != raw:
                raise ValueError(f'{name}: source CP932 round trip differs')
            if any(arm9[offset:offset + len(raw)] != raw for arm9 in (clean, canonical, current)):
                raise ValueError(f'{name}: source bytes differ')
            actual_refs = reference_map.get(offset, [])
            if len(actual_refs) != 1:
                raise ValueError(f'{name}: reviewed single-reference source differs')
            if any(canonical[p:p + 4] != clean[p:p + 4] or current[p:p + 4] != clean[p:p + 4]
                   for p in actual_refs):
                raise ValueError(f'{name}: source pointers differ')
            padded_end = (offset + len(raw) + 3) & ~3
            padding = clean[offset + len(raw):padded_end]
            if any(padding):
                raise ValueError(f'{name}: presumed alignment padding is not zero')
            parts.append({'offset': offset, 'japanese': japanese,
                          'source_hex': raw.hex().upper(), 'source_bytes_including_nul': len(raw),
                          'aligned_source_bytes_including_nul': padded_end - offset,
                          'aligned_pointer_fields': actual_refs})
        raw_english = english.encode('ascii')
        if not raw_english or any(byte < 0x20 or byte > 0x7E for byte in raw_english):
            raise ValueError(f'{name}: nonprintable or empty English')
        records.append({'id': f'GRAND_RACE_UI_{name.upper()}', 'english': english,
                        'speaker': 'System', 'context': context, 'source_meaning': gloss,
                        'localization_note': 'Fresh clean-source localization. Complete paragraph is independent of original widget fragments and allocations; preserve all conditions when laying it out.',
                        'source_parts_in_reading_order': parts,
                        'presentation': 'measured-menu-button' if name in {'limits', 'basic_rules', 'map_supplies', 'read_rules', 'about', 'start'} else 'wireless-widget-unclassified',
                        'encoded_bytes_including_nul': len(raw_english) + 1,
                        'unwrapped_width_pixels': len(raw_english) * 6,
                        'review': {'source': True, 'context': False, 'localization': True,
                                   'naturalness': True, 'formatting': False}})
    manuscript = {'format': 'dk4-grand-race-ui-manuscript-v2',
                  'translation_policy': 'natural-dialogue-v2', 'target_locale': 'en-US',
                  'status': 'source-reviewed-prose-consumer-layout-and-integration-pending',
                  'clean_arm9_sha256': hashlib.sha256(clean).hexdigest(),
                  'canonical_arm9_sha256': hashlib.sha256(canonical).hexdigest(),
                  'research_candidate': str(CANDIDATE), 'research_candidate_sha256': CANDIDATE_SHA,
                  'source_part_count': len(covered), 'logical_message_count': len(records),
                  'integration_blockers': ['Resolve complete menu button draw path and lock source/geometry.',
                                           'Verify wireless line-widget order and coordinates for each screen.',
                                           'Relocate full English where original slots do not fit; no clipping or abbreviation.',
                                           'Generate and review exact-font native-context previews.',
                                           'Register complete V134-derived transform input and candidate, then verify saved selections.'],
                  'records': records}
    path = Path('translations/grand_race_remaining_ui_manuscript_v2.json')
    path.write_text(json.dumps(manuscript, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(json.dumps({'manuscript': str(path), 'source_parts': len(covered),
                      'logical_messages': len(records), 'candidate_changed': False}))


if __name__ == '__main__':
    main()
