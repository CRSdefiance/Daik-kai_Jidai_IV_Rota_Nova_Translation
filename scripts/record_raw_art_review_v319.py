"""Current source/English editorial review with separate native display limits."""

import json
from pathlib import Path

from dk4tool.patch.grand_race_menu_release import sha

ROOT = Path('work/analysis/raw_art_review_v319')


def read(path):
    return json.loads(Path(path).read_text(encoding='utf-8'))


def main():
    inventory, preservation = read(ROOT / 'inventory.json'), read(ROOT / 'source_protection.json')
    letters = read(ROOT / 'final_letters/proof.json')
    assert inventory['candidate_sha256'] == letters['candidate_sha256']
    assert len(inventory['rows']) == 8 and all(r['source_current_bit15_preserved'] for r in inventory['rows'])
    assert letters['records_checked'] == 18 and letters['final_quantized_character_bounds_checked'] == 331
    assert letters['first_final_erasure_negative_cases'] == 36
    assert preservation['all_source_words_outside_declared_edit_boxes_exact']
    assert preservation['all1612800_original_bit15_values_preserved']
    green = read(ROOT / 'green_remnants.json')
    assert green == []
    review = [
        {'frames': [4, 10], 'source_and_current_full_images_reviewed': True,
         'meaning': 'Recruiting New Crew, named art/story credits and The End preserve the original caption functions.',
         'visual': 'Current credit/title placement is readable and clear of the running figures and creature; restored caption/photo edges reviewed.',
         'hidden_source_background_exactly_recovered': False},
        {'frames': [5], 'source_and_current_full_images_reviewed': True,
         'meaning': 'Bullfighter declaration, go-to-sea demand, refusal and pursuit call retain the complete source actions.',
         'reading': 'The slanted text is まちやがれ コラー, not an established character-name call; existing Hey! Get back here! retained.',
         'visual': 'Complete English and bubble contours reviewed with running figures and restored sea region; existing source restoration retained.',
         'hidden_source_background_exactly_recovered': False},
        {'frames': [6, 7, 8, 9], 'source_and_current_full_images_reviewed': True,
         'meaning': 'Huh?!, TA-DA!, Who are you? and Sea cow retain the surprise/reveal/identity sequence and cow depiction.',
         'visual': 'Source/current creature silhouette, English and protected scene details reviewed. No source-green lettering pixels remain in the inspected horn area.',
         'interpretation_limit': 'Small neutral flecks are not confirmed old lettering; brown water shapes remain unreadable/unclassified and source-exact. No anatomical or kana reading invented.',
         'hidden_source_background_exactly_recovered': False},
        {'frames': [13], 'source_and_current_full_images_reviewed': True,
         'meaning': 'Maria Mode and thanks for playing through preserve the source heading/player thanks; painted by/creator marks stay original.',
         'visual': 'Portrait/flowers, vertical heading, source credit marks and complete English footer reviewed.',
         'hidden_source_background_exactly_recovered': False},
    ]
    proof = {'candidate_unchanged': inventory['candidate'], 'candidate_sha256': inventory['candidate_sha256'],
             'documentation': 'docs/raw_art_review_v319.md', 'source_current_editorial_reviews': review,
             'complete_current_letter_records': 18, 'complete_current_quantized_character_bounds': 331,
             'first_final_erasure_negatives': 36, 'all_source_pixels_outside_declared_edit_boxes_exact': True,
             'all1612800_source_bit15_values_preserved': True,
             'current_raw_source_art_borders_and_full_context_visually_reviewed': True,
             'ambiguous_brown_water_shapes_interpretation_still_open': True,
             'no_confirmed_new_pixel_defect_or_ROM_change_from_this_review': True,
             'actual_native_raw_viewer_crops_scaling_readability_and_GPU_still_unproved': True,
             'all11_legacy_gates_and18_plaques_remain_open': True,
             'low_resolution_Online_images_translation_exempt': True,
             'inventory': str(ROOT / 'inventory.json'), 'source_protection': str(ROOT / 'source_protection.json'),
             'letter_proof': str(ROOT / 'final_letters/proof.json'), 'ROM_modified': False, 'full_goal_complete': False}
    (ROOT / 'review_proof.json').write_text(json.dumps(proof, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    for filename in ('graphics_completion_campaign_v1.json', 'graphics_visual_audit_v150.json'):
        path = Path('translations') / filename
        data = read(path)
        assert data['latest_candidate_sha256'] == proof['candidate_sha256']
        assert all(not r['fully_completed'] for r in data['plaque_style_v247']['ongoing_plaque_inventory'])
        assert not data['user_scope_exceptions']['low_resolution_online_images']['translation_required']
        data['current_raw_art_editorial_review_v319'] = {**proof, 'review_proof': str(ROOT / 'review_proof.json'),
                                                        'review_proof_sha256': sha((ROOT / 'review_proof.json').read_bytes())}
        data['current_goal_turn_classification'] = 'progress-current8-raw-frame-editorial-and331-complete-character-preservation-checks'
        path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    section = '''## V319: current raw-art context and restoration review

Eight original/current comic/heading frames are reviewed directly from V318.
Source meaning, complete English, portrait/creature/bubble/photo context and
restored caption areas are checked. Existing pursuit wording is retained:
source isまちやがれ コラー. No source-green lettering pixels remain near the
reveal horns; neutral flecks are not proven residue, so no speculative erasure.
All18 stored caption records,331 quantized character bounds and36 first/final
erasure negatives pass; all source pixels outside edit boxes/protected bubble
regions and1,612,800 bit15 values remain exact. Hidden covered backgrounds stay
approximate; brown shapes and actual raw viewer/crops/readability remain open.
V318 unchanged;18 plaques open; Online images exempt. See
[V319 review](raw_art_review_v319.md).

'''
    for filename in ('translation_progress.md', 'known_issues.md', 'todo.md'):
        path = Path('docs') / filename
        text = path.read_text(encoding='utf-8')
        if '## V319:' not in text:
            title, rest = text.split('\n\n', 1)
            path.write_text(title + '\n\n' + section + rest, encoding='utf-8')
    print('Current8 raw frames visually/source reviewed;18 captions/331 characters/36 negative cases and original source protection pass; V318 unchanged.')


if __name__ == '__main__':
    main()
