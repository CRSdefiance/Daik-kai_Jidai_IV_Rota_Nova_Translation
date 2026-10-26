"""Exact B33/runtime-scoped profile, including the native Xien0A selector."""
import json
from dataclasses import replace
from pathlib import Path

from dk4tool.dialogue.profiles import get_dialogue_profile
from dk4tool.patch.grand_race_menu_release import sha

PROOF = Path('work/analysis/maria_opening_approval_v2045/source_bound_presentation_macro_and_visual_contract.json')
PROOF_SHA = '9ed5d1aa04ffcc70e52bc3e00d6174360054807d4b3b3e76784fb6d629ca9cc1'
ARM9_SHA = '500b7d6cea559d7252ae4e67f94540e67739428823a17cf26842b6827712a41e'
SOURCE_SHA = '576c40906ac944b5f0ba26422c05691325df618fcb3890b803b4efd0862726d5'


def profile_for(arm, source_block, number, *, modal=False):
    if modal or number != 33 or sha(arm) != ARM9_SHA or sha(source_block) != SOURCE_SHA:
        raise ValueError('Maria opening requires the exact progressive B33/runtime scope')
    if sha(PROOF.read_bytes()) != PROOF_SHA:
        raise ValueError('Maria opening presentation proof differs')
    proof = json.loads(PROOF.read_text(encoding='utf-8'))
    flags = (
        'clean_current_complete_six_byte_preambles_and_CS0101_equal',
        'source0A_is_Xien_actor_not_text_LF',
        'all_six_actual_portraits_complete_nameplates_and38_body_panels_viewed',
        'native_selectors_and_isolated_copy_full_catalog_names_verified',
        'all38_logical_wrapped_macros_four_alignments308_calls_and_all4MiB_ABI_guards_pass',
        'all38_complete_native_independent_planes_and_final_parity_equal',
        'all5_native_and7_actual_review_sheets_viewed_no_warnings_or_waivers',
        'native_literal_guard_and_source_runtime_substitutions_preserved',
        'CS0101_85_commands47_opaque_commands303_loads606_parent_modes_exact',
        'actual_original_and_revised38_speeches85_commands_normal_Hangzhou_return',
        'existing_system_unlock_save_not_earned_no_story_location_RNG_funds_outcome_or_savestate_fixture',
    )
    if not all(proof.get(key) is True for key in flags):
        raise ValueError('Maria opening requires complete native and representative actual evidence')
    if proof['macro_ascii_lengths'] != {'FI': 5, 'FA': 2, 'FO': 7}:
        raise ValueError('Maria opening measured native substitutions differ')
    base = get_dialogue_profile('maria-story-shared-events-live')
    if base.literal_prefix_policy != 'forbid' or base.macro_ascii_lengths['FA'] != 3:
        raise ValueError('Global Maria profile changed; review this private scope again')
    return replace(
        base, name='maria-opening-editorial-native-v1',
        leading_speaker_bytes=frozenset({10, 21, 74}), balanced_wrapping=True,
        literal_prefix_policy='native-guard-v255',
        macro_widths={'FI': 30, 'FA': 12, 'FO': 42, 'I': 12},
        macro_ascii_lengths={'FI': 5, 'FA': 2, 'FO': 7},
        metrics_source='V2045 exact B33:38 native/actual panels,308 guarded macro calls,default Maria5/Li2/LiClan7,six actual portraits and normal Hangzhou return.',
    )
