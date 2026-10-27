"""Measure the existing balanced helper at24 columns before selecting a runtime."""
from pathlib import Path
from keystone import Ks, KS_ARCH_ARM, KS_MODE_ARM, KS_MODE_THUMB
from capstone import Cs, CS_ARCH_ARM, CS_MODE_THUMB

from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_personal_gameplay_v841 import get_machine
from scripts.verify_village_wrap_v608 import read, save

BASE = 0x02000000
ROOT = Path('work/analysis/duel_existing_balancer_v1126')
ROM = Path('out/all_routes_combined_v1105_candidate.nds')
TEMP, INPUT, OUTPUT = 0x02470000, 0x02468000, 0x02469000
BALANCE = 0x02147AE4


def main():
    assert not ROOT.exists()
    catalog = read('work/analysis/duel_scope_names_v1117b/source_name_layout_catalogue.json')
    rom = NdsImage.open(ROM)
    arm = rom.read_file('/__arm9__.bin')
    assert sha(ROM.read_bytes()) == catalog['candidate_sha256']
    prefix = list(Cs(CS_ARCH_ARM, CS_MODE_THUMB).disasm(arm[BALANCE - BASE:BALANCE - BASE + 16], BALANCE))
    assert [instruction.mnemonic for instruction in prefix] == ['push', 'sub', 'mov', 'mov', 'movs', 'lsls', 'adds', 'str']
    head = bytes(Ks(KS_ARCH_ARM, KS_MODE_ARM).asm('add ip,pc,#1;bx ip', TEMP)[0])
    assembly = f'''push {{r4-r7,lr}}
sub sp,#8
mov r4,r0
mov r5,r1
movs r0,#24
lsls r0,r0,#8
adds r0,#24
str r0,[sp,#0]
ldr r3,resume
bx r3
.align 2
resume: .word {BALANCE+17}
'''
    body = bytes(Ks(KS_ARCH_ARM, KS_MODE_THUMB).asm(assembly, TEMP + 8)[0])
    raw = Path(catalog['snapshot']).read_bytes()
    assert sha(raw) == catalog['snapshot_sha256']
    cpu, get = get_machine(arm, raw)
    cpu.mem_write(TEMP, head + body)
    cases, findings = [], []
    for item in catalog['all4160_complete_word_layouts']:
        text = bytes.fromhex(item['paragraph_hex'])
        cpu.mem_write(INPUT, text + b'\0')
        cpu.mem_write(OUTPUT, bytes(256))
        count = get(TEMP - BASE, INPUT, OUTPUT)
        output = bytes(cpu.mem_read(OUTPUT, 256)).split(b'\0')[0]
        assert count == len(output) and count > 0
        assert b' '.join(output.split()) == text
        lines = [line.strip() for line in output.split(b'\n')]
        widths = [len(line) for line in lines]
        issues = []
        if len(lines) > 3:
            issues.append('more-than-three-visible-rows')
        if max(widths) > 24:
            issues.append('exceeds-visible24-columns')
        if len(lines) > 1 and len(lines[-1].split()) == 1:
            issues.append('single-word-final-row')
        case = {'actor_slot': item['actor_slot'], 'message_ID': item['message_ID'],
                'source_hex': text.hex(), 'native_generated_hex': output.hex(),
                'complete_source_words_retained': True, 'line_widths': widths,
                'lines': [line.decode('cp932') for line in lines], 'findings': issues}
        cases.append(case)
        if issues:
            findings.append(case)
    assert len(cases) == 4160
    ROOT.mkdir(parents=True)
    save(ROOT / 'existing_balancer24_matrix.json', {
        'candidate': str(ROM), 'candidate_sha256': catalog['candidate_sha256'],
        'original_helper_address': BALANCE, 'original_helper_prefix_hex': arm[BALANCE - BASE:BALANCE - BASE + 16].hex(),
        'CPU_only_profile_initialization_trampoline_hex': (head + body).hex(),
        'all4160_original_helper_stack_and_callee_saved_ABI_and_complete_words_pass': True,
        'cases': cases, 'unacceptable_for_duel_without_additional_policy': findings,
        'no_ROM_runtime_storage_or_completion_credit_change': True,
        'producer_sha256': sha(Path(__file__).read_bytes()), 'full_goal_complete': False})
    print(f'Existing helper24-column matrix:{len(cases)} complete-word/ABI cases;{len(findings)} row/bounds/orphan findings. Not a runtime approval.')


if __name__ == '__main__':
    main()
