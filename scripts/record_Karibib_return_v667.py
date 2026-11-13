"""Retain failed approaches and the source-verified actual Karibib Town scene."""

from pathlib import Path

from PIL import Image, ImageDraw

from dk4tool.patch.grand_race_menu_release import sha
from scripts.record_regional_ui_v616 import checked_copy
from scripts.run_Karibib_return_v667 import ROOT
from scripts.run_village_visits_v664 import CAP
from scripts.verify_village_wrap_v608 import read, save

ARCHIVE = Path('E:/Rota Nova translations/Screenshots/Test fixtures/V667 Karibib return')
DOC = Path('docs/Karibib_return_v667_checkpoint.md')
KEY = 'actual_Maria_Karibib_development_return_complete_native_Town_and_retained_Hodram_encounter_v667'
SCRIPTS = ('scripts/run_Karibib_return_v667.py', 'scripts/run_Karibib_followup_v667.py',
           'scripts/run_Karibib_Maria_v667.py', 'scripts/run_Karibib_Maria_reapproach_v667.py',
           'scripts/verify_Karibib_return_v667.py', 'scripts/record_Karibib_return_v667.py',
           'scripts/run_village_consistency_v666.py', 'scripts/run_village_development_v665.py',
           'scripts/run_village_return_v665.py', 'scripts/native_village_town_v665.py')


def copy(source, destination):
    destination = Path(destination)
    destination.parent.mkdir(parents=True, exist_ok=True)
    checked_copy(source, destination)


