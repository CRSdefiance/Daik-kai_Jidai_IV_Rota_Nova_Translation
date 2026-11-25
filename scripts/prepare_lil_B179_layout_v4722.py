"""Freeze B179's three dialogue identities and A000/end-only native display contract."""
from pathlib import Path
from scripts.prepare_lil_B156_layout_v3705 import derive
from scripts.verify_village_wrap_v608 import read,save
from dk4tool.patch.grand_race_menu_release import sha

ROOT=Path('work/analysis/lil_B179_layout_tools_v4722');assert not ROOT.exists()
doc=read('translations/lil_B179_editorial_manuscript_v1.json');source=read(doc['source_context'])
deps={doc[k]:doc[k+'_sha256'] for k in ['source_context','control_contract','actor_voice_contract','branch_proof','source_entry_proof',
    'source_effect_and_predicate_contract','actor_terminology_reconciliation','source_nameplate_consumer_proof']}
hashes=sorted({r[k] for r in source['blocks'] for k in ['clean_block_sha256','current_block_sha256']})
profile=Path('dk4tool/dialogue/lil_B179_profile.py');assert not profile.exists()
text='''"""B179 exact controls:thirteen progressive speeches,one impersonal FE,A000 and end only."""
from dataclasses import replace
from pathlib import Path
import json
from dk4tool.dialogue.profiles import get_dialogue_profile
from dk4tool.patch.grand_race_menu_release import sha
ARM9_SHA='''+repr(source['current_ARM9_sha256'])+'''
BLOCKS=frozenset('''+repr(hashes)+''')
SELECTORS=frozenset({92,96,152})
DEPENDENCIES='''+repr(deps)+'''
CONTROL='''+repr(doc['control_contract'])+'''

def profile_for(arm,source_block,consumer='progressive'):
    if sha(arm)!=ARM9_SHA or sha(source_block) not in BLOCKS:raise ValueError('Exact B179 source/current block and runtime required')
    for path,digest in DEPENDENCIES.items():
        if sha(Path(path).read_bytes())!=digest:raise ValueError('B179 source contract changed:'+path)
    control=json.loads(Path(CONTROL).read_bytes());cases=control['speech_dispatch_cases']
    if len(cases)!=28 or sum(r['source_selector']==254 for r in cases)!=2:raise ValueError('All fourteen source/current dispatch pairs required')
    if any(r['resolved_actor_ID'] is not None for r in cases if r['source_selector']==254):raise ValueError('FE notice must remain null-actor')
    if control['source_macro_counts']!={'FI':0,'FA':0,'FO':0}:raise ValueError('B179 has no source substitutions')
    base=get_dialogue_profile('lil-opening-editorial-native-v1')
    if consumer=='progressive':
        return replace(base,name='lil-B179-progressive-runtime-bound-v1',leading_speaker_bytes=SELECTORS,
            metrics_source=base.metrics_source+';thirteen original54020 speeches,Barkeep92/Patron96/Sailor152. Catalog Retainer152 is a distinct getter and does not override dialogue identity. Zero FI/FA/FO. Exact16 commands,opaque A0008,single end508;no C200. Six read-only name paths;no resource,presentation,predicate,relative or typed object. No natural eligibility or earned fashion-state claim.')
    if consumer=='FE-paper':
        return replace(base,name='lil-B179-FE-runtime-bound-v1',leading_speaker_bytes=frozenset({254}),
            metrics_source=base.metrics_source+';one impersonal prospective Sao Jorge wine-fashion notice,original24310null actor then5473C before fallback.228x48logical/228x64physical paper;conservative216px planning. No invented speaker/name label;complete-page native approval remains separate. The separate Japanese city alias reference lead stays open.')
    raise ValueError('Unknown B179 consumer')
'''
compile(text,str(profile),'exec');profile.write_text(text,encoding='utf-8',newline='\n')
tools=[derive('dk4tool/dialogue/lil_B178_layout_v1.py','dk4tool/dialogue/lil_B179_layout_v1.py',{
    "{'lil-B178-progressive-runtime-bound-v1':frozenset({166,167,168}),'lil-B178-FE-runtime-bound-v1':frozenset({254})}":
        "{'lil-B179-progressive-runtime-bound-v1':frozenset({92,96,152}),'lil-B179-FE-runtime-bound-v1':frozenset({254})}",
    'source-bound B178 profile':'source-bound B179 profile',
})]
tools.append(derive('scripts/plan_lil_B178_layout_v4676.py','scripts/plan_lil_B179_layout_v4723.py',{
    'Plan13':'Plan14','lil_B178_layout_v1':'lil_B179_layout_v1','lil_B178_profile':'lil_B179_profile',
    'lil_B178_layout_v4676':'lil_B179_layout_v4723','lil_B178_editorial':'lil_B179_editorial',
    'all13_paragraph_layout':'all14_paragraph_layout','len(reports)==13':'len(reports)==14','plans=13':'plans=14',
}))
tools.append(derive('scripts/verify_lil_B178_fonts_v4677.py','scripts/verify_lil_B179_fonts_v4724.py',{
    'Complete B178 progressive/FE native planes and104 original alignment cases.':'Complete B179 progressive/FE native planes and112 original alignment cases.',
    'lil_B178_profile':'lil_B179_profile','lil_B178_layout_v1':'lil_B179_layout_v1','lil_B178_fonts_v4677':'lil_B179_fonts_v4724',
    'lil_B178_editorial':'lil_B179_editorial',
    'len(cases)==len(qa_reports)==13 and macro_calls==104':'len(cases)==len(qa_reports)==14 and macro_calls==112',
    'blocks[178]':'blocks[179]','blocks[177]':'blocks[178]',
    'for selector in [166,167,168,254]':'for selector in [92,96,152,254]',
    'format(167 if selector==166 else 166':'format(96 if selector==92 else 92',
    "r['source_selector']==166 and":"r['source_selector']==92 and",
    'all13_progressive_FE_native_planes_and104_alignment_cases':'all14_progressive_FE_native_planes_and112_alignment_cases',
    'current_original_macro_alignment_calls=104,progressive_alignment_calls=96,FE_null_actor_alignment_calls=8':
        'current_original_macro_alignment_calls=112,progressive_alignment_calls=104,FE_null_actor_alignment_calls=8',
    'complete_progressive_planes=12,complete_FE_logical_and_physical_planes=1':'complete_progressive_planes=13,complete_FE_logical_and_physical_planes=1',
    'actual_selected_B178_IDs':'actual_selected_B179_IDs',
    'All13 complete native planes,104 alignment cases and20 source-consumer negatives pass;two sheets need visual review.':
        'All14 complete native planes,112 alignment cases and20 source-consumer negatives pass;two sheets need visual review.',
}))
ROOT.mkdir(parents=True)
save(ROOT/'source_derivation.json',dict(profile=str(profile),profile_sha256=sha(profile.read_bytes()),dependencies=deps,tools=tools,
    progressive_speeches=13,FE_null_actor_notices=1,source_macro_counts={'FI':0,'FA':0,'FO':0},
    no_new_phrase_exception_shared_metric_guard_or_source_control_change=True,no_C200_inherited=True,
    source_Sailor152_and_distinct_catalogue_Retainer152_preserved=True,city_alias_reference_lead_stays_open=True,
    source_prose_or_completion_credit_added=0,full_goal_complete=False))
print('Prepared B179 exact profiles,14-paragraph planner and112 native alignment cases;no C200 or credit.')
