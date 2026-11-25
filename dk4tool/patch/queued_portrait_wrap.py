"""Apply paragraph wrapping to both original queued role/portrait factories.

The parent returns identify the same actor-backed 228-pixel message widget.
Voice-table addresses select prose, not a different text renderer. Keep the
existing bounded paragraph helper and every unrelated caller unchanged.
"""

from pathlib import Path

from keystone import KS_ARCH_ARM, KS_MODE_ARM, Ks
from ndspy.code import MainCodeFile

from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read

SOURCE = 'f88dda630fd7eaf589a98b918b0b0050722b8058045515ed3fbbc43bd875c2ff'
ADDRESS, SIZE = 0x01FFCE1C, 36
PREFIX = '''ldr ip,[pc,#-60]
eor ip,r3,ip
cmp ip,#0
cmpne ip,#0x9c
bne 0x01ffcd98
'''
OLD_ASM = PREFIX + '''ldr r3,[sp,#0x27c]
ldr ip,[pc,#-76]
sub r3,r3,ip
b 0x01ffc664
'''
ASM = PREFIX + '''b 0x01ffcf78
nop
nop
nop
'''


def transform(source):
    if sha(source) != SOURCE:
        raise ValueError('Queued portrait wrapping requires the complete pinned V651 ARM9')
    code = MainCodeFile(source, 0x02000000)
    before = [bytes(s.data) for s in code.sections]
    assert len(before) == 5 and code.sections[4].ramAddress == 0x01FFC000
    assert len(before[4]) == 4096
    ks = Ks(KS_ARCH_ARM, KS_MODE_ARM)
    old, new = [bytes(ks.asm(text, ADDRESS)[0]) for text in (OLD_ASM, ASM)]
    assert len(old) == len(new) == SIZE
    at = ADDRESS - code.sections[4].ramAddress
    assert before[4][at:at + SIZE] == old and old[:20] == new[:20]
    assert int.from_bytes(before[4][0xDE8:0xDEC], 'little') == 0x02053DB8
    code.sections[4].data[at:at + SIZE] = new
    result = bytes(code.save())
    after = MainCodeFile(result, 0x02000000)
    assert all(bytes(after.sections[i].data) == before[i] for i in range(4))
    restored = bytearray(after.sections[4].data)
    restored[at:at + SIZE] = old
    assert restored == before[4]
    return result, {
        'source_arm9_sha256': SOURCE, 'target_arm9_sha256': sha(result),
        'owned_existing_dispatcher': [ADDRESS, ADDRESS + SIZE],
        'exact_original_role_parent_returns': [0x02053D24, 0x02053DB8],
        'first20_bytes_parent_guard_unchanged': True,
        'voice_table_does_not_select_widget_geometry': True,
        'unchanged_active_expansion_and_wrap_path': 0x01FFCF78,
        'unchanged_bounded_paragraph_helper': 0x01FFCA00,
        'unchanged_other_parent_dispatch': 0x01FFCD98,
        'no_new_prose_or_manual_line_breaks': True,
        'only_existing36_byte_dispatcher_owned_all_other_sections_bytes_exact': True,
        'all_fonts_graphics_COMMON_text_native_tables_pool_cache_and_arenas_unchanged': True,
        'changed_records': ['COMMON_QUEUED_ROLE_PORTRAIT_SHARED_WORD_WRAP'],
        'experimental': True, 'full_goal_complete': False}


def apply_release(source, path):
    config = read(Path(path))
    assert config['format'] == 'dk4-queued-portrait-wrap-v1'
    target, proof = transform(source)
    if config['proof'] != proof:
        raise ValueError('Queued portrait wrapper source, scope or target differs')
    return target, proof
