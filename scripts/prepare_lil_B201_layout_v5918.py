"""Bind exact current name-data runtime and B201 source-specific native display contracts."""
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/lil_B201_layout_tools_v5918')
PROFILE=Path('dk4tool/dialogue/lil_B201_profile.py')

if __name__=='__main__':
    assert not ROOT.exists() and not PROFILE.exists()
    doc=read('translations/lil_B201_editorial_manuscript_v1.json');packet=read(doc['source_context'])
    proof=read('work/analysis/generic_speaker_labels_release_v5895/registered_release_verification.json')
    assert packet['current_ARM9_sha256']==proof['ARM9_sha256'] and proof['only_three_owned_primary_label_prefixes_changed_from_V5872']
    assert proof['every_other_file_story_font_graphic_ARM7_overlay_entry_and_name_field_exact_to_V5872']
    keys=['source_context','actor_voice_contract','control_contract','branch_proof','source_entry_proof','source_effect_and_predicate_contract',
        'source_nameplate_consumer_proof','source_payment_proof','actor_terminology_reconciliation','actual_original_response_paths']
    deps={doc[k]:doc[k+'_sha256'] for k in keys}
    code='''"""Exact B201 complete rigging negotiation,three actors/twoFI/threeFE and both source paths."""
import json
from dataclasses import replace
from pathlib import Path
from dk4tool.dialogue.profiles import get_dialogue_profile
from dk4tool.patch.grand_race_menu_release import sha
ARM9_SHA=ARM_LITERAL
BLOCKS=BLOCK_LITERAL
SELECTORS=frozenset({2,19,105})
DEPENDENCIES=DEPS_LITERAL
CONTROL=CONTROL_LITERAL
TERMS=TERMS_LITERAL

def profile_for(arm,source_block,consumer='progressive'):
    if sha(arm)!=ARM9_SHA or sha(source_block) not in BLOCKS:raise ValueError('Exact B201 source/current block and runtime required')
    for path,digest in DEPENDENCIES.items():
        if sha(Path(path).read_bytes())!=digest:raise ValueError('B201 source contract changed:'+path)
    control=json.loads(Path(CONTROL).read_bytes());cases=control['speech_dispatch_cases']
    if len(cases)!=48 or sum(r['source_selector']==254 for r in cases)!=6:raise ValueError('All24 source/current dispatch pairs required')
    if any(r['resolved_actor_ID'] is not None for r in cases if r['source_selector']==254):raise ValueError('FE must remain null actor')
    if control['source_macro_counts']!={'FI':2,'FA':0,'FO':0}:raise ValueError('B201 has exactly two original FI macros')
    terms=json.loads(Path(TERMS).read_bytes())
    if terms['source_actual_speeches']!=24 or terms['offline_only_speeches']:raise ValueError('Complete24-source-panel evidence required')
    if not terms['source_menu_Buy_decline_order_0_1_both_observed_no_delegation'] or terms['final_native_payment']!=100000:raise ValueError('Original two choice paths and final price required')
    if terms['native_source_voices']!={'2':3,'19':7,'105':0}:raise ValueError('All three source actors/voices required')
    if [r['stat'] for r in terms['source_FE_notices']]!=['Charm','Wits','Spirit']:raise ValueError('Three distinct original system notices required')
    base=get_dialogue_profile('lil-opening-editorial-native-v1')
    if consumer=='progressive':
        return replace(base,name='lil-B201-progressive-runtime-bound-v1',leading_speaker_bytes=SELECTORS,
            metrics_source=base.metrics_source+';21 original54020 speeches,Lil2 voice3/Carlo19 voice7/Trader105 voice0,six original name consumers.44 source commands,one2100,four relative sites,no predicates,one complete end/no tailzeros. V5891 only name-data differs from prior font/runtime;native width,guard,pair phase and four rows unchanged.')
    if consumer=='FE-paper':
        return replace(base,name='lil-B201-FE-runtime-bound-v1',leading_speaker_bytes=frozenset({254}),
            metrics_source=base.metrics_source+';three original24310 null-actor then5473C notices:FI Charm+1,Carlo Wits+1,FI Spirit+1. Current defaultFI expandsLil3.228x48logical/228x64physical,conservative216px planning. Complete source paths observed;English scene and full effect semantics remain separate.')
    raise ValueError('Unknown B201 consumer')
'''
    for a,b in {'ARM_LITERAL':repr(packet['current_ARM9_sha256']),'BLOCK_LITERAL':repr({packet['blocks'][0][k] for k in ['clean_block_sha256','current_block_sha256']}),
        'DEPS_LITERAL':repr(deps),'CONTROL_LITERAL':repr(doc['control_contract']),'TERMS_LITERAL':repr(doc['actor_terminology_reconciliation'])}.items():
        assert a in code;code=code.replace(a,b)
    compile(code,str(PROFILE),'exec');PROFILE.write_text(code,encoding='utf-8',newline='\n')
    tools=[]
    tools.append(derive('scripts/lil_current_font_oracles_v4792.py','scripts/lil_current_font_oracles_v5918.py',{
        "CURRENT_ARM9='39b11636e9b9904f96e18691154c813ebcad6e61647db412fa60b7344221b4a1'":"CURRENT_ARM9="+repr(packet['current_ARM9_sha256']),
        'Exact V4766 font oracles':'Exact V5891 name-data-only successor font oracles',
        "B180's actual FE visit is pending.":'New B201 English FE observation remains separate;earlier source geometry is retained.'}))
    tools.append(derive('dk4tool/dialogue/lil_B200_layout_v2.py','dk4tool/dialogue/lil_B201_layout_v1.py',{
        'B200':'B201','frozenset({19,172})':'frozenset({2,19,105})',
        '# Preserve the complete B200 reassurance transition,request and leave-taking idioms.\nPROTECTED_BOUNDARIES = PROTECTED_BOUNDARIES | frozenset({(\'still\',\'you\'),(\'take\',\'care\'),(\'care\',\'of\'),(\'please\',\'accept\'),(\'accept\',\'it\')})':
        '# Preserve B201 sale questions,power hearsay,and complete price/currency units.\nPROTECTED_BOUNDARIES = PROTECTED_BOUNDARIES | frozenset({(\'mysterious\',\'power\'),(\'replace\',\'it\'),(\'paying\',\'that\'),(\'150,000\',\'gold\'),(\'200,000\',\'gold\'),(\'100,000\',\'gold\')})'}))
    tools.append(derive('scripts/plan_lil_B200_layout_v5847.py','scripts/plan_lil_B201_layout_v5919.py',{
        'B200':'B201','lil_B200_layout_v2':'lil_B201_layout_v1','layout_v5847':'layout_v5919',
        'manuscript_v2.json':'manuscript_v1.json','manuscript_v3.json':'manuscript_v2.json',
        'Plan19':'Plan24','all19':'all24','len(reports)==19':'len(reports)==24','plans=19':'plans=24'}))
    ROOT.mkdir(parents=True);save(ROOT/'exact_profile_font_oracle_layout_and_planner_derivations.json',dict(
        profile=str(PROFILE),profile_sha256=sha(PROFILE.read_bytes()),dependencies=deps,tools=tools,
        exact_V5891_name_only_ARM9_rebind_source_proof='work/analysis/generic_speaker_labels_release_v5895/registered_release_verification.json',
        original_font_native_instructions_metrics_width_guards_phase_and_four_row_limit_preserved=True,
        no_authored_break_prose_change_fit_shortening_or_boundary_waiver=True,new_ROMs=0,new_emulator_runs=0,new_review_credit=0,full_goal_complete=False))
    print('Exact B201 profile/current-name-data font-oracle/phrase-layout successors prepared;all native addresses unchanged. No earlier helper edited.')
