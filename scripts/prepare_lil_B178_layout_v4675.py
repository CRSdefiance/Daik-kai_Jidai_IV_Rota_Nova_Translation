"""Freeze B178 controls/three actors and derive native layout checks without new exceptions."""
from pathlib import Path
from scripts.prepare_lil_B156_layout_v3705 import derive
from scripts.verify_village_wrap_v608 import read,save
from dk4tool.patch.grand_race_menu_release import sha

ROOT=Path('work/analysis/lil_B178_layout_tools_v4675')
assert not ROOT.exists()
doc=read('translations/lil_B178_editorial_manuscript_v1.json');source=read(doc['source_context'])
deps={doc[k]:doc[k+'_sha256'] for k in ['source_context','control_contract','actor_voice_contract','branch_proof',
    'source_entry_proof','source_effect_and_predicate_contract','actor_terminology_reconciliation','source_nameplate_consumer_proof']}
hashes=sorted({r[k] for r in source['blocks'] for k in ['clean_block_sha256','current_block_sha256']})
profile=Path('dk4tool/dialogue/lil_B178_profile.py');assert not profile.exists()
text='''"""B178 exact controls:twelve progressive speeches and one impersonal FE notice."""
from dataclasses import replace
from pathlib import Path
import json
from dk4tool.dialogue.profiles import get_dialogue_profile
from dk4tool.patch.grand_race_menu_release import sha
ARM9_SHA='''+repr(source['current_ARM9_sha256'])+'''
BLOCKS=frozenset('''+repr(hashes)+''')
SELECTORS=frozenset({166,167,168})
DEPENDENCIES='''+repr(deps)+'''
CONTROL='''+repr(doc['control_contract'])+'''

def profile_for(arm,source_block,consumer='progressive'):
    if sha(arm)!=ARM9_SHA or sha(source_block) not in BLOCKS:raise ValueError('Exact B178 source/current block and runtime required')
    for path,digest in DEPENDENCIES.items():
        if sha(Path(path).read_bytes())!=digest:raise ValueError('B178 source contract changed:'+path)
    control=json.loads(Path(CONTROL).read_bytes());cases=control['speech_dispatch_cases']
    if len(cases)!=26 or sum(r['source_selector']==254 for r in cases)!=2:raise ValueError('All thirteen source/current dispatch pairs required')
    if any(r['resolved_actor_ID'] is not None for r in cases if r['source_selector']==254):raise ValueError('FE notice must remain null-actor')
    if control['source_macro_counts']!={'FI':0,'FA':0,'FO':0}:raise ValueError('B178 has no source substitutions')
    base=get_dialogue_profile('lil-opening-editorial-native-v1')
    if consumer=='progressive':
        return replace(base,name='lil-B178-progressive-runtime-bound-v1',leading_speaker_bytes=SELECTORS,
            metrics_source=base.metrics_source+';twelve original54020 speeches,Lady166/167/168,no source FI/FA/FO. Exact16 commands,opaque A0008,C200488,end490. Six read-only name paths;no resource,presentation,predicate,relative or typed object. No natural eligibility or earned fashion-state claim.')
    if consumer=='FE-paper':
        return replace(base,name='lil-B178-FE-runtime-bound-v1',leading_speaker_bytes=frozenset({254}),
            metrics_source=base.metrics_source+';one impersonal prospective Amsterdam wheat-fashion notice,original24310null actor then5473C before fallback.228x48logical/228x64physical paper;conservative216px planning. No invented speaker/name label;native complete-page approval remains separate.')
    raise ValueError('Unknown B178 consumer')
'''
compile(text,str(profile),'exec');profile.write_text(text,encoding='utf-8',newline='\n')
tools=[derive('dk4tool/dialogue/lil_B177_layout_v1.py','dk4tool/dialogue/lil_B178_layout_v1.py',{
    "{'lil-B177-progressive-runtime-bound-v1':frozenset({174,175}),'lil-B177-FE-runtime-bound-v1':frozenset({254})}":
        "{'lil-B178-progressive-runtime-bound-v1':frozenset({166,167,168}),'lil-B178-FE-runtime-bound-v1':frozenset({254})}",
    'source-bound B177 profile':'source-bound B178 profile',
})]
tools.append(derive('scripts/plan_lil_B177_layout_v4614.py','scripts/plan_lil_B178_layout_v4676.py',{
    'Plan10':'Plan13','lil_B177_layout_v1':'lil_B178_layout_v1','lil_B177_profile':'lil_B178_profile',
    'lil_B177_layout_v4614':'lil_B178_layout_v4676','lil_B177_editorial':'lil_B178_editorial',
    'all10_paragraph_layout':'all13_paragraph_layout','len(reports)==10':'len(reports)==13','plans=10':'plans=13',
}))
tools.append(derive('scripts/verify_lil_B177_fonts_v4615.py','scripts/verify_lil_B178_fonts_v4677.py',{
    'Complete B177 progressive/FE native planes and80 original alignment cases.':'Complete B178 progressive/FE native planes and104 original alignment cases.',
    'lil_B177_profile':'lil_B178_profile','lil_B177_layout_v1':'lil_B178_layout_v1','lil_B177_fonts_v4615':'lil_B178_fonts_v4677',
    'lil_B177_editorial':'lil_B178_editorial',
    'len(cases)==len(qa_reports)==10 and macro_calls==80':'len(cases)==len(qa_reports)==13 and macro_calls==104',
    'blocks[177]':'blocks[178]','blocks[176]':'blocks[177]',
    'for selector in [174,175,254]':'for selector in [166,167,168,254]',
    'format(175 if selector==174 else 174':'format(167 if selector==166 else 166',
    "r['source_selector']==174 and":"r['source_selector']==166 and",
    'len(negatives)==18':'len(negatives)==20','all10_progressive_FE_native_planes_and80_alignment_cases':'all13_progressive_FE_native_planes_and104_alignment_cases',
    'current_original_macro_alignment_calls=80,progressive_alignment_calls=72,FE_null_actor_alignment_calls=8':
        'current_original_macro_alignment_calls=104,progressive_alignment_calls=96,FE_null_actor_alignment_calls=8',
    'complete_progressive_planes=9,complete_FE_logical_and_physical_planes=1':'complete_progressive_planes=12,complete_FE_logical_and_physical_planes=1',
    'native_source_FI0_FA0_FO0_and_all_three_selectors_preserved':'native_source_FI0_FA0_FO0_and_all_four_selectors_preserved',
    'actual_selected_B177_IDs':'actual_selected_B178_IDs',
    'All10 complete native planes,80 alignment cases and18 source-consumer negatives pass;two sheets need visual review.':
        'All13 complete native planes,104 alignment cases and20 source-consumer negatives pass;two sheets need visual review.',
}))
ROOT.mkdir(parents=True)
save(ROOT/'source_derivation.json',dict(profile=str(profile),profile_sha256=sha(profile.read_bytes()),dependencies=deps,tools=tools,
    progressive_speeches=12,FE_null_actor_notices=1,source_macro_counts={'FI':0,'FA':0,'FO':0},
    no_new_B176_or_B177_phrase_exception_inherited=True,no_shared_metrics_guards_or_source_control_change=True,
    source_prose_or_completion_credit_added=0,full_goal_complete=False))
print('Prepared B178 exact profiles,13-paragraph planner and104 native alignment cases;no credit.')
