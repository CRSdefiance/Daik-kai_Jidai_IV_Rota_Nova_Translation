"""Stage/register Maria270 while retaining the entire 710-entry corrected prefix."""
from pathlib import Path
from types import SimpleNamespace
import sys
from scripts import build_registered_maria301_v1 as template
from scripts.prepare_maria270_registered_v2 import ARCHIVE,ARM,CLEAN,CONFIG,PARENT,QUALIFICATION,REGISTRY,FINAL,ROOT
from dk4tool.patch.maria270_release_v1 import plan_release
from scripts.source_locked_derivation_v5118 import checked_text

STORED=ROOT/'stored270_v1/stored_native_verification.json'
OUT=Path('work/maria270_release_v1')
PROFILE='all-routes-maria270-dialogue-v1-20261109'
CANDIDATE=OUT/'all_routes_maria270_candidate.nds'
MANIFEST=CANDIDATE.with_suffix('.manifest.json');PATCH=CANDIDATE.with_suffix('.xdelta')
INVERSE_PATCH=OUT/'clean_input_reconstruction_RESEARCH_ONLY.nds'
STAGED=OUT/'staged_successor.json';RELEASE=OUT/'registered_release_verification.json'
STARTUP=OUT/'own_registered_startup_verification.json';GETTERS=OUT/'own_registered_name_getters_v1.json'
PARENT_REGISTRY=OUT/'release_stack_before_Maria270.json'
CHECK_SC1='registered_Maria270_dialogue_and_complete_parent_target_inverse'
NEGATIVES=ROOT/'registered_semantic_checks_v1/qualification.json'
MARKET_CONFIG=Path('work/market_goods_info_terminator_release_v1/market_goods_info_terminator_release.json')
MARKET_CHECK='registered_market_goods_info_terminated_format_and_complete_parent_inverse'
predecessor=SimpleNamespace(CHECK_SC1=MARKET_CHECK)

stage_source=checked_text(template.stage_source,{
    "assert Path(old_manifest['batches'][-2])==previous.FINAL\n    assert Path(old_manifest['batches'][-1])==previous.NAME_CONFIG\n    assert release['owned_Hodram_residual_surnames_verified']":
        "assert Path(old_manifest['batches'][-1])==MARKET_CONFIG\n    assert old_manifest['checks'][MARKET_CHECK] and not release['market_gameplay_pending']\n    assert release['all_709_entries_114_accepted_layers_andASCII_right_bound_preserved'] and release['owned_Hodram_residual_surnames_verified']",
    "len(old_manifest['batches']) == 708 and len(old_manifest['checks']) == 43":"len(old_manifest['batches']) == 710 and len(old_manifest['checks']) == 45",
    "len(dialogue_proof['changed_records']) == 301":"len(dialogue_proof['changed_records']) == 270",
    'all_other_files_components_graphics_names_andruntime_exact_to_parent=True,':
        'all_other_files_components_graphics_names_andruntime_exact_to_parent=True,registered_market_format_andboth_data_pointers_preserved=True,',
    'Staged Maria301.':'Staged Maria270.',
})
register_source=checked_text(template.register_source,{
    'verified_Hodram_residual_output_reused=True':'verified_market_goods_info_output_reused=True',
    "r['id']) for r in bindings}) == 301":"r['id']) for r in bindings}) == 270",
    'verified_hodram_residual_predecessor=predecessor, maria301_late_dialogue':'verified_market_goods_info_predecessor=predecessor, maria270_late_dialogue',
    'Maria B0–B32 contextual dialogue and wrapping.':'Maria B37–B49 contextual dialogue and wrapping, retaining the market fix.',
    'release_stack.Maria301.pending.json':'release_stack.Maria270.pending.json',
    'late_editorial:maria301':'late_editorial:maria270','Maria301_registered_successor_pipeline':'Maria270_registered_successor_pipeline',
    "result['batches'][:708] == old_manifest['batches'] and len(result['batches']) == 709":"result['batches'][:710] == old_manifest['batches'] and len(result['batches']) == 711",
    "len(result['checks']) == 44":"len(result['checks']) == 46",
    "'complete_stack_entries': 709, 'registered_manifest_entries': 709, 'passing_release_checks': 44":"'complete_stack_entries': 711, 'registered_manifest_entries': 711, 'passing_release_checks': 46",
    "'new_contextual_records': 301, 'prose_revisions': 178":"'new_contextual_records': 270, 'prose_revisions': 161",
    "'justified_retentions': 123":"'justified_retentions': 109",
    'Registered Maria301 with709 entries and44 release checks.':'Registered Maria270 with711 entries and46 release checks.',
})
env={**template.env,**vars(template),**globals(),'previous':predecessor,'__file__':__file__}
exec(compile(stage_source+'\n'+register_source,__file__+'::same-complete-cumulative-contract-exact-market-fixed-predecessor','exec'),env)
if __name__=='__main__':
    if sys.argv[1:]==['--register']:env['register']()
    else:assert not sys.argv[1:];env['stage']()
