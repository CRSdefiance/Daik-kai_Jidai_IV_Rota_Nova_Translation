"""Prepare an exact progressive-only B202 profile and frozen paragraph planner."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive,checked_text
from scripts.verify_village_wrap_v608 import read,save
from dk4tool.patch.grand_race_menu_release import sha
ROOT=Path('work/analysis/lil_B202_layout_tools_v5974')
PROFILE=Path('dk4tool/dialogue/lil_B202_profile.py')
if __name__=='__main__':
    assert not ROOT.exists() and not PROFILE.exists();doc=read('translations/lil_B202_editorial_manuscript_v1.json');packet=read(doc['source_context'])
    keys=['source_context','actor_voice_contract','control_contract','branch_proof','source_entry_proof','source_effect_and_predicate_contract','source_nameplate_consumer_proof','actor_terminology_reconciliation','contextual_reconciliation','actual_original_response_paths'];deps={doc[k]:doc[k+'_sha256'] for k in keys}
    code='''"""Exact B202 four-speaker,zero-macro progressive scene;no FE consumer."""
import json
from dataclasses import replace
from pathlib import Path
from dk4tool.dialogue.profiles import get_dialogue_profile
from dk4tool.patch.grand_race_menu_release import sha
ARM9_SHA=ARM_LITERAL
BLOCKS=BLOCK_LITERAL
SELECTORS=frozenset({2,18,147,157})
DEPENDENCIES=DEPS_LITERAL
CONTROL=CONTROL_LITERAL
TERMS=TERMS_LITERAL
VOICES=VOICES_LITERAL
def profile_for(arm,source_block,consumer='progressive'):
    if sha(arm)!=ARM9_SHA or sha(source_block) not in BLOCKS:raise ValueError('Exact B202 source/current block and runtime required')
    for path,digest in DEPENDENCIES.items():
        if sha(Path(path).read_bytes())!=digest:raise ValueError('B202 source contract changed:'+path)
    control=json.loads(Path(CONTROL).read_bytes());cases=control['speech_dispatch_cases']
    if len(cases)!=38 or any(c['source_selector'] not in SELECTORS or c['resolved_actor_ID']!=c['source_selector'] for c in cases):raise ValueError('All19 source/current progressive dispatch pairs required')
    if control['source_macro_counts']!={'FI':0,'FA':0,'FO':0}:raise ValueError('B202 has no source runtime name macro')
    terms=json.loads(Path(TERMS).read_bytes())
    if not terms['all19_source_speeches_observed'] or not terms['all26_source_commands_and9_original_initializers_observed'] or terms['visual_review_pending']:raise ValueError('Complete viewed source context required')
    if terms['source_item14']['Japanese']!='ガラスの製法辞典' or terms['source_item14']['current_English']!='Glassmaking Guide':raise ValueError('Exact source spoken-title/item binding required')
    voices=json.loads(Path(VOICES).read_bytes())
    if {r['actor_ID']:r['original_voice_class'] for r in voices['fresh4_actor_names']['rows']}!={2:3,18:0,147:0,157:4}:raise ValueError('All four source actors/voices required')
    if consumer!='progressive':raise ValueError('B202 has no FE or alternate display consumer')
    base=get_dialogue_profile('lil-opening-editorial-native-v1')
    return replace(base,name='lil-B202-progressive-runtime-bound-v1',leading_speaker_bytes=SELECTORS,metrics_source=base.metrics_source+';19 original54020 speeches,Lil2 voice3/Charles18 voice0/Guildmaster147 voice0/Sailor157 voice4.Original Sailor alias differs from catalogue Retainer.26 source commands,no FE,choices,predicates,relative sites or macros.One complete end/two tailzeros.Native width,guard,pair phase,four rows and current bceb font unchanged.')
'''
    for a,b in {'ARM_LITERAL':repr(packet['current_ARM9_sha256']),'BLOCK_LITERAL':repr({packet['blocks'][0][k] for k in ['clean_block_sha256','current_block_sha256']}),'DEPS_LITERAL':repr(deps),'CONTROL_LITERAL':repr(doc['control_contract']),'TERMS_LITERAL':repr(doc['contextual_reconciliation']),'VOICES_LITERAL':repr(doc['actor_voice_contract'])}.items():assert a in code;code=code.replace(a,b)
    compile(code,str(PROFILE),'exec')
    previous=Path('dk4tool/dialogue/lil_B201_layout_v4.py').read_text(encoding='utf-8');a=previous.index('# Preserve B201 sale questions');b=previous.index('\ndef _word(',a)
    changes={previous[a:b]:'# B202 needs no inherited B201 sale-specific phrase or boundary exceptions.\n',
      "    expected={'lil-B201-progressive-runtime-bound-v1':frozenset({2,19,105}),'lil-B201-FE-runtime-bound-v1':frozenset({254})}":"    expected={'lil-B202-progressive-runtime-bound-v1':frozenset({2,18,147,157})}",
      'B201':'B202'}
    checked_text(previous,changes);PROFILE.write_text(code,encoding='utf-8',newline='\n')
    tools=[derive('dk4tool/dialogue/lil_B201_layout_v4.py','dk4tool/dialogue/lil_B202_layout_v1.py',changes)]
    tools.append(derive('scripts/plan_lil_B201_layout_v5919.py','scripts/plan_lil_B202_layout_v5975.py',{'B201':'B202','layout_v5919':'layout_v5975','all24':'all19','Plan24':'Plan19','len(reports)==24':'len(reports)==19','plans=24':'plans=19'}))
    ROOT.mkdir(parents=True);save(ROOT/'prepared_profile_and_planner.json',dict(profile=str(PROFILE),profile_sha256=sha(PROFILE.read_bytes()),tools=tools,no_prose_metrics_width_guards_pair_phase_or_four_row_limits_changed=True,no_FE_consumer_or_record_specific_boundary_exception_added=True,dependencies=deps,full_goal_complete=False))
    print('B202 progressive-only source-locked profile/planner prepared;four actual source actors,zero macros. Native display checks next.')
