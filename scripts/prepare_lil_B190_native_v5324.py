"""Freeze remedy-rumor selectors and conditional source/runtime formatting scope."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import read,save
from dk4tool.patch.grand_race_menu_release import sha
ROOT=Path('work/analysis/lil_B190_native_tools_v5324')
if __name__=='__main__':
    assert not ROOT.exists();doc=read('translations/lil_B190_editorial_manuscript_v1b.json');packet=read(doc['source_context'])
    keys=['source_context','control_contract','actor_voice_contract','branch_proof','source_entry_proof','source_effect_and_predicate_contract','actor_terminology_reconciliation','source_nameplate_consumer_proof']
    deps={doc[k]:doc[k+'_sha256'] for k in keys};predicate='work/analysis/lil_B190_predicate500_v5318/all8_original500_predicate_RNG_ownership_cases.json';deps[predicate]=sha(Path(predicate).read_bytes())
    hashes=sorted({b[k] for b in packet['blocks'] for k in ['clean_block_sha256','current_block_sha256']})
    profile=Path('dk4tool/dialogue/lil_B190_profile.py');assert not profile.exists()
    text='''"""Exact B190 two-actor conditional source/current progressive and FE profile."""
from dataclasses import replace
from pathlib import Path
import json
from dk4tool.dialogue.profiles import get_dialogue_profile
from dk4tool.patch.grand_race_menu_release import sha
'''
    text+='ARM9_SHA='+repr(packet['current_ARM9_sha256'])+'\nBLOCKS=frozenset('+repr(hashes)+')\nSELECTORS=frozenset({119,159})\nDEPENDENCIES='+repr(deps)+'\nCONTROL='+repr(doc['control_contract'])+'\n\n'
    text+='''def profile_for(arm,source_block,consumer='progressive'):
    if sha(arm)!=ARM9_SHA or sha(source_block) not in BLOCKS:raise ValueError('Exact B190 source/current block and runtime required')
    for path,digest in DEPENDENCIES.items():
        if sha(Path(path).read_bytes())!=digest:raise ValueError('B190 source contract changed:'+path)
    control=json.loads(Path(CONTROL).read_bytes());cases=control['speech_dispatch_cases']
    if len(cases)!=34 or sum(r['source_selector']==254 for r in cases)!=2:raise ValueError('All17 source/current dispatch pairs required')
    if any(r['resolved_actor_ID'] is not None for r in cases if r['source_selector']==254):raise ValueError('The FE object must remain null-actor')
    if control['source_macro_counts']!={'FI':0,'FA':0,'FO':0}:raise ValueError('B190 has no source substitutions')
    base=get_dialogue_profile('lil-opening-editorial-native-v1')
    if consumer=='progressive':
        return replace(base,name='lil-B190-progressive-runtime-bound-v1',leading_speaker_bytes=SELECTORS,
            metrics_source=base.metrics_source+';16 original54020 speeches,clean PortWorker119 voice0/progressive Sailor159 voice4,distinct catalogue Retainer159,four read-only name consumers. Hex77/9F are decimal119/159.29 commands,one500 predicate at8,six relatives,three alternatives28/40/52,C200600,end602,two tailzeros. Current V5304 font/guards;fresh native approval required.')
    if consumer=='FE-paper':
        return replace(base,name='lil-B190-FE-runtime-bound-v1',leading_speaker_bytes=frozenset({254}),
            metrics_source=base.metrics_source+';one original24310null actor then5473C object:tentative Medicine/Havana notice.228x48logical/228x64physical,conservative216px planning. Source category13 medicine,fullMedicine/compactMed labels unchanged;no single brand,verified cure,earned boom or earlier location claim;fresh native approval required.')
    raise ValueError('Unknown B190 consumer')
'''
    compile(text,str(profile),'exec');profile.write_text(text,encoding='utf-8',newline='\n')
    rows=[derive('dk4tool/dialogue/lil_B189_layout_v1.py','dk4tool/dialogue/lil_B190_layout_v1.py',{'B189':'B190','frozenset({82,104,113,147})':'frozenset({119,159})'})]
    rows.append(derive('scripts/plan_lil_B189_layout_v5284.py','scripts/plan_lil_B190_layout_v5325.py',{
        'B189':'B190','layout_v5284':'layout_v5325','translations/lil_B189_editorial_manuscript_v1.json':'translations/lil_B190_editorial_manuscript_v1b.json'}))
    rows.append(derive('scripts/verify_lil_B189_fonts_v5285.py','scripts/verify_lil_B190_fonts_v5326.py',{
        'B189':'B190','fonts_v5285':'fonts_v5326','voices_v5274b':'voices_v5315','blocks[189]':'blocks[190]','blocks[188]':'blocks[189]',
        '[82,104,113,147,254]':'[119,159,254]','104 if selector==82 else 82':'159 if selector==119 else 119',"r['source_selector']==82":"r['source_selector']==119",
        "b'\\x82Japanese','{SPEAKER:82}Hello.'":"b'\\x77Japanese','{SPEAKER:77}Hello.'",'len(negatives)==22':'len(negatives)==18',
        'native_source_FI0_FA0_FO0_and_all_five_selectors_preserved':'native_source_FI0_FA0_FO0_and_all_three_selectors_preserved','136 alignment cases and22 source-consumer':'136 alignment cases and18 source-consumer'}))
    rows.append(derive('scripts/approve_lil_B189_native_v5286.py','scripts/approve_lil_B190_native_v5327.py',{
        'B189':'B190','native_approval_v5286':'native_approval_v5327','fonts_v5285':'fonts_v5326',"len(font['negative_controls'])==22":"len(font['negative_controls'])==18",
        'blocks[189]':'blocks[190]',"('progressive',82)":"('progressive',119)",'source_consumer_negatives=22':'source_consumer_negatives=18',
        'source_both_pairs_recent_acquisition_market_claims_irony_short_funds_antecedent_and_tentative_notice_preserved':
        'source_unknown_cause_retail_medicine_reported_one_go_cure_doubt_panacea_reputation_personal_wish_and_tentative_notice_preserved',
        '136 alignments,22 consumer':'136 alignments,18 consumer'}))
    ROOT.mkdir(parents=True);save(ROOT/'prepared_source_bound_native_tools.json',dict(profile=str(profile),profile_sha256=sha(profile.read_bytes()),dependencies=deps,tools=rows,
        source_exact119_159_selectors_and_original_predicate_contract_guarded_before_planning=True,no_inherited_record_specific_boundary_exception=True,
        no_prose_shortening_authored_break_font_width_metric_guard_or_global_weak_word_change=True,new_review_credit=0,new_emulator_runs=0,full_goal_complete=False))
