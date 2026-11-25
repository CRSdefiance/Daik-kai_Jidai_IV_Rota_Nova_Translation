"""Stage and register the full-stack SC1 successor without promoting main."""
from pathlib import Path
import sys
from scripts import build_registered_hodram_B211_B230_v1 as previous
from scripts.finalize_hodram_B231_B250_research_v1 import FINAL,STORED
from scripts.prepare_hodram_B231_B250_registered_v1 import ARCHIVE,ARM,CLEAN,CONFIG,PARENT,QUALIFICATION,REGISTRY
from dk4tool.patch.hodram_b231_b250_release_v1 import plan_release
from scripts.source_locked_derivation_v5118 import checked_text

OUT=Path('work/hodram_B231_B250_release_v1');PROFILE='all-routes-hodram-b231-b250-dialogue-v1-20261107'
CANDIDATE=OUT/'all_routes_hodram_B231_B250_candidate.nds';MANIFEST=CANDIDATE.with_suffix('.manifest.json');PATCH=CANDIDATE.with_suffix('.xdelta')
INVERSE_PATCH=OUT/'clean_input_reconstruction_RESEARCH_ONLY.nds';STAGED=OUT/'staged_successor.json';RELEASE=OUT/'registered_release_verification.json'
STARTUP=OUT/'own_registered_startup_verification.json';GETTERS=OUT/'own_registered_name_getters_v1.json'
PARENT_REGISTRY=OUT/'release_stack_before_Hodram_B231_B250.json'
CHECK_SC1='registered_Hodram_B231_B250_dialogue_and_complete_parent_target_inverse'
NEGATIVES=Path('work/Hodram_B231_B250_clean_20261107/registered_semantic_checks_v1/qualification.json')

stage_source=checked_text(previous.stage_source,{
    "    assert [Path(p) for p in old_manifest['batches'][-2:]]==[previous.FINAL,previous.NAME_CONFIG]\n    assert old_manifest['checks'][previous.CHECK_SC0] and old_manifest['checks'][previous.CHECK_NAMES]":
        "    assert Path(old_manifest['batches'][-1])==previous.FINAL\n    assert old_manifest['checks'][previous.CHECK_SC1]",
    "len(old_manifest['batches']) == 700 and len(old_manifest['checks']) == 35":"len(old_manifest['batches']) == 701 and len(old_manifest['checks']) == 36",
    "len(dialogue_proof['changed_records']) == 277":"len(dialogue_proof['changed_records']) == 225",
    'Staged Hodram B211-B230.':'Staged Hodram B231-B250.',
})
register_source=checked_text(previous.register_source,{
    'verified_Rafael5186_output_reused=True':'verified_Hodram_B211_B230_output_reused=True',
    "r['id']) for r in bindings}) == 277":"r['id']) for r in bindings}) == 225",
    'verified_rafael5186_predecessor':'verified_hodram_b211_b230_predecessor',
    'hodram_B211_B230_late_dialogue':'hodram_B231_B250_late_dialogue',
    'Hodram B211–B230 dialogue.':'Hodram B231–B250 dialogue.',
    'release_stack.Hodram_B211_B230.pending.json':'release_stack.Hodram_B231_B250.pending.json',
    'late_editorial:hodram-b211-b230':'late_editorial:hodram-b231-b250',
    'Hodram_B211_B230_registered_successor_pipeline':'Hodram_B231_B250_registered_successor_pipeline',
    "result['batches'][:700] == old_manifest['batches'] and len(result['batches']) == 701":"result['batches'][:701] == old_manifest['batches'] and len(result['batches']) == 702",
    "len(result['checks']) == 36":"len(result['checks']) == 37",
    "'complete_stack_entries': 701, 'registered_manifest_entries': 701, 'passing_release_checks': 36":"'complete_stack_entries': 702, 'registered_manifest_entries': 702, 'passing_release_checks': 37",
    "'new_contextual_records': 277, 'prose_revisions': 170":"'new_contextual_records': 225, 'prose_revisions': 115",
    "'justified_retentions': 107":"'justified_retentions': 110",
    'Registered Hodram B211-B230 with 701 entries and 36 release checks.':'Registered Hodram B231-B250 with 702 entries and 37 release checks.',
})
env={**vars(previous),**globals(),'previous':previous,'__file__':__file__}
exec(compile(stage_source+'\n'+register_source,__file__+'::same-cumulative-successor-contract-new-exact-scope','exec'),env)
if __name__=='__main__':
    if sys.argv[1:]==['--register']:env['register']()
    else:
        assert not sys.argv[1:]
        env['stage']()
