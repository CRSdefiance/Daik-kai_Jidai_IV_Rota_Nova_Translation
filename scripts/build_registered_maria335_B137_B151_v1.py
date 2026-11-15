"""Preserve the717-entry prefix and append335 reviewed source objects."""
from pathlib import Path
from types import SimpleNamespace
import sys
from scripts import build_registered_maria337_v1 as template
from scripts.prepare_maria335_B137_B151_registered_v2 import ARCHIVE,ARM,CLEAN,CONFIG,PARENT,QUALIFICATION,REGISTRY,FINAL,ROOT
from dk4tool.patch.maria335_B137_B151_release_v1 import plan_release
from scripts.source_locked_derivation_v5118 import checked_text

STORED=ROOT/'stored_v1/stored_native_verification.json'
OUT=Path('work/maria335_B137_B151_release_v1')
PROFILE='all-routes-maria335-b137-b151-dialogue-v1-20261109'
CANDIDATE=OUT/'all_routes_maria335_B137_B151_candidate.nds'
MANIFEST=CANDIDATE.with_suffix('.manifest.json');PATCH=CANDIDATE.with_suffix('.xdelta')
INVERSE_PATCH=OUT/'clean_input_reconstruction_RESEARCH_ONLY.nds'
STAGED=OUT/'staged_successor.json';RELEASE=OUT/'registered_release_verification.json'
STARTUP=OUT/'own_registered_startup_verification.json';GETTERS=OUT/'own_registered_name_getters_v1.json'
PARENT_REGISTRY=OUT/'release_stack_before_Maria335_B137_B151.json'
CHECK_SC1='registered_Maria335_B137_B151_dialogue_and_complete_parent_target_inverse'
NEGATIVES=ROOT/'registered_semantic_checks_v1/qualification.json'
SOURCE25_SPEC=template.SOURCE25_SPEC
predecessor=SimpleNamespace(CHECK_SC1=template.CHECK_SC1)

stage_source=checked_text(template.stage_source,{
    "len(old_manifest['batches']) == 716 and len(old_manifest['checks']) == 51":
        "len(old_manifest['batches']) == 717 and len(old_manifest['checks']) == 52",
    "len(dialogue_proof['changed_records']) == 337":"len(dialogue_proof['changed_records']) == 335",
    'Staged Maria337.':'Staged Maria335 B137-B151.',
})
register_source=checked_text(template.register_source,{
    "r['id']) for r in bindings}) == 337":"r['id']) for r in bindings}) == 335",
    "sum(len(r['registered_native_pages']) for r in bindings)==337":"sum(len(r['registered_native_pages']) for r in bindings)==335",
    'verified_Maria330_output_reused':'verified_Maria337_output_reused',
    'verified_Maria330_predecessor':'verified_Maria337_predecessor',
    'maria337_late_dialogue':'maria335_B137_B151_late_dialogue',
    'Maria B125–B136 contextual dialogue, tutorial wrapping and repaired choice captions':
        'Maria B137–B151 contextual dialogue, tutorial and glyph repairs, scoped FE guards and complete captions',
    'release_stack.Maria337.pending.json':'release_stack.Maria335_B137_B151.pending.json',
    'late_editorial:maria337':'late_editorial:maria335_B137_B151',
    'Maria337_registered_successor_pipeline':'Maria335_B137_B151_registered_successor_pipeline',
    'scripts/build_registered_maria337_v1.py':'scripts/build_registered_maria335_B137_B151_v1.py',
    "result['batches'][:716] == old_manifest['batches'] and len(result['batches']) == 717":
        "result['batches'][:717] == old_manifest['batches'] and len(result['batches']) == 718",
    "len(result['checks']) == 52":"len(result['checks']) == 53",
    "'complete_stack_entries': 717, 'registered_manifest_entries': 717, 'passing_release_checks': 52":
        "'complete_stack_entries': 718, 'registered_manifest_entries': 718, 'passing_release_checks': 53",
    "'new_contextual_records': 337, 'prose_revisions': 224":"'new_contextual_records': 335, 'prose_revisions': 185",
    "'justified_retentions': 113,'physical_body_candidates':335,'native_FE_panels':6":
        "'justified_retentions': 150,'physical_body_candidates':333,'native_FE_panels':18",
    'Registered Maria337 with717 entries and52 release checks.':'Registered Maria335 B137-B151 with718 entries and53 release checks.',
})
env={**template.env,**globals(),'previous':predecessor,'__file__':__file__}
exec(compile(stage_source+'\n'+register_source,__file__+'::same-cumulative-stage-register-preserved-prefix-andruntime','exec'),env)
if __name__=='__main__':
    if sys.argv[1:]==['--register']:env['register']()
    else:assert not sys.argv[1:];env['stage']()
