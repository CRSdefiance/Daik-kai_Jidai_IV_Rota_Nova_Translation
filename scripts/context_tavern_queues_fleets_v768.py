"""Original queued price ABI and destination/docked fleet rumor providers.

CPU-only scratch object fixtures; no ROM, save or gameplay writes. The price
loader boundary returns the exact selected current COMMON bytes so the original
wrapper can be observed at its original core entry, before any UI execution.
"""

import struct
from pathlib import Path

from unicorn import UC_HOOK_CODE
from unicorn.arm_const import (UC_ARM_REG_LR, UC_ARM_REG_PC, UC_ARM_REG_R0,
    UC_ARM_REG_R1, UC_ARM_REG_R2, UC_ARM_REG_R3, UC_ARM_REG_R4, UC_ARM_REG_R5,
    UC_ARM_REG_R6, UC_ARM_REG_R7, UC_ARM_REG_R8, UC_ARM_REG_SP)

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from dk4tool.script.common_message_table import common_message_entries
from scripts.context_tavern_continuation_v768 import ROOT, CURRENT, RAM_REPORT
from scripts.native_call_abi_v764 import call
from scripts.native_machine_scoped_v764 import machine
from scripts.probe_button_prompt_native import BASE, STACK, STOP
from scripts.verify_market_gameplay_v753 import snapshot
from scripts.verify_village_wrap_v608 import read, save


