"""Native texture/material fixtures from all actually observed FLS texture poses.

These are isolated source-derived inputs, not gameplay or a final GPU renderer.
Each fresh object binds one observed pose through the original allocator/loader.
"""

import argparse
import json
import struct
from pathlib import Path

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
from scripts.research_fls_stream_v310 import SNAPSHOT, case
from scripts.research_fls_submission_v323 import IO, ROM, ROOT, draw

POSE_PROOF = Path('work/analysis/fls_frames_v312/all_files_proof.json')


def read(path):
    return json.loads(Path(path).read_text(encoding='utf-8'))


def fixture(record):
    def inspect(u, obj):
        u.mem_map(IO, 0x1000)
        u.mem_write(obj + 0x1A94, bytes.fromhex(record['global_camera_colour_alpha_and_canvas_hex']))
        u.mem_write(obj + 0x10, struct.pack('<I', record['depth_spacing']))
        u.mem_write(obj + 0x1A0A, struct.pack('<h', record['native_frame_counter']))
        writer = struct.unpack('<I', u.mem_read(obj + 0x1A04, 4))[0]
        slot = record['pose']['slot']
        pose_address = writer + slot * 0x60
        raw = bytes.fromhex(record['pose']['state_hex'])
        allocation = struct.unpack('<I', u.mem_read(obj + 4, 4))[0]
        prefix_size = struct.unpack('<I', u.mem_read(allocation + 12, 4))[0]
        header = struct.unpack_from('<I', raw, 4)[0]
        assert allocation <= header < allocation + prefix_size
        assert list(struct.unpack('<2h', u.mem_read(header, 4))) == record['pose']['native_texture_bounds']
        u.mem_write(pose_address, raw)
        saved = {r: u.reg_read(r) for r in SAVED}
        u.reg_write(UC_ARM_REG_SP, STACK)
        u.reg_write(UC_ARM_REG_LR, STOP)
        u.reg_write(UC_ARM_REG_R0, obj)
        u.reg_write(UC_ARM_REG_R1, record['pose']['texture_input'] & 0xFFFFFFFF)
        u.emu_start(BASE + 0x100390, STOP, count=10000)
        assert u.reg_read(UC_ARM_REG_PC) == STOP
        assert u.reg_read(UC_ARM_REG_R0) == record['pose']['native_texture_index']
        u.reg_write(UC_ARM_REG_SP, STACK)
        u.reg_write(UC_ARM_REG_LR, STOP)
        u.reg_write(UC_ARM_REG_R0, obj)
        u.reg_write(UC_ARM_REG_R1, pose_address)
        u.emu_start(BASE + 0xFFD14, STOP, count=100000)
        assert u.reg_read(UC_ARM_REG_PC) == STOP and u.reg_read(UC_ARM_REG_SP) == STACK
        assert all(u.reg_read(r) == v for r, v in saved.items())
        bound = bytes(u.mem_read(pose_address, 0x60))
        buffer = struct.unpack('<h', u.mem_read(obj + 0x1A08, 2))[0] ^ 1
        previous = obj + 0x204 + buffer * 0xC00 + slot * 0x60
        u.mem_write(previous, bound)
        result = draw(u, obj, slot)
        assert 'error' not in result, result
        parameters = [row['value'] for row in result['writes'] if row['address'] == IO + 0x4A8]
        assert len(parameters) == 1 and (parameters[0] >> 26) & 7
        palettes = [row['value'] for row in result['writes'] if row['address'] == IO + 0x4AC]
        cache = []
        for index in range(32):
            owner, texture, palette = [struct.unpack('<I', u.mem_read(obj + offset + index * 4, 4))[0]
                                       for offset in (0x34, 0xB4, 0x134)]
            if owner:
                cache.append({'owner_relative_to_prefix': owner - allocation,
                              'texture_key': texture, 'palette_key': palette})
        assert len(cache) == 1 and cache[0]['texture_key'] != 0
        return {'texture_index': record['pose']['native_texture_index'],
                'observed_pose_tick': record['tick'], 'slot': slot,
                'native_dimensions': record['pose']['native_texture_bounds'],
                'actual_native_texture_parameter': parameters[0], 'actual_native_palette_parameters': palettes,
                'native_bound_pose_suffix_hex': bound[0x48:].hex(), 'native_allocated_cache': cache,
                'native_writes': result['writes'],
                'all_native_loader_draw_return_register_and_stack_checks_pass': True,
                'native_draw_code_executed_addresses': result['executed_addresses'],
                'contextual_masks_projection_upload_and_final_GPU_not_certified': True}
    return inspect


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--all', action='store_true')
    args = parser.parse_args()
    ROOT.mkdir(parents=True, exist_ok=True)
    poses = read(POSE_PROOF)
    assert poses['candidate_sha256'] == sha(Path(poses['candidate']).read_bytes())
    current, clean = NdsImage.open(ROM), NdsImage.open('work/clean.nds')
    arm, ram = current.read_file('/__arm9__.bin'), SNAPSHOT.read_bytes()
    previous = NdsImage.open(poses['candidate']).read_file('/__arm9__.bin')
    assert arm[0xFD178:0x10044C] == previous[0xFD178:0x10044C]
    selected = []
    for file in poses['cases']:
        seen = set()
        for state in file['frames']['states']:
            global_bytes = bytes.fromhex(state['global_camera_colour_alpha_and_canvas_hex'])
            for pose in state['slots']:
                index = pose['native_texture_index']
                raw = bytes.fromhex(pose['state_hex'])
                alpha = struct.unpack_from('<h', raw, 0x2C)[0]
                bias = struct.unpack_from('<h', raw, 0x2E)[0]
                global_bias = struct.unpack_from('<h', global_bytes, 0x1E)[0]
                combined = global_bias + (bias >> 8) + ((global_bytes[0x23] * alpha) >> 8)
                if pose['draw_kind'] or pose['native_texture_bounds'] is None or index in seen or combined <= 0:
                    continue
                seen.add(index)
                selected.append({'path': file['path'], 'tick': state['tick'],
                                 'native_frame_counter': state['native_frame_counter'],
                                 'global_camera_colour_alpha_and_canvas_hex': state['global_camera_colour_alpha_and_canvas_hex'],
                                 'depth_spacing': state['depth_spacing'], 'pose': pose})
    assert len(selected) == 260
    if not args.all:
        selected = [r for r in selected if r['path'] == '/FLS/M22.fls'][:1]
    results = []
    for record in selected:
        versions = []
        for rom in (current, clean):
            native = case(rom, arm, ram, record['path'], inspect=fixture(record))
            inspected = native.get('additional_scoped_inspection')
            assert inspected is not None, native
            versions.append(inspected)
        assert versions[0] == versions[1]
        # Keep the source-derived contract in the evidence, but avoid repeating
        # hundreds of native instruction addresses in every compact result.
        native = versions[0]
        addresses = native.pop('native_draw_code_executed_addresses')
        native['native_draw_executed_address_count'] = len(addresses)
        native['native_draw_executed_addresses_sha256'] = sha(struct.pack(f'<{len(addresses)}I', *addresses))
        results.append({'path': record['path'], **native,
                        'clean_and_current_bindings_and_native_commands_exact': True})
        (ROOT / 'binding_progress.json').write_text(json.dumps({'completed': len(results), 'total': len(selected),
                                                               'path': record['path'], 'texture': native['texture_index']}) + '\n', encoding='utf-8')
    proof = {'candidate': str(ROM), 'candidate_sha256': sha(ROM.read_bytes()),
             'source_poses': str(POSE_PROOF), 'source_poses_sha256': sha(POSE_PROOF.read_bytes()),
             'captured_global_state': str(SNAPSHOT), 'captured_global_state_sha256': sha(ram),
             'cases': results, 'independent_fresh_constructor_parser_loader_and_allocator_per_pose': True,
             'original_engine_source_bytes_unchanged': True,
             'texture_and_palette_jobs_queued_but_not_uploaded': True,
             'no_contextual_masks_or_final_GPU_claim': True,
             'raw_root_has_no_observed_pose_and_remains_open': True,
             'ROM_modified': False, 'goal_complete': False}
    (ROOT / ('all_bindings_proof.json' if args.all else 'sample_binding_proof.json')).write_text(
        json.dumps(proof, indent=2) + '\n', encoding='utf-8')
    print(json.dumps({'native_bindings': len(results), 'clean_and_current_commands_exact': True,
                      'final_GPU_verified': False, 'goal_complete': False}))


if __name__ == '__main__':
    main()
