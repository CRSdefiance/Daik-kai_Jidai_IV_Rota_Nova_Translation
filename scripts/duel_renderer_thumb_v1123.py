"""Research-only faithful Thumb transcription of the original duel renderer.

No playable ROM is built. Compacting the existing function may provide owned
storage for its post-expansion formatter without changing a section or arena.
"""
from pathlib import Path
from keystone import Ks, KS_ARCH_ARM, KS_MODE_ARM, KS_MODE_THUMB

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.verify_village_wrap_v608 import read, save

BASE = 0x02000000
START, END = BASE + 0xDA28, BASE + 0xDB5C
ROOT = Path('work/analysis/duel_renderer_thumb_v1123')
ROM = Path('out/all_routes_combined_v1105_candidate.nds')

ASSEMBLY = '''
push {r4-r7,lr}
sub sp,#16
sub sp,#508
sub sp,#508
sub sp,#100
mov r4,r0
mov r5,r1
mov r6,r2
mov r7,r3
movs r0,#0
str r0,[r4,#48]
str r6,[r4,#52]
str r7,[r4,#56]
movs r2,#1
str r2,[r4,#16]
add r0,sp,#8
blx 0x020cf2c4
ldr r2,[sp,#8]
ldr r1,[sp,#12]
str r2,[sp,#0]
str r1,[sp,#4]
mov r0,r4
adds r0,#60
blx 0x020d393c
add r0,sp,#16
mov r1,r5
movs r2,#0
blx 0x02053914
add r0,sp,#1008
adds r0,#32
mov r1,r4
adds r1,#60
movs r2,#1
blx 0x020d5160
ldr r0,[sp,#4]
cmp r0,#1
movs r3,#0
bne y_ready
movs r3,#12
y_ready:
add r0,sp,#1008
adds r0,#32
movs r1,#15
str r1,[r0,#48]
movs r2,#0
str r2,[r0,#36]
str r3,[r0,#40]
add r1,sp,#16
blx 0x020d5404
font_return:
ldr r0,[r4,#56]
cmp r0,#0
bne done
movs r5,#0
wait_loop:
ldr r0,wait_a
movs r1,#0
blx 0x020ca890
ldr r0,wait_b
blx 0x020c9d98
ldr r0,wait_c
movs r1,#5
movs r2,#0
blx 0x020cf534
cmp r0,#0
beq next_wait
movs r0,#159
lsls r0,r0,#4
blx 0x020c9c48
b wait_done
next_wait:
adds r5,#1
cmp r5,#60
ble wait_loop
wait_done:
movs r0,#0
str r0,[r4,#16]
done:
add r0,sp,#1008
adds r0,#32
blx 0x020d5140
add sp,#508
add sp,#508
add sp,#100
add sp,#16
pop {r4-r7,pc}
.align 2
wait_a: .word 0x022cf7dc
wait_b: .word 0x022cf784
wait_c: .word 0x023120b4
'''


def assemble(arm):
    # Original literal values are exact;never infer engine context constants.
    import struct
    expected = tuple(struct.unpack_from('<I', arm, off)[0] for off in (0xDB50, 0xDB54, 0xDB58))
    assert expected == (0x022CF7DC, 0x022CF784, 0x023120B4), tuple(hex(n) for n in expected)
    head = bytes(Ks(KS_ARCH_ARM, KS_MODE_ARM).asm('add ip,pc,#1;bx ip', START)[0])
    body = bytes(Ks(KS_ARCH_ARM, KS_MODE_THUMB).asm(ASSEMBLY, START + len(head))[0])
    assert len(head + body) <= END - START
    return head + body


def main():
    assert not ROOT.exists()
    rom = NdsImage.open(ROM)
    arm = rom.read_file('/__arm9__.bin')
    source = NdsImage.open('work/clean.nds').read_file('/__arm9__.bin')
    assert arm[START - BASE:END - BASE] == source[START - BASE:END - BASE]
    fonts = read('work/analysis/duel_full_name_fonts_v1119/native_all_source_names_font_proof.json')
    assert sha(ROM.read_bytes()) == fonts['candidate_sha256']
    replacement = assemble(arm)
    ROOT.mkdir(parents=True)
    target = bytearray(arm)
    target[START - BASE:END - BASE] = replacement + bytes(END - START - len(replacement))
    path = ROOT / 'proposed_ARM9_RESEARCH_ONLY.bin'
    path.write_bytes(target)
    save(ROOT / 'assembly_proposal.json', {
        'candidate': str(ROM), 'candidate_sha256': fonts['candidate_sha256'],
        'source_ARM9_sha256': sha(arm), 'research_ARM9_sha256': sha(target),
        'owned_existing_function': [START, END], 'old_bytes': END - START,
        'transcription_bytes': len(replacement), 'remaining_function_tail_bytes': END - START - len(replacement),
        'original_ARM_entry_switches_to_Thumb_and_preserves_all_callee_saved_registers': True,
        'proposed_private_frame_alloc_bytes': 0x45C, 'proposed_saved_register_bytes': 20, 'proposed_private_padding_bytes':16,
        'new_outer_return_font_SP_offset': 0x47C, 'new_voice_table_font_SP_offset': 0x4A4,
        'source_hex': arm[START - BASE:END - BASE].hex(), 'target_hex': bytes(target[START - BASE:END - BASE]).hex(),
        'ASM': ASSEMBLY, 'native_caller_geometry_timing_and_storage_ownership_checks_pending': True,
        'not_a_production_formatter_or_playable_ROM': True,
        'producer_sha256': sha(Path(__file__).read_bytes()), 'full_goal_complete': False})
    print(f'Research transcription:{len(replacement)} bytes within original{END-START};remaining{END-START-len(replacement)}. Native equivalence pending.')


if __name__ == '__main__':
    main()
