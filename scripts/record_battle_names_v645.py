"""Archive bounded battle-name evidence while retaining the full graphics scope."""

from pathlib import Path

from dk4tool.patch.grand_race_menu_release import sha
from scripts.record_regional_ui_v616 import checked_copy
from scripts.verify_battle_names_v645 import CAP, ROOT
from scripts.verify_village_wrap_v608 import read, save

KEY = 'actual_original_duel_name_setup_frame_composition_and_complete_namefield_pixels_v645'
DOC = Path('docs/battle_names_v645_checkpoint.md')
ARCHIVE = Path('E:/Rota Nova translations/Screenshots/Test fixtures/V645 Duel nameplates')


def main():
    pp = ROOT / 'battle_name_proof.json'
    proof, pre = read(pp), read(ROOT / 'preflight.json')
    assert len(proof['cases']) == 2 and not proof['full_goal_complete']
    for path, digest in pre['release_hashes'].items():
        assert sha(Path(path).read_bytes()) == digest
    for path, digest in proof['scripts'].items():
        assert sha(Path(path).read_bytes()) == digest
    frozen = read('work/analysis/confirm_material_v572/audit_scope_before.json')
    for name, scope in frozen.items():
        current = read(Path('translations') / name)
        assert all(current[k] == v for k, v in pre['all_original_audits_before'][name].items()
                   if k not in (KEY, 'current_goal_turn_classification'))
        assert current.get('historical_pending_items_retained') == scope['historical_pending_items_retained']
        assert current.get('plaque_style_v247', {}).get('ongoing_plaque_inventory') == scope['ongoing_plaque_inventory']
    ARCHIVE.mkdir(parents=True, exist_ok=True)
    captures = ARCHIVE / 'Unmodified exploratory captures'
    captures.mkdir(exist_ok=True)
    report = read(proof['report'])
    copied = []
    for shot in report['frames_captured']:
        assert sha(Path(shot['path']).read_bytes()) == shot['PNG_sha256']
        destination = captures / Path(shot['path']).name
        checked_copy(shot['path'], destination)
        copied.append({'frame': shot['frame'], 'path': str(destination), 'PNG_sha256': shot['PNG_sha256']})
    assert len(copied) == 15 and len({s['frame'] for s in copied}) == 13
    sources = [DOC, pp, ROOT / 'preflight.json', ROOT / 'name_font_diagnostic.json',
        ROOT / 'duel_nameplate_8x.png', CAP / 'navigation_command_journal.json',
        Path(proof['report']), Path(__file__)] + [Path(p) for p in proof['scripts']]
    for source in sources:
        checked_copy(source, ARCHIVE / source.name)
    native_paths = []
    for case in proof['cases']:
        target = ARCHIVE / f"native_state_{case['frame']:06d}.json"
        checked_copy(case['native_state'], target)
        native_paths.append(str(target))
    save(ARCHIVE / 'provenance.json', {'candidate': proof['candidate'],
        'candidate_sha256': proof['candidate_sha256'], 'unmodified_captures': copied,
        'full_native_exports_and_RAM_remain_under_original_run_on_E': str(CAP),
        'copied_native_manifests': native_paths,
        'derived_not_gameplay': ['duel_nameplate_8x.png'],
        'source_donor_unchanged_authorized_recovery_proximity_only': True,
        'no_new_victory_earned_voyage_hardware_or_guide_candidate': True,
        'files': {str(p.relative_to(ARCHIVE)): sha(p.read_bytes())
                  for p in ARCHIVE.rglob('*') if p.is_file() and p.name != 'provenance.json'}})
    entry = {'documentation': str(DOC), 'proof': str(pp), 'proof_sha256': sha(pp.read_bytes()),
        'candidate': proof['candidate'], 'candidate_sha256': proof['candidate_sha256'],
        'actual_current_22001_frame_cold_boot_no_savestate': True,
        'single_bounded_own_ship_recovery_proximity_fixture_source_save_unchanged': True,
        'actual_original_Hodram_first_name_and_Speyer_surname_getters_and_setup': True,
        'each_6144_source_cells_and_all2304_actual_namefield_pixels_exact_in_two_frames': True,
        'original_frame_background_and_transparent_names_composed_over_poisoned_destinations': True,
        'full196608_byte_native_two_name_draw_result_and_ABI_exact': True,
        'all_first_final_glyph_deletions_rejected_and_four_y_not_v_pixels_correct': True,
        'Spever_visual_suspicion_rejected_no_spelling_or_font_change_needed': True,
        'fifteen_unmodified_PNG_records_thirteen_distinct_frames_no_new_guide_candidate': True,
        'miniature_Confirm_and_other_legacy_card_material_movie_acceptance_gates_open': True,
        'all18_original_plaques_incomplete_all22_historical_scopes_exact': True,
        'ROM_patch_registry_canonical_and_all_release_pointers_unchanged': True,
        'archive': str(ARCHIVE), 'full_goal_complete': False}
    for name in frozen:
        path = Path('translations') / name
        current = read(path)
        current[KEY] = entry
        current['current_goal_turn_classification'] = 'progress'
        save(path, current)
        assert all(read(path)[k] == v for k, v in pre['all_original_audits_before'][name].items()
                   if k not in (KEY, 'current_goal_turn_classification'))
    heading = '## V645: actual original duel nameplates and complete source composition'
    text = """
Current V640 cold boots to original encounter and Functions menu,then enters the
duel after one authorized own-ship recovery/proximity fixture;normal stop22001.
Original actual name setup/getters produce Hodram/Speyer,not Spever. Each6144
source cells and2304 complete actual namefield pixels pass in two same-frame
RAM/ITCM-bound cases. Original frame prefix resolves the whole cached Frame and
fully paints both fields over poison;dark-gray fill/bevels replace the rejected
flat-black model with no excluded pixels. Both complete native name draws pass
all196608 output bytes and ABI;four first/final deletions and all four y/v
distinguishing pixels pass per case.15 unmodified PNGs/13 sampled frames archived
on E,no guide candidate or new victory/playthrough claim. No ROM/patch/registry/
release-pointer change. All18 plaques remain incomplete and22 historical scopes
exact;miniature/Confirm,card/legacy/material/movie/acceptance gates remain open.
See [V645 checkpoint](battle_names_v645_checkpoint.md).
"""
    for name in ('todo.md', 'translation_progress.md', 'known_issues.md', 'release_build.md'):
        path = Path('docs') / name
        old = path.read_text(encoding='utf-8')
        if heading not in old:
            path.write_text(old.rstrip() + '\n\n' + heading + '\n\n' + text, encoding='utf-8')
    for path, digest in pre['release_hashes'].items():
        assert sha(Path(path).read_bytes()) == digest
    print('V645 evidence/progress archived; all original scope and release pointers retained.')


if __name__ == '__main__':
    main()
