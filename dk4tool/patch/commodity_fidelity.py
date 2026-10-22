"""Restore complete commodity meanings within exclusively owned name storage."""

import json
import struct
from itertools import pairwise
from pathlib import Path

from ndspy.code import MainCodeFile

from dk4tool.patch.grand_race_menu_release import sha

BASE, TABLE, COUNT = 0x02000000, 0x15EF18, 124
SOURCE = '910a4543c51cbc886df98daf8410f0169970fade2d7fe5f209b46733fe4319bc'
CHANGES = {
    15: ('ヤシ油', 'Palm Oil'), 20: ('フカヒレ', 'Shark Fins'),
    24: ('シナモン', 'Cinnamon'), 40: ('白金', 'Platinum'),
    43: ('漆器', 'Lacquerware'), 47: ('生糸', 'Raw Silk'),
    49: ('毛織物', 'Wool Cloth'), 50: ('綿織物', 'Cotton Cloth'),
    52: ('麻織物', 'Hemp Cloth'), 60: ('乳香', 'Frankincense'),
    65: ('ベッコウ', 'Tortoiseshell'), 80: ('ウコン', 'Turmeric'),
    90: ('鉄鉱石', 'Iron Ore'), 91: ('銅鉱石', 'Copper Ore'),
    106: ('鯨肉', 'Whale Meat'), 107: ('黒羊毛', 'Black Wool'),
    118: ('鮭の燻製', 'Smoked Salmon'),
}
CHANGES_V2 = {**CHANGES, 15: ('ヤシ油', 'Coconut Oil')}


def transform(source, clean, config):
    if sha(source) != SOURCE:
        raise ValueError('Commodity fidelity requires the exact complete V633 ARM9')
    rows = config['records']
    changes = CHANGES_V2 if config.get('format') == 'dk4-commodity-fidelity-v2' else CHANGES
    regions = [tuple(r) for r in config['regions']]
    if len(rows) != COUNT or [r['index'] for r in rows] != list(range(COUNT)):
        raise ValueError('All124 commodity owners are required')
    if sum(hi - lo for lo, hi in regions) != 1124 or len(regions) != 94:
        raise ValueError('Require the reviewed source spans excluding native helper code')
    if regions != sorted(regions) or any(hi > ll for (_, hi), (ll, _) in pairwise(regions)):
        raise ValueError('Name spans overlap or differ in order')
    fields = {TABLE + i * 12 for i in range(COUNT)}
    covered, expected_refs = set(), set()
    changed = []
    for row in rows:
        i = row['index']
        field = TABLE + i * 12
        old = struct.unpack_from('<I', source, field)[0] - BASE
        jp = struct.unpack_from('<I', clean, field)[0] - BASE
        if source[old:source.index(0, old)].decode('ascii') != row['current']:
            raise ValueError('Current name identity differs')
        if clean[jp:clean.index(0, jp)].decode('cp932') != row['Japanese']:
            raise ValueError('Clean Japanese source differs')
        expected = changes.get(i, (row['Japanese'], row['current']))
        if (row['Japanese'], row['English']) != expected:
            raise ValueError('An unreviewed commodity meaning changed')
        covered.update(range(old, old + len(row['current']) + 1))
        if i != 106:
            if not any(lo <= old < old + len(row['current']) + 1 <= hi for lo, hi in regions):
                raise ValueError('Existing name leaves reviewed owned storage')
            expected_refs.add((field, BASE + old))
        if row['English'] != row['current']:
            changed.append(i)
    if set(changed) != set(changes):
        raise ValueError('Require exactly the17 reviewed complete labels')
    if any(source[i] for lo, hi in regions for i in range(lo, hi) if i not in covered):
        raise ValueError('An unowned nonzero byte or helper appears in name spans')
    # Visit every byte position, not only aligned literal words.
    actual = set()
    first, last = regions[0][0] + BASE, regions[-1][1] + BASE
    for at in range(len(source) - 3):
        word = struct.unpack_from('<I', source, at)[0]
        if first <= word < last and any(lo + BASE <= word < hi + BASE for lo, hi in regions):
            actual.add((at, word))
    if actual != expected_refs:
        raise ValueError('An additional source name owner or interior alias exists')
    result = bytearray(source)
    for lo, hi in regions:
        result[lo:hi] = bytes(hi - lo)
    written = set()
    roots = {int(i): offset for i, offset in config['root_offsets'].items()}
    by_id = {r['index']: r for r in rows}
    for i, offset in roots.items():
        raw = by_id[i]['English'].encode('ascii') + b'\0'
        if not any(lo <= offset < offset + len(raw) <= hi for lo, hi in regions):
            raise ValueError('A complete name overflows its source-owned span')
        span = set(range(offset, offset + len(raw)))
        if written & span:
            raise ValueError('Independent full names overlap')
        written |= span
        result[offset:offset + len(raw)] = raw
    mappings = []
    for row in rows:
        name = row['English']
        choices = [(i, offset + len(by_id[i]['English']) - len(name)) for i, offset in roots.items()
                   if by_id[i]['English'] == name or by_id[i]['English'].endswith(' ' + name)]
        if not choices:
            raise ValueError('A complete null-terminated name is missing')
        root_id, offset = min(choices)
        raw = name.encode('ascii') + b'\0'
        if result[offset:offset + len(raw)] != raw:
            raise ValueError('A suffix alias drops a character or terminator')
        field = TABLE + row['index'] * 12
        struct.pack_into('<I', result, field, BASE + offset)
        mappings.append({'index': row['index'], 'English': name, 'offset': offset,
                         'root_index': root_id,
                         'complete_suffix_alias': root_id != row['index'] and name != by_id[root_id]['English'],
                         'shared_complete_name': root_id != row['index']})
    restored = bytearray(result)
    for lo, hi in regions:
        restored[lo:hi] = source[lo:hi]
    for field in fields:
        restored[field:field + 4] = source[field:field + 4]
        if result[field + 4:field + 12] != source[field + 4:field + 12]:
            raise ValueError('Commodity gameplay metadata changed')
    if bytes(restored) != source:
        raise ValueError('Unowned ARM9 change')
    old, new = MainCodeFile(source, BASE), MainCodeFile(bytes(result), BASE)
    if [(s.ramAddress, len(s.data), s.bssSize) for s in old.sections] != [(s.ramAddress, len(s.data), s.bssSize) for s in new.sections]:
        raise ValueError('Section shape or bounds changed')
    if any(a.data != b.data for a, b in zip(old.sections[1:], new.sections[1:], strict=True)):
        raise ValueError('A staged payload or native ITCM section changed')
    return bytes(result), {'source_arm9_sha256': SOURCE, 'target_arm9_sha256': sha(result),
                           'records': mappings, 'changed_label_indices': changed,
                           'complete_names': COUNT, 'root_strings': len(roots),
                           'source_owned_bytes': 1124, 'stored_root_bytes': len(written),
                           'all124_metadata_fields_and_other107_name_meanings_exact': True,
                           'shared_old_Whale_string_and_its_other_owners_preserved': True,
                           'all_native_helpers_fonts_palettes_other_bytes_and_section_shapes_exact': True,
                           'no_pool_or_section_growth': True,
                           'changed_records': ['COMMODITY_COMPLETE_MEANING_' + str(i) for i in changed]}


