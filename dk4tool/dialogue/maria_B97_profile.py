"""Exact B97 consumers;physical216x64/4rows,source72-only two-page planning."""
from dataclasses import replace
from pathlib import Path
from dk4tool.dialogue.profiles import get_dialogue_profile
from dk4tool.patch.grand_race_menu_release import sha
ARM9_SHA='39b11636e9b9904f96e18691154c813ebcad6e61647db412fa60b7344221b4a1'
BLOCKS=frozenset(['4282e72bfd9fa80dac4d460db5bfab08bc23a157faa3621ec0d7a24f91e58412', '8ebaccbe57f9ee49c0e0c21b8a5f7a14e3524ebd6836e3a1d6c2cc4a64fd9443'])
SELECTORS=frozenset({3,10,180})
PAGED_SOURCE_SHA='7101280dd916152927a4b57fd35924affa25d3c56b92bc838b0a4f6ce10ec1e0'
DEPENDENCIES={'work\\analysis\\maria_B97_source_v4998\\all32_clean_current_complete_context.json': 'e91698d2df0cb6fb3b69df410d8d579a8d104f89367e29188f1590fc7eb6263d', 'work\\analysis\\maria_B97_controls_v5005\\eight_source_leaves_resource633E_item4820_hide_and_two_effects.json': '91aeffc24ca31325501dc01640efbfcd61d6eaa62b98d687757544dea2a60649', 'work\\analysis\\maria_B97_voices_v5000\\current207_catalog_eight_voices_and_three_Maria_selectors.json': 'e5936d8dc62a59d2a50b0769e637d2c33a3a4d511b6a8f816911756acc64da4a', 'work\\analysis\\maria_B97_dispatches_v5001\\all32_clean_current_Maria_dispatches_FE_and_FO.json': '13bccc619208836ce0a82d01be85eb25a3a8cfcde1076b2e7b86aef42dcad727', 'work\\analysis\\maria_B97_entry_v5002\\source_EV3_B97_action_dependency_and_native_getter_binding.json': 'bd43575b6501d7874f6aa54a1cfe081d1c86d971a799549b005237286a6fbe73', 'work\\analysis\\maria_B97_terms_v5006\\bound_Maria_Xien_Bandit_Li_Clan_Sao_Jorge_Proof_and_tablet_context.json': 'f28dbb5d7ce216fdb53ff37431a6168eda4843697f39657ff88bea61253f4ad3', 'work\\analysis\\maria_B97_names_v5003\\six_original_progressive_and_catalogue_name_consumers.json': 'eed359d9793db5890ba601a613971f4f89f8f39638dbb72c9a15c1fc3b0c2245', 'work\\analysis\\maria_B97_macros_v5004\\three_actors_default_and_real_FO20_alignment_cases.json': '39d5247b2f34aaa4157df5d61e5c583ced5eaefe8b987336ac70462bb7716112'}

def profile_for(arm,source_block,consumer='progressive',source_raw=None):
    if sha(arm)!=ARM9_SHA or sha(source_block) not in BLOCKS:raise ValueError('Exact Maria B97 source/current block and runtime required')
    for path,digest in DEPENDENCIES.items():
        if sha(Path(path).read_bytes())!=digest:raise ValueError('Maria B97 source contract changed:'+path)
    base=get_dialogue_profile('maria-story-shared-events-live')
    common=dict(balanced_wrapping=True,literal_prefix_policy='native-guard-v255',macro_widths={'FI':30,'FA':12,'FO':42,'I':12},macro_ascii_lengths={'FI':5,'FA':2,'FO':7})
    if consumer=='progressive':
        return replace(base,name='maria-B97-progressive-runtime-bound-v1',leading_speaker_bytes=SELECTORS,**common,metrics_source='B97 current captain3 Maria/Xien/Bandit voices3/5/0 and64 source/current dispatches.216x64 physical viewport,four16px rows.20 measured default macro cases bindMaria5/Li2/Li Clan7;one real FO. All40 commands/eight source leaves preserved. Current native and actual approval required.')
    if consumer=='progressive-two-page':
        if source_raw is None or sha(source_raw)!=PAGED_SOURCE_SHA:raise ValueError('Two-page plan is restricted to exact clean B97R72')
        return replace(base,name='maria-B97-progressive-two-page-runtime-bound-v1',leading_speaker_bytes=SELECTORS,max_lines=8,**common,metrics_source='Exact source72 only. max_lines8 is a bounded two-page host plan,not a taller native viewport. Original216x64 physical viewport,four16px rows per page and A continuation stay unchanged. Complete current native planes and fresh actual page advance remain required;historicalV288 is a lead,not current Maria proof.')
    if consumer=='FE-paper':
        return replace(base,name='maria-B97-FE-runtime-bound-v1',leading_speaker_bytes=frozenset({254}),**common,metrics_source='One original24310 null actor then5473C whisper sound.228x48 logical/228x64 physical;conservative216px host planning. No FE speech actor. Current font and focused actual approval required.')
    raise ValueError('Unknown B97 consumer')
