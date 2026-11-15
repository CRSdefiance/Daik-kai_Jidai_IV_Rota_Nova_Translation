"""Research front:exact duel scope,existing COMMON cache and native cache ops."""
from pathlib import Path
from keystone import Ks, KS_ARCH_ARM, KS_MODE_THUMB
from scripts.verify_village_wrap_v608 import read, save
from dk4tool.patch.grand_race_menu_release import sha

ADDRESS, END = 0x0200DAF0, 0x0200DB5C
ROOT = Path('work/analysis/duel_cache_front_v1142')


def assemble(size):
    assembly = f'''push {{r4-r6,lr}}
mov r4,r0
mov r5,r1
ldr r2,[r0,#108]
ldr r3,parent
cmp r2,r3
bne original
adds r0,#148
ldr r2,[r0]
ldr r3,table
subs r2,r2,r3
beq selected
cmp r2,#32
beq selected
movs r3,#208
lsls r3,r3,#1
cmp r2,r3
bne original
selected:
ldr r0,carrier
blx 0x0205528c
ldr r6,cache
mov r0,r6
subs r0,#1
ldr r1,length
blx 0x020e4430
mov r0,r6
subs r0,#1
ldr r1,length
blx 0x020e447c
mov r0,r4
mov r1,r5
blx r6
pop {{r4-r6,pc}}
original:
mov r0,r4
mov r1,r5
blx 0x020d5404
pop {{r4-r6,pc}}
.align 2
parent: .word 0x0200d4bc
table: .word 0x02117340
carrier: .word 1931
cache: .word 0x0228e70d
length: .word {size}
'''
    code = bytes(Ks(KS_ARCH_ARM, KS_MODE_THUMB).asm(assembly, ADDRESS)[0])
    assert len(code) <= END - ADDRESS, len(code)
    return code, assembly


def main():
    assert not ROOT.exists()
    plan = read('work/analysis/duel_layout_native_v1141b/compiler_provenance.json')
    code, assembly = assemble(plan['binary_bytes'])
    ROOT.mkdir(parents=True)
    (ROOT / 'front_RESEARCH_ONLY.bin').write_bytes(code)
    save(ROOT / 'front_assembly_proposal.json', {'address': ADDRESS, 'owned_tail_end': END,
        'code_bytes': len(code), 'code_hex': code.hex(), 'assembly': assembly,
        'COMMON_owner': 0x0228E6DC, 'existing_single_cache_base': 0x0228E70C,
        'native_data_flush_range': 0x020E4430, 'native_instruction_invalidate_range': 0x020E447C,
        'PIC_component_bytes': plan['binary_bytes'], 'scope_tables': [0x02117340,0x02117360,0x021174E0],
        'scope_outer_return': 0x0200D4BC, 'carrier_message_ID': 1931,
        'all_cache_lifetime_PIC_relocation_prefix_ownership_and_native_tests_pending': True,
        'no_ROM_or_completion_credit': True, 'producer_sha256': sha(Path(__file__).read_bytes()), 'full_goal_complete':False})
    print(f'Cache front fits:{len(code)}/{END-ADDRESS} owned bytes;PIC/lifetime/loader/cache-op proofs remain required.')


if __name__ == '__main__':
    main()
