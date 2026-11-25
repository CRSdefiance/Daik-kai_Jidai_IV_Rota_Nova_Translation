"""Replay original captain call fragments through real COMMON lookup/preparation."""

import struct
from pathlib import Path

from ndspy.code import MainCodeFile
from unicorn import UC_HOOK_CODE
from unicorn.arm_const import (
    UC_ARM_REG_PC,
    UC_ARM_REG_R0,
    UC_ARM_REG_R1,
    UC_ARM_REG_R11,
    UC_ARM_REG_SP,
)

from dk4tool.patch.captain_prompt_wrap import ADDRESS, SIZE, transform
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.probe_button_prompt_native import BASE, STACK, machine
from scripts.verify_village_wrap_v608 import read, save

ROOT = Path('work/analysis/captain_prompt_wrap_v651')
RUN = Path('E:/Rota Nova translations/Generated/work/emulation_v193/fleet_capacity_v650_actual')


def main():
    arm = NdsImage.open('out/all_routes_combined_v640_candidate.nds').read_file('/__arm9__.bin')
    target, _ = transform(arm)
    clean = NdsImage.open('work/clean.nds').read_file('/__arm9__.bin')
    rows = []
    for number, frame, start in ((269, 32600, 0x0205A94C), (272, 35800, 0x0205A9A8)):
        assert arm[start - BASE:start - BASE + 8] == clean[start - BASE:start - BASE + 8]
        if number == 269:
            assert struct.unpack_from('<I', arm, 0x5AA60)[0] == 269
        else:
            # This FP value is established by the exact original MOV at0205A944.
            assert arm[0x5A944:0x5A948] == clean[0x5A944:0x5A948] == bytes.fromhex('11beA0E3')
        raw = (RUN / f'frame_{frame:06d}_arm9_ram.bin').read_bytes()
        state = read(RUN / f'native_state_{frame:06d}/native_state.json')
        region = state['regions']['ITCM']
        itcm = Path(region['path']).read_bytes()
        assert sha(itcm) == region['sha256'] and len(itcm) == 32768
        cases = []
        for label, data in (('current_V640', arm), ('repaired_V651', target)):
            u = machine(data)
            u.mem_write(BASE, raw)
            u.mem_write(0x01FF0000, itcm)
            u.mem_write(0x01FF8000, itcm)
            payload = bytes(MainCodeFile(data, BASE).sections[4].data)
            at = ADDRESS - 0x01FFC000
            u.mem_write(ADDRESS, payload[at:at + SIZE])
            u.reg_write(UC_ARM_REG_SP, STACK)
            u.reg_write(UC_ARM_REG_R11, 272)
            observed, outputs = [], []

            def hook(cpu, address, size, unused, observed=observed, outputs=outputs):
                if address == 0x01FFC900:
                    sp = cpu.reg_read(UC_ARM_REG_SP)
                    observed.append({'parent': struct.unpack('<I', cpu.mem_read(sp + 0xC4, 4))[0],
                                     'native_ID': struct.unpack('<I', cpu.mem_read(sp + 0xD0, 4))[0]})
                if address == 0x02053914:
                    pointer = cpu.reg_read(UC_ARM_REG_R1)
                    outputs.append({'destination': cpu.reg_read(UC_ARM_REG_R0),
                                    'selected_paragraph': bytes(cpu.mem_read(pointer, 256)).split(b'\0')[0].decode('ascii')})

            h = u.hook_add(UC_HOOK_CODE, hook)
            try:
                u.emu_start(start, 0x0205479C, count=300000)
            finally:
                u.hook_del(h)
            assert u.reg_read(UC_ARM_REG_PC) == 0x0205479C
            assert observed == [{'parent': 0x020546E8, 'native_ID': number}]
            assert len(outputs) == 1
            output = bytes(u.mem_read(outputs[0]['destination'], 256)).split(b'\0')[0].decode('ascii')
            assert ' '.join(output.split()) == outputs[0]['selected_paragraph']
            cases.append({'label': label, 'actual_original_modal_call_frame': observed[0],
                          'original_COMMON_lookup_selected_paragraph': outputs[0]['selected_paragraph'],
                          'complete_prepared_output': output,
                          'native_call_to_lookup_expansion_and_dispatch_connected': True,
                          'stop_before_UI_widget_construction_not_full_function_replay': True})
        assert '\n' not in cases[0]['complete_prepared_output'] and '\n' in cases[1]['complete_prepared_output']
        rows.append({'native_ID': number, 'original_call_fragment': start, 'captured_frame': frame,
                     'captured_RAM_sha256': sha(raw), 'cases': cases})
    save(ROOT / 'connected_caller_proof.json', {'cases': rows,
         'all_original_lookup_and_macro_expansion_executed_no_selected_text_bridge': True,
         'original_FP_constant_is_declared_fragment_input_for272': True,
         'actual_complete_UI_presentation_pending': True, 'script_sha256': sha(Path(__file__).read_bytes()),
         'full_goal_complete': False})
    print('Both original captain call fragments establish parent546E8 and native IDs269/272;complete repaired paragraphs wrap.')


if __name__ == '__main__':
    main()
