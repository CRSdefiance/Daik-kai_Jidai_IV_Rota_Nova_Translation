"""Verify exact integrated preservation, patch reconstruction and actual prompts."""

import argparse
import struct
from pathlib import Path

from PIL import Image

from dk4tool.dialogue.font_audit import GameAsciiFont
from dk4tool.patch.captain_prompt_wrap import transform
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.xdelta import apply_xdelta, make_xdelta
from dk4tool.rom.nds import NdsImage
from scripts.probe_button_prompt_native import BASE, call, machine
from scripts.verify_common_alignment_native_v257 import raster
from scripts.verify_regional_ui_v616 import full_cells
from scripts.verify_village_wrap_v608 import read, save

ROOT = Path('work/analysis/captain_prompt_wrap_v651')
ROM = Path('out/all_routes_combined_v651_candidate.nds')
OLD = Path('out/all_routes_combined_v640_candidate.nds')


def static():
    old, new = NdsImage.open(OLD), NdsImage.open(ROM)
    before = {p: d for _, p, d in old.iter_files()} | dict(old.iter_components())
    after = {p: d for _, p, d in new.iter_files()} | dict(new.iter_components())
    assert before.keys() == after.keys()
    assert [p for p in before if before[p] != after[p]] == ['/__arm9__.bin']
    target, proof = transform(before['/__arm9__.bin'])
    assert target == after['/__arm9__.bin']
    manifest, parent = read(ROM.with_suffix('.manifest.json')), read(OLD.with_suffix('.manifest.json'))
    stack, pre = read('translations/release_stack.json'), read(ROOT / 'preflight.json')
    assert manifest['profile'] == pre['profile'] == 'all-routes-unified-v651'
    assert manifest['candidate_sha256'] == sha(ROM.read_bytes())
    assert manifest['release_stack_sha256'] == sha(Path('translations/release_stack.json').read_bytes())
    assert stack['accepted_layers'] == pre['accepted_layers'] and len(stack['accepted_layers']) == 114
    assert manifest['base_sha256'] == stack['canonical_baseline']['sha256'] == parent['base_sha256']
    assert sha(Path(manifest['base_rom']).read_bytes()) == manifest['base_sha256']
    assert manifest['batches'] == parent['batches'] and len(manifest['batches']) == 470
    assert manifest['required_batches'] == parent['required_batches'] and all(manifest['checks'].values())
    assert manifest['changed_paths'] == parent['changed_paths']
    assert stack['profiles']['all-routes-unified-v640'] == pre['inherited_profile']
    old_preservation = read('work/analysis/region_boundaries_v640/preservation_proof.json')
    assert old_preservation['candidate_sha256'] == sha(OLD.read_bytes())
    assert old_preservation['current921_format_palette_extent_checks'] and old_preservation['all57_embedded_block_extents_exact']
    graphics = [p for p in before if p.lower().endswith(('.pxl', '.fls'))]
    assert len(graphics) == 675 and len(old_preservation['entries']) == 921
    assert {r['path'] for r in old_preservation['entries']} == set(graphics)
    assert all(before[p] == after[p] for p in graphics)
    clean = Path('work/clean.nds')
    assert sha(clean.read_bytes()) == 'f4f07c975cc293f5b2ba469747693d3dd37f2e6dfc408cf5910adf5e83d9177d'
    patch = ROM.with_suffix('.xdelta')
    make_xdelta(clean, ROM, patch)
    rebuilt = ROOT / 'all_routes_combined_v651_PATCH_RECONSTRUCTION.nds'
    apply_xdelta(clean, patch, rebuilt)
    assert rebuilt.read_bytes() == ROM.read_bytes()
    result = {'candidate': str(ROM), 'candidate_sha256': sha(ROM.read_bytes()), 'profile': manifest['profile'],
              'manifest_sha256': sha(ROM.with_suffix('.manifest.json').read_bytes()),
              'ARM9_sha256': sha(target), 'patch_sha256': sha(patch.read_bytes()),
              'clean_sha256': sha(clean.read_bytes()), 'base': manifest['base_rom'], 'base_sha256': manifest['base_sha256'],
              'transform': proof, 'only_ARM9_differs_from_complete_V640': True,
              'all921_graphics_and_every_other_ROM_file_exact_V640': True,
              'graphics_containers': 675, 'decoded_graphics_views': 921,
              'inherited921_palette_geometry_and57_embedded_preservation_proof_sha256': sha(Path('work/analysis/region_boundaries_v640/preservation_proof.json').read_bytes()),
              'all470_batches114_accepted_layers_and_existing_profiles_retained': True,
              'exact_all_byte_clean_patch_reconstruction': True,
              'reconstructed_ROM': str(rebuilt), 'canonical_promoted': False, 'full_goal_complete': False}
    save(ROOT / 'static_release_proof.json', result)
    print('V651 static:only existing128-byte ARM9 wrapper;all graphics/files retained;exact clean patch reconstructed.')


