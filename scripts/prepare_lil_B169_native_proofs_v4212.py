"""Derive six-static-actor dispatch, twelve-relative-site and B169 source-entry proofs."""
from pathlib import Path
from scripts.prepare_lil_B156_layout_v3705 import derive
from scripts.verify_village_wrap_v608 import save

ROOT = Path('work/analysis/lil_B169_native_tools_v4212')
OLD = 'lil_B168_source_v4168/all54_clean_current_complete_context'
SOURCE = 'lil_B169_source_v4211/all36_clean_current_complete_context'
if __name__ == '__main__':
    assert not ROOT.exists()
    tools = []
    tools.append(derive('scripts/reconcile_lil_B168_voices_v4170.py', 'scripts/reconcile_lil_B169_voices_v4213.py', {
        'Bind eight source-owned static names/voices': 'Bind six source-owned static names/voices',
        'lil_B168_voices_v4170': 'lil_B169_voices_v4213', OLD: SOURCE,
        'len(chosen)==8': 'len(chosen)==6', '::8_source_names': '::6_source_names',
        'current8_static_names_voices': 'current6_static_names_voices', 'fresh8_actor_names': 'fresh6_actor_names',
        'three_FE_source_objects_have_no_static_actor_getter_calls': 'no_FE_source_objects_or_static_getter_calls',
        'all54_dispatches_still_require_separate_proof': 'all36_dispatches_still_require_separate_proof',
        '8 static names/voices pass': '6 static names/voices pass',
    }))
    tools.append(derive('scripts/prove_lil_B168_dispatches_v4171.py', 'scripts/prove_lil_B169_dispatches_v4214.py', {
        'Bind108 source/current speech calls and16 exact non-relative control leaves.': 'Bind72 source/current speech calls and5 exact non-relative control leaves.',
        'lil_B168_dispatches_v4171': 'lil_B169_dispatches_v4214', OLD: SOURCE,
        'lil_B168_voices_v4170': 'lil_B169_voices_v4213',
        'len(cases)==108 and len(leaves)==16': 'len(cases)==72 and len(leaves)==5',
        "sum(c['source_selector']==254 for c in cases)==6": "sum(c['source_selector']==254 for c in cases)==0",
        'all54_source_current_dispatches_macros_FE_and16_control_leaves': 'all36_source_current_dispatches_FI5_FO2_and5_control_leaves',
        'all16_nonrelative_nonspeech_nonchoice_source_current_leaf_commands_exact': 'all5_nonrelative_nonspeech_nonchoice_source_current_leaf_commands_exact',
        'all8_static_actors_without_role_or_roster_fixture': 'all6_static_actors_without_role_or_roster_fixture',
        'three_FE_panels_keep_distinct_original_null_actor_modal_dispatch': 'no_FE_system_objects_in_this_source_scope',
        'actual_selected_B168_IDs': 'actual_selected_B169_IDs',
        '108 source/current dispatches pass:eight static actors,three FE panels,FI7/FA1/FO1. All16 nonrelative nontext leaves exact.': '72 source/current dispatches pass:six static actors,FI5/FO2,noFE. All5 nonrelative nontext leaves exact.',
    }))
    tools.append(derive('scripts/prove_lil_B168_branches_v4172.py', 'scripts/prove_lil_B169_branches_v4215.py', {
        'lil_B168_branches_v4172': 'lil_B169_branches_v4215', OLD: SOURCE,
    }))
    tools.append(derive('scripts/prove_lil_B168_entry_v4173.py', 'scripts/prove_lil_B169_entry_v4216.py', {
        'lil_B168_entry_v4173': 'lil_B169_entry_v4216', OLD: SOURCE,
        'lil_B168_voices_v4170': 'lil_B169_voices_v4213', 'B168': 'B169', 'in [168]': 'in [169]',
    }))
    ROOT.mkdir(parents=True)
    save(ROOT / 'source_derivation.json', dict(tools=tools, source_scope=dict(block=169, speech_objects=36,
        static_actors=[2,6,9,20,21,76], source_commands=53, relative_sites=12, FI=5, FA=0, FO=2,
        predicates=3, one_later_A000=True, FE=0, resources=0, presentations=0), no_ROM_registry_ledger_credit_change=True))
    print('Four source-bound B169 native proof successors created;no credit.')
