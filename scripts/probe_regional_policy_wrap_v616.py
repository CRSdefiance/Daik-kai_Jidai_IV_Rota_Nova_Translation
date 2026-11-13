"""Exercise the real macro/wrap dispatcher for every native ID and parent guards."""

import struct
from pathlib import Path

from ndspy.code import MainCodeFile
from unicorn import UC_HOOK_CODE
from unicorn.arm_const import (
    UC_ARM_REG_LR,
    UC_ARM_REG_PC,
    UC_ARM_REG_R0,
    UC_ARM_REG_R1,
    UC_ARM_REG_R2,
    UC_ARM_REG_SP,
)

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.main_pool_cache_visibility import POOL
from dk4tool.patch.regional_policy_wrap import ADDRESS, SIZE, transform
from dk4tool.rom.nds import NdsImage
from scripts.probe_button_prompt_native import BASE, STACK, STOP, machine
from scripts.verify_village_wrap_v608 import read, save

ROOT = Path('work/analysis/regional_fleet_v616')
TEXT, DEST = 0x0242D000, 0x0242E000


def run(uc, parent, message_id, text):
    raw = text.encode('ascii') + b'\0'
    uc.mem_write(TEXT, raw)
    uc.mem_write(DEST, b'\xa5' * 256)
    uc.mem_write(STACK + 0xC4, struct.pack('<I', parent))
    uc.mem_write(STACK + 0xD0, struct.pack('<I', message_id))
    for reg, value in ((UC_ARM_REG_SP, STACK), (UC_ARM_REG_LR, STOP), (UC_ARM_REG_R0, DEST),
                       (UC_ARM_REG_R1, TEXT), (UC_ARM_REG_R2, 0)):
        uc.reg_write(reg, value)
    visited = set()
    hook = uc.hook_add(UC_HOOK_CODE, lambda _, address, size, data: visited.add(address))
    try:
        uc.emu_start(ADDRESS, STOP, count=50000)
    finally:
        uc.hook_del(hook)
    assert uc.reg_read(UC_ARM_REG_PC) == STOP and uc.reg_read(UC_ARM_REG_SP) == STACK
    assert 0x02053914 in visited and bytes(uc.mem_read(TEXT, len(raw))) == raw
    output = bytes(uc.mem_read(DEST, 256)).split(b'\0')[0]
    return output, 0x01FFCA00 in visited


def main():
    source = NdsImage.open('out/all_routes_combined_v615_candidate.nds').read_file('/__arm9__.bin')
    target, transform_proof = transform(source)
    ROOT.mkdir(parents=True, exist_ok=True)
    code = MainCodeFile(source, BASE)
    incoming = []
    for section in code.sections:
        for at in range(0, len(section.data) - 3, 4):
            word = struct.unpack_from('<I', section.data, at)[0]
            address = section.ramAddress + at
            if word & 0x0E000000 != 0x0A000000:
                continue
            displacement = word & 0xFFFFFF
            if displacement & 0x800000:
                displacement -= 0x1000000
            destination = address + 8 + displacement * 4
            if ADDRESS <= destination < ADDRESS + SIZE and not ADDRESS <= address < ADDRESS + SIZE:
                incoming.append([address, destination])
    assert incoming == [[0x02054798, ADDRESS]], incoming
    old, new = machine(source), machine(target)
    for uc, data in ((old, source), (new, target)):
        uc.mem_write(POOL, bytes(MainCodeFile(data, BASE).sections[3].data[:-48]))
    text = 'These orders contain several complete words and preserve every leading and final character.'
    unchanged, changed = 0, []
    for message_id in range(3668):
        before, before_wrap = run(old, 0x020546E8, message_id, text)
        after, after_wrap = run(new, 0x020546E8, message_id, text)
        if 127 <= message_id <= 134:
            assert not before_wrap and after_wrap and after != before
            assert b' '.join(after.split()) == text.encode('ascii')
            changed.append(message_id)
        else:
            assert (after, after_wrap) == (before, before_wrap), message_id
            unchanged += 1
    controls = []
    for parent in (0x0205469C, 0x02054720, 0x02054764, 0x02054014):
        for message_id in (*range(127, 135), 321, 327):
            before, bw = run(old, parent, message_id, text)
            after, aw = run(new, parent, message_id, text)
            assert (before, bw) == (after, aw)
            controls.append({'parent': parent, 'message_id': message_id, 'unchanged': True})
    rows = []
    manuscript = read('translations/regional_policy_prompts_manuscript_v1.json')
    for row in manuscript['records']:
        plain = row['english'].removesuffix('{PAD}')
        prepared, wrapped = run(new, 0x020546E8, row['message_id'], plain)
        assert wrapped and b' '.join(prepared.split()) == plain.encode('ascii')
        assert all(len(line) <= 37 for line in prepared.split(b'\n'))
        rows.append({'message_id': row['message_id'], 'English': plain,
                     'complete_prepared_text': prepared.decode('ascii'), 'original_expander_and_existing_guarded_wrapper_execute': True})
    proof = {'transform': transform_proof, 'incoming_ARM_branch_calls': incoming,
             'all3668_native_IDs_exercised': True, 'unrelated_IDs_exact': unchanged,
             'added_exact_scope': changed, 'other_parent_negative_controls': controls,
             'all8_complete_prepared_paragraphs': rows,
             'actual_original_macro_expander_always_executed_and_inputs_unchanged': True,
             'source_arm9_sha256': sha(source), 'target_arm9_sha256': sha(target),
             'hardware_or_actual_emulator_pixel_verification': False, 'full_goal_complete': False,
             'script_sha256': sha(Path(__file__).read_bytes())}
    save(ROOT / 'native_dispatch_proof.json', proof)
    (ROOT / 'guarded_wrap_RESEARCH_ONLY_ARM9.bin').write_bytes(target)
    print('All3668 native modal IDs,40 other-parent controls and all8 complete guarded paragraphs pass; scope expands only127..134.')


if __name__ == '__main__':
    main()
