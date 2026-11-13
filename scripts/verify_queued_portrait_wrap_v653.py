"""Integrated preservation, exact patch and fresh whole-screen portrait checks."""

import argparse
import struct
from pathlib import Path

from PIL import Image

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.queued_portrait_wrap import transform
from dk4tool.patch.xdelta import apply_xdelta, make_xdelta
from dk4tool.rom.nds import NdsImage
from scripts.native_full_fleet_proximity_v653 import apply_fixture
from scripts.probe_button_prompt_native import BASE, call, machine
from scripts.verify_dialogue_palette_v628 import captured_rgb, raster
from scripts.verify_full_fleet_battle_v652 import fleet_models
from scripts.verify_village_wrap_v608 import read, save

ROOT = Path('work/analysis/queued_portrait_wrap_v653')
ROM = Path('out/all_routes_combined_v653_candidate.nds')
OLD = Path('out/all_routes_combined_v651_candidate.nds')


def static():
    old, new = NdsImage.open(OLD), NdsImage.open(ROM)
    before = {p: d for _, p, d in old.iter_files()} | dict(old.iter_components())
    after = {p: d for _, p, d in new.iter_files()} | dict(new.iter_components())
    assert before.keys() == after.keys()
    assert [p for p in before if before[p] != after[p]] == ['/__arm9__.bin']
    target, change = transform(before['/__arm9__.bin'])
    assert target == after['/__arm9__.bin']
    manifest, parent = read(ROM.with_suffix('.manifest.json')), read(OLD.with_suffix('.manifest.json'))
    stack, pre = read('translations/release_stack.json'), read(ROOT / 'preflight.json')
    assert manifest['profile'] == pre['profile'] == 'all-routes-unified-v653'
    assert manifest['candidate_sha256'] == sha(ROM.read_bytes())
    assert manifest['release_stack_sha256'] == sha(Path('translations/release_stack.json').read_bytes())
    assert stack['accepted_layers'] == pre['accepted_layers'] and len(stack['accepted_layers']) == 114
    assert manifest['base_sha256'] == stack['canonical_baseline']['sha256'] == parent['base_sha256']
    assert sha(Path(manifest['base_rom']).read_bytes()) == manifest['base_sha256']
    assert manifest['batches'] == parent['batches'] and len(manifest['batches']) == 470
    assert manifest['required_batches'] == parent['required_batches'] and all(manifest['checks'].values())
    assert manifest['changed_paths'] == parent['changed_paths']
    assert stack['profiles']['all-routes-unified-v651'] == pre['inherited_profile']
    previous = read('work/analysis/captain_prompt_wrap_v651/static_release_proof.json')
    assert previous['candidate_sha256'] == sha(OLD.read_bytes())
    assert previous['all921_graphics_and_every_other_ROM_file_exact_V640']
    inherited = read('work/analysis/region_boundaries_v640/preservation_proof.json')
    assert sha(Path('work/analysis/region_boundaries_v640/preservation_proof.json').read_bytes()) == previous['inherited921_palette_geometry_and57_embedded_preservation_proof_sha256']
    graphics = [p for p in before if p.lower().endswith(('.pxl', '.fls'))]
    assert len(graphics) == 675 and len(inherited['entries']) == 921
    assert {r['path'] for r in inherited['entries']} == set(graphics)
    assert all(before[p] == after[p] for p in graphics)
    assert inherited['current921_format_palette_extent_checks'] and inherited['all57_embedded_block_extents_exact']
    clean = Path('work/clean.nds')
    assert sha(clean.read_bytes()) == 'f4f07c975cc293f5b2ba469747693d3dd37f2e6dfc408cf5910adf5e83d9177d'
    patch = ROM.with_suffix('.xdelta')
    make_xdelta(clean, ROM, patch)
    rebuilt = ROOT / 'all_routes_combined_v653_PATCH_RECONSTRUCTION.nds'
    apply_xdelta(clean, patch, rebuilt)
    assert rebuilt.read_bytes() == ROM.read_bytes()
    result = {'candidate': str(ROM), 'candidate_sha256': sha(ROM.read_bytes()), 'profile': manifest['profile'],
              'manifest_sha256': sha(ROM.with_suffix('.manifest.json').read_bytes()),
              'ARM9_sha256': sha(target), 'patch_sha256': sha(patch.read_bytes()),
              'base': manifest['base_rom'], 'base_sha256': manifest['base_sha256'], 'transform': change,
              'only_ARM9_existing36_byte_dispatcher_owned_changes_from_V651': True,
              'actual_changed_ARM9_file_bytes': sum(a != b for a, b in zip(before['/__arm9__.bin'], target, strict=True)),
              'all921_views675_containers57_embedded_extents_and_every_other_ROM_file_exact_V651': True,
              'all470_batches114_accepted_layers_and_prior_profiles_retained': True,
              'exact_clean_patch_reconstruction': True, 'reconstructed_ROM': str(rebuilt),
              'canonical_promoted': False, 'full_goal_complete': False}
    save(ROOT / 'static_release_proof.json', result)
    print('V653 static: only original dispatcher; every other file/graphic exact; exact clean patch reconstructed.')


