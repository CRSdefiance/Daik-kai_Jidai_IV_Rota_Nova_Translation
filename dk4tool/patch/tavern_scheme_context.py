"""Bind every scheme name and wrap the complete later Tavern portrait family."""

import json
import struct
from pathlib import Path

from keystone import KS_ARCH_ARM, KS_MODE_ARM, Ks
from ndspy.code import MainCodeFile

from dk4tool.dialogue.review import validate_natural_dialogue_batch
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from dk4tool.script.common_message_table import common_message_entries

SOURCE = 'e7c4e62f4fe5b621b1d4bed2123ab26d033698237e47b4b425e6fc9176a5b5a0'
MANUSCRIPT = Path('translations/tavern_scheme_context_manuscript_v1.json')
NAMES = ((6, 0x14C600, 0x0214C558, 0x02143B6C, 'Lure Fleet'),
         (7, 0x14C604, 0x0214C594, 0x02143B77, 'Forge Papers'),
         (8, 0x14C608, 0x0214C550, 0x02143B84, 'Bad Rumors'),
         (9, 0x14C60C, 0x0214C530, 0x02143B54, 'Bribe'))
HOOK = 0x01FFCF54


def transform(common, arm):
    if sha(arm) != SOURCE:
        raise ValueError('Scheme contexts require the complete V624 ARM9')
    manuscript = json.loads(MANUSCRIPT.read_text(encoding='utf-8'))
    validate_natural_dialogue_batch(manuscript)
    rows = manuscript['records']
    assert [r['message_id'] for r in rows] == [918, 920]
    clean_rom = NdsImage.open('work/clean.nds')
    clean = clean_rom.read_file('/__arm9__.bin')
    original = common_message_entries(clean_rom.read_file('/COMMON/MESFILE.DK4'), clean, clean=True)
    entries = common_message_entries(common, arm, clean=False)
    data = IlnkContainer.parse(common)
    for row in rows:
        n = row['message_id']
        assert row['source_hex'] == original[n].text.hex()
        assert row['japanese'] == original[n].text.decode('cp932')
        assert entries[n].text.startswith(b'The charge is %s coins. Is that acceptable?')
        text = row['english'].removesuffix('{PAD}').encode('ascii')
        assert len(text) <= len(entries[n].text) and text.count(b'%s') == 1
        entry = entries[n]
        block = bytearray(data.blocks[entry.block])
        assert block[entry.block_offset:entry.block_offset + len(entry.text)] == entry.text
        block[entry.block_offset:entry.block_offset + len(entry.text)] = text.ljust(len(entry.text), b' ')
        data.blocks[entry.block] = bytes(block)
    result_common = data.to_bytes()
    assert len(result_common) == len(common)
    code = MainCodeFile(arm, 0x02000000)
    before = [bytes(s.data) for s in code.sections]
    assert len(before) == 5 and code.sections[4].ramAddress == 0x01FFC000 and len(before[4]) == 4096
    assert arm[0x93D28:0x93D6C] == clean[0x93D28:0x93D6C]
    for _, field, old, target, text in NAMES:
        assert struct.unpack_from('<I', arm, field)[0] == old == struct.unpack_from('<I', clean, field)[0]
        assert arm[target - 0x02000000:].split(b'\0', 1)[0] == text.encode('ascii')
        struct.pack_into('<I', code.sections[0].data, field, target)
    ks = Ks(KS_ARCH_ARM, KS_MODE_ARM)
    at = HOOK - code.sections[4].ramAddress
    old = bytes(ks.asm('cmp r3,#53', HOOK)[0])
    new = bytes(ks.asm('cmp r3,#168', HOOK)[0])
    assert before[4][at:at + 4] == old
    # r3 is native_message_id-820 here. Retain all existing branches, including
    # the exact portrait caller filter, repair801 and later clue family.
    code.sections[4].data[at:at + 4] = new
    result_arm = bytes(code.save())
    parsed = MainCodeFile(result_arm, 0x02000000)
    restored = bytearray(parsed.sections[0].data)
    for _, field, *_ in NAMES:
        restored[field:field + 4] = before[0][field:field + 4]
    assert restored == before[0]
    assert all(bytes(parsed.sections[i].data) == before[i] for i in (1, 2, 3))
    restored = bytearray(parsed.sections[4].data)
    restored[at:at + 4] = old
    assert restored == before[4]
    after = common_message_entries(result_common, result_arm, clean=False)
    assert len(entries) == len(after)
    replacements = {r['message_id']: r['english'].removesuffix('{PAD}').encode('ascii') for r in rows}
    for a, b in zip(entries, after, strict=True):
        assert (a.block, a.block_offset, a.copy_end) == (b.block, b.block_offset, b.copy_end)
        assert b.text == (replacements[a.message_id].ljust(len(a.text), b' ') if a.message_id in replacements else a.text)
    return result_common, result_arm, {
        'source_arm9_sha256': SOURCE, 'target_arm9_sha256': sha(result_arm),
        'source_common_sha256': sha(common), 'target_common_sha256': sha(result_common),
        'manuscript_sha256': sha(MANUSCRIPT.read_bytes()), 'name_bindings': [list(r) for r in NAMES],
        'original_scheme_getters': [0x02093D28, 0x02093D5C],
        'retained_portrait_family': [820, 873], 'added_portrait_family': [874, 988],
        'original_exact_portrait_parent_return': 0x02054014,
        'only_four_pointer_fields_one_cmp_and_two_owned_message_texts_changed': True,
        'all_other_prose_controls_native_offsets_copy_extents_and_code_preserved': True,
        'all_section_extents_pool_cache_startup_arenas_and_artwork_exact': True,
        'changed_records': ['GENERAL_SCHEME_NAME_' + str(n) for n, *_ in NAMES] +
                           ['COMMON_MESSAGE_918', 'COMMON_MESSAGE_920', 'COMMON_LATER_TAVERN_PORTRAIT_WORD_WRAP'],
        'experimental': True, 'full_goal_complete': False}


def apply_release(common, arm, path):
    config = json.loads(Path(path).read_text(encoding='utf-8'))
    assert config['format'] == 'dk4-tavern-scheme-context-v1'
    result_common, result_arm, proof = transform(common, arm)
    assert config['proof'] == proof
    return result_common, result_arm, proof
