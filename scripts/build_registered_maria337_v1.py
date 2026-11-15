"""Preserve the complete716-entry prefix and append337 reviewed source objects."""
from pathlib import Path
from types import SimpleNamespace
import sys
from scripts import build_registered_maria330_v1 as template
from scripts.prepare_maria337_registered_v1 import ARCHIVE,ARM,CLEAN,CONFIG,PARENT,QUALIFICATION,REGISTRY,FINAL,ROOT
from dk4tool.patch.maria337_release_v1 import plan_release
from scripts.source_locked_derivation_v5118 import checked_text

STORED=ROOT/'stored_v1/stored_native_verification.json'
OUT=Path('work/maria337_release_v1')
PROFILE='all-routes-maria337-dialogue-v1-20261109'
CANDIDATE=OUT/'all_routes_maria337_candidate.nds'
MANIFEST=CANDIDATE.with_suffix('.manifest.json');PATCH=CANDIDATE.with_suffix('.xdelta')
INVERSE_PATCH=OUT/'clean_input_reconstruction_RESEARCH_ONLY.nds'
STAGED=OUT/'staged_successor.json';RELEASE=OUT/'registered_release_verification.json'
STARTUP=OUT/'own_registered_startup_verification.json';GETTERS=OUT/'own_registered_name_getters_v1.json'
PARENT_REGISTRY=OUT/'release_stack_before_Maria337.json'
CHECK_SC1='registered_Maria337_dialogue_and_complete_parent_target_inverse'
NEGATIVES=ROOT/'registered_semantic_checks_v1/qualification.json'
SOURCE25_SPEC=template.SOURCE25_SPEC
predecessor=SimpleNamespace(CHECK_SC1=template.CHECK_SC1)

stage_source=checked_text(template.stage_source,{
    "len(old_manifest['batches']) == 715 and len(old_manifest['checks']) == 50":"len(old_manifest['batches']) == 716 and len(old_manifest['checks']) == 51",
    "len(dialogue_proof['changed_records']) == 330":"len(dialogue_proof['changed_records']) == 337",
    'Staged Maria330.':'Staged Maria337.',
})
register_source=checked_text(template.register_source,{
    "row['id'] in {'DK4_MES_B116_R0041','DK4_MES_B116_R0051'}":"False",
    "r['id']) for r in bindings}) == 330":"r['id']) for r in bindings}) == 337",
    "sum(len(r['registered_native_pages']) for r in bindings)==332":"sum(len(r['registered_native_pages']) for r in bindings)==337",
    'verified_Maria328_output_reused':'verified_Maria330_output_reused',
    'verified_Maria328_predecessor':'verified_Maria330_predecessor','maria330_late_dialogue':'maria337_late_dialogue',
    'Maria B96–B124 contextual dialogue, menu, styles andtwo source-owned FE continuations':'Maria B125–B136 contextual dialogue, tutorial wrapping and repaired choice captions',
    'release_stack.Maria330.pending.json':'release_stack.Maria337.pending.json',
    'late_editorial:maria330':'late_editorial:maria337','Maria330_registered_successor_pipeline':'Maria337_registered_successor_pipeline',
    'scripts/build_registered_maria330_v1.py':'scripts/build_registered_maria337_v1.py',
    "result['batches'][:715] == old_manifest['batches'] and len(result['batches']) == 716":"result['batches'][:716] == old_manifest['batches'] and len(result['batches']) == 717",
    "len(result['checks']) == 51":"len(result['checks']) == 52",
    "'complete_stack_entries': 716, 'registered_manifest_entries': 716, 'passing_release_checks': 51":"'complete_stack_entries': 717, 'registered_manifest_entries': 717, 'passing_release_checks': 52",
    "'new_contextual_records': 330, 'prose_revisions': 249":"'new_contextual_records': 337, 'prose_revisions': 224",
    "'justified_retentions': 81,'physical_body_candidates':330,'native_FE_panels':10,'additional_exact_source_FE_controls':2":"'justified_retentions': 113,'physical_body_candidates':335,'native_FE_panels':6,'additional_exact_source_FE_controls':0",
    'Registered Maria330 with716 entries and51 release checks.':'Registered Maria337 with717 entries and52 release checks.',
})
env={**template.env,**globals(),'previous':predecessor,'__file__':__file__}
exec(compile(stage_source+'\n'+register_source,__file__+'::same-complete-cumulative-stage-register-with-no-new-FE-owners','exec'),env)

if __name__=='__main__':
    if sys.argv[1:]==['--register']:env['register']()
    else:assert not sys.argv[1:];env['stage']()
