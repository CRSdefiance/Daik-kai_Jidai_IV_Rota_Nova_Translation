"""Replay the real provider fragments with the mapped English resources."""

import struct
from pathlib import Path

from unicorn import UC_HOOK_CODE, UC_HOOK_MEM_WRITE
from unicorn.arm_const import (UC_ARM_REG_PC, UC_ARM_REG_R0, UC_ARM_REG_R1,
    UC_ARM_REG_R2, UC_ARM_REG_R3, UC_ARM_REG_R4, UC_ARM_REG_R5, UC_ARM_REG_R6,
    UC_ARM_REG_R7, UC_ARM_REG_R8, UC_ARM_REG_R9, UC_ARM_REG_SP)

from dk4tool.patch import tavern_editorial_runtime as owned
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.shipyard_editorial import BANKS as OLD_BANKS
from dk4tool.rom.nds import NdsImage
from scripts.native_call_abi_v764 import call
from scripts.probe_button_prompt_native import BASE, STACK
from scripts.probe_tavern_conversations_v764 import CURRENT, loaded
from scripts.verify_village_wrap_v608 import read, save

ROOT = Path('work/analysis/tavern_storage_v764')


def main():
    arm = NdsImage.open(CURRENT).read_file('/__arm9__.bin')
    proof = read(ROOT / 'owned_storage_and_native_research.json')
    assert proof['source_ARM9_sha256'] == sha(arm)
    assert proof['module_sha256'] == sha(Path(owned.__file__).read_bytes())
    u = loaded(arm, False)
    for patch in proof['patches']:
        at = patch['address']; before, after = bytes.fromhex(patch['source_hex']), bytes.fromhex(patch['target_hex'])
        assert bytes(u.mem_read(at, len(before))) == before
        u.mem_write(at, after)
    def get(fn, args=()):
        call(u, fn, args); return u.reg_read(UC_ARM_REG_R0)
    def pointer(at): return struct.unpack('<I', u.mem_read(at, 4))[0]
    def string(at): return bytes(u.mem_read(at, 256)).split(b'\0')[0]
    officer, force_root = get(0xCB184), get(0xCB160)
    force = force_root + 4 + get(0x397D8, (force_root,)) * 0x4C
    actor = officer + 4 + get(0x7F244) * 32
    town, goods = get(0xB6618), get(0xCB124)
    context = read('work/analysis/tavern_conversations_v763/native_context.json')
    item = context['actual218_item_names'][60]['object']
    events, writes = [], []
    counts = {820: 3, 821: 3, 843: 5, 844: 3, 845: 3, 846: 1, 847: 1, 848: 1, 849: 2, 850: 2}
    def stop(cpu, pc, size, unused):
        if pc != BASE + 0x53FE4: return
        number = cpu.reg_read(UC_ARM_REG_R1)
        args = [cpu.reg_read(UC_ARM_REG_R2), cpu.reg_read(UC_ARM_REG_R3)]
        args.extend(struct.unpack('<3I', cpu.mem_read(cpu.reg_read(UC_ARM_REG_SP), 12)))
        events.append({'id': number, 'arguments_hex': [string(p).hex() for p in args[:counts[number]]]})
        cpu.emu_stop()
    def watch(cpu, kind, at, length, value, unused):
        if any(at < hi and at + length > lo for lo, hi in (*OLD_BANKS, *owned.BANKS)):
            writes.append([at, length, value]); raise AssertionError('Immutable source bank written')
    h = u.hook_add(UC_HOOK_CODE, stop); w = u.hook_add(UC_HOOK_MEM_WRITE, watch)
    def fragment(start, end):
        events.clear(); u.reg_write(UC_ARM_REG_SP, STACK)
        u.emu_start(BASE + start, BASE + end, count=10000)
        assert u.reg_read(UC_ARM_REG_PC) == BASE + 0x53FE4 and len(events) == 1
        return dict(events[0])
    cases = []
    for old in context['392_hint_provider_cases_and6_person_trend_fragments']:
        if 'supplied_internal_axis_distances' in old:
            if not old['private_English_provider']: continue
            dx, dy = old['supplied_internal_axis_distances']; xdir, ydir = old['supplied_direction_indices']
            for offset, value in ((0x10, actor), (0x18, ydir), (0x24, dx), (0x28, dy)):
                u.mem_write(STACK + offset, struct.pack('<I', value))
            u.reg_write(UC_ARM_REG_R4, item); u.reg_write(UC_ARM_REG_R9, xdir)
            event = fragment(0x58D4C, 0x58EA4)
        elif old['id'] in (820, 821):
            for reg, value in ((UC_ARM_REG_R7, actor), (UC_ARM_REG_R5, town), (UC_ARM_REG_R6, force), (UC_ARM_REG_R4, actor), (UC_ARM_REG_R8, old['id'])):
                u.reg_write(reg, value)
            event = fragment(0x59C9C, 0x59CE4)
        elif old['id'] in (849, 850):
            u.mem_write(STACK + 4, struct.pack('<I', actor))
            for reg, value in ((UC_ARM_REG_R4, town), (UC_ARM_REG_R5, goods + 4), (UC_ARM_REG_R6, old['supplied_native_trend_selector_value'])):
                u.reg_write(reg, value)
            event = fragment(0x58990, 0x589D4)
        else:
            for reg, value in ((UC_ARM_REG_R0, goods + 4), (UC_ARM_REG_R4, actor), (UC_ARM_REG_R7, old['supplied_native_trend_selector_value'])):
                u.reg_write(reg, value)
            event = fragment(0x58A70, 0x58A98)
        expected = list(old['arguments_hex'])
        if old['id'] in (820, 821):
            expected[2] = bytes.fromhex(expected[2]).lower().hex()
        assert event['id'] == old['id'] and event['arguments_hex'] == expected, (event, old)
        cases.append(event)
    assert len(cases) == 202 and not writes
    u.hook_del(h)
    # The original global coordinate formatter retains its complete output bytes.
    coordinates = []
    for old in context['actual_coordinate_formatter_arguments_for842']:
        u.mem_write(0x02450000, bytes.fromhex(old['original_position_hex']))
        actual = string(get(0x51580, (0x02450000,)))
        assert actual.hex() == old['argument_hex']
        coordinates.append({'item_ID': old['item_ID'], 'unchanged_argument_hex': actual.hex()})
    u.hook_del(w)
    save(ROOT / 'owned_provider_fragments.json', {'source_ARM9_sha256': sha(arm),
        'all196_original_qualitative_direction_boundary_cases': True,
        'all6_real_person_and_trend_provider_fragments': True, 'cases': cases,
        'all94_global_coordinate_provider_outputs_unchanged': coordinates,
        'native_writes_into_all_reviewed_banks': writes,
        'mapped_owned_resources_only_no_scratch_provider_tables': True,
        'scope': 'Original provider fragments stopped at original UI boundary; eligibility, earned events and complete gameplay remain unproven.',
        'producer_sha256': sha(Path(__file__).read_bytes()), 'module_sha256': sha(Path(owned.__file__).read_bytes())})
    print('202 original provider fragments and94 unchanged coordinate outputs pass at mapped storage addresses.', flush=True)


if __name__ == '__main__': main()
