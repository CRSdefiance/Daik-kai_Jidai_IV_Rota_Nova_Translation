"""Bind source-specific progressive and FE consumers without changing native metrics."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import read,save
from dk4tool.patch.grand_race_menu_release import sha
ROOT=Path('work/analysis/lil_B203_layout_tools_v6026')
PROFILE=Path('dk4tool/dialogue/lil_B203_profile.py')
if __name__=='__main__':
    assert not ROOT.exists() and not PROFILE.exists();doc=read('translations/lil_B203_editorial_manuscript_v1.json');packet=read(doc['source_context'])
    keys=['source_context','actor_voice_contract','control_contract','branch_proof','source_entry_proof','source_effect_and_predicate_contract','source_nameplate_consumer_proof','actor_terminology_reconciliation','contextual_reconciliation','actual_original_response_paths']
    deps={doc[k]:doc[k+'_sha256'] for k in keys}
    code='''"""Exact B203 three actors,21 progressive speeches and one original FE/FI notice."""
import json
from dataclasses import replace
from pathlib import Path
from dk4tool.dialogue.profiles import get_dialogue_profile
from dk4tool.patch.grand_race_menu_release import sha
ARM9_SHA=ARM_LITERAL
BLOCKS=BLOCK_LITERAL
SELECTORS=frozenset({2,76,170})
DEPENDENCIES=DEPS_LITERAL
CONTROL=CONTROL_LITERAL
TERMS=TERMS_LITERAL
VOICES=VOICES_LITERAL

def profile_for(arm,source_block,consumer='progressive'):
    if sha(arm)!=ARM9_SHA or sha(source_block) not in BLOCKS:raise ValueError('Exact B203 source/current block and runtime required')
    for path,digest in DEPENDENCIES.items():
        if sha(Path(path).read_bytes())!=digest:raise ValueError('B203 source contract changed:'+path)
    control=json.loads(Path(CONTROL).read_bytes());cases=control['speech_dispatch_cases']
    if len(cases)!=44 or sum(c['source_selector']==254 for c in cases)!=2:raise ValueError('All22 source/current dispatch pairs required')
    if any(c['resolved_actor_ID'] is not None for c in cases if c['source_selector']==254):raise ValueError('FE must remain null actor')
    if any(c['source_selector'] not in SELECTORS or c['resolved_actor_ID']!=c['source_selector'] for c in cases if c['source_selector']!=254):raise ValueError('Three exact static actors required')
    if control['source_macro_counts']!={'FI':1,'FA':0,'FO':0}:raise ValueError('B203 has exactly one original FI macro')
    terms=json.loads(Path(TERMS).read_bytes())
    if not terms['all22_source_objects_observed'] or not terms['all31_source_commands_and9_original_initializers_observed'] or terms['visual_review_pending']:raise ValueError('Complete viewed source context required')
    if terms['source_item18']['Japanese']!='漢方医の聖典' or terms['source_item18']['current_English']!="Herbalist's Bible":raise ValueError('Exact source item18 binding required;no title insertion')
    voices=json.loads(Path(VOICES).read_bytes())
    if {r['actor_ID']:r['original_voice_class'] for r in voices['fresh3_actor_names']['rows']}!={2:3,76:5,170:0}:raise ValueError('All three source actors/voices required')
    base=get_dialogue_profile('lil-opening-editorial-native-v1')
    if consumer=='progressive':
        return replace(base,name='lil-B203-progressive-runtime-bound-v1',leading_speaker_bytes=SELECTORS,metrics_source=base.metrics_source+';21 original54020 speeches,Lil2 voice3/Mikhail76 voice5/MysteriousOldMan170 voice0,six distinct name consumers.31 original commands,no choices,predicates,relative sites or2000 pauses.One complete four-byte end/two tailzeros.Current bceb font,width,guard,pair phase and four rows unchanged.')
    if consumer=='FE-paper':
        return replace(base,name='lil-B203-FE-runtime-bound-v1',leading_speaker_bytes=frozenset({254}),metrics_source=base.metrics_source+';one original24310 null-actor then5473C notice:FI Charm+1. DefaultFI expandsLil3,FA/FO absent.228x48logical/228x64physical,conservative216px planning. Generated item-acquired notice is separate and unchanged. Actual English scene and complete effect semantics remain separate.')
    raise ValueError('Unknown B203 consumer')
'''
    for a,b in {'ARM_LITERAL':repr(packet['current_ARM9_sha256']),'BLOCK_LITERAL':repr({packet['blocks'][0][k] for k in ['clean_block_sha256','current_block_sha256']}),'DEPS_LITERAL':repr(deps),'CONTROL_LITERAL':repr(doc['control_contract']),'TERMS_LITERAL':repr(doc['contextual_reconciliation']),'VOICES_LITERAL':repr(doc['actor_voice_contract'])}.items():assert a in code;code=code.replace(a,b)
    compile(code,str(PROFILE),'exec');PROFILE.write_text(code,encoding='utf-8',newline='\n')
    tools=[derive('dk4tool/dialogue/lil_B202_layout_v1.py','dk4tool/dialogue/lil_B203_layout_v1.py',{
        "expected={'lil-B202-progressive-runtime-bound-v1':frozenset({2,18,147,157})}":"expected={'lil-B203-progressive-runtime-bound-v1':frozenset({2,76,170}),'lil-B203-FE-runtime-bound-v1':frozenset({254})}",
        'B202':'B203',
    })]
    tools.append(derive('scripts/plan_lil_B202_layout_v5975.py','scripts/plan_lil_B203_layout_v6027.py',{
        'B202':'B203','layout_v5975':'layout_v6027','Plan19':'Plan22','all19':'all22','len(reports)==19':'len(reports)==22','plans=19':'plans=22',
    }))
    tools.append(derive('scripts/verify_lil_B201_fonts_v5920.py','scripts/verify_lil_B203_fonts_v6028.py',{
        'B201':'B203','fonts_v5920':'fonts_v6028','voices_v5903':'voices_v6011',
        'blocks[201]':'blocks[203]','blocks[200]':'blocks[202]',
        'len(cases)==len(qa_reports)==24 and macro_calls==192':'len(cases)==len(qa_reports)==22 and macro_calls==176',
        "sum(c['kind']=='system-FE' for c in cases)==3":"sum(c['kind']=='system-FE' for c in cases)==1",
        '[2,19,105,254]':'[2,76,170,254]','format(19 if selector==2 else 2':'format(76 if selector==2 else 2',
        "r['source_selector']==19":"r['source_selector']==76",'len(negatives)==24':'len(negatives)==22',
        'all24_progressive_FE_native_planes_and192_alignment_cases':'all22_progressive_FE_native_planes_and176_alignment_cases',
        'current_original_macro_alignment_calls=192':'current_original_macro_alignment_calls=176','FE_null_actor_alignment_calls=24':'FE_null_actor_alignment_calls=8',
        'complete_FE_logical_and_physical_planes=3':'complete_FE_logical_and_physical_planes=1',
        'native_source_FI2_FA0_FO0':'native_source_FI1_FA0_FO0',
        'All24 current-font native planes,192 alignment cases and24 source-consumer negatives':'All22 current-font native planes,176 alignment cases and22 source-consumer negatives',
        'Complete B201 current-font progressive/FE planes and152 native alignment cases.':'Complete B203 current-font progressive/FE planes and176 native alignment cases.',
    }))
    ROOT.mkdir(parents=True);save(ROOT/'prepared_profile_and_planner.json',dict(profile=str(PROFILE),profile_sha256=sha(PROFILE.read_bytes()),tools=tools,dependencies=deps,no_prose_metrics_width_guards_pair_phase_or_four_row_limits_changed=True,one_original_FE_FI_consumer_bound=True,full_goal_complete=False))
    print('B203 source-locked progressive/FE profile and planner prepared;native geometry and prose unchanged.')
