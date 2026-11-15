"""Verify whole relocated planes, two embedded ARM9 UI atlases and control crops."""

import struct
from pathlib import Path

from PIL import Image, ImageDraw

from dk4tool.graphics.pxl import PxlImage, bgr555
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.inspect_committed_gpu_v646 import CORE, CORE_SHA
from scripts.research_relocated_sources_v695 import CURRENT, ROOT
from scripts.scan_graphic_template_aliases_v602 import TEMPLATES, find_matches
from scripts.verify_graphic_paints_v669 import intersecting
from scripts.verify_village_wrap_v608 import read, save

FRAMES = (6400, 7200, 8000)
SOURCE_ART = {0x021279AC: ('Original button backdrops', 24, 48, 576),
              0x0211B688: ('Original A B X Y L R icons', 96, 28, 1344)}


def unpack(packed, depth):
    return bytes(v for b in packed for v in (b & 15, b >> 4)) if depth == 4 else packed


def index_words(indices):
    return b''.join(struct.pack('<H', i) for i in indices)


def template(image, name, path, box):
    p = PxlImage.from_bytes(image.read_file(path))
    left, top, right, bottom = box
    lines = [index_words(p.indices[y * p.width + left:y * p.width + right]) for y in range(top, bottom)]
    anchor = max(range(len(lines)), key=lambda i: sum(lines[i]))
    return {'name': name, 'width': right - left, 'height': bottom - top, 'rows': lines, 'anchor': anchor}


