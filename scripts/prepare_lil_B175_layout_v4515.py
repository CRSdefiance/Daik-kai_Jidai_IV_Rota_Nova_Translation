"""Bind B175's five progressive speakers and distinct anonymous FE consumer."""
from pathlib import Path
from scripts.prepare_lil_B156_layout_v3705 import derive
from scripts.verify_village_wrap_v608 import read,save
from dk4tool.patch.grand_race_menu_release import sha

ROOT=Path('work/analysis/lil_B175_layout_tools_v4515')
if __name__=='__main__':
    assert not ROOT.exists()
    doc=read('translations/lil_B175_editorial_manuscript_v1.json');source=read(doc['source_context'])
    deps={doc[k]:doc[k+'_sha256'] for k in ['source_context','control_contract','actor_voice_contract','branch_proof',
        'source_entry_proof','source_effect_and_predicate_contract','actor_terminology_reconciliation','source_nameplate_consumer_proof']}
    hashes=sorted({r[k] for r in source['blocks'] for k in ['clean_block_sha256','current_block_sha256']})
    profile=Path('dk4tool/dialogue/lil_B175_profile.py');assert not profile.exists()
    text='''"""B175 exact source/current controls:23 progressive and9 null-actor FE panels."""
from dataclasses import replace
from pathlib import Path
import json
from dk4tool.dialogue.profiles import get_dialogue_profile
from dk4tool.patch.grand_race_menu_release import sha
ARM9_SHA='''+repr(source['current_ARM9_sha256'])+'''
BLOCKS=frozenset('''+repr(hashes)+''')
SELECTORS=frozenset({2,9,183,184,185})
DEPENDENCIES='''+repr(deps)+'''
CONTROL='''+repr(doc['control_contract'])+'''

def profile_for(arm,source_block,consumer='progressive'):
    if sha(arm)!=ARM9_SHA or sha(source_block) not in BLOCKS:raise ValueError('Exact B175 clean/current source and runtime required')
    for path,digest in DEPENDENCIES.items():
        if sha(Path(path).read_bytes())!=digest:raise ValueError('B175 source contract changed:'+path)
    control=json.loads(Path(CONTROL).read_bytes())
    cases=control['speech_dispatch_cases']
    if len(cases)!=64 or sum(r['source_selector']==254 for r in cases)!=18:
        raise ValueError('B175 requires all32 clean/current native dispatch pairs')
    if any(r['resolved_actor_ID'] is not None for r in cases if r['source_selector']==254):
        raise ValueError('B175 FE must remain an original null-actor consumer')
    if control['source_macro_counts']!={'FI':4,'FA':1,'FO':0}:raise ValueError('B175 source macros changed')
    base=get_dialogue_profile('lil-opening-editorial-native-v1')
    if consumer=='progressive':
        return replace(base,name='lil-B175-progressive-runtime-bound-v1',leading_speaker_bytes=SELECTORS,
            metrics_source=base.metrics_source+';23 original54020 speeches,Lil2/Camille9/Angel183/Snake184/Dandy185.FI3/FA5/FO9 use Lil captain2 context.Preserve39 commands,seven leaves,resource6344,three presentations,C200 andtwo ends.No predicates,relative skips,A000s or typed menus. Four owned andsix read-only names;no event eligibility claim.')
    if consumer=='FE-paper':
        return replace(base,name='lil-B175-FE-runtime-bound-v1',leading_speaker_bytes=frozenset({254}),
            metrics_source=base.metrics_source+';nine anonymous woman-pirate panels,original24310null actor then5473C beforedynamic fallback.No static actor/nameplate inferred from presentation operands.228x48logical/228x64physical paper,conservative216px planning;native complete-page painter approval remains separate.No invented woman or sword name.')
    raise ValueError('Unknown B175 consumer')
'''
    compile(text,str(profile),'exec');profile.write_text(text,encoding='utf-8',newline='\n')
    tools=[derive('dk4tool/dialogue/lil_B174_layout_v2.py','dk4tool/dialogue/lil_B175_layout_v1.py',{
        "{'lil-B174-progressive-runtime-bound-v1':frozenset({2,14,26,201})}":
            "{'lil-B175-progressive-runtime-bound-v1':frozenset({2,9,183,184,185}),'lil-B175-FE-runtime-bound-v1':frozenset({254})}",
        'source-bound B174 profile':'source-bound B175 profile',
        '\ndef _word(value):':"\nPROTECTED_BOUNDARIES = PROTECTED_BOUNDARIES | frozenset({('in','one'),('one','piece'),('done','for'),('for','this'),('this','time'),('pirate','woman'),('some','nerve'),('act','tough'),('even','scarier'),('from','now'),('now','on')})\n\ndef _word(value):",
    })]
    tools.append(derive('scripts/plan_lil_B174_layout_v4472.py','scripts/plan_lil_B175_layout_v4516.py',{
        'Plan33':'Plan32','lil_B174_layout_v2':'lil_B175_layout_v1','lil_B174_profile':'lil_B175_profile',
        'lil_B174_layout_v4472':'lil_B175_layout_v4516','lil_B174_editorial_manuscript_v3':'lil_B175_editorial_manuscript_v1',
        'lil_B174_editorial_manuscript_v4':'lil_B175_editorial_manuscript_v2',
        'all33_paragraph_layout':'all32_paragraph_layout','len(reports)==33':'len(reports)==32','plans=33':'plans=32',
    }))
    ROOT.mkdir(parents=True);save(ROOT/'source_derivation.json',dict(profile=str(profile),profile_sha256=sha(profile.read_bytes()),
        dependencies=deps,tools=tools,progressive_speeches=23,FE_null_actor_panels=9,source_macro_counts={'FI':4,'FA':1,'FO':0},
        progressive_geometry=[216,64],FE_native_geometry_logical=[228,48],FE_native_geometry_physical=[228,64],
        FE_conservative_planning_width=216,no_shared_metrics_guard_or_source_control_change=True,
        native_and_actual_approval_pending=True,source_prose_or_completion_credit_added=0,full_goal_complete=False))
    print('Prepared exact mixed B175 profiles and32-paragraph planner; distinct native FE approval remains pending.')
