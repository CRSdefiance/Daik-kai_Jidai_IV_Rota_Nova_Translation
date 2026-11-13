"""Archive the Narvik evidence without finalizing historical graphics requirements."""

from pathlib import Path

from dk4tool.patch.grand_race_menu_release import sha
from scripts.record_regional_ui_v616 import checked_copy
from scripts.verify_village_contexts_v618 import ROM, ROOT, RUN
from scripts.verify_village_wrap_v608 import read, save

DOC = Path('docs/village_contexts_v618_checkpoint.md')
ARCHIVE = Path('E:/Rota Nova translations/Screenshots/Test fixtures/V618 Narvik village')
KEY = 'original_Narvik_development_and_complete_long_specialty_context_v618'


def main():
    path = ROOT / 'release_proof.json'
    proof = read(path)
    assert proof['script_sha256'] == sha(Path('scripts/verify_village_contexts_v618.py').read_bytes())
    assert proof['candidate_sha256'] == sha(ROM.read_bytes())
    assert len(proof['all24_original_menu_filter_cases']) == 24
    assert len(proof['six_complete_actual_dialogue_boxes']) == 6
    assert sha(ROM.with_suffix('.xdelta').read_bytes()) == '7704724a6d57aa5c22ed20ab896e2e5b500da6bf53793d0c3b426a7573bb8343'
    ARCHIVE.mkdir(parents=True, exist_ok=True)
    files = [DOC, path, ROOT / 'actual_V617_RAM_all24_water_proof.json', ROOT / 'source_water_fixture_proof.json',
             ROOT / 'fixture_negative_controls.json', ROOT / 'original_menu_filter_cases.json',
             ROOT / 'rejected_setup_controls.json', ROOT / 'Narvik_development_observation.json',
             ROOT / 'sea_prefix_inputs.json', RUN / 'capture_report.json', RUN / 'navigation_command_journal.json',
             Path('scripts/native_village_contexts_v618.py'), Path('scripts/run_village_contexts_v618.py'),
             Path('scripts/verify_village_contexts_v618.py'), Path(__file__)]
    for source in files:
        checked_copy(source, ARCHIVE / source.name)
    report = read(RUN / 'capture_report.json')
    screenshots = []
    wanted = (5200, 5600, 6000, 6400, 7200, 7600, 8000, 8400, 8800, 9300,
              10000, 11800, 12200, 12600, 13000, 13400, 14100, 14500, 15300, 15700)
    shots = {r['frame']: r for r in report['frames_captured']}
    for frame in wanted:
        row = shots[frame]
        target = ARCHIVE / f'Narvik_{frame:06d}_UNMODIFIED_NATIVE.png'
        checked_copy(row['path'], target)
        screenshots.append({'frame': frame, 'path': str(target), 'sha256': row['PNG_sha256'],
                            'ROM_sha256': proof['candidate_sha256'], 'source_DSV_copy_used': True,
                            'isolated_location_fixture_active': frame > 5200, 'unmodified_capture': True,
                            'not_ordinary_long_distance_travel_or_guide_publication': True})
    save(ARCHIVE / 'provenance.json', {'candidate_sha256': proof['candidate_sha256'], 'screenshots': screenshots,
         'production_ROM_and_patch_unchanged': True, 'publication_approved': False, 'full_goal_complete': False,
         'files': {p.name: sha(p.read_bytes()) for p in ARCHIVE.iterdir() if p.is_file() and p.name != 'provenance.json'}})
    entry = {'documentation': str(DOC), 'proof': str(path), 'proof_sha256': sha(path.read_bytes()),
             'candidate': str(ROM), 'candidate_sha256': proof['candidate_sha256'],
             'status': 'source_fixtures_and_actual_Narvik_context_verified_no_ROM_change',
             'all24_terrain_distance_and_original_menu_filter_cases_pass': True,
             'five_invalid_fixture_controls_reject_before_mutation': True,
             'original_Svartisen_keyboard_acceptance_development_and_return_verified': True,
             'actual_six_complete_dialogues_and_both_menu_variants_pass': True,
             'complete_Black_Glacier_Sword_215_pixels_at_actual_right_boundary': True,
             'no_new_specialty_clipping_defect_or_ROM_repair_needed': True,
             'all8_village_card_ordinary_contexts_remain_open': True,
             'all18_original_plaques_incomplete_all22_historical_objects_exact': True,
             'archive': str(ARCHIVE), 'unmodified_screenshots': len(screenshots),
             'full_goal_complete': False, 'canonical_promoted': False}
    frozen = read('work/analysis/confirm_material_v572/audit_scope_before.json')
    for name, scope in frozen.items():
        audit = Path('translations') / name
        data = read(audit)
        assert data.get('historical_pending_items_retained') == scope['historical_pending_items_retained']
        assert data.get('plaque_style_v247', {}).get('ongoing_plaque_inventory') == scope['ongoing_plaque_inventory']
        pointers = {k: v for k, v in data.items() if k in ('candidate', 'candidate_sha256', 'latest_candidate',
                    'latest_candidate_sha256', 'current_verified_release_candidate', 'current_verified_release_candidate_sha256',
                    'latest_graphics_preservation', 'latest_compiled_experimental_candidate_with_inherited_native_gap')}
        data[KEY] = entry
        data['current_goal_turn_classification'] = 'progress'
        save(audit, data)
        now = read(audit)
        assert all(now[k] == v for k, v in pointers.items())
        assert now.get('historical_pending_items_retained') == scope['historical_pending_items_retained']
        assert now.get('plaque_style_v247', {}).get('ongoing_plaque_inventory') == scope['ongoing_plaque_inventory']
    heading = '## V618 research: original Narvik village development and complete long specialty'
    text = '''

Unchanged V617 gains24 source-terrain/distance/8-coordinate-byte fixture cases
and24 original menu-filter replays. Actual normal controls within one location
fixture discover Narvik,enter Svartisen through the original keyboard,change
town105 development0 to2,and depart/return to the developed port. Six whole
dialogue boxes and both5/4-row menus pass complete native-font masks. Developed
Narvik supplies Black Glacier Sword through original stock logic;all215 ink
points and96x12 foreground positions pass,including final d at the right edge.
An initial visual clipping suspicion is disproved;V502's existing renderer works.

Five unsafe fixture controls reject. The PTY/omitted-donor setup failures are
retained without finalized-run credit. Wanganui's old helper page50 overrun is
corrected with the original2500-tile horizontal boundary in the isolated fixture;
no production code changes. All8 ordinary village-card contexts remain open.
Neither ROM,patch,registry,source DSV nor canonical changes. Twenty unmodified
test-fixture screenshots,reports,journal and hashes are on E. All18 original
plaques remain incomplete and22 historical scopes exact. Full graphics goal
active;broader miniature/Confirm,legacy,comic,movie/material/gameplay work remains.
See [V618 Narvik checkpoint](village_contexts_v618_checkpoint.md).
'''
    for name in ('todo', 'translation_progress', 'known_issues', 'release_build'):
        target = Path('docs') / (name + '.md')
        content = target.read_text(encoding='utf-8')
        if heading not in content:
            target.write_text(content.rstrip() + '\n\n' + heading + '\n' + text, encoding='utf-8')
    print('Archived20 unmodified Narvik captures;all3 audits and progress updated;V617 unchanged;18/22 scopes retained;goal active.')


if __name__ == '__main__':
    main()
