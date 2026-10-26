"""Every current layout through complete native font pagination,including zero-origin64."""
from pathlib import Path
from scripts.verify_village_wrap_v608 import read,save
from dk4tool.patch.grand_race_menu_release import sha
source=Path('scripts/verify_tavern_fonts_v2189.py').read_text()
for old,new in(('tavern_fonts_v2189','ceremony_fonts_v2269'),('tavern_layouts_v2188/all63_current_native_layouts.json','ceremony_layouts_v2268/all52_current_native_layouts.json'),("matrix['case_count']==67454","matrix['case_count']==202"),('len(fonts)==310','len(fonts)==202'),('set(range(820,883))','set([64,289,290,291,293,294,295,*range(1200,1245)])'),('all63','all52'),('all67454','all202'),('all310','all202')):
    assert old in source;source=source.replace(old,new)
old=";assert plane==independent_font(arm,kanji,case['lines'])and[e['code']for e in events if e['code']!=32]==glyph_codes(text)"
new=";expected=independent_font(arm,kanji,case['lines']);expected=(b''.join(expected[y*228+6:(y+1)*228]+bytes(6)for y in range(64))if case['message_ID']==64 else expected);assert plane==expected and[e['code']for e in events if e['code']!=32]==glyph_codes(text)"
assert source.count(old)==1;source=source.replace(old,new)
env={'__name__':'__main__','__file__':__file__};exec(compile(source,__file__,'exec'),env)
proof=read(env['ROOT']/'all52_native_font_pagination_and_physical_samples.json');bare,=[r for r in proof['full_font_samples']if r['message_ID']==64];assert bare['native_production_control']['ordered_glyphs'][0]['x']==0
save(env['ROOT']/'font_scope.json',dict(current202_complete_native_pages_for_all52_IDs=True,source_bare64_first_glyph_x0_confirmed=True,all_other51_source_protected_indents_preserved=True,shared_postformat_font_core_geometry=[228,48],metrics=[6,12],source_fixture_current_observed655_not_a_claimed_actual_modal_callback=True,six_modal_result_consumers_and_wrong_parent_controls_separate='work/analysis/ceremony_layouts_v2268/all52_current_native_layouts.json',physical228x64_pitch16_oracle_not_logical_capacity=True,no_new_current_emulator_visit_claim=True,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