def main():
    partial_path = ROOT / 'native_context_partial.json'
    partial = read(partial_path)
    rom = NdsImage.open(CURRENT)
    arm, common = rom.read_file('/__arm9__.bin'), rom.read_file('/COMMON/MESFILE.DK4')
    assert sha(arm) == partial['current_ARM9_sha256']
    entries = common_message_entries(common, arm, clean=False)
    raw = snapshot(read(RAM_REPORT), 3200)
    cpu = machine(arm); cpu.mem_write(BASE, raw)

    def get(fn, args=()):
        call(cpu, fn, args)
        return cpu.reg_read(UC_ARM_REG_R0)

    def ptr(address): return struct.unpack('<I', cpu.mem_read(address, 4))[0]
    def text(address): return bytes(cpu.mem_read(address, 256)).split(b'\0')[0]
    town = get(0xB6618); npc = get(0xB2CD8, (town, 13))
    fleet_root = get(0xCB1A8)
    current_fleet = fleet_root + 4 + get(0x2E58C) * 0x84
    fleet_source = bytes(cpu.mem_read(current_fleet, 0x84))
    queues, selected, core, price_entry = [], [], [], []

    def price_stop(u, pc, size, unused):
        price_entry.append({'role': u.reg_read(UC_ARM_REG_R0),
            'table': u.reg_read(UC_ARM_REG_R1),
            'price_text_pointer': u.reg_read(UC_ARM_REG_R2),
            'price_hex': text(u.reg_read(UC_ARM_REG_R2)).hex(),
            'numeric_price': u.reg_read(UC_ARM_REG_R8),
            'wrapper_entry_SP': u.reg_read(UC_ARM_REG_SP)})
        u.emu_stop()

    hook = cpu.hook_add(UC_HOOK_CODE, price_stop, begin=BASE + 0x53CB0, end=BASE + 0x53CB0)
    cpu.reg_write(UC_ARM_REG_SP, STACK); cpu.reg_write(UC_ARM_REG_LR, STOP)
    cpu.reg_write(UC_ARM_REG_R0, 0x02471000)
    cpu.emu_start(BASE + 0x58350, BASE + 0x5839C, count=10000)
    cpu.hook_del(hook)
    assert len(price_entry) == 1
    price = price_entry[0]
    assert price['role'] == 3 and price['table'] == 0x02118400
    assert text(price['price_text_pointer']).decode('cp932') == str(price['numeric_price']).translate(str.maketrans('0123456789', '０１２３４５６７８９'))

    def loader_stub(u, pc, size, unused):
        n = u.reg_read(UC_ARM_REG_R0); assert 852 <= n <= 858
        selected.append(n)
        u.mem_write(0x02472000, entries[n].text + b'\0')
        u.reg_write(UC_ARM_REG_R0, 0x02472000)
        u.reg_write(UC_ARM_REG_PC, u.reg_read(UC_ARM_REG_LR))

    def core_stop(u, pc, size, unused):
        at = u.reg_read(UC_ARM_REG_SP)
        core.append({'mode': u.reg_read(UC_ARM_REG_R0), 'actor': u.reg_read(UC_ARM_REG_R1),
            'text_hex': text(u.reg_read(UC_ARM_REG_R2)).hex(),
            'va_list': u.reg_read(UC_ARM_REG_R3), 'SP': at,
            'parent_LR': u.reg_read(UC_ARM_REG_LR),
            'saved_table': ptr(at + 20),
            'first_argument_hex': text(ptr(u.reg_read(UC_ARM_REG_R3))).hex()})
        u.emu_stop()

    hooks = [cpu.hook_add(UC_HOOK_CODE, loader_stub, begin=BASE + 0x5528C, end=BASE + 0x5528C),
             cpu.hook_add(UC_HOOK_CODE, core_stop, begin=BASE + 0x54058, end=BASE + 0x54058)]
    cpu.emu_start(BASE + 0x53CB0, BASE + 0x53D24, count=10000)
    for hook in hooks: cpu.hook_del(hook)
    assert len(core) == len(selected) == 1
    result = core[0]
    assert result['mode'] == 1 and result['parent_LR'] == BASE + 0x53D24
    assert result['SP'] == price['wrapper_entry_SP'] - 32
    assert result['saved_table'] == 0x02118400
    assert result['va_list'] == price['wrapper_entry_SP'] - 8
    assert result['first_argument_hex'] == price['price_hex']
    assert result['text_hex'] == entries[selected[0]].text.hex()
    chosen = get(0x53F4C, (result['actor'], 0x02118400))
    assert chosen == selected[0]
    queues.append({'price_provider': price, 'original_core_entry': result, 'selected_message': chosen,
        'loader_stub_scope': 'Only5528C; exact current COMMON selected text; no UI or gameplay claim'})

    events, cases = [], []
    def observe(u, pc, size, unused):
        events.append({'id': u.reg_read(UC_ARM_REG_R1),
            'organization_hex': text(u.reg_read(UC_ARM_REG_R2)).hex(),
            'town_hex': text(u.reg_read(UC_ARM_REG_R3)).hex()})
        u.emu_stop()

    hook = cpu.hook_add(UC_HOOK_CODE, observe, begin=BASE + 0x53FE4, end=BASE + 0x53FE4)
    try:
        for category in ('destination', 'docked'):
            for formal in (0, 1):
                for company in partial['real_company_names']:
                    for place in partial['real_town_names']:
                        events.clear()
                        scratch = bytearray(fleet_source)
                        scratch[0x3F if category == 'destination' else 0x3C] = place['index']
                        if category == 'docked': scratch[0x50] &= ~8
                        cpu.mem_write(0x02474000, bytes(scratch))
                        cpu.mem_write(0x02474100, struct.pack('<3I', 0, 0, formal))
                        cpu.reg_write(UC_ARM_REG_SP, STACK)
                        cpu.mem_write(STACK, struct.pack('<I', 0x02474100))
                        cpu.reg_write(UC_ARM_REG_R6, npc)
                        if category == 'destination':
                            cpu.reg_write(UC_ARM_REG_R4, 0x02474000)
                            cpu.reg_write(UC_ARM_REG_R7, company['index'])
                            lo, hi, n = 0x57DDC, 0x57E4C, 879 if formal else 880
                        else:
                            cpu.reg_write(UC_ARM_REG_R5, 0x02474000)
                            cpu.reg_write(UC_ARM_REG_R4, company['index'])
                            lo, hi, n = 0x57BA4, 0x57C18, 881 if formal else 882
                        cpu.emu_start(BASE + lo, BASE + hi, count=10000)
                        assert len(events) == 1 and cpu.reg_read(UC_ARM_REG_PC) == BASE + 0x53FE4
                        event = events[0]
                        assert event == {'id': n, 'organization_hex': company['name_hex'], 'town_hex': place['name_hex']}, event
                        cases.append({**event, 'mode': formal, 'fleet_field': hex(0x3F if category == 'destination' else 0x3C),
                            'company_index': company['index'], 'town_index': place['index']})
    finally:
        cpu.hook_del(hook)
    assert len(cases) == 7200 and {c['id'] for c in cases} == {879, 880, 881, 882}
    save(ROOT / 'native_context_complete.json', {
        'candidate': str(CURRENT), 'candidate_sha256': sha(CURRENT.read_bytes()),
        'source_ARM9_sha256': partial['source_ARM9_sha256'], 'current_ARM9_sha256': sha(arm),
        'prior_provider_proof': str(partial_path), 'prior_provider_proof_sha256': sha(partial_path.read_bytes()),
        'original_price_provider_and_queue_binding': queues,
        'original_fleet_provider_cases': cases,
        'remaining_context_gates': [],
        'synthetic_fixture_scope': 'Supplied native CPU fragments and copied fleet objects only; destination3F/dock3C and formal context8; all original save/ROM bytes unchanged',
        'producer_sha256': sha(Path(__file__).read_bytes()), 'full_goal_complete': False})
    print('Original price amount/role/table/actor/va_list binding and7200 source fleet-provider cases pass.', flush=True)


if __name__ == '__main__': main()
