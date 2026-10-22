"""Record actual confirmation translation and the ordinary voyage prerequisites."""

import json
from pathlib import Path

from dk4tool.patch.grand_race_menu_release import sha
from scripts.prepare_auto_move_v316 import ROOT
from scripts.verify_auto_move_v316 import ROM, read


def main():
    proof = read(ROOT / 'release_proof.json')
    assert not proof['actual_confirmation_pending'] and proof['candidate_sha256'] == sha(ROM.read_bytes())
    discovery_path = Path('work/emulation_v193/ordinary_voyage_v315/capture_report.json')
    discovery = read(discovery_path)
    assert discovery['frames'] == 17600 and discovery['cold_boot'] and not discovery['savestate_loaded']
    assert not discovery['callback_errors']
    checkpoint = {**proof, 'documentation': 'docs/auto_move_caption_v316.md',
                  'release_proof': str(ROOT / 'release_proof.json'),
                  'source_discovery_capture': str(discovery_path), 'source_discovery_sha256': sha(discovery_path.read_bytes()),
                  'ordinary_Auto_Move_Ceuta_selection_verified': True,
                  'actual_No_surveyor_aboard_and_Survey_room_Need120_no_eligible_crew_observed': True,
                  'actual_Deck_Lookout_Mast_Survey_Helm_and_manual_roster_views_observed': True,
                  'no_voyage_weapon_armor_acquisition_or_equipment_clearance_in_discovery_run': True,
                  'other_related_Japanese_Auto_Move_contexts_still_require_consumer_review': True,
                  'all18_plaques_and_variants_remain_incomplete': True,
                  'low_resolution_Online_images_translation_exempt': True,
                  'experimental_user_acceptance_pending': True, 'full_goal_complete': False}
    for filename in ('graphics_completion_campaign_v1.json', 'graphics_visual_audit_v150.json'):
        path = Path('translations') / filename
        data = read(path)
        assert not data['user_scope_exceptions']['low_resolution_online_images']['translation_required']
        assert all(not r['fully_completed'] for r in data['plaque_style_v247']['ongoing_plaque_inventory'])
        data['Auto_Move_confirmation_v316'] = checkpoint
        data['latest_candidate'], data['latest_candidate_sha256'] = str(ROM), proof['candidate_sha256']
        data['current_goal_turn_classification'] = 'progress-ordinary-navigation-new-Japanese-confirmation-source-native-live-fix'
        path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    section = '''## V315/V316: ordinary navigation and Auto Move confirmation

A genuine saved-game cold boot selects Ceuta through Auto Move and exposes
Japanese自動移動 in the confirmation. V316 translates that original12-byte
ARM9 slot as Auto Move, with descriptor/pointers/code unchanged. Complete123
native lettering pixels pass in the same6,000-frame ordinary replay; earlier
comparable frames remain exact and changes stay inside the popup. All470 batches
and inherited art/routes/shared text are retained; V309 reproduces before/after
builder change, and the clean-input patch reconstructs exactly. The voyage
requires a Survey120 navigator; the current crew is ineligible, so no voyage
or weapon/armor acquisition is credited. Other related Auto Move contexts,
all18 plaques and broader graphics gates remain open; Online images exempt.
Experimental. See [V316 evidence](auto_move_caption_v316.md).

'''
    for filename in ('translation_progress.md', 'known_issues.md', 'todo.md'):
        path = Path('docs') / filename
        content = path.read_text(encoding='utf-8')
        if '## V315/V316:' not in content:
            title, rest = content.split('\n\n', 1)
            path.write_text(title + '\n\n' + section + rest, encoding='utf-8')
    print('V316 current: actual Auto Move lettering complete, full inherited release and exact patch; remaining audits stay open.')


if __name__ == '__main__':
    main()
