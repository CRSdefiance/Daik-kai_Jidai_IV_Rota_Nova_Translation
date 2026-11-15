"""Verify genuine cartridge-save cold boot and correct prior persistence claims."""

import json
from pathlib import Path

from dk4tool.patch.grand_race_menu_release import sha

ROOT = Path('work/analysis/battery_continue_v314')
CAPTURE = Path('work/emulation_v193/battery_continue_v314')
SOURCE = Path('work/emulation_v193/gallery_menu_v307/saves/all_routes_combined_v307_candidate.dsv')
ROM = Path('out/all_routes_combined_v309_candidate.nds')


def read(path):
    return json.loads(Path(path).read_text(encoding='utf-8'))


def main():
    ROOT.mkdir(parents=True, exist_ok=True)
    report_path = CAPTURE / 'capture_report.json'
    report = read(report_path)
    digest, source_digest = sha(ROM.read_bytes()), sha(SOURCE.read_bytes())
    assert source_digest == '58d7c0d4cc43a43579cc218ef2a391a4a71fec83e77803924189b6d023ca8af0'
    assert SOURCE.read_bytes().startswith(b'DK4R') and SOURCE.read_bytes().endswith(b'|-DESMUME SAVE-|')
    assert report['ROM_sha256'] == digest and report['cold_boot'] and not report['savestate_loaded']
    assert report['frames'] == 3200 and not report['callback_errors']
    preload = report['battery_save_preloaded']
    assert preload['source_sha256'] == source_digest and preload['copied_byte_exact_before_cold_boot']
    original = read('work/emulation_v193/gallery_menu_v307/capture_report.json')
    assert original['cold_boot'] and not original['savestate_loaded'] and original['frames'] == 31200
    rows = {}
    for row in report['frames_captured']:
        assert sha(Path(row['path']).read_bytes()) == row['PNG_sha256']
        rows[row['frame']] = row
    source_headers = SOURCE.read_bytes()[:128].hex()
    proof = {'candidate_unchanged': str(ROM), 'candidate_sha256': digest,
             'source_battery_file': str(SOURCE), 'source_battery_sha256': source_digest,
             'source_battery_bytes': len(SOURCE.read_bytes()), 'source_header128_hex': source_headers,
             'source_ordinary_in_game_save_capture': 'work/emulation_v193/gallery_menu_v307/capture_report.json',
             'source_capture_sha256': sha(Path('work/emulation_v193/gallery_menu_v307/capture_report.json').read_bytes()),
             'cold_boot_cartridge_save_native_Continue_load_success': True,
             'loaded_Rafael_Lisbon_docked_observed': True, 'loaded_date_visually_observed': '1M11D',
             'loaded_company_visually_observed': 'Castor Co.',
             'actual_title_slot_confirmation_and_loaded_town_frames_visually_reviewed': [2000, 2400, 2800, 3200],
             'ordinary_title_Continue_slot_and_confirmation_inputs': report['scripted_input_schedule'],
             'capture_report': str(report_path), 'capture_report_sha256': sha(report_path.read_bytes()),
             'no_savestate_load_ROM_unlock_patch_or_live_RAM_injection': True,
             'prior_no_DSV_files_or_no_persistence_claim_is_superseded': True,
             'cartridge_save_header_is_DK4R_not_assumed_DK4R6_ASCII': True,
             'hidden_Gallery_and_occupied_weapon_armor_not_yet_verified': True,
             'all18_plaque_audit_entries_and_variants_remain_incomplete': True,
             'low_resolution_Online_images_exempt': True, 'ROM_modified': False,
             'full_goal_complete': False, 'documentation': 'docs/battery_continue_v314.md'}
    (ROOT / 'proof.json').write_text(json.dumps(proof, indent=2) + '\n', encoding='utf-8')
    for filename in ('graphics_completion_campaign_v1.json', 'graphics_visual_audit_v150.json'):
        path = Path('translations') / filename
        audit = read(path)
        assert audit['latest_candidate_sha256'] == digest
        assert not audit['user_scope_exceptions']['low_resolution_online_images']['translation_required']
        assert all(not r['fully_completed'] for r in audit['plaque_style_v247']['ongoing_plaque_inventory'])
        audit['ordinary_battery_Continue_v314'] = {**proof, 'proof': str(ROOT / 'proof.json')}
        audit['current_goal_turn_classification'] = 'progress-genuine-cartridge-save-cold-boot-Continue-and-persistence-correction'
        path.write_text(json.dumps(audit, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    section = '''## V314: genuine cartridge-save Continue and persistence correction

The V307 ordinary Gallery save did produce a262,266-byte DSV file. Prior claims
that no DSV existed or that the frontend could not persist gameplay were wrong.
The game header is DK4R; searching for DK4R6 as one ASCII string missed it.
A byte-exact copy in a fresh V309 save folder cold-boots normally: Continue is
enabled, Rafael's Lisbon slot loads, and the observed date is1M11D.
No savestate, unlock patch or live RAM injection is used. Optional --battery-save
records provenance and refuses an existing destination. Native file persistence
now supports longer ordinary acquisition tests. Weapon/Armor, hidden Gallery
and18 plaques remain open; Online images exempt. V309 unchanged. See
[V314 evidence](battery_continue_v314.md).

'''
    for filename in ('translation_progress.md', 'known_issues.md', 'todo.md'):
        path = Path('docs') / filename
        content = path.read_text(encoding='utf-8')
        if '## V314:' not in content:
            title, rest = content.split('\n\n', 1)
            path.write_text(title + '\n\n' + section + rest, encoding='utf-8')
    print('Genuine in-game battery save cold-boots and loads through Continue; source unchanged; longer ordinary tests now feasible.')


if __name__ == '__main__':
    main()
