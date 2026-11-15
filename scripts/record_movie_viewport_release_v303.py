"""Record the actual crop defect, complete movie repair and still-open audit."""

import json
from pathlib import Path

from dk4tool.patch.grand_race_menu_release import sha
from scripts.prepare_movie_viewport_release_v303 import ROOT
from scripts.verify_movie_viewport_release_v303 import ROM, read


def main():
    release, actual = read(ROOT / 'release_proof.json'), read(ROOT / 'proof.json')
    defect = read('work/analysis/movie_playback_v302/crop_defect.json')
    assert release['candidate_sha256'] == actual['candidate_sha256'] == sha(ROM.read_bytes())
    assert actual['all_five_actual_subtitles_full_pixels_verified'] and not actual['missing_actual_cards']
    assert len(actual['cards']) == 5 and all(len(row['matches']) >= 3 for row in actual['cards'])
    assert defect['missing_fill_pixels'] + defect['missing_outline_pixels'] == 42
    release.update({'current_actual_full_movie_subtitle_pixels_pending': False,
                    'all5_actual_movie_subtitle_cards_complete': True,
                    'complete_distinct_white_fill_and_black_outline_pixels': sum(r['source_opaque_pixels'] for r in actual['cards']),
                    'complete_actual_card_instances': sum(len(r['matches']) for r in actual['cards']),
                    'three_production_ordinary_cold_boots_no_movie_skips_savestates_or_RAM_injection': True,
                    'actual_playback_proof_sha256': sha((ROOT / 'proof.json').read_bytes()),
                    'before_fix_missing_pixels': 42, 'M24_inference_preserved': True,
                    'preview_visually_reviewed': True, 'experimental_user_acceptance_pending': True})
    (ROOT / 'release_proof.json').write_text(json.dumps(release, indent=2) + '\n', encoding='utf-8')
    checkpoint = {**release, 'documentation': 'docs/movie_subtitle_viewport_v303.md',
                  'release_proof': str(ROOT / 'release_proof.json'), 'actual_playback_proof': str(ROOT / 'proof.json'),
                  'exact_source_FLS_textures_checked_for_subtitle_copies': actual['complete_clean_FLS_textures_scanned_for_exact_subtitle_copies'],
                  'all11_legacy_native_composition_gates_still_open': True,
                  'Online_low_resolution_translation_exemption_preserved': True, 'full_goal_complete': False}
    for name in ('graphics_completion_campaign_v1.json', 'graphics_visual_audit_v150.json'):
        path = Path('translations') / name
        data = read(path)
        assert not data['user_scope_exceptions']['low_resolution_online_images']['translation_required']
        assert all(not r['fully_completed'] for r in data['plaque_style_v247']['ongoing_plaque_inventory'])
        data['movie_crop_defect_v302'] = {'candidate': defect['candidate'], 'asset': defect['asset'],
                                        'texture_index': 1, 'missing_fill_pixels': defect['missing_fill_pixels'],
                                        'missing_outline_pixels': defect['missing_outline_pixels'],
                                        'native_width': 176, 'storage_width': 256,
                                        'proof': 'work/analysis/movie_playback_v302/crop_defect.json',
                                        'status': 'corrected-and-actual-playback-verified-in-V303'}
        data['movie_subtitle_viewport_v303'] = checkpoint
        data['latest_candidate'], data['latest_candidate_sha256'] = str(ROM), release['candidate_sha256']
        path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    section = '''## V302/V303: actual movie subtitle crop found and corrected

Unskipped V299 movie playback finds42 missing M22 card1 fill/outline pixels:
256-column authoring exceeded its176-column native view. The new source-metadata
viewport policy rejects conflicting storage widths and out-of-view ink. Four
complete M22/M24 cards are centered in176/216 widths; M20's168 layout is retained.
M24 now preserves the source's inference with "Looks like a foreign merchant ship!"
All five cards pass complete actual production movie pixels, including8559
distinct fill/outline pixels across31 card instances and transparent backgrounds.
All261 FLS source textures checked for exact subtitle copies; none missed.
V303 retains467 inherited batches plus two new batches, only four compressed
pixel slots change, all metadata/palettes/code/other art/text remain exact, full
V299 reproduces before/after builder edits and the clean patch reconstructs.
Experimental; user acceptance, legacy/Gallery/deep scenes and all18 plaque audits
remain open. Online images stay exempt. See [V303 repair](movie_subtitle_viewport_v303.md).

'''
    for name in ('translation_progress.md', 'known_issues.md', 'todo.md'):
        path = Path('docs') / name
        text = path.read_text(encoding='utf-8')
        if '## V302/V303:' not in text:
            title, rest = text.split('\n\n', 1)
            path.write_text(title + '\n\n' + section + rest, encoding='utf-8')
    print(f'V303 recorded: all5 actual movie cards, {release["complete_distinct_white_fill_and_black_outline_pixels"]} complete pixels, {release["complete_actual_card_instances"]} instances; full goal still open.')


if __name__ == '__main__':
    main()
