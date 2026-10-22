"""Execute original notification composition, guarded dispatch and fleet naming."""

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
from dk4tool.patch.regional_assignment_wrap import ADDRESS, HOOK, transform
from dk4tool.patch.regional_fleet_ordinal_label import FIELD
from dk4tool.patch.regional_fleet_ordinal_label import transform as ordinal_transform
from dk4tool.rom.nds import NdsImage
from scripts.probe_button_prompt_native import BASE, STACK, call, machine
from scripts.verify_village_wrap_v608 import save

ROOT = Path('work/analysis/regional_missions_v617')
TEXT, DEST = 0x0242D000, 0x0242E000
RETURN = 0x0205479C
SNAPSHOT = Path('E:/Rota Nova translations/Generated/work/emulation_v193/regional_missions_v617/frame_011800_arm9_ram.bin')


def cpu(arm, raw=None):
    u = machine(arm)
    if raw is None:
        u.mem_write(POOL, bytes(MainCodeFile(arm, BASE).sections[3].data[:-48]))
    else:
        u.mem_write(BASE, raw)
        for at in (HOOK, FIELD):
            u.mem_write(BASE + at, arm[at:at + 4])
    return u


def macro(u, parent, caller, message_id, raw):
    u.mem_write(TEXT, raw + b'\0')
    u.mem_write(DEST, b'\xa5' * 256)
    u.mem_write(STACK + 0xC4, struct.pack('<I', parent))
    u.mem_write(STACK + 0xCC, struct.pack('<I', caller))
    u.mem_write(STACK + 0xD0, struct.pack('<I', message_id))
    for reg, value in ((UC_ARM_REG_SP, STACK), (UC_ARM_REG_R0, DEST), (UC_ARM_REG_R1, TEXT), (UC_ARM_REG_R2, 0)):
        u.reg_write(reg, value)
    visited = set()
    handle = u.hook_add(UC_HOOK_CODE, lambda _, address, size, data: visited.add(address))
    try:
        u.emu_start(BASE + HOOK, RETURN, count=100000)
    finally:
        u.hook_del(handle)
    assert u.reg_read(UC_ARM_REG_PC) == RETURN and u.reg_read(UC_ARM_REG_SP) == STACK
    assert 0x02053914 in visited
    assert bytes(u.mem_read(TEXT, len(raw) + 1)) == raw + b'\0'
    output = bytes(u.mem_read(DEST, 256))
    return output, visited


def composed(arm, raw, policy, town):
    u = cpu(arm, raw)
    for reg, value in ((UC_ARM_REG_SP, STACK), (UC_ARM_REG_LR, 0x027E0000),
                       (UC_ARM_REG_R0, 57), (UC_ARM_REG_R1, policy), (UC_ARM_REG_R2, town)):
        u.reg_write(reg, value)
    visited = set()
    handle = u.hook_add(UC_HOOK_CODE, lambda _, address, size, data: visited.add(address))
    try:
        u.emu_start(0x0208AD58, RETURN, count=150000)
    finally:
        u.hook_del(handle)
    assert u.reg_read(UC_ARM_REG_PC) == RETURN and 0x02053914 in visited
    destination = struct.unpack_from('<I', arm, 0x54894)[0]
    return bytes(u.mem_read(destination, 256)).split(b'\0', 1)[0], visited


