"""Append Maria359 to the complete722-entry prefix; require own startup before registration."""
from pathlib import Path
from types import SimpleNamespace
import sys
from scripts import build_registered_maria363_v1 as template
from scripts.prepare_maria359_registered_v1 import ARCHIVE,ARM,CLEAN,CONFIG,PARENT,QUALIFICATION,REGISTRY,FINAL,ROOT
from dk4tool.patch.maria359_release_v1 import plan_release
from scripts.source_locked_derivation_v5118 import checked_text

STORED=ROOT/'stored_v1/stored_native_verification.json'
OUT=Path('work/maria359_B253_B274_release_v1')
PROFILE='all-routes-maria359-b253-b274-dialogue-v1-20261110'
CANDIDATE=OUT/'all_routes_maria359_B253_B274_candidate.nds'
MANIFEST=CANDIDATE.with_suffix('.manifest.json');PATCH=CANDIDATE.with_suffix('.xdelta')
INVERSE_PATCH=OUT/'clean_input_reconstruction_RESEARCH_ONLY.nds'
STAGED=OUT/'staged_successor.json';RELEASE=OUT/'registered_release_verification.json'
STARTUP=OUT/'own_registered_startup_verification.json';GETTERS=OUT/'own_registered_name_getters_v1.json'
PARENT_REGISTRY=OUT/'release_stack_before_Maria359.json'
CHECK_SC1='registered_Maria359_B253_B274_dialogue_and_complete_parent_target_inverse'
NEGATIVES=ROOT/'registered_semantic_checks_v1/qualification.json'
SOURCE25_SPEC=template.SOURCE25_SPEC
predecessor=SimpleNamespace(CHECK_SC1=template.CHECK_SC1)

stage_source=checked_text(template.stage_source,{
    "len(old_manifest['batches']) == 721 and len(old_manifest['checks']) == 56":"len(old_manifest['batches']) == 722 and len(old_manifest['checks']) == 57",
    "len(dialogue_proof['changed_records']) == 363":"len(dialogue_proof['changed_records']) == 359",
    'Staged Maria363 B216-B252.':'Staged Maria359 B253-B274.',
})
register_source=checked_text(template.register_source,{
    "r['id']) for r in bindings}) == 363":"r['id']) for r in bindings}) == 359",
    "sum(len(r['registered_native_pages']) for r in bindings)==363":"sum(len(r['registered_native_pages']) for r in bindings)==359",
    'verified_Maria321_B196_B215_output_reused':'verified_Maria363_B216_B252_output_reused',
    'verified_Maria321_B196_B215_predecessor':'verified_Maria363_B216_B252_predecessor',
    'maria363_B216_B252_late_dialogue':'maria359_B253_B274_late_dialogue',
    'Maria B216–B252 contextual town andguild quests, forest exchanges, complete riddle instructions, readable wrapping, menus andscoped names':
        'Maria B253–B274 contextual town quests, scurvy medicine, jungle andforest exchanges, carronade research, readable wrapping, menus andscoped names',
    'release_stack.Maria363_B216_B252.pending.json':'release_stack.Maria359_B253_B274.pending.json',
    'late_editorial:maria363_B216_B252':'late_editorial:maria359_B253_B274',
    'Maria363_B216_B252_registered_successor_pipeline':'Maria359_B253_B274_registered_successor_pipeline',
    'scripts/build_registered_maria363_v1.py':'scripts/build_registered_maria359_v1.py',
    "result['batches'][:721] == old_manifest['batches'] and len(result['batches']) == 722":"result['batches'][:722] == old_manifest['batches'] and len(result['batches']) == 723",
    "len(result['checks']) == 57":"len(result['checks']) == 58",
    "'complete_stack_entries': 722, 'registered_manifest_entries': 722, 'passing_release_checks': 57":"'complete_stack_entries': 723, 'registered_manifest_entries': 723, 'passing_release_checks': 58",
    "'new_contextual_records': 363, 'prose_revisions': 202":"'new_contextual_records': 359, 'prose_revisions': 219",
    "'justified_retentions': 161,'physical_body_candidates':351,'native_FE_panels':38":"'justified_retentions': 140,'physical_body_candidates':349,'native_FE_panels':17",
    'Registered Maria363 B216-B252 with722 entries and57 release checks.':'Registered Maria359 B253-B274 with723 entries and58 release checks.',
})
env={**template.env,**globals(),'previous':predecessor,'__file__':__file__}
exec(compile(stage_source+'\n'+register_source,__file__+'::same-complete-cumulative-prefix-runtime-source25-andmixed-guards','exec'),env)

if __name__=='__main__':
    if sys.argv[1:]==['--register']:env['register']()
    else:
        assert not sys.argv[1:];env['stage']()
