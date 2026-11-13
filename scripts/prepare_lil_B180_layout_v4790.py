"""Create source-bound B180 paragraph profiles; historical formatters stay frozen."""
from pathlib import Path
from scripts.prepare_lil_B156_layout_v3705 import derive
from scripts.verify_village_wrap_v608 import read,save
from dk4tool.patch.grand_race_menu_release import sha

ROOT=Path('work/analysis/lil_B180_layout_tools_v4790')
if __name__=='__main__':
    assert not ROOT.exists()
    doc=read('translations/lil_B180_editorial_manuscript_v1.json');source=read(doc['source_context'])
    keys=['source_context','control_contract','actor_voice_contract','branch_proof','source_entry_proof',
          'source_effect_and_predicate_contract','actor_terminology_reconciliation','source_nameplate_consumer_proof',
          'predicate_RNG_ownership_proof','current_C200_source_ownership_proof']
    deps={doc[k]:doc[k+'_sha256'] for k in keys}
    hashes=sorted({r[k] for r in source['blocks'] for k in ['clean_block_sha256','current_block_sha256']})
    profile=Path('dk4tool/dialogue/lil_B180_profile.py');assert not profile.exists()
    text='''"""B180 ten progressive speeches,one impersonal FE and conditional native controls."""
from dataclasses import replace
from pathlib import Path
import json
from dk4tool.dialogue.profiles import get_dialogue_profile
from dk4tool.patch.grand_race_menu_release import sha
ARM9_SHA='''+repr(source['current_ARM9_sha256'])+'''
BLOCKS=frozenset('''+repr(hashes)+''')
SELECTORS=frozenset({166,167})
DEPENDENCIES='''+repr(deps)+'''
CONTROL='''+repr(doc['control_contract'])+'''

def profile_for(arm,source_block,consumer='progressive'):
    if sha(arm)!=ARM9_SHA or sha(source_block) not in BLOCKS:raise ValueError('Exact B180 source/current block and runtime required')
    for path,digest in DEPENDENCIES.items():
        if sha(Path(path).read_bytes())!=digest:raise ValueError('B180 source contract changed:'+path)
    control=json.loads(Path(CONTROL).read_bytes());cases=control['speech_dispatch_cases']
    if len(cases)!=22 or sum(r['source_selector']==254 for r in cases)!=2:raise ValueError('All eleven source/current dispatch pairs required')
    if any(r['resolved_actor_ID'] is not None for r in cases if r['source_selector']==254):raise ValueError('FE notice must remain null-actor')
    if control['source_macro_counts']!={'FI':0,'FA':0,'FO':0}:raise ValueError('B180 has no source substitutions')
    base=get_dialogue_profile('lil-opening-editorial-native-v1')
    if consumer=='progressive':
        return replace(base,name='lil-B180-progressive-runtime-bound-v1',leading_speaker_bytes=SELECTORS,
            metrics_source=base.metrics_source+';ten original54020 speeches,Lady166/Lady167,four read-only name paths. No inferred noble rank,marriage or third-person gender.28 commands,ten relative sites,two original500 threshold/RNG predicates,three alternative opaque effects,C200570,end572. Current V4766 font and guards;native planes still need fresh approval.')
    if consumer=='FE-paper':
        return replace(base,name='lil-B180-FE-runtime-bound-v1',leading_speaker_bytes=frozenset({254}),
            metrics_source=base.metrics_source+';one prospective Lisbon Scents-category notice,original24310null actor then5473C.228x48logical/228x64physical,conservative216px planning. No earlier location,earned boom or demand/price inference. Current font native plane still needs fresh approval.')
    raise ValueError('Unknown B180 consumer')
'''
    compile(text,str(profile),'exec');profile.write_text(text,encoding='utf-8',newline='\n')
    tools=[derive('dk4tool/dialogue/lil_B179_layout_v1.py','dk4tool/dialogue/lil_B180_layout_v1.py',{
        "{'lil-B179-progressive-runtime-bound-v1':frozenset({92,96,152}),'lil-B179-FE-runtime-bound-v1':frozenset({254})}":
        "{'lil-B180-progressive-runtime-bound-v1':frozenset({166,167}),'lil-B180-FE-runtime-bound-v1':frozenset({254})}",
        'source-bound B179 profile':'source-bound B180 profile'}),
        derive('scripts/plan_lil_B179_layout_v4723.py','scripts/plan_lil_B180_layout_v4791.py',{
            'Plan14':'Plan11','lil_B179_layout_v1':'lil_B180_layout_v1','lil_B179_profile':'lil_B180_profile',
            'lil_B179_layout_v4723':'lil_B180_layout_v4791','lil_B179_editorial':'lil_B180_editorial',
            'all14_paragraph_layout':'all11_paragraph_layout','len(reports)==14':'len(reports)==11','plans=14':'plans=11'})]
    ROOT.mkdir(parents=True);save(ROOT/'source_derivation.json',dict(profile=str(profile),profile_sha256=sha(profile.read_bytes()),
        tools=tools,dependencies=deps,progressive=10,FE=1,no_shared_metric_guard_source_control_or_phrase_exception_change=True,
        full_native_width_used_without_the_shop_compiler_shrinking_loop=True,
        no_new_native_font_approval_or_credit=True,full_goal_complete=False))
    print('Prepared B180 exact profiles and11-paragraph planner;current font native approval still pending.')
