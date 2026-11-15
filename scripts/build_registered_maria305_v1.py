"""Preserve719 entries and append305 reviewed mixed source objects exactly once."""
from pathlib import Path
from types import SimpleNamespace
import sys
from scripts import build_registered_maria390_v1 as template
from scripts.prepare_maria305_registered_v2 import ARCHIVE,ARM,CLEAN,CONFIG,PARENT,QUALIFICATION,REGISTRY,FINAL,ROOT
from dk4tool.patch.maria305_release_v2 import plan_release
from scripts.source_locked_derivation_v5118 import checked_text

STORED=ROOT/'stored_v1/stored_native_verification.json'
OUT=Path('work/maria305_B176_B195_release_v1')
PROFILE='all-routes-maria305-b176-b195-dialogue-v1-20261110'
CANDIDATE=OUT/'all_routes_maria305_B176_B195_candidate.nds'
MANIFEST=CANDIDATE.with_suffix('.manifest.json');PATCH=CANDIDATE.with_suffix('.xdelta')
INVERSE_PATCH=OUT/'clean_input_reconstruction_RESEARCH_ONLY.nds'
STAGED=OUT/'staged_successor.json';RELEASE=OUT/'registered_release_verification.json'
STARTUP=OUT/'own_registered_startup_verification.json';GETTERS=OUT/'own_registered_name_getters_v1.json'
PARENT_REGISTRY=OUT/'release_stack_before_Maria305.json'
CHECK_SC1='registered_Maria305_B176_B195_dialogue_and_complete_parent_target_inverse'
NEGATIVES=ROOT/'registered_semantic_checks_v1/qualification.json'
SOURCE25_SPEC=template.SOURCE25_SPEC
predecessor=SimpleNamespace(CHECK_SC1=template.CHECK_SC1)

stage_source=checked_text(template.stage_source,{
    "len(old_manifest['batches']) == 718 and len(old_manifest['checks']) == 53":
        "len(old_manifest['batches']) == 719 and len(old_manifest['checks']) == 54",
    "len(dialogue_proof['changed_records']) == 390":"len(dialogue_proof['changed_records']) == 305",
    'Staged Maria390 B152-B175.':'Staged Maria305 B176-B195.',
})
register_source=checked_text(template.register_source,{
    "r['id']) for r in bindings}) == 390":"r['id']) for r in bindings}) == 305",
    "sum(len(r['registered_native_pages']) for r in bindings)==390":"sum(len(r['registered_native_pages']) for r in bindings)==305",
    'verified_Maria335_B137_B151_output_reused':'verified_Maria390_B152_B175_output_reused',
    'verified_Maria335_B137_B151_predecessor':'verified_Maria390_B152_B175_predecessor',
    'maria390_B152_B175_late_dialogue':'maria305_B176_B195_late_dialogue',
    'Maria B152–B175 contextual town/random dialogue, whole-exchange reply, readable wrapping, menu andowned FE padding repairs':
        'Maria B176–B195 contextual dialogue, letter voices andsignatures, readable wrapping, complete menus, glyph andFE row repairs',
    'release_stack.Maria390_B152_B175.pending.json':'release_stack.Maria305_B176_B195.pending.json',
    'late_editorial:maria390_B152_B175':'late_editorial:maria305_B176_B195',
    'Maria390_B152_B175_registered_successor_pipeline':'Maria305_B176_B195_registered_successor_pipeline',
    'scripts/build_registered_maria390_v1.py':'scripts/build_registered_maria305_v1.py',
    "result['batches'][:718] == old_manifest['batches'] and len(result['batches']) == 719":
        "result['batches'][:719] == old_manifest['batches'] and len(result['batches']) == 720",
    "len(result['checks']) == 54":"len(result['checks']) == 55",
    "'complete_stack_entries': 719, 'registered_manifest_entries': 719, 'passing_release_checks': 54":
        "'complete_stack_entries': 720, 'registered_manifest_entries': 720, 'passing_release_checks': 55",
    "'new_contextual_records': 390, 'prose_revisions': 154":"'new_contextual_records': 305, 'prose_revisions': 205",
    "'justified_retentions': 236,'physical_body_candidates':373,'native_FE_panels':32":
        "'justified_retentions': 100,'physical_body_candidates':294,'native_FE_panels':16",
    'Registered Maria390 B152-B175 with719 entries and54 release checks.':'Registered Maria305 B176-B195 with720 entries and55 release checks.',
})
env={**template.env,**globals(),'previous':predecessor,'__file__':__file__}
exec(compile(stage_source+'\n'+register_source,__file__+'::same-cumulative-prefix-runtime-source25-andmixed-bindings','exec'),env)
if __name__=='__main__':
    if sys.argv[1:]==['--register']:env['register']()
    else:assert not sys.argv[1:];env['stage']()
