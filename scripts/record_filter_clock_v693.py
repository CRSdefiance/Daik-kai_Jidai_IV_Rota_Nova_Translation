"""Record the closed same-frame cursor gap while preserving the full graphics audit."""

from pathlib import Path

from dk4tool.patch.grand_race_menu_release import sha
from scripts.inspect_committed_gpu_v646 import SOURCE
from scripts.record_memory_streams_v682 import copy
from scripts.run_filter_predecessors_v693 import ROOT
from scripts.run_village_visits_v664 import CAP
from scripts.verify_village_wrap_v608 import read, save

BASE = ROOT.parent
ARCHIVE = Path('E:/Rota Nova translations/Screenshots/Test fixtures/V693 Original cursor clocks and DMA')
DOC = Path('docs/filter_clock_v693_checkpoint.md')
KEY = 'actual_filter_highlights40_clocks16_native_paints_DMA55_97_four_full_same_frame_planes_v693'
SOURCES = ('scripts/observe_filter_clock_v693.py', 'scripts/run_filter_clock_v693.py',
    'scripts/replay_filter_clock_v693.py', 'scripts/run_filter_predecessors_v693.py',
    'scripts/replay_filter_predecessors_v693.py', 'scripts/verify_filter_clock_v693.py',
    'scripts/record_filter_clock_v693.py', 'scripts/verify_filter_clock_archive_v693.py',
    'scripts/observe_transition_scanlines_v659.py', 'scripts/verify_transition_scanlines_v659.py',
    'scripts/observe_file_requests_v681.py', 'scripts/check_file_requests_v681.py')


