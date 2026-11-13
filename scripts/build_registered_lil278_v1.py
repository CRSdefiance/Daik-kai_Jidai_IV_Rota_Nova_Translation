"""Append the 278 reviewed Lil records to the exact 728-entry cumulative prefix."""

from pathlib import Path
import sys

from dk4tool.patch.lil278_release_v1 import plan_release
from scripts import build_registered_lil361_v1 as template
from scripts.prepare_lil278_registered_v1 import ARCHIVE, ARM, CLEAN, CONFIG, PARENT, QUALIFICATION, REGISTRY, FINAL, ROOT
from scripts.source_locked_derivation_v5118 import checked_text


STORED = ROOT / 'stored_v1/stored_native_verification.json'
OUT = Path('work/lil278_B299_B311_release_v1')
PROFILE = 'all-routes-lil278-b299-b311-dialogue-v1-20261110'
CANDIDATE = OUT / 'all_routes_lil278_B299_B311_candidate.nds'
MANIFEST = CANDIDATE.with_suffix('.manifest.json')
PATCH = CANDIDATE.with_suffix('.xdelta')
INVERSE_PATCH = OUT / 'clean_input_reconstruction_RESEARCH_ONLY.nds'
STAGED = OUT / 'staged_successor.json'
RELEASE = OUT / 'registered_release_verification.json'
STARTUP = OUT / 'own_registered_startup_verification.json'
GETTERS = OUT / 'own_registered_name_getters_v1.json'
PARENT_REGISTRY = OUT / 'release_stack_before_Lil278.json'
CHECK_SC1 = 'registered_Lil278_B299_B311_dialogue_and_complete_parent_target_inverse'
NEGATIVES = ROOT / 'registered_semantic_checks_v1/qualification.json'
SOURCE25_SPEC = template.SOURCE25_SPEC

stage_source = checked_text(template.stage_source, {
    "len(old_manifest['batches']) == 727 and len(old_manifest['checks']) == 62":
        "len(old_manifest['batches']) == 728 and len(old_manifest['checks']) == 63",
    "len(dialogue_proof['changed_records']) == 361": "len(dialogue_proof['changed_records']) == 278",
    'Staged Lil361 B283-B298.': 'Staged Lil278 B299-B311.',
})
register_source = checked_text(template.register_source, {
    "r['id']) for r in bindings}) == 361": "r['id']) for r in bindings}) == 278",
    "sum(len(r['registered_native_pages']) for r in bindings)==361": "sum(len(r['registered_native_pages']) for r in bindings)==278",
    'verified_Lil269_B243_B282': 'verified_Lil361_B283_B298',
    'lil361_B283_B298': 'lil278_B299_B311',
    'Lil361_B283_B298': 'Lil278_B299_B311',
    'Lil B283-B298 contextual forest, cave, Angkor riddle, fog, cliff and wristband exchanges':
        'Lil B299-B311 contextual snake, oasis, Basra spice, ferry and temple exchanges',
    'scripts/build_registered_lil361_v1.py': 'scripts/build_registered_lil278_v1.py',
    "result['batches'][:727] == old_manifest['batches'] and len(result['batches']) == 728":
        "result['batches'][:728] == old_manifest['batches'] and len(result['batches']) == 729",
    "len(result['checks']) == 63": "len(result['checks']) == 64",
    "'complete_stack_entries': 728, 'registered_manifest_entries': 728, 'passing_release_checks': 63":
        "'complete_stack_entries': 729, 'registered_manifest_entries': 729, 'passing_release_checks': 64",
    "'new_contextual_records': 361, 'prose_revisions': 178": "'new_contextual_records': 278, 'prose_revisions': 170",
    "'justified_retentions': 183,'physical_body_candidates':352,'native_FE_panels':15":
        "'justified_retentions': 108,'physical_body_candidates':272,'native_FE_panels':8",
    'Registered Lil361 B283-B298 with728 entries and63 release checks.':
        'Registered Lil278 B299-B311 with 729 entries and 64 release checks.',
})

env = {**template.env, **globals(), 'previous': template.template}
exec(compile(stage_source + '\n' + register_source, __file__, 'exec'), env)

if __name__ == '__main__':
    if sys.argv[1:] == ['--register']:
        env['register']()
    else:
        assert not sys.argv[1:]
        env['stage']()
