"""Complete Ship Name captions in existing owned keyboard data space."""

import json
import struct
from pathlib import Path

from ndspy.code import MainCodeFile, loadOverlayTable

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage

BASE, START, END = 0x02000000, 0x01FFC7B4, 0x01FFC800
POINTERS = ((0x636E0, 0x021447D0), (0xAEB90, 0x02156080))
SOURCE = '35a29ad707a3d035c1db3aed3e98646180bdc5bde8bd6b38cf57f3a6252e9ada'
TEXT = b'Ship Name\0'


def transform(source):
    if sha(source) != SOURCE:
        raise ValueError('Ship Name heading requires the complete pinned V613 ARM9')
    clean_rom = NdsImage.open('work/clean.nds')
    clean = clean_rom.read_file('/__arm9__.bin')
    code = MainCodeFile(source, BASE)
    before = [bytes(s.data) for s in code.sections]
    assert len(before) == 5 and code.sections[4].ramAddress == 0x01FFC000 and len(before[4]) == 4096
    offset = START - code.sections[4].ramAddress
    assert before[4][offset:END - code.sections[4].ramAddress] == bytes(END - START)
    # The V599 keyboard wrapper ends exactly at START and tail-calls the native
    # painter. This remaining zero gap is data, with no code fall-through.
    units = [(s.ramAddress, bytes(s.data)) for s in code.sections]
    units += [(s.ramAddress, bytes(s.data)) for s in loadOverlayTable(
        clean_rom.rom.arm9OverlayTable, lambda _, index: clean_rom.rom.files[index]).values()]
    aliases = [(base + i, struct.unpack_from('<I', data, i)[0]) for base, data in units
               for i in range(len(data) - 3) if START <= struct.unpack_from('<I', data, i)[0] < END]
    if aliases:
        raise ValueError('Keyboard data gap has an existing original code/data reference')
    for at, pointer in POINTERS:
        assert struct.unpack_from('<I', source, at)[0] == struct.unpack_from('<I', clean, at)[0] == pointer
        assert source[pointer - BASE:pointer - BASE + 5] == clean[pointer - BASE:pointer - BASE + 5] == bytes.fromhex('914496bc00')
        struct.pack_into('<I', code.sections[0].data, at, START)
    code.sections[4].data[offset:offset + len(TEXT)] = TEXT
    result = bytes(code.save())
    parsed = MainCodeFile(result, BASE)
    assert all(len(s.data) == len(before[i]) and s.ramAddress == code.sections[i].ramAddress
               for i, s in enumerate(parsed.sections))
    restored = bytearray(parsed.sections[0].data)
    for at, _ in POINTERS:
        restored[at:at + 4] = before[0][at:at + 4]
    assert restored == before[0]
    restored_helper = bytearray(parsed.sections[4].data)
    restored_helper[offset:offset + len(TEXT)] = before[4][offset:offset + len(TEXT)]
    assert restored_helper == before[4]
    assert all(bytes(parsed.sections[i].data) == before[i] for i in (1, 2, 3))
    return result, {'source_arm9_sha256': sha(source), 'target_arm9_sha256': sha(result),
                    'source_Japanese': '船名', 'English': 'Ship Name',
                    'source_pointer_literals': [[at, pointer] for at, pointer in POINTERS],
                    'replacement_pointer': START, 'owned_existing_zero_gap': [START, END],
                    'new_string_bytes': len(TEXT), 'existing_unaligned_main_autoload_overlay_aliases': aliases,
                    'original_Japanese_literals_and_all_keyboard_categories_inputs_names_unchanged': True,
                    'all_section_extents_pool_cache_heap_startup_and_native_instructions_unchanged': True,
                    'changed_records': ['SHIP_PURCHASE_NAME_HEADING', 'SHIP_RENAME_HEADING'],
                    'experimental': True, 'actual_native_caption_verification_pending': True, 'full_goal_complete': False}


def apply_release(source, path):
    config = json.loads(Path(path).read_text(encoding='utf-8'))
    assert config['format'] == 'dk4-ship-name-heading-v1'
    target, proof = transform(source)
    if config['proof'] != proof:
        raise ValueError('Ship Name source,ownership or complete target differs')
    return target, proof
