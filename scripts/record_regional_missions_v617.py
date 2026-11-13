"""Archive verified regional mission evidence while preserving historical audit scope."""

from pathlib import Path

from dk4tool.patch.grand_race_menu_release import sha
from scripts.record_regional_ui_v616 import checked_copy
from scripts.verify_regional_missions_v617 import CAP, ROM, ROOT
from scripts.verify_village_wrap_v608 import read, save

DOC = Path('docs/regional_missions_v617_checkpoint.md')
ARCHIVE = Path('E:/Rota Nova translations/Screenshots/Test fixtures/V617 Regional missions')
KEY = 'actual_all4_regional_orders_missions_contract_branches_and_financial_display_v617'


def main():
    proof_path = ROOT / 'release_proof.json'
    proof = read(proof_path)
    assert proof['candidate_sha256'] == sha(ROM.read_bytes())
    assert proof['script_sha256'] == sha(Path('scripts/verify_regional_missions_v617.py').read_bytes())
    assert len(proof['four_complete_assignment_confirmations']) == len(proof['four_complete_mission_displays']) == 4
    assert len(proof['five_actual_instruction_contract_war_notices']) == 5
    ARCHIVE.mkdir(parents=True, exist_ok=True)
    files = [DOC, proof_path, ROOT / 'native_guarded_assignment_proof.json', ROOT / 'financial_fixture_source_proof.json',
             ROOT / 'patch_proof.json', ROOT / 'preservation_proof.json', ROOT / 'static_combined_proof.json',
             ROOT / 'observed_V616_assignment_defect.json', ROOT / 'original_caller_return_correction.json',
             ROOT / 'original_rejection_input_handling_note.json', ROOT / 'actual_existing_war_contract_census.json',
             ROOT / 'complete_V616_control_inputs.json', ROOT / 'ordinary_market_inputs.json', ROOT / 'build.log',
             ROM.with_suffix('.manifest.json'), Path('translations/regional_assignment_wrap_v1.json'),
             Path('translations/regional_fleet_ordinal_label_v1.json'),
             Path('work/analysis/regional_fleet_v615/formed_fixture_manifest.json'),
             Path('dk4tool/patch/regional_assignment_wrap.py'), Path('dk4tool/patch/regional_fleet_ordinal_label.py'),
             Path('scripts/prepare_regional_missions_v617.py'), Path('scripts/probe_regional_missions_v617.py'),
             Path('scripts/native_regional_finance_v617.py'), Path('scripts/run_regional_missions_v617.py'),
             Path('scripts/verify_regional_missions_v617.py'), Path(__file__)]
    for source in files:
        checked_copy(source, ARCHIVE / source.name)
    actual_frames = {39400}
    for key in ('four_complete_assignment_confirmations', 'four_complete_mission_displays',
                'five_actual_instruction_contract_war_notices'):
        actual_frames.update(row['frame'] for row in proof[key])
    screenshots = []
    for receipt in proof['reports']:
        path = Path(receipt['path'])
        assert sha(path.read_bytes()) == receipt['sha256']
        run = read(path)
        context = path.parent.name.removeprefix('regional_missions_v617_')
        checked_copy(path, ARCHIVE / (context + '_capture_report.json'))
        shots = {row['frame']: row for row in run['frames_captured']}
        for frame in sorted(actual_frames if context == 'actual' else shots):
            row = shots[frame]
            target = ARCHIVE / f'{context}_{frame:06d}_UNMODIFIED_NATIVE.png'
            checked_copy(row['path'], target)
            screenshots.append({'path': str(target), 'frame': frame, 'sha256': row['PNG_sha256'],
                                'ROM_sha256': run['ROM_sha256'], 'context': context,
                                'formed_test_save_used': context == 'actual',
                                'synthetic_financial_display_active': context == 'actual' and frame > 37800,
                                'unmodified_capture': True})
    for name in ('navigation_command_journal.json',):
        checked_copy(CAP / 'regional_missions_v617_actual' / name, ARCHIVE / name)
    failed_report_path = CAP / 'regional_missions_v617/capture_report.json'
    failed_report = read(failed_report_path)
    failed_row = next(r for r in failed_report['frames_captured'] if r['frame'] == 10200)
    failed = Path(failed_row['path'])
    assert sha(failed.read_bytes()) == failed_row['PNG_sha256']
    assert failed_report['ROM_sha256'] == '6432df058b2782bf764886fc717dada1177aabe39490744287073922c78ae236'
    checked_copy(failed_report_path, ARCHIVE / 'V616_failed_control_capture_report.json')
    checked_copy(failed, ARCHIVE / 'V616_FAILED_DROPPED_INITIAL_010200.png')
    save(ARCHIVE / 'provenance.json', {'candidate': str(ROM), 'candidate_sha256': proof['candidate_sha256'],
         'screenshots': screenshots, 'publication_approved': False, 'full_goal_complete': False,
         'financial_values_are_isolated_display_fixtures_not_monthly_earnings': True,
         'V616_failed_control_sha256': sha(failed.read_bytes()),
         'files': {p.name: sha(p.read_bytes()) for p in ARCHIVE.iterdir() if p.is_file() and p.name != 'provenance.json'}})
    entry = {'documentation': str(DOC), 'proof': str(proof_path), 'proof_sha256': sha(proof_path.read_bytes()),
             'candidate': str(ROM), 'candidate_sha256': proof['candidate_sha256'], 'profile': proof['profile'],
             'patch_sha256': proof['patch_sha256'], 'status': 'experimental_actual_mission_and_financial_display_variants_verified',
             'all4_complete_confirmations_and_mission_descriptions_native_verified': True,
             'actual_native_notices128_131_132_133_134_complete': True,
             'nonzero_financial_display_including_unsigned_maximum_verified': True,
             'actual_monthly_or_earned_financial_progression_verified': False,
             'full_role_native5_background_foreground_and_original_CP932_shadow_verified': True,
             'all5_source_framed_regional_plaques_verified_complete_native_pixels': 16608,
             'all3668_native_IDs_11_other_callers_and112_field_variants_pass': True,
             'ordinary19_no_save_no_fixture_screens_exact_V616': True,
             'all470_batches114_layers921_graphics57_embedded_extents_and_exact_patch_retained': True,
             'all18_original_plaques_incomplete_all22_historical_objects_exact': True,
             'V610_verified_pointers_retained': True, 'archive': str(ARCHIVE),
             'unmodified_V617_screenshots': len(screenshots), 'full_goal_complete': False, 'canonical_promoted': False}
    frozen = read('work/analysis/confirm_material_v572/audit_scope_before.json')
    for name, scope in frozen.items():
        path = Path('translations') / name
        data = read(path)
        assert data.get('historical_pending_items_retained') == scope['historical_pending_items_retained']
        assert data.get('plaque_style_v247', {}).get('ongoing_plaque_inventory') == scope['ongoing_plaque_inventory']
        pointers = {k: v for k, v in data.items() if k in ('candidate', 'candidate_sha256', 'latest_candidate',
                    'latest_candidate_sha256', 'current_verified_release_candidate', 'current_verified_release_candidate_sha256',
                    'latest_graphics_preservation')}
        data[KEY] = entry
        data['latest_compiled_experimental_candidate_with_inherited_native_gap'] = {
            'candidate': str(ROM), 'sha256': proof['candidate_sha256'], 'profile': proof['profile'],
            'regional_fleet_native_context_still_open': False,
            'regional_policy_confirmation_war_contract_and_financial_display_variants_still_open': False,
            'actual_monthly_earnings_or_progression_verified': False,
            'full_role_native5_composition_verified': True,
            'broader_graphics_gates_remain_open': True}
        data['current_goal_turn_classification'] = 'progress'
        save(path, data)
        now = read(path)
        assert all(now[k] == v for k, v in pointers.items())
        assert now.get('historical_pending_items_retained') == scope['historical_pending_items_retained']
        assert now.get('plaque_style_v247', {}).get('ongoing_plaque_inventory') == scope['ongoing_plaque_inventory']
    heading = '## V617: complete regional order guards and actual mission/financial variants'
    text = '''

V616's actual assignment lost Stockholm's initial S after a bare newline. V617
guards both original newlines only in the original assignment caller after macro
expansion. All3668 IDs,11 other direct callers,112 field variants and5 malformed
controls pass. The source-specific ordinal now reads Fleet 2 Admiral; proper
fleet names remain unchanged. No pool/cache/section/startup/arena growth occurs.

Actual original controls verify all4 complete three-line confirmations,all4
mission labels/descriptions and notices128/131/132/133/134. All5 plaques across4
states pass16608 complete native pixels. Existing war with faction5 permits the
Hamburg attack; no war/input logic is changed. Exactly12 isolated finance bytes
test complete9/10-digit values including4294967295; all480 digit ink points pass.
These are display fixtures,not monthly earnings or earned progression. The role
foreground and all1152 native5 background/foreground/shadow pixels pass in each
of4 mission states. Original paletted ASCII/CP932 rendering,source colour table
and its shadow routine reproduce all18 formerly unexplained digit-shadow pixels.

Both emulator runs end normally. All19 ordinary no-save/no-fixture New Game/Market
screens match V616. Full470/114 integration,all921/57 preservation and exact clean
patch reconstruction pass. The ROM,patch,33 unmodified V617 screenshots,failed
V616 control,reports,schedules and provenance are on E. All18 original plaques
remain incomplete,all22 historical objects exact,V610 verified pointers/canonical
unchanged. Broader miniature/Confirm,village-card,comic,legacy,movie,material and
gameplay gates remain. Goal active. See [V617 checkpoint](regional_missions_v617_checkpoint.md).
'''
    for name in ('todo', 'translation_progress', 'known_issues', 'plaque_background_texture_defect', 'release_build'):
        path = Path('docs') / (name + '.md')
        content = path.read_text(encoding='utf-8')
        if heading in content:
            before, old_entry = content.split(heading, 1)
            assert '\n## ' not in old_entry
            content = before.rstrip()
        path.write_text(content.rstrip() + '\n\n' + heading + '\n' + text, encoding='utf-8')
    print(f'Archived{len(screenshots)} unmodified V617 captures plus failed V616 control;3 audits and progress updated;18/22 scopes exact;goal active.')


if __name__ == '__main__':
    main()
