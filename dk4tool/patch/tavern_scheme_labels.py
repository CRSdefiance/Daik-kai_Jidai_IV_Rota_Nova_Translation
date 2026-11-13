"""Complete source-owned Tavern scheme labels without expanding any section."""

import json
import struct
from pathlib import Path

from ndspy.code import MainCodeFile, loadOverlayTable

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage

SOURCE = '9a05ef9a25367d53dc7affa1c24e70b84fa9123388701adefcf94e0d21add280'
LABELS = (
    (0x118BD4, 0x143B84, '策謀の立案', 'Schemes', 0x143B3C),
    (0x118B64, 0x143B6C, '艦隊誘導', 'Lure Fleet', 0x143B6C),
    (0x118B74, 0x143B78, '偽文書制作', 'Forge Papers', 0x143B77),
    (0x118B84, 0x143B54, '悪い噂', 'Bad Rumors', 0x143B84),
    (0x118B94, 0x143B3C, '買収', 'Bribe', 0x143B54),
)
SPANS = ((0x143B3C, 0x143B44), (0x143B54, 0x143B5C), (0x143B6C, 0x143B90))


def transform(source):
    if sha(source) != SOURCE:
        raise ValueError('Tavern scheme labels require the complete V623 stack')
    clean_rom = NdsImage.open('work/clean.nds')
    clean = clean_rom.read_file('/__arm9__.bin')
    for lo, hi in SPANS:
        assert source[lo:hi] == clean[lo:hi]
    for field, old, jp, _, _ in LABELS:
        assert struct.unpack_from('<I', source, field)[0] == 0x02000000 + old
        assert clean[old:].split(b'\0', 1)[0] == jp.encode('cp932')
    code = MainCodeFile(source, 0x02000000)
    before = [bytes(s.data) for s in code.sections]
    units = [(f'main{i}', s.ramAddress, bytes(s.data)) for i, s in enumerate(code.sections)]
    units += [(f'overlay{i}', s.ramAddress, bytes(s.data)) for i, s in loadOverlayTable(
        clean_rom.rom.arm9OverlayTable, lambda _, fid: clean_rom.rom.files[fid]).items()]
    owners = [(name, base + at, struct.unpack_from('<I', data, at)[0])
              for name, base, data in units for at in range(len(data) - 3)
              if any(0x02000000 + lo <= struct.unpack_from('<I', data, at)[0] < 0x02000000 + hi
                     for lo, hi in SPANS)]
    assert owners == sorted([('main0', 0x02000000 + f, 0x02000000 + old)
                             for f, old, _, _, _ in LABELS], key=lambda x: x[1])
    main = code.sections[0].data
    for lo, hi in SPANS:
        main[lo:hi] = bytes(hi - lo)
    for field, _, _, text, target in LABELS:
        payload = text.encode('ascii') + b'\0'
        assert any(lo <= target and target + len(payload) <= hi for lo, hi in SPANS)
        assert not any(main[target:target + len(payload)])
        main[target:target + len(payload)] = payload
        struct.pack_into('<I', main, field, 0x02000000 + target)
    result = bytes(code.save())
    parsed = MainCodeFile(result, 0x02000000)
    restored = bytearray(parsed.sections[0].data)
    for lo, hi in SPANS:
        restored[lo:hi] = before[0][lo:hi]
    for field, *_ in LABELS:
        restored[field:field + 4] = before[0][field:field + 4]
    assert restored == before[0]
    assert all(bytes(s.data) == before[i] for i, s in enumerate(parsed.sections) if i)
    draft = json.loads(Path('translations/tavern_scheme_labels_review_v1.json').read_text(encoding='utf-8'))
    assert [(r['field'], r['japanese'], r['english']) for r in draft['records']] == [
        (f, jp, en) for f, _, jp, en, _ in LABELS]
    return result, {
        'source_arm9_sha256': SOURCE, 'target_arm9_sha256': sha(result),
        'translation_policy': 'natural-dialogue-v2', 'target_locale': 'en-US',
        'records': draft['records'], 'owned_spans': [list(x) for x in SPANS],
        'all_unaligned_source_owners': [list(x) for x in owners],
        'all_other_strings_RTTI_interjections_code_rules_pool_startup_extents_exact': True,
        'changed_records': [r['id'] for r in draft['records']],
        'experimental': True, 'full_goal_complete': False}


def apply_release(source, path):
    config = json.loads(Path(path).read_text(encoding='utf-8'))
    assert config['format'] == 'dk4-tavern-scheme-labels-v1'
    target, proof = transform(source)
    for row in proof['records']:
        row['review']['formatting'] = True
    cases = config['proof']['native_label_fit_cases']
    assert [r['text'] for r in cases] == [x[3] for x in LABELS]
    assert all(r['whole_256x16_plane_and_guards_exact'] for r in cases)
    proof['native_label_fit_cases'] = cases
    assert proof == config['proof']
    return target, proof
