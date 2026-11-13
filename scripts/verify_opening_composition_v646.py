"""Current opening: source-bound committed geometry, VRAM, and full RGB checks."""

import struct
from collections import defaultdict
from pathlib import Path

from PIL import Image

from dk4tool.graphics.fls import FlsArchive
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.research_committed_composition_v646 import render_order, vram_bindings
from scripts.research_ending_blend_v631 import plane
from scripts.research_ending_transitions_v642 import compose
from scripts.verify_ending_photo_markers_v594 import find_live
from scripts.verify_village_wrap_v608 import read, save

ROOT = Path('work/analysis/opening_composition_v646')
CAP = Path('E:/Rota Nova translations/Generated/work/emulation_v193/opening_composition_v646_committed_full')
ROM = Path('out/all_routes_combined_v640_candidate.nds')
ENGLISH = [4, 5, *range(27, 47)]


def checked_export(state, actual_exporter):
    assert sha(Path(state['path']).read_bytes()) == state['sha256']
    assert state['read_only_export'] and not state['state_loaded'] and state['main_RAM_unchanged_by_export']
    for item in state['files'].values():
        assert sha(Path(item['path']).read_bytes()) == item['sha256']
    committed = state['read_only_committed_geometry']
    path = Path(committed['path'])
    assert sha(path.read_bytes()) == committed['sha256'] and read(path) == {k: v for k, v in committed.items() if k not in ('path', 'sha256')}
    assert committed['script_sha256'] == actual_exporter
    assert committed['read_only_same_process_core_image_export']
    assert committed['RAM_geometry_and_source_VRAM_unchanged_by_read_export']
    assert committed['source_anchors_inside_readable_core_image_sections']
    assert committed['render_array_pointers_from_source_GFX3D_layout_bounded_and_VirtualQuery_checked']
    assert committed['both_state_layouts_all_declared_member_addresses_verified_against_binary_SFORMAT'] == 21
    assert committed['committed_render_lists_not_pending_serialization_lists']
    for p, digest in committed['source_files'].items():
        assert sha(Path(p).read_bytes()) == digest
    for item in committed['files'].values():
        assert sha(Path(item['path']).read_bytes()) == item['sha256']
    # Decode the raw host structs independently of the JSON export.
    pb = Path(committed['files']['committed_polygons_native.bin']['path']).read_bytes()
    vb = Path(committed['files']['committed_vertices_native.bin']['path']).read_bytes()
    assert len(pb) == committed['polygon_count'] * 40 and len(vb) == committed['vertex_count'] * 64
    parsed = []
    for index in range(committed['polygon_count']):
        values = struct.unpack_from('<2I4H4I2f', pb, index * 40)
        kind, primitive = values[:2]
        assert kind in (3, 4) and primitive <= 7
        indices = list(values[2:2 + kind])
        assert all(i < committed['vertex_count'] for i in indices)
        parsed.append({'indices': indices, 'attributes': values[6], 'texture_parameter': values[7],
            'palette': values[8], 'viewport': values[9],
            'vertices': [list(struct.unpack_from('<6f', vb, i * 64)) for i in indices],
            'vertex_colors_RGB6': [list(vb[i * 64 + 48:i * 64 + 51]) for i in indices]})
    assert parsed == committed['polygons']
    return committed


def english_edges(polys, movie, bindings, texture_id, actual):
    texture = movie.texture(texture_id)
    p = next(p for p in polys if bindings[p['texture_parameter'], p['palette']] == texture_id
             and p['attributes'] >> 16 & 31 == 31)
    sampled = {s for s in plane(p, texture) if s is not None}
    ink = {i for i, value in enumerate(texture.indices) if value}
    assert ink and ink <= sampled  # Complete ink/shadow source, no clipped edges.
    original = bytes(texture.indices)
    low, high = min(i % texture.width for i in ink), max(i % texture.width for i in ink)
    controls = []
    if 27 <= texture_id <= 46:
        # Original progressive cards are a source-backed sequence. Remove the
        # first reveal, or restore the previous distinct reveal, to test actual
        # lettering rather than an outer black shadow that can equal its backdrop.
        first = movie.texture(27)
        assert first.palette == texture.palette
        first_ink = {i for i, value in enumerate(first.indices) if value}
        assert first_ink <= ink
        leading = bytearray(original)
        for i in first_ink:
            leading[i] = 0
        previous = next((i for i in range(texture_id - 1, 26, -1)
                         if bytes(movie.texture(i).indices) != original), None)
        trailing = bytes(len(original)) if previous is None else bytes(movie.texture(previous).indices)
        controls = [('remove first revealed name prefix', bytes(leading)),
                    ('remove last distinct name reveal unit', trailing)]
    else:
        for label, column in (('leading source ink column', low), ('trailing source ink column', high)):
            changed = bytearray(original)
            for i in ink:
                if i % texture.width == column:
                    changed[i] = 0
            controls.append((label, bytes(changed)))
    results = []
    for label, altered_source in controls:
        texture.indices[:] = altered_source
        try:
            altered, _ = compose(polys, movie, bindings)
        finally:
            texture.indices[:] = original
        changed = sum(a != b for a, b in zip(altered, actual, strict=True))
        assert changed > 0
        results.append({'control': label, 'changed_source_texels': sum(a != b for a, b in zip(original, altered_source)),
                        'whole_RGB_pixels_changed': changed})
    return {'complete_nonzero_source_ink_and_shadow_texels_sampled': len(ink),
            'both_boundary_deletions_rejected': results}


