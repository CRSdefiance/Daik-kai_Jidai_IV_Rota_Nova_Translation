"""Bind B206's24 original progressive speakers;no FE,no inherited parrot/menu renderer shape."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/lil_B206_layout_tools_v6291');PROFILE=Path('dk4tool/dialogue/lil_B206_profile_v1.py')
if __name__=='__main__':
    assert not ROOT.exists() and not PROFILE.exists();doc=read('translations/lil_B206_editorial_manuscript_v3.json');packet=read(doc['source_context']);assert packet['ordinary_source_speeches']==24 and packet['system_FE_panels']==0 and packet['typed_choice_objects']==2 and len(packet['source_relative_sites'])==8
    keys=['source_context','control_contract','effective_current_comparison','actor_terminology_reconciliation','actual_source_visual_review','source_prose_module','typed_choice_manuscript'];deps={doc[k]:doc[k+'_sha256'] for k in keys}
    for p in ['translations/lil_B206_editorial_manuscript_v3.json','work/analysis/lil_B206_menu_approval_v6288/four_menu_labels_native_approved24_speeches_pending_no_credit.json','work/analysis/current_V6270_native_v6279/verified_current_context_binding.json','work/analysis/shady_man_label_release_v6271/registered_release_verification.json']:deps[p]=sha(Path(p).read_bytes())
    code='''"""Exact24-speech B206 progressive contract,three static actors,no FE or macros."""
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
SELECTORS=frozenset({2,7,173})
def profile_for(arm,source_block,consumer='progressive'):
    if sha(arm)!=ARM9_SHA or sha(source_block) not in BLOCKS:raise ValueError('Exact B206 source/current block and V6270 runtime required')
    for p,h in DEPENDENCIES.items():
        if sha(Path(p).read_bytes())!=h:raise ValueError('Frozen B206 dependency changed:'+p)
    control=json.loads(Path(CONTROL).read_bytes());source=json.loads(Path(SOURCE).read_bytes());cases=control['speech_dispatch_cases']
    if len(cases)!=48 or any(r['source_selector'] not in SELECTORS or r['resolved_actor_ID']!=r['source_selector'] for r in cases):raise ValueError('All24 source/current static-actor dispatch pairs required')
    if control['source_macro_counts']!={'FI':0,'FA':0,'FO':0} or len(control['source_current_opaque_nonrelative_control_leaves'])!=8:raise ValueError('Eight nonchoice leaves and zero source macros required')
    if source['ordinary_source_speeches']!=24 or source['system_FE_panels']!=0 or source['typed_choice_objects']!=2 or len(source['source_relative_sites'])!=8:raise ValueError('Exact B206 progressive/menu/branch shape required')
    if consumer!='progressive':raise ValueError('B206 has no source FE or other speech consumer')
    base=get_dialogue_profile('lil-opening-editorial-native-v1')
    return replace(base,name='lil-B206-progressive-runtime-bound-v1',leading_speaker_bytes=SELECTORS,metrics_source=base.metrics_source+';24 original54020 progressive speeches:actors2/7/173,voices3/3/0. Exact original216x64 canvas,6px ASCII,four16px rows,guards and pair phase preserved. Two2100 menus/eight relative spans have separate native proofs;no FE/macros/predicates/C200/2000 pause is inherited. Shady Man is separately validated in V6270;Cristina Erneco remains the working name. Full effects and natural event206 remain unproved.')
'''
    for key,value in {'ARM_LITERAL':repr(packet['current_ARM9_sha256']),'BLOCK_LITERAL':repr({packet['blocks'][0][k] for k in ['clean_block_sha256','current_block_sha256']}),'DEPS_LITERAL':repr(deps),'CONTROL_LITERAL':repr(doc['control_contract']),'SOURCE_LITERAL':repr(doc['source_context'])}.items():assert key in code;code=code.replace(key,value)
    compile(code,str(PROFILE),'exec');PROFILE.write_text(code,encoding='utf-8',newline='\n')
    derivation=derive('dk4tool/dialogue/lil_B205_layout_v2.py','dk4tool/dialogue/lil_B206_layout_v1.py',{
      'B205':'B206',
      "expected={'lil-B205-progressive-runtime-bound-v1':frozenset({2,15}),'lil-B205-FE-runtime-bound-v1':frozenset({254})}":"expected={'lil-B206-progressive-runtime-bound-v1':frozenset({2,7,173})}",
      '# Exact B205 whole-exchange review:keep the mimicry and final idiom intact.':'# Exact B206 exchange:keep the qualified legend,personal intent and full information pitch intact.',
      "frozenset({('stop','copying'),('copying','me'),('had','enough'),('finally','got'),('got','it'),('got','caught'),('save','face')})":"frozenset({(\"world's\",'best'),('dance','better'),('that','far'),('win','her'),('her','over'),('in','no'),('no','time'),('pick','up'),('all','sorts'),('sorts','of'),('9,000','gold'),('coin','less'),('get','lost'),('spoke','to')})",
      "frozenset({(\"i'm\",'going'),('going','to'),('to','catch'),('catch','you'),('trying','to'),('to','save')})":"frozenset({('what','about'),('about','you'),('on','my'),('my','nerves')})",
    })
    ROOT.mkdir(parents=True);save(ROOT/'three_actor_no_FE_profile_and_source_locked_paragraph_planner.json',dict(profile=str(PROFILE),profile_sha256=sha(PROFILE.read_bytes()),planner_derivation=derivation,dependencies=deps,source24_progressive_three_static_actors_zero_FE_macros=True,native216px_four_rows_fonts_guards_and_pair_phase_unchanged=True,all_four_menu_gates_and_all28_prose_words_retained=True,new_ROMs=0,new_emulator_runs=0,new_review_credit=0,full_goal_complete=False));print('Exact B206 three-actor/no-FE progressive profile and paragraph planner prepared;native metrics and all prose retained.')
