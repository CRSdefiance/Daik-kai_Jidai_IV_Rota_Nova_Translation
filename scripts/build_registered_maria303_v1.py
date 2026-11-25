"""Stage/register303 reviews, preserving the exact713-entry accepted cumulative prefix."""
from pathlib import Path
from types import SimpleNamespace
import sys
from scripts import build_registered_maria270_v2 as template
from scripts import build_registered_maria310_v1 as prior310
from scripts.prepare_maria303_registered_v2 import ARCHIVE, ARM, CLEAN, CONFIG, PARENT, QUALIFICATION, REGISTRY, FINAL, ROOT
from dk4tool.patch.maria303_release_v1 import plan_release
from dk4tool.script.format_safety_relocated_v2 import bind_registered_story_percent_guard
from scripts.source_locked_derivation_v5118 import checked_text

STORED = ROOT/'stored_v1/stored_native_verification.json'
OUT = Path('work/maria303_release_v1')
PROFILE = 'all-routes-maria303-dialogue-v1-20261109'
CANDIDATE = OUT/'all_routes_maria303_candidate.nds'
MANIFEST = CANDIDATE.with_suffix('.manifest.json')
PATCH = CANDIDATE.with_suffix('.xdelta')
INVERSE_PATCH = OUT/'clean_input_reconstruction_RESEARCH_ONLY.nds'
STAGED = OUT/'staged_successor.json'
RELEASE = OUT/'registered_release_verification.json'
STARTUP = OUT/'own_registered_startup_verification.json'
GETTERS = OUT/'own_registered_name_getters_v1.json'
PARENT_REGISTRY = OUT/'release_stack_before_Maria303.json'
CHECK_SC1 = 'registered_Maria303_dialogue_and_complete_parent_target_inverse'
NEGATIVES = ROOT/'registered_semantic_checks_v1/qualification.json'
SOURCE25_SPEC = template.SOURCE25_SPEC
predecessor = SimpleNamespace(CHECK_SC1=prior310.CHECK_SC1)

stage_source = checked_text(template.stage_source, {
    "assert Path(old_manifest['batches'][-1])==MARKET_CONFIG\n    assert old_manifest['checks'][MARKET_CHECK] and not release['market_gameplay_pending']\n    assert release['all_709_entries_114_accepted_layers_andASCII_right_bound_preserved'] and release['owned_Hodram_residual_surnames_verified']":
        "assert Path(old_manifest['batches'][-1]) == prior310.FINAL\n    assert old_manifest['checks'][prior310.CHECK_SC1]\n    assert release['registered_market_format_andboth_data_pointers_preserved'] and release['owned_Hodram_residual_surnames_verified']",
    "len(old_manifest['batches']) == 710 and len(old_manifest['checks']) == 45": "len(old_manifest['batches']) == 713 and len(old_manifest['checks']) == 48",
    "len(dialogue_proof['changed_records']) == 270": "len(dialogue_proof['changed_records']) == 303",
    "old_percent=old_manifest['story_percent_contract']\n    assert {k:v for k,v in percent.items() if k in old_percent and k!='exact_relocation_receipt'}=={k:v for k,v in old_percent.items() if k!='exact_relocation_receipt'}\n    assert percent['exact_prior_relocation_receipt']==old_percent['exact_relocation_receipt']\n    assert percent['additional_exact_source_bound_relocated_leading25_count']==2 and percent['total_exact_source_bound_relocated_leading25_count']==7":
        "assert percent == old_manifest['story_percent_contract']\n    assert percent['total_exact_source_bound_relocated_leading25_count'] == 7",
    'Staged Maria270.': 'Staged Maria303.',
})
register_source = checked_text(template.register_source, {
    'verified_market_goods_info_output_reused=True': 'verified_Maria310_output_reused=True',
    "r['id']) for r in bindings}) == 270": "r['id']) for r in bindings}) == 303",
    'verified_market_goods_info_predecessor=predecessor, maria270_late_dialogue': 'verified_Maria310_predecessor=predecessor, maria303_late_dialogue',
    'Maria B37–B49 contextual dialogue and wrapping, retaining the market fix.': 'Maria B58–B70 contextual dialogue, menus and wrapping, retaining every prior layer.',
    'release_stack.Maria270.pending.json': 'release_stack.Maria303.pending.json',
    'late_editorial:maria270': 'late_editorial:maria303',
    'Maria270_registered_successor_pipeline': 'Maria303_registered_successor_pipeline',
    "result['batches'][:710] == old_manifest['batches'] and len(result['batches']) == 711": "result['batches'][:713] == old_manifest['batches'] and len(result['batches']) == 714",
    "len(result['checks']) == 46": "len(result['checks']) == 49",
    "'complete_stack_entries': 711, 'registered_manifest_entries': 711, 'passing_release_checks': 46": "'complete_stack_entries': 714, 'registered_manifest_entries': 714, 'passing_release_checks': 49",
    "'new_contextual_records': 270, 'prose_revisions': 161": "'new_contextual_records': 303, 'prose_revisions': 181",
    "'justified_retentions': 109": "'justified_retentions': 122",
    'Registered Maria270 with711 entries and46 release checks.': 'Registered Maria303 with714 entries and49 release checks.',
})
env = {**template.env, **vars(template), **globals(), 'previous': predecessor, '__file__': __file__}
exec(compile(stage_source+'\n'+register_source, __file__+'::same-complete-cumulative-successor-contract714', 'exec'), env)

if __name__ == '__main__':
    if sys.argv[1:] == ['--register']:
        env['register']()
    else:
        assert not sys.argv[1:]
        env['stage']()
