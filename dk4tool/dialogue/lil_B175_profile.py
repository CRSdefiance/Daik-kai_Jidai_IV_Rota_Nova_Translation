"""B175 exact source/current controls:23 progressive and9 null-actor FE panels."""
from dataclasses import replace
from pathlib import Path
import json
from dk4tool.dialogue.profiles import get_dialogue_profile
from dk4tool.patch.grand_race_menu_release import sha
ARM9_SHA='d9415c1e0eb18c9eec9b76329f3dedb724a1a754a4829be103c6b958f927b9aa'
BLOCKS=frozenset(['3bf9d6678ada4a07930036b5b76a5b498eb7492088ae000124ee6c286852dc1e', 'eada871a0a34bb9e1c27e6e135fe8832587b55a89252a22cb3bac75bade8c2b3'])
SELECTORS=frozenset({2,9,183,184,185})
DEPENDENCIES={'work\\analysis\\lil_B175_source_v4503\\all32_clean_current_complete_context.json': '5c252b6e73ef81075c20cf41db170f8d88a134ec01b83ca205ab960e645aebd4', 'work\\analysis\\lil_B175_dispatches_v4505\\all32_source_current_dispatches_FI4_FA1_and7_control_leaves.json': 'c079d2b7367b917f6587e2345452196a838831d1b744dbdf4af8df58a71dadbc', 'work/analysis/lil_B175_voices_v4504/current5_static_names_voices_and207_catalog_rebind.json': '2a4fd047b279e5fcff78740623d177ed1609d7e426ffc656d45ce6ea30484df2', 'work/analysis/lil_B175_branches_v4506/original_relative_skip_operand_proof.json': 'f045a8e8bdaa0f26e13fe3372524cf96303a46ac46b5c3bad5c5f54c30b03a7b', 'work/analysis/lil_B175_entry_v4507/source_EV2_B175_action_dependency_and_native_getter_binding.json': 'a4ad2ee1394be06c621a496a017c77903c5da2295191027a091a25c893dac557', 'work/analysis/lil_B175_controls_v4509/one_resource_three_presentations_C200_two_ends_and7_source_leaves.json': '000b331cb2069a5f7bc306f353c499a3b3fda344c1eee629a98bf3043093d27d', 'work\\analysis\\lil_B175_terms_v4510\\current_five_names_anonymous_woman_unidentified_sword_and_admiral_reconciliation.json': '54e3ccaa6b4eb1a03b61f23beba7428aea23db4c1115a7990ee5bf480135b39e', 'work/analysis/lil_B175_names_v4508/ten_original_name_consumers_owned_and_readonly_paths.json': '4b2c9bf48bdd288660c2b1207ea18944394f7dedfbb3f40f1d04c42b1730f98c'}
CONTROL='work\\analysis\\lil_B175_dispatches_v4505\\all32_source_current_dispatches_FI4_FA1_and7_control_leaves.json'

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
