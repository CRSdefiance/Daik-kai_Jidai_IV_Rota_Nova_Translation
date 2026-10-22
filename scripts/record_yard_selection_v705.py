"""Retain ordinary Yard source selections and queue the real Refit layout defect."""

from pathlib import Path

from dk4tool.patch.grand_race_menu_release import sha
from scripts.record_memory_streams_v682 import copy
from scripts.run_room_gender_v694 import CAP
from scripts.run_yard_selection_v705 import ROOT
from scripts.verify_village_wrap_v608 import read, save

DOC = Path('docs/yard_selection_v705_checkpoint.md')
ARCHIVE = Path('E:/Rota Nova translations/Screenshots/Test fixtures/V705 Yard selection and Refit findings')
KEY = 'ordinary_five_ship_Yard_Sell_Refit275702_paints59_whole_pairs_five_wrap_defects30_help_IDs_v705'
SOURCES = ('scripts/run_yard_selection_v705.py', 'scripts/verify_yard_selection_v705.py',
    'scripts/record_yard_selection_v705.py', 'scripts/verify_yard_archive_v705.py',
    'scripts/observe_graphic_paints_v669.py', 'scripts/inspect_graphic_paints_v669.py',
    'scripts/verify_graphic_paints_v669.py', 'scripts/verify_full_fleet_battle_v652.py',
    'scripts/verify_full_fleet_victory_v654.py')


def main():
    proof_path = ROOT / 'proof.json'
    proof, pre = read(proof_path), read(ROOT / 'preflight.json')
    assert proof['verifier_sha256'] == sha(Path('scripts/verify_yard_selection_v705.py').read_bytes())
    assert proof['observer_baseline_whole_RGB_pairs'] == proof['observer_baseline_full4MiB_capture_RAM_pairs'] == 59
    assert len(proof['five_complete_source_bound_Refit_body_wrap_defects']) == 5
    assert len(proof['30_source_help_IDs_queued_for_shared_layout_fix']) == 30
    for path, digest in pre['release_hashes'].items():
        assert sha(Path(path).read_bytes()) == digest
    assert sha(Path(pre['donor']).read_bytes()) == pre['donor_sha256']
    save(ROOT / 'visual_review.json', {'pilot_complete24_panel_source_context_sheet_inspected': True,
        'review_sheet': str(ROOT / 'pilot_review_sheet.png'),
        'Sell_four_support_rows_Remodel_five_rows_Refit_and_final_cancel_prompt_reviewed': True,
        'five_source_bound_split_word_help_defects_remain_unfixed': True,
        'final_cancel_confirmation_not_completed_and_no_guide_promotion': True})
    entry = {'documentation': str(DOC), 'proof': str(proof_path), 'proof_sha256': sha(proof_path.read_bytes()),
        'candidate': pre['candidate'], 'candidate_sha256': pre['candidate_sha256'],
        'three_terminal19700_frame_ordinary_cold_boots_no_savestate_or_gameplay_fixture': True,
        'all59_whole_RGB_RAM_pairs59_pilot_RGB_pairs_and_last_emulated_frame_RAM_exact': True,
        '275702_original_paint_entries85072_whole_Frame6132_whole_Marker_and13_host_controls': True,
        'selected_Frame_footprints_do_not_use_miniatures_Confirm_not_selected_no_global_nonuse': True,
        'six_typed_fleet_and_funds_states_no_ship_sold_or_funds_change': True,
        'five_actual_Refit_split_word_body_planes_complete_source_font_masks_and_live_strings_bound': True,
        'source_stable30_help_message_IDs_queued_for_shared_natural_word_wrap_fix': str(ROOT / 'refit_repair_queue.json'),
        'not_all30_contexts_tested_or_fixed_no_new_production_fix': True,
        'final_cancel_prompt_not_completed_cancel_save_or_earned_progress_claim': True,
        'all18_plaques_incomplete22_historical_objects_exact': True,
        'production_ROM_graphics_patch_manifest_registry_canonical_donor_release_pointers_unchanged': True,
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
    heading = '## V705: ordinary Yard selection and five source-bound Refit wrapping defects'
    text = (
        'Three terminal19700-frame ordinary cold boots use the isolated five-ship '
        'Copenhagen save,no gameplay fixtures. All59 observed/baseline whole RGB '
        'and4MiB RAM pairs,59 pilot RGB pairs and exact last-frame RAM match. '
        '275702 original drawing entries bind85072 complete Frame and6132 Marker '
        'files;all guards pass,13 native host controls pass and the private handler '
        'restores. These Sell/Remodel/Refit paths select no miniature footprint or '
        'Confirm through the three traced primitives;normal parents remain open. '
        'Six native fleet/fund states retain all5 ships and25975 funds. Final '
        'screen is Cancel remodeling confirmation,not completed cancellation/save. '
        'Five complete Refit body font planes and actual live strings prove split '
        'tailwinds/damaged/buyouts/ailments/fatigue words and legacy indentation. '
        'Stable native IDs identify30 help entries for a shared source-reviewed '
        'word-wrap correction;not all30 contexts tested or fixed. Initial EOF,'
        'missing-export/path/fixed-allocation verifier assumptions are retained '
        'and corrected without replaying successful producers. Full24-panel '
        'context sheet reviewed. V692/graphics/patch/registry/pointers/donor '
        'unchanged;all18 plaques incomplete,22 historical scopes exact,broader '
        'graphics/older checks/acceptance open. Evidence archived on E,no guide '
        'promotion/commit/push;full goal active. See '
        '[V705 checkpoint](yard_selection_v705_checkpoint.md).\n')
    for name in ('todo.md', 'translation_progress.md', 'known_issues.md', 'release_build.md'):
        path = Path('docs') / name
        content = path.read_text(encoding='utf-8')
        assert heading not in content
        path.write_text(content.rstrip() + '\n\n' + heading + '\n\n' + text, encoding='utf-8')
        copy(path, ARCHIVE / 'docs' / name)
    for path in (*map(Path, SOURCES), DOC):
        copy(path, ARCHIVE / 'sources' / path)
    for path in ROOT.rglob('*'):
        if path.is_file():
            copy(path, ARCHIVE / 'analysis' / path.relative_to(ROOT))
    external = {}
    for folder in CAP.glob('yard_selection_v705_*'):
        for path in folder.rglob('*'):
            if path.is_file():
                external[str(path)] = sha(path.read_bytes())
    save(ARCHIVE / 'provenance.json', {'scripts': {p: sha(Path(p).read_bytes()) for p in SOURCES},
        'files': {str(p.relative_to(ARCHIVE)): sha(p.read_bytes()) for p in ARCHIVE.rglob('*')
            if p.is_file() and p.name != 'provenance.json'},
        'external_E_drive_evidence': external,
        'actual_ordinary_Refit_word_wrap_defects_not_yet_fixed': True, 'full_goal_complete': False})
    print('V705 source selections and five actual Refit wrap defects recorded; 30-message correction remains open.', flush=True)


if __name__ == '__main__':
    main()
