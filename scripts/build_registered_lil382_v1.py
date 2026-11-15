"""Append the qualified Lil382 transaction to the exact cumulative registered prefix."""
from pathlib import Path
from types import SimpleNamespace
import sys
from scripts import build_registered_maria315_v1 as template
from scripts.prepare_lil382_registered_v1 import ARCHIVE,ARM,CLEAN,CONFIG,PARENT,QUALIFICATION,REGISTRY,FINAL,ROOT
from dk4tool.patch.lil382_release_v1 import plan_release
from scripts.source_locked_derivation_v5118 import checked_text

STORED=ROOT/'stored_v1/stored_native_verification.json'
OUT=Path('work/lil382_residual_A_release_v1')
PROFILE='all-routes-lil382-residual-a-dialogue-v1-20261110'
CANDIDATE=OUT/'all_routes_lil382_residual_A_candidate.nds'
MANIFEST=CANDIDATE.with_suffix('.manifest.json');PATCH=CANDIDATE.with_suffix('.xdelta')
INVERSE_PATCH=OUT/'clean_input_reconstruction_RESEARCH_ONLY.nds'
STAGED=OUT/'staged_successor.json';RELEASE=OUT/'registered_release_verification.json'
STARTUP=OUT/'own_registered_startup_verification.json';GETTERS=OUT/'own_registered_name_getters_v1.json'
PARENT_REGISTRY=OUT/'release_stack_before_Lil382.json'
CHECK_SC1='registered_Lil382_residual_A_dialogue_and_complete_parent_target_inverse'
NEGATIVES=ROOT/'registered_semantic_checks_v1/qualification.json'
SOURCE25_SPEC=template.SOURCE25_SPEC
predecessor=SimpleNamespace(CHECK_SC1=template.template.CHECK_SC1)
stage_source=checked_text(template.stage_source, {
    "qualification['only_SC3_changes']": "qualification['only_SC2_changes']",
    "len(old_manifest['batches']) == 724 and len(old_manifest['checks']) == 59":
        "len(old_manifest['batches']) == 725 and len(old_manifest['checks']) == 60",
    "len(dialogue_proof['changed_records']) == 315": "len(dialogue_proof['changed_records']) == 382",
    'target_SC3_sha256': 'target_SC2_sha256',
    'only_owned_SC3_blocks_changed': 'only_owned_SC2_blocks_changed',
    'Staged Maria315 B286-B302.': 'Staged Lil382 residual A.',
    '# The final four-archive guard runs fresh because SC3 changed. Earlier':
        '# The final four-archive guard runs fresh because SC2 changed. Earlier',
})
register_source=checked_text(template.register_source, {
    'target_SC3_sha256': 'target_SC2_sha256',
    "r['id']) for r in bindings}) == 315": "r['id']) for r in bindings}) == 382",
    "sum(len(r['registered_native_pages']) for r in bindings)==315": "sum(len(r['registered_native_pages']) for r in bindings)==382",
    'verified_Maria349_B275_B285_output_reused': 'verified_Maria315_B286_B302_output_reused',
    'verified_Maria349_B275_B285_predecessor': 'verified_Maria315_B286_B302_predecessor',
    'maria315_B286_B302_late_dialogue': 'lil382_residual_A_late_dialogue',
    'Maria B286–B302 contextual incense, armor, fog/cave, ghost ship, guardian, Sextant andmonk/book exchanges, readable wrapping, glyphs, menus andscoped names':
        'Lil residual A contextual crew, Aziza, cross-story, letters, town and quest exchanges, readable wrapping, glyphs, menus and scoped names',
    'release_stack.Maria315_B286_B302.pending.json': 'release_stack.Lil382_residual_A.pending.json',
    'late_editorial:maria315_B286_B302': 'late_editorial:lil382_residual_A',
    'Maria315_B286_B302_registered_successor_pipeline': 'Lil382_residual_A_registered_successor_pipeline',
    'scripts/build_registered_maria315_v1.py': 'scripts/build_registered_lil382_v1.py',
    "result['batches'][:724] == old_manifest['batches'] and len(result['batches']) == 725":
        "result['batches'][:725] == old_manifest['batches'] and len(result['batches']) == 726",
    "len(result['checks']) == 60": "len(result['checks']) == 61",
    "'complete_stack_entries': 725, 'registered_manifest_entries': 725, 'passing_release_checks': 60":
        "'complete_stack_entries': 726, 'registered_manifest_entries': 726, 'passing_release_checks': 61",
    "'new_contextual_records': 315, 'prose_revisions': 162": "'new_contextual_records': 382, 'prose_revisions': 257",
    "'justified_retentions': 153,'physical_body_candidates':309,'native_FE_panels':13":
        "'justified_retentions': 125,'physical_body_candidates':378,'native_FE_panels':3",
    'Registered Maria315 B286-B302 with725 entries and60 release checks.': 'Registered Lil382 residual A with726 entries and61 release checks.',
})
env={**template.env,**globals(),'previous':predecessor,'__file__':__file__}
exec(compile(stage_source+'\n'+register_source,__file__+'::same-cumulative-prefix-runtime-source25-andmixed-guards','exec'),env)
if __name__=='__main__':
    if sys.argv[1:]==['--register']:env['register']()
    else:
        assert not sys.argv[1:];env['stage']()
