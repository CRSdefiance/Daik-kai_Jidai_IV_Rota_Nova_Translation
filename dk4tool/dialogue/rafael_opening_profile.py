"""Exact B44/runtime-scoped progressive profile; global profiles stay unchanged."""
import json
from dataclasses import replace
from pathlib import Path

from dk4tool.dialogue.profiles import get_dialogue_profile
from dk4tool.patch.grand_race_menu_release import sha

PROOF = Path('work/analysis/rafael_opening_approval_v2010b/source_bound_presentation_macro_and_visual_contract.json')
PROOF_SHA = '8b23d03e1a791471bd7a14c29ce6eeef10ad9937c64981182166f06dd6016576'
ARM9_SHA = '500b7d6cea559d7252ae4e67f94540e67739428823a17cf26842b6827712a41e'
SOURCE_SHA = 'da3b1abf8e644c355fa1653534fc90c0728aca3f3ec49958c21d11d3ac6047cb'


def profile_for(arm, source_block):
    if sha(arm) != ARM9_SHA or sha(source_block) != SOURCE_SHA:
        raise ValueError('Rafael opening requires the exact proven runtime and current B44')
    if sha(PROOF.read_bytes()) != PROOF_SHA:
        raise ValueError('Rafael opening source-bound presentation proof differs')
    proof = json.loads(PROOF.read_text(encoding='utf-8'))
    flags = (
        'clean_and_current_complete_speech_preambles_equal',
        'actual_Rafael_Janus_Claudio_Julio_portraits_and_complete_nameplates_viewed',
        'all114_logical_and_wrapped_macro_inputs_four_alignments_all4MiB_ABI_guards_pass',
        'native_literal_guard_F_and_I_preserves_real_macros_and_forbids_IC_I_control_suffix_collisions',
        'native_font_planes114_and_all15_review_sheets_viewed',
        'all114_final_parity_native_planes_equal_reviewed_planes',
        'source00_actor_byte_owned_by_whole_native_preamble_not_NUL_text_formatter',
        'both_ordinary_controller_choices_repaired_skips_and_normal_Lisbon_returns_verified',
    )
    if not all(proof.get(key) is True for key in flags):
        raise ValueError('Rafael opening requires complete native and actual presentation evidence')
    if proof['macro_ascii_lengths'] != {'FI': 6, 'FA': 6, 'FO': 10}:
        raise ValueError('Rafael opening measured native substitutions differ')
    base = get_dialogue_profile('raphael-story-live')
    if base.literal_prefix_policy != 'forbid' or base.macro_ascii_lengths['FI'] != 7:
        raise ValueError('Global Rafael profile changed; review the scoped contract again')
    return replace(
        base,
        name='rafael-opening-editorial-native-v1',
        balanced_wrapping=True,
        literal_prefix_policy='native-guard-v255',
        macro_widths={'FI': 36, 'FA': 36, 'FO': 60, 'I': 12},
        macro_ascii_lengths={'FI': 6, 'FA': 6, 'FO': 10},
        metrics_source='Exact B44/V2010b:114 native planes,916 macro calls,default Rafael6/Castor6/CastorCo.10,both ordinary choices and Lisbon returns.',
    )
