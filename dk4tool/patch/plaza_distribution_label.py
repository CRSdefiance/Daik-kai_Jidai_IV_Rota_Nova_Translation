"""Localize the source-owned Square goods-distribution menu without pool growth."""

import json
import struct
from pathlib import Path

from ndspy.code import MainCodeFile, loadOverlayTable

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage

SOURCE = 'a49549b7300e6e101d52cdeabeab857ba32a20a49bbe7bad75f69d17a6f5be3b'
START, END = 0x143E98, 0x143EB4
FIELD = 0x143F88
TEXT = b'Trends\0Distribute Goods\0'


def transform(source):
    if sha(source) != SOURCE:
        raise ValueError('Square distribution label requires complete V621')
    clean_rom = NdsImage.open('work/clean.nds')
    clean = clean_rom.read_file('/__arm9__.bin')
    original = '流行情報'.encode('cp932') + bytes(4) + '交易品の配布'.encode('cp932') + bytes(4)
    current = b'Trends' + bytes(6) + '交易品の配布'.encode('cp932') + bytes(4)
    assert clean[START:END] == original and source[START:END] == current
    assert struct.unpack_from('<I', source, FIELD)[0] == 0x02143EA4
    code = MainCodeFile(source, 0x02000000)
    before = [bytes(s.data) for s in code.sections]
    units = [(f'main{i}', s.ramAddress, bytes(s.data)) for i, s in enumerate(code.sections)]
    units += [(f'overlay{i}', s.ramAddress, bytes(s.data)) for i, s in loadOverlayTable(
        clean_rom.rom.arm9OverlayTable, lambda _, fid: clean_rom.rom.files[fid]).items()]
    owners = [(name, base + at, struct.unpack_from('<I', data, at)[0])
              for name, base, data in units for at in range(len(data) - 3)
              if 0x02000000 + START <= struct.unpack_from('<I', data, at)[0] < 0x02000000 + END]
    assert owners == [('main0', 0x02143F78, 0x02143E98), ('main0', 0x02143F88, 0x02143EA4)]
    target_pointer = 0x02000000 + START + len(b'Trends\0')
    code.sections[0].data[START:END] = TEXT.ljust(END - START, b'\0')
    struct.pack_into('<I', code.sections[0].data, FIELD, target_pointer)
    target = bytes(code.save())
    parsed = MainCodeFile(target, 0x02000000)
    restored = bytearray(parsed.sections[0].data)
    restored[START:END] = before[0][START:END]
    restored[FIELD:FIELD + 4] = before[0][FIELD:FIELD + 4]
    assert restored == before[0]
    assert all(bytes(s.data) == before[i] for i, s in enumerate(parsed.sections) if i)
    record = {
        'id': 'SQUARE_DISTRIBUTE_GOODS', 'japanese': '交易品の配布', 'english': 'Distribute Goods',
        'speaker': 'Square action menu',
        'context': 'Original Plaza menu action1 opens Cargo Setup mode2 through0205ED34 and020832E0 when cargo and an eligible sailor are available. The neighboring action is Trends.',
        'source_meaning': 'Distribute trade goods.',
        'localization_note': 'Use a complete verb-object menu label. Keep the distinct Distributed Goods header and Trends action. Repack both exclusively owned strings so no English word needs abbreviation and no pool expands.',
        'review': {'source': True, 'context': True, 'localization': True, 'naturalness': True, 'formatting': False}}
    return target, {'source_arm9_sha256': SOURCE, 'target_arm9_sha256': sha(target),
                    'translation_policy': 'natural-dialogue-v2', 'target_locale': 'en-US', 'records': [record],
                    'owned_span': [START, END], 'all_unaligned_source_owners': [list(row) for row in owners],
                    'target_pointer': target_pointer, 'repacked_bytes': len(TEXT),
                    'all_other_strings_code_menu_enable_rules_sections_startup_pool_and_arenas_exact': True,
                    'changed_records': ['SQUARE_DISTRIBUTE_GOODS'], 'experimental': True, 'full_goal_complete': False}


def apply_release(source, path):
    config = json.loads(Path(path).read_text(encoding='utf-8'))
    assert config['format'] == 'dk4-plaza-distribution-label-v1'
    target, proof = transform(source)
    assert config['proof']['records'][0]['review']['formatting'] is True
    cases = config['proof']['native_label_fit_cases']
    assert [r['text'] for r in cases] == ['Trends', 'Distribute Goods']
    assert all(r['whole_256x16_plane_and_guards_exact'] for r in cases)
    proof['records'][0]['review']['formatting'] = True
    proof['native_label_fit_cases'] = cases
    assert config['proof'] == proof
    return target, proof
