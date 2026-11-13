"""Stage/register the400-record append, preserving the complete cumulative prefix and main."""
from pathlib import Path
import sys
from scripts import build_registered_hodram_B301_B310_v1 as previous
from scripts.finalize_hodram_B311_B324_research_v1 import FINAL, STORED
from scripts.prepare_hodram_B311_B324_registered_v1 import ARCHIVE, ARM, CLEAN, CONFIG, PARENT, QUALIFICATION, REGISTRY
from dk4tool.patch.hodram_b311_b324_release_v1 import plan_release
from scripts.source_locked_derivation_v5118 import checked_text

OUT = Path('work/hodram_B311_B324_release_v1')
PROFILE = 'all-routes-hodram-b311-b324-dialogue-v1-20261107'
CANDIDATE = OUT/'all_routes_hodram_B311_B324_candidate.nds'
MANIFEST = CANDIDATE.with_suffix('.manifest.json')
PATCH = CANDIDATE.with_suffix('.xdelta')
INVERSE_PATCH = OUT/'clean_input_reconstruction_RESEARCH_ONLY.nds'
STAGED = OUT/'staged_successor.json'
RELEASE = OUT/'registered_release_verification.json'
STARTUP = OUT/'own_registered_startup_verification.json'
GETTERS = OUT/'own_registered_name_getters_v1.json'
PARENT_REGISTRY = OUT/'release_stack_before_Hodram_B311_B324.json'
CHECK_SC1 = 'registered_Hodram_B311_B324_dialogue_and_complete_parent_target_inverse'
NEGATIVES = Path('work/Hodram_B311_B324_clean_20261107/registered_semantic_checks_v1/qualification.json')

stage_source = checked_text(previous.stage_source, {
    "len(old_manifest['batches']) == 704 and len(old_manifest['checks']) == 39":
        "len(old_manifest['batches']) == 705 and len(old_manifest['checks']) == 40",
    "len(dialogue_proof['changed_records']) == 234": "len(dialogue_proof['changed_records']) == 400",
    'Staged Hodram B301-B310.': 'Staged Hodram B311-B324.',
})
register_source = checked_text(previous.register_source, {
    'verified_Hodram_B281_B300_output_reused=True': 'verified_Hodram_B301_B310_output_reused=True',
    "r['id']) for r in bindings}) == 234": "r['id']) for r in bindings}) == 400",
    'verified_hodram_b281_b300_predecessor': 'verified_hodram_b301_b310_predecessor',
    'hodram_B301_B310_late_dialogue': 'hodram_B311_B324_late_dialogue',
    'Hodram B301–B310 dialogue.': 'Hodram B311–B324 dialogue.',
    'release_stack.Hodram_B301_B310.pending.json': 'release_stack.Hodram_B311_B324.pending.json',
    'late_editorial:hodram-b301-b310': 'late_editorial:hodram-b311-b324',
    'Hodram_B301_B310_registered_successor_pipeline': 'Hodram_B311_B324_registered_successor_pipeline',
    "result['batches'][:704] == old_manifest['batches'] and len(result['batches']) == 705":
        "result['batches'][:705] == old_manifest['batches'] and len(result['batches']) == 706",
    "len(result['checks']) == 40": "len(result['checks']) == 41",
    "'complete_stack_entries': 705, 'registered_manifest_entries': 705, 'passing_release_checks': 40":
        "'complete_stack_entries': 706, 'registered_manifest_entries': 706, 'passing_release_checks': 41",
    "'new_contextual_records': 234, 'prose_revisions': 127": "'new_contextual_records': 400, 'prose_revisions': 175",
    "'justified_retentions': 107": "'justified_retentions': 225",
    'Registered Hodram B301-B310 with705 entries and40 release checks.':
        'Registered Hodram B311-B324 with706 entries and41 release checks.',
})
env = {**previous.env, **vars(previous), **globals(), 'previous':previous, '__file__':__file__}
exec(compile(stage_source+'\n'+register_source,__file__+'::same-complete-cumulative-registered-successor-contract-new-scope','exec'),env)
if __name__ == '__main__':
    if sys.argv[1:] == ['--register']:
        env['register']()
    else:
        assert not sys.argv[1:]
        env['stage']()
