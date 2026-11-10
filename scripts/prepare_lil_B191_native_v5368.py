"""Freeze exact source/runtime profile and automatic native layout gates for B191."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import read,save
from dk4tool.patch.grand_race_menu_release import sha
ROOT=Path('work/analysis/lil_B191_native_tools_v5368')
if __name__=='__main__':
    assert not ROOT.exists();doc=read('translations/lil_B191_editorial_manuscript_v1.json');packet=read(doc['source_context'])
    keys=['source_context','control_contract','actor_voice_contract','branch_proof','source_entry_proof','source_effect_and_predicate_contract','actor_terminology_reconciliation','source_nameplate_consumer_proof']
    deps={doc[k]:doc[k+'_sha256'] for k in keys};predicate='work/analysis/lil_B191_predicates_v5362/all24_original_mixed_predicate_RNG_ownership_cases.json';deps[predicate]=sha(Path(predicate).read_bytes())
    hashes=sorted({b[k] for b in packet['blocks'] for k in ['clean_block_sha256','current_block_sha256']})
    profile=Path('dk4tool/dialogue/lil_B191_profile.py');assert not profile.exists()
    text='''"""Exact B191 two-actor mixed-predicate progressive/FE formatting profile."""
from dataclasses import replace
from pathlib import Path
import json
from dk4tool.dialogue.profiles import get_dialogue_profile
from dk4tool.patch.grand_race_menu_release import sha
'''
    text+='ARM9_SHA='+repr(packet['current_ARM9_sha256'])+'\nBLOCKS=frozenset('+repr(hashes)+')\nSELECTORS=frozenset({86,154})\nDEPENDENCIES='+repr(deps)+'\nCONTROL='+repr(doc['control_contract'])+'\n\n'
    text+='''def profile_for(arm,source_block,consumer='progressive'):
    if sha(arm)!=ARM9_SHA or sha(source_block) not in BLOCKS:raise ValueError('Exact B191 source/current block and runtime required')
    for path,digest in DEPENDENCIES.items():
        if sha(Path(path).read_bytes())!=digest:raise ValueError('B191 source contract changed:'+path)
    control=json.loads(Path(CONTROL).read_bytes());cases=control['speech_dispatch_cases']
    if len(cases)!=26 or sum(r['source_selector']==254 for r in cases)!=2:raise ValueError('All13 source/current dispatch pairs required')
    if any(r['resolved_actor_ID'] is not None for r in cases if r['source_selector']==254):raise ValueError('FE must remain null actor')
    if control['source_macro_counts']!={'FI':0,'FA':0,'FO':0}:raise ValueError('B191 has no source substitutions')
    base=get_dialogue_profile('lil-opening-editorial-native-v1')
    if consumer=='progressive':
        return replace(base,name='lil-B191-progressive-runtime-bound-v1',leading_speaker_bytes=SELECTORS,
            metrics_source=base.metrics_source+';12 original54020 speeches,Shopkeeper86 voice0/Sailor154 voice4,distinct full Retainer154,four original read-only names. Hex56/9A equal decimal86/154.38 commands,three500/700/500 predicates at8/28/76,16relatives,four alternatives and no-effect paths,C200728,end730,two tailzeros. Current V5346 font/guards;fresh approval required.')
    if consumer=='FE-paper':
        return replace(base,name='lil-B191-FE-runtime-bound-v1',leading_speaker_bytes=frozenset({254}),
            metrics_source=base.metrics_source+';one original24310null actor then5473C:prospective Dyes/Calicut notice.228x48logical/228x64physical,conservative216px planning. Category14 Dyes/two Calicut aliases unchanged. No single pigment,earned fashion,earlier location or guaranteed profit inferred;fresh approval required.')
    raise ValueError('Unknown B191 consumer')
'''
    compile(text,str(profile),'exec');profile.write_text(text,encoding='utf-8',newline='\n')
    rows=[derive('dk4tool/dialogue/lil_B190_layout_v1.py','dk4tool/dialogue/lil_B191_layout_v1.py',{'B190':'B191','frozenset({119,159})':'frozenset({86,154})'})]
    rows.append(derive('scripts/plan_lil_B190_layout_v5325.py','scripts/plan_lil_B191_layout_v5369.py',{
        'B190':'B191','layout_v5325':'layout_v5369','editorial_manuscript_v1b':'editorial_manuscript_v1','Plan17':'Plan13','all17':'all13','len(reports)==17':'len(reports)==13','plans=17':'plans=13',
    }))
    rows.append(derive('scripts/verify_lil_B190_fonts_v5326.py','scripts/verify_lil_B191_fonts_v5370.py',{
        'B190':'B191','fonts_v5326':'fonts_v5370','voices_v5315':'voices_v5357','blocks[190]':'blocks[191]','blocks[189]':'blocks[190]',
        '[119,159,254]':'[86,154,254]','159 if selector==119 else 119':'154 if selector==86 else 86',"r['source_selector']==119":"r['source_selector']==86",
        "b'\\x77Japanese','{SPEAKER:77}Hello.'":"b'\\x56Japanese','{SPEAKER:56}Hello.'",
        'len(cases)==len(qa_reports)==17':'len(cases)==len(qa_reports)==13','136':'104','progressive_alignment_calls=128':'progressive_alignment_calls=96',
        'complete_progressive_planes=16':'complete_progressive_planes=12','all17':'all13','All17':'All13','three sheets need':'two sheets need',
    }))
    rows.append(derive('scripts/approve_lil_B190_native_v5327.py','scripts/approve_lil_B191_native_v5371.py',{
        'B190':'B191','native_approval_v5327':'native_approval_v5371','fonts_v5326':'fonts_v5370','len(font[\'cases\'])==17':'len(font[\'cases\'])==13',
        '136':'104','==(16,1)':'==(12,1)',"len(font['review_sheets'])==3":"len(font['review_sheets'])==2",'blocks[190]':'blocks[191]',
        "{'revise':10,'retain-wording':7}":"{'revise':5,'retain-wording':8}","('progressive',119)":"('progressive',86)",
        'all17':'all13','All17':'All13','viewed17-panel':'viewed13-panel','on_three_sheets':'on_two_sheets',
        'ten_revisions_and_seven_individually_justified_retentions':'five_revisions_and_eight_individually_justified_retentions',
        'source_unknown_cause_retail_medicine_reported_one_go_cure_doubt_panacea_reputation_personal_wish_and_tentative_notice_preserved':'source_color_competitor_buyout_urgency_popularity_scarcity_and_conditional_profit_claims_repeated_doubt_and_tentative_notice_preserved',
        '10 revisions/7 justified retentions':'5 revisions/8 justified retentions',
    }))
    ROOT.mkdir(parents=True);save(ROOT/'prepared_exact_source_native_tools.json',dict(profile=str(profile),profile_sha256=sha(profile.read_bytes()),dependencies=deps,tools=rows,
        source_selectors86_154_three_mixed_predicates16_branches_and_no_effect_paths_guarded=True,
        no_record_specific_boundary_exception_font_width_metric_guard_or_manual_break_change=True,no_credit=True,full_goal_complete=False))
