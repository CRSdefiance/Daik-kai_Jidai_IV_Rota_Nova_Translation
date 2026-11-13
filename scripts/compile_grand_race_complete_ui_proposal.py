"""Compile complete scoped UI dependencies in memory; never build a playable ROM."""

import json
import struct
from pathlib import Path

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.grand_race_waiting_widget import rewrite_function
from dk4tool.patch.name_editor_atomic_append import END, START, apply
from dk4tool.rom.nds import NdsImage
from scripts.execute_grand_race_name_append import execute as execute_append
from scripts.execute_grand_race_waiting_widgets import TABLE
from scripts.execute_grand_race_waiting_widgets import execute as execute_widgets
from scripts.plan_grand_race_ui_allocation_v136 import CANDIDATE, CANDIDATE_SHA


def compile_ui(source, allocation, manuscript):
    rows = {row['id'].removeprefix('GRAND_RACE_UI_'): row for row in manuscript['records']}
    if len(rows) != 51 or len(allocation['selections']) != 60:
        raise ValueError('Full scoped text is required')
    proposed, code_changes = rewrite_function(source)
    proposed = bytearray(proposed)
    allowed = [tuple(span) for span in allocation['owned_ranges']]
    allowed.extend((change['offset'], change['offset'] + 4) for change in code_changes)
    selected = {}
    expected_fields = {field: part['offset'] for row in rows.values()
                       for part in row['source_parts_in_reading_order']
                       for field in part['aligned_pointer_fields']}
    for selection in allocation['selections']:
        name, offset = selection['message'], selection['offset']
        raw = bytes.fromhex(selection['raw_hex'])
        if raw != selection['line'].encode('ascii') + b'\0':
            raise ValueError('Full line or terminator differs')
        selected.setdefault(name, []).append(selection)
        if (not any(lo <= offset and offset + len(raw) <= hi for lo, hi in allowed)
                and source[offset:offset + len(raw)] != raw):
            raise ValueError('Shared complete title is outside unchanged source')
        proposed[offset:offset + len(raw)] = raw
        for field in selection['pointer_fields']:
            if (field not in expected_fields
                    or struct.unpack_from('<I', source, field)[0] != 0x02000000 + expected_fields[field]):
                raise ValueError('Text pointer field is not an original mapped consumer')
            struct.pack_into('<I', proposed, field, 0x02000000 + offset)
            allowed.append((field, field + 4))
    for name, selections in selected.items():
        ordered = sorted(selections, key=lambda selection: int(selection['key'].rsplit(':', 1)[1]))
        if ' '.join(selection['line'] for selection in ordered) != rows[name]['english']:
            raise ValueError('Complete manuscript prose was shortened or changed')
    for heading in allocation['shared_complete_help_headings']:
        field = heading['descriptor_field']
        if struct.unpack_from('<I', source, field)[0] != 0x02000000 + heading['old_offset']:
            raise ValueError('Shared heading original descriptor differs')
        struct.pack_into('<I', proposed, field, 0x02000000 + heading['new_offset'])
        allowed.append((field, field + 4))
    host = sorted(selected['HOST_SELECTING'], key=lambda selection: selection['key'])
    pointers = tuple(0x02000000 + selection['offset'] for selection in host)
    for index, pointer in enumerate(pointers):
        struct.pack_into('<I', proposed, TABLE + index * 4, pointer)
    struct.pack_into('<I', proposed, 0xF89DC, 0x02000000 + TABLE)
    allowed.extend(((TABLE, TABLE + 12), (0xF89DC, 0xF89E0)))
    proposed = bytearray(apply(proposed))
    allowed.append((START, END))
    if struct.unpack_from('<I', source, 0x12ED04)[0] != 156:
        raise ValueError('Result frame source width changed')
    struct.pack_into('<I', proposed, 0x12ED04, 180)
    allowed.append((0x12ED04, 0x12ED08))
    for lo, hi in allocation['inherited_reserved_spans']:
        if proposed[lo:hi] != source[lo:hi]:
            raise ValueError('Inherited menu/status bytes changed')
    for selection in allocation['selections']:
        offset = selection['offset']
        if proposed[offset:proposed.index(0, offset)].decode('ascii') != selection['line']:
            raise ValueError('Saved leading character or complete string changed')
        for field in selection['pointer_fields']:
            if struct.unpack_from('<I', proposed, field)[0] != 0x02000000 + offset:
                raise ValueError('Compiled text selection differs')
    changed = [offset for offset, (old, new) in enumerate(zip(source, proposed, strict=True)) if old != new]
    if any(not any(lo <= offset < hi for lo, hi in allowed) for offset in changed):
        raise ValueError('Complete proposal changed unrelated bytes')
    widgets = execute_widgets(proposed, pointers, scratch_table=False)
    append_cases = [execute_append(proposed, b'A' * size, inserted, 16, full_return=True)
                    for size in range(17) for inserted in (b'B', 'ア'.encode('cp932'))]
    for case in append_cases:
        name, inserted = bytes.fromhex(case['name_hex']), bytes.fromhex(case['inserted_hex'])
        expected = name + inserted if len(name) + len(inserted) <= 16 else name
        if bytes.fromhex(case['result_hex']) != expected or not case['stack_balanced']:
            raise ValueError('Combined native name repair failed')
    return bytes(proposed), {'message_count': len(rows), 'saved_string_count': 60,
                             'changed_bytes': len(changed), 'allowed_ranges': allowed,
                             'waiting_widget_execution': widgets, 'name_append_cases': append_cases}


def main():
    if sha(CANDIDATE.read_bytes()) != CANDIDATE_SHA:
        raise ValueError('Pinned current candidate differs')
    allocation_path = Path('work/analysis/grand_race_ui_allocation_v136/report.json')
    manuscript_path = Path('translations/grand_race_remaining_ui_manuscript_v2.json')
    allocation = json.loads(allocation_path.read_text())
    manuscript = json.loads(manuscript_path.read_text(encoding='utf-8'))
    if allocation['manuscript_sha256'] != sha(manuscript_path.read_bytes()) or allocation['candidate_sha256'] != CANDIDATE_SHA:
        raise ValueError('Complete allocation source is stale')
    source = NdsImage.open(CANDIDATE).read_file('/__arm9__.bin')
    proposed, report = compile_ui(source, allocation, manuscript)
    report.update({'format': 'dk4-grand-race-complete-ui-proposal-v1',
                   'status': 'compiled-research-not-release-ready', 'rom_written': False,
                   'runtime_verified': False, 'candidate_sha256': CANDIDATE_SHA,
                   'manuscript_sha256': sha(manuscript_path.read_bytes()),
                   'allocation_sha256': sha(allocation_path.read_bytes()),
                   'proposed_arm9_sha256': sha(proposed),
                   'limitations': ['Research proposal only; strict release editorial/ownership/dependency gates still required.',
                                   'Complete 51 messages preserved; eight inherited slots byte-exact.',
                                   'Result row geometry uses reviewed 180-pixel proposal; full artwork/gameplay pending.',
                                   'Name append/caller and third waiting widget execution are scoped; external drawing modeled.',
                                   'No ROM, registered batch, progress credit or canonical promotion.']})
    output = Path('work/analysis/grand_race_complete_ui_proposal_v136')
    output.mkdir(parents=True, exist_ok=True)
    (output / 'proposed_arm9.bin').write_bytes(proposed)
    (output / 'report.json').write_text(json.dumps(report, indent=2) + '\n')
    print('Complete 51-message proposal compiled; 60 saved strings, inherited slots, three waiting widgets and atomic names pass.')


if __name__ == '__main__':
    main()
