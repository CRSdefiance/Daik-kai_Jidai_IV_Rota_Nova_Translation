"""Complete shared sailing-condition names in the existing owned staged pool."""

import json
import struct
from pathlib import Path

from ndspy.code import MainCodeFile

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.main_pool_cache_visibility import BASE, POOL, STAGE, cache_plan, wrapper
from scripts.probe_common_display_name_hook import branch_link

SOURCE = '4db3361c2c281d38a0329151b83e8fad399594b4e8ed35615174e8669a941e3f'
TABLE = 0x148E00
LABELS = (
    ('壊血病', 'Scurvy'), ('鼠発生', 'Rat Infestation'), ('嵐', 'Storm'), ('吹雪', 'Blizzard'),
    ('雨', 'Rain'), ('雪', 'Snow'), ('雷', 'Lightning'), ('霧', 'Fog'), ('オーロラ', 'Aurora'),
    ('大イカ', 'Giant Squid'), ('化け魚', 'Monster Fish'), ('鯨', 'Whales'), ('イルカ', 'Dolphins'),
    ('セイレーン', 'Sirens'), ('人魚', 'Mermaids'), ('謎の泡', 'Strange Bubbles'), ('竜巻', 'Tornado'),
    ('大渦潮', 'Whirlpool'), ('暗礁', 'Reefs'), ('流氷', 'Drift Ice'), ('反乱', 'Mutiny'),
    ('混乱', 'Confusion'), ('水漏れ', 'Leaks'), ('伝染病', 'Epidemic'), ('凪', 'Calm'), ('サメ', 'Sharks'),
)


def transform(source, clean, canonical):
    if sha(source) != SOURCE:
        raise ValueError('Exact complete V307 ARM9 required')
    code = MainCodeFile(source, BASE)
    before = [bytes(s.data) for s in code.sections]
    cache_plan(source)
    packed = bytearray(before[3][:-48])
    preserved = len(packed)
    records, changes = [], []
    for index, (japanese, english) in enumerate(LABELS):
        field = TABLE + index * 4
        original = struct.unpack_from('<I', source, field)[0]
        offset = original - BASE
        raw = japanese.encode('cp932') + b'\0'
        for arm in (source, clean, canonical):
            if (struct.unpack_from('<I', arm, field)[0] != original
                    or arm[offset:offset + len(raw)] != raw):
                raise ValueError('Original condition label or table order differs')
        if [p for p in range(len(source) - 3) if source[p:p + 4] == struct.pack('<I', original)] != [field]:
            raise ValueError('Condition name has unclassified pointer aliases')
        pointer = POOL + len(packed)
        packed.extend(english.encode('ascii') + b'\0')
        struct.pack_into('<I', code.sections[0].data, field, pointer)
        changes.append({'offset': field, 'before': original, 'after': pointer})
        records.append({'id': f'DK4_SAILING_CONDITION_{index:02d}', 'index': index,
                        'Japanese': japanese, 'English': english, 'source_pointer': original,
                        'table_field': field, 'target_pointer': pointer})
    packed.extend(bytes((-len(packed)) % 32))
    size = len(packed) + 64
    if POOL + size > STAGE or STAGE + size + 48 > 0x023F4000:
        raise ValueError('Condition names exceed the owned arena')
    entry, copy = STAGE + len(packed), STAGE + size
    packed.extend(wrapper(entry, copy, size, source))
    code.sections[3].data = packed + before[3][-48:-4] + struct.pack('<I', size)
    for field, value in ((0x8E4, branch_link(BASE + 0x8E4, entry)), (0xE45DC, POOL + size)):
        changes.append({'offset': field, 'before': struct.unpack_from('<I', source, field)[0], 'after': value})
        struct.pack_into('<I', code.sections[0].data, field, value)
    saved = bytes(code.save())
    parsed = MainCodeFile(saved, BASE)
    restored = bytearray(parsed.sections[0].data)
    for row in changes:
        at = row['offset']
        restored[at:at + 4] = before[0][at:at + 4]
    at = code.codeSettingsOffs
    restored[at:at + 12] = before[0][at:at + 12]
    assert bytes(restored) == before[0]
    assert all(bytes(parsed.sections[n].data) == before[n] for n in (1, 2))
    assert bytes(parsed.sections[3].data[:preserved]) == before[3][:-48]
    return saved, {'source_arm9_sha256': SOURCE, 'target_arm9_sha256': sha(saved), 'records': records,
                   'changes': changes, 'payload_bytes': size, 'prior_payload_bytes_preserved': preserved,
                   'owned_pool_remaining_bytes': STAGE - POOL - size, 'cache': cache_plan(saved),
                   'changed_records': [r['id'] for r in records],
                   'original_strings_native_selector_and_all_other_data_code_preserved': True}


def apply_release(source, clean, canonical, path):
    config = json.loads(Path(path).read_text(encoding='utf-8'))
    if config.get('format') != 'dk4-sailing-condition-names-release-v1':
        raise ValueError('Unknown sailing condition names release')
    for filename, digest in config['verification_evidence_sha256'].items():
        if sha(Path(filename).read_bytes()) != digest:
            raise ValueError('Condition name native evidence differs')
    saved, proof = transform(source, clean, canonical)
    if sha(saved) != config['target_arm9_sha256']:
        raise ValueError('Condition name target differs')
    return saved, proof
