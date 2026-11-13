"""Stage and register the approved Lil B312–B319 cumulative successor."""

from pathlib import Path
import sys

from dk4tool.patch.lil254_release_v1 import plan_release
from scripts import build_registered_lil278_v1 as template
from scripts.prepare_lil254_registered_v1 import ARCHIVE, ARM, CLEAN, CONFIG, PARENT, QUALIFICATION, REGISTRY, FINAL, ROOT
from scripts.source_locked_derivation_v5118 import checked_text


STORED = ROOT / 'stored_v1/stored_native_verification.json'
OUT = Path('work/lil254_B312_B319_release_v1')
PROFILE = 'all-routes-lil254-b312-b319-dialogue-v1-20261110'
CANDIDATE = OUT / 'all_routes_lil254_B312_B319_candidate.nds'
MANIFEST = CANDIDATE.with_suffix('.manifest.json')
PATCH = CANDIDATE.with_suffix('.xdelta')
INVERSE_PATCH = OUT / 'clean_input_reconstruction_RESEARCH_ONLY.nds'
STAGED = OUT / 'staged_successor.json'
RELEASE = OUT / 'registered_release_verification.json'
STARTUP = OUT / 'own_registered_startup_verification.json'
GETTERS = OUT / 'own_registered_name_getters_v1.json'
PARENT_REGISTRY = OUT / 'release_stack_before_Lil254.json'
CHECK_SC1 = 'registered_Lil254_B312_B319_dialogue_and_complete_parent_target_inverse'
NEGATIVES = ROOT / 'registered_semantic_checks_v1/qualification.json'
SOURCE25_SPEC = template.SOURCE25_SPEC

stage_source = checked_text(template.stage_source, {
    "len(old_manifest['batches']) == 728 and len(old_manifest['checks']) == 63":
        "len(old_manifest['batches']) == 729 and len(old_manifest['checks']) == 64",
    "len(dialogue_proof['changed_records']) == 278": "len(dialogue_proof['changed_records']) == 254",
    'Staged Lil278 B299-B311.': 'Staged Lil254 B312-B319.',
})
register_source = checked_text(template.register_source, {
    "r['id']) for r in bindings}) == 278": "r['id']) for r in bindings}) == 254",
    "sum(len(r['registered_native_pages']) for r in bindings)==278":
        "sum(len(r['registered_native_pages']) for r in bindings)==254",
    'verified_Lil361_B283_B298': 'verified_Lil278_B299_B311',
    'lil278_B299_B311': 'lil254_B312_B319',
    'Lil278_B299_B311': 'Lil254_B312_B319',
    'Lil B299-B311 contextual snake, oasis, Basra spice, ferry and temple exchanges':
        'Lil B312-B319 contextual expedition, ruins, divination and trade exchanges',
    'scripts/build_registered_lil278_v1.py': 'scripts/build_registered_lil254_v1.py',
    "result['batches'][:728] == old_manifest['batches'] and len(result['batches']) == 729":
        "result['batches'][:729] == old_manifest['batches'] and len(result['batches']) == 730",
    "len(result['checks']) == 64": "len(result['checks']) == 65",
    "'complete_stack_entries': 729, 'registered_manifest_entries': 729, 'passing_release_checks': 64":
        "'complete_stack_entries': 730, 'registered_manifest_entries': 730, 'passing_release_checks': 65",
    "'new_contextual_records': 278, 'prose_revisions': 170": "'new_contextual_records': 254, 'prose_revisions': 151",
    "'justified_retentions': 108,'physical_body_candidates':272,'native_FE_panels':8":
        "'justified_retentions': 103,'physical_body_candidates':246,'native_FE_panels':7",
    'Registered Lil278 B299-B311 with 729 entries and 64 release checks.':
        'Registered Lil254 B312-B319 with 730 entries and 65 release checks.',
})

env = {**template.env, **globals(), 'previous': template.template}
exec(compile(stage_source + '\n' + register_source, __file__, 'exec'), env)

if __name__ == '__main__':
    if sys.argv[1:] == ['--register']:
        env['register']()
    else:
        assert not sys.argv[1:]
        env['stage']()