def main():
    proof_path = ROOT / 'proof.json'
    proof, pre = read(proof_path), read(ROOT / 'preflight.json')
    assert proof['verifier_sha256'] == sha(Path('scripts/verify_Karibib_return_v667.py').read_bytes())
    assert proof['full_both_native_Town_screens98304_pixels_exact_including_footer']
    assert proof['actual_captain_index'] == 3 and not proof['full_goal_complete']
    receipts, exports = [], {}
    for tag in ('noncombat', 'early_approach', 'Maria_Seoul', 'Maria_Seoul_reapproach'):
        folder = CAP / ('Karibib_return_v667_' + tag)
        rp = folder / 'capture_report.json'
        r, controller = read(rp), read(folder / 'controller_progress.json')
        assert r['ROM_sha256'] == pre['candidate_sha256']
        assert r['cold_boot'] and not r['savestate_loaded'] and not r['callback_errors']
        assert (controller['error'] is None) == (tag == 'Maria_Seoul_reapproach')
        receipts.append({'path': str(rp), 'sha256': sha(rp.read_bytes()), 'frames': r['frames'],
            'capture_records': len(r['frames_captured']), 'retained_controller_error': controller['error'],
            'actual_Karibib_Town_credit': tag == 'Maria_Seoul_reapproach'})
        for shot in r['frames_captured']:
            assert sha(Path(shot['path']).read_bytes()) == shot['PNG_sha256']
        for key in ('read_only_RAM_snapshot', 'read_only_native_state'):
            row = r.get(key)
            if row:
                exports[row['path']] = row['sha256']
                exports.update({q['path']: q['sha256'] for q in row.get('regions', {}).values()})
        for key in ('read_only_pause_RAM_snapshots', 'read_only_capture_RAM_snapshots'):
            exports.update({q['path']: q['sha256'] for q in r.get(key, [])})
    for path, digest in exports.items():
        assert Path(path).resolve().drive.upper() == 'E:' and sha(Path(path).read_bytes()) == digest
    frozen = read('work/analysis/confirm_material_v572/audit_scope_before.json')
    for name, scope in frozen.items():
        data = read(Path('translations') / name)
        assert all(data[k] == v for k, v in pre['all_original_audits_before'][name].items()
                   if k != 'current_goal_turn_classification')
        assert data.get('historical_pending_items_retained') == scope['historical_pending_items_retained']
        assert data.get('plaque_style_v247', {}).get('ongoing_plaque_inventory') == scope['ongoing_plaque_inventory']
    for path, digest in pre['release_hashes'].items():
        assert sha(Path(path).read_bytes()) == digest
    folder = Path(proof['report']).parent
    sheet = Image.new('RGB', (1040, 804), '#263238')
    draw = ImageDraw.Draw(sheet)
    for column, phase in enumerate(('reapproach_docking_prompt', 'developed_town_return')):
        frame = proof['phases'][phase]
        image = Image.open(folder / f'frame_{frame:06d}_navigation.png').convert('RGB')
        draw.text((8 + column * 520, 8), 'V666 Maria - ' + phase + ' - LOCATION FIXTURE', fill='white')
        sheet.paste(image.resize((512, 768), Image.Resampling.NEAREST), (8 + column * 520, 28))
    sheet.save(ROOT / 'Karibib_ACTUAL_REVIEW.png')
    entry = {'documentation': str(DOC), 'proof': str(proof_path), 'proof_sha256': sha(proof_path.read_bytes()),
        'candidate': pre['candidate'], 'candidate_sha256': pre['candidate_sha256'],
        'status': 'actual_Karibib_common_Town_verified_with_authorized_Maria_save_Hodram_encounter_not_closed',
        'all9_password_prefixes_and_original0_to2_development_pass': True,
        'complete_docking_header_specialty_and98304_native_Town_pixels_pass': True,
        'all24_developed_ports_have_native_scene_evidence_across_recorded_candidates': True,
        'previous_Maria_missed_return_full_prefix_matches': True,
        'Hodram_decline_choice_still_leads_to_encounter_and_footer_identity_assumption_rejected': True,
        'three_failed_attempts_retained_without_Town_credit': True,
        'two_coordinate_only_Maria_approaches_no_outcome_or_story_injection': True,
        'previously_authorized_Maria_selection_bypass_donor_not_earned_unlock': True,
        'Hodram_encounter_eight_cards_six_controls_other_contexts_and_final_acceptance_open': True,
        'all18_original_plaques_incomplete22_historical_scopes_exact': True,
        'ROM_patch_registry_and_release_pointers_unchanged': True, 'archive': str(ARCHIVE), 'full_goal_complete': False}
    for name in frozen:
        target = Path('translations') / name
        data = read(target)
        data[KEY], data['current_goal_turn_classification'] = entry, 'progress'
        save(target, data)
    heading = '## V667: actual Maria Karibib return and complete common Town scene'
    addition = ('The unchanged V666 ROM cold-loads the previously authorized Maria Seoul save '
        '(selection bypass provenance retained). Original keyboard typing accepts Kalahari and '
        'changes Karibib0 to2. A fresh repeat adds one coordinate-only reapproach after a missed '
        'return; all earlier sampled screens match. Complete docking, title, specialty and both '
        'native Town screens98304 pixels pass with the original footer registration contract. '
        'All24 developed villages now have actual native Town evidence across the recorded '
        'candidates. Three failed attempts remain retained: Hodram still encounters slavers after '
        'the decline choice; its exact-footer state detector misses visible Sea states; an earlier '
        'approach still cannot dock; Maria first sails past range. These receive no port credit. '
        'Hodram encounter completion remains open. No recovery/outcome/story flags, new ROM, '
        'patch, registry, release-pointer changes or guide promotion. All18 plaques remain '
        'incomplete and22 scopes exact; eight card contexts, six controls, legacy/material/other '
        'contexts, older record checks and final acceptance stay open. Evidence on E; full goal '
        'active. See [V667 checkpoint](Karibib_return_v667_checkpoint.md).\n')
    for name in ('todo.md', 'translation_progress.md', 'known_issues.md', 'release_build.md'):
        target = Path('docs') / name
        text = target.read_text(encoding='utf-8')
        if heading not in text:
            target.write_text(text.rstrip() + '\n\n' + heading + '\n\n' + addition, encoding='utf-8')
    ARCHIVE.mkdir(parents=True, exist_ok=True)
    for receipt in receipts:
        folder = Path(receipt['path']).parent
        for source in folder.iterdir():
            if source.is_file() and source.suffix.lower() in ('.json', '.png'):
                copy(source, ARCHIVE / 'captures' / folder.name / source.name)
    for source in [DOC, *map(Path, SCRIPTS)]:
        copy(source, ARCHIVE / 'sources' / source.name)
    for source in ROOT.rglob('*'):
        if source.is_file():
            copy(source, ARCHIVE / 'analysis' / source.relative_to(ROOT))
    for name in frozen:
        copy(Path('translations') / name, ARCHIVE / 'audits' / name)
    for name in ('todo.md', 'translation_progress.md', 'known_issues.md', 'release_build.md'):
        copy(Path('docs') / name, ARCHIVE / 'docs' / name)
    save(ARCHIVE / 'provenance.json', {'candidate_sha256': pre['candidate_sha256'], 'reports': receipts,
        'all_four_runs_terminal': True, 'three_controller_failures_retained': True,
        'actual_Karibib_Town_credit_only_for_final_Maria_reapproach': True,
        'source_scripts': {p: sha(Path(p).read_bytes()) for p in SCRIPTS},
        'read_only_RAM_native_exports_retained_at_original_E_paths': exports,
        'files': {str(p.relative_to(ARCHIVE)): sha(p.read_bytes()) for p in ARCHIVE.rglob('*')
                  if p.is_file() and p.name != 'provenance.json'}, 'full_goal_complete': False})
    print('V667 four terminal attempts archived; actual Karibib native scene added;18/22 scope preserved.', flush=True)


if __name__ == '__main__':
    main()
