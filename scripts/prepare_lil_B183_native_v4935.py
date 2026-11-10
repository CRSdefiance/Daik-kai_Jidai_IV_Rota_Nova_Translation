"""Freeze five B183 roles and both FE objects under the measured native display rules."""
from pathlib import Path
from scripts.prepare_lil_B156_layout_v3705 import derive
from scripts.verify_village_wrap_v608 import read,save
from dk4tool.patch.grand_race_menu_release import sha

ROOT=Path('work/analysis/lil_B183_native_tools_v4935')
if __name__=='__main__':
    assert not ROOT.exists();doc=read('translations/lil_B183_editorial_manuscript_v1.json');source=read(doc['source_context'])
    keys=['source_context','control_contract','actor_voice_contract','branch_proof','source_entry_proof',
        'source_effect_and_predicate_contract','actor_terminology_reconciliation','source_nameplate_consumer_proof','current_C200_source_ownership_proof']
    deps={doc[k]:doc[k+'_sha256'] for k in keys};hashes=sorted({b[k] for b in source['blocks'] for k in ['clean_block_sha256','current_block_sha256']})
    text='''"""Exact B183 source/current commands,five roles and progressive/FE consumers."""
from dataclasses import replace
from pathlib import Path
import json
from dk4tool.dialogue.profiles import get_dialogue_profile
from dk4tool.patch.grand_race_menu_release import sha
'''
    text+='ARM9_SHA='+repr(source['current_ARM9_sha256'])+'\nBLOCKS=frozenset('+repr(hashes)+')\nSELECTORS=frozenset({85,110,132,148,153})\nDEPENDENCIES='+repr(deps)+'\nCONTROL='+repr(doc['control_contract'])+'\n'
    text+='''
def profile_for(arm,source_block,consumer='progressive'):
    if sha(arm)!=ARM9_SHA or sha(source_block) not in BLOCKS:raise ValueError('Exact B183 source/current block and runtime required')
    for path,digest in DEPENDENCIES.items():
        if sha(Path(path).read_bytes())!=digest:raise ValueError('B183 source contract changed:'+path)
    control=json.loads(Path(CONTROL).read_bytes());cases=control['speech_dispatch_cases']
    if len(cases)!=50 or sum(r['source_selector']==254 for r in cases)!=4:raise ValueError('All25 source/current dispatch pairs required')
    if any(r['resolved_actor_ID'] is not None for r in cases if r['source_selector']==254):raise ValueError('Both FE objects must remain null-actor')
    if control['source_macro_counts']!={'FI':0,'FA':0,'FO':0}:raise ValueError('B183 has no source substitutions')
    base=get_dialogue_profile('lil-opening-editorial-native-v1')
    if consumer=='progressive':
        return replace(base,name='lil-B183-progressive-runtime-bound-v1',leading_speaker_bytes=SELECTORS,
            metrics_source=base.metrics_source+';23 original54020 speeches,five static actors and ten read-only names.153 is progressive Sailor,separate catalogue Retainer,voice4;other four source voices0.28 linear commands,A0008 raw00a0ffff013926a1,C200950,end952. No inferred player identity or relationship. Current V4914 font/guards;native planes need fresh approval.')
    if consumer=='FE-paper':
        return replace(base,name='lil-B183-FE-runtime-bound-v1',leading_speaker_bytes=frozenset({254}),
            metrics_source=base.metrics_source+';two original24310null actor then5473C objects:closing impact sound and prospective Artwork/Basra notice.228x48logical/228x64physical,conservative216px planning. No earlier scene location or earned boom inference. Current native planes need fresh approval.')
    raise ValueError('Unknown B183 consumer')
'''
    profile=Path('dk4tool/dialogue/lil_B183_profile.py');assert not profile.exists();compile(text,str(profile),'exec');profile.write_text(text,encoding='utf-8',newline='\n')
    tools=[derive('dk4tool/dialogue/lil_B181_layout_v1.py','dk4tool/dialogue/lil_B183_layout_v1.py',{
        "{'lil-B181-progressive-runtime-bound-v1':frozenset({166,167,168}),'lil-B181-FE-runtime-bound-v1':frozenset({254})}":
        "{'lil-B183-progressive-runtime-bound-v1':frozenset({85,110,132,148,153}),'lil-B183-FE-runtime-bound-v1':frozenset({254})}",
        'source-bound B181 profile':'source-bound B183 profile'})]
    tools.append(derive('scripts/plan_lil_B181_layout_v4843.py','scripts/plan_lil_B183_layout_v4936.py',{
        'B181':'B183','layout_v4843':'layout_v4936','Plan10':'Plan25','all10_paragraph':'all25_paragraph','len(reports)==10':'len(reports)==25','plans=10':'plans=25'}))
    tools.append(derive('scripts/verify_lil_B181_fonts_v4844.py','scripts/verify_lil_B183_fonts_v4937.py',{
        'B181':'B183','fonts_v4844':'fonts_v4937','voices_v4833':'voices_v4926',
        'len(cases)==len(qa_reports)==10 and macro_calls==80':'len(cases)==len(qa_reports)==25 and macro_calls==200',
        "sum(c['kind']=='system-FE' for c in cases)==1":"sum(c['kind']=='system-FE' for c in cases)==2",
        'blocks[181]':'blocks[183]','blocks[180]':'blocks[182]',
        'for selector in [166,167,168,254]':'for selector in [85,110,132,148,153,254]',
        'format(167 if selector==166 else 166':'format(110 if selector==85 else 85',
        "r['source_selector']==166":"r['source_selector']==85",
        "b'\\x02Japanese','{SPEAKER:02}Hello.'":"b'\\x55Japanese','{SPEAKER:55}Hello.'",
        'assert len(negatives)==20':'assert len(negatives)==24',
        'all10_progressive_FE_native_planes_and80_alignment_cases':'all25_progressive_FE_native_planes_and200_alignment_cases',
        'current_original_macro_alignment_calls=80,progressive_alignment_calls=72,FE_null_actor_alignment_calls=8':
        'current_original_macro_alignment_calls=200,progressive_alignment_calls=184,FE_null_actor_alignment_calls=16',
        'complete_progressive_planes=9,complete_FE_logical_and_physical_planes=1':'complete_progressive_planes=23,complete_FE_logical_and_physical_planes=2',
        'all_four_selectors_preserved':'all_six_selectors_preserved',
        '10 current-font native planes,80 alignment cases and20':'25 current-font native planes,200 alignment cases and24',
        'planes and80 native alignment cases':'planes and200 native alignment cases','two sheets need visual review':'four sheets need visual review'}))
    tools.append(derive('scripts/approve_lil_B181_native_v4845.py','scripts/approve_lil_B183_native_v4938.py',{
        'B181':'B183','native_approval_v4845':'native_approval_v4938','fonts_v4844':'fonts_v4937',
        'all10_progressive_FE_native_planes_and80_alignment_cases':'all25_progressive_FE_native_planes_and200_alignment_cases',
        "len(font['cases'])==10":"len(font['cases'])==25","font['current_original_macro_alignment_calls']==80":"font['current_original_macro_alignment_calls']==200",
        '==(9,1)':'==(23,2)',"len(font['negative_controls'])==20":"len(font['negative_controls'])==24",'blocks[181]':'blocks[183]',
        "len(font['review_sheets'])==2":"len(font['review_sheets'])==4",
        "{'revise':5,'retain-wording':5}":"{'revise':16,'retain-wording':9}",
        "[('progressive',166),('FE-paper',254)]":"[('progressive',85),('FE-paper',254)]",
        'all10':'all25','all80':'all200','source_consumer_negatives=20':'source_consumer_negatives=24',
        'on_two_sheets':'on_four_sheets','five_revisions_and_five_individually_justified_retentions':'sixteen_revisions_and_nine_individually_justified_retentions',
        'explicit_wistful_wish_and_three_audible_sighs_refined':'source_art_judgments_purchase_intentions_candid_shopkeeper_and_discretion_preserved',
        'viewed10-panel':'viewed25-panel','All10':'All25',
        '5 revisions/5 justified retentions,80 alignments,20':'16 revisions/9 justified retentions,200 alignments,24'}))
    ROOT.mkdir(parents=True);save(ROOT/'source_derivation.json',dict(profile=str(profile),profile_sha256=sha(profile.read_bytes()),tools=tools,dependencies=deps,
        source_progressive23_FE2_distinct_roles_and_voice4_preserved=True,no_shared_metric_guard_phrase_exception_or_manual_break_change=True,
        new_emulator_runs=0,new_review_credit=0,full_goal_complete=False))
    print('B183 exact profiles,25-paragraph planner and200 current-native alignment cases prepared;no global display-rule change.')
