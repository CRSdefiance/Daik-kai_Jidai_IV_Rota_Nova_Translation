"""Bind the18 plaque terminology decisions to actual original/current crops."""

from pathlib import Path

from PIL import Image

from dk4tool.patch.grand_race_menu_release import sha
from scripts.review_current_plaques_v714 import CAP, ROOT
from scripts.verify_village_wrap_v608 import read, save

MEANINGS = (
    ('Fleet Crew', '艦隊水夫数', 'Number of sailors in the fleet.', 'Crew is the collective noun for the displayed fleet total.'),
    ('Unassigned', '未編成水夫数', 'Number of sailors not assigned to a formation.', 'The adjacent count supplies the noun; this does not imply a separate reserve fleet.'),
    ('Endurance', '航行可能日数', 'Number of days the fleet can remain at sea.', 'The value includes days. Endurance describes duration; Range would suggest distance.'),
    ('Quarters', '海兵詰所', 'Marine quarters or barracks.', 'This field counts marine-quarters compartments, not the current number of marines.'),
    ('Cannon', '砲種', 'Type of cannon.', 'The adjacent model and number supply the cannon type and quantity.'),
    ('Fore/Aft', '縦帆性能', 'Fore-and-aft sail performance.', 'A compact nautical heading for the displayed sail-performance values.'),
    ('Square', '横帆性能', 'Square-sail performance.', 'The sail icon and neighboring performance value supply the abbreviated context.'),
    ('Health', '身体', 'Physical condition.', 'The neighboring Healthy/illness condition makes Health natural here.'),
    ('Mood', '精神', 'Mental condition or spirits.', 'This condition field displays Normal and other mood states; it differs from the numeric Spirit attribute.'),
    ('Level', 'レベル', 'Level.', 'Direct established game terminology.'),
    ('HP', 'HP', 'HP.', 'Preserve the original Latin abbreviation.'),
    ('Stamina', '体力', 'Physical strength or stamina.', 'Stamina is a natural stat label for this physical attribute.'),
    ('Agility', '敏捷', 'Agility or quickness.', 'Natural stat terminology.'),
    ('Charm', '魅力', 'Charm or charisma.', 'Preserves the personal appeal attribute.'),
    ('Wits', '知力', 'Intellect or mental ability.', 'A compact natural English attribute label.'),
    ('Spirit', '精神', 'Spirit or mental strength.', 'The numeric attribute is distinct from the condition field localized as Mood.'),
    ('Luck', '運勢', 'Fortune or luck.', 'Natural English stat terminology.'),
    ('Equipped Items', '装備アイテム', 'Equipped items.', 'Describes the selected equipment row and its item slots.'),
)


def main():
    proof_path = ROOT / 'current_plaque_review_proof.json'
    proof = read(proof_path)
    rows = proof['all18_current_native_review_entries']
    assert len(rows) == len(MEANINGS) == 18
    decisions = []
    for row, (english, japanese, meaning, reason) in zip(rows, MEANINGS, strict=True):
        assert (row['English'], row['Japanese']) == (english, japanese)
        assert sha(Path(row['source_crop']).read_bytes()) == row['source_crop_sha256']
        assert sha(Path(row['current_crop']).read_bytes()) == row['current_crop_sha256']
        decisions.append({'number': row['number'], 'id': row['id'], 'original': japanese,
            'English': english, 'source_meaning': meaning, 'contextual_localization_reason': reason,
            'original_native_crop': row['source_crop'], 'English_native_crop': row['current_crop'],
            'source_current_crop_provenance': str(proof_path), 'translation_revision_required': False,
            'material_review_pending': True, 'fully_completed': False})
    # The complete current screens also check intervening UI outside these crops.
    old = read('work/analysis/plaque_review_v671/current_plaque_review_proof.json')
    previous = read(old['new_current_capture_report'])
    current = read(CAP / 'capture_report.json')
    assert current['core_DLL_sha256'] == previous['core_DLL_sha256']
    before = {r['frame']: r for r in previous['frames_captured']}
    pairs = []
    for row in current['frames_captured']:
        if row['frame'] not in (4300, 6300, 6700, 7100):
            continue
        a, b = Path(before[row['frame']]['path']), Path(row['path'])
        assert sha(a.read_bytes()) == before[row['frame']]['PNG_sha256']
        assert sha(b.read_bytes()) == row['PNG_sha256']
        assert Image.open(a).convert('RGB').tobytes() == Image.open(b).convert('RGB').tobytes()
        pairs.append(row['frame'])
    assert set(pairs) == {4300, 6300, 6700, 7100}
    save(ROOT / 'terminology_review.json', {'all18_source_context_and_natural_English_decisions': decisions,
        'all_four_current_whole_two_screen_images_match_previous_V666_review': sorted(set(pairs)),
        'current_original_core_DLL_exact': current['core_DLL_sha256'],
        'source_backed_texture_not_exact_recovery_of_concealed_pixels': True,
        'no_new_large_block_or_vertical_seam_identified_in_opened_current_sheets': True,
        'all18_entries_remain_open_user_material_response_pending': True,
        'verifier_sha256': sha(Path(__file__).read_bytes()), 'full_goal_complete': False})
    print('V714 all18 source meanings/contextual English reviewed; all4 full V712/V666 screen pairs exact.', flush=True)


if __name__ == '__main__':
    main()