def main():
    current, original = NdsImage.open(CURRENT), NdsImage.open('work/clean.nds')
    old = NdsImage.open('out/all_routes_combined_v653_candidate.nds')
    assert sha(Path('out/all_routes_combined_v653_candidate.nds').read_bytes()) == read('work/analysis/equipment_cursor_v663/preflight.json')['candidate_sha256']
    assert sha(CORE.read_bytes()) == CORE_SHA
    arm, old_arm, clean_arm = [r.read_file('/__arm9__.bin') for r in (current, old, original)]
    source_hash = sha(Path('scripts/research_relocated_sources_v695.py').read_bytes())
    preflight = ROOT / 'preflight.json'
    if not preflight.exists():
        frozen = read('work/analysis/confirm_material_v572/audit_scope_before.json')
        paths = (CURRENT, CURRENT.with_suffix('.manifest.json'), CURRENT.with_suffix('.xdelta'),
                 Path('translations/release_stack.json'), Path('work/clean.nds'),
                 Path('out/raphael_natural_v2_accepted_base.nds'))
        save(preflight, {'candidate': str(CURRENT), 'candidate_sha256': sha(CURRENT.read_bytes()),
            'release_hashes': {str(p): sha(p.read_bytes()) for p in paths},
            'all_original_audits_before': {name: read(Path('translations') / name) for name in frozen},
            'previous_goal_turn_classification': 'progress: V694 actual second room symbol coverage recorded',
            'captured_V653_is_retained_research_not_new_current_gameplay': True})
    pre = read(preflight)
    for path, digest in pre['release_hashes'].items():
        assert sha(Path(path).read_bytes()) == digest
    pxls = [(path, data) for _, path, data in current.iter_files() if path.lower().endswith('.pxl')]
    assert len(pxls) == 660 and all(data == old.read_file(path) for path, data in pxls)
    templates = [(version, template(r, *row)) for version, r in (('current_English', current), ('original_Japanese', original))
                 for row in TEMPLATES]
    bodies, selected, art, references = [], [], [], {}
    sheet = Image.new('RGB', (1024, 1400), '#263238')
    draw = ImageDraw.Draw(sheet)
    for frame in FRAMES:
        folder = ROOT / f'{frame}_complete_planes'
        report = read(folder / 'research.json')
        assert report['script_sha256'] == source_hash and report['all660_current_PXL_files_exact_captured_ROM']
        assert report['all_executed_current_code_matches'] and not report['current_registered_code_differences']
        assert len(report['calls']) == 59 and len(report['headers']) == 14
        result = report['native_paint_result']
        assert result['whole98304_bytes_written_over_poison']
        assert result['no_output_read_before_write_no_visible_VRAM_source_no_VRAM_write']
        assert result['original_fragment_ABI_guards_and_registered_instruction_bytes_pass']
        # Same explicit off-phase input as the retained independent V663 component.
        native_path = folder / f'native_lower_{frame}_off.bin'
        retained = Path('work/analysis/equipment_cursor_v663') / f'native_lower_{frame}_off.bin'
        assert native_path.read_bytes() == retained.read_bytes()
        references[str(retained)] = sha(retained.read_bytes())
        fields = []
        for n, h in enumerate(report['headers']):
            assert not h.get('unsupported_extent') and not h.get('whole_declared_plane_not_readable')
            packed = Path(h['packed_path']).read_bytes()
            palette = Path(h['selected_palette_path']).read_bytes()
            assert sha(packed) == h['packed_sha256'] and sha(palette) == h['selected_palette_sha256']
            assert len(packed) == h['width'] * h['height'] * h['depth'] // 8
            indices = unpack(packed, h['depth'])
            assert len(indices) == h['width'] * h['height'] and sha(indices) == h['indices_sha256']
            matches = h['whole_index_plane_matching_current_PXL_paths']
            for path in matches:
                data = current.read_file(path)
                flags, width_words, height, palette_at, pixels_at = struct.unpack('<5I', data[:20])
                depth = flags & 255
                assert (depth, width_words * (16 // depth), height) == (h['depth'], h['width'], h['height'])
                assert data[pixels_at:] == packed
                bank = h['bank']
                assert data[palette_at + bank * (2 << depth):palette_at + (bank + 1) * (2 << depth)] == palette
            whole_matches = []
            encoded = index_words(indices)
            for version, t in templates:
                for box in find_matches(encoded, h['width'], h['height'], t):
                    whole_matches.append({'version': version, 'template': t['name'], 'box': box})
            if whole_matches:
                assert matches == ['/_pxl/__frame.pxl']
                assert len(whole_matches) == 5 and all(m['version'] == 'current_English' for m in whole_matches)
                assert {m['template'] for m in whole_matches} == {'Pick_Cargo', 'Pick_Ship', 'Done', 'Rank', 'Cancel'}
            body = {'frame': frame, 'header_index': n, 'words': h['words'], 'whole_pixel_and_selected_palette_matches': matches,
                    'complete_source_plane_template_matches': whole_matches,
                    'packed_bytes': len(packed), 'selected_palette_bytes': len(palette)}
            bodies.append(body)
            if h['pixels_pointer'] in SOURCE_ART:
                label, width, height, size = SOURCE_ART[h['pixels_pointer']]
                assert (h['width'], h['height'], len(packed)) == (width, height, size)
                at = h['pixels_pointer'] - 0x02000000
                assert packed == arm[at:at + size] == old_arm[at:at + size] == clean_arm[at:at + size]
                assert not whole_matches
                art.append({'frame': frame, 'classification': label, 'address': h['pixels_pointer'],
                            'bytes': size, 'sha256': sha(packed), 'clean_V653_and_current_ROM_exact': True,
                            'no_Japanese_text_in_visually_reviewed_source': True,
                            'original_Latin_controller_labels_or_decorative_UI_retained': True})
            if frame == 6400:
                colors = [bgr555(v)[:3] for v, in struct.iter_unpack('<H', palette)]
                im = Image.new('RGB', (h['width'], h['height']))
                im.putdata([colors[i] for i in indices])
                image_path = ROOT / f'source_plane_{n:02d}.png'
                im.save(image_path)
                x, y = n % 4 * 256, n // 4 * 350
                draw.text((x + 3, y + 3), f"{n} {h['width']}x{h['height']} bank{h['bank']}", fill='white')
                im.thumbnail((250, 320))
                sheet.paste(im, (x + 3, y + 25))
        for row in report['calls']:
            h = report['headers'][row['header_index']]
            native_matches = next(b['complete_source_plane_template_matches'] for b in bodies
                                  if b['frame'] == frame and b['header_index'] == row['header_index'])
            cells = [(m['template'], tuple(m['box'])) for m in native_matches]
            touched = intersecting(row['source_XYWH'], row['primitive'] == 0x01FFAE70, cells)
            assert not touched
            fields.append({'primitive': row['primitive'], 'header': row['header_index'],
                           'source': row['source_XYWH'], 'miniature_template_intersections': touched})
        selected.append({'frame': frame, 'calls': fields,
                         'off_phase_retained_native_bytes_exact': True,
                         'controlled_off_phase_vs_capture_RGB_differences_unwaived': result['complete_lower_RGB_difference_count']})
        # Preserve all source state files used by the original replay, not just PNGs.
        cap = Path('E:/Rota Nova translations/Generated/work/emulation_v193/equipment_cursor_v663_current')
        capture = read(cap / 'capture_report.json')
        assert capture['ROM_sha256'] == read('work/analysis/equipment_cursor_v663/preflight.json')['candidate_sha256']
        assert capture['core_DLL_sha256'] == CORE_SHA and capture['cold_boot']
        assert not capture['savestate_loaded'] and not capture['callback_errors']
        assert not any(v for k, v in capture.items() if k.startswith('synthetic_'))
        snapshot = next(s for s in capture['read_only_capture_RAM_snapshots'] if s['frame'] == frame)
        assert sha(Path(snapshot['path']).read_bytes()) == snapshot['sha256']
        for path in (cap / 'capture_report.json', cap / f'frame_{frame:06d}_arm9_ram.bin',
                     cap / f'capture_native_state_{frame:06d}/native_state.json'):
            references[str(path)] = sha(path.read_bytes())
        state = read(cap / f'capture_native_state_{frame:06d}/native_state.json')
        for region in state['regions'].values():
            p = Path(region['path'])
            assert sha(p.read_bytes()) == region['sha256']
            references[str(p)] = region['sha256']
    assert len(bodies) == 42 and len(art) == 6 and sum(len(x['calls']) for x in selected) == 177
    # Complete matcher controls retain a source crop at a different row stride.
    t = templates[2][1]
    canvas = bytearray(150 * 20 * 2)
    for y, line in enumerate(t['rows']):
        canvas[((4 + y) * 150 + 13) * 2:((4 + y) * 150 + 13) * 2 + len(line)] = line
    assert list(find_matches(bytes(canvas), 150, 20, t)) == [[13, 4, 13 + t['width'], 4 + t['height']]]
    y = next(y for y in range(t['height']) if y != t['anchor'] and any(t['rows'][y]))
    x = next(x for x in range(t['width']) if t['rows'][y][x * 2:x * 2 + 2] != b'\0\0')
    canvas[((4 + y) * 150 + 13 + x) * 2] ^= 1
    assert not list(find_matches(bytes(canvas), 150, 20, t))
    sp = ROOT / 'source_planes_review.png'
    sheet.save(sp)
    save(ROOT / 'proof.json', {'candidate': str(CURRENT), 'candidate_sha256': pre['candidate_sha256'],
        'all660_current_PXL_files_equal_V653_source': True,
        'complete_actual_native_source_planes': bodies, 'selected_actual_original_paint_calls': selected,
        'two_original_ARM9_embedded_UI_atlases': art,
        'three_complete_registered_and_current_code_native_paints_and_retained_output_exact': True,
        'seven_current_and_seven_original_control_templates_search_all42_whole_planes': True,
        'only_known_Frame_planes_contain_five_templates_none_selected_in177_calls': True,
        'no_missing_parent_no_global_unused_or_current_gameplay_claim': True,
        'row_stride_and_changed_non_anchor_ink_controls_pass': True,
        'three_off_phase_RGB_capture_mismatches_retained_not_new_frame_equivalence': True,
        'review_sheet': str(sp), 'review_sheet_sha256': sha(sp.read_bytes()),
        'external_retained_capture_sources': references,
        'all18_plaques_incomplete22_original_scopes_six_control_contexts_and_broader_goal_open': True,
        'verifier_sha256': sha(Path(__file__).read_bytes()), 'producer_sha256': source_hash,
        'reused_helper_sources': {p: sha(Path(p).read_bytes()) for p in (
            'scripts/research_equipment_cursor_v663.py', 'scripts/research_town_scene_v644.py',
            'scripts/scan_graphic_template_aliases_v602.py', 'scripts/verify_graphic_paints_v669.py')},
        'ROM_manifest_patch_registry_canonical_and_release_pointers_unchanged': True,
        'full_goal_complete': False})
    print('V695: 42 whole relocated planes/177 native selections; two original ARM9 UI atlases classified; seven current and original control templates exclude additional copies in these planes; actual missing parents remain open.', flush=True)


if __name__ == '__main__':
    main()
