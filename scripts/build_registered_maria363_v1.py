"""Preserve721 registered entries and append363 complete reviewed objects once."""
from pathlib import Path
from types import SimpleNamespace
import sys
from scripts import build_registered_maria321_v1 as template
from scripts.prepare_maria363_registered_v1 import ARCHIVE,ARM,CLEAN,CONFIG,PARENT,QUALIFICATION,REGISTRY,FINAL,ROOT
from dk4tool.patch.maria363_release_v1 import plan_release
from scripts.source_locked_derivation_v5118 import checked_text

STORED = ROOT/'stored_v1/stored_native_verification.json'
OUT = Path('work/maria363_B216_B252_release_v1')
PROFILE = 'all-routes-maria363-b216-b252-dialogue-v1-20261110'
CANDIDATE = OUT/'all_routes_maria363_B216_B252_candidate.nds'
MANIFEST = CANDIDATE.with_suffix('.manifest.json'); PATCH = CANDIDATE.with_suffix('.xdelta')
INVERSE_PATCH = OUT/'clean_input_reconstruction_RESEARCH_ONLY.nds'
STAGED = OUT/'staged_successor.json'; RELEASE = OUT/'registered_release_verification.json'
STARTUP = OUT/'own_registered_startup_verification.json'; GETTERS = OUT/'own_registered_name_getters_v1.json'
PARENT_REGISTRY = OUT/'release_stack_before_Maria363.json'
CHECK_SC1 = 'registered_Maria363_B216_B252_dialogue_and_complete_parent_target_inverse'
NEGATIVES = ROOT/'registered_semantic_checks_v1/qualification.json'
SOURCE25_SPEC = template.SOURCE25_SPEC
predecessor = SimpleNamespace(CHECK_SC1=template.CHECK_SC1)

stage_source = checked_text(template.stage_source, {
    "len(old_manifest['batches']) == 720 and len(old_manifest['checks']) == 55":"len(old_manifest['batches']) == 721 and len(old_manifest['checks']) == 56",
    "len(dialogue_proof['changed_records']) == 321":"len(dialogue_proof['changed_records']) == 363",
    'Staged Maria321 B196-B215.':'Staged Maria363 B216-B252.',
})
register_source = checked_text(template.register_source, {
    "r['id']) for r in bindings}) == 321":"r['id']) for r in bindings}) == 363",
    "sum(len(r['registered_native_pages']) for r in bindings)==321":"sum(len(r['registered_native_pages']) for r in bindings)==363",
    'verified_Maria305_B176_B195_output_reused':'verified_Maria321_B196_B215_output_reused',
    'verified_Maria305_B176_B195_predecessor':'verified_Maria321_B196_B215_predecessor',
    'maria321_B196_B215_late_dialogue':'maria363_B216_B252_late_dialogue',
    'Maria B196–B215 contextual letters, training andtown quests, source-faithful instructions, readable wrapping, complete menus andscoped names':'Maria B216–B252 contextual town andguild quests, forest exchanges, complete riddle instructions, readable wrapping, menus andscoped names',
    'release_stack.Maria321_B196_B215.pending.json':'release_stack.Maria363_B216_B252.pending.json',
    'late_editorial:maria321_B196_B215':'late_editorial:maria363_B216_B252',
    'Maria321_B196_B215_registered_successor_pipeline':'Maria363_B216_B252_registered_successor_pipeline',
    'scripts/build_registered_maria321_v1.py':'scripts/build_registered_maria363_v1.py',
    "result['batches'][:720] == old_manifest['batches'] and len(result['batches']) == 721":"result['batches'][:721] == old_manifest['batches'] and len(result['batches']) == 722",
    "len(result['checks']) == 56":"len(result['checks']) == 57",
    "'complete_stack_entries': 721, 'registered_manifest_entries': 721, 'passing_release_checks': 56":"'complete_stack_entries': 722, 'registered_manifest_entries': 722, 'passing_release_checks': 57",
    "'new_contextual_records': 321, 'prose_revisions': 171":"'new_contextual_records': 363, 'prose_revisions': 202",
    "'justified_retentions': 150,'physical_body_candidates':317,'native_FE_panels':2":"'justified_retentions': 161,'physical_body_candidates':351,'native_FE_panels':38",
    'Registered Maria321 B196-B215 with721 entries and56 release checks.':'Registered Maria363 B216-B252 with722 entries and57 release checks.',
})
env = {**template.env, **globals(), 'previous':predecessor, '__file__':__file__}
exec(compile(stage_source+'\n'+register_source,__file__+'::same-complete-cumulative-prefix-runtime-andmixed-guards','exec'),env)

if __name__ == '__main__':
    if sys.argv[1:] == ['--register']: env['register']()
    else:
        assert not sys.argv[1:]
        env['stage']()
