"""Freeze four source selectors and prepare every native text plane and alignment."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import read,save
from dk4tool.patch.grand_race_menu_release import sha
ROOT=Path('work/analysis/lil_B189_native_tools_v5283')
if __name__=='__main__':
    assert not ROOT.exists();doc=read('translations/lil_B189_editorial_manuscript_v1.json');packet=read(doc['source_context'])
    keys=['source_context','control_contract','actor_voice_contract','branch_proof','source_entry_proof','source_effect_and_predicate_contract','actor_terminology_reconciliation','source_nameplate_consumer_proof']
    deps={doc[k]:doc[k+'_sha256'] for k in keys};hashes=sorted({b[k] for b in packet['blocks'] for k in ['clean_block_sha256','current_block_sha256']})
    profile=Path('dk4tool/dialogue/lil_B189_profile.py');assert not profile.exists()
    text='''"""Exact B189 four-actor source/current progressive and null-actor FE profile."""
from dataclasses import replace
from pathlib import Path
import json
from dk4tool.dialogue.profiles import get_dialogue_profile
from dk4tool.patch.grand_race_menu_release import sha
'''
    text+='ARM9_SHA='+repr(packet['current_ARM9_sha256'])+'\nBLOCKS=frozenset('+repr(hashes)+')\nSELECTORS=frozenset({82,104,113,147})\nDEPENDENCIES='+repr(deps)+'\nCONTROL='+repr(doc['control_contract'])+'\n\n'
    text+='''def profile_for(arm,source_block,consumer='progressive'):
    if sha(arm)!=ARM9_SHA or sha(source_block) not in BLOCKS:raise ValueError('Exact B189 source/current block and runtime required')
    for path,digest in DEPENDENCIES.items():
        if sha(Path(path).read_bytes())!=digest:raise ValueError('B189 source contract changed:'+path)
    control=json.loads(Path(CONTROL).read_bytes());cases=control['speech_dispatch_cases']
    if len(cases)!=34 or sum(r['source_selector']==254 for r in cases)!=2:raise ValueError('All17 source/current dispatch pairs required')
    if any(r['resolved_actor_ID'] is not None for r in cases if r['source_selector']==254):raise ValueError('The FE object must remain null-actor')
    if control['source_macro_counts']!={'FI':0,'FA':0,'FO':0}:raise ValueError('B189 has no source substitutions')
    base=get_dialogue_profile('lil-opening-editorial-native-v1')
    if consumer=='progressive':
        return replace(base,name='lil-B189-progressive-runtime-bound-v1',leading_speaker_bytes=SELECTORS,
            metrics_source=base.metrics_source+';16 original54020 speeches,clean Shopkeeper82/Trader104/PortWorker113/Guildmaster147,all voice0,eight read-only name consumers. Hex selectors52/68/71/93 are decimal82/104/113/147.20 linear commands,A0008 raw00a0ffff012a05a1,C200764,end766,two tailzeros,no predicates/relative sites. Current V5263 font/guards;fresh native approval required.')
    if consumer=='FE-paper':
        return replace(base,name='lil-B189-FE-runtime-bound-v1',leading_speaker_bytes=frozenset({254}),
            metrics_source=base.metrics_source+';one original24310null actor then5473C object:tentative Ceramics/Hamburg notice.228x48logical/228x64physical,conservative216px planning. Ceramics is source collective;commodity42 legacy UI China stays unchanged without Chinese-origin claim. No earned boom or earlier location claim;fresh native approval required.')
    raise ValueError('Unknown B189 consumer')
'''
    compile(text,str(profile),'exec');profile.write_text(text,encoding='utf-8',newline='\n')
    rows=[derive('dk4tool/dialogue/lil_B188_layout_v1.py','dk4tool/dialogue/lil_B189_layout_v1.py',{'B188':'B189','frozenset({130,150})':'frozenset({82,104,113,147})'})]
    rows.append(derive('scripts/plan_lil_B188_layout_v5243.py','scripts/plan_lil_B189_layout_v5284.py',{
        'B188':'B189','layout_v5243':'layout_v5284','Plan11':'Plan17','all11':'all17','len(reports)==11':'len(reports)==17','plans=11':'plans=17'}))
    rows.append(derive('scripts/verify_lil_B188_fonts_v5244.py','scripts/verify_lil_B189_fonts_v5285.py',{
        'B188':'B189','fonts_v5244':'fonts_v5285','voices_v5233':'voices_v5274b',
        'len(cases)==len(qa_reports)==11 and macro_calls==88':'len(cases)==len(qa_reports)==17 and macro_calls==136',
        'blocks[188]':'blocks[189]','blocks[187]':'blocks[188]','[130,150,254]':'[82,104,113,147,254]',
        '150 if selector==130 else 130':'104 if selector==82 else 82',"r['source_selector']==130":"r['source_selector']==82",
        'all11_progressive_FE_native_planes_and88_alignment_cases':'all17_progressive_FE_native_planes_and136_alignment_cases',
        'current_original_macro_alignment_calls=88,progressive_alignment_calls=80,FE_null_actor_alignment_calls=8':
        'current_original_macro_alignment_calls=136,progressive_alignment_calls=128,FE_null_actor_alignment_calls=8',
        'complete_progressive_planes=10':'complete_progressive_planes=16','len(negatives)==18':'len(negatives)==22',
        'native_source_FI0_FA0_FO0_and_all_three_selectors_preserved':'native_source_FI0_FA0_FO0_and_all_five_selectors_preserved',
        'B188 current-font progressive/FE planes and88 native alignment cases':'B189 current-font progressive/FE planes and136 native alignment cases',
        'All11 current-font native planes,88 alignment cases and18 source-consumer negatives pass;two sheets':'All17 current-font native planes,136 alignment cases and22 source-consumer negatives pass;three sheets'}))
    rows.append(derive('scripts/approve_lil_B188_native_v5245.py','scripts/approve_lil_B189_native_v5286.py',{
        'B188':'B189','native_approval_v5245':'native_approval_v5286','fonts_v5244/all11':'fonts_v5285/all17','and88_alignment_cases':'and136_alignment_cases',
        "len(font['cases'])==11":"len(font['cases'])==17","font['current_original_macro_alignment_calls']==88":"font['current_original_macro_alignment_calls']==136",'==(10,1)':'==(16,1)',
        "len(font['negative_controls'])==18":"len(font['negative_controls'])==22","len(font['review_sheets'])==2":"len(font['review_sheets'])==3",
        'blocks[188]':'blocks[189]',"{'revise':4,'retain-wording':7}":"{'revise':10,'retain-wording':7}","('progressive',130)":"('progressive',82)",
        'all11':'all17','viewed11-panel':'viewed17-panel','All11':'All17','on_two_sheets':'on_three_sheets','four_revisions_and_seven':'ten_revisions_and_seven',
        'source_consumer_negatives=18':'source_consumer_negatives=22',
        'source_giyaman_glass_praise_conjecture_collection_decision_order_formal_compliance_and_tentative_notice_preserved':
        'source_both_pairs_recent_acquisition_market_claims_irony_short_funds_antecedent_and_tentative_notice_preserved',
        'all88_current':'all136_current','4 revisions/7 justified retentions,88 alignments,18 consumer':'10 revisions/7 justified retentions,136 alignments,22 consumer'}))
    ROOT.mkdir(parents=True);save(ROOT/'prepared_source_bound_native_tools.json',dict(profile=str(profile),profile_sha256=sha(profile.read_bytes()),dependencies=deps,tools=rows,
        source_exact82_104_113_147_selectors_guarded_before_planning=True,no_inherited_record_specific_boundary_exception=True,
        no_prose_shortening_authored_break_font_width_metric_guard_or_global_weak_word_change=True,new_review_credit=0,new_emulator_runs=0,full_goal_complete=False))
