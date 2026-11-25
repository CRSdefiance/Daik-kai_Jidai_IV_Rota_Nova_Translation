"""Recognize original queued Strategist voice tables before portrait wrapping."""

import json
import struct
from pathlib import Path

from keystone import KS_ARCH_ARM, KS_MODE_ARM, Ks
from ndspy.code import MainCodeFile, loadOverlayTable

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage

SOURCE = '98b57756ef56ef0cebf6c5ee7b1b18a45c56b1809cec81561253fe04f3457a01'
ENTRY, SECOND, ALIGN, FALLBACK = 0x01FFCE1C, 0x01FFC664, 0x0214C550, 0x0214C530
SPANS = ((ENTRY, ENTRY + 36), (SECOND, SECOND + 28), (ALIGN, ALIGN + 20), (FALLBACK, FALLBACK + 8))
TABLES = (0x02117B40, 0x021181E0, 0x02118200, 0x02118220, 0x02118240, 0x02118260,
          0x02118280, 0x021182A0, 0x021182C0, 0x02118300, 0x02118320, 0x02118340)


def transform(source):
    if sha(source) != SOURCE:
        raise ValueError('Queued Strategist wrapping requires complete V625')
    code = MainCodeFile(source, 0x02000000)
    before = [bytes(s.data) for s in code.sections]
    assert len(before) == 5 and code.sections[4].ramAddress == 0x01FFC000
    assert len(before[4]) == 4096
    clean_rom = NdsImage.open('work/clean.nds')
    clean = clean_rom.read_file('/__arm9__.bin')
    for lo, hi in ((0x53CB0, 0x53D44), (0x53D44, 0x53DCC), (0x572D0, 0x57408)):
        assert source[lo:hi] == clean[lo:hi]
    groups = []
    for pointer in TABLES:
        at = pointer - 0x02000000
        assert source[at:at + 32] == clean[at:at + 32]
        ids = list(struct.unpack_from('<8I', source, at))
        assert all(n == 0xFFFFFFFF or 908 <= n <= 988 for n in ids)
        groups.append({'table': pointer, 'source_voice_message_IDs': ids})
    assert struct.unpack_from('<I', before[4], 0xDE8)[0] == 0x02053DB8
    assert struct.unpack_from('<I', before[4], 0xDF0)[0] == 0x02118800
    # Two immutable-string padding spans, not the Square pixel scratch surface
    # C1A0..C360 or mutable resource pointers C680/C6A0.
    assert before[4][0xE00:0xE1C] == b'Joachim\0Hodram\0Bergstrom\0'.ljust(28, b'\0')
    assert before[4][0x658:0x661] == b'Fleet %s\0'
    assert before[4][0xE1C:0xE40] == bytes(36)
    assert before[4][0x664:0x680] == bytes(28)
    assert source[0x14C530:0x14C538] == '買収'.encode('cp932') + bytes(4)
    assert source[0x14C550:0x14C564] == '悪い噂'.encode('cp932') + bytes(2) + '艦隊誘導'.encode('cp932') + bytes(4)
    units = [(s.ramAddress, bytes(s.data)) for s in code.sections]
    units += [(s.ramAddress, bytes(s.data)) for s in loadOverlayTable(
        clean_rom.rom.arm9OverlayTable, lambda _, f: clean_rom.rom.files[f]).values()]
    aliases = [(base + at, struct.unpack_from('<I', data, at)[0])
               for base, data in units for at in range(len(data) - 3)
               if any(lo <= struct.unpack_from('<I', data, at)[0] < hi for lo, hi in SPANS)]
    assert not aliases
    ks = Ks(KS_ARCH_ARM, KS_MODE_ARM)
    blocks = (
        (ENTRY, f'''ldr ip,[pc,#-60]
eor ip,r3,ip
cmp ip,#0
cmpne ip,#0x9c
bne 0x01ffcd98
ldr r3,[sp,#0x27c]
ldr ip,[pc,#-76]
sub r3,r3,ip
b {SECOND}'''),
        (SECOND, f'''add r3,r3,#0x620
cmp r3,#352
bls {ALIGN}
cmn r3,#0x6a0
beq 0x01ffcf78
b {FALLBACK}
nop'''),
        (ALIGN, f'''tst r3,#31
bne {FALLBACK}
cmp r3,#256
bne 0x01ffcf78
b {FALLBACK}'''),
        (FALLBACK, 'ldr r3,[sp,#0x264]; b 0x01ffcd98'))
    for (address, text), (lo, hi) in zip(blocks, SPANS, strict=True):
        assert address == lo
        data = bytes(ks.asm(text, address)[0])
        assert len(data) == hi - lo
        section = next(s for s in code.sections if s.ramAddress <= lo < s.ramAddress + len(s.data))
        section.data[lo - section.ramAddress:hi - section.ramAddress] = data
    old = bytes(ks.asm('bne 0x01ffcd98', 0x01FFCF48)[0])
    assert before[4][0xF48:0xF4C] == old
    code.sections[4].data[0xF48:0xF4C] = bytes(ks.asm(f'bne {ENTRY}', 0x01FFCF48)[0])
    result = bytes(code.save())
    parsed = MainCodeFile(result, 0x02000000)
    for i, s in enumerate(parsed.sections):
        restored = bytearray(s.data)
        for lo, hi in SPANS:
            if s.ramAddress <= lo < s.ramAddress + len(s.data):
                at = lo - s.ramAddress
                restored[at:at + hi - lo] = before[i][at:at + hi - lo]
        if i == 4:
            restored[0xF48:0xF4C] = old
        assert restored == before[i]
    return result, {
        'source_arm9_sha256': SOURCE, 'target_arm9_sha256': sha(result),
        'original_queued_role_portrait_parent_returns': [0x02053D24, 0x02053DB8],
        'original_voice_table_stack_offset': 0x27C, 'exact_source_voice_tables': groups,
        'table_interval_gap_021182E0_and_unaligned_addresses_excluded': True,
        'owned_immutable_padding_and_released_three_Japanese_name_strings': [list(r) for r in SPANS],
        'all_unaligned_main_autoload_overlay_aliases': aliases,
        'unmatched_callers_restore_original_parent_before_unchanged_SeaFoam_dispatch': True,
        'Square_scratch_mutable_market_slots_all_existing_names_and_helper_bodies_preserved': True,
        'all_section_extents_pool_cache_startup_arenas_and_other_bytes_exact': True,
        'changed_records': ['COMMON_QUEUED_STRATEGIST_SCHEME_VOICE_WORD_WRAP'],
        'experimental': True, 'full_goal_complete': False}


def apply_release(source, path):
    config = json.loads(Path(path).read_text(encoding='utf-8'))
    assert config['format'] == 'dk4-tavern-strategist-wrap-v1'
    target, proof = transform(source)
    assert proof == config['proof']
    return target, proof
