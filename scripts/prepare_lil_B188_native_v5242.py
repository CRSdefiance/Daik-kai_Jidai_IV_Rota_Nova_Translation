"""Freeze exact source/runtime selectors and prepare full paragraph native checks."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import read,save
from dk4tool.patch.grand_race_menu_release import sha
ROOT=Path('work/analysis/lil_B188_native_tools_v5242')
if __name__=='__main__':
    assert not ROOT.exists();doc=read('translations/lil_B188_editorial_manuscript_v1.json');packet=read(doc['source_context'])
    keys=['source_context','control_contract','actor_voice_contract','branch_proof','source_entry_proof','source_effect_and_predicate_contract','actor_terminology_reconciliation','source_nameplate_consumer_proof']
    deps={doc[k]:doc[k+'_sha256'] for k in keys};hashes=sorted({b[k] for b in packet['blocks'] for k in ['clean_block_sha256','current_block_sha256']})
    profile=Path('dk4tool/dialogue/lil_B188_profile.py');assert not profile.exists()
    text='''"""Exact B188 Daimyo/Guildmaster source/runtime progressive and FE profile."""
from dataclasses import replace
from pathlib import Path
import json
from dk4tool.dialogue.profiles import get_dialogue_profile
from dk4tool.patch.grand_race_menu_release import sha
'''
    text+='ARM9_SHA='+repr(packet['current_ARM9_sha256'])+'\nBLOCKS=frozenset('+repr(hashes)+')\nSELECTORS=frozenset({130,150})\nDEPENDENCIES='+repr(deps)+'\nCONTROL='+repr(doc['control_contract'])+'\n\n'
    text+='''def profile_for(arm,source_block,consumer='progressive'):
    if sha(arm)!=ARM9_SHA or sha(source_block) not in BLOCKS:raise ValueError('Exact B188 source/current block and runtime required')
    for path,digest in DEPENDENCIES.items():
        if sha(Path(path).read_bytes())!=digest:raise ValueError('B188 source contract changed:'+path)
    control=json.loads(Path(CONTROL).read_bytes());cases=control['speech_dispatch_cases']
    if len(cases)!=22 or sum(r['source_selector']==254 for r in cases)!=2:raise ValueError('All11 source/current dispatch pairs required')
    if any(r['resolved_actor_ID'] is not None for r in cases if r['source_selector']==254):raise ValueError('The FE object must remain null-actor')
    if control['source_macro_counts']!={'FI':0,'FA':0,'FO':0}:raise ValueError('B188 has no source substitutions')
    base=get_dialogue_profile('lil-opening-editorial-native-v1')
    if consumer=='progressive':
        return replace(base,name='lil-B188-progressive-runtime-bound-v1',leading_speaker_bytes=SELECTORS,
            metrics_source=base.metrics_source+';10 original54020 speeches,clean Daimyo130/Guildmaster150,both voice0,four read-only name consumers.14 linear commands,A0008 raw00a0ffff01293ba1,C200476,end478,two tailzeros,no predicates/relative sites. Current V5219 font/guards;fresh native approval required.')
    if consumer=='FE-paper':
        return replace(base,name='lil-B188-FE-runtime-bound-v1',leading_speaker_bytes=frozenset({254}),
            metrics_source=base.metrics_source+';one original24310null actor then5473C object:tentative Glass/Osaka notice.228x48logical/228x64physical,conservative216px planning. Source giyaman is glossed glass,commodity41. No earlier location or earned boom claim;fresh native approval required.')
    raise ValueError('Unknown B188 consumer')
'''
    compile(text,str(profile),'exec');profile.write_text(text,encoding='utf-8',newline='\n')
    rows=[derive('dk4tool/dialogue/lil_B187_layout_v1.py','dk4tool/dialogue/lil_B188_layout_v1.py',{'B187':'B188','frozenset({87,155})':'frozenset({130,150})'})]
    rows.append(derive('scripts/plan_lil_B187_layout_v5199.py','scripts/plan_lil_B188_layout_v5243.py',{
        'B187':'B188','layout_v5199':'layout_v5243','Plan16':'Plan11','all16':'all11','len(reports)==16':'len(reports)==11','plans=16':'plans=11'}))
    rows.append(derive('scripts/verify_lil_B187_fonts_v5200.py','scripts/verify_lil_B188_fonts_v5244.py',{
        'B187':'B188','fonts_v5200':'fonts_v5244','voices_v5189':'voices_v5233',
        'len(cases)==len(qa_reports)==16 and macro_calls==128':'len(cases)==len(qa_reports)==11 and macro_calls==88',
        'blocks[187]':'blocks[188]','blocks[186]':'blocks[187]','[87,155,254]':'[130,150,254]',
        '155 if selector==87 else 87':'150 if selector==130 else 130',"r['source_selector']==87":"r['source_selector']==130",
        "b'\\x57Japanese','{SPEAKER:57}Hello.'":"b'\\x82Japanese','{SPEAKER:82}Hello.'",
        'all16_progressive_FE_native_planes_and128_alignment_cases':'all11_progressive_FE_native_planes_and88_alignment_cases',
        'current_original_macro_alignment_calls=128,progressive_alignment_calls=120,FE_null_actor_alignment_calls=8':
        'current_original_macro_alignment_calls=88,progressive_alignment_calls=80,FE_null_actor_alignment_calls=8',
        'complete_progressive_planes=15':'complete_progressive_planes=10','B187 current-font progressive/FE planes and128 native alignment cases':'B188 current-font progressive/FE planes and88 native alignment cases',
        'All16 current-font native planes,128 alignment cases':'All11 current-font native planes,88 alignment cases'}))
    rows.append(derive('scripts/approve_lil_B187_native_v5201.py','scripts/approve_lil_B188_native_v5245.py',{
        'B187':'B188','native_approval_v5201':'native_approval_v5245','fonts_v5200/all16':'fonts_v5244/all11','and128_alignment_cases':'and88_alignment_cases',
        "len(font['cases'])==16":"len(font['cases'])==11","font['current_original_macro_alignment_calls']==128":"font['current_original_macro_alignment_calls']==88",'==(15,1)':'==(10,1)',
        'blocks[187]':'blocks[188]',"{'revise':7,'retain-wording':9}":"{'revise':4,'retain-wording':7}","('progressive',87)":"('progressive',130)",
        'all16':'all11','viewed16-panel':'viewed11-panel','All16':'All11','seven_revisions_and_nine':'four_revisions_and_seven',
        'source_reported_remedy_effectiveness_sales_forgotten_name_memory_trigger_search_intentions_and_tentative_notice_preserved':
        'source_giyaman_glass_praise_conjecture_collection_decision_order_formal_compliance_and_tentative_notice_preserved',
        'all128_current':'all88_current','7 revisions/9 justified retentions,128 alignments':'4 revisions/7 justified retentions,88 alignments'}))
    ROOT.mkdir(parents=True);save(ROOT/'prepared_source_bound_native_tools.json',dict(profile=str(profile),profile_sha256=sha(profile.read_bytes()),dependencies=deps,tools=rows,
        source_exact130_150_selector_guard_prepared_before_planning=True,no_inherited_record_specific_boundary_exception=True,
        no_prose_shortening_authored_break_font_width_metric_guard_or_global_weak_word_change=True,new_review_credit=0,new_emulator_runs=0,full_goal_complete=False))
