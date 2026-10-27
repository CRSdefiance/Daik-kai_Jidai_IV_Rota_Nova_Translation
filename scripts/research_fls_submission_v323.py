"""Run original FLS draw through native hardware writes, without a GPU model."""

import argparse
import json
import struct
from pathlib import Path

from unicorn import UC_HOOK_CODE, UC_HOOK_MEM_WRITE, UcError
from unicorn.arm_const import (
    UC_ARM_REG_LR,
    UC_ARM_REG_PC,
    UC_ARM_REG_R0,
    UC_ARM_REG_R1,
    UC_ARM_REG_SP,
)

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.probe_button_prompt_native import BASE, SAVED, STACK, STOP
from scripts.research_fls_stream_v310 import case

ROOT = Path('work/analysis/fls_submission_v323')
ROM = Path('out/all_routes_combined_v322_candidate.nds')
SNAPSHOT = Path('work/emulation_v193/sea_inspect_v322/final_arm9_ram.bin')
IO = 0x04000000


def draw(u, obj, slot):
    context = u.context_save()
    stack = bytes(u.mem_read(STACK - 4096, 4128))
    state = bytes(u.mem_read(obj, 0x1B18))
    io = bytes(u.mem_read(IO, 0x1000))
    writes, executed = [], set()
    saved = {r: u.reg_read(r) for r in SAVED}

    def observe(uc, address, size, _):
        executed.add(address)
        if address == STOP:
            uc.emu_stop()

    def write(uc, access, address, size, value, _):
        writes.append({'address': address, 'size': size, 'value': value,
                       'PC': uc.reg_read(UC_ARM_REG_PC)})

    code_hook = u.hook_add(UC_HOOK_CODE, observe)
    write_hook = u.hook_add(UC_HOOK_MEM_WRITE, write, begin=IO, end=IO + 0xFFF)
    try:
        u.reg_write(UC_ARM_REG_SP, STACK)
        u.reg_write(UC_ARM_REG_LR, STOP)
        u.reg_write(UC_ARM_REG_R0, obj)
        u.reg_write(UC_ARM_REG_R1, slot)
        u.emu_start(BASE + 0xFEB28, STOP, count=200000)
        assert u.reg_read(UC_ARM_REG_PC) == STOP and u.reg_read(UC_ARM_REG_SP) == STACK
        assert all(u.reg_read(r) == v for r, v in saved.items())
        assert bytes(u.mem_read(STACK - 4096, 32)) == stack[:32]
        assert bytes(u.mem_read(STACK, 32)) == stack[-32:]
        return {'writes': writes, 'native_draw_return_and_saved_registers_preserved': True,
                'executed_addresses': sorted(executed),
                'clip_count': struct.unpack_from('<I', state, 0x1A90)[0],
                'clipping_selectors_hex': state[0x1A10:0x1A94].hex(),
                'global_camera_colour_alpha_canvas_hex': state[0x1A94:0x1AB8].hex()}
    except (UcError, AssertionError) as error:
        return {'error': str(error), 'PC': u.reg_read(UC_ARM_REG_PC), 'writes': writes,
                'executed_addresses': sorted(executed)}
    finally:
        u.hook_del(code_hook)
        u.hook_del(write_hook)
        u.mem_write(STACK - 4096, stack)
        u.mem_write(obj, state)
        u.mem_write(IO, io)
        u.context_restore(context)


def inspect(u, obj):
    u.mem_map(IO, 0x1000)
    draws = []
    for tick in range(1, 301):
        u.reg_write(UC_ARM_REG_SP, STACK)
        u.reg_write(UC_ARM_REG_LR, STOP)
        u.reg_write(UC_ARM_REG_R0, obj)
        u.emu_start(BASE + 0xFD478, STOP, count=500000)
        assert u.reg_read(UC_ARM_REG_PC) == STOP and u.reg_read(UC_ARM_REG_SP) == STACK
        buffer = struct.unpack('<h', u.mem_read(obj + 0x1A08, 2))[0] ^ 1
        pose = obj + 0x204 + buffer * 0xC00
        for slot in range(1, 32):
            raw = bytes(u.mem_read(pose + slot * 0x60, 0x60))
            if struct.unpack_from('<h', raw)[0] and struct.unpack_from('<h', raw, 0x34)[0] == 0:
                result = draw(u, obj, slot)
                if result.get('writes') or result.get('error'):
                    draws.append({'tick': tick, 'slot': slot, 'texture_input': struct.unpack_from('<h', raw, 2)[0],
                                  'pose_hex': raw.hex(),
                                  'native_texture_cache_keys_hex': bytes(u.mem_read(obj + 0xB4, 256)).hex(),
                                  **result})
        if draws:
            break
    return {'sample_draws': draws, 'writes_observed_not_GPU_execution': True}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--path', default='/FLS/M22.fls')
    args = parser.parse_args()
    ROOT.mkdir(parents=True, exist_ok=True)
    rom = NdsImage.open(ROM)
    arm = rom.read_file('/__arm9__.bin')
    capture = json.loads(SNAPSHOT.with_name('capture_report.json').read_text(encoding='utf-8'))
    assert capture['ROM_sha256'] == sha(ROM.read_bytes())
    assert capture['read_only_RAM_snapshot']['sha256'] == sha(SNAPSHOT.read_bytes())
    assert capture['cold_boot'] and not capture['savestate_loaded']
    older_arm = NdsImage.open('out/all_routes_combined_v309_candidate.nds').read_file('/__arm9__.bin')
    assert arm[0xFEB28:0xFFA04] == older_arm[0xFEB28:0xFFA04]
    result = case(rom, arm, SNAPSHOT.read_bytes(), args.path, inspect=inspect)
    proof = {'candidate': str(ROM), 'candidate_sha256': sha(ROM.read_bytes()),
             'original_draw_code_unchanged': True, 'case': result,
             'snapshot': str(SNAPSHOT), 'snapshot_sha256': sha(SNAPSHOT.read_bytes()),
             'native_parent_update_includes_original_texture_loader_and_allocators': True,
             'mapped_hardware_register_sink_without_GPU_emulation': [IO, 0x1000],
             'ROM_modified': False, 'goal_complete': False}
    (ROOT / 'exploration.json').write_text(json.dumps(proof, indent=2) + '\n', encoding='utf-8')
    extra = result.get('additional_scoped_inspection', {})
    print(json.dumps({'draws': len(extra.get('sample_draws', [])),
                      'errors': [r.get('error') for r in extra.get('sample_draws', [])],
                      'writes': [len(r.get('writes', [])) for r in extra.get('sample_draws', [])]}, indent=2))


if __name__ == '__main__':
    main()