def main():
    rom = NdsImage.open('out/all_routes_combined_v616_candidate.nds')
    before = rom.read_file('/__arm9__.bin')
    intermediate, guards = transform(before)
    after, ordinal = ordinal_transform(intermediate)
    raw = SNAPSHOT.read_bytes()
    old, new = cpu(before), cpu(after)
    paragraph = b'These regional orders preserve every complete word and the leading and final letters.'
    unchanged = 0
    for message_id in range(3668):
        a, _ = macro(old, 0x020546E8, 0x0208AE38, message_id, paragraph)
        b, _ = macro(new, 0x020546E8, 0x0208AE38, message_id, paragraph)
        assert a == b, message_id
        unchanged += 1
    # Enumerate every original direct ARM caller of the direct-text dialog API.
    callers = []
    sections = MainCodeFile(before, BASE).sections
    units = [(s.ramAddress, bytes(s.data)) for s in sections]
    units.append((POOL, bytes(sections[3].data[:-48])))
    for base, data in units:
        for at in range(0, len(data) - 3, 4):
            word = struct.unpack_from('<I', data, at)[0]
            if word & 0x0F000000 != 0x0B000000:
                continue
            delta = word & 0xFFFFFF
            delta -= 0x1000000 if delta & 0x800000 else 0
            pc = base + at
            if pc + 8 + delta * 4 == 0x0205473C:
                callers.append(pc + 4)
    callers = sorted(set(callers))
    assert 0x0208AE38 in callers
    sample = b'Manuel Fleet:\nStockholm\nPatrol orders issued.'
    controls = []
    for caller in callers:
        a, _ = macro(old, 0x02054764, caller, 0, sample)
        b, _ = macro(new, 0x02054764, caller, 0, sample)
        if caller == 0x0208AE38:
            assert b.split(b'\0', 1)[0] == a.split(b'\0', 1)[0].replace(b'\n', b'\n  ')
        else:
            assert a == b, hex(caller)
            controls.append(caller)
    variants = []
    for name in (b'Manuel Fleet', b'Lil Fleet', b'Camille Fleet', b'Rafael Fleet', b'A' * 25,
                 'Ｆelix Fleet'.encode('cp932'), 'Ｉris Fleet'.encode('cp932')):
        for city in (b'Stockholm', b'Oslo', b'Lubeck', b'Rio de Janeiro'):
            for suffix in (b'Area management orders issued.', b'Patrol orders issued.', b'Docking orders issued.', b'Attack orders issued.'):
                source = name + b':\n' + city + b'\n' + suffix
                a, _ = macro(old, 0x02054764, 0x0208AE38, 0, source)
                b, visited = macro(new, 0x02054764, 0x0208AE38, 0, source)
                expected = a.split(b'\0', 1)[0].replace(b'\n', b'\n  ')
                assert b.split(b'\0', 1)[0] == expected and ADDRESS in visited
                variants.append({'name_hex': name.hex(), 'city': city.decode('ascii'), 'policy': suffix.decode('ascii'),
                                 'all_complete_original_expanded_text_and_two_LFs_preserved': True})
    rejected = []
    for malformed in (b'No newline.', b'One\nnewline.', b'Three\nnew\nline\nfields.', b'A' * 240 + b'\nTown\nOrders.',
                      b'Fleet:\nTown\nTab\tcontrol.'):
        a, _ = macro(old, 0x02054764, 0x0208AE38, 0, malformed)
        b, _ = macro(new, 0x02054764, 0x0208AE38, 0, malformed)
        assert a == b
        rejected.append({'input_hex': malformed.hex(), 'expanded_output_unchanged_no_partial_commit': True})
    notifications = []
    for policy, town in ((1, 7), (4, 7), (3, 7), (5, 5)):
        a, _ = composed(before, raw, policy, town)
        b, visited = composed(after, raw, policy, town)
        assert b == a.replace(b'\n', b'\n  ') and ADDRESS in visited
        notifications.append({'source_policy_ID': policy, 'source_town_ID': town,
                              'original_complete_composed_text': a.decode('cp932'), 'guarded_complete_text': b.decode('cp932'),
                              'original_fleet_and_city_getters_ring_allocation_concat_and_macro_expansion_execute': True})
    a, b = cpu(before, raw), cpu(after, raw)
    call(a, 0xCB1A8, ())
    table = a.reg_read(UC_ARM_REG_R0)
    ranks = []
    for fleet_index in (1, 57):
        actor = table + 4 + fleet_index * 0x84
        outputs, names = [], []
        for u in (a, b):
            call(u, 0x35258, (actor,))
            outputs.append(bytes(u.mem_read(u.reg_read(UC_ARM_REG_R0), 64)).split(b'\0', 1)[0])
            vt = struct.unpack('<I', u.mem_read(actor, 4))[0]
            fn = struct.unpack('<I', u.mem_read(vt + 8, 4))[0]
            call(u, fn - BASE, (actor,))
            names.append(bytes(u.mem_read(u.reg_read(UC_ARM_REG_R0), 64)).split(b'\0', 1)[0])
        assert outputs[0].endswith(b' Fleet') and outputs[1] == b'Fleet ' + outputs[0][:-6]
        assert names[0] == names[1]
        ranks.append({'fleet_index': fleet_index, 'before': outputs[0].decode('cp932'), 'after': outputs[1].decode('cp932'),
                      'proper_fleet_name_preserved': names[0].decode('cp932')})
    save(ROOT / 'native_guarded_assignment_proof.json', {'source_ARM9_sha256': sha(before), 'target_ARM9_sha256': sha(after),
         'guard_transform': guards, 'ordinal_transform': ordinal, 'all3668_native_ID_dispatch_outputs_exact': unchanged,
         'all_original_direct_text_callers': callers, 'unchanged_other_direct_text_callers': controls,
         'exact_active_parent_and_caller': [0x02054764, 0x0208AE38], 'complete_field_variants': variants,
         'unsafe_or_wrong_field_count_negative_controls': rejected, 'four_original_composed_notifications': notifications,
         'original_live_fleet_number_and_name_getters': ranks, 'actual_RAM_snapshot': str(SNAPSHOT), 'snapshot_sha256': sha(raw),
         'actual_emulator_display_verification_pending': True, 'full_goal_complete': False, 'script_sha256': sha(Path(__file__).read_bytes())})
    (ROOT / 'assignment_guards_RESEARCH_ONLY_ARM9.bin').write_bytes(after)
    print(f'All{unchanged} ID paths,{len(controls)} other direct callers,{len(variants)} field variants,4 original compositions and proper fleet names pass.')


if __name__ == '__main__':
    main()
