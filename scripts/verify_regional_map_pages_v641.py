"""Actual ordinary selection of all seven regional map pages; no ROM edits."""

import struct
from pathlib import Path

from PIL import Image

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.probe_worldmap_overlays_v638 import color5
from scripts.verify_village_wrap_v608 import read, save
from scripts.verify_worldmap_composition_v638 import native_callback

ROOT = Path('work/analysis/regional_map_pages_v641')
CAP = Path('E:/Rota Nova translations/Generated/work/emulation_v193/regional_map_pages_v641')
CONTROL = CAP.with_name(CAP.name + '_control')
ROM = Path('out/all_routes_combined_v640_candidate.nds')
PARENT = Path('out/all_routes_combined_v636_candidate.nds')
BASE, CONTEXT, MAP_SPRITE = 0x02000000, 0x023117C4, 0x02190E80
HEADER, PAGE_BYTES = 0x02279B38, 19520
CASES = [(39600, 0, 'N. Sea'), (42800, 1, 'Med.'), (44000, 2, 'Africa'),
         (45200, 3, 'Indian'), (46400, 4, 'SE Asia'), (47600, 5, 'E Asia'),
         (48800, 6, 'Americas'), (50000, 0, 'N. Sea repeated')]


def report(folder, digest):
    path = folder / 'capture_report.json'
    data = read(path)
    assert data['ROM_sha256'] == digest and data['frames'] == 50000
    assert data['cold_boot'] and not data['savestate_loaded'] and not data['callback_errors']
    assert not data.get('battery_save_preloaded')
    assert not any(v for k, v in data.items() if k.startswith('synthetic_'))
    shots = {}
    for shot in data['frames_captured']:
        assert sha(Path(shot['path']).read_bytes()) == shot['PNG_sha256']
        shots[shot['frame']] = shot
    snapshots = data.get('read_only_capture_RAM_snapshots', []) + data.get('read_only_pause_RAM_snapshots', [])
    ram = {}
    for row in snapshots:
        assert row['read_only_export'] and sha(Path(row['path']).read_bytes()) == row['sha256']
        ram[row['frame']] = row
    return data, shots, ram, {'path': str(path), 'sha256': sha(path.read_bytes())}


def chain(raw):
    node = struct.unpack_from('<I', raw, CONTEXT - BASE + 20)[0]
    seen, rows = set(), []
    while node:
        assert node not in seen and len(seen) < 100
        assert BASE <= node <= BASE + len(raw) - 48
        seen.add(node)
        vtable, next_node = struct.unpack_from('<2I', raw, node - BASE)
        method = struct.unpack_from('<I', raw, vtable - BASE + 12)[0]
        rows.append({'sprite': node, 'vtable': vtable, 'callback': method})
        node = next_node
    assert MAP_SPRITE in seen
    return rows


def native_export(frame, journal):
    assert any(r['frame'] == frame and r['command'].get('export_native_state')
               and r['validation_passed'] for r in journal['commands_received'])
    path = CAP / f'native_state_{frame:06d}/native_state.json'
    data = read(path)
    assert data['read_only_export'] and not data['state_loaded']
    assert data['serialized_RAM_matches_same_frame_direct_export'] and data['main_RAM_unchanged_by_export']
    for row in data['regions'].values():
        assert Path(row['path']).stat().st_size == row['bytes']
        assert sha(Path(row['path']).read_bytes()) == row['sha256']
    return data, {'path': str(path), 'sha256': sha(path.read_bytes()), 'frame': frame}


def validate_page(raw, blob, index):
    assert 0 <= index < 7
    assert struct.unpack_from('<5I', raw, HEADER - BASE) == (4, 61, 160, 20, 52)
    assert raw[HEADER - BASE + 20:HEADER - BASE + 52] == blob[20:52]
    plane = raw[HEADER - BASE + 52:HEADER - BASE + 52 + PAGE_BYTES]
    assert len(plane) == PAGE_BYTES
    assert plane == blob[276 + index * PAGE_BYTES:276 + (index + 1) * PAGE_BYTES]
    assert [i for i in range(8) if plane == blob[276 + i * PAGE_BYTES:276 + (i + 1) * PAGE_BYTES]] == [index]
    return plane


