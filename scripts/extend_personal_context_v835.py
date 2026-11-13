"""Prove the normal state1 path, beyond the initial selector parameter3 probe."""

import struct

from unicorn import UC_HOOK_CODE
from unicorn.arm_const import UC_ARM_REG_LR, UC_ARM_REG_PC, UC_ARM_REG_R0

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.native_call_abi_v764 import call
from scripts.native_machine_scoped_v764 import machine
from scripts.prepare_personal_chatter_v835 import ROOT, ROM, MANUSCRIPT, BASE
from scripts.verify_village_wrap_v608 import read, save


def main():
    plan = read(ROOT / 'Rafael_context_run_plan.json')
    folder = __import__('pathlib').Path(plan['folder'])
    raw = (folder / 'frame_003200_arm9_ram.bin').read_bytes()
    arm = NdsImage.open(ROM).read_file('/__arm9__.bin')
    clean = NdsImage.open('work/clean.nds').read_file('/__arm9__.bin')
    for lo, hi in ((0x12104, 0x12920), (0x13D80, 0x13E0C), (0x15948, 0x159C4), (0x1CA10, 0x1CB84)):
        assert arm[lo:hi] == clean[lo:hi]
    cpu = machine(arm)
    cpu.mem_write(BASE, raw)
    call(cpu, 0x3F0F8, ())
    state = cpu.reg_read(UC_ARM_REG_R0)
    source_fields = list(struct.unpack('<2I', cpu.mem_read(state + 8, 8)))
    assert source_fields != [0, 1]
    assert struct.unpack_from('<I', clean, 0x128B0)[0] == 1361
    selected = []
    def hook(u, pc, size, unused):
        selected.append(u.reg_read(UC_ARM_REG_R0))
        u.reg_write(UC_ARM_REG_R0, 0x02450000)
        u.reg_write(UC_ARM_REG_PC, u.reg_read(UC_ARM_REG_LR))
    h = cpu.hook_add(UC_HOOK_CODE, hook, begin=BASE + 0x5528C, end=BASE + 0x5528C)
    cases = []
    try:
        for actor in range(25):
            for fn, args in ((0x12838, (actor,)), (0x12104, (actor, 1))):
                selected.clear()
                call(cpu, fn, args)
                assert selected == [1361 + actor] and cpu.reg_read(UC_ARM_REG_R0) == 0x02450000
                cases.append({'function': BASE + fn, 'arguments': list(args), 'selected_ID': selected[0], 'complete_native_ABI_pass': True})
    finally:
        cpu.hook_del(h)
    path = ROOT / 'normal_activity_path.json'
    save(path, {'candidate': str(ROM), 'candidate_sha256': sha(ROM.read_bytes()),
        'raw_RAM_source': str(folder / 'frame_003200_arm9_ram.bin'), 'raw_RAM_sha256': sha(raw),
        'original_global_context_fields_at8_and12': source_fields,
        'all25_original_activity_selector_and25_state1_paths': cases,
        'normal_source_chain': ['0201CB6C forwards live Deck list-state', '02013DCC calls02015948 with state and selected actor',
                                '020159B0 calls02015334', '02015478 calls02012104(actor,state)',
                                '02012284 calls02012838 for state1 when global fields are not0,1',
                                '0201288C adds original1361 base to actor0-24', '02012894 calls originalCOMMON loader0205528C'],
        'parameter3_is_only_an_additional_control_not_the_sole_normal_path': True,
        'global_context_is_not_labeled_day_night_without_further_evidence': True,
        'no_actual1365_1366_UI_activation_or_prose_completion_credit': True})
    doc = read(MANUSCRIPT)
    doc['normal_activity_context_proof'] = str(path)
    doc['normal_activity_context_proof_sha256'] = sha(path.read_bytes())
    for row in doc['records']:
        row['context'] = 'Independent actor-specific Deck Personnel comment. Original12838 selects1361+actor,also reached by original12104 state1 under the captured global context. The following storage record belongs to a different actor;not a spoken continuation. Actual new wording and UI activation remain pending.'
    save(MANUSCRIPT, doc)
    print('V835 normal path:25 native activity selections and25 native state1 calls pass;parameter3 is supplementary,not the sole reachability argument.', flush=True)


if __name__ == '__main__':
    main()
