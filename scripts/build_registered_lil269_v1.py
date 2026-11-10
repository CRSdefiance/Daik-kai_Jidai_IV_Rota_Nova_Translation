"""Append269 reviewed objects to the exact726-entry registered cumulative prefix."""
from pathlib import Path
from types import SimpleNamespace
import sys
from scripts import build_registered_lil382_v1 as template
from scripts.prepare_lil269_registered_v1 import ARCHIVE, ARM, CLEAN, CONFIG, PARENT, QUALIFICATION, REGISTRY, FINAL, ROOT
from dk4tool.patch.lil269_release_v1 import plan_release
from scripts.source_locked_derivation_v5118 import checked_text

STORED = ROOT / 'stored_v1/stored_native_verification.json'
OUT = Path('work/lil269_B243_B282_release_v1')
PROFILE = 'all-routes-lil269-b243-b282-dialogue-v1-20261110'
CANDIDATE = OUT / 'all_routes_lil269_B243_B282_candidate.nds'
MANIFEST = CANDIDATE.with_suffix('.manifest.json'); PATCH = CANDIDATE.with_suffix('.xdelta')
INVERSE_PATCH = OUT / 'clean_input_reconstruction_RESEARCH_ONLY.nds'
STAGED = OUT / 'staged_successor.json'; RELEASE = OUT / 'registered_release_verification.json'
STARTUP = OUT / 'own_registered_startup_verification.json'; GETTERS = OUT / 'own_registered_name_getters_v1.json'
PARENT_REGISTRY = OUT / 'release_stack_before_Lil269.json'
CHECK_SC1 = 'registered_Lil269_B243_B282_dialogue_and_complete_parent_target_inverse'
NEGATIVES = ROOT / 'registered_semantic_checks_v1/qualification.json'
SOURCE25_SPEC = template.SOURCE25_SPEC
predecessor = SimpleNamespace(CHECK_SC1=template.CHECK_SC1)

stage_source = checked_text(template.stage_source, {
    "len(old_manifest['batches']) == 725 and len(old_manifest['checks']) == 60":
        "len(old_manifest['batches']) == 726 and len(old_manifest['checks']) == 61",
    "len(dialogue_proof['changed_records']) == 382": "len(dialogue_proof['changed_records']) == 269",
    'Staged Lil382 residual A.': 'Staged Lil269 B243-B282.',
})
register_source = checked_text(template.register_source, {
    "r['id']) for r in bindings}) == 382": "r['id']) for r in bindings}) == 269",
    "sum(len(r['registered_native_pages']) for r in bindings)==382": "sum(len(r['registered_native_pages']) for r in bindings)==269",
    'verified_Maria315_B286_B302_output_reused': 'verified_Lil382_residual_A_output_reused',
    'verified_Maria315_B286_B302_predecessor': 'verified_Lil382_residual_A_predecessor',
    'lil382_residual_A_late_dialogue': 'lil269_B243_B282_late_dialogue',
    'Lil residual A contextual crew, Aziza, cross-story, letters, town and quest exchanges, readable wrapping, glyphs, menus and scoped names':
        'Lil B243-B282 contextual town, expedition, figurehead, riddle and wanted-person exchanges, readable wrapping, glyphs, menus and scoped names',
    'release_stack.Lil382_residual_A.pending.json': 'release_stack.Lil269_B243_B282.pending.json',
    'late_editorial:lil382_residual_A': 'late_editorial:lil269_B243_B282',
    'Lil382_residual_A_registered_successor_pipeline': 'Lil269_B243_B282_registered_successor_pipeline',
    'scripts/build_registered_lil382_v1.py': 'scripts/build_registered_lil269_v1.py',
    "result['batches'][:725] == old_manifest['batches'] and len(result['batches']) == 726":
        "result['batches'][:726] == old_manifest['batches'] and len(result['batches']) == 727",
    "len(result['checks']) == 61": "len(result['checks']) == 62",
    "'complete_stack_entries': 726, 'registered_manifest_entries': 726, 'passing_release_checks': 61":
        "'complete_stack_entries': 727, 'registered_manifest_entries': 727, 'passing_release_checks': 62",
    "'new_contextual_records': 382, 'prose_revisions': 257": "'new_contextual_records': 269, 'prose_revisions': 104",
    "'justified_retentions': 125,'physical_body_candidates':378,'native_FE_panels':3":
        "'justified_retentions': 165,'physical_body_candidates':262,'native_FE_panels':36",
    'Registered Lil382 residual A with726 entries and61 release checks.': 'Registered Lil269 B243-B282 with727 entries and62 release checks.',
})
env = {**template.env, **globals(), 'previous': predecessor, '__file__': __file__}
exec(compile(stage_source + '\n' + register_source, __file__ + '::same-complete-prefix-runtime-source25-andmixed-guards', 'exec'), env)
if __name__ == '__main__':
    if sys.argv[1:] == ['--register']:
        env['register']()
    else:
        assert not sys.argv[1:]
        env['stage']()
