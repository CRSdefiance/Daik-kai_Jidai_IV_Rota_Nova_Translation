"""Preserve720 entries and append321 reviewed mixed source objects exactly once."""
from pathlib import Path
from types import SimpleNamespace
import sys
from scripts import build_registered_maria305_v1 as template
from scripts.prepare_maria321_registered_v2 import ARCHIVE,ARM,CLEAN,CONFIG,PARENT,QUALIFICATION,REGISTRY,FINAL,ROOT
from dk4tool.patch.maria321_release_v1 import plan_release
from scripts.source_locked_derivation_v5118 import checked_text

STORED = ROOT/'stored_v1/stored_native_verification.json'
OUT = Path('work/maria321_B196_B215_release_v1')
PROFILE = 'all-routes-maria321-b196-b215-dialogue-v1-20261110'
CANDIDATE = OUT/'all_routes_maria321_B196_B215_candidate.nds'
MANIFEST = CANDIDATE.with_suffix('.manifest.json'); PATCH = CANDIDATE.with_suffix('.xdelta')
INVERSE_PATCH = OUT/'clean_input_reconstruction_RESEARCH_ONLY.nds'
STAGED = OUT/'staged_successor.json'; RELEASE = OUT/'registered_release_verification.json'
STARTUP = OUT/'own_registered_startup_verification.json'; GETTERS = OUT/'own_registered_name_getters_v1.json'
PARENT_REGISTRY = OUT/'release_stack_before_Maria321.json'
CHECK_SC1 = 'registered_Maria321_B196_B215_dialogue_and_complete_parent_target_inverse'
NEGATIVES = ROOT/'registered_semantic_checks_v1/qualification.json'
SOURCE25_SPEC = template.SOURCE25_SPEC
predecessor = SimpleNamespace(CHECK_SC1=template.CHECK_SC1)

stage_source = checked_text(template.stage_source, {
    "len(old_manifest['batches']) == 719 and len(old_manifest['checks']) == 54":
        "len(old_manifest['batches']) == 720 and len(old_manifest['checks']) == 55",
    "len(dialogue_proof['changed_records']) == 305": "len(dialogue_proof['changed_records']) == 321",
    'Staged Maria305 B176-B195.': 'Staged Maria321 B196-B215.',
})
register_source = checked_text(template.register_source, {
    "r['id']) for r in bindings}) == 305": "r['id']) for r in bindings}) == 321",
    "sum(len(r['registered_native_pages']) for r in bindings)==305":
        "sum(len(r['registered_native_pages']) for r in bindings)==321",
    'verified_Maria390_B152_B175_output_reused': 'verified_Maria305_B176_B195_output_reused',
    'verified_Maria390_B152_B175_predecessor': 'verified_Maria305_B176_B195_predecessor',
    'maria305_B176_B195_late_dialogue': 'maria321_B196_B215_late_dialogue',
    'Maria B176–B195 contextual dialogue, letter voices andsignatures, readable wrapping, complete menus, glyph andFE row repairs':
        'Maria B196–B215 contextual letters, training andtown quests, source-faithful instructions, readable wrapping, complete menus andscoped names',
    'release_stack.Maria305_B176_B195.pending.json': 'release_stack.Maria321_B196_B215.pending.json',
    'late_editorial:maria305_B176_B195': 'late_editorial:maria321_B196_B215',
    'Maria305_B176_B195_registered_successor_pipeline': 'Maria321_B196_B215_registered_successor_pipeline',
    'scripts/build_registered_maria305_v1.py': 'scripts/build_registered_maria321_v1.py',
    "result['batches'][:719] == old_manifest['batches'] and len(result['batches']) == 720":
        "result['batches'][:720] == old_manifest['batches'] and len(result['batches']) == 721",
    "len(result['checks']) == 55": "len(result['checks']) == 56",
    "'complete_stack_entries': 720, 'registered_manifest_entries': 720, 'passing_release_checks': 55":
        "'complete_stack_entries': 721, 'registered_manifest_entries': 721, 'passing_release_checks': 56",
    "'new_contextual_records': 305, 'prose_revisions': 205":
        "'new_contextual_records': 321, 'prose_revisions': 171",
    "'justified_retentions': 100,'physical_body_candidates':294,'native_FE_panels':16":
        "'justified_retentions': 150,'physical_body_candidates':317,'native_FE_panels':2",
    'Registered Maria305 B176-B195 with720 entries and55 release checks.':
        'Registered Maria321 B196-B215 with721 entries and56 release checks.',
})
env = {**template.env, **globals(), 'previous':predecessor, '__file__':__file__}
exec(compile(stage_source+'\n'+register_source,__file__+'::same-cumulative-prefix-runtime-source25-andmixed-bindings','exec'),env)

if __name__ == '__main__':
    if sys.argv[1:] == ['--register']: env['register']()
    else:
        assert not sys.argv[1:]
        env['stage']()