def apply_release(source, clean, path):
    config = json.loads(Path(path).read_text(encoding='utf-8'))
    if config.get('format') not in ('dk4-commodity-fidelity-v1', 'dk4-commodity-fidelity-v2') or config.get('status') != 'reviewed-native-previews-experimental':
        raise ValueError('Reviewed complete-name preview configuration required')
    changes = CHANGES_V2 if config['format'] == 'dk4-commodity-fidelity-v2' else CHANGES
    layout_path = Path(config['original_layout_proof'])
    if sha(layout_path.read_bytes()) != config['original_layout_proof_sha256']:
        raise ValueError('Original owned name/helper layout proof changed')
    layout = json.loads(layout_path.read_text(encoding='utf-8'))
    regions = []
    for lo, hi in layout['name_repack']['source_string_regions']:
        segments = [(lo, hi)]
        for x, y, _ in layout['owned_tail_blocks']:
            segments = [r for left, right in segments for r in ((left, min(x, right)), (max(y, left), right)) if r[0] < r[1]]
        regions.extend(segments)
    if [list(r) for r in regions] != config['regions']:
        raise ValueError('Name storage overlaps or omits original helper exclusions')
    manuscript = json.loads(Path(config['manuscript']).read_text(encoding='utf-8'))
    if sha(Path(config['manuscript']).read_bytes()) != config['manuscript_sha256']:
        raise ValueError('Commodity source review changed after preview')
    if {r['index'] for r in manuscript['records']} != set(changes) or len(manuscript['records']) != len(changes):
        raise ValueError('All17 source and localization reviews are required')
    for row in manuscript['records']:
        if (row['Japanese'], row['English']) != changes[row['index']]:
            raise ValueError('Review text and complete intended name disagree')
    if any(not all(r['review'].values()) for r in manuscript['records']):
        raise ValueError('A corrected commodity review is incomplete')
    target, proof = transform(source, clean, config)
    if sha(target) != config['target_arm9_sha256']:
        raise ValueError('Target differs from reviewed native previews')
    return target, proof
