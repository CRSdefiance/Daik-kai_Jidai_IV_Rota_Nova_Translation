"""Bind the already viewed menu/name sheets and measure final layout changes."""
from pathlib import Path
from scripts.audit_story_glyph_consistency import load, save
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest

ROOT = Path('work/Lil269_B243_B282_clean_20261110')

if __name__ == '__main__':
    output = ROOT / 'mixed_visual_review_v3.json'
    assert not output.exists()
    before = ROOT / 'mixed_visual_review_v2.json'
    prior = load(before)
    for p, h in prior['directly_viewed_sheets'].items():
        assert digest(p) == h
    menus = load(ROOT / 'menu_native_v1/group_verification.json')
    names = load(ROOT / 'name_planes_v1/native_name_planes.json')
    assert menus['runtime'] == names['runtime']
    assert menus['captions'] == 7 and names['distinct_current_strings'] == 24
    save(output, {**prior, 'runtime': menus['runtime'],
        'all_names_andcaptions_directly_viewed': True, 'distinct_name_strings': 24,
        'original_direct_visual_receipt': str(before), 'original_direct_visual_receipt_sha256': digest(before)})
    first = ROOT / 'plan_v1/automatic_plans.json'
    final = ROOT / 'plan_v13/automatic_plans.json'
    old = {r['id']: r for r in load(first)['records']}
    new = {r['id']: r for r in load(final)['records']}
    assert old.keys() == new.keys()
    changed = [k for k in old if old[k]['encoded_hex'] != new[k]['encoded_hex']]
    prose = [k for k in old if old[k]['logical_English'] != new[k]['logical_English']]
    assert set(prose) == {'SC2_B251_STYLE_352_212', 'SC2_B251_STYLE_900_214'}
    for k in prose:
        assert old[k]['logical_English'].replace("ceiling's caving in!", "ceiling's collapsing!") == new[k]['logical_English']
    oldpages = sum(r['expected_native_pages'] for r in old.values())
    newpages = sum(r['expected_native_pages'] for r in new.values())
    assert (oldpages, newpages) == (265, 264)
    save(ROOT / 'final_layout_delta_v1.json', dict(initial_plan=str(first), initial_plan_sha256=digest(first),
        final_plan=str(final), final_plan_sha256=digest(final), changed_record_IDs=changed,
        same_prose_wrap_changes=[k for k in changed if k not in prose],
        two_source_faithful_longer_style_synonym_changes=prose,
        old_pages=oldpages, final_pages=newpages, reclaimed_pages=1,
        no_prose_shortened_for_fit=True, physical_width_font_andruntime_unchanged=True, new_credit=0))
    print(dict(changed_layouts=len(changed), wrap_only=len(changed)-len(prose), pages_reclaimed=1))
