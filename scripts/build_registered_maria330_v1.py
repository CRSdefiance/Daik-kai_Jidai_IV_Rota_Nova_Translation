"""Preserve the full715-entry prefix and add330 once-only source bindings."""
from pathlib import Path
from types import SimpleNamespace
import sys
from scripts import build_registered_maria328_v2 as template
from scripts import register_maria328_v1 as registration
from scripts.prepare_maria330_registered_v1 import ARCHIVE,ARM,CLEAN,CONFIG,PARENT,QUALIFICATION,REGISTRY,FINAL,ROOT
from dk4tool.patch.maria330_release_v1 import plan_release
from scripts.source_locked_derivation_v5118 import checked_text

STORED=ROOT/'stored_v1/stored_native_verification.json'
OUT=Path('work/maria330_release_v1')
PROFILE='all-routes-maria330-dialogue-v1-20261109'
CANDIDATE=OUT/'all_routes_maria330_candidate.nds'
MANIFEST=CANDIDATE.with_suffix('.manifest.json'); PATCH=CANDIDATE.with_suffix('.xdelta')
INVERSE_PATCH=OUT/'clean_input_reconstruction_RESEARCH_ONLY.nds'
STAGED=OUT/'staged_successor.json'; RELEASE=OUT/'registered_release_verification.json'
STARTUP=OUT/'own_registered_startup_verification.json'; GETTERS=OUT/'own_registered_name_getters_v1.json'
PARENT_REGISTRY=OUT/'release_stack_before_Maria330.json'
CHECK_SC1='registered_Maria330_dialogue_and_complete_parent_target_inverse'
NEGATIVES=ROOT/'registered_semantic_checks_v1/qualification.json'
SOURCE25_SPEC=template.SOURCE25_SPEC
predecessor=SimpleNamespace(CHECK_SC1=template.CHECK_SC1)

stage_source=checked_text(template.stage_source,{
    'prior303.FINAL':'template.FINAL','prior303.CHECK_SC1':'template.CHECK_SC1',
    "len(old_manifest['batches']) == 714 and len(old_manifest['checks']) == 49":"len(old_manifest['batches']) == 715 and len(old_manifest['checks']) == 50",
    "len(dialogue_proof['changed_records']) == 328":"len(dialogue_proof['changed_records']) == 330",
    'Staged Maria328.':'Staged Maria330.',
})
register_source=checked_text(registration.source,{
    "row['id']=='DK4_MES_B87_R0139'":"row['id'] in {'DK4_MES_B116_R0041','DK4_MES_B116_R0051'}",
    "r['id']) for r in bindings}) == 328":"r['id']) for r in bindings}) == 330",
    "sum(len(r['registered_native_pages']) for r in bindings)==329":"sum(len(r['registered_native_pages']) for r in bindings)==332",
    'verified_Maria303_output_reused':'verified_Maria328_output_reused',
    'verified_Maria303_predecessor':'verified_Maria328_predecessor','maria328_late_dialogue':'maria330_late_dialogue',
    'Maria B73–B95 contextual dialogue, menus, styles andsource-owned FE pagination':'Maria B96–B124 contextual dialogue, menu, styles andtwo source-owned FE continuations',
    'release_stack.Maria328.pending.json':'release_stack.Maria330.pending.json',
    'late_editorial:maria328':'late_editorial:maria330','Maria328_registered_successor_pipeline':'Maria330_registered_successor_pipeline',
    'scripts/build_registered_maria328_v2.py':'scripts/build_registered_maria330_v1.py',
    "result['batches'][:714] == old_manifest['batches'] and len(result['batches']) == 715":"result['batches'][:715] == old_manifest['batches'] and len(result['batches']) == 716",
    "len(result['checks']) == 50":"len(result['checks']) == 51",
    "'complete_stack_entries': 715, 'registered_manifest_entries': 715, 'passing_release_checks': 50":"'complete_stack_entries': 716, 'registered_manifest_entries': 716, 'passing_release_checks': 51",
    "'new_contextual_records': 328, 'prose_revisions': 143":"'new_contextual_records': 330, 'prose_revisions': 249",
    "'justified_retentions': 185,'physical_body_candidates':314,'native_FE_panels':28,'additional_exact_source_FE_controls':1":"'justified_retentions': 81,'physical_body_candidates':330,'native_FE_panels':10,'additional_exact_source_FE_controls':2",
    'Registered Maria328 with715 entries and50 release checks.':'Registered Maria330 with716 entries and51 release checks.',
})
env={**template.env,**globals(),'previous':predecessor,'__file__':__file__}
exec(compile(stage_source+'\n'+register_source,__file__+'::same-complete-cumulative-stage-andregister-with-two-owner-reference-bindings','exec'),env)

if __name__=='__main__':
    if sys.argv[1:]==['--register']:env['register']()
    else:assert not sys.argv[1:];env['stage']()
