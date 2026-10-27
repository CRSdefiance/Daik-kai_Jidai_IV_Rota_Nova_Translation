"""Restore the source approximation marker in the crew Endurance caption."""

import json
import struct
from pathlib import Path

from ndspy.code import MainCodeFile

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.main_pool_cache_visibility import BASE, POOL, STAGE, cache_plan, wrapper
from scripts.probe_common_display_name_hook import branch_link

SOURCE = '651da6a67282b1abca58ac7b01769aee01ed78edf26e72245a0e9a469a856559'
FIELD, OFFSET = 0x1FD20, 0x133FF4
ENGLISH = b'~%d days\0'


def transform(source, clean, canonical):
    assert sha(source) == SOURCE
    japanese = '約%d日'.encode('cp932') + b'\0\0'
    assert clean[OFFSET:OFFSET + 8] == japanese
    assert source[OFFSET:OFFSET + 8] == b'%d days\0'
    assert canonical[OFFSET:OFFSET + 8] in (japanese, b'%d days\0')
    for arm in (source, clean, canonical):
        assert struct.unpack_from('<I', arm, FIELD)[0] == BASE + OFFSET
    cache_plan(source)
    code = MainCodeFile(source, BASE)
    before = [bytes(section.data) for section in code.sections]
    packed = bytearray(before[3][:-48])
    preserved = len(packed)
    pointer = POOL + len(packed)
    packed.extend(ENGLISH)
    packed.extend(bytes(-len(packed) % 32))
    size = len(packed) + 64
    assert POOL + size <= STAGE and STAGE + size + 48 <= 0x023F4000
    packed.extend(wrapper(STAGE + len(packed), STAGE + size, size, source))
    code.sections[3].data = packed + before[3][-48:-4] + struct.pack('<I', size)
    changes = []
    for offset, value in [(FIELD, pointer), (0x8E4, branch_link(BASE + 0x8E4, STAGE + size - 64)),
                          (0xE45DC, POOL + size)]:
        changes.append({'offset': offset, 'before': struct.unpack_from('<I', source, offset)[0], 'after': value})
        struct.pack_into('<I', code.sections[0].data, offset, value)
    saved = bytes(code.save())
    parsed = MainCodeFile(saved, BASE)
    restored = bytearray(parsed.sections[0].data)
    for row in changes:
        off = row['offset']
        restored[off:off + 4] = before[0][off:off + 4]
    off = code.codeSettingsOffs
    restored[off:off + 12] = before[0][off:off + 12]
    assert bytes(restored) == before[0]
    assert all(bytes(parsed.sections[i].data) == before[i] for i in (1, 2))
    assert bytes(parsed.sections[3].data[:preserved]) == before[3][:-48]
    return saved, {'source_arm9_sha256': SOURCE, 'target_arm9_sha256': sha(saved),
                   'Japanese': '約%d日', 'English': '~%d days', 'pointer': pointer,
                   'changes': changes, 'cache': cache_plan(saved), 'inherited_pool_bytes_preserved': preserved,
                   'original_numeric_calculation_format_argument_and_old_string_unchanged': True,
                   'changed_records': ['DK4_ENDURANCE_APPROXIMATION_MARKER']}


def apply_release(source, clean, canonical, path):
    config = json.loads(Path(path).read_text(encoding='utf-8'))
    assert config['format'] == 'dk4-endurance-approximation-release-v1'
    for name, digest in config['verification_evidence_sha256'].items():
        assert sha(Path(name).read_bytes()) == digest
    saved, plan = transform(source, clean, canonical)
    assert sha(saved) == config['target_arm9_sha256']
    return saved, plan
