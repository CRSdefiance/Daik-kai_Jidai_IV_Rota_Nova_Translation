"""Exact13-speech B207 progressive contract,two static actors,no FE/macros/choices/branches."""
import json
from dataclasses import replace
from pathlib import Path
from dk4tool.dialogue.profiles import get_dialogue_profile
from dk4tool.patch.grand_race_menu_release import sha
ARM9_SHA='4f4e41d26a0b24610a38a9da03dc549e4afec82121a1c72f35665104bb7ea351'
BLOCKS={'d71c5d7bed8013e9ea0f72889904e422556f1316215b6b3ebda18f813cf42bf4', '4d63bbb3f034d7c70f428ee1688f1e2770235b928222dae9d3400641b5ff30e4'}
DEPENDENCIES={'scripts\\lil_B207_prose_v6350.py': '94f9831841fd9564ffe5fe536bcca2e61498c007e5b9a4c3ed4da5dc3d2d7ddc', 'translations\\lil_B207_editorial_manuscript_v2.json': 'c04f3d72d34bd741ccaaf74211e0aa5fb52de1c5da4678337c76643559a5694c', 'translations\\lil_B207_speaker_names_review_v1.json': 'd50dec624fcad4a38b818e43ea34b2d66c39191503a7e018d189f7210c8dd5f4', 'work/analysis/current_V6327_native_v6337/verified_current_context_binding.json': '64d5a4c28e57669c080068aa557ce8fe3859727d8e33f8a4cc62da52c74bcac5', 'work/analysis/lil_B207_name_approval_v6355/two_name_retentions51_headers_no_asset_change.json': '3a4f8362779007c1f6b646b055348c83729705e64d295e37210eaa31e4ca8374', 'work\\analysis\\lil_B207_dispatches_v6342\\all13_source_current_dispatches_two_actors_no_macros_and2_control_leaves.json': '8018fe2747194a23f91e6927b39de7ead236b65914b4c5569f7cd7cd120c4899', 'work\\analysis\\lil_B207_effective_v6349b\\all13_effective_current_paragraphs_and_source_item_name.json': '3809706b0aa2dffa6dcf1db345046ccf053da6ebbafdf05868b85b4ef72f1681', 'work\\analysis\\lil_B207_name_planes_v6354d\\two_complete_native_names32_literal_macro_alignments_and_actual_headers.json': '3ceb19b3c07ba9c52b579168a011c8ed0ced369e8d9a90f1a6683f1df99e4212', 'work\\analysis\\lil_B207_source_names_v6341\\two_exact_source_name_fields_voices_and_distinct_name_consumers.json': '61019239326eaa61e5f837be72517beefaf4282e3b290b1e6bd61db005958f43', 'work\\analysis\\lil_B207_source_v6338\\all13_clean_current_complete_context.json': '4b9172ea77397a190f651af5534f4a4d578e09e9b832c2f09d3ef836049888d7'}
CONTROL='work\\analysis\\lil_B207_dispatches_v6342\\all13_source_current_dispatches_two_actors_no_macros_and2_control_leaves.json'
SOURCE='work\\analysis\\lil_B207_source_v6338\\all13_clean_current_complete_context.json'

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
