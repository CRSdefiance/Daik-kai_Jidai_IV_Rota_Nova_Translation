"""Record source review and verified native-height genre release, preserving gaps."""

import json
from pathlib import Path

from dk4tool.patch.grand_race_menu_release import sha
from scripts.prepare_genre_card_v305 import ROOT
from scripts.verify_genre_card_release_v305 import ROM, read


def main():
    release, live = read(ROOT / 'release_proof.json'), read(ROOT / 'live_proof.json')
    source = read('work/analysis/root_fls_v304/source_proof.json')
    assert release['candidate_sha256'] == live['candidate_sha256'] == sha(ROM.read_bytes())
    assert live['complete_foreground_pixels'] == 787 and len(live['matches']) == 2
    release.update({'actual_startup_pixels_pending': False, 'actual_complete_genre_foreground_pixels': 787,
                    'actual_startup_matching_frames': [r['frame'] for r in live['matches']],
                    'native_genre_center_y': 96, 'actual_cold_boot_frames': 20000,
                    'actual_title_New_Game_Rafael_opening_and_town_captured': True,
                    'no_savestate_loaded_or_RAM_injection': True,
                    'live_proof_sha256': sha((ROOT / 'live_proof.json').read_bytes()),
                    'startup_title_and_town_frames_visually_reviewed': True,
                    'focused_opening_movie_tests_passed': 2, 'experimental_user_acceptance_pending': True})
    (ROOT / 'release_proof.json').write_text(json.dumps(release, indent=2) + '\n', encoding='utf-8')
    checkpoint = {**release, 'documentation': 'docs/genre_native_view_v305.md',
                  'release_proof': str(ROOT / 'release_proof.json'), 'live_proof': str(ROOT / 'live_proof.json'),
                  'all11_legacy_composition_gates_and_brown_mark_interpretation_still_open': True,
                  'all18_plaques_and_variants_incomplete': True, 'Online_low_resolution_images_exempt': True,
                  'full_goal_complete': False}
    source_checkpoint = {'source_proof': 'work/analysis/root_fls_v304/source_proof.json',
                         'source_proof_sha256': sha(Path('work/analysis/root_fls_v304/source_proof.json').read_bytes()),
                         'documentation': 'docs/genre_native_view_v305.md',
                         'all262144_root_pixels_palette_padding_and_file_exact_clean': True,
                         'source_retain_art_decision_revalidated': True,
                         'all261_FLS_textures_exact_copy_search_only_root_self_match': True,
                         'root_native_consumer_and_projection_unknown': True,
                         'retained_brown_mark_regions_source_exact': source['retained_brown_mark_source_regions'],
                         'reading_anatomy_and_creator_intent_not_inferred': True,
                         'all11_legacy_native_gates_remain_open': True, 'full_goal_complete': False}
    for name in ('graphics_completion_campaign_v1.json', 'graphics_visual_audit_v150.json'):
        path = Path('translations') / name
        data = read(path)
        assert not data['user_scope_exceptions']['low_resolution_online_images']['translation_required']
        assert all(not r['fully_completed'] for r in data['plaque_style_v247']['ongoing_plaque_inventory'])
        data['root_and_retained_source_v304'] = source_checkpoint
        data['genre_native_view_v305'] = checkpoint
        data['latest_candidate'], data['latest_candidate_sha256'] = str(ROM), release['candidate_sha256']
        path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    section = '''## V304/V305: native-height genre layout restored

Original genre lettering is centered in256x192, while inherited English used
the256x256 padded texture and appeared32 pixels too low. New header-size-v2
authoring derives both native dimensions and rejects conflicts/out-of-view ink.
Complete established English now matches the original's approximate width and
center y96. All787 lettering pixels match two actual startup frames, followed
by title/New Game/Rafael opening/town in a fresh20000-frame cold boot. V305 keeps
469 inherited batches plus one genre batch; only one logo compressed slot changes,
all metadata/palettes/code/other art/text stay exact, V303 reproduces before/after
the API change, the clean patch reconstructs and focused movie tests pass.
Root scenery remains clean/source-exact; no exact copy elsewhere in261 FLS
textures is inferred. Brown source marks remain exact but uninterpreted. All11
legacy composition gates and all18 plaque audits stay open; Online images exempt.
See [V305 evidence](genre_native_view_v305.md).

'''
    for name in ('translation_progress.md', 'known_issues.md', 'todo.md'):
        path = Path('docs') / name
        text = path.read_text(encoding='utf-8')
        if '## V304/V305:' not in text:
            title, rest = text.split('\n\n', 1)
            path.write_text(title + '\n\n' + section + rest, encoding='utf-8')
    print('V305 native-height genre and exact source-retain evidence recorded; legacy/plaque gates remain open.')


if __name__ == '__main__':
    main()
