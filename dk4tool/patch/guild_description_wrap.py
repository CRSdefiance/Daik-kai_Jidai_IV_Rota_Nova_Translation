"""Whole-family Guild treasure descriptions in the existing portrait wrapper."""

import json
import struct
from pathlib import Path

from capstone import CS_ARCH_ARM, CS_MODE_ARM, Cs
from keystone import KS_ARCH_ARM, KS_MODE_ARM, Ks
from ndspy.code import MainCodeFile

from dk4tool.dialogue.review import validate_natural_dialogue_batch
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.script.common_message_table import common_message_entries

TEXT = "They call this a twisted horn. Some say it's a dragon's and that it can become medicine for any illness."


def transform(common, arm, manuscript):
    validate_natural_dialogue_batch(manuscript)
    if len(manuscript['records']) != 1 or manuscript['records'][0]['message_id'] != 3665 or manuscript['records'][0]['english'].removesuffix('{PAD}') != TEXT:
        raise ValueError('Complete reviewed Guild description required')
    before = common_message_entries(common, arm, clean=False)
    row = before[3665]
    if len(TEXT.encode()) > len(row.text):
        raise ValueError('Complete prose exceeds owned native entry')
    container = IlnkContainer.parse(common)
    block = bytearray(container.blocks[row.block])
    block[row.block_offset:row.block_offset + len(row.text)] = TEXT.encode().ljust(len(row.text), b' ')
    container.blocks[row.block] = bytes(block)
    target_common = container.to_bytes()
    code = MainCodeFile(arm, 0x02000000)
    sections = [bytes(s.data) for s in code.sections]
    if len(sections[4]) != 4092 or code.sections[4].ramAddress != 0x01FFC000:
        raise ValueError('Existing portrait wrapper extent differs')
    ks = Ks(KS_ARCH_ARM, KS_MODE_ARM)
    old = bytes(ks.asm(Path('dk4tool/patch/tavern_address_release.asm').read_text(encoding='utf-8'), 0x01FFCF3C)[0])
    if sections[4][3900:] != old:
        raise ValueError('Complete inherited portrait wrapper differs')
    new = bytes(ks.asm(Path(__file__).with_suffix('.asm').read_text(encoding='utf-8'), 0x01FFCF3C)[0])
    if len(new) != 196:
        raise ValueError('Guild wrapper exceeds the remaining four bytes')
    code.sections[4].data[3900:] = new
    # The old equipment continuation budget is one cell too wide for this
    # portrait context. Use existing zero padding for a tiny scoped selector;
    # equipment and old rumor/clue budgets remain37.
    reset, selector = 0x01FFCAB0, 0x01FFCB40
    if struct.unpack_from('<I', sections[4], reset - 0x01FFC000)[0] != 0xE3A07025:
        raise ValueError('Original continuation budget instruction differs')
    calls = [i.address + 4 for i in Cs(CS_ARCH_ARM, CS_MODE_ARM).disasm(new, 0x01FFCF3C)
             if i.mnemonic == 'bl' and i.op_str == '#0x1ffca00']
    if len(calls) != 1:
        raise ValueError('Portrait word-helper call identity differs')
    selection = f'''ldr ip,[sp,#32]
        ldr r7,caller
        cmp ip,r7
        mov r7,#37
        bxne lr
        ldr ip,[sp,#0x390]
        sub ip,ip,#0xe00
        sub ip,ip,#0x40
        cmp ip,#19
        movls r7,#36
        bx lr
    caller: .word {calls[0]}'''
    stub = bytes(ks.asm(selection, selector)[0])
    offset = selector - 0x01FFC000
    if any(sections[4][offset:offset + len(stub)]) or offset + len(stub) > 0xC00:
        raise ValueError('Original owned word-helper padding differs')
    code.sections[4].data[offset:offset + len(stub)] = stub
    hook = bytes(ks.asm(f'bl {selector}', reset)[0])
    code.sections[4].data[reset - 0x01FFC000:reset - 0x01FFC000 + 4] = hook
    saved = bytes(code.save())
    parsed = MainCodeFile(saved, 0x02000000)
    assert len(parsed.sections[4].data) == 4096
    restored_itcm = bytearray(parsed.sections[4].data[:3900])
    restored_itcm[offset:offset + len(stub)] = sections[4][offset:offset + len(stub)]
    restored_itcm[reset - 0x01FFC000:reset - 0x01FFC000 + 4] = sections[4][reset - 0x01FFC000:reset - 0x01FFC000 + 4]
    assert bytes(restored_itcm) == sections[4][:3900]
    assert all(bytes(parsed.sections[i].data) == sections[i] for i in (1, 2, 3))
    restored = bytearray(parsed.sections[0].data)
    restored[code.codeSettingsOffs:code.codeSettingsOffs + 12] = sections[0][code.codeSettingsOffs:code.codeSettingsOffs + 12]
    assert bytes(restored) == sections[0]
    after = common_message_entries(target_common, saved, clean=False)
    for a, b in zip(before, after):
        assert (a.block, a.block_offset, a.copy_end) == (b.block, b.block_offset, b.copy_end)
        assert b.text.rstrip() == TEXT.encode() if a.message_id == 3665 else b.text == a.text
    assert len(target_common) == len(common)
    return target_common, saved, {'changed_records': ['COMMON_MESSAGE_3665', 'GUILD_TREASURE_DESCRIPTION_WORD_WRAP'],
                                  'whole_Guild_description_family': [3648, 3667],
                                  'all3668_offsets_and_COMMON_cache_sizes_preserved': True,
                                  'all3667_other_messages_exact': True,
                                  'portrait_wrapper_bytes': 196, 'SDK_section4_bytes': 4096,
                                  'scoped_Guild_continuation_cells': 36,
                                  'old_equipment_rumor_clue_continuation_cells': 37,
                                  'selector_in_existing_owned_zero_padding': [selector, len(stub)],
                                  'all_other_first3900_ITCM_and_main_pool_exact': True,
                                  'no_arena_or_main_pool_growth': True}


def apply_release(common, arm, config_path):
    config = json.loads(Path(config_path).read_text(encoding='utf-8'))
    if config['format'] != 'dk4-guild-description-wrap-v1' or sha(common) != config['source_common_sha256'] or sha(arm) != config['source_arm9_sha256']:
        raise ValueError('Guild description source/config differs')
    if sha(Path(config['manuscript']).read_bytes()) != config['manuscript_sha256'] or sha(Path(__file__).with_suffix('.asm').read_bytes()) != config['wrapper_asm_sha256']:
        raise ValueError('Reviewed Guild manuscript/wrapper changed')
    common, arm, report = transform(common, arm, json.loads(Path(config['manuscript']).read_text(encoding='utf-8')))
    assert sha(common) == config['target_common_sha256'] and sha(arm) == config['target_arm9_sha256']
    return common, arm, report