def load_run(case, config):
    path = Path(config['output']) / 'capture_report.json'
    report = read(path)
    assert report['ROM_sha256'] == config['ROM_sha256'] and report['frames'] == config['frames']
    assert report['cold_boot'] and not report['savestate_loaded'] and not report['callback_errors']
    assert not any(v for k, v in report.items() if k.startswith('synthetic_'))
    assert report['scripted_input_schedule'] == read(config['inputs'])
    if case.startswith('fleet'):
        assert report['battery_save_preloaded']['source_sha256'] == config['donor_sha256']
    else:
        assert not report.get('battery_save_preloaded')
    shots = {}
    for shot in report['frames_captured']:
        assert sha(Path(shot['path']).read_bytes()) == shot['PNG_sha256']
        if shot['frame'] in shots:
            assert Image.open(shots[shot['frame']]['path']).tobytes() == Image.open(shot['path']).tobytes()
        shots[shot['frame']] = shot
    for region in report.get('read_only_capture_RAM_snapshots', []):
        assert region['read_only_export'] and sha(Path(region['path']).read_bytes()) == region['sha256']
    return report, shots, {'case': case, 'path': str(path), 'sha256': sha(path.read_bytes())}


def actual():
    proof = read(ROOT / 'static_release_proof.json')
    assert proof['candidate_sha256'] == sha(ROM.read_bytes())
    assert proof['patch_sha256'] == sha(ROM.with_suffix('.xdelta').read_bytes())
    configs = read(ROOT / 'run_configs.json')
    runs = {case: load_run(case, config) for case, config in configs.items()}
    comparisons = {}
    differences = []
    for prefix in ('fleet', 'newgame'):
        old, os, _ = runs[prefix + '_control']
        new, ns, _ = runs[prefix + '_candidate']
        assert old['scripted_input_schedule'] == new['scripted_input_schedule'] and old['core_options'] == new['core_options']
        assert os.keys() == ns.keys()
        exact, changed = [], []
        for frame in sorted(os):
            a, b = [Image.open(s[frame]['path']).convert('RGB') for s in (os, ns)]
            if a.tobytes() == b.tobytes():
                exact.append(frame)
            else:
                changed.append(frame)
                differences.append((frame, a, b))
        assert changed == ([32600, 34800, 35000, 35800, 36600] if prefix == 'fleet' else []), (prefix, changed)
        comparisons[prefix] = {'whole_two_screen_exact_frames': exact, 'changed_frames': changed,
                               'total_unique_frames': len(os), 'exact_compared_pixel_positions': len(exact) * 256 * 384}
    target = NdsImage.open(ROM).read_file('/__arm9__.bin')
    native = read(ROOT / 'native_dispatch_proof.json')
    assert native['transform'] == proof['transform'] and native['added_exact_scope'] == list(range(269, 273))
    assert native['unrelated_IDs_byte_exact'] == 3664
    prompts = []
    for frame, old, new in differences:
        # The three additional states visibly repeat269;their original full-line
        # masks independently establish that identity before the repaired check.
        number = 272 if frame == 35800 else 269
        row = next(r for r in native['four_complete_native_instruction_rasters'] if r['native_ID'] == number)
        text, font = row['unchanged_English'], GameAsciiFont.from_arm9(target)
        original_lines = [full_cells(old, font, text[:36], 16, 296, (0, 8, 0)),
                          full_cells(old, font, text[36:], 16, 312, (0, 8, 0))]
        report = runs['fleet_candidate'][0]
        ram_row = next(r for r in report['read_only_capture_RAM_snapshots'] if r['frame'] == frame)
        raw = Path(ram_row['path']).read_bytes()
        parents = [at for at in range(0x170000, len(raw) - 0x90, 4)
                   if struct.unpack_from('<I', raw, at)[0] == 0x021438A0
                   and struct.unpack_from('<2I', raw, at + 0x28) == (228, 48)]
        assert len(parents) == 1
        parent = parents[0]
        assert struct.unpack_from('<4I', raw, parent + 0x40) == (8, 16, 0, 0)
        node_offset = struct.unpack_from('<I', target, 0x1438A0 - 16)[0]
        assert node_offset == 0x64
        frame_origin = struct.unpack_from('<2I', raw, parent + node_offset + 0x20)
        assert frame_origin == (0, 96)
        # Exact original02054A24/28 adds16/8 to the frame origin. No screenshot
        # letters select the model's placement. The lower screen starts at192.
        clean_arm = NdsImage.open('work/clean.nds').read_file('/__arm9__.bin')
        assert target[0x54988:0x54A34] == clean_arm[0x54988:0x54A34]
        origin = (frame_origin[0] + 16, 192 + frame_origin[1] + 8)
        assert origin == (16, 296)
        events = []
        expected_plane = raster(target, row['prepared'].encode('ascii'), 0x01FFCE40 - 0x02000000,
                                size=(228, 48), instruction_limit=400000, glyph_events=events)
        expected = {(origin[0] + i % 228, origin[1] + i // 228) for i, v in enumerate(expected_plane) if v}
        actual = {(x, y) for y in range(296, 344) for x in range(16, 244) if new.getpixel((x, y)) == (0, 8, 0)}
        assert actual == expected, (number, sorted(actual ^ expected)[:8])
        old_ink = {(x, y) for y in range(296, 344) for x in range(16, 244) if old.getpixel((x, y)) == (0, 8, 0)}
        changes = {(x, y) for y in range(384) for x in range(256) if old.getpixel((x, y)) != new.getpixel((x, y))}
        assert changes == old_ink ^ expected
        controls = []
        visible = [e for e in events if e['code'] != 32]
        for event in (visible[0], visible[-1]):
            edge = {(x, y) for x, y in expected if origin[0] + event['x'] <= x < origin[0] + 6 + event['x'] and 296 + event['y'] <= y < 307 + event['y']}
            assert edge and expected - edge != actual
            controls.append({'code': event['code'], 'erased_ink_points': len(edge), 'rejected': True})
        vram_proof = None
        if frame in (32600, 35800):
            state = next(s for s in report['read_only_capture_native_states'] if s['frame'] == frame)
            assert state['read_only_export'] and state['main_RAM_unchanged_by_export'] and not state['state_loaded']
            io_row, vram_row = [state['regions'][tag] for tag in ('9REG', 'LCDM')]
            io, vram = Path(io_row['path']).read_bytes(), Path(vram_row['path']).read_bytes()
            assert sha(io) == io_row['sha256'] and sha(vram) == vram_row['sha256'] and io[0x243] == 0x81
            header = struct.unpack_from('<I', raw, parent + 16)[0]
            flags, words, height, pd, xd = struct.unpack_from('<5I', raw, header - 0x02000000)
            assert (flags, words, height) == (4, 72, 48)
            palette = (header + pd) & 0xFFFFFFFF
            assert palette == 0x02125A20
            assert struct.unpack_from('<H', raw, palette - BASE + 30)[0] == 0x8020
            pixels = (header + xd) & 0xFFFFFFFF
            assert pixels == 0x0601A000
            packed = vram[0x60000 + pixels - 0x06000000:0x60000 + pixels - 0x06000000 + 72 * 4 * 48 // 2]
            indices = bytes(v for b in packed for v in (b & 15, b >> 4))
            view = b''.join(indices[y * 288:y * 288 + 228] for y in range(48))
            # The actual bitmap uses12-pixel rows and palette15. Original modal
            # composition spaces those source rows16 pixels apart on screen.
            # Execute the captured view/context instead of assuming the generic
            # display-raster helper's16-pixel source-row metric is native here.
            itcm_row = state['regions']['ITCM']
            itcm = Path(itcm_row['path']).read_bytes()
            assert sha(itcm) == itcm_row['sha256']
            u = machine(target)
            u.mem_write(BASE, raw)
            u.mem_write(0x01FF0000, itcm)
            u.mem_write(0x01FF8000, itcm)
            u.mem_map(0x06000000, 0x20000)
            u.mem_write(0x06000000, vram[0x60000:0x80000])
            byte_size = 288 * 48 // 2
            u.mem_write(pixels - 16, b'\xA5' * 16 + bytes(byte_size) + b'\xA5' * 16)
            font_pointer = struct.unpack_from('<I', target, 0xD5088)[0]
            assert struct.unpack('<2I', u.mem_read(font_pointer + 4, 8)) == (6, 12)
            ctx = 0x02450000
            call(u, 0xD5160, (ctx, parent + BASE, 1))
            u.mem_write(ctx + 0x30, struct.pack('<I', 15))
            call(u, 0xD5A10, (ctx, 1))
            call(u, 0xD5A18, (ctx, parent + BASE + 0x48))
            call(u, 0xD4DA0, (ctx, parent + BASE + 0x40))
            call(u, 0xD5A2C, (ctx, parent + BASE + 0x30))
            text_pointer = struct.unpack_from('<I', target, 0x54894)[0]
            prepared = row['prepared'].encode('ascii') + b'\0'
            assert bytes(u.mem_read(text_pointer, len(prepared))) == prepared
            call(u, 0x01FFCE40 - BASE, (ctx, text_pointer), instruction_limit=400000)
            generated = bytes(u.mem_read(pixels, byte_size))
            generated_indices = bytes(v for b in generated for v in (b & 15, b >> 4))
            generated_view = b''.join(generated_indices[y * 288:y * 288 + 228] for y in range(48))
            assert set(view) == {0, 15} and view == generated_view
            assert bytes(u.mem_read(pixels - 16, 16)) == bytes(u.mem_read(pixels + byte_size, 16)) == b'\xA5' * 16
            vram_proof = {'header': header, 'original_header_words': [flags, words, height],
                          'actual_view': [228, 48], 'backing_storage': [288, 48],
                          'all10944_declared_view_indices_exact_native_raster': True,
                          'actual_native_font_metrics': [6, 12], 'actual_foreground_palette_index': 15,
                          'actual_foreground_BGR555_word': 0x8020,
                          'captured_original_view_and_prepared_text_pointer_used': True,
                          'full_native_draw_and_ABI_and_backing_guards_pass': True,
                          'undrawn60_column_storage_padding_not_assumed_blank': True,
                          'VRAM_sha256': vram_row['sha256']}
        prompts.append({'native_ID': number, 'frame': frame, 'unchanged_English': row['unchanged_English'],
                        'original_complete_split_line_masks': original_lines,
                        'complete_prepared_lines': row['prepared'].splitlines(),
                        'complete_actual_ink_and_blank_cells_match_native_raster': True,
                        'actual_complete_ink_points': len(actual), 'changed_pixels': len(changes),
                        'all_other_two_screen_pixels_exact': True,
                        'first_final_glyph_erasure_controls': controls,
                        'source_frame_origin': list(frame_origin), 'source_text_view_origin': list(origin),
                        'actual_native_view_VRAM': vram_proof,
                        'both_visible_line_origins': [22, 22]})
    connected = read(ROOT / 'connected_caller_proof.json')
    assert connected['all_original_lookup_and_macro_expansion_executed_no_selected_text_bridge']
    proof.update({'reports': [r[2] for r in runs.values()], 'comparisons': comparisons,
                  'actual_complete_prompt269_and272_pixels': prompts,
                  'native_dispatch_proof_sha256': sha((ROOT / 'native_dispatch_proof.json').read_bytes()),
                  'connected_caller_proof_sha256': sha((ROOT / 'connected_caller_proof.json').read_bytes()),
                  'initial_two_frame_expectation_replaced_by_five_full_text_verified_repeated_states': True,
                  'all4_source_captain_instructions_native_word_rasters_pass': True,
                  'actual_other_two_short_instructions_not_newly_display_verified': True,
                  'no_gameplay_fixtures_in_four_terminal_runs': True,
                  'script_sha256': sha(Path(__file__).read_bytes()),
                  'all18_plaques_incomplete_22_historical_scopes_retained': True})
    save(ROOT / 'release_proof.json', proof)
    print('V651 actual:two complete repaired prompts,left aligned;every other sampled whole screen exact;four terminal cold boots pass.')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--static-only', action='store_true')
    args = parser.parse_args()
    if args.static_only:
        static()
    else:
        actual()


if __name__ == '__main__':
    main()
