"""Exact B19930 progressive speeches and one four-impact null-actor FE object."""
import json
from dataclasses import replace
from pathlib import Path
from dk4tool.dialogue.profiles import get_dialogue_profile
from dk4tool.patch.grand_race_menu_release import sha
ARM9_SHA='39b11636e9b9904f96e18691154c813ebcad6e61647db412fa60b7344221b4a1'
BLOCKS={'b359c1c0e03a492b33e9a3ccf56446f8cb34629c63c47555f312c13ad0fe8e07', '073596745ef69273fdf1e5c54d895003cb859947f2e14e244fe8872eaa7f27c8'}
SELECTORS=frozenset({2,9,22})
DEPENDENCIES={'work\\analysis\\lil_B199_source_v5767\\all31_clean_current_complete_context.json': 'de574da7961bc9de9eafe19184f03b32157d15a5028ecf4dc714656d69029622', 'work/analysis/lil_B199_voices_v5768/current207_catalog_eight_voices_and_three_source_selectors.json': '04f6bfbe59b3b76899a247704357d270b283de6334cff255edf6d321c39e0a91', 'work/analysis/lil_B199_dispatches_v5769/all31_source_current_dispatches_one_FI_and16_control_leaves.json': '85fcc33238d6bd62d13275fdfb219d17e7c1c2fc63bae9f34455edda8afc0d90', 'work/analysis/lil_B199_branches_v5771/original_relative_skip_operand_proof.json': '00d8b43251b16c4f7d2bcca627fa45a62d428a87e812b2b4854e5fcce770fd81', 'work/analysis/lil_B199_entry_v5770/source_EV2_B199_action_dependency_and_native_getter_binding.json': '6062894dab82beca3c667f3d5476ccf279285895a9466c6419b5102c94c7c312', 'work/analysis/lil_B199_controls_v5778/sixteen_exact_leaves_four_resources_two_pictures_two47xx_pause_and_end.json': 'ad10168692a5a8005906c9313d56207f14e53db9a233d77e9318dc4b0e23be11', 'work/analysis/lil_B199_names_v5772/six_original_progressive_and_catalogue_name_consumers.json': '542672180605302d749c48ed1423d06b7250516017d6be601cd0621cde3ea3f1', 'work/analysis/couple_context_review_v5775/five_whole_source_contexts_paired_label_draft_and_B199_name_fields.json': '6032a8c0d25c06499f250762d7881d910aea1bfa2968baa2deba24f3e87d7a84', 'work\\analysis\\lil_B199_comparison_v5783b\\complete_clean_context_actual_source_and_project_name_reconciliation.json': '4b51addadaf0438e481c653dd64fc2bbf5516542b1753e897e893e1d6d815d2e', 'work\\analysis\\lil_B199_source_paths_v5782\\one_actual_source_path_and_complete_command_intervals.json': '9985aab655264b8a41d73efd519bb27ac9ccc636126f7d4bfe8ef3aa4241254b'}
CONTROL='work/analysis/lil_B199_dispatches_v5769/all31_source_current_dispatches_one_FI_and16_control_leaves.json'
TERMS='work\\analysis\\lil_B199_comparison_v5783b\\complete_clean_context_actual_source_and_project_name_reconciliation.json'

def profile_for(arm,source_block,consumer='progressive'):
    if sha(arm)!=ARM9_SHA or sha(source_block) not in BLOCKS:raise ValueError('Exact B199 source/current block and runtime required')
    for path,digest in DEPENDENCIES.items():
        if sha(Path(path).read_bytes())!=digest:raise ValueError('B199 source contract changed:'+path)
    control=json.loads(Path(CONTROL).read_bytes());cases=control['speech_dispatch_cases']
    if len(cases)!=62 or sum(r['source_selector']==254 for r in cases)!=2:raise ValueError('All31 source/current dispatch pairs required')
    if any(r['resolved_actor_ID'] is not None for r in cases if r['source_selector']==254):raise ValueError('FE must remain null actor')
    if control['source_macro_counts']!={'FI':1,'FA':0,'FO':0}:raise ValueError('Exactly one original FI macro required')
    terms=json.loads(Path(TERMS).read_bytes())
    if not terms['source_FE_four_impacts_not_stat_notice_or_named_speaker']:raise ValueError('Four-impact scene context required')
    if terms['source_actual_speeches']!=31 or terms['offline_only_speeches']:raise ValueError('Complete31-source-panel fixture evidence required')
    base=get_dialogue_profile('lil-opening-editorial-native-v1')
    if consumer=='progressive':
        return replace(base,name='lil-B199-progressive-runtime-bound-v1',leading_speaker_bytes=SELECTORS,
            metrics_source=base.metrics_source+';30 original54020 speeches,Lil2 voice3/Camille9 voice2/Samwell22 voice2,six name consumers.47 source commands/no choices or relatives/one2000/one end with two tailzeros.One source FI.V5756 unchanged font,width,guard and pair phase.')
    if consumer=='FE-paper':
        return replace(base,name='lil-B199-FE-runtime-bound-v1',leading_speaker_bytes=frozenset({254}),
            metrics_source=base.metrics_source+';one original24310 null actor then5473C four-impact sound-effect panel,no FE macros.228x48logical/228x64physical,conservative216px planning.All31 Japanese source panels observed;English scene and complete effect-body semantics unapproved.')
    raise ValueError('Unknown B199 consumer')
