"""Bind source/runtime profile and prepare automatic44-paragraph layout."""
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save
SOURCE=Path('work/analysis/lil_remaining_B138_B140_source_v3422/next44_B138_clean_current_context.json')
CONTROL=Path('work/analysis/lil_B138_controls_v3426e/all44_source_current_dispatches10_predicates_and1_query.json')
VOICE=Path('work/analysis/lil_B138_voices_v3425/current_seven_static_names_voices_and207_catalog_rebind.json')
TERMS=Path('work/analysis/lil_B138_terms_v3429/clean_current_names_leaf_price_macro_and_entry_reconciliation.json')
BRANCH=Path('work/analysis/lil_B138_branches_v3427b/original_relative_skip_operand_proof.json')
PROFILE=Path('dk4tool/dialogue/lil_B138_profile.py')
FORMATTER=Path('dk4tool/dialogue/lil_B138_layout_v1.py')
if __name__=='__main__':
    root=Path('work/analysis/lil_B138_layout_tools_v3433');assert not root.exists() and not PROFILE.exists() and not FORMATTER.exists()
    source,control=map(read,[SOURCE,CONTROL]);dependencies=[SOURCE,CONTROL,VOICE,TERMS,BRANCH,Path(control['registered_catalog_binding']),Path(control['source_exact_conditional_result_contract'])]
    hashes={str(p):sha(p.read_bytes()) for p in dependencies};blocks={b[k] for b in source['blocks'] for k in ['clean_block_sha256','current_block_sha256']}
    text='''"""Exact B138 progressive profile with raw result2 and the source event137 query."""
from dataclasses import replace
from pathlib import Path
import json
from dk4tool.dialogue.profiles import get_dialogue_profile
from dk4tool.patch.grand_race_menu_release import sha
ARM9_SHA=__ARM__
BLOCKS=frozenset(__BLOCKS__)
SELECTORS=frozenset({2,14,20,21,22,23,92})
DEPENDENCIES=__DEPS__
CONTROL=Path(__CONTROL__)
VOICE=Path(__VOICE__)
def profile_for(arm,source_block,consumer='progressive'):
    if sha(arm)!=ARM9_SHA or sha(source_block) not in BLOCKS:raise ValueError('B138 exact clean/current block andruntime required')
    for p,digest in DEPENDENCIES.items():
        if sha(Path(p).read_bytes())!=digest:raise ValueError('B138 source contract changed:'+p)
    control=json.loads(CONTROL.read_text(encoding='utf-8'));voice=json.loads(VOICE.read_text(encoding='utf-8'))
    if consumer!='progressive' or len(control['speech_dispatch_cases'])!=88 or len(control['current_original_predicate_cases'])!=11 or len(control['original_event_queries'])!=1 or control['original_event_queries'][0]['event']!=137 or control['source_macro_counts']!={'FI':0,'FA':0,'FO':1} or len(voice['fresh_seven_actor_names']['rows'])!=7:raise ValueError('Complete B138 actors,predicates,event137 query andFO contracts required')
    result2=[c for c in control['current_original_predicate_cases'] if c['source_command_hex']=='0080ffff200301a1']
    if len(result2)!=1 or result2[0]['native_result']!=[2,2,0,0,0,0]:raise ValueError('B138 source raw-result2 contract required')
    base=get_dialogue_profile('lil-opening-editorial-native-v1')
    return replace(base,name='lil-B138-progressive-runtime-bound-v1',leading_speaker_bytes=SELECTORS,metrics_source=base.metrics_source+';44 progressive speeches,seven static actors. FI3/FA5/FO9 use Lil captain2;FO1 in source. Ten predicates preserve raw result2 andone event137 query remains Boolean. No FE/source00/dynamic/4100/2000/2100.')
'''
    for a,b in [('__ARM__',repr(source['current_ARM9_sha256'])),('__BLOCKS__',repr(sorted(blocks))),('__DEPS__',repr(hashes)),('__CONTROL__',repr(str(CONTROL))),('__VOICE__',repr(str(VOICE)))]:text=text.replace(a,b)
    compile(text,str(PROFILE),'exec');PROFILE.write_text(text,encoding='utf-8')
    old=Path('dk4tool/dialogue/lil_B137_layout_v3.py');t=old.read_text(encoding='utf-8').replace('B137','B138')
    assert 'frozenset({2,9,14,16,17,20,22,23,38,92,198})' in t;t=t.replace('frozenset({2,9,14,16,17,20,22,23,38,92,198})','frozenset({2,14,20,21,22,23,92})')
    needle='PROTECTED_BOUNDARIES=frozenset({';assert t.count(needle)==1
    t=t.replace(needle,needle+"('good','customer'),('taken','over'),('one','problem'),('problem','after'),('after','another'),('run','out'),('fawned','over'),('lost','my'),('my','dignity'),('with','dignity'),('opened','my'),('my','eyes'),('end','up'),")
    compile(t,str(FORMATTER),'exec');FORMATTER.write_text(t,encoding='utf-8')
    a=Path('scripts/plan_lil_B137_layout_v3397b.py');b=Path('scripts/plan_lil_B138_layout_v3433b.py');assert not b.exists();t=a.read_text(encoding='utf-8')
    changes=[('plan 155 speeches/four labels','plan44 progressive speeches'),('lil_B137_layout_v3397b','lil_B138_layout_v3433b'),('lil_remaining_B137_B140_source_v3380b','lil_remaining_B138_B140_source_v3422'),('next48_B137','next44_B138'),('lil_B137_profile','lil_B138_profile'),('lil_B137_layout_v3','lil_B138_layout_v1'),('lil_B137_editorial_manuscript_v5','lil_B138_editorial_manuscript_v1'),('lil_B137_editorial_manuscript_v6','lil_B138_editorial_manuscript_v2'),('all48','all44'),('len(reports)==48','len(reports)==44'),('plans=48','plans=44')]
    for x,y in changes:assert x in t,x;t=t.replace(x,y)
    compile(t,str(b),'exec');b.write_text(t,encoding='utf-8');root.mkdir(parents=True)
    save(root/'provenance.json',dict(profile=str(PROFILE),profile_sha256=sha(PROFILE.read_bytes()),profile_dependencies=hashes,previous_formatter=str(old),previous_formatter_sha256=sha(old.read_bytes()),formatter=str(FORMATTER),formatter_sha256=sha(FORMATTER.read_bytes()),previous_planner=str(a),previous_planner_sha256=sha(a.read_bytes()),planner=str(b),planner_sha256=sha(b.read_bytes()),all_prior_profiles_formatters_manuscripts_and_producers_preserved=True,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
