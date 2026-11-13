"""Exact B159 source binding:41 progressive speeches/five original static actors."""
from dataclasses import replace
from pathlib import Path
from dk4tool.dialogue.profiles import get_dialogue_profile
from dk4tool.patch.grand_race_menu_release import sha
ARM9_SHA='d9415c1e0eb18c9eec9b76329f3dedb724a1a754a4829be103c6b958f927b9aa'
BLOCKS=frozenset(['af7e96911d35b904e312a04464284910fc0b9e9dd73c89be04ccc907955bdd4d', 'bc2916695045cf393482937421466af1c2f75238c19aeff86037ef2bb3648669'])
SELECTORS=frozenset({2,9,14,20,22})
DEPENDENCIES={'work\\analysis\\lil_B159_source_v3828\\all41_clean_current_complete_context.json': '3ed3559bcf94581f5b1cce911bb7f1f5f65da5a01137413b6f0cf8971b211481', 'work\\analysis\\lil_B159_source_v3828\\subset82_dispatches_and23_source_exact_control_leaves.json': '92bf8b9fbb56c6aaff3803fd7acd055b4c7a2eb28c66515680ccd86389daaf1d', 'work\\analysis\\lil_B159_B160_source_v3825\\voices_and_entry_evidence_rebind.json': 'f999f8032a0f8ca3481a48464198606863e2f74ac07e56c0c2e7def1427277d0', 'work\\analysis\\lil_B159_branches_v3829\\original_relative_skip_operand_proof.json': 'd1596510526daf148a924ea50b600e5a6c08cf7d334096a5230d6f6496c04e0f', 'work\\analysis\\lil_B159_source_v3828\\five_names_distinct_Samwell_consumers_and_original_entry_binding.json': '10474b12852febd5c52f532a51d358843b80222c3389cce3ccc66d04c6504b6e', 'work\\analysis\\lil_B159_controls_v3830\\six_predicates_four_resource_sites_one_effect_two_ends_and23_source_leaves.json': '7781087bcb1497c9d5a710adca6858328f3462a992cec0a6780808eff78d1ca0', 'work\\analysis\\lil_B159_name_consumers_v3827\\source_progressive_Samwell_Khan_vs_full_catalogue_middle_field.json': 'd5e459ed2efb772769e7800ffd240cb37b94355765ac63199d471d8b04cee96b'}
def profile_for(arm,source_block,consumer='progressive'):
    if sha(arm)!=ARM9_SHA or sha(source_block) not in BLOCKS:raise ValueError('Exact B159 clean/current source and runtime required')
    if consumer!='progressive':raise ValueError('Only original B159 progressive consumer is source-bound')
    for path,digest in DEPENDENCIES.items():
        if sha(Path(path).read_bytes())!=digest:raise ValueError('Source contract changed:'+path)
    base=get_dialogue_profile('lil-opening-editorial-native-v1')
    return replace(base,name='lil-B159-progressive-runtime-bound-v1',leading_speaker_bytes=SELECTORS,metrics_source=base.metrics_source+';41 original54020 speeches/five static actors, FI4,24 spans,23 leaves,one A000 andtwo ends;Samwell Khan original progressive name consumer separately bound. No natural eligibility claim.')
