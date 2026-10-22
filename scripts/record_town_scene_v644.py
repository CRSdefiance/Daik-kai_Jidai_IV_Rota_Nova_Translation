"""Archive complete observed Town composition without narrowing the graphics goal."""

from pathlib import Path

from dk4tool.patch.grand_race_menu_release import sha
from scripts.record_regional_ui_v616 import checked_copy
from scripts.research_town_scene_v644 import ROOT
from scripts.verify_village_wrap_v608 import read, save

DOC = Path('docs/town_scene_composition_v644_checkpoint.md')
ARCHIVE = Path('E:/Rota Nova translations/Screenshots/Test fixtures/V644 Complete Town composition')
KEY = 'complete_actual_Town_98304_pixel_composition_original_iterator_VRAM_aliases_and_DTCM_v644'


def main():
    pp = ROOT / 'complete_town_scene_proof.json'
    proof, pre = read(pp), read(ROOT / 'preflight.json')
    assert proof['candidate_sha256'] == pre['candidate_sha256']
    assert proof['all98304_full16bit_output_words_exact_physical_VRAM_including_bit15']
    assert proof['all98304_full_RGB888_capture_pixels_exact_via_original_RGB565_expansion']
    assert len(proof['four_leading_and_final_footer_glyph_deletions_rejected']) == 4
    assert not proof['full_goal_complete'] and not proof['new_emulator_run_claimed']
    for p, digest in proof['scripts'].items():
        assert sha(Path(p).read_bytes()) == digest
    for p, digest in pre['release_hashes'].items():
        assert sha(Path(p).read_bytes()) == digest
    frozen = read('work/analysis/confirm_material_v572/audit_scope_before.json')
    for name, scope in frozen.items():
        data = read(Path('translations') / name)
        assert all(data[k] == v for k, v in pre['all_original_audits_before'][name].items()
                   if k not in (KEY, 'current_goal_turn_classification'))
        assert data.get('historical_pending_items_retained') == scope['historical_pending_items_retained']
        assert data.get('plaque_style_v247', {}).get('ongoing_plaque_inventory') == scope['ongoing_plaque_inventory']
    ARCHIVE.mkdir(parents=True, exist_ok=True)
    sources = ARCHIVE / 'Original core source'
    sources.mkdir(parents=True, exist_ok=True)
    for p, digest in pre['source_files'].items():
        source = Path(p)
        assert sha(source.read_bytes()) == digest
        checked_copy(source, sources / source.name)
    copying = Path(next(iter(pre['source_files']))).parent.parent / 'COPYING'
    if copying.exists():
        checked_copy(copying, sources / 'COPYING')
    files = [DOC, pp, ROOT / 'preflight.json', ROOT / 'visual_review.json',
        ROOT / 'original_iterator_diagnostic.json', ROOT / 'iterator_and_footer_diagnostic.json',
        ROOT / 'DTCM_restored_town_diagnostic.json', ROOT / 'full_iterator_write_domains.json',
        ROOT / 'footer_source_diagnostic.json', ROOT / 'initial_iterator_probe_script.py',
        ROOT / 'pre_DTCM_footer_probe_script.py', Path(__file__),
        Path('work/analysis/village_backgrounds_v643/font_chain_failure_detail.json'),
        Path(proof['reused_actual_report']), Path(proof['read_only_native_state']['path'])]
    files.extend(Path(p) for p in proof['scripts'])
    replay = Path(proof['complete_native_source_replay_RGB8_PNG'])
    words = Path(proof['native_surface_words'])
    assert sha(replay.read_bytes()) == proof['replay_PNG_sha256']
    assert sha(words.read_bytes()) == proof['native_surface_words_sha256']
    files.extend((replay, words))
    for source in files:
        checked_copy(source, ARCHIVE / source.name)
    shot = proof['reused_frame']
    target = ARCHIVE / 'REUSED_V643_CURRENT_V640_frame015700_UNMODIFIED_NATIVE.png'
    checked_copy(shot['path'], target)
    save(ARCHIVE / 'provenance.json', {'candidate_sha256': proof['candidate_sha256'],
        'reused_unmodified_V643_capture': {'path': str(target), 'sha256': shot['PNG_sha256'],
            'source_report': proof['reused_actual_report'], 'source_report_sha256': proof['reused_actual_report_sha256']},
        'derived_reconstruction_labeled_separately': str(ARCHIVE / replay.name),
        'no_new_emulator_run_or_guide_candidate': True, 'full_goal_complete': False,
        'all_complete_original_RAM_VRAM_DTCM_ITCM_exports_remain_on_E': True,
        'files': {str(p.relative_to(ARCHIVE)): sha(p.read_bytes()) for p in ARCHIVE.rglob('*')
                  if p.is_file() and p.name != 'provenance.json'}})
    execution = proof['original_iterator_and_footer_execution']
    entry = {'documentation': str(DOC), 'proof': str(pp), 'proof_sha256': sha(pp.read_bytes()),
        'candidate': proof['candidate'], 'candidate_sha256': proof['candidate_sha256'],
        'reuses_actual_V643_current_capture_not_a_new_emulator_run': True,
        'original_iterator_filters18_nodes_runs17_painters_then_original_shared_footer': True,
        'all98304_pixels_rebuilt_from_poisoned_surfaces_exact_full16bit_physical_VRAM_and_RGB888_capture': True,
        'actual_source_VRAM_reads': len(execution['VRAM_reads']),
        'all_VRAM_reads_offscreen_font_cache_no_VRAM_writes_no_visible_output_inputs': True,
        'captured_DTCM_actual_footer_bitmap720_active_cells140_ink_and_blank_cells_verified': True,
        'four_leading_and_final_Menu_Select_glyph_deletion_controls_rejected': True,
        'absent_DTCM_reproduces140_missing_ink_pixels_visible_output_erasure_has_no_effect': True,
        'all_executed_words_match_captured_main_RAM_or_ITCM_fragment_ABI_and_guards_pass': True,
        'SDK_frame_setup_GPU_timing_other_scenes_and_hardware_not_inferred': True,
        'all18_original_plaques_incomplete_all22_historical_scopes_exact': True,
        'ordinary_card_miniature_Confirm_legacy_and_wider_graphics_gates_open': True,
        'ROM_patch_registry_canonical_and_all_release_pointers_unchanged': True,
        'archive': str(ARCHIVE), 'full_goal_complete': False, 'canonical_promoted': False}
    for name in frozen:
        path = Path('translations') / name
        data = read(path)
        data[KEY] = entry
        data['current_goal_turn_classification'] = 'progress'
        save(path, data)
        assert all(read(path)[k] == v for k, v in pre['all_original_audits_before'][name].items()
                   if k not in (KEY, 'current_goal_turn_classification'))
    heading = '## V644: complete actual Town composition from VRAM aliases and DTCM'
    addition = """

Reuses the hash-bound actual current V640 Narvik capture at15700,not a new run.
Pinned core bank controls supply the real offscreen font cache;captured DTCM
supplies the shared footer bitmap. Original iterator filters18 nodes,executes17
painters and the original footer,fully assigning both poisoned destination planes.
All98304 full16bit words match physical VRAM including bit15;all98304 RGB888 pixels
match the capture.5688 VRAM reads exclude both visible outputs,and erasing those
outputs leaves reconstruction unchanged. Native code/fragment ABI/guards pass;
no source,getter,painter bridge or VRAM write. Independent720 active footer cells
include140 complete Menu/Select strokes;four first/final deletions are rejected.
Missing DTCM reproduces exactly140 missing strokes;earlier failures are retained.
Original inactive cache tail172 nonzero cells stays untouched and undrawn.
Proof,exact-color reconstruction and one clearly reused screenshot are archived
on E;no new guide candidate. No ROM/patch/registry/pointer change. All18 plaques
remain incomplete and22 scopes exact;other native/card/legacy/material/acceptance
gates remain open. See [V644 checkpoint](town_scene_composition_v644_checkpoint.md).
"""
    for name in ('todo.md', 'translation_progress.md', 'known_issues.md', 'release_build.md'):
        path = Path('docs') / name
        text = path.read_text(encoding='utf-8')
        if heading not in text:
            path.write_text(text.rstrip() + '\n\n' + heading + '\n' + addition, encoding='utf-8')
    for p, digest in pre['release_hashes'].items():
        assert sha(Path(p).read_bytes()) == digest
    print('Archived complete Town native composition/retained diagnostics and reused capture;3 additive audits;all18/22 scopes and release artifacts preserved.')


if __name__ == '__main__':
    main()