def main():
    pp = ROOT / 'proof.json'
    proof, pre = read(pp), read(ROOT / 'preflight.json')
    assert proof['verifier_sha256'] == sha(Path('scripts/verify_filter_clock_v693.py').read_bytes())
    assert proof['specific_V692_cursor_timing_gap_closed_without_ROM_or_artwork_change']
    assert len(proof['all4_complete_same_frame_native_bitmap_and_RGB_predictions']) == 4
    assert proof['total_whole_same_ROM_unobserved_pairs'] == 152
    for path, digest in pre['release_hashes'].items():
        assert sha(Path(path).read_bytes()) == digest
    save(ROOT / 'visual_review.json', {'actual_and_original_native_predicted_four_lower_screens_opened': proof['review_sheet'],
        'sheet_sha256': proof['review_sheet_sha256'],
        'portrait_frames_sprites_complete_popup_letters_and_original_highlights_match': True,
        'specific_two_cursor_observations_resolved_other_graphics_and_all18_plaques_remain_open': True,
        'no_fixture_or_observer_picture_promoted_to_guide': True})
    entry = {'documentation': str(DOC), 'proof': str(pp), 'proof_sha256': sha(pp.read_bytes()),
        'candidate': proof['candidate'], 'candidate_sha256': proof['candidate_sha256'],
        'all16_original_native_paints1572864_output_bytes_registers_CPSR_and_registered_code_exact': True,
        'all40_observed_SDK_clock_inputs_native_original_modulo_decisions_verified': True,
        'switch_rows55_97_from_original_DMA_PC_full_arguments_not_pixels_or_frame_fit': True,
        'all4_full_same_frame98304_byte_bitmap_and49152_pixel_RGB_compositions_exact': True,
        'four_wrong_phase_controls_fail_152_whole_baseline_pairs_four_complete_RAM_pairs_pass': True,
        'V692_87_and1446_highlight_observations_explained_by_original_clock_and_transfer_timing': True,
        'specific_V692_cursor_gap_closed_no_ROM_or_artwork_change': True,
        'second_gender_other_contexts_all18_plaques_and22_original_scopes_remain_open_or_exact': True,
        'ROM_manifest_patch_registry_canonical_and_release_pointers_unchanged': True,
        'archive': str(ARCHIVE), 'full_goal_complete': False}
    frozen = read('work/analysis/confirm_material_v572/audit_scope_before.json')
    for name, scope in frozen.items():
        path = Path('translations') / name
        data = read(path)
        assert data == pre['all_original_audits_before'][name]
        assert data.get('historical_pending_items_retained') == scope['historical_pending_items_retained']
        assert data.get('plaque_style_v247', {}).get('ongoing_plaque_inventory') == scope['ongoing_plaque_inventory']
        data[KEY], data['current_goal_turn_classification'] = entry, 'progress'
        save(path, data)
        copy(path, ARCHIVE / 'audits' / name)
    heading = '## V693: original cursor clocks and exact same-frame DMA composition'
    addition = (
        'The two V692 highlight observations are explained without artwork or ROM changes. '
        'Four15200-frame read-only observer runs match152 whole unobserved baseline pairs '
        'and four complete terminal RAM states. Sixteen original lower paints reproduce '
        '1572864 output bytes,all writes/no prior reads,return registers/CPSR and every '
        'executed registered ARM/ITCM/overlay/pool instruction. Forty actual SDK tick '
        'inputs reproduce original modulo highlight decisions. Original DMA command PC '
        'and full source/destination/count/channel arguments independently give source '
        'switch rows55/97;current paints completed in the preceding frame. All four '
        'complete98304-byte scanline bitmaps and196608 total RGB pixels are predicted '
        'exactly,without pixel masks,retiming or fitted boundaries. Four wrong-phase '
        'controls fail;15 host-prefix,8 mirror and12 scanline controls pass. Actual/native '
        'sheet reviewed. This closes the specific87/1446-pixel timing gap,not every '
        'animation/device. Initial short-range captures retained;frozen producers use '
        'process-local extended ranges. Second gender,embedded/controls/cards/comics/'
        'legacy/material/older checks/final acceptance remain open. All18 plaques '
        'incomplete and22 original scopes exact. V692 ROM/patch/registry/canonical/'
        'pointers unchanged; evidence on E,no guide promotion,commit or push. See '
        '[V693 checkpoint](filter_clock_v693_checkpoint.md).\n')
    for name in ('todo.md', 'translation_progress.md', 'known_issues.md', 'release_build.md'):
        path = Path('docs') / name
        text = path.read_text(encoding='utf-8')
        assert heading not in text
        path.write_text(text.rstrip() + '\n\n' + heading + '\n\n' + addition, encoding='utf-8')
        copy(path, ARCHIVE / 'docs' / name)
    for path in (*map(Path, SOURCES), DOC):
        copy(path, ARCHIVE / 'sources' / path)
    for name in ('MMU.cpp', 'MMU.h', 'GPU.cpp', 'GPU.h', 'NDSSystem.cpp', 'saves.cpp', 'armcpu.h'):
        copy(SOURCE / name, ARCHIVE / 'core_source' / name)
    for path in BASE.rglob('*'):
        if path.is_file():
            copy(path, ARCHIVE / 'analysis' / path.relative_to(BASE))
    external = {}
    for folder in CAP.glob('filter_clock_v693_*'):
        for path in folder.rglob('*'):
            if path.is_file():
                external[str(path)] = sha(path.read_bytes())
    # Retain the whole unobserved baselines used by the final verifier.
    for case in ('source_full', 'hodram_full'):
        folder = CAP / ('navigator_filter_v692_' + case)
        rp = folder / 'capture_report.json'
        report = read(rp)
        for path in (rp, folder / 'final_arm9_ram.bin', *(Path(r['path']) for r in report['frames_captured'])):
            external[str(path)] = sha(path.read_bytes())
    save(ARCHIVE / 'provenance.json', {'scripts': {p: sha(Path(p).read_bytes()) for p in SOURCES},
        'files': {str(p.relative_to(ARCHIVE)): sha(p.read_bytes()) for p in ARCHIVE.rglob('*')
                  if p.is_file() and p.name != 'provenance.json'},
        'external_E_drive_evidence': external, 'no_guide_promotion_or_new_ROM': True, 'full_goal_complete': False})
    print('V693 original clock/DMA proof and unchanged full audit scope recorded on E.', flush=True)


if __name__ == '__main__':
    main()
