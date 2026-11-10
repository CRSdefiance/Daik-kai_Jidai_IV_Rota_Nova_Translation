"""Bind the two actual B204 consumers and preserve the frozen earlier planners."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import read,save
from dk4tool.patch.grand_race_menu_release import sha
ROOT=Path('work/analysis/lil_B204_layout_tools_v6121');PROFILE=Path('dk4tool/dialogue/lil_B204_profile.py')
if __name__=='__main__':
    assert not ROOT.exists() and not PROFILE.exists();doc=read('translations/lil_B204_editorial_manuscript_v1.json');packet=read(doc['source_context'])
    deps={doc[k]:doc[k+'_sha256'] for k in ['source_context','effective_current_comparison','control_contract','actor_terminology_reconciliation','actual_source_visual_review','source_prose_module']}
    deps['translations/lil_B204_editorial_manuscript_v1.json']=sha(Path('translations/lil_B204_editorial_manuscript_v1.json').read_bytes())
    code='''"""Exact B204 five actors,16 progressive speeches and four actorless letter objects."""
import json
from dataclasses import replace
from pathlib import Path
from dk4tool.dialogue.profiles import get_dialogue_profile
from dk4tool.patch.grand_race_menu_release import sha
ARM9_SHA=ARM_LITERAL
BLOCKS=BLOCK_LITERAL
DEPENDENCIES=DEPS_LITERAL
CONTROL=CONTROL_LITERAL
SOURCE=SOURCE_LITERAL
SELECTORS=frozenset({2,11,124,130,145})
def profile_for(arm,source_block,consumer='progressive'):
    if sha(arm)!=ARM9_SHA or sha(source_block) not in BLOCKS:raise ValueError('Exact B204 source/current block and current V6110 runtime required')
    for p,h in DEPENDENCIES.items():
        if sha(Path(p).read_bytes())!=h:raise ValueError('Frozen B204 contract changed:'+p)
    control=json.loads(Path(CONTROL).read_bytes());source=json.loads(Path(SOURCE).read_bytes());cases=control['speech_dispatch_cases']
    if len(cases)!=40 or sum(r['source_selector']==254 for r in cases)!=8:raise ValueError('All20 clean/current speech pairs and four FE letters required')
    if any(r['resolved_actor_ID'] is not None for r in cases if r['source_selector']==254):raise ValueError('FE letters remain null actor')
    if any(r['source_selector'] not in SELECTORS or r['resolved_actor_ID']!=r['source_selector'] for r in cases if r['source_selector']!=254):raise ValueError('All five original static actors required')
    if control['source_macro_counts']!={'FI':0,'FA':0,'FO':0} or len(control['source_current_opaque_nonrelative_control_leaves'])!=6:raise ValueError('B204 has six leaves and no speech macros')
    if source['ordinary_source_speeches']!=16 or source['system_FE_panels']!=4:raise ValueError('Source16 progressive/four FE consumer split required')
    base=get_dialogue_profile('lil-opening-editorial-native-v1')
    if consumer=='progressive':return replace(base,name='lil-B204-progressive-runtime-bound-v1',leading_speaker_bytes=SELECTORS,metrics_source=base.metrics_source+';16 source-bound progressive54020 speeches,five static actors. Original216x64 consumer,6px ASCII,four rows,guard and pair phase preserved. No macros,choices,predicates,relative sites or2000 pauses.')
    if consumer=='FE-paper':return replace(base,name='lil-B204-FE-runtime-bound-v1',window_width_px=228,leading_speaker_bytes=frozenset({254}),metrics_source=base.metrics_source+';four original24310 null-actor then5473C letter objects. Source-owned typed descriptor proves228x48logical/228x64physical,6x12logical glyph placement. Host planning uses the actual228px width;no native viewport,font,clip,guard,pair-phase or four-row change. Each new plane must prove complete glyphs and one-page return before approval. No macros.')
    raise ValueError('Unknown B204 consumer')
'''
    for a,b in {'ARM_LITERAL':repr(packet['current_ARM9_sha256']),'BLOCK_LITERAL':repr({packet['blocks'][0][k] for k in ['clean_block_sha256','current_block_sha256']}),'DEPS_LITERAL':repr(deps),'CONTROL_LITERAL':repr(doc['control_contract']),'SOURCE_LITERAL':repr(doc['source_context'])}.items():assert a in code;code=code.replace(a,b)
    compile(code,str(PROFILE),'exec');PROFILE.write_text(code,encoding='utf-8',newline='\n')
    tools=[derive('dk4tool/dialogue/lil_B203_layout_v2.py','dk4tool/dialogue/lil_B204_layout_v1.py',{
        'B203':'B204','frozenset({2,76,170})':'frozenset({2,11,124,130,145})',
        'profile.window_width_px!=216':"profile.window_width_px!={'lil-B204-progressive-runtime-bound-v1':216,'lil-B204-FE-runtime-bound-v1':228}[profile.name]",
    })]
    tools.append(derive('scripts/lil_current_font_oracles_v5918.py','scripts/lil_current_font_oracles_v6122.py',{'bceb685cd92f2ecf26746999fc7fc5e3c0a82b681f269d4e8a00044bb234360e':'03a905a9e4a4df117b8a4b5280ec3c669a4db00547972397413bc8bebc4afbbd'}))
    tools.append(derive('scripts/plan_lil_B203_layout_v6029.py','scripts/plan_lil_B204_layout_v6123.py',{'B203':'B204','lil_B203_layout_v2':'lil_B204_layout_v1','layout_v6029':'layout_v6123','Plan22':'Plan20','all22':'all20','len(reports)==22':'len(reports)==20','plans=22':'plans=20','manuscript_v2':'manuscript_v1','manuscript_v3':'manuscript_v2'}))
    ROOT.mkdir(parents=True);save(ROOT/'source_locked_profile_planner_and_oracles.json',dict(profile=str(PROFILE),profile_sha256=sha(PROFILE.read_bytes()),tools=tools,dependencies=deps,progressive_216x64_FE_228x48_native_views_unchanged=True,FE_host_planning_uses_validated_original228px_not_a_widened_native_viewport=True,all_native_addresses_font_metrics_guards_pair_phase_and_four_row_limits_preserved=True,all_source_consumer_native_planes_still_required=True,new_ROMs=0,new_emulator_runs=0,new_review_credit=0,full_goal_complete=False));print('B204 exact consumer profiles,planner and current font oracles prepared. Original216px progressive/228px FE views;no native changes.')
