"""Bind B181 to unchanged current font/geometry and prepare all ten native planes."""
from pathlib import Path
from scripts.prepare_lil_B156_layout_v3705 import derive
from scripts.verify_village_wrap_v608 import read,save
from dk4tool.patch.grand_race_menu_release import sha

ROOT=Path('work/analysis/lil_B181_native_tools_v4842')
if __name__=='__main__':
    assert not ROOT.exists();doc=read('translations/lil_B181_editorial_manuscript_v1.json');source=read(doc['source_context'])
    keys=['source_context','control_contract','actor_voice_contract','branch_proof','source_entry_proof',
        'source_effect_and_predicate_contract','actor_terminology_reconciliation','source_nameplate_consumer_proof','current_C200_source_ownership_proof']
    deps={doc[k]:doc[k+'_sha256'] for k in keys};hashes=sorted({b[k] for b in source['blocks'] for k in ['clean_block_sha256','current_block_sha256']})
    original=Path('dk4tool/dialogue/lil_B180_profile.py').read_text(encoding='utf-8')
    a=original.index('ARM9_SHA=');b=original.index('\ndef profile_for',a)
    constants='ARM9_SHA='+repr(source['current_ARM9_sha256'])+'\nBLOCKS=frozenset('+repr(hashes)+')\nSELECTORS=frozenset({166,167,168})\nDEPENDENCIES='+repr(deps)+'\nCONTROL='+repr(doc['control_contract'])+'\n'
    text=original[:a]+constants+original[b:]
    changes={
        'B180':'B181','ten progressive speeches,one impersonal FE and conditional native controls':'nine progressive speeches,one impersonal FE and three linear control leaves',
        'len(cases)!=22':'len(cases)!=20','All eleven source/current dispatch pairs required':'All ten source/current dispatch pairs required',
        ';ten original54020 speeches,Lady166/Lady167,four read-only name paths. No inferred noble rank,marriage or third-person gender.28 commands,ten relative sites,two original500 threshold/RNG predicates,three alternative opaque effects,C200570,end572. Current V4766 font and guards;native planes still need fresh approval.':
        ';nine original54020 speeches,Lady166/Lady167/Lady168,six read-only name paths. No inferred rank,marriage,giver identity or necklace gift provenance.13 commands,A0008,C200390,end392;no predicates or relative sites. Current V4821 font and guards;native planes still need approval.',
        ';one prospective Lisbon Scents-category notice,original24310null actor then5473C.228x48logical/228x64physical,conservative216px planning. No earlier location,earned boom or demand/price inference. Current font native plane still needs fresh approval.':
        ';one prospective Athens Rubies notice,original24310null actor then5473C.228x48logical/228x64physical,conservative216px planning. No earlier location,earned boom or demand/price inference. Current font native plane still needs approval.'}
    import re
    for key in changes:assert key in text,key
    text=re.sub('|'.join(re.escape(k) for k in sorted(changes,key=len,reverse=True)),lambda m:changes[m.group(0)],text)
    profile=Path('dk4tool/dialogue/lil_B181_profile.py');assert not profile.exists();compile(text,str(profile),'exec');profile.write_text(text,encoding='utf-8',newline='\n')
    tools=[derive('dk4tool/dialogue/lil_B180_layout_v1.py','dk4tool/dialogue/lil_B181_layout_v1.py',{
        "{'lil-B180-progressive-runtime-bound-v1':frozenset({166,167}),'lil-B180-FE-runtime-bound-v1':frozenset({254})}":
        "{'lil-B181-progressive-runtime-bound-v1':frozenset({166,167,168}),'lil-B181-FE-runtime-bound-v1':frozenset({254})}",
        'source-bound B180 profile':'source-bound B181 profile'})]
    tools.append(derive('scripts/plan_lil_B180_layout_v4791.py','scripts/plan_lil_B181_layout_v4843.py',{
        'B180':'B181','layout_v4791':'layout_v4843','Plan11':'Plan10','all11_paragraph':'all10_paragraph',
        'len(reports)==11':'len(reports)==10','plans=11':'plans=10'}))
    tools.append(derive('scripts/verify_lil_B180_fonts_v4794.py','scripts/verify_lil_B181_fonts_v4844.py',{
        'B180':'B181','fonts_v4794':'fonts_v4844','voices_v4775':'voices_v4833',
        'len(cases)==len(qa_reports)==11 and macro_calls==88':'len(cases)==len(qa_reports)==10 and macro_calls==80',
        'blocks[180]':'blocks[181]','blocks[179]':'blocks[180]',
        'for selector in [166,167,254]':'for selector in [166,167,168,254]',
        'assert len(negatives)==18':'assert len(negatives)==20',
        'all11_progressive_FE_native_planes_and88_alignment_cases':'all10_progressive_FE_native_planes_and80_alignment_cases',
        'current_original_macro_alignment_calls=88,progressive_alignment_calls=80':'current_original_macro_alignment_calls=80,progressive_alignment_calls=72',
        'complete_progressive_planes=10':'complete_progressive_planes=9','all_three_selectors_preserved':'all_four_selectors_preserved',
        '11 current-font native planes,88 alignment cases and18':'10 current-font native planes,80 alignment cases and20',
        'planes and88 native alignment cases':'planes and80 native alignment cases'}))
    tools.append(derive('scripts/approve_lil_B180_native_v4795.py','scripts/approve_lil_B181_native_v4845.py',{
        'B180':'B181','native_approval_v4795':'native_approval_v4845','fonts_v4794':'fonts_v4844',
        'all11_progressive_FE_native_planes_and88_alignment_cases':'all10_progressive_FE_native_planes_and80_alignment_cases',
        "len(font['cases'])==11":"len(font['cases'])==10","font['current_original_macro_alignment_calls']==88":"font['current_original_macro_alignment_calls']==80",
        '==(10,1)':'==(9,1)',"len(font['negative_controls'])==18":"len(font['negative_controls'])==20",'blocks[180]':'blocks[181]',
        "{'revise':5,'retain-wording':6}":"{'revise':5,'retain-wording':5}",
        'all11':'all10','all88':'all80','source_consumer_negatives=18':'source_consumer_negatives=20',
        'four_narrow_Japanese_English_rowcount_notes_not_other_safety_waivers':'source_English_rowcount_notes_not_other_safety_waivers',
        'five_revisions_and_six_individually_justified_retentions':'five_revisions_and_five_individually_justified_retentions',
        'unsupported_third_person_gender_and_wrong_Spices_category_corrected':'explicit_wistful_wish_and_three_audible_sighs_refined',
        'viewed11-panel':'viewed10-panel','All11':'All10','5 revisions/6 justified retentions,88 alignments,18':'5 revisions/5 justified retentions,80 alignments,20'}))
    ROOT.mkdir(parents=True);save(ROOT/'source_derivation.json',dict(profile=str(profile),profile_sha256=sha(profile.read_bytes()),tools=tools,
        dependencies=deps,no_shared_metric_guard_phrase_exception_or_manual_break_change=True,
        current_ARM9_and_font_identical_to_previously_calibrated_V4766=True,current_B181_actual_display_still_pending=True,
        new_emulator_runs=0,new_review_credit=0,full_goal_complete=False))
    print('Prepared B181 exact profiles,ten-paragraph planner and80 current-native alignment cases;no global display-rule change.')
