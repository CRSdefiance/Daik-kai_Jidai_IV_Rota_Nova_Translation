"""Private profiles bound to the reviewed three-block native display contract."""
import json
from dataclasses import replace
from pathlib import Path

from dk4tool.dialogue.profiles import get_dialogue_profile
from dk4tool.patch.grand_race_menu_release import sha

PROOF = Path('work/analysis/hodram_opening_approval_v2028/source_bound_presentation_macro_and_visual_contract.json')
PROOF_SHA = 'f11e19d8af50298e465c8053ad6f6f832a96664db5e8e2d411d7b51930c8aeef'
ARM9_SHA = '500b7d6cea559d7252ae4e67f94540e67739428823a17cf26842b6827712a41e'


def profile_for(arm, source_block, number, *, modal=False):
    if sha(PROOF.read_bytes()) != PROOF_SHA or sha(arm) != ARM9_SHA:
        raise ValueError('Hodram opening native presentation/runtime proof differs')
    proof = json.loads(PROOF.read_text(encoding='utf-8'))
    if sha(source_block) != proof['source_blocks_sha256'].get(str(number)):
        raise ValueError('Hodram opening requires an exact proven source block')
    flags = (
        'clean_and_current_complete_speech_preambles_equal',
        'FE_owned_by_separate_original_mode1_consumer',
        'actual_Hodram_Gerhard_Charles_Manuel_portraits_full_nameplates_and37_complete_panels_viewed',
        'exact_runtime_Lil_Camille_source02_09_live_controls_inherited',
        'native_selector_same_on_current_route1_all_six_actors_and_isolated_catalog_names_verified',
        'all67_progressive_planes540_macro_calls_and_six_FE_planes48_null_actor_calls_pass',
        'all73_final_parity_native_planes_exact',
        'native_literal_guard_F_I_and_source_substitutions_preserved',
        'all9_progressive_and1_FE_preview_sheets_and7_actual_sheets_viewed',
        'ordinary_revised_opening_normal_Stockholm_return_and_current_departure_context_verified',
    )
    if not all(proof.get(key) is True for key in flags):
        raise ValueError('Hodram opening complete native and representative actual evidence required')
    if proof['macro_ascii_lengths'] != {'FI': 6, 'FA': 9, 'FO': 15}:
        raise ValueError('Hodram opening native substitutions differ')
    base = get_dialogue_profile('hodram-story-live')
    if base.literal_prefix_policy != 'forbid':
        raise ValueError('Global Hodram profile changed; review the private scope again')
    return replace(
        base,
        name='hodram-opening-editorial-native-v1' + ('-FE' if modal else ''),
        leading_speaker_bytes=frozenset({254} if modal else {16, 18, 23}),
        balanced_wrapping=True,
        literal_prefix_policy='native-guard-v255',
        macro_widths={'FI': 36, 'FA': 54, 'FO': 90, 'I': 12},
        macro_ascii_lengths={'FI': 6, 'FA': 9, 'FO': 15},
        metrics_source='V2028 source-bound73 planes,588 macro calls and37 actual opening panels. FE uses its separate228x48 native consumer.',
    )
