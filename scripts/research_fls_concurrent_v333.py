"""Concurrent native allocations from observed poses; GPU uploads stay deferred."""

import argparse
import json
import struct
from itertools import pairwise
from pathlib import Path

from unicorn import UC_HOOK_CODE
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
from scripts.research_fls_submission_v323 import IO, draw

ROOT = Path('work/analysis/fls_concurrent_v333')
ROM = Path('out/all_routes_combined_v326_candidate.nds')
POSES = Path('work/analysis/fls_frames_v312/all_files_proof.json')


def read(path):
    return json.loads(Path(path).read_text(encoding='utf-8'))


def eligible(state):
    global_bytes = bytes.fromhex(state['global_camera_colour_alpha_and_canvas_hex'])
    values = []
    for pose in state['slots']:
        raw = bytes.fromhex(pose['state_hex'])
        alpha, bias = struct.unpack_from('<2h', raw, 0x2C)
        combined = struct.unpack_from('<h', global_bytes, 0x1E)[0] + (bias >> 8) + ((global_bytes[0x23] * alpha) >> 8)
        if alpha >= 2 and combined > 0 and pose['draw_kind'] == 0 and pose['native_texture_bounds'] is not None:
            values.append(pose)
    return values


def fixture(state):
    def inspect(u, obj):
        u.mem_map(IO, 0x1000)
        u.mem_write(obj + 0x1A94, bytes.fromhex(state['global_camera_colour_alpha_and_canvas_hex']))
        u.mem_write(obj + 0x10, struct.pack('<I', state['depth_spacing']))
        u.mem_write(obj + 0x1A0A, struct.pack('<h', state['native_frame_counter']))
        writer = struct.unpack('<I', u.mem_read(obj + 0x1A04, 4))[0]
        allocation = struct.unpack('<I', u.mem_read(obj + 4, 4))[0]
        prefix_size = struct.unpack('<I', u.mem_read(allocation + 12, 4))[0]
        selected = eligible(state)
        queued = []

        def observe(uc, address, size, _):
            if address in (BASE + 0xFFB7C, BASE + 0xFFC48):
                queued.append({'kind': 'palette' if address == BASE + 0xFFB7C else 'pixels',
                               'destination_offset': uc.reg_read(UC_ARM_REG_R1)})

        hook = u.hook_add(UC_HOOK_CODE, observe)

        def bind(pose):
            pointer = writer + pose['slot'] * 0x60
            saved = {r: u.reg_read(r) for r in SAVED}
            u.reg_write(UC_ARM_REG_SP, STACK)
            u.reg_write(UC_ARM_REG_LR, STOP)
            u.reg_write(UC_ARM_REG_R0, obj)
            u.reg_write(UC_ARM_REG_R1, pointer)
            u.emu_start(BASE + 0xFFD14, STOP, count=100000)
            assert u.reg_read(UC_ARM_REG_PC) == STOP and u.reg_read(UC_ARM_REG_SP) == STACK
            assert all(u.reg_read(r) == v for r, v in saved.items())

        def cache():
            result = []
            for index in range(32):
                owner, tex, pal = [struct.unpack('<I', u.mem_read(obj + field + index * 4, 4))[0]
                                   for field in (0x34, 0xB4, 0x134)]
                if owner:
                    assert tex
                    result.append({'cache_slot': index, 'owner_relative_to_prefix': owner - allocation,
                                   'texture_key': tex, 'palette_key': pal,
                                   'texture_interval': [(tex & 0xFFFF) * 8, (tex & 0xFFFF) * 8 + ((tex >> 16) & 0x7FFF) * 16],
                                   'palette_interval': [(pal & 0xFFFF) * 8, (pal & 0xFFFF) * 8 + (pal >> 16) * 8]})
            return result

        try:
            for pose in selected:
                raw = bytes.fromhex(pose['state_hex'])
                header = struct.unpack_from('<I', raw, 4)[0]
                assert allocation <= header < allocation + prefix_size
                assert list(struct.unpack('<2h', u.mem_read(header, 4))) == pose['native_texture_bounds']
                u.mem_write(writer + pose['slot'] * 0x60, raw)
            for pose in selected:
                bind(pose)
            allocated = cache()
            assert len(allocated) == len({p['native_texture_index'] for p in selected})
            for kind in ('texture_interval', 'palette_interval'):
                intervals = sorted(r[kind] for r in allocated if r[kind][1] > r[kind][0])
                assert all(a[1] <= b[0] for a, b in pairwise(intervals))
            first_queued = list(queued)
            for pose in selected:
                bind(pose)
            assert cache() == allocated and queued == first_queued
            materials = []
            buffer = struct.unpack('<h', u.mem_read(obj + 0x1A08, 2))[0] ^ 1
            for pose in selected:
                bound = bytes(u.mem_read(writer + pose['slot'] * 0x60, 0x60))
                u.mem_write(obj + 0x204 + buffer * 0xC00 + pose['slot'] * 0x60, bound)
                result = draw(u, obj, pose['slot'])
                assert 'error' not in result
                params = [w['value'] for w in result['writes'] if w['address'] == IO + 0x4A8]
                assert len(params) == 1 and (params[0] >> 26) & 7
                materials.append({'slot': pose['slot'], 'texture': pose['native_texture_index'],
                                  'material_parameter': params[0], 'native_commands': result['writes']})
            return {'observed_tick': state['tick'], 'visible_slots': len(selected),
                    'native_allocations': allocated, 'queued_upload_requests': first_queued,
                    'repeat_binding_reuses_keys_without_additional_jobs': True,
                    'live_texture_palette_allocations_do_not_overlap': True,
                    'native_materials_and_commands': materials,
                    'uploads_lifetime_free_recycling_GPU_aliases_and_pixels_not_verified': True}
        finally:
            u.hook_del(hook)
    return inspect


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--all', action='store_true')
    args = parser.parse_args()
    ROOT.mkdir(parents=True, exist_ok=True)
    poses = read(POSES)
    current, clean, older = NdsImage.open(ROM), NdsImage.open('work/clean.nds'), NdsImage.open(poses['candidate'])
    arm, ram = current.read_file('/__arm9__.bin'), SNAPSHOT.read_bytes()
    rows = []
    for movie in poses['cases']:
        assert current.read_file(movie['path']) == older.read_file(movie['path'])
        states = [max(movie['frames']['states'], key=lambda s: len(eligible(s)))]
        if args.all:
            unique = {}
            for state in movie['frames']['states']:
                key = tuple((p['slot'], p['native_texture_index']) for p in eligible(state))
                if key and key not in unique:
                    unique[key] = state
            states = list(unique.values())
        if not states or not eligible(states[0]):
            rows.append({'path': movie['path'], 'no_visible_texture_pose_in_recorded_path': True,
                         'raw_root_usage_not_inferred': True})
            continue
        for state in states:
            pair = [case(rom, arm, ram, movie['path'], inspect=fixture(state)) for rom in (current, clean)]
            inspected = [r.get('additional_scoped_inspection') for r in pair]
            assert all(inspected), pair
            assert inspected[0] == inspected[1]
            rows.append({'path': movie['path'], 'bindings': inspected[0], 'clean_current_concurrent_state_exact': True})
            (ROOT / 'progress.json').write_text(json.dumps({'completed': sum('bindings' in r for r in rows),
                                                           'path': movie['path']}) + '\n', encoding='utf-8')
    proof = {'candidate': str(ROM), 'candidate_sha256': sha(ROM.read_bytes()),
             'source_observed_poses': str(POSES), 'source_pose_proof_sha256': sha(POSES.read_bytes()),
             'cases': rows, 'captured_globals_and_max_visible_observed_pose_are_contracts': True,
             'original_native_allocators_and_loader_execute': True,
             'ROM_modified': False, 'full_goal_complete': False}
    (ROOT / ('all_combinations_proof.json' if args.all else 'proof.json')).write_text(
        json.dumps(proof, indent=2) + '\n', encoding='utf-8')
    print(json.dumps({'files_with_visible_cases': sum('bindings' in r for r in rows),
                      'maximum_visible_slots': max(r['bindings']['visible_slots'] for r in rows if 'bindings' in r),
                      'current_clean_exact': True, 'GPU_pixels_verified': False}))


if __name__ == '__main__':
    main()
