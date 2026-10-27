"""Replay original numeric/name providers, voice lookup and the shared wrapper."""

import struct
from pathlib import Path

from ndspy.code import MainCodeFile
from unicorn import UC_HOOK_CODE
from unicorn.arm_const import (
    UC_ARM_REG_PC,
    UC_ARM_REG_R0,
    UC_ARM_REG_R4,
    UC_ARM_REG_R8,
    UC_ARM_REG_SP,
)

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.queued_portrait_wrap import ADDRESS, SIZE, transform
from dk4tool.rom.nds import NdsImage
from scripts.probe_button_prompt_native import BASE, STACK, call, machine
from scripts.verify_village_wrap_v608 import save

ROOT = Path('work/analysis/queued_portrait_wrap_v653')
CAP = Path('E:/Rota Nova translations/Generated/work/emulation_v193')


def main():
    arm = NdsImage.open('out/all_routes_combined_v651_candidate.nds').read_file('/__arm9__.bin')
    target, _ = transform(arm)
    clean = NdsImage.open('work/clean.nds').read_file('/__arm9__.bin')
    destination = struct.unpack_from('<I', arm, 0x54450)[0]
    cases = []
    for label, run, frame, start, number, table, parent, value in (
        ('cost', 'full_fleet_staffing_v652_actual', 5200, 0x02057470, 890, 0x02118380, 0x02053D24, 1180),
        ('unassigned', 'full_fleet_staffing_v652_actual', 12800, 0x0201DD20, 71, 0x02117460, 0x02053D24, 106),
        ('retreat', 'full_fleet_battle_v652_near_target', 15200, 0x020351C4, 2684, 0x02117080, 0x02053DB8, None)):
        assert arm[start - BASE:start - BASE + 28] == clean[start - BASE:start - BASE + 28]
        raw = (CAP / run / f'frame_{frame:06d}_arm9_ram.bin').read_bytes()
        outputs = []
        for tag, data in (('original_V651', arm), ('repaired_V653', target)):
            u = machine(data)
            u.mem_write(BASE, raw)
            payload = bytes(MainCodeFile(data, BASE).sections[4].data)
            at = ADDRESS - 0x01FFC000
            u.mem_write(ADDRESS, payload[at:at + SIZE])
            if label == 'retreat':
                call(u, 0xCB1A8, ())
                u.reg_write(UC_ARM_REG_R4, u.reg_read(UC_ARM_REG_R0) + 4 + 0x84)
            else:
                u.reg_write(UC_ARM_REG_R0, value)
                u.reg_write(UC_ARM_REG_R8, value)
            u.reg_write(UC_ARM_REG_SP, STACK)
            observed, selected = [], []

            def hook(cpu, address, size, unused, selected=selected, observed=observed):
                if address in (0x02053D0C, 0x02053DA0):
                    selected.append(cpu.reg_read(UC_ARM_REG_R0))
                if address == 0x01FFCF3C:
                    sp = cpu.reg_read(UC_ARM_REG_SP)
                    observed.append({'parent': struct.unpack('<I', cpu.mem_read(sp + 0x264, 4))[0],
                                     'table': struct.unpack('<I', cpu.mem_read(sp + 0x27C, 4))[0]})

            h = u.hook_add(UC_HOOK_CODE, hook)
            try:
                u.emu_start(start, 0x02054164, count=600000)
            finally:
                u.hook_del(h)
            assert u.reg_read(UC_ARM_REG_PC) == 0x02054164
            assert selected == [number] and observed == [{'parent': parent, 'table': table}]
            result = bytes(u.mem_read(destination, 256)).split(b'\0')[0]
            if tag == 'original_V651':
                assert result == raw[destination - BASE:destination - BASE + 256].split(b'\0')[0]
            outputs.append({'case': tag, 'prepared': result.decode('cp932'),
                            'selected_native_ID': selected[0], 'actual_dispatch_frame': observed[0]})
        assert b' '.join(outputs[0]['prepared'].encode('cp932').split()) == b' '.join(outputs[1]['prepared'].encode('cp932').split())
        assert '\n' not in outputs[0]['prepared'] and '\n' in outputs[1]['prepared']
        cases.append({'context': label, 'captured_frame': frame, 'original_fragment_start': start,
                      'RAM_sha256': sha(raw), 'cases': outputs,
                      'numeric_fragment_input_contract': value,
                      'actual_captured_original_prepared_text_matches_connected_replay': True,
                      'original_numeric_or_ship_name_provider_and_role_selector_and_COMMON_lookup_executed': True,
                      'stop_before_original_widget_construction_not_full_UI_replay': True})
    save(ROOT / 'connected_caller_proof.json', {
        'cases': cases, 'no_selected_text_or_role_or_table_bridge_inside_original_fragments': True,
        'cost1180_and_unassigned106_are_declared_fragment_inputs_not_complete_transaction_replays': True,
        'retreat_name_and_role_are_produced_by_original_fleet_and_ship_methods': True,
        'ITCM_uses_pinned_initialized_ROM_sections_not_a_same_frame_ITCM_capture': True,
        'script_sha256': sha(Path(__file__).read_bytes()), 'full_goal_complete': False})
    print('Three original providers/selectors/lookups reach the exact queued parents and repair all three complete paragraphs.')


if __name__ == '__main__':
    main()
