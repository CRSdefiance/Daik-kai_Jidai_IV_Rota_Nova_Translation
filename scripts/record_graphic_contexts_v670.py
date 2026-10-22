"""Retain wider source-selection evidence without closing unresolved contexts."""

from pathlib import Path

from dk4tool.patch.grand_race_menu_release import sha
from scripts.prepare_graphic_contexts_v670 import ROOT
from scripts.record_regional_ui_v616 import checked_copy
from scripts.verify_village_wrap_v608 import read, save

ARCHIVE = Path('E:/Rota Nova translations/Screenshots/Test fixtures/V670 Crew and race image calls')
DOC = Path('docs/graphic_contexts_v670_checkpoint.md')
KEY = 'ordinary_crew_and_isolated_race337252_image_entries100_current_retained_baseline_pairs_v670'
SCRIPTS = ('scripts/prepare_graphic_contexts_v670.py', 'scripts/run_graphic_contexts_v670.py',
           'scripts/verify_graphic_contexts_v670.py', 'scripts/record_graphic_contexts_v670.py',
           'scripts/observe_graphic_paints_v669.py', 'scripts/verify_graphic_paints_v669.py',
           'scripts/observe_resource_dispatch_v668.py', 'scripts/inspect_committed_gpu_v646.py')


def copy(source, destination):
    destination = Path(destination)
    destination.parent.mkdir(parents=True, exist_ok=True)
    checked_copy(source, destination)


def main():
    pp = ROOT / 'proof.json'
    proof, pre = read(pp), read(ROOT / 'preflight.json')
    assert proof['verifier_sha256'] == sha(Path('scripts/verify_graphic_contexts_v670.py').read_bytes())
    assert proof['primitive_entries'] == 337252 and len(proof['reports']) == 4
    assert proof['observer_baseline_whole_two_screen_pairs'] == 50
    assert proof['retained_V657_V661_whole_two_screen_pairs'] == 50
    assert proof['all_original_fixture_events_exact_between_observed_and_baseline_and_restored']
    for path, digest in pre['release_hashes'].items():
        assert sha(Path(path).read_bytes()) == digest
    frozen = read('work/analysis/confirm_material_v572/audit_scope_before.json')
    for name, scope in frozen.items():
        data = read(Path('translations') / name)
        assert all(data[k] == v for k, v in pre['all_original_audits_before'][name].items()
                   if k != 'current_goal_turn_classification')
        assert data.get('historical_pending_items_retained') == scope['historical_pending_items_retained']
        assert data.get('plaque_style_v247', {}).get('ongoing_plaque_inventory') == scope['ongoing_plaque_inventory']
    entry = {'documentation': str(DOC), 'proof': str(pp), 'proof_sha256': sha(pp.read_bytes()),
        'candidate': pre['candidate'], 'candidate_sha256': pre['candidate_sha256'],
        'status': 'two_additional_UI_schedules_verified_six_control_contexts_still_open',
        'four_terminal_cold_boots_observed_and_baseline_no_savestate': True,
        'all50_current_and50_retained_whole_two_screen_pairs_exact': True,
        'ordinary_crew_no_live_gameplay_fixture': True,
        'race_fixture_exact_original_V661_receive_fields_and_restoration': True,
        'race_wireless_earned_unlock_or_outcome_verified': False,
        'all337252_original_primitive_entries_guarded': True,
        'whole_Frame47662_and_Marker2530_entries': True,
        'five_miniature_cells_and_Confirm_not_selected_in_these_schedules_not_global_nonuse': True,
        'embedded_aliases_other_primitives_other_contexts_and_six_controls_open': True,
        'no_individual_paint_retirement_or_pixel_per_call_credit': True,
        'all18_plaques_incomplete22_historical_scopes_exact': True,
        'ROM_patch_registry_canonical_and_release_pointers_unchanged': True,
        'archive': str(ARCHIVE), 'full_goal_complete': False}
    for name in frozen:
        target = Path('translations') / name
        data = read(target)
        data[KEY], data['current_goal_turn_classification'] = entry, 'progress'
        save(target, data)
    heading = '## V670: crew and isolated race source-selection coverage'
    addition = ('Four cold boots of the unchanged V666 candidate verify ordinary crew allocation '
        'and the retained isolated Grand Race receive-ring UI. All50 current baseline and50 '
        'retained two-screen pairs match. The unchanged host observer records337252 guarded '
        'primitive entries, binding47662 complete Frame files and2530 Marker files. The race '
        'fixture validates every declared write and restores all fields; no wireless, earned '
        'unlock or outcome credit. These schedules select neither the five miniature Frame '
        'caption cells nor separate Confirm through the traced primitives. Embedded aliases, '
        'other paths and all six contexts remain open; no global non-use or individual paint '
        'completion inferred. All18 plaques remain incomplete and22 scopes exact. No ROM, '
        'patch, registry, pointer or guide change. See [V670 checkpoint](graphic_contexts_v670_checkpoint.md).\n')
    for name in ('todo.md', 'translation_progress.md', 'known_issues.md', 'release_build.md'):
        target = Path('docs') / name
        text = target.read_text(encoding='utf-8')
        if heading not in text:
            target.write_text(text.rstrip() + '\n\n' + heading + '\n\n' + addition, encoding='utf-8')
    ARCHIVE.mkdir(parents=True, exist_ok=True)
    for receipt in proof['reports']:
        folder = Path(receipt['path']).parent
        assert sha(Path(receipt['path']).read_bytes()) == receipt['sha256']
        for source in folder.rglob('*'):
            if source.is_file() and source.suffix.lower() in ('.json', '.png', '.bin'):
                copy(source, ARCHIVE / 'runs' / folder.name / source.relative_to(folder))
    for source in [DOC, *map(Path, SCRIPTS)]:
        copy(source, ARCHIVE / 'sources' / source.name)
    for source in ROOT.rglob('*'):
        if source.is_file():
            copy(source, ARCHIVE / 'analysis' / source.relative_to(ROOT))
    for name in frozen:
        copy(Path('translations') / name, ARCHIVE / 'audits' / name)
    for name in ('todo.md', 'translation_progress.md', 'known_issues.md', 'release_build.md'):
        copy(Path('docs') / name, ARCHIVE / 'docs' / name)
    save(ARCHIVE / 'provenance.json', {'candidate_sha256': pre['candidate_sha256'], 'reports': proof['reports'],
        'all_four_runs_terminal': True, 'source_scripts': {p: sha(Path(p).read_bytes()) for p in SCRIPTS},
        'files': {str(p.relative_to(ARCHIVE)): sha(p.read_bytes()) for p in ARCHIVE.rglob('*')
                  if p.is_file() and p.name != 'provenance.json'},
        'six_controls_and_full_graphics_goal_open': True, 'full_goal_complete': False})
    print('V670 four runs archived; three audits/four docs updated;18/22 scopes retained.', flush=True)


if __name__ == '__main__':
    main()
