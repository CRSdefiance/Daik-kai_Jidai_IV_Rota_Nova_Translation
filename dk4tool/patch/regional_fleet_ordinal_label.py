"""Give the source numbered-fleet formatter natural English word order."""

import json
import struct
from pathlib import Path

from ndspy.code import MainCodeFile, loadOverlayTable

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage

SOURCE = '44ddcbe97a8841727ccd766533cda20132389f269493eddab29337a9195c8b5c'
FIELD, ORIGINAL, SHARED, ADDRESS, END = 0x35288, 0x0213523C, 0x0215E977, 0x01FFC658, 0x01FFC680
TEXT = b'Fleet %s\0'


def transform(source):
    if sha(source) != SOURCE:
        raise ValueError('Numbered-fleet label requires complete V616 plus guarded assignments')
    clean_rom = NdsImage.open('work/clean.nds')
    clean = clean_rom.read_file('/__arm9__.bin')
    assert struct.unpack_from('<I', clean, FIELD)[0] == ORIGINAL
    japanese = '第%s艦隊'.encode('cp932') + b'\0'
    assert clean[ORIGINAL - 0x02000000:ORIGINAL - 0x02000000 + len(japanese)] == japanese
    assert struct.unpack_from('<I', source, FIELD)[0] == SHARED
    assert source[SHARED - 0x02000000:SHARED - 0x02000000 + 9] == b'%s Fleet\0'
    # Only this consumer is ordinal. The other three are person/company names.
    named_fields = (0x36B4C, 0x82E70, 0x9AE84)
    for field in named_fields:
        pointer = struct.unpack_from('<I', clean, field)[0]
        assert clean[pointer - 0x02000000:].split(b'\0', 1)[0].decode('cp932') == '%s艦隊'
        assert struct.unpack_from('<I', source, field)[0] == SHARED
    code = MainCodeFile(source, 0x02000000)
    before = [bytes(s.data) for s in code.sections]
    assert len(before) == 5 and code.sections[4].ramAddress == 0x01FFC000 and len(before[4]) == 4096
    at = ADDRESS - code.sections[4].ramAddress
    assert before[4][0x640:0x655] == b'Shortage\0\0\0\0Trending\0'
    assert before[4][at:END - code.sections[4].ramAddress] == bytes(END - ADDRESS)
    units = [(s.ramAddress, bytes(s.data)) for s in code.sections]
    units += [(s.ramAddress, bytes(s.data)) for s in loadOverlayTable(
        clean_rom.rom.arm9OverlayTable, lambda _, index: clean_rom.rom.files[index]).values()]
    aliases = [(base + i, struct.unpack_from('<I', data, i)[0]) for base, data in units
               for i in range(len(data) - 3) if ADDRESS <= struct.unpack_from('<I', data, i)[0] < END]
    assert not aliases
    # This constant follows Trending's terminator/padding and stops before the
    # mutable market-resource pointer at C680. Square's C1A0 buffer is untouched.
    code.sections[4].data[at:at + len(TEXT)] = TEXT
    struct.pack_into('<I', code.sections[0].data, FIELD, ADDRESS)
    result = bytes(code.save())
    parsed = MainCodeFile(result, 0x02000000)
    assert all(bytes(parsed.sections[i].data) == before[i] for i in (1, 2, 3))
    restored = bytearray(parsed.sections[0].data)
    restored[FIELD:FIELD + 4] = before[0][FIELD:FIELD + 4]
    assert restored == before[0]
    helper = bytearray(parsed.sections[4].data)
    helper[at:at + len(TEXT)] = before[4][at:at + len(TEXT)]
    assert helper == before[4]
    return result, {'source_arm9_sha256': sha(source), 'target_arm9_sha256': sha(result),
                    'source_Japanese': '第%s艦隊', 'English': 'Fleet %s',
                    'source_meaning': 'A fleet identified by its ordinal fleet number; the supplied number remains unchanged.',
                    'localization_note': 'English fleet numbering places Fleet before the number. The separate name-based %s Fleet formatter must remain unchanged.',
                    'review': {'source': True, 'context': True, 'localization': True, 'naturalness': True, 'formatting': True},
                    'sole_numbered_fleet_pointer_field': FIELD, 'original_clean_pointer': ORIGINAL,
                    'original_shared_pointer_and_name_based_fields_preserved': [SHARED, *named_fields],
                    'new_constant_address': ADDRESS, 'owned_zero_gap_excluding_mutable_market_slot': [ADDRESS, END],
                    'compiled_constant_bytes': len(TEXT), 'existing_unaligned_aliases': aliases,
                    'all_other_text_native_code_arguments_section_extents_pools_and_markets_preserved': True,
                    'changed_records': ['NUMBERED_FLEET_ENGLISH_WORD_ORDER'],
                    'experimental': True, 'full_goal_complete': False}


def apply_release(source, path):
    config = json.loads(Path(path).read_text(encoding='utf-8'))
    assert config['format'] == 'dk4-regional-fleet-ordinal-label-v1'
    target, proof = transform(source)
    if config['proof'] != proof:
        raise ValueError('Numbered-fleet source,ownership or target differs')
    return target, proof
