"""Archive the explicit UI fixtures and append scoped evidence to all three audits."""

from pathlib import Path

from dk4tool.patch.grand_race_menu_release import sha
from scripts.record_regional_ui_v616 import checked_copy
from scripts.verify_village_wrap_v608 import read, save

ROOT = Path('work/analysis/race_roster_v661')
DOC = Path('docs/race_roster_v661_checkpoint.md')
ARCHIVE = Path('E:/Rota Nova translations/Screenshots/Test fixtures/V661 Grand Race roster')
KEY = 'source_bound_four_Grand_Race_cards_and_separate_Back_Select_ready_footer_v661'


def copy(source, destination):
    destination.parent.mkdir(parents=True, exist_ok=True)
    checked_copy(source, destination)


def main():
    proof_path = ROOT / 'proof.json'
    proof, pre = read(proof_path), read(ROOT / 'preflight.json')
    for path, digest in proof['scripts'].items():
        assert sha(Path(path).read_bytes()) == digest
    for path, digest in pre['release_hashes'].items():
        assert sha(Path(path).read_bytes()) == digest
    assert len(proof['complete_card_name_masks']) == 32
    assert proof['first_final_deletion_controls_rejected'] == 64
    assert not proof['full_goal_complete']
    frozen = read('work/analysis/confirm_material_v572/audit_scope_before.json')
    for name, scope in frozen.items():
        data = read(Path('translations') / name)
        assert all(data[k] == v for k, v in pre['all_original_audits_before'][name].items()
                   if k not in (KEY, 'current_goal_turn_classification'))
        assert data.get('historical_pending_items_retained') == scope['historical_pending_items_retained']
        assert data.get('plaque_style_v247', {}).get('ongoing_plaque_inventory') == scope['ongoing_plaque_inventory']
    for source in (DOC, Path(__file__), *(Path(p) for p in proof['scripts']),
                   *ROOT.glob('*.json'), *ROOT.glob('*.txt'), *ROOT.glob('*.bin'),
                   *ROOT.glob('*.png'), *ROOT.glob('*.py')):
        copy(source, ARCHIVE / source.name)
    captures = []
    for label, item in proof['reports'].items():
        report_path = Path(item['path'])
        assert sha(report_path.read_bytes()) == item['sha256']
        report = read(report_path)
        folder = report_path.parent
        tag = label.upper() + '_ISOLATED_SYSTEM_UNLOCK' + ('' if label == 'baseline' else '_SYNTHETIC_UI')
        for source in folder.rglob('*'):
            if source.is_file():
                copy(source, ARCHIVE / tag / source.relative_to(folder))
        for shot in report['frames_captured']:
            captures.append({'run': tag, 'frame': shot['frame'], 'source': shot['path'],
                'PNG_sha256': shot['PNG_sha256'], 'wireless_verified': False,
                'guide_or_publication_approved': False})
    entry = {'documentation': str(DOC), 'proof': str(proof_path), 'proof_sha256': sha(proof_path.read_bytes()),
        'candidate': proof['candidate'], 'candidate_sha256': proof['candidate_sha256'],
        'three_terminal_cold_boots_system_unlock_fixture_and_two_UI_fixtures_disclosed': True,
        'four_original_cards32_complete_name_fields64_boundary_controls': True,
        'all34208_native_card_pixels_repainted_over_poison49152_lower_RGB_pixels_exact': True,
        'actual_portrait_cache_bound_not_new_independent_source_art_transcript': True,
        'separate_ready_only_fixture1228_changed_footer_pixels_whole_screen_restoration': True,
        'Grand_Race_waiting_ready_uses_Back_Select_text_footer_not_separate_Confirm_graphic': True,
        'no_simultaneous_four_peer_ready_wireless_race_or_full_footer_lettering_claim': True,
        'all_six_control_parents_other_graphics_and_final_acceptance_remain_open': True,
        'ROM_patch_manifest_registry_canonical_and_release_pointers_unchanged': True,
        'all18_original_plaques_incomplete22_historical_scopes_exact': True,
        'archive': str(ARCHIVE), 'no_guide_promotion': True, 'full_goal_complete': False}
    for name in frozen:
        path = Path('translations') / name
        data = read(path)
        data[KEY], data['current_goal_turn_classification'] = entry, 'progress'
        save(path, data)
        assert all(data[k] == v for k, v in pre['all_original_audits_before'][name].items()
                   if k not in (KEY, 'current_goal_turn_classification'))
    heading = '## V661: Grand Race four-card roster and separate ready text footer'
    addition = ('Three targeted cold boots finish normally. An explicit receive-ring fixture '
        'populates all four original cards;32 complete name fields and64 leading/trailing '
        'deletion controls pass. Native original accessors/setters/painters reconstruct '
        '34,208 card pixels over poison with no old-output reads; all49,152 lower RGB pixels '
        'match. Actual initialized portrait cache is used, not a new independent art transcript. '
        'A separate readiness-only fixture changes1,228 footer pixels to Back/Select and '
        'restores the whole waiting screen. Original source descriptors resolve this '
        'Grand Race lead as rendered text, not the separate Confirm graphic. Both UI '
        'fixtures and artificial system unlock are disclosed; no simultaneous four-peer '
        'ready state, wireless, completed race or full footer lettering claim. Unsuccessful '
        'output-packet/uninitialized-portrait/geometry leads retained. All six control '
        'parents, other graphics and acceptance remain open. No ROM/patch/registry/pointer '
        'change; all18 plaques incomplete and22 historical scopes exact. Evidence on E, '
        'no guide promotion. See [V661 checkpoint](race_roster_v661_checkpoint.md).\n')
    for name in ('todo.md', 'translation_progress.md', 'known_issues.md', 'release_build.md'):
        path = Path('docs') / name
        text = path.read_text(encoding='utf-8')
        if heading not in text:
            path.write_text(text.rstrip() + '\n\n' + heading + '\n\n' + addition, encoding='utf-8')
    save(ARCHIVE / 'provenance.json', {'candidate_sha256': proof['candidate_sha256'],
        'captures': captures, 'no_guide_or_wireless_or_publication_approval': True,
        'scripts': {str(p): sha(p.read_bytes()) for p in (Path(__file__), *(Path(p) for p in proof['scripts']))},
        'files': {str(p.relative_to(ARCHIVE)): sha(p.read_bytes()) for p in ARCHIVE.rglob('*')
                  if p.is_file() and p.name != 'provenance.json'}, 'full_goal_complete': False})
    print(f'V661 archived {len(captures)} capture records; three audits/four documents updated; full goal active.')


if __name__ == '__main__':
    main()