def load(path, digest, frames):
    report = read(path)
    assert report['ROM_sha256'] == digest and report['frames'] == frames
    assert report['cold_boot'] and not report['savestate_loaded'] and not report['callback_errors']
    shots = {}
    for shot in report['frames_captured']:
        assert sha(Path(shot['path']).read_bytes()) == shot['PNG_sha256']
        if shot['frame'] in shots:
            assert Image.open(shots[shot['frame']]['path']).tobytes() == Image.open(shot['path']).tobytes()
        shots[shot['frame']] = shot
    for key in ('read_only_capture_RAM_snapshots', 'read_only_pause_RAM_snapshots'):
        for row in report.get(key, []):
            assert row['read_only_export'] and sha(Path(row['path']).read_bytes()) == row['sha256']
    return report, shots


def view_replay(arm, raw, parent, prepared, state):
    assert state['read_only_export'] and state['main_RAM_unchanged_by_export'] and not state['state_loaded']
    regions = {}
    for key in ('9REG', 'LCDM', 'ITCM'):
        row = state['regions'][key]
        regions[key] = Path(row['path']).read_bytes()
        assert sha(regions[key]) == row['sha256']
    assert regions['9REG'][0x243] == 0x81
    header = struct.unpack_from('<I', raw, parent - BASE + 16)[0]
    flags, words, height, pd, xd = struct.unpack_from('<5I', raw, header - BASE)
    assert (flags, words, height) == (4, 72, 48)
    pixels = (header + xd) & 0xFFFFFFFF
    assert (header + pd) & 0xFFFFFFFF == 0x02125A20 and pixels == 0x0601A000
    count = 288 * 48 // 2
    packed = regions['LCDM'][0x60000 + pixels - 0x06000000:0x60000 + pixels - 0x06000000 + count]
    u = machine(arm)
    u.mem_write(BASE, raw)
    u.mem_write(0x01FF0000, regions['ITCM'])
    u.mem_write(0x01FF8000, regions['ITCM'])
    u.mem_map(0x06000000, 0x20000)
    u.mem_write(0x06000000, regions['LCDM'][0x60000:0x80000])
    u.mem_write(pixels - 16, b'\xA5' * 16 + bytes(count) + b'\xA5' * 16)
    font = struct.unpack_from('<I', arm, 0xD5088)[0]
    assert struct.unpack('<2I', u.mem_read(font + 4, 8)) == (6, 12)
    ctx = 0x02450000
    call(u, 0xD5160, (ctx, parent, 1))
    u.mem_write(ctx + 0x30, struct.pack('<I', 15))
    call(u, 0xD5A10, (ctx, 1))
    call(u, 0xD5A18, (ctx, parent + 0x48))
    call(u, 0xD4DA0, (ctx, parent + 0x40))
    call(u, 0xD5A2C, (ctx, parent + 0x30))
    pointer = struct.unpack_from('<I', arm, 0x54894)[0]
    assert bytes(u.mem_read(pointer, len(prepared) + 1)) == prepared + b'\0'
    call(u, 0x01FFCE40 - BASE, (ctx, pointer), instruction_limit=600000)
    generated = bytes(u.mem_read(pixels, count))
    def extent(data):
        indices = bytes(v for b in data for v in (b & 15, b >> 4))
        return b''.join(indices[y * 288:y * 288 + 228] for y in range(48))
    assert extent(generated) == extent(packed)
    assert bytes(u.mem_read(pixels - 16, 16)) == bytes(u.mem_read(pixels + count, 16)) == b'\xA5' * 16
    return {'all10944_declared_view_indices_exact_native_replay': True,
            'actual6x12_font_and_captured_context_and_prepared_pointer': True,
            'backing_guards_saved_register_ABI_and_complete_native_draw_pass': True,
            'native_view': [228, 48], 'backing_storage': [288, 48],
            'undrawn_storage_padding_not_assumed_blank': True,
            'state_manifest_sha256': sha(Path(state['manifest']).read_bytes()) if state.get('manifest') else None}


