"""Preserve the718-entry prefix and append390 reviewed source objects once."""
from pathlib import Path
from types import SimpleNamespace
import sys
from scripts import build_registered_maria335_B137_B151_v1 as template
from scripts.prepare_maria390_registered_v1 import ARCHIVE,ARM,CLEAN,CONFIG,PARENT,QUALIFICATION,REGISTRY,FINAL,ROOT
from dk4tool.patch.maria390_release_v1 import plan_release
from scripts.source_locked_derivation_v5118 import checked_text

STORED=ROOT/'stored_v3/stored_native_verification.json'
OUT=Path('work/maria390_B152_B175_release_v1')
PROFILE='all-routes-maria390-b152-b175-dialogue-v1-20261110'
CANDIDATE=OUT/'all_routes_maria390_B152_B175_candidate.nds'
MANIFEST=CANDIDATE.with_suffix('.manifest.json');PATCH=CANDIDATE.with_suffix('.xdelta')
INVERSE_PATCH=OUT/'clean_input_reconstruction_RESEARCH_ONLY.nds'
STAGED=OUT/'staged_successor.json';RELEASE=OUT/'registered_release_verification.json'
STARTUP=OUT/'own_registered_startup_verification.json';GETTERS=OUT/'own_registered_name_getters_v1.json'
PARENT_REGISTRY=OUT/'release_stack_before_Maria390.json'
CHECK_SC1='registered_Maria390_B152_B175_dialogue_and_complete_parent_target_inverse'
NEGATIVES=ROOT/'registered_semantic_checks_v1/qualification.json'
SOURCE25_SPEC=template.SOURCE25_SPEC
predecessor=SimpleNamespace(CHECK_SC1=template.CHECK_SC1)

stage_source=checked_text(template.stage_source,{
    "len(old_manifest['batches']) == 717 and len(old_manifest['checks']) == 52":
        "len(old_manifest['batches']) == 718 and len(old_manifest['checks']) == 53",
    "len(dialogue_proof['changed_records']) == 335":"len(dialogue_proof['changed_records']) == 390",
    'Staged Maria335 B137-B151.':'Staged Maria390 B152-B175.',
})
register_source=checked_text(template.register_source,{
    "r['id']) for r in bindings}) == 335":"r['id']) for r in bindings}) == 390",
    "sum(len(r['registered_native_pages']) for r in bindings)==335":"sum(len(r['registered_native_pages']) for r in bindings)==390",
    'verified_Maria337_output_reused':'verified_Maria335_B137_B151_output_reused',
    'verified_Maria337_predecessor':'verified_Maria335_B137_B151_predecessor',
    'maria335_B137_B151_late_dialogue':'maria390_B152_B175_late_dialogue',
    'Maria B137–B151 contextual dialogue, tutorial and glyph repairs, scoped FE guards and complete captions':
        'Maria B152–B175 contextual town/random dialogue, whole-exchange reply, readable wrapping, menu andowned FE padding repairs',
    'release_stack.Maria335_B137_B151.pending.json':'release_stack.Maria390_B152_B175.pending.json',
    'late_editorial:maria335_B137_B151':'late_editorial:maria390_B152_B175',
    'Maria335_B137_B151_registered_successor_pipeline':'Maria390_B152_B175_registered_successor_pipeline',
    'scripts/build_registered_maria335_B137_B151_v1.py':'scripts/build_registered_maria390_v1.py',
    "result['batches'][:717] == old_manifest['batches'] and len(result['batches']) == 718":
        "result['batches'][:718] == old_manifest['batches'] and len(result['batches']) == 719",
    "len(result['checks']) == 53":"len(result['checks']) == 54",
    "'complete_stack_entries': 718, 'registered_manifest_entries': 718, 'passing_release_checks': 53":
        "'complete_stack_entries': 719, 'registered_manifest_entries': 719, 'passing_release_checks': 54",
    "'new_contextual_records': 335, 'prose_revisions': 185":"'new_contextual_records': 390, 'prose_revisions': 154",
    "'justified_retentions': 150,'physical_body_candidates':333,'native_FE_panels':18":
        "'justified_retentions': 236,'physical_body_candidates':373,'native_FE_panels':32",
    'Registered Maria335 B137-B151 with718 entries and53 release checks.':'Registered Maria390 B152-B175 with719 entries and54 release checks.',
})
env={**template.env,**globals(),'previous':predecessor,'__file__':__file__}
exec(compile(stage_source+'\n'+register_source,__file__+'::same-cumulative-stage-register-prefix-runtime-andsource25-guards','exec'),env)
if __name__=='__main__':
    if sys.argv[1:]==['--register']:env['register']()
    else:assert not sys.argv[1:];env['stage']()
