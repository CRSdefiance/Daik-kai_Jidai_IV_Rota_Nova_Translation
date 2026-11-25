"""Append315 reviews to the724-entry prefix; require own startup before registration."""
from pathlib import Path
from types import SimpleNamespace
import sys
from scripts import build_registered_maria349_v1 as template
from scripts.prepare_maria315_registered_v1 import ARCHIVE, ARM, CLEAN, CONFIG, PARENT, QUALIFICATION, REGISTRY, FINAL, ROOT
from dk4tool.patch.maria315_release_v1 import plan_release
from scripts.source_locked_derivation_v5118 import checked_text

STORED = ROOT/'stored_v1/stored_native_verification.json'
OUT = Path('work/maria315_B286_B302_release_v1')
PROFILE = 'all-routes-maria315-b286-b302-dialogue-v1-20261110'
CANDIDATE = OUT/'all_routes_maria315_B286_B302_candidate.nds'
MANIFEST = CANDIDATE.with_suffix('.manifest.json')
PATCH = CANDIDATE.with_suffix('.xdelta')
INVERSE_PATCH = OUT/'clean_input_reconstruction_RESEARCH_ONLY.nds'
STAGED = OUT/'staged_successor.json'
RELEASE = OUT/'registered_release_verification.json'
STARTUP = OUT/'own_registered_startup_verification.json'
GETTERS = OUT/'own_registered_name_getters_v1.json'
PARENT_REGISTRY = OUT/'release_stack_before_Maria315.json'
CHECK_SC1 = 'registered_Maria315_B286_B302_dialogue_and_complete_parent_target_inverse'
NEGATIVES = ROOT/'registered_semantic_checks_v1/qualification.json'
SOURCE25_SPEC = template.SOURCE25_SPEC
predecessor = SimpleNamespace(CHECK_SC1=template.CHECK_SC1)
stage_source = checked_text(template.stage_source, {
    "len(old_manifest['batches']) == 723 and len(old_manifest['checks']) == 58":
        "len(old_manifest['batches']) == 724 and len(old_manifest['checks']) == 59",
    "len(dialogue_proof['changed_records']) == 349": "len(dialogue_proof['changed_records']) == 315",
    'Staged Maria349 B275-B285.': 'Staged Maria315 B286-B302.',
})
register_source = checked_text(template.register_source, {
    "r['id']) for r in bindings}) == 349": "r['id']) for r in bindings}) == 315",
    "sum(len(r['registered_native_pages']) for r in bindings)==349":
        "sum(len(r['registered_native_pages']) for r in bindings)==315",
    'verified_Maria359_B253_B274_output_reused': 'verified_Maria349_B275_B285_output_reused',
    'verified_Maria359_B253_B274_predecessor': 'verified_Maria349_B275_B285_predecessor',
    'maria349_B275_B285_late_dialogue': 'maria315_B286_B302_late_dialogue',
    'Maria B275–B285 contextual smuggler andimpostor exchanges, guardian clue, forest/desert exploration, readable wrapping, menus andscoped names':
        'Maria B286–B302 contextual incense, armor, fog/cave, ghost ship, guardian, Sextant andmonk/book exchanges, readable wrapping, glyphs, menus andscoped names',
    'release_stack.Maria349_B275_B285.pending.json': 'release_stack.Maria315_B286_B302.pending.json',
    'late_editorial:maria349_B275_B285': 'late_editorial:maria315_B286_B302',
    'Maria349_B275_B285_registered_successor_pipeline': 'Maria315_B286_B302_registered_successor_pipeline',
    'scripts/build_registered_maria349_v1.py': 'scripts/build_registered_maria315_v1.py',
    "result['batches'][:723] == old_manifest['batches'] and len(result['batches']) == 724":
        "result['batches'][:724] == old_manifest['batches'] and len(result['batches']) == 725",
    "len(result['checks']) == 59": "len(result['checks']) == 60",
    "'complete_stack_entries': 724, 'registered_manifest_entries': 724, 'passing_release_checks': 59":
        "'complete_stack_entries': 725, 'registered_manifest_entries': 725, 'passing_release_checks': 60",
    "'new_contextual_records': 349, 'prose_revisions': 184":
        "'new_contextual_records': 315, 'prose_revisions': 162",
    "'justified_retentions': 165,'physical_body_candidates':341,'native_FE_panels':7":
        "'justified_retentions': 153,'physical_body_candidates':309,'native_FE_panels':13",
    'Registered Maria349 B275-B285 with724 entries and59 release checks.':
        'Registered Maria315 B286-B302 with725 entries and60 release checks.',
})
env = {**template.env, **globals(), 'previous': predecessor, '__file__': __file__}
exec(compile(stage_source+'\n'+register_source, __file__+'::same-cumulative-prefix-runtime-source25-andmixed-guards', 'exec'), env)
if __name__ == '__main__':
    if sys.argv[1:] == ['--register']:
        env['register']()
    else:
        assert not sys.argv[1:]
        env['stage']()
