"""Carry actual gender-cell displays forward; retain separate replay limits."""

from pathlib import Path

from ndspy.code import MainCodeFile, loadOverlayTable
from PIL import Image

from dk4tool.graphics.pxl import PxlImage
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.inspect_committed_gpu_v646 import CORE, CORE_SHA
from scripts.verify_portrait_native_pixels_v202 import native5
from scripts.verify_room_gender_v694 import marker_cell
from scripts.verify_village_wrap_v608 import read, save

ROOT = Path('work/analysis/gender_reconciliation_v720')
ROM = Path('out/all_routes_combined_v712_candidate.nds')
CAP = Path('E:/Rota Nova translations/Generated/work/emulation_v193')
PROOFS = {
    'room': Path('work/analysis/room_gender_v694/proof.json'),
    'room_exception': Path('work/analysis/gender_exception_v697/proof.json'),
    'person_exception': Path('work/analysis/person_gender_v698/final/screen1/proof.json'),
}


def main():
    ROOT.mkdir(exist_ok=True)
    assert not (ROOT / 'proof.json').exists()
    proofs = {k: read(p) for k, p in PROOFS.items()}
    current = NdsImage.open(ROM)
    digest = sha(ROM.read_bytes())
    assert digest == '6534e5619673ea6bdffa3a2342622b99ef393bef52ef58cac131ee94ae0f4030'
    old_path = Path(proofs['room']['candidate'])
    assert all(p['candidate_sha256'] == sha(old_path.read_bytes()) for p in proofs.values())
    old = NdsImage.open(old_path)
    marker_path = '/_pxl/__marker.pxl'
    raw = current.read_file(marker_path)
    assert raw == old.read_file(marker_path)
    marker = PxlImage.from_bytes(raw)
    assert (marker.width, marker.height, marker.bits_per_pixel) == (256, 256, 4)
    arms = [r.read_file('/__arm9__.bin') for r in (current, old)]
    # Complete original draw/helper and update regions, plus source destination
    # points; no whole-update equivalence is inferred from these byte checks.
    ranges = [(0x14BE8, 0x14F60), (0x157D8, 0x15948), (0x9C1DC, 0x9C27C),
        (0x80324, 0x80A48), (0x23C60, 0x23CB0), (0xD3A1C, 0xD41E8),
        (0xD6558, 0xD6690), (0x1146A8, 0x1146B0)]
    for lo, hi in ranges:
        assert arms[0][lo:hi] == arms[1][lo:hi], (hex(lo), hex(hi))
    low = []
    for a, b in zip(MainCodeFile(arms[0], 0x02000000).sections,
                    MainCodeFile(arms[1], 0x02000000).sections, strict=True):
        if a.ramAddress < 0x02000000:
            assert a.ramAddress == b.ramAddress and a.data == b.data
            low.append({'address': a.ramAddress, 'bytes': len(a.data), 'sha256': sha(bytes(a.data))})
    overlays = []
    for image in (current, old):
        overlays.append(loadOverlayTable(image.rom.arm9OverlayTable, lambda _, f, image=image: image.rom.files[f]))
    assert overlays[0].keys() == overlays[1].keys()
    for key in overlays[0]:
        assert overlays[0][key].data == overlays[1][key].data
    source_hash = sha(raw)
    for row in proofs['room']['whole_file_original_native_owner_getters']:
        assert row['complete_file_sha256'] == source_hash
    for row in proofs['room_exception']['original_raw_gender1_both_states_processed_male0_then_female1']:
        assert row['whole_cached_Marker_sha256'] == source_hash
    for row in proofs['person_exception']['original_source_getters_and_draw_arguments']:
        assert row['cached_Marker_sha256'] == source_hash
    assert sha(CORE.read_bytes()) == CORE_SHA

    reports, pictures = {}, {}

    def report(path, expected=None):
        path = Path(path)
        if str(path) in reports:
            return pictures[str(path)]
        if expected is not None:
            assert sha(path.read_bytes()) == expected
        d = read(path)
        assert d['ROM_sha256'] == proofs['room']['candidate_sha256']
        assert d['core_DLL_sha256'] == CORE_SHA and d['cold_boot'] and not d['savestate_loaded']
        assert not d['callback_errors'] and not d['hardware_device_verification']
        frames = {}
        for row in d['frames_captured']:
            p = Path(row['path'])
            assert sha(p.read_bytes()) == row['PNG_sha256']
            if row['frame'] in frames:
                assert frames[row['frame']]['PNG_sha256'] == row['PNG_sha256']
            frames[row['frame']] = row
        reports[str(path)] = {'path': str(path), 'sha256': sha(path.read_bytes()),
            'historical_ROM_sha256': d['ROM_sha256'], 'frames': d['frames'],
            'historical_not_new_V712_execution': True}
        pictures[str(path)] = frames
        return frames

    cells, used = [], {}

    def check(frame_row, sex, point, family, metadata):
        path = Path(frame_row['path'])
        used[str(path)] = frame_row['PNG_sha256']
        image = Image.open(path).convert('RGB')
        x, y = point
        actual = [native5(p) for p in image.crop((x, y, x + 16, y + 16)).get_flattened_data()]
        expected = marker_cell(marker, 48, sex)
        assert actual == expected, (family, frame_row['frame'])
        cells.append({'family': family, 'frame': frame_row['frame'], 'image': str(path),
            'sex_selector': sex, 'source': list(((232, 96), (240, 112))[sex]),
            'palette_bank': 48, 'destination': point,
            'all256_native5_pixels_with_complete_symbol_edges_and_background_exact': True, **metadata})

    for row in proofs['room']['complete_actual_cells']:
        frames = report(CAP / ('room_gender_v694_' + row['case']) / 'capture_report.json')
        check(frames[row['frame']], row['sex'], [80, 80], 'Deck personnel ordinary selected officers',
            {'actor': row['actor'], 'fixture_for_actor_gender_selection': False})
    for key, field, report_field, point in (
            ('room_exception', 'complete_actual_symbol_cells', 'four_declared_fixture_cold_boot_runs', [80, 80]),
            ('person_exception', 'complete_symbol_cells', 'four_fixture_cold_boot_runs', [84, 76])):
        by = {r['case']: r for r in proofs[key][report_field]}
        for row in proofs[key][field]:
            item = by[f"flag{row['flag9']}_observed"]
            frames = report(item['path'], item['sha256'])
            sex = row.get('selector', row['flag9'])
            check(frames[row['frame']], sex, point, key,
                {'flag9': row['flag9'], 'authorized_private_lookup_story_flag_fixture': True,
                 'earned_recruitment_reveal_or_normal_restored_portrait_not_claimed': True})
    assert len(cells) == 44
    limits_path = Path('work/analysis/thumb_controls_v700/native_IO_diagnostic.json')
    limits = read(limits_path)
    failure_path = Path('work/analysis/person_gender_v698/final/screen1/native_flag0_call1_failure.json')
    assert limits['failure'] == read(failure_path)
    assert limits['first_failure_is_original_halfword_read_of_unmapped_DS_IO_04000204']
    assert limits['later_prefix_behavior_full_state_equivalence_and_V694_suffix_NOT_proven']
    releases = [ROM, ROM.with_suffix('.manifest.json'), ROM.with_suffix('.xdelta'),
        Path('translations/release_stack.json'), Path('out/raphael_natural_v2_accepted_base.nds')]
    save(ROOT / 'proof.json', {'candidate': str(ROM), 'candidate_sha256': digest,
        'prior_display_proofs': {k: {'path': str(p), 'sha256': sha(p.read_bytes())} for k, p in PROOFS.items()},
        'whole_Marker_file_sha256': source_hash, 'whole_file_exact_to_actual_cached_sources': True,
        'unchanged_original_native_code_ranges': [{'ARM9_range': [a, b], 'sha256': sha(arms[0][a:b])} for a, b in ranges],
        'unchanged_complete_low_main_sections': low, 'whole_overlay_bytes_exact': True,
        'historical_reports_rechecked': list(reports.values()),
        'all44_complete_actual_symbol_cells': cells, 'complete_native5_pixel_comparisons': 44 * 256,
        'reused_screenshot_hashes': used,
        'two_original_loose_PXL_parents_both_symbols_and_tested_identity8_exception_display_scope_complete': True,
        'diagnostic_IO_limit': {'path': str(limits_path), 'sha256': sha(limits_path.read_bytes()),
            'original_failure': str(failure_path), 'original_failure_sha256': sha(failure_path.read_bytes()),
            'not_a_production_graphics_failure_or_complete_prefix_equivalence_proof': True},
        'V694_full_suffix_RAM_DTCM_comparison_still_unresolved_not_waived': True,
        'embedded_marker_copy_consumer_and_unknown_other_parents_remain_open': True,
        'no_new_emulator_run_no_guide_promotion_no_ROM_or_art_edit': True,
        'release_hashes_unchanged': {str(p): sha(p.read_bytes()) for p in releases},
        'verifier_sha256': sha(Path(__file__).read_bytes()), 'full_goal_complete': False})
    print('V720: 44 actual complete cells/11264 pixels source-exact to V712 across two verified parents; replay limits retained.', flush=True)


if __name__ == '__main__':
    main()
