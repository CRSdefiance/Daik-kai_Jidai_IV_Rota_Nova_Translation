"""Approve full viewer formatting only with title/footer/modal native evidence."""

import copy

TARGET_SHA = '9a4b950d452631a6cc60721177e1f8e2b1ad778d854b6e42b11df04fdb2828a5'


def approve(document, evidence):
    if len(document['records']) != 6 or len({row['id'] for row in document['records']}) != 6:
        raise ValueError('All six Golden Route records are required')
    statuses = {'headings': 'pass-both-golden-route-title-selections-native-printf-and-ascii-pixels',
                'footer': 'pass-native-golden-route-footer-transfer-placement-and-complete-ascii-raster',
                'empty': 'pass-native-zero-record-dispatch-printf-expansion-and-modal-ascii-pixels'}
    for name in ('headings', 'footer', 'empty'):
        if evidence[name]['proposed_arm9_sha256'] != TARGET_SHA:
            raise ValueError('Native viewer evidence covers a different target')
        if evidence[name]['status'] != statuses[name]:
            raise ValueError('Native viewer formatting evidence did not pass')
    headings, footer, empty = (evidence[name] for name in ('headings', 'footer', 'empty'))
    if len(headings['cases']) != 8 or {(row['selection'], row['mode'], row['native']['y']) for row in headings['cases']} != {
            (selection, mode, y) for selection in (0, 1) for mode in (4, 16) for y in (0, 12)}:
        raise ValueError('Complete native heading coverage is required')
    if len(footer['cases']) != 6 or {(row['table'], row['mode']) for row in footer['cases']} != {
            (table, mode) for table in (0x12EC10, 0x12EC28, 0x12EC3C) for mode in (4, 16)}:
        raise ValueError('Complete native footer coverage is required')
    if len(empty['cases']) != 2 or {row['mode'] for row in empty['cases']} != {4, 16}:
        raise ValueError('Both native modal pixel formats are required')
    if [(row['count'], row['empty_dialog_selected']) for row in empty['dispatches']] != [(0, True), (1, False), (2, False), (255, False)]:
        raise ValueError('Native zero/nonzero dialog dispatch coverage is required')
    if any(not row['stack_and_registers_preserved'] or not row['native_state_copy_and_font_cleanup'] for row in footer['cases']):
        raise ValueError('Native footer state/cleanup is incomplete')
    if any(not row['native']['native_strlen_printf_executed'] or not row['native']['stack_and_owners_preserved']
           for row in headings['cases']):
        raise ValueError('Native title copy/state is incomplete')
    if any(row['glyph_count'] != len(row['english']) or row['width_pixels'] != len(row['english']) * 6
           or not row['stack_and_registers_preserved'] for row in empty['cases']):
        raise ValueError('Native modal full text/state is incomplete')
    titles = {row['english'] for row in headings['cases']}
    controls = {row['text'] for case in footer['cases'] for row in case['placements']} - {'Back'}
    modal = {row['english'] for row in empty['cases']}
    if titles | controls | modal != {row['english'] for row in document['records']}:
        raise ValueError('Complete manuscript differs from native consumed labels')
    result = copy.deepcopy(document)
    for row in result['records']:
        if not all(row['review'][gate] is True for gate in ('source', 'context', 'localization', 'naturalness')):
            raise ValueError('Golden Route editorial review is incomplete')
        row['review']['formatting'] = True
    result['status'] = 'reviewed-native-viewer-formatting-experimental-runtime-pending'
    result['native_formatting_limits'] = {name: evidence[name]['limitations'] for name in ('headings', 'footer', 'empty')}
    return result
