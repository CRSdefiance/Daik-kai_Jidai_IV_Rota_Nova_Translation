"""Archive ordinary recruitment evidence while preserving the full graphics audit."""

from pathlib import Path

from dk4tool.patch.grand_race_menu_release import sha
from scripts.record_regional_ui_v616 import checked_copy
from scripts.verify_tavern_recruitment_release_v627 import CAP, ROM, ROOT
from scripts.verify_village_wrap_v608 import read, save

DOC = Path('docs/tavern_recruitment_v627_checkpoint.md')
ARCHIVE = Path('E:/Rota Nova translations/Screenshots/Test fixtures/V627 Complete recruitment voices')
KEY = 'actual_ordinary_recruitment_and_all7_complete_voice_calls_v627'


def main():
    proof_path = ROOT / 'release_proof.json'
    proof = read(proof_path)
    native = read(ROOT / 'native_proof.json')
    assert proof['candidate_sha256'] == sha(ROM.read_bytes()) == native['candidate_sha256']
    assert proof['script_sha256'] == sha(Path('scripts/verify_tavern_recruitment_release_v627.py').read_bytes())
    assert native['script_sha256'] == sha(Path('scripts/verify_tavern_recruitment_native_v627.py').read_bytes())
    assert len(native['every_changed_entry_hot_and_cold_cache_copy']) == 166
    assert len(native['all14_voice_parent_whole_native_font_planes']) == 14
    ARCHIVE.mkdir(parents=True, exist_ok=True)
    files = [DOC, ROM.with_suffix('.manifest.json'), Path('translations/tavern_recruitment_manuscript_v1.json'),
             Path('translations/tavern_recruitment_v1.json'), Path('dk4tool/patch/tavern_recruitment.py'),
             Path('scripts/prepare_tavern_recruitment_v627.py'), Path('scripts/verify_tavern_recruitment_native_v627.py'),
             Path('scripts/verify_tavern_recruitment_release_v627.py'), Path(__file__)]
    for source in files:
        checked_copy(source, ARCHIVE / source.name)
    for name in ('release_proof.json', 'native_proof.json', 'source_and_native_preview_proof.json',
                 'patch_proof.json', 'preservation_proof.json', 'full_prefix.json'):
        checked_copy(ROOT / name, ARCHIVE / name)
    for source in ROOT.glob('voice_*_native.png'):
        checked_copy(source, ARCHIVE / source.name)
    screenshots = []
    for label, root, selected in (
        ('V626_truncated_control', CAP / 'tavern_recruitment_v626_control', (5600, 6000, 6800, 7600)),
        ('V627_ordinary_recruitment', CAP / 'tavern_recruitment_v627_actual', range(3200, 7602)),
        ('V627_ordinary_Finish_and_Town', CAP / 'tavern_recruitment_v627_finish', range(7600, 8802)),
        ('V627_ordinary_New_Game_Market', CAP / 'tavern_recruitment_v627_market', None)):
        report_path = root / 'capture_report.json'
        report = read(report_path)
        assert report['cold_boot'] and not report['savestate_loaded'] and not report['callback_errors']
        assert not any(v for k, v in report.items() if k.startswith('synthetic_'))
        checked_copy(report_path, ARCHIVE / (label + '_capture_report.json'))
        journal = root / 'navigation_command_journal.json'
        if journal.exists():
            checked_copy(journal, ARCHIVE / (label + '_navigation_journal.json'))
        shots = {r['frame']: r for r in report['frames_captured']}
        for frame, shot in sorted(shots.items()):
            if selected is not None and frame not in selected:
                continue
            assert sha(Path(shot['path']).read_bytes()) == shot['PNG_sha256']
            target = ARCHIVE / f'{label}_{frame:06d}_UNMODIFIED_NATIVE.png'
            checked_copy(shot['path'], target)
            screenshots.append({'path': str(target), 'sha256': shot['PNG_sha256'], 'frame': frame,
                                'ROM_sha256': report['ROM_sha256'], 'unmodified_capture': True,
                                'no_synthetic_gameplay_fixtures': True, 'cold_boot_no_savestate': True,
                                'historical_truncated_control': label.startswith('V626')})
    save(ARCHIVE / 'provenance.json', {
        'candidate': str(ROM), 'candidate_sha256': proof['candidate_sha256'], 'screenshots': screenshots,
        'full_RAM_and_ITCM_exports_retained_in_Generated_runs': True, 'publication_approved': False,
        'full_goal_complete': False,
        'files': {p.name: sha(p.read_bytes()) for p in ARCHIVE.iterdir() if p.is_file() and p.name != 'provenance.json'}})
    entry = {
        'documentation': str(DOC), 'proof': str(proof_path), 'proof_sha256': sha(proof_path.read_bytes()),
        'candidate': str(ROM), 'candidate_sha256': proof['candidate_sha256'], 'profile': proof['profile'],
        'patch_sha256': proof['patch_sha256'], 'status': 'experimental_complete_recruitment_voice_family_verified',
        'all7_independent_source_calls_preserve_complete_English_and_Admiral': True,
        'all83_affected_native_entries_hot_and_cold_cache166_copies_and14_full_glyph_planes_pass': True,
        'ordinary_Charles_voice897_full228x80_actual_foreground_background_mask_exact': True,
        'same35_recruits1573_cost_and_full_fleet_control_state_normal_Finish_Town': True,
        'no_gameplay_fixtures_or_savestates': True,
        'other_six_voices_have_native_component_not_ordinary_gameplay_credit': True,
        'all19_ordinary_no_save_New_Game_Market_screens_exact_V626': True,
        'all470_batches114_accepted_layers921_graphics57_embedded_extents_and_exact_patch_retained': True,
        'all18_original_plaques_incomplete_all22_historical_objects_retained': True,
        'CP932_I_model_and_broader_graphics_material_legacy_village_Confirm_miniature_gates_open': True,
        'archive': str(ARCHIVE), 'unmodified_screenshots': len(screenshots),
        'full_goal_complete': False, 'canonical_promoted': False}
    frozen = read('work/analysis/confirm_material_v572/audit_scope_before.json')
    for name, scope in frozen.items():
        path = Path('translations') / name
        data = read(path)
        assert data.get('historical_pending_items_retained') == scope['historical_pending_items_retained']
        assert data.get('plaque_style_v247', {}).get('ongoing_plaque_inventory') == scope['ongoing_plaque_inventory']
        protected = {k: v for k, v in data.items() if k in (
            'candidate', 'candidate_sha256', 'latest_candidate', 'latest_candidate_sha256',
            'current_verified_release_candidate', 'current_verified_release_candidate_sha256', 'latest_graphics_preservation')}
        data[KEY] = entry
        latest = data.get('latest_compiled_experimental_candidate_with_inherited_native_gap', {}).copy()
        latest.update({'candidate': str(ROM), 'sha256': proof['candidate_sha256'], 'profile': proof['profile'],
                       'all7_recruitment_calls_and_ordinary_Charles_recruitment_verified': True,
                       'broader_graphics_gates_remain_open': True})
        data['latest_compiled_experimental_candidate_with_inherited_native_gap'] = latest
        data['current_goal_turn_classification'] = 'progress'
        save(path, data)
        current = read(path)
        assert all(current[k] == v for k, v in protected.items())
        assert current.get('historical_pending_items_retained') == scope['historical_pending_items_retained']
        assert current.get('plaque_style_v247', {}).get('ongoing_plaque_inventory') == scope['ongoing_plaque_inventory']
    heading = '## V627: complete independent Tavern recruitment calls'
    text = '''

All seven clean-source recruitment voices now have complete natural English,
including the Admiral and both explicit calls to step forward. Old897/898 were
incorrectly split across independent cache selections;902/903 also lost meaning.
Native repacking preserves every3668 message/NUL identity,41 cache extents and
all other prose while funding complete lines from terminal padding. All83
affected entries pass166 hot/cold native copies;14 full original-font planes
and exact added-table scopes pass. Two ordinary no-fixture cold boots verify
Charles's full call,identical35 recruits/1573 cost/whole fleet state and every
other captured frame. Normal Finish/Yes/Back reaches Town in a further cold boot.
All19 ordinary no-save New Game/Market screens match V626;470/114 stack,921/57
preservation and exact patch roundtrip pass. Experimental V627 SHA256:
0a03862a0a0a75c748e2f806016d2316f881eb9799907590715c41d251bf2a09.

Only Charles's selected alternative has ordinary gameplay credit;the others have
full source/native component verification. The older CP932-I model difference
and broader graphics gates remain open. All18 original plaques incomplete,
all22 historical scopes exact,canonical/verified pointers retained. ROM,patch,
manifest and unmodified evidence are on E;full goal remains active. See
[V627 checkpoint](tavern_recruitment_v627_checkpoint.md).
'''
    for name in ('todo', 'translation_progress', 'known_issues', 'release_build'):
        path = Path('docs') / (name + '.md')
        content = path.read_text(encoding='utf-8')
        if heading not in content:
            path.write_text(content.rstrip() + '\n\n' + heading + '\n' + text, encoding='utf-8')
    print(f'Archived {len(screenshots)} unmodified screenshots; three audits/progress updated;18/22 scopes and canonical retained.')


if __name__ == '__main__':
    main()
