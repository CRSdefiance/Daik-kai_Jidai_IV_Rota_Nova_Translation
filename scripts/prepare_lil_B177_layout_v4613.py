"""Bind B177 Owner/Cook progressive dialogue and its separate impersonal FE notice."""
from pathlib import Path
from scripts.prepare_lil_B156_layout_v3705 import derive
from scripts.verify_village_wrap_v608 import read,save
from dk4tool.patch.grand_race_menu_release import sha

ROOT=Path('work/analysis/lil_B177_layout_tools_v4613')
if __name__=='__main__':
    assert not ROOT.exists()
    doc=read('translations/lil_B177_editorial_manuscript_v1.json');source=read(doc['source_context'])
    deps={doc[k]:doc[k+'_sha256'] for k in ['source_context','control_contract','actor_voice_contract','branch_proof',
        'source_entry_proof','source_effect_and_predicate_contract','actor_terminology_reconciliation','source_nameplate_consumer_proof']}
    hashes=sorted({r[k] for r in source['blocks'] for k in ['clean_block_sha256','current_block_sha256']})
    profile=Path('dk4tool/dialogue/lil_B177_profile.py');assert not profile.exists()
    text='''"""B177 exact source/current controls:nine progressive and one impersonal null-actor FE notice."""
from dataclasses import replace
from pathlib import Path
import json
from dk4tool.dialogue.profiles import get_dialogue_profile
from dk4tool.patch.grand_race_menu_release import sha
ARM9_SHA='''+repr(source['current_ARM9_sha256'])+'''
BLOCKS=frozenset('''+repr(hashes)+''')
SELECTORS=frozenset({174,175})
DEPENDENCIES='''+repr(deps)+'''
CONTROL='''+repr(doc['control_contract'])+'''

def profile_for(arm,source_block,consumer='progressive'):
    if sha(arm)!=ARM9_SHA or sha(source_block) not in BLOCKS:raise ValueError('Exact B177 source/current block and runtime required')
    for path,digest in DEPENDENCIES.items():
        if sha(Path(path).read_bytes())!=digest:raise ValueError('B177 source contract changed:'+path)
    control=json.loads(Path(CONTROL).read_bytes());cases=control['speech_dispatch_cases']
    if len(cases)!=20 or sum(r['source_selector']==254 for r in cases)!=2:raise ValueError('All ten source/current dispatch pairs required')
    if any(r['resolved_actor_ID'] is not None for r in cases if r['source_selector']==254):raise ValueError('FE notice must remain null-actor')
    if control['source_macro_counts']!={'FI':0,'FA':0,'FO':0}:raise ValueError('B177 has no source substitutions')
    base=get_dialogue_profile('lil-opening-editorial-native-v1')
    if consumer=='progressive':
        return replace(base,name='lil-B177-progressive-runtime-bound-v1',leading_speaker_bytes=SELECTORS,
            metrics_source=base.metrics_source+';nine original54020 speeches,Owner174/Cook175,no source FI/FA/FO. Exact13 commands,opaque leading A0008,C200480,end482. Four read-only name paths;no resource,presentation,predicate,relative or typed objects. No natural eligibility or earned fashion-state claim.')
    if consumer=='FE-paper':
        return replace(base,name='lil-B177-FE-runtime-bound-v1',leading_speaker_bytes=frozenset({254}),
            metrics_source=base.metrics_source+';one impersonal prospective Genoa tomato-fashion notice,original24310null actor then5473C before fallback.228x48logical/228x64physical paper;conservative216px planning. No invented speaker or name label;native complete-page approval remains separate.')
    raise ValueError('Unknown B177 consumer')
'''
    compile(text,str(profile),'exec');profile.write_text(text,encoding='utf-8',newline='\n')
    tools=[derive('dk4tool/dialogue/lil_B175_layout_v1.py','dk4tool/dialogue/lil_B177_layout_v1.py',{
        "{'lil-B175-progressive-runtime-bound-v1':frozenset({2,9,183,184,185}),'lil-B175-FE-runtime-bound-v1':frozenset({254})}":
            "{'lil-B177-progressive-runtime-bound-v1':frozenset({174,175}),'lil-B177-FE-runtime-bound-v1':frozenset({254})}",
        'source-bound B175 profile':'source-bound B177 profile',
    })]
    tools.append(derive('scripts/plan_lil_B175_layout_v4516.py','scripts/plan_lil_B177_layout_v4614.py',{
        'Plan32':'Plan10','lil_B175_layout_v1':'lil_B177_layout_v1','lil_B175_profile':'lil_B177_profile',
        'lil_B175_layout_v4516':'lil_B177_layout_v4614','lil_B175_editorial':'lil_B177_editorial',
        'all32_paragraph_layout':'all10_paragraph_layout','len(reports)==32':'len(reports)==10','plans=32':'plans=10',
    }))
    tools.append(derive('scripts/verify_lil_B175_fonts_v4517.py','scripts/verify_lil_B177_fonts_v4615.py',{
        'Complete B175 progressive/FE native planes and256 original macro alignment cases.':'Complete B177 progressive/FE native planes and80 original alignment cases.',
        'lil_B175_profile':'lil_B177_profile','lil_B175_layout_v1':'lil_B177_layout_v1','lil_B175_fonts_v4517':'lil_B177_fonts_v4615',
        'lil_B175_editorial':'lil_B177_editorial','len(cases)==len(qa_reports)==32 and macro_calls==256':'len(cases)==len(qa_reports)==10 and macro_calls==80',
        "sum(c['kind']=='system-FE' for c in cases)==9":"sum(c['kind']=='system-FE' for c in cases)==1",
        'blocks[175]':'blocks[177]','blocks[174]':'blocks[176]','for selector in [2,9,183,184,185,254]':'for selector in [174,175,254]',
        'format(9 if selector==2 else 2':'format(175 if selector==174 else 174',
        "r['source_selector']==2 and":"r['source_selector']==174 and",
        'len(negatives)==24':'len(negatives)==18','all32_progressive_FE_native_planes_and256_alignment_cases':'all10_progressive_FE_native_planes_and80_alignment_cases',
        'current_original_macro_alignment_calls=256,progressive_alignment_calls=184,FE_null_actor_alignment_calls=72':
            'current_original_macro_alignment_calls=80,progressive_alignment_calls=72,FE_null_actor_alignment_calls=8',
        'complete_progressive_planes=23,complete_FE_logical_and_physical_planes=9':'complete_progressive_planes=9,complete_FE_logical_and_physical_planes=1',
        'native_source_FI4_FA1_and_all_six_selectors_preserved':'native_source_FI0_FA0_FO0_and_all_three_selectors_preserved',
        'actual_selected_B175_IDs':'actual_selected_B177_IDs',
        'All32 complete native planes,256 alignment cases and24 source-consumer negatives pass;four sheets need visual review.':
            'All10 complete native planes,80 alignment cases and18 source-consumer negatives pass;two sheets need visual review.',
    }))
    ROOT.mkdir(parents=True);save(ROOT/'source_derivation.json',dict(profile=str(profile),profile_sha256=sha(profile.read_bytes()),
        dependencies=deps,tools=tools,progressive_speeches=9,FE_null_actor_notices=1,source_macro_counts={'FI':0,'FA':0,'FO':0},
        progressive_geometry=[216,64],FE_logical_geometry=[228,48],FE_physical_geometry=[228,64],no_shared_metrics_guard_or_source_control_change=True,
        native_and_actual_approval_pending=True,source_prose_or_completion_credit_added=0,full_goal_complete=False))
    print('Prepared B177 exact profiles,ten-paragraph planner and80 native alignment-case producer;no credit.')
