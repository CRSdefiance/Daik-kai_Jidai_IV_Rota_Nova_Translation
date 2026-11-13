"""Exact24-speech B206 progressive contract,three static actors,no FE or macros."""
import json
from dataclasses import replace
from pathlib import Path
from dk4tool.dialogue.profiles import get_dialogue_profile
from dk4tool.patch.grand_race_menu_release import sha
ARM9_SHA='4f4e41d26a0b24610a38a9da03dc549e4afec82121a1c72f35665104bb7ea351'
BLOCKS={'c94e3be21fca3e328fbac8b150df693f45aedf30b99b76fc1b432abeeaf9f81e', '18abedd3d442d332b48a377fd6330e5dfc94a900c489157fbe1063710aeb3269'}
DEPENDENCIES={'work\\analysis\\lil_B206_current_v6280\\all28_clean_current_context_rebound_to_V6270.json': '5682fcf48ca63524cc0d10afd0f381bfe537d80b5bd1754fffd2fce9664c054c', 'work\\analysis\\lil_B206_dispatches_v6236\\all24_source_current_dispatches_three_actors_no_macros_and8_control_leaves.json': '20c3f31eba20d1b5bd022b616a4426aa451021257774313ee9980ef9830c841a', 'work\\analysis\\lil_B206_prose_v6253\\all28_exact_source_current_findings_sixteen_revisions_twelve_retentions.json': '93536f0116f05570ac8a1cd0ce7991cc86e357acc362ce3632e6d3d2d0328f87', 'work\\analysis\\lil_B206_source_names_v6235\\three_exact_source_name_fields_voices_and_distinct_name_consumers.json': 'e51aa775641738c1ed108e78e2fe75fa24f054e706a870048f0bd227e2589140', 'work\\analysis\\lil_B206_source_view_v6248\\all24_source_speeches_four_labels_and_three_returns_viewed.json': 'd3848a7154d910d3a96ec4f5782d98ce62b323a7ae8639e5225a6d692cb4fed7', 'scripts\\lil_B206_prose_v6253.py': '36a900011471dfce9ac9cc171c18dd1e9fe7f43ab6ea57bc68c6a8c94a5004b4', 'translations\\lil_B206_choice_manuscript_v2.json': 'a7a913a0e704f3ee0514030182e25fe8afdf638892ed75839c031fbf590c590b', 'translations/lil_B206_editorial_manuscript_v3.json': '85eef588fbbc5bdad8a0c190a1e93970120d72a7e20976c63e9c8081e375d3a3', 'work/analysis/lil_B206_menu_approval_v6288/four_menu_labels_native_approved24_speeches_pending_no_credit.json': '55dff6ef7dcbb68d70831f5f27f39cd3696161863b89b517095d7f8ea448ff1f', 'work/analysis/current_V6270_native_v6279/verified_current_context_binding.json': '87b81c6447a1c005b4b9228159074c460d605b66cb9b81f284624a85e2c2514d', 'work/analysis/shady_man_label_release_v6271/registered_release_verification.json': '2aec2290af51acc50345bea388f4bbca1c464d4b2d339c63ac8522d459349aee'}
CONTROL='work\\analysis\\lil_B206_dispatches_v6236\\all24_source_current_dispatches_three_actors_no_macros_and8_control_leaves.json'
SOURCE='work\\analysis\\lil_B206_current_v6280\\all28_clean_current_context_rebound_to_V6270.json'
SELECTORS=frozenset({2,7,173})
def profile_for(arm,source_block,consumer='progressive'):
    if sha(arm)!=ARM9_SHA or sha(source_block) not in BLOCKS:raise ValueError('Exact B206 source/current block and V6270 runtime required')
    for p,h in DEPENDENCIES.items():
        if sha(Path(p).read_bytes())!=h:raise ValueError('Frozen B206 dependency changed:'+p)
    control=json.loads(Path(CONTROL).read_bytes());source=json.loads(Path(SOURCE).read_bytes());cases=control['speech_dispatch_cases']
    if len(cases)!=48 or any(r['source_selector'] not in SELECTORS or r['resolved_actor_ID']!=r['source_selector'] for r in cases):raise ValueError('All24 source/current static-actor dispatch pairs required')
    if control['source_macro_counts']!={'FI':0,'FA':0,'FO':0} or len(control['source_current_opaque_nonrelative_control_leaves'])!=8:raise ValueError('Eight nonchoice leaves and zero source macros required')
    if source['ordinary_source_speeches']!=24 or source['system_FE_panels']!=0 or source['typed_choice_objects']!=2 or source['source_relative_sites']!=8:raise ValueError('Exact B206 progressive/menu/branch shape required')
    if consumer!='progressive':raise ValueError('B206 has no source FE or other speech consumer')
    base=get_dialogue_profile('lil-opening-editorial-native-v1')
    return replace(base,name='lil-B206-progressive-runtime-bound-v1',leading_speaker_bytes=SELECTORS,metrics_source=base.metrics_source+';24 original54020 progressive speeches:actors2/7/173,voices3/3/0. Exact original216x64 canvas,6px ASCII,four16px rows,guards and pair phase preserved. Two2100 menus/eight relative spans have separate native proofs;no FE/macros/predicates/C200/2000 pause is inherited. Shady Man is separately validated in V6270;Cristina Erneco remains the working name. Full effects and natural event206 remain unproved.')