def actual():
    proof = read(ROOT / 'static_release_proof.json')
    assert proof['candidate_sha256'] == sha(ROM.read_bytes())
    assert proof['patch_sha256'] == sha(ROM.with_suffix('.xdelta').read_bytes())
    arm = NdsImage.open(ROM).read_file('/__arm9__.bin')
    kanji = NdsImage.open(ROM).read_file('/GRP/KANJI.FNT')
    configs = read(ROOT / 'run_configs.json')
    comparisons, rows, receipts, census = {}, [], [], {}
    pointer = struct.unpack_from('<I', arm, 0x54450)[0]
    palette = struct.unpack_from('<16H', arm, 0x125A20)
    colors = {i: captured_rgb(palette[i]) for i in (14, 15)}
    for case, config in configs.items():
        baseline = Path(config['baseline_report'])
        assert sha(baseline.read_bytes()) == config['baseline_report_sha256']
        old_report, old = load(baseline, sha(OLD.read_bytes()), config['frames'])
        rp = Path(config['output']) / 'capture_report.json'
        report, new = load(rp, proof['candidate_sha256'], config['frames'])
        assert old_report['scripted_input_schedule'] == report['scripted_input_schedule']
        assert old_report['core_options'] == report['core_options'] and old.keys() == new.keys()
        if config.get('donor'):
            assert report['battery_save_preloaded']['source_sha256'] == config['donor_sha256']
            assert sha(Path(config['donor']).read_bytes()) == config['donor_sha256']
        changed = [frame for frame in old if Image.open(old[frame]['path']).tobytes() != Image.open(new[frame]['path']).tobytes()]
        census[case] = changed
        save(ROOT / 'actual_difference_census.json', census)
        if case in ('staffing', 'battle', 'newgame'):
            for frame in changed:
                raws = [(Path(r['path']).parent / f'frame_{frame:06d}_arm9_ram.bin').read_bytes() for r in (old[frame], new[frame])]
                texts = [raw[pointer - BASE:pointer - BASE + 256].split(b'\0')[0] for raw in raws]
                assert b' '.join(texts[0].split()) == b' '.join(texts[1].split())
                images = [Image.open(r['path']).convert('RGB') for r in (old[frame], new[frame])]
                planes, event_lists = [], []
                for text, image in zip(texts, images, strict=True):
                    plane, events = raster(arm, kanji, text)
                    crop = list(image.crop((16, 296, 244, 376)).get_flattened_data())
                    for index in (14, 15):
                        observed = {i for i, rgb in enumerate(crop) if rgb == colors[index]}
                        expected = {i for i, p in enumerate(plane) if p == index}
                        assert observed == expected, (case, frame, index, sorted(observed ^ expected)[:12], text)
                    planes.append(plane)
                    event_lists.append(events)
                visible = [e for e in event_lists[1] if e['code'] not in (0, 10, 13, 32)]
                text = texts[1].decode('cp932')
                expected_codes = [int.from_bytes(c.encode('cp932'), 'big') for c in text if not c.isspace()]
                assert [e['code'] for e in visible] == expected_codes
                at = 0
                for word in text.split():
                    group = visible[at:at + len(word)]
                    assert len({e['y'] for e in group}) == 1, (frame, word)
                    at += len(word)
                delta = {(i % 228 + 16, i // 228 + 296) for i, (a, b) in enumerate(zip(*planes, strict=True)) if a != b}
                observed_delta = {(x, y) for y in range(384) for x in range(256) if images[0].getpixel((x, y)) != images[1].getpixel((x, y))}
                assert delta == observed_delta, (case, frame, len(delta ^ observed_delta))
                controls = []
                for event in (visible[0], visible[-1]):
                    width = 12 if event['code'] > 255 else 6
                    erased = [i for i, v in enumerate(planes[1]) if v and event['x'] <= i % 228 < event['x'] + width and event['y'] <= i // 228 < event['y'] + 12]
                    assert erased
                    modified = bytearray(planes[1])
                    for i in erased:
                        modified[i] = 0
                    assert any({i for i, p in enumerate(modified) if p == index}
                               != {i for i, p in enumerate(planes[1]) if p == index}
                               for index in (14, 15))
                    controls.append({'code': event['code'], 'erasing_native_ink_points_rejected': len(erased)})
                parents = [a for a in range(0x170000, len(raws[1]) - 0x90, 4)
                           if struct.unpack_from('<I', raws[1], a)[0] == 0x021438A0
                           and struct.unpack_from('<2I', raws[1], a + 0x28) == (228, 48)]
                assert len(parents) == 1
                parent = parents[0]
                assert struct.unpack_from('<2I', raws[1], parent + 0x84) == (0, 96)
                state = next((s for key in ('read_only_capture_native_states', 'read_only_pause_native_states')
                              for s in report.get(key, []) if s['frame'] == frame), None)
                if state is None:
                    state_path = Path(config['output']) / f'native_state_{frame:06d}/native_state.json'
                    if state_path.exists():
                        state = read(state_path)
                        state['manifest'] = str(state_path)
                native = view_replay(arm, raws[1], parent + BASE, texts[1], state) if state else None
                rows.append({'case': case, 'frame': frame,
                    'original_prepared': texts[0].decode('cp932'), 'repaired_prepared': text,
                    'whole228x80_display_ink_shadow_and_blank_cells_exact': True,
                    'all_words_single_row_and_all_leading_trailing_glyphs_in_order': True,
                    'first_final_erasure_controls': controls,
                    'only_complete_native_ink_shadow_delta_changes_any_two_screen_pixel': True,
                    'changed_pixel_positions': len(delta), 'actual_native_view': native,
                    'source_PNG': old[frame], 'candidate_PNG': new[frame]})
            # Independently retain original fleet outcomes, not only pictures.
            model_frames = {'staffing': (14000, 16800), 'battle': (13200, 14400, 16000, 23600), 'newgame': ()}
            for frame in model_frames[case]:
                paths = [Path(r[frame]['path']).parent / f'frame_{frame:06d}_arm9_ram.bin' for r in (old, new)]
                states = [fleet_models(arm, p.read_bytes(), 1) for p in paths]
                fields = [[(s['name'], s['canonical_Hull_Crew'], s['live_Hull_Crew']) for s in fleet] for fleet in states]
                assert fields[0] == fields[1]
        fixtures = report.get('synthetic_battle_recovery_proximity_fixtures', [])
        if case == 'battle':
            assert [(f['frame'], f['action']) for f in fixtures] == [(4800, 'approach'), (5200, 'approach')]
            for fixture in fixtures:
                raw = (Path(config['output']) / f"frame_{fixture['frame']:06d}_arm9_ram.bin").read_bytes()
                after, expected = apply_fixture(arm, raw, 'approach')
                assert expected == {k: v for k, v in fixture.items() if k != 'frame'}
                assert sha(after) == fixture['after_RAM_sha256'] and len(fixture['owned_bytes']) == 8
        else:
            assert not any(v for k, v in report.items() if k.startswith('synthetic_'))
        comparisons[case] = {'total_unique_frames': len(old), 'changed_frames': changed,
                             'unchanged_whole_two_screen_frames': len(old) - len(changed),
                             'original_inputs_and_core_options_exact': True,
                             'native_fleet_outcomes_checked_frames': model_frames[case]}
        receipts.append({'case': case, 'path': str(rp), 'sha256': sha(rp.read_bytes())})
    assert any(r['case'] == 'staffing' and r['frame'] == 5200 for r in rows)
    assert any(r['case'] == 'staffing' and r['frame'] == 12800 for r in rows)
    assert any(r['case'] == 'battle' and r['frame'] == 15200 for r in rows)
    assert sum(r['actual_native_view'] is not None for r in rows) >= 3
    proof.update({'reports': receipts, 'comparisons': comparisons, 'actual_complete_portrait_planes': rows,
                  'all114_native_voice_layouts_proof_sha256': sha((ROOT / 'native_dispatch_proof.json').read_bytes()),
                  'connected_original_callers_proof_sha256': sha((ROOT / 'connected_caller_proof.json').read_bytes()),
                  'all_three_observed_word_splits_repaired': True,
                  'all18_original_plaques_incomplete_22_historical_scopes_retained': True,
                  'three_terminal_cold_boots_two_coordinate_only_battle_fixtures_disclosed': True,
                  'script_sha256': sha(Path(__file__).read_bytes())})
    save(ROOT / 'release_proof.json', proof)
    print('V653 actual: three repaired contexts, complete native text planes and every other sampled pixel verified.')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--static-only', action='store_true')
    args = parser.parse_args()
    static() if args.static_only else actual()


if __name__ == '__main__':
    main()
