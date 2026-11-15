"""Stage/register the301-record SC3 append over the verified708-entry cumulative prefix."""
from pathlib import Path
import sys
from scripts import build_registered_hodram_B311_B324_v1 as template
from scripts import build_registered_hodram_residual_v1 as predecessor
from scripts.prepare_maria301_registered_v2 import ARCHIVE,ARM,CLEAN,CONFIG,PARENT,QUALIFICATION,REGISTRY,FINAL,ROOT
from dk4tool.patch.maria301_release_v2 import plan_release
from scripts.source_locked_derivation_v5118 import checked_text

STORED = ROOT/'stored_v1/stored_native_verification.json'
OUT = Path('work/maria301_release_v1')
PROFILE = 'all-routes-maria301-dialogue-v1-20261109'
CANDIDATE = OUT/'all_routes_maria301_candidate.nds'
MANIFEST = CANDIDATE.with_suffix('.manifest.json');PATCH = CANDIDATE.with_suffix('.xdelta')
INVERSE_PATCH = OUT/'clean_input_reconstruction_RESEARCH_ONLY.nds'
STAGED = OUT/'staged_successor.json';RELEASE = OUT/'registered_release_verification.json'
STARTUP = OUT/'own_registered_startup_verification.json';GETTERS = OUT/'own_registered_name_getters_v1.json'
PARENT_REGISTRY = OUT/'release_stack_before_Maria301.json'
CHECK_SC1 = 'registered_Maria301_dialogue_and_complete_parent_target_inverse'
NEGATIVES = ROOT/'registered_semantic_checks_v1/qualification.json'

stage_source = checked_text(template.stage_source, {
    "qualification['only_SC1_changes']": "qualification['only_SC3_changes']",
    "assert Path(old_manifest['batches'][-1])==previous.FINAL":
        "assert Path(old_manifest['batches'][-2])==previous.FINAL\n    assert Path(old_manifest['batches'][-1])==previous.NAME_CONFIG\n    assert release['owned_Hodram_residual_surnames_verified']",
    "len(old_manifest['batches']) == 705 and len(old_manifest['checks']) == 40":
        "len(old_manifest['batches']) == 708 and len(old_manifest['checks']) == 43",
    "len(dialogue_proof['changed_records']) == 400": "len(dialogue_proof['changed_records']) == 301",
    'because SC1 changed': 'because SC3 changed',
    'target_SC1_sha256': 'target_SC3_sha256',
    'only_owned_SC1_blocks_changed': 'only_owned_SC3_blocks_changed',
    'Staged Hodram B311-B324.': 'Staged Maria301.',
})
register_source = checked_text(template.register_source, {
    'both_name_getters_exact_for_all9_protected_actors': 'both_name_getters_exact_for_all12_protected_actors',
    "startup['frames'] == 4001 and startup['ordinary_title_NewGame_Rafael_Castor_andopening_observed']":
        "startup['frames'] == 31000 and startup['ordinary_title_NewGame_Maria_opening_andHangzhou_observed']",
    'verified_Hodram_B301_B310_output_reused=True': 'verified_Hodram_residual_output_reused=True',
    'target_SC1_sha256': 'target_SC3_sha256',
    "r['id']) for r in bindings}) == 400": "r['id']) for r in bindings}) == 301",
    'verified_hodram_b301_b310_predecessor': 'verified_hodram_residual_predecessor',
    'hodram_B311_B324_late_dialogue': 'maria301_late_dialogue',
    'Hodram B311–B324 dialogue.': 'Maria B0–B32 contextual dialogue and wrapping.',
    'release_stack.Hodram_B311_B324.pending.json': 'release_stack.Maria301.pending.json',
    'late_editorial:hodram-b311-b324': 'late_editorial:maria301',
    'Hodram_B311_B324_registered_successor_pipeline': 'Maria301_registered_successor_pipeline',
    "result['batches'][:705] == old_manifest['batches'] and len(result['batches']) == 706":
        "result['batches'][:708] == old_manifest['batches'] and len(result['batches']) == 709",
    "len(result['checks']) == 41": "len(result['checks']) == 44",
    "'complete_stack_entries': 706, 'registered_manifest_entries': 706, 'passing_release_checks': 41":
        "'complete_stack_entries': 709, 'registered_manifest_entries': 709, 'passing_release_checks': 44",
    "'changed_components': [], 'owned_Rafael_residual_middle_fields_verified': True, 'new_contextual_records': 400, 'prose_revisions': 175":
        "'changed_components': [], 'owned_Hodram_residual_surnames_verified':True,'owned_Rafael_residual_middle_fields_verified': True, 'new_contextual_records': 301, 'prose_revisions': 178",
    "'justified_retentions': 225": "'justified_retentions': 123",
    'Registered Hodram B311-B324 with706 entries and41 release checks.':
        'Registered Maria301 with709 entries and44 release checks.',
})
env = {**template.env,**vars(template),**globals(),'previous':predecessor,'__file__':__file__}
exec(compile(stage_source+'\n'+register_source,__file__+'::same-complete-cumulative-successor-contract-explicit-SC3','exec'),env)

if __name__ == '__main__':
    if sys.argv[1:] == ['--register']:env['register']()
    else:assert not sys.argv[1:];env['stage']()
