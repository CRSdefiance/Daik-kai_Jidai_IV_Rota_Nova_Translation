"""Freeze conditional three-actor progressive/FE formatting with one source FI."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import read,save
from dk4tool.patch.grand_race_menu_release import sha
ROOT=Path('work/analysis/lil_B194_native_tools_v5500')
if __name__=='__main__':
    assert not ROOT.exists();doc=read('translations/lil_B194_editorial_manuscript_v1.json');packet=read(doc['source_context'])
    keys=['source_context','control_contract','actor_voice_contract','branch_proof','source_entry_proof','source_effect_and_predicate_contract','actor_terminology_reconciliation','source_nameplate_consumer_proof']
    deps={doc[k]:doc[k+'_sha256'] for k in keys};hashes=sorted({b[k] for b in packet['blocks'] for k in ['clean_block_sha256','current_block_sha256']})
    profile=Path('dk4tool/dialogue/lil_B194_profile.py');assert not profile.exists()
    text='''"""Exact B194 source/current native profile,with default FI-to-Lil binding."""
from dataclasses import replace
from pathlib import Path
import json
from dk4tool.dialogue.profiles import get_dialogue_profile
from dk4tool.patch.grand_race_menu_release import sha
'''
    text+='ARM9_SHA='+repr(packet['current_ARM9_sha256'])+'\nBLOCKS=frozenset('+repr(hashes)+')\nSELECTORS=frozenset({6,117,156})\nDEPENDENCIES='+repr(deps)+'\nCONTROL='+repr(doc['control_contract'])+'\nTERMS='+repr(doc['actor_terminology_reconciliation'])+'\n\n'
    text+='''def profile_for(arm,source_block,consumer='progressive'):
    if sha(arm)!=ARM9_SHA or sha(source_block) not in BLOCKS:raise ValueError('Exact B194 source/current block and runtime required')
    for path,digest in DEPENDENCIES.items():
        if sha(Path(path).read_bytes())!=digest:raise ValueError('B194 source contract changed:'+path)
    control=json.loads(Path(CONTROL).read_bytes());cases=control['speech_dispatch_cases']
    if len(cases)!=22 or sum(r['source_selector']==254 for r in cases)!=2:raise ValueError('All11 source/current dispatch pairs required')
    if any(r['resolved_actor_ID'] is not None for r in cases if r['source_selector']==254):raise ValueError('FE must remain null actor')
    if control['source_macro_counts']!={'FI':1,'FA':0,'FO':0}:raise ValueError('B194 has exactly one source FI')
    terms=json.loads(Path(TERMS).read_bytes())
    if terms['FI_default_expansion']!='Lil' or terms['FI_default_ASCII_bytes']!=3:raise ValueError('Exact current default FI name/parity required')
    if any(bytes.fromhex(r['output_hex'])!=b'Lil' for r in terms['original_default_captain_FI_four_alignment_cases']['cases']):raise ValueError('Original FI expansion differs')
    base=get_dialogue_profile('lil-opening-editorial-native-v1')
    if consumer=='progressive':
        return replace(base,name='lil-B194-progressive-runtime-bound-v1',leading_speaker_bytes=SELECTORS,
            metrics_source=base.metrics_source+';10 original54020 speeches,Julio6 voice5/PortWorker117 voice0/Sailor156 voice4,six original names with two owned Julio scratch paths. One FI expands to default Lil in four original alignments;Admiral title is source-explicit.21 commands,one conditional,four spans,resource42,two C200 and one end. Current V5478 font/guards. Custom name lengths and actual scene remain outside this proof.')
    if consumer=='FE-paper':
        return replace(base,name='lil-B194-FE-runtime-bound-v1',leading_speaker_bytes=frozenset({254}),
            metrics_source=base.metrics_source+';one original24310 null actor then5473C prospective Sake/Hangzhou notice.228x48logical/228x64physical,conservative216px planning. Sake37 and one Hangzhou alias unchanged;no earned fashion or earlier location claim;fresh approval required.')
    raise ValueError('Unknown B194 consumer')
'''
    compile(text,str(profile),'exec');profile.write_text(text,encoding='utf-8',newline='\n')
    rows=[derive('dk4tool/dialogue/lil_B193_layout_v1.py','dk4tool/dialogue/lil_B194_layout_v1.py',{'B193':'B194','frozenset({166,167,168})':'frozenset({6,117,156})'})]
    rows.append(derive('scripts/plan_lil_B193_layout_v5458.py','scripts/plan_lil_B194_layout_v5501.py',{
        'B193':'B194','layout_v5458':'layout_v5501','Plan15':'Plan11','all15':'all11','len(reports)==15':'len(reports)==11','plans=15':'plans=11'}))
    src=Path('scripts/verify_lil_B193_fonts_v5459.py');t=src.read_text(encoding='utf-8')
    old='    assert len(negatives)==20'
    extra="""    active=next(r for r in doc['records'] if '{MACRO:FI}' in r['english'])
    active_profile=profile_for(arm,blocks[194]);source_active=bytes.fromhex(active['source_hex'])
    for label,target in [('dropped-source-FI',active['english'].replace('{MACRO:FI}','')),
        ('changed-source-FI',active['english'].replace('{MACRO:FI}','{MACRO:FO}')),
        ('duplicated-source-FI',active['english']+' {MACRO:FI}'),
        ('literal-name-replaces-source-FI',active['english'].replace('{MACRO:FI}','Lil'))]:
        reject(label,lambda target=target:encode_relocatable_dialogue(source_active,target,active_profile))
    assert len(negatives)==24"""
    rows.append(derive(src,'scripts/verify_lil_B194_fonts_v5502.py',{
        old:extra,'B193':'B194','fonts_v5459':'fonts_v5502','voices_v5448':'voices_v5490','blocks[193]':'blocks[194]','blocks[192]':'blocks[193]',
        '[166,167,168,254]':'[6,117,156,254]','167 if selector==166 else 166':'117 if selector==6 else 6',"r['source_selector']==166":"r['source_selector']==117",
        "b'\\xa6Japanese','{SPEAKER:A6}Hello.'":"b'\\x75Japanese','{SPEAKER:75}Hello.'",'len(cases)==len(qa_reports)==15':'len(cases)==len(qa_reports)==11',
        'and120 native':'and88 native','macro_calls==120':'macro_calls==88','and120_alignment':'and88_alignment','alignment_calls=120':'alignment_calls=88',
        'progressive_alignment_calls=112':'progressive_alignment_calls=80','complete_progressive_planes=14':'complete_progressive_planes=10','all15':'all11','All15':'All11',
        'and20 source-consumer':'and24 source-consumer','120 alignment cases':'88 alignment cases','native_source_FI0_FA0_FO0':'native_source_FI1_FA0_FO0'}))
    rows.append(derive('scripts/approve_lil_B193_native_v5460.py','scripts/approve_lil_B194_native_v5503.py',{
        'B193':'B194','native_approval_v5460':'native_approval_v5503','fonts_v5459':'fonts_v5502',"len(font['cases'])==15":"len(font['cases'])==11",
        "font['current_original_macro_alignment_calls']==120":"font['current_original_macro_alignment_calls']==88",'and120_alignment':'and88_alignment','==(14,1)':'==(10,1)',
        "len(font['negative_controls'])==20":"len(font['negative_controls'])==24",'blocks[193]':'blocks[194]',
        "{'revise':8,'retain-wording':7}":"{'revise':4,'retain-wording':7}","('progressive',166)":"('progressive',117)",
        "        assert not any(s in raw[1:] for s in [b'FI',b'FA',b'FO']) and '{MACRO:' not in row['english']":
        "        assert [(m,raw[1:].count(m.encode())) for m in ['FI','FA','FO']]==[(m,row['english'].count('{MACRO:'+m+'}')) for m in ['FI','FA','FO']]",
        "macro_ascii_lengths={**p.macro_ascii_lengths,'FO':10}":"macro_ascii_lengths={**p.macro_ascii_lengths,'FI':4}",
        'all15':'all11','All15':'All11','viewed15-panel':'viewed11-panel','eight_revisions_and_seven_individually_justified_retentions':'four_revisions_and_seven_individually_justified_retentions',
        'source_cooking_price_concern_reported_spice_classification_teaching_offer_and_explicit_friendship_preserved':'source_sake_gossip_rice_hearsay_causal_invitation_conditional_Julio_belief_purchase_intention_and_FI_title_preserved',
        'all120_current_native':'all88_current_native','source_consumer_negatives=20':'source_consumer_negatives=24','8 revisions/7 justified retentions,120 alignments,20 consumer':'4 revisions/7 justified retentions,88 alignments,24 consumer'}))
    ROOT.mkdir(parents=True);save(ROOT/'prepared_exact_source_native_tools.json',dict(profile=str(profile),profile_sha256=sha(profile.read_bytes()),dependencies=deps,tools=rows,
        source_three_actors_21_conditional_commands_resource42_two_C200_and_one_FI_bound=True,no_inherited_boundary_exception=True,
        default_FI_name_alignment_bound_not_all_custom_names_or_actual_conditional_gameplay=True,no_manual_break_or_font_width_metric_guard_change=True,no_credit=True,full_goal_complete=False))
