"""Approve native tooltip formatting with complete static/dynamic source evidence."""

import copy

TARGET_SHA = 'd937be33b97b654038d03f1aed57ae30a2a49e0afce7d96ae1e2c972c1b758b3'


def approve(documents, evidence):
    statuses = {
        'allocation': 'complete-owned-pool-allocation-native-formatting-pending',
        'complete': 'pass-all-39-class-tooltip-substitutions-and-inherited-golden-consumers',
        'factions': 'pass-native-fixed-faction-names-and-all-static-class-combinations',
        'numeric': 'pass-source-bounded-numeric-getters-conversion-and-mixed-glyph-requests',
        'player': 'pass-native-eighteen-byte-editor-and-nineteen-byte-serialization',
        'pixels': 'pass-real-itcm-full-width-numeric-pixels',
    }
    for key, status in statuses.items():
        proof = evidence[key]
        if proof['status'] != status or proof['target_arm9_sha256'] != TARGET_SHA:
            raise ValueError('Native tooltip evidence failed or covers another target')
    complete, factions, numeric, player, pixels = (evidence[k] for k in ('complete', 'factions', 'numeric', 'player', 'pixels'))
    if len(complete['tooltip_cases']) != 312 or {(r['class_index'], r['name'], r['mode']) for r in complete['tooltip_cases']} != {
            (i, name, mode) for i in range(39) for name in ('Pirates', 'Monster', '???', 'FleetX') for mode in (4, 16)}:
        raise ValueError('All static class/category raster combinations are required')
    if complete['inherited_caption_count'] != 164 or len(complete['inherited_golden_raster_cases']) != 16:
        raise ValueError('Inherited caption/Golden rendering preservation is required')
    if len(factions['native_name_selections']) != 80 or {(r['index'], r['route']) for r in factions['native_name_selections']} != {
            (i, route) for i in range(20) for route in range(4)}:
        raise ValueError('All faction/route native name selections are required')
    if len(factions['fixed_name_rasters']) != 1560 or {(r['faction_index'], r['class_index'], r['mode']) for r in factions['fixed_name_rasters']} != {
            (i, c, mode) for i in range(20) for c in range(39) for mode in (4, 16)}:
        raise ValueError('All fixed faction/class rasters are required')
    if any(not r['native_constructor_and_name_getter_executed'] or not r['stack_return_and_adjacent_owner_guards_preserved'] for r in factions['native_name_selections']):
        raise ValueError('Native faction name state proof is required')
    if len(numeric['percentage_cases']) != 768 or {(r['percentage'], r['matching_entry']) for r in numeric['percentage_cases']} != {
            (value, entry) for value in range(256) for entry in range(3)}:
        raise ValueError('Source-bounded percentage coverage is required')
    if numeric['source_bounds'] != {'percentage': [0, 255], 'armament': [0, 65535], 'ring_slots': 32, 'slot_capacity': 128}:
        raise ValueError('Native numeric source bounds differ')
    if len(numeric['boundary_cases']) != 20 or {(r['armament'], r['ring_index']) for r in numeric['boundary_cases']} != {
            (v, ring) for v in (0, 9, 10, 99, 100, 999, 1000, 9999, 10000, 65535) for ring in (0, 31)}:
        raise ValueError('Numeric decimal/ring boundaries are required')
    if any(not r['complete_digits_nul_stack_and_distinct_ring_slots_preserved'] or not r['all_other_ring_slots_preserved']
           for r in numeric['percentage_cases'] + numeric['boundary_cases']):
        raise ValueError('Complete native numeric bytes/slot lifetime proof is required')
    if player['editor_capacity_bytes'] != 18 or player['serialized_storage_bytes'] != 19 or len(player['cases']) != 27:
        raise ValueError('Actual player-name editor/save capacity is required')
    names = {bytes.fromhex(r['name_hex']) for r in player['cases']}
    if names != {b'A' * i for i in range(1, 19)} | {'ア'.encode('cp932') * i for i in range(1, 10)}:
        raise ValueError('Complete ASCII/CP932 player-name boundaries are required')
    for row in player['cases']:
        name = bytes.fromhex(row['name_hex'])
        field = name + b'\0' + b'\xA5' * (18 - len(name))
        if row['editor']['limit'] != 18 or any(bytes.fromhex(row[k]['complete_field_hex']) != field or row[k]['byte_calls'] != 19 for k in ('save', 'load')):
            raise ValueError('Player-name native editor/save/load loses complete bytes')
    if len(player['maximum_ascii_raster_cases']) != 156 or {(r['name_bytes'], r['class_index'], r['mode']) for r in player['maximum_ascii_raster_cases']} != {
            (size, c, mode) for size in (17, 18) for c in range(39) for mode in (4, 16)}:
        raise ValueError('Maximum ASCII player-name/class rasters are required')
    for row in complete['tooltip_cases'] + factions['fixed_name_rasters'] + player['maximum_ascii_raster_cases']:
        if not row['stack_registers_guard_and_cleanup_preserved'] or row['second_row_first_glyph_x'] != 6 or row['width'] > 256 or row['height'] != 24:
            raise ValueError('Complete leading glyph/pixel dimensions/state proof is required')
    if len(pixels['cases']) != 66 or {(r['name'], r['percentage'], r['armament'], r['mode']) for r in pixels['cases']} != {
            (name, p, a, mode) for name in ('Fleet', 'FleetX', 'A' * 18)
            for p, a in [(i, i) for i in range(10)] + [(255, 65535)] for mode in (4, 16)}:
        raise ValueError('Complete native numeric ITCM pixel coverage is required')
    if len(pixels['name_cases']) != 68 or any(not r['complete_ordered_glyph_sequence_and_independent_pixels_match'] or r['leading_class_x'] != 6 for r in pixels['name_cases']):
        raise ValueError('Complete CP932 player-name pixels and leading class are required')
    if any(not r['native_itcm_and_font_lookup_executed'] or not r['independent_full_buffer_pixels_match'] or not r['stack_registers_and_buffer_guards_preserved'] for r in pixels['cases']):
        raise ValueError('Actual ITCM pixel/state proof is required')
    if evidence['preview']['status'] != 'reviewed' or evidence['preview']['sample_count'] != 6:
        raise ValueError('Native ink preview review is required')
    consumed = {r['id']: r['english'] for r in evidence['allocation']['selections']}
    records = [r for document in documents for r in document['records']]
    expected_ids = {'MAP_ENTITY_TOOLTIP_' + k for k in ('PIRATES', 'MONSTER', 'UNKNOWN', 'CLASS', 'ARMAMENT')} | {
        'MAP_CREATURE_CLASS_' + str(i) for i in range(34, 38)}
    if len(records) != 9 or {r['id'] for r in records} != expected_ids:
        raise ValueError('All nine complete tooltip/creature translations are required')
    result = copy.deepcopy(documents)
    for document in result:
        if document['translation_policy'] != 'natural-dialogue-v2' or document['target_locale'] != 'en-US':
            raise ValueError('Natural American English policy is required')
        for row in document['records']:
            if row['english'] != consumed[row['id']] or not all(row['review'][gate] is True for gate in ('source', 'context', 'localization', 'naturalness')):
                raise ValueError('Complete editorial text differs from native consumed wording')
            row['review']['formatting'] = True
        document['status'] = 'reviewed-native-tooltip-formatting-experimental-runtime-pending'
        document['native_formatting_limits'] = [
            'Font disk loading and bitmap origin/clear/physical compositor remain contracts.',
            'Keyboard UI and physical save I/O backend remain contracts.',
            'Load preserves nineteen bytes; malformed saved-field NUL validation is absent.',
            'Physical palette/routing and cold-boot gameplay remain pending.',
            'Native formatting is approved for the experimental combined candidate; canonical acceptance is pending.'
        ]
    return result