def main():
    before = read(ROOT / 'preflight.json')
    for path, digest in before['release_hashes'].items():
        assert sha(Path(path).read_bytes()) == digest
    assert before['candidate_sha256'] == sha(ROM.read_bytes())
    rom, parent, clean = NdsImage.open(ROM), NdsImage.open(PARENT), NdsImage.open('work/clean.nds')
    source = rom.read_file('/_pxl/seaarea.pxl')
    assert source == parent.read_file('/_pxl/seaarea.pxl') == clean.read_file('/_pxl/seaarea.pxl')
    assert all(source[20 + i * 32:52 + i * 32] == source[20:52] for i in range(8))
    sepia = rom.read_file('/_pxl/seamap.pxl')
    assert sepia == clean.read_file('/_pxl/seamap.pxl') and sepia != source
    current, shots, snapshots, receipt = report(CAP, sha(ROM.read_bytes()))
    control, controls, control_ram, control_receipt = report(CONTROL, sha(PARENT.read_bytes()))
    assert current['core_DLL_sha256'] == control['core_DLL_sha256']
    assert current['core_options'] == control['core_options']
    assert current['scripted_input_schedule'] == control['scripted_input_schedule'] == read(ROOT / 'complete_replay_inputs.json')
    journal_path = CAP / 'navigation_command_journal.json'
    journal = read(journal_path)
    assert journal['ROM_sha256'] == current['ROM_sha256']
    assert all(r['validation_passed'] for r in journal['commands_received'])
    assert journal['commands_received'][-1]['frame'] == 50000
    assert journal['commands_received'][-1]['command']['stop']
    assert [(r['frame'], r['page']) for r in read(ROOT / 'actual_page_cases.json')] == [(f, i) for f, i, _ in CASES]
    rows = []
    for frame, index, name in CASES:
        raw = Path(snapshots[frame]['path']).read_bytes()
        assert len(raw) == 0x400000
        plane = validate_page(raw, source, index)
        old_raw = Path(control_ram[frame]['path']).read_bytes()
        assert validate_page(old_raw, source, index) == plane
        registered = chain(raw)
        callback = native_callback(rom, clean, raw, MAP_SPRITE)
        draw = callback['draw']
        assert draw['header'] == HEADER and draw['header_words'] == [4, 61, 160, 20, 52]
        assert draw['source_xy'] == [0, 0] and draw['source_size'] == [244, 160]
        assert draw['destination_point'] == [6, 16] and draw['palette_bank'] == 0 and draw['screen_selector'] == 0
        export, export_receipt = native_export(frame, journal)
        actual = Image.open(shots[frame]['path']).convert('RGB')
        old = Image.open(controls[frame]['path']).convert('RGB')
        assert actual.size == old.size == (256, 384) and actual.tobytes() == old.tobytes()
        vram = Path(export['regions']['LCDM']['path']).read_bytes()
        screen = [color5(actual.getpixel((x + 6, y + 208))) for y in range(160) for x in range(244)]
        physical = [struct.unpack_from('<H', vram, 0x60000 + 2 * ((y + 16) * 256 + x + 6))[0] & 32767
                    for y in range(160) for x in range(244)]
        assert screen == physical
        # This reports overlay differences; it does not mask or excuse them.
        # Whole displayed images are positively compared with the control above.
        palette = struct.unpack_from('<16H', source, 20)
        source_colors = [palette[n] & 32767 for b in plane for n in (b & 15, b >> 4)]
        owner = 0x0231336C
        filename_ptr = struct.unpack_from('<I', raw, owner - BASE + 12)[0]
        assert raw[filename_ptr - BASE:].split(b'\0')[0] == b'_pxl/seaarea.pxl'
        resident = raw.find(source)
        assert resident >= 0 and raw.find(source, resident + 1) == -1
        rows.append({'frame': frame, 'actual_region': name, 'actual_source_page': index,
            'RAM': snapshots[frame], 'PNG': shots[frame], 'control_PNG': controls[frame],
            'native_export': export_receipt, 'map_registered_draw_callback': callback,
            'actual_registered_sprite_chain': registered,
            'source_map_owner': owner, 'source_owner_filename': '_pxl/seaarea.pxl',
            'entire_unique_resident_source_file_address': BASE + resident,
            'whole_map_packed_bytes_exact_source': PAGE_BYTES,
            'whole_map_indices_exact_source': 39040, 'actual_palette_exact_source': True,
            'whole_two_screen_control_pixels_exact': 98304,
            'whole_actual_map_crop_VRAM_pixels_exact': 39040,
            'actual_source_color_pixels_changed_by_ordinary_overlays': sum(a != b for a, b in zip(source_colors, screen, strict=True)),
            'ordinary_route_overlays_not_independently_reconstructed': True,
            'not_a_voyage_docking_or_earned_route_unlock_test': True})
    # A wrong region must fail the whole-page comparison, despite a valid PXL header.
    raw = Path(snapshots[39600]['path']).read_bytes()
    try:
        validate_page(raw, source, 1)
    except AssertionError:
        rejected = True
    else:
        raise AssertionError('Wrong Mediterranean page accepted for actual North Sea')
    # Preserve the diagnostic that motivated using A Done, rather than crediting hover.
    raw = (CAP / 'frame_041600_arm9_ram.bin').read_bytes()
    assert validate_page(raw, source, 0)
    proof = {'candidate': str(ROM), 'candidate_sha256': sha(ROM.read_bytes()),
        'control_candidate': str(PARENT), 'control_candidate_sha256': sha(PARENT.read_bytes()),
        'reports': [receipt, control_receipt], 'journal_sha256': sha(journal_path.read_bytes()),
        'original_source_seaarea_sha256': sha(source), 'original_source_seamap_sha256': sha(sepia),
        'all7_actual_regional_pages_and_North_Sea_repeat': rows,
        'unique_actual_regional_pages_verified': list(range(7)),
        'all8_callbacks_full_ABI_and_executed_code_words_exact_clean': True,
        'all312320_native_map_indices_and_physical_VRAM_crop_pixels_checked': True,
        'all786432_two_screen_control_pixels_exact': True,
        'negative_wrong_page_rejected': rejected,
        'hover_Med_Y_diagnostic_actual_page0_not_page1': True,
        'ordinary_no_preloaded_save_no_savestate_no_fixture_in_both_runs': True,
        'source_retention_decisions_preserved_no_new_Japanese_text_review_claimed': True,
        'route_overlay_producers_sepia_legacy_consumers_other_states_remain_open': True,
        'all18_original_plaques_incomplete_all22_historical_scopes_retained': True,
        'full_goal_complete': False, 'hardware_device_verification': False,
        'ROM_patch_registry_canonical_and_all_release_pointers_unchanged': True,
        'scripts': {str(p): sha(p.read_bytes()) for p in (Path(__file__),
            Path('scripts/verify_worldmap_composition_v638.py'), Path('scripts/headless_desmume_v193.py'),
            Path('scripts/inspect_desmume_state_v249.py'))}}
    save(ROOT / 'actual_regional_pages_proof.json', proof)
    print('All7 actual regional pages plus North Sea repeat:312320 source indices/VRAM pixels and786432 paired full-screen pixels pass;wrong page rejected.')


if __name__ == '__main__':
    main()
