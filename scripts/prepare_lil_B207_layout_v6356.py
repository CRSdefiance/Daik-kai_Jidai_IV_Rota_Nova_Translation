"""Create an exact13-speech profile and a planner without B206's boundary exceptions."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import read,save
from dk4tool.patch.grand_race_menu_release import sha
ROOT=Path('work/analysis/lil_B207_layout_tools_v6356')
PROFILE=Path('dk4tool/dialogue/lil_B207_profile_v1.py')
FORMATTER=Path('dk4tool/dialogue/lil_B207_layout_v1.py')
DOC=Path('translations/lil_B207_editorial_manuscript_v2.json')
if __name__=='__main__':
    assert not any(p.exists() for p in [ROOT,PROFILE,FORMATTER]);doc=read(DOC);packet=read(doc['source_context']);block=packet['blocks'][0]
    deps={doc[k] for k in ['source_context','control_contract','actor_terminology_reconciliation','source_prose_module','effective_current_comparison','speaker_name_contextual_review','name_native_font_and_actual_proof']}
    deps.update([str(DOC),'work/analysis/current_V6327_native_v6337/verified_current_context_binding.json','work/analysis/lil_B207_name_approval_v6355/two_name_retentions51_headers_no_asset_change.json'])
    dependencies={p:sha(Path(p).read_bytes()) for p in sorted(deps)}
    source='''"""Exact13-speech B207 progressive contract,two static actors,no FE/macros/choices/branches."""
import json
from dataclasses import replace
from pathlib import Path
from dk4tool.dialogue.profiles import get_dialogue_profile
from dk4tool.patch.grand_race_menu_release import sha
'''+f'ARM9_SHA={doc["required_runtime_ARM9_sha256"]!r}\nBLOCKS={set([block["clean_block_sha256"],block["current_block_sha256"]])!r}\nDEPENDENCIES={dependencies!r}\nCONTROL={doc["control_contract"]!r}\nSOURCE={doc["source_context"]!r}\n'+'''
SELECTORS=frozenset({2,14})
def profile_for(arm,source_block,consumer='progressive'):
    if sha(arm)!=ARM9_SHA or sha(source_block) not in BLOCKS:raise ValueError('Exact B207 source/current block and V6327 runtime required')
    for p,h in DEPENDENCIES.items():
        if sha(Path(p).read_bytes())!=h:raise ValueError('Frozen B207 dependency changed:'+p)
    control=json.loads(Path(CONTROL).read_bytes());source=json.loads(Path(SOURCE).read_bytes());cases=control['speech_dispatch_cases']
    if len(cases)!=26 or any(r['source_selector'] not in SELECTORS or r['resolved_actor_ID']!=r['source_selector'] for r in cases):raise ValueError('All13 source/current actor dispatch pairs required')
    leaves=control['source_current_opaque_nonrelative_control_leaves']
    if control['source_macro_counts']!={'FI':0,'FA':0,'FO':0} or [(r['offset'],r['clean_current_hex']) for r in leaves]!=[(642,'00a0ffff29000110'),(650,'00000000')]:raise ValueError('One exact A000,complete end and zero macros required')
    if (source['ordinary_source_speeches'],source['system_FE_panels'],source['typed_choice_objects'],source['source_relative_sites'],source['source_A000'])!=(13,0,0,0,1):raise ValueError('Exact B207 source shape required')
    if consumer!='progressive':raise ValueError('B207 has no source FE or other speech consumer')
    base=get_dialogue_profile('lil-opening-editorial-native-v1')
    return replace(base,name='lil-B207-progressive-runtime-bound-v1',leading_speaker_bytes=SELECTORS,metrics_source=base.metrics_source+';13 original54020 progressive speeches:actors2/14,voices3/6. Exact original216x64 canvas,6px ASCII,four16px rows,guards and pair phase preserved. No FE,macros,typed menus,relative sites,predicates,pictures,47xx or2000 pause. One source A000 and complete end650/logical654/stored656/tail2 have separate guarded proofs. Lil Argot/Emilio Ferog names and original style11 are contextually retained with complete current headers. Full effects and natural event207 remain unproved.')
'''
    compile(source,str(PROFILE),'exec');PROFILE.write_text(source,encoding='utf-8',newline='\n')
    old='''# Exact B206 exchange:keep the qualified legend,personal intent and full information pitch intact.
PROTECTED_BOUNDARIES = PROTECTED_BOUNDARIES | frozenset({("world's",'best'),('dance','better'),('that','far'),('win','her'),('her','over'),('in','no'),('no','time'),('pick','up'),('all','sorts'),('sorts','of'),('9,000','gold'),('coin','less'),('get','lost'),('spoke','to')})

PROTECTED_BOUNDARIES = PROTECTED_BOUNDARIES | frozenset({('what','about'),('about','you'),('on','my'),('my','nerves')})'''
    new='''# B207's source-named weapon and ordinary idiom;no source-specific boundary exemption.
PROTECTED_BOUNDARIES = PROTECTED_BOUNDARIES | frozenset({('minotaur','axe'),('my','eye'),('feel','like')})'''
    derivation=derive('dk4tool/dialogue/lil_B206_layout_v1.py',str(FORMATTER),{old:new,'B206':'B207','frozenset({2,7,173})':'frozenset({2,14})'})
    ROOT.mkdir(parents=True);save(ROOT/'exact_profile_and_scoped_formatter.json',dict(profile=str(PROFILE),profile_sha256=sha(PROFILE.read_bytes()),formatter=derivation,source_speeches=13,source_static_actors=[2,14],source_macros=0,source_FE=0,no_inherited_B206_ordinary_boundary_exemptions=True,no_font_width_row_guard_pair_phase_or_global_formatter_change=True,source_native_name_retention_bound=True,new_ROMs=0,new_emulator_runs=0,new_review_credit=0,full_goal_complete=False));print('Exact B207 profile/scoped formatter prepared:13 speeches,actors2/14,no FE/macros/menus/branches or inherited B206 exceptions.')