def main():
    pre, config = read(ROOT / 'preflight.json'), read(ROOT / 'full_config.json')
    for p, digest in pre['release_hashes'].items():
        assert sha(Path(p).read_bytes()) == digest
    rom, clean = NdsImage.open(ROM), NdsImage.open('work/clean.nds')
    source = {p: rom.read_file(p) for p in ('/FLS/M28.fls', '/FLS/logo.fls')}
    movies = {p: FlsArchive(data) for p, data in source.items()}
    assert sha(source['/FLS/M28.fls']) == pre['opening_movie_sha256']
    cm = FlsArchive(clean.read_file('/FLS/M28.fls'))
    assert source['/FLS/M28.fls'] == NdsImage.open('out/all_routes_combined_v573_candidate.nds').read_file('/FLS/M28.fls')
    storage = []
    for i, (a, b) in enumerate(zip(cm.records, movies['/FLS/M28.fls'].records, strict=True)):
        assert a[:4] == b[:4] and a[4] + a[5] == b[4] + b[5]
        if a != b:
            storage.append({'texture': i, 'clean_record': a, 'current_record': b,
                'original_native_geometry_palette_start_size_and_whole_slot_end_preserved': True})
    assert [r['texture'] for r in storage] == list(range(27, 47))
    save(ROOT / 'inherited_name_slot_partition_diagnostic.json', {
        'rejected_assumption_all_current_records_equal_clean': True,
        'whole_current_movie_exact_V573': True, 'twenty_preexisting_palette_padding_pixel_slot_repartitions': storage,
        'no_new_storage_or_ROM_change': True})
    changed = []
    for i in range(cm.count):
        before, now = cm.texture(i), movies['/FLS/M28.fls'].texture(i)
        assert (before.flags, before.width, before.height, before.palette) == (now.flags, now.width, now.height, now.palette)
        if before.indices != now.indices:
            changed.append(i)
    assert changed == ENGLISH and cm.count == 170
    logo = movies['/FLS/logo.fls']
    clean_logo = FlsArchive(clean.read_file('/FLS/logo.fls'))
    assert logo.count == clean_logo.count == 4 and logo.records == clean_logo.records
    assert source['/FLS/logo.fls'] == NdsImage.open('out/all_routes_combined_v573_candidate.nds').read_file('/FLS/logo.fls')
    assert [i for i in range(4) if logo.texture(i).indices != clean_logo.texture(i).indices] == [3]
    assert all(logo.texture(i).palette == clean_logo.texture(i).palette for i in range(4))
    report_path = CAP / 'capture_report.json'
    report = read(report_path)
    assert report['ROM_sha256'] == pre['candidate_sha256'] and report['frames'] == config['frames']
    assert report['cold_boot'] and not report['savestate_loaded'] and not report['callback_errors']
    assert not report['scripted_input_schedule'] and not report.get('battery_save_preloaded')
    assert not any(k.startswith('synthetic_') for k in report)
    assert {r['frame'] for r in report['read_only_capture_GPU_states']} == set(config['gpu_export_frames'])
    actual_exporter = sha((ROOT / 'exporter_committed_full_source.py').read_bytes())
    shots = {s['frame']: s for s in report['frames_captured']}
    cases, failures, english, seen, lag_failures = [], [], {}, defaultdict(set), defaultdict(list)
    seen_groups = defaultdict(set)
    for number, state in enumerate(report['read_only_capture_GPU_states'], 1):
        frame = state['frame']
        committed = checked_export(state, actual_exporter)
        raw = Path(state['files']['arm9_main_ram.bin']['path']).read_bytes()
        assert sha(raw) == state['main_RAM_sha256']
        active = [p for p, data in source.items() if find_live(raw, data)]
        try:
            matches = {}
            for candidate in source:
                try:
                    matches[candidate] = vram_bindings(committed, movies[candidate])
                except (AssertionError, ValueError):
                    pass
            assert matches, ('No whole source match for committed list', active)
            preferred = [p for p in active if p in matches]
            name = preferred[0] if len(preferred) == 1 else next(iter(matches))
            movie = movies[name]
            binding, resources = matches[name]
            ordered, order = render_order(committed)
            expected, draws = compose(ordered, movie, binding)
            shot = shots[frame + 1]
            assert sha(Path(shot['path']).read_bytes()) == shot['PNG_sha256']
            actual = list(Image.open(shot['path']).convert('RGB').crop((0, 0, 256, 192)).get_flattened_data())
            differences = sum(a != b for a, b in zip(expected, actual, strict=True))
            if differences:
                failures.append({'frame': frame, 'RGB_differences': differences})
                continue
            for r in resources:
                seen[name].update(r['source_equivalence_candidates'])
                seen_groups[name].add(tuple(r['source_equivalence_candidates']))
            for tid in ENGLISH if name == '/FLS/M28.fls' else ():
                if tid in english:
                    continue
                control_binding = dict(binding)
                equivalence = []
                for resource in resources:
                    if tid in resource['source_equivalence_candidates']:
                        equivalence = resource['source_equivalence_candidates']
                        control_binding[resource['texture_parameter'], resource['palette']] = tid
                if not any(control_binding[p['texture_parameter'], p['palette']] == tid
                           and p['attributes'] >> 16 & 31 == 31 for p in committed['polygons']):
                    continue
                try:
                    assert compose(ordered, movie, control_binding)[0] == actual
                    edge = english_edges(ordered, movie, control_binding, tid, actual)
                except AssertionError:
                    continue  # Retained as unproved until a full opaque sample exists.
                english[tid] = {'frame': frame, 'display_frame': frame + 1,
                    'source_equivalence_candidates': equivalence,
                    'equivalent_index_control_does_not_identify_indistinguishable_runtime_ID': len(equivalence) > 1, **edge}
            if frame in (706, 707, 708, 709, 1922, 1923, 1924, 1925):
                for lag in (0, 2, 3):
                    other = shots.get(frame + lag)
                    if other is None:
                        continue
                    actual_other = list(Image.open(other['path']).convert('RGB').crop((0, 0, 256, 192)).get_flattened_data())
                    wrong = sum(a != b for a, b in zip(expected, actual_other, strict=True))
                    if wrong:
                        lag_failures[lag].append({'frame': frame, 'whole_RGB_differences': wrong})
            cases.append({'frame': frame, 'display_frame': frame + 1, 'source_movie': name,
                'RAM_controller_source_candidates': active, 'complete_VRAM_source_movie_candidates': list(matches),
                'committed_export': committed['path'], 'committed_export_sha256': committed['sha256'],
                'source_VRAM_bindings': resources, 'native_draws': draws,
                'source_native_render_order': order,
                'whole49152_RGB_pixels_exact_without_exclusions': True})
        except (AssertionError, ValueError, KeyError) as error:
            failures.append({'frame': frame, 'error': repr(error)})
            print('unresolved', frame, repr(error), flush=True)
        if number % 64 == 0:
            print(number, '/', len(config['gpu_export_frames']), 'exact', len(cases),
                  'failures', len(failures), 'M28 source candidates', len(seen['/FLS/M28.fls']), flush=True)
            save(ROOT / 'verification_progress.json', {'cases': cases, 'failures': failures,
                'through_state': number, 'not_a_final_verification': True})
    save(ROOT / 'full_composition_results.json', {'cases': cases, 'failures': failures,
        'source_candidates_seen': {k: sorted(v) for k, v in seen.items()},
        'source_equivalence_groups': {k: sorted(v) for k, v in seen_groups.items()},
        'opaque_English_boundary_controls': english,
        'unproved_English_boundary_controls': sorted(set(ENGLISH) - english.keys()),
        'fixed_lag1_alternatives_rejected': dict(lag_failures),
        'actual_exporter_source_sha256': actual_exporter,
        'script_sha256': sha(Path(__file__).read_bytes()), 'full_goal_complete': False})
    print('cases', len(cases), 'failures', len(failures), 'M28 candidates', len(seen['/FLS/M28.fls']),
          'English opaque controls', len(english), flush=True)


if __name__ == '__main__':
    main()
