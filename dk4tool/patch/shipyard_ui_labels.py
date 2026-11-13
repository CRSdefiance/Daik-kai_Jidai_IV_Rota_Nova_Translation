"""Source-bound Ship Name and regional-policy labels; no section growth."""

import json
import struct
from pathlib import Path

from ndspy.code import MainCodeFile

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.ship_name_heading import BASE, END
from dk4tool.patch.ship_name_heading import transform as heading_transform
from dk4tool.rom.nds import NdsImage

START = 0x01FFC7C0
LABELS = (
    (0x119A40, 0x0214B864, '海域委任', 'Manage Area'),
    (0x119A50, 0x0214B848, '哨戒', 'Patrol'),
    (0x119A60, 0x0214B838, '寄港', 'Dock'),
    (0x119A70, 0x0214B850, '街攻撃', 'Attack Town'),
)
MAP_LABELS = ((0x8E580, 0x0214C2E0, 0), (0x8E588, 0x0214C304, 3),
              (0x8E590, 0x0214C31C, 1), (0x8E598, 0x0214C338, 2))
# These are original concatenation fragments, not manually wrapped dialogue.
# The controller supplies fleet/city names and the two original newlines.
FRAGMENTS = (
    (0x0214C060, 'を基点の海域委任の任務を与えました', 'Area management orders issued.', 35, 0x8AE40),
    (0x0214C084, 'を攻撃する任務を与えました', 'Attack orders issued.', 27, 0x8AE44),
    (0x0214C0A0, 'を基点の哨戒の任務を与えました', 'Patrol orders issued.', 31, 0x8AE48),
    (0x0214C0C0, 'に寄港の任務を与えました', 'Docking orders issued.', 25, 0x8AE4C),
    (0x0214C0DC, 'に\n', ':\n', 4, 0x8AE54),
    (0x0214C2EC, 'を基点の海域委任です', ' is the base.', 21, 0x8E584),
    (0x0214C30C, 'を攻撃します', ' is the target.', 16, 0x8E58C),
    (0x0214C340, 'に寄港します', ' is the port.', 16, 0x8E59C),
)


