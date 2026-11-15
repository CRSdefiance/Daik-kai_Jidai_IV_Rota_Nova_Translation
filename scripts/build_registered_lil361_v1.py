"""Append361 reviewed records to the exact727-entry cumulative registered prefix."""
from pathlib import Path
from types import SimpleNamespace
import sys
from scripts import build_registered_lil269_v1 as template
from scripts.prepare_lil361_registered_v1 import ARCHIVE, ARM, CLEAN, CONFIG, PARENT, QUALIFICATION, REGISTRY, FINAL, ROOT
from dk4tool.patch.lil361_release_v1 import plan_release
from scripts.source_locked_derivation_v5118 import checked_text

STORED = ROOT / 'stored_v1/stored_native_verification.json'
OUT = Path('work/lil361_B283_B298_release_v1')
PROFILE = 'all-routes-lil361-b283-b298-dialogue-v1-20261110'
CANDIDATE = OUT / 'all_routes_lil361_B283_B298_candidate.nds'
MANIFEST = CANDIDATE.with_suffix('.manifest.json'); PATCH = CANDIDATE.with_suffix('.xdelta')
INVERSE_PATCH = OUT / 'clean_input_reconstruction_RESEARCH_ONLY.nds'
STAGED = OUT / 'staged_successor.json'; RELEASE = OUT / 'registered_release_verification.json'
STARTUP = OUT / 'own_registered_startup_verification.json'; GETTERS = OUT / 'own_registered_name_getters_v1.json'
PARENT_REGISTRY = OUT / 'release_stack_before_Lil361.json'
CHECK_SC1 = 'registered_Lil361_B283_B298_dialogue_and_complete_parent_target_inverse'
NEGATIVES = ROOT / 'registered_semantic_checks_v1/qualification.json'
SOURCE25_SPEC = template.SOURCE25_SPEC
predecessor = SimpleNamespace(CHECK_SC1=template.CHECK_SC1)

stage_source = checked_text(template.stage_source, {
    "len(old_manifest['batches']) == 726 and len(old_manifest['checks']) == 61":
        "len(old_manifest['batches']) == 727 and len(old_manifest['checks']) == 62",
    "len(dialogue_proof['changed_records']) == 269": "len(dialogue_proof['changed_records']) == 361",
    'Staged Lil269 B243-B282.': 'Staged Lil361 B283-B298.',
})
register_source = checked_text(template.register_source, {
    "r['id']) for r in bindings}) == 269": "r['id']) for r in bindings}) == 361",
    "sum(len(r['registered_native_pages']) for r in bindings)==269": "sum(len(r['registered_native_pages']) for r in bindings)==361",
    'verified_Lil382_residual_A_output_reused': 'verified_Lil269_B243_B282_output_reused',
    'verified_Lil382_residual_A_predecessor': 'verified_Lil269_B243_B282_predecessor',
    'lil269_B243_B282_late_dialogue': 'lil361_B283_B298_late_dialogue',
    'Lil B243-B282 contextual town, expedition, figurehead, riddle and wanted-person exchanges, readable wrapping, glyphs, menus and scoped names':
        'Lil B283-B298 contextual forest, cave, Angkor riddle, fog, cliff and wristband exchanges, readable wrapping, glyphs, menus and scoped names',
    'release_stack.Lil269_B243_B282.pending.json': 'release_stack.Lil361_B283_B298.pending.json',
    'late_editorial:lil269_B243_B282': 'late_editorial:lil361_B283_B298',
    'Lil269_B243_B282_registered_successor_pipeline': 'Lil361_B283_B298_registered_successor_pipeline',
    'scripts/build_registered_lil269_v1.py': 'scripts/build_registered_lil361_v1.py',
    "result['batches'][:726] == old_manifest['batches'] and len(result['batches']) == 727":
        "result['batches'][:727] == old_manifest['batches'] and len(result['batches']) == 728",
    "len(result['checks']) == 62": "len(result['checks']) == 63",
    "'complete_stack_entries': 727, 'registered_manifest_entries': 727, 'passing_release_checks': 62":
        "'complete_stack_entries': 728, 'registered_manifest_entries': 728, 'passing_release_checks': 63",
    "'new_contextual_records': 269, 'prose_revisions': 104": "'new_contextual_records': 361, 'prose_revisions': 178",
    "'justified_retentions': 165,'physical_body_candidates':262,'native_FE_panels':36":
        "'justified_retentions': 183,'physical_body_candidates':352,'native_FE_panels':15",
    'Registered Lil269 B243-B282 with727 entries and62 release checks.': 'Registered Lil361 B283-B298 with728 entries and63 release checks.',
})

env = {**template.env, **globals(), 'previous': predecessor, '__file__': __file__}
exec(compile(stage_source + '\n' + register_source, __file__ + '::same-complete-prefix-runtime-source25-andmixed-guards', 'exec'), env)
if __name__ == '__main__':
    if sys.argv[1:] == ['--register']:
        env['register']()
    else:
        assert not sys.argv[1:]
        env['stage']()
