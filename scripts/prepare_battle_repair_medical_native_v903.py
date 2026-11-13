"""Reviewed native previews and explicit source-preserving release/audit successors."""

from copy import deepcopy
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.prepare_battle_repair_medical_prose_v901 import MANUSCRIPT,IDS
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/battle_repair_medical_v904')
PRODUCTION=Path('translations/battle_repair_medical_editorial_manuscript_v2.json')


def replace(text,old,new):
    assert old in text,old
    return text.replace(old,new)


def main():
    ROOT.mkdir(parents=True,exist_ok=True)
    font_path=Path('work/analysis/battle_repair_medical_v902/native_font_proof.json');fonts=read(font_path)
    assert fonts['manuscript_sha256']==sha(MANUSCRIPT.read_bytes())
    assert tuple(c['message_id'] for c in fonts['cases'])==IDS
    for c in fonts['cases']:assert sha(Path(c['preview']).read_bytes())==c['preview_sha256']
    visual=Path('work/analysis/battle_repair_medical_v902/visual_review.json')
    visual_data={'native_font_proof':str(font_path),'native_font_proof_sha256':sha(font_path.read_bytes()),
        'review_sheet':fonts['review_sheet'],'review_sheet_sha256':fonts['review_sheet_sha256'],
        'all24_previews_visually_reviewed':True,'native_IDs':list(IDS),'visual_review_pending':False,
        'findings':'All24 complete native body previews reviewed. Rows start at x0;all words and punctuation fit216x36,including full36-cell1600/1615 lines,complete ASCII initial I1610 and full33-cell emergency-repair continuation after odd25-character1605 first row. No split words,padding gaps,stray text or extra pages. Actual scenes and normal transitions remain required.',
        'CPU_only_font_scope_no_actual_gameplay_credit':True,'full_goal_complete':False}
    if visual.exists():assert read(visual)==visual_data
    else:save(visual,visual_data)
    doc=deepcopy(read(MANUSCRIPT));doc['reviewed_research_manuscript']=str(MANUSCRIPT)
    doc['reviewed_research_manuscript_sha256']=sha(MANUSCRIPT.read_bytes())
    for key,p in [('native_font_proof',font_path),('visual_review_proof',visual)]:doc[key]=str(p);doc[key+'_sha256']=sha(p.read_bytes())
    doc['formatting_review_pending']=False;doc['review_gates']=['source','context','localization','naturalness','formatting']
    doc['status']='24-source-prose-native-font-and-visual-reviewed-registered-release-and-actual-pending'
    for r in doc['records']:r['review']['formatting']=True
    if PRODUCTION.exists():assert read(PRODUCTION)==doc
    else:save(PRODUCTION,doc)
    provenance=[]
    source=Path('dk4tool/patch/gunnery_deck_editorial.py');before=source.read_bytes();text=before.decode('utf-8').replace('\r\n','\n')
    for old,new in [
        ('from dk4tool.patch.sails_boarding_editorial import current_entries as previous_entries','from dk4tool.patch.battle_personal_editorial import current_entries as previous_entries'),
        ('gunnery_deck','battle_repair_medical'),('battle_repair_medical_layout_v887','battle_repair_medical_layout_v902'),
        ('range(1547,1571)','range(1596,1620)'),
        ('5b72c41ff2c0d060c2d30144e9b67b71d523fab08883b34da8beb66b43fde6ce','4168b52812ce30b8d03ccb6fe0f9df8b1caff57071c477f5a0962a1ea3fae135'),
        ('c00b3cd02509c214a06ffcab127464c75ef4636e48e537798f634baa43d00415','1c2382455732761a6bb569bfb89ffe9afacefe133d111147dd62c75cffad59bd'),
        ('deck-gunnery-deck-visible-v1','deck-battle-repair-medical-visible-v1'),
        ('dk4-gunnery-deck-editorial-v1','dk4-battle-repair-medical-editorial-v1'),
        ('complete_ASCII_initial_I1561_empty_stomach_and_mentor_words_pass','complete_ASCII_initial_I1610_and_all_source_words_pass')]:
        text=replace(text,old,new)
    old="    assert len(context['all50_original_role_helper_selections'])==50\n    assert {r['selected_message_ID'] for r in context['all50_original_role_helper_selections']}==set(IDS)"
    new="""    cases=context['all150_original_battle_helper_main_and_ordinary_control_selections'];assert len(cases)==150
    battle=[r for r in cases if r['case']!='main_ordinary_working_control']
    ordinary=[r for r in cases if r['case']=='main_ordinary_working_control']
    assert len(battle)==100 and len(ordinary)==50
    assert {r['selected_message_ID'] for r in battle}==set(IDS)
    assert all(r['isolated_CPU_mode_fields8_12']==[0,1] for r in battle)
    assert all(r['isolated_CPU_mode_fields8_12']==[0,0] for r in ordinary)
    for r in cases:
        role=r['source_role_type'];assert role in (13,14)
        suffix=8+r['actor_ID'] if r['actor_ID']<4 else r['native_voice_class']
        first=(1386 if role==13 else 1398) if r['case']=='main_ordinary_working_control' else (1596 if role==13 else 1608)
        assert r['selected_message_ID']==first+suffix"""
    text=replace(text,old,new)
    old="""    terms=read(doc['native_pronoun_proof']);assert terms['source1561_IC_plus_plural_ra_means_our_ship']
    assert len(terms['all25_current_and_clean_parser_control_cases'])==25 and terms['native_actor14_given_name']=='Emilio'
    assert terms['source1561_hex']==next(r['source_hex'] for r in doc['records'] if r['message_id']==1561)"""
    new="""    terms=read(doc['native_pronoun_proof']);assert terms['IC_is_first_person_not_actor_name']
    assert terms['source1610_means_I_am_here_so_do_not_worry']
    assert len(terms['all25_current_and_clean_parser_control_cases'])==25
    assert terms['source1610_hex']==next(r['source_hex'] for r in doc['records'] if r['message_id']==1610)"""
    text=replace(text,old,new)
    text=replace(text,"'bitmap_and_input_guards_exact','all_body_ink_inside_registered216x36_crop'","'bitmap_and_input_guards_exact','all_body_ink_inside_registered216x36_crop','original_working_selector_selected_battle_message'")
    assert 'source1561' not in text and 'sails_boarding_editorial import' not in text
    target=Path('dk4tool/patch/battle_repair_medical_editorial.py');assert not target.exists()
    with target.open('x',encoding='utf-8') as f:f.write(text)
    assert source.read_bytes()==before
    provenance.append({'source':str(source),'source_before_sha256':sha(before),'source_after_sha256':sha(source.read_bytes()),
        'source_unchanged':True,'successor':str(target),'successor_sha256':sha(target.read_bytes())})
    source=Path('scripts/audit_gunnery_deck_native_v888.py');before=source.read_bytes();text=before.decode('utf-8').replace('\r\n','\n')
    for old,new in [('gunnery_deck','battle_repair_medical'),('battle_repair_medical_layout_v887','battle_repair_medical_layout_v902'),
        ('probe_battle_repair_medical_fonts_v887','probe_battle_repair_medical_fonts_v902'),
        ('deck-gunnery-deck-visible-v1','deck-battle-repair-medical-visible-v1'),
        ('all50_original_role_helper_selections','all150_original_battle_helper_main_and_ordinary_control_selections'),
        ('==50','==150'),('Gunnery and deck cleaning native-consumer audit','Battle repair and medical native-consumer audit')]:
        text=replace(text,old,new)
    target=Path('scripts/audit_battle_repair_medical_native_v904.py');assert not target.exists()
    with target.open('x',encoding='utf-8') as f:f.write(text)
    assert source.read_bytes()==before
    provenance.append({'source':str(source),'source_before_sha256':sha(before),'source_after_sha256':sha(source.read_bytes()),
        'source_unchanged':True,'successor':str(target),'successor_sha256':sha(target.read_bytes())})
    save(ROOT/'native_successor_provenance.json',{'files':provenance,'all_source_hashes_unchanged':True,
        'producer_sha256':sha(Path(__file__).read_bytes())})
    print('All24 native previews reviewed;production manuscript and strict battle release/audit successors created.',flush=True)


if __name__=='__main__':main()