def transform(source):
    intermediate, heading = heading_transform(source)
    clean = NdsImage.open('work/clean.nds').read_file('/__arm9__.bin')
    code = MainCodeFile(intermediate, BASE)
    before = [bytes(s.data) for s in code.sections]
    position, rows = START, []
    for offset, pointer, japanese, english in LABELS:
        raw = japanese.encode('cp932') + b'\0'
        assert source[pointer - BASE:pointer - BASE + len(raw)] == raw
        assert clean[pointer - BASE:pointer - BASE + len(raw)] == raw
        assert struct.unpack_from('<I', source, offset)[0] == pointer
        assert struct.unpack_from('<I', clean, offset)[0] == pointer
        aliases = [i for i in range(len(before[0]) - 3)
                   if before[0][i:i + 4] == struct.pack('<I', pointer)]
        assert aliases == [offset]
        text = english.encode('ascii') + b'\0'
        assert position + len(text) <= END
        at = position - code.sections[4].ramAddress
        assert not any(code.sections[4].data[at:at + len(text)])
        code.sections[4].data[at:at + len(text)] = text
        struct.pack_into('<I', code.sections[0].data, offset, position)
        rows.append({'pointer_field': offset, 'original_pointer': pointer,
                     'target_pointer': position, 'Japanese': japanese, 'English': english,
                     'original_main_pointer_aliases': aliases})
        position += len(text)
    for field, pointer, index in MAP_LABELS:
        assert struct.unpack_from('<I', source, field)[0] == pointer
        assert struct.unpack_from('<I', clean, field)[0] == pointer
        struct.pack_into('<I', code.sections[0].data, field, rows[index]['target_pointer'])
    # The patrol sentence has its own complete allocation in the remaining gap.
    patrol = b' is the patrol base.\0'
    assert position + len(patrol) <= END
    at = position - code.sections[4].ramAddress
    assert not any(code.sections[4].data[at:at + len(patrol)])
    code.sections[4].data[at:at + len(patrol)] = patrol
    patrol_at = position
    position += len(patrol)
    assert struct.unpack_from('<I', source, 0x8E594)[0] == 0x0214C324
    assert struct.unpack_from('<I', clean, 0x8E594)[0] == 0x0214C324
    struct.pack_into('<I', code.sections[0].data, 0x8E594, patrol_at)
    fragments = []
    for pointer, japanese, english, size, field in FRAGMENTS:
        at, raw, replacement = pointer - BASE, japanese.encode('cp932') + b'\0', english.encode('ascii') + b'\0'
        assert source[at:at + len(raw)] == clean[at:at + len(raw)] == raw
        assert source[at:at + size] == clean[at:at + size] == raw.ljust(size, b'\0')
        assert len(replacement) <= size and struct.unpack_from('<I', source, field)[0] == pointer
        aliases = [i for i in range(len(before[0]) - 3)
                   if pointer <= struct.unpack_from('<I', before[0], i)[0] < pointer + size]
        assert aliases == [field], (japanese, aliases)
        code.sections[0].data[at:at + size] = replacement.ljust(size, b'\0')
        fragments.append({'pointer': pointer, 'allocation_bytes': size, 'pointer_field': field,
                          'Japanese': japanese, 'English': english, 'unaligned_main_aliases': aliases})
    result = bytes(code.save())
    parsed = MainCodeFile(result, BASE)
    restored = bytearray(parsed.sections[0].data)
    for offset, _, _, _ in LABELS:
        restored[offset:offset + 4] = before[0][offset:offset + 4]
    for field, _, _ in MAP_LABELS:
        restored[field:field + 4] = before[0][field:field + 4]
    restored[0x8E594:0x8E598] = before[0][0x8E594:0x8E598]
    for pointer, _, _, size, _ in FRAGMENTS:
        restored[pointer - BASE:pointer - BASE + size] = before[0][pointer - BASE:pointer - BASE + size]
    assert restored == before[0]
    helper = bytearray(parsed.sections[4].data)
    helper[START - code.sections[4].ramAddress:position - code.sections[4].ramAddress] = bytes(position - START)
    assert helper == before[4]
    assert all(bytes(parsed.sections[i].data) == before[i] for i in (1, 2, 3))
    assert [(s.ramAddress, len(s.data)) for s in parsed.sections] == [(s.ramAddress, len(s.data)) for s in code.sections]
    return result, {'source_arm9_sha256': sha(source), 'target_arm9_sha256': sha(result),
                    'ship_name_heading': heading, 'policy_labels': rows,
                    'map_policy_label_pointer_reuse': [list(row) for row in MAP_LABELS],
                    'original_assignment_and_map_fragments': fragments,
                    'patrol_map_description': {'original_pointer': 0x0214C324, 'target_pointer': patrol_at,
                                               'Japanese': 'を基点に哨戒します', 'English': patrol[:-1].decode('ascii')},
                    'policy_string_span': [START, position],
                    'all_original_policy_row_IDs_flags_source_strings_native_code_and_section_extents_preserved': True,
                    'changed_records': heading['changed_records'] + [f'REGIONAL_POLICY_{i}' for i in range(4)]
                    + [f'REGIONAL_MAP_POLICY_{i}' for i in range(4)] + [f'REGIONAL_FRAGMENT_{i}' for i in range(9)],
                    'experimental': True, 'actual_native_caption_and_policy_dispatch_verification_pending': True,
                    'full_goal_complete': False}


def apply_release(source, path):
    config = json.loads(Path(path).read_text(encoding='utf-8'))
    assert config['format'] == 'dk4-shipyard-ui-labels-v1'
    target, proof = transform(source)
    if config['proof'] != proof:
        raise ValueError('Shipyard label source ownership or complete target differs')
    return target, proof
