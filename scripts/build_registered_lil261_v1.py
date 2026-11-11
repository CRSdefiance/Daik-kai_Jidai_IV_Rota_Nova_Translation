"""Stage and register the approved Lil B323–B335 cumulative successor."""

from pathlib import Path
import sys

from dk4tool.patch.lil261_release_v1 import plan_release
from scripts import build_registered_lil254_v1 as template
from scripts.prepare_lil261_registered_v1 import ARCHIVE, ARM, CLEAN, CONFIG, PARENT, QUALIFICATION, REGISTRY, FINAL, ROOT
from scripts.source_locked_derivation_v5118 import checked_text


STORED = ROOT / 'stored_v1/stored_native_verification.json'
OUT = Path('work/lil261_B323_B335_release_v1')
PROFILE = 'all-routes-lil261-b323-b335-dialogue-v1-20261110'
CANDIDATE = OUT / 'all_routes_lil261_B323_B335_candidate.nds'
MANIFEST = CANDIDATE.with_suffix('.manifest.json')
PATCH = CANDIDATE.with_suffix('.xdelta')
INVERSE_PATCH = OUT / 'clean_input_reconstruction_RESEARCH_ONLY.nds'
STAGED = OUT / 'staged_successor.json'
RELEASE = OUT / 'registered_release_verification.json'
STARTUP = OUT / 'own_registered_startup_verification.json'
GETTERS = OUT / 'own_registered_name_getters_v1.json'
PARENT_REGISTRY = OUT / 'release_stack_before_Lil261.json'
CHECK_SC1 = 'registered_Lil261_B323_B335_dialogue_and_complete_parent_target_inverse'
NEGATIVES = ROOT / 'registered_semantic_checks_v1/qualification.json'
SOURCE25_SPEC = template.SOURCE25_SPEC

stage_source = checked_text(template.stage_source, {
    "len(old_manifest['batches']) == 729 and len(old_manifest['checks']) == 64": "len(old_manifest['batches']) == 730 and len(old_manifest['checks']) == 65",
    "len(dialogue_proof['changed_records']) == 254": "len(dialogue_proof['changed_records']) == 261",
    "Staged Lil254 B312-B319.": "Staged Lil261 B323-B335.",
})
register_source = checked_text(template.register_source, {
    "r['id']) for r in bindings}) == 254": "r['id']) for r in bindings}) == 261",
    "sum(len(r['registered_native_pages']) for r in bindings)==254": "sum(len(r['registered_native_pages']) for r in bindings)==261",
    "verified_Lil278_B299_B311": "verified_Lil254_B312_B319",
    "lil254_B312_B319": "lil261_B323_B335",
    "Lil254_B312_B319": "Lil261_B323_B335",
    "Lil B312-B319 contextual expedition, ruins, divination and trade exchanges": "Lil B323-B335 contextual fog, cave, trade commissions, survey and alchemy exchanges",
    "scripts/build_registered_lil254_v1.py": "scripts/build_registered_lil261_v1.py",
    "result['batches'][:729] == old_manifest['batches'] and len(result['batches']) == 730": "result['batches'][:730] == old_manifest['batches'] and len(result['batches']) == 731",
    "len(result['checks']) == 65": "len(result['checks']) == 66",
    "'complete_stack_entries': 730, 'registered_manifest_entries': 730, 'passing_release_checks': 65": "'complete_stack_entries': 731, 'registered_manifest_entries': 731, 'passing_release_checks': 66",
    "'new_contextual_records': 254, 'prose_revisions': 151": "'new_contextual_records': 261, 'prose_revisions': 198",
    "'justified_retentions': 103,'physical_body_candidates':246,'native_FE_panels':7": "'justified_retentions': 63,'physical_body_candidates':255,'native_FE_panels':13",
    "Registered Lil254 B312-B319 with 730 entries and 65 release checks.": "Registered Lil261 B323-B335 with 731 entries and 66 release checks.",
})
env = {**template.env, **globals(), 'previous': template.template}
exec(compile(stage_source + '\n' + register_source, __file__, 'exec'), env)

if __name__ == '__main__':
    if sys.argv[1:] == ['--register']:
        env['register']()
    else:
        assert not sys.argv[1:]
        env['stage']()
