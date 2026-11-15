"""Stage/register the cumulative successor while preserving all earlier stages and main."""
from pathlib import Path
import sys
from scripts import build_registered_hodram_B231_B250_v1 as previous
from scripts.finalize_hodram_B251_B280_research_v1 import FINAL,STORED
from scripts.prepare_hodram_B251_B280_registered_v1 import ARCHIVE,ARM,CLEAN,CONFIG,PARENT,QUALIFICATION,REGISTRY
from dk4tool.patch.hodram_b251_b280_release_v1 import plan_release
from scripts.source_locked_derivation_v5118 import checked_text

OUT=Path('work/hodram_B251_B280_release_v1');PROFILE='all-routes-hodram-b251-b280-dialogue-v1-20261107'
CANDIDATE=OUT/'all_routes_hodram_B251_B280_candidate.nds';MANIFEST=CANDIDATE.with_suffix('.manifest.json');PATCH=CANDIDATE.with_suffix('.xdelta')
INVERSE_PATCH=OUT/'clean_input_reconstruction_RESEARCH_ONLY.nds';STAGED=OUT/'staged_successor.json';RELEASE=OUT/'registered_release_verification.json'
STARTUP=OUT/'own_registered_startup_verification.json';GETTERS=OUT/'own_registered_name_getters_v1.json'
PARENT_REGISTRY=OUT/'release_stack_before_Hodram_B251_B280.json'
CHECK_SC1='registered_Hodram_B251_B280_dialogue_and_complete_parent_target_inverse'
NEGATIVES=Path('work/Hodram_B251_B280_clean_20261107/registered_semantic_checks_v2/qualification.json')

stage_source=checked_text(previous.stage_source,{
    'len(old_manifest[\'batches\']) == 701 and len(old_manifest[\'checks\']) == 36':
        'len(old_manifest[\'batches\']) == 702 and len(old_manifest[\'checks\']) == 37',
    "len(dialogue_proof['changed_records']) == 225":"len(dialogue_proof['changed_records']) == 216",
    'Staged Hodram B231-B250.':'Staged Hodram B251-B280.',
})
register_source=checked_text(previous.register_source,{
    'verified_Hodram_B211_B230_output_reused=True':'verified_Hodram_B231_B250_output_reused=True',
    "r['id']) for r in bindings}) == 225":"r['id']) for r in bindings}) == 216",
    'verified_hodram_b211_b230_predecessor':'verified_hodram_b231_b250_predecessor',
    'hodram_B231_B250_late_dialogue':'hodram_B251_B280_late_dialogue',
    'Hodram B231–B250 dialogue.':'Hodram B251–B280 dialogue.',
    'release_stack.Hodram_B231_B250.pending.json':'release_stack.Hodram_B251_B280.pending.json',
    'late_editorial:hodram-b231-b250':'late_editorial:hodram-b251-b280',
    'Hodram_B231_B250_registered_successor_pipeline':'Hodram_B251_B280_registered_successor_pipeline',
    "result['batches'][:701] == old_manifest['batches'] and len(result['batches']) == 702":
        "result['batches'][:702] == old_manifest['batches'] and len(result['batches']) == 703",
    "len(result['checks']) == 37":"len(result['checks']) == 38",
    "'complete_stack_entries': 702, 'registered_manifest_entries': 702, 'passing_release_checks': 37":
        "'complete_stack_entries': 703, 'registered_manifest_entries': 703, 'passing_release_checks': 38",
    "'new_contextual_records': 225, 'prose_revisions': 115":"'new_contextual_records': 216, 'prose_revisions': 129",
    "'justified_retentions': 110":"'justified_retentions': 87",
    'Registered Hodram B231-B250 with 702 entries and 37 release checks.':'Registered Hodram B251-B280 with 703 entries and 38 release checks.',
})
env={**previous.env,**vars(previous),**globals(),'previous':previous,'__file__':__file__}
exec(compile(stage_source+'\n'+register_source,__file__+'::same-cumulative-successor-contract-new-scope','exec'),env)
if __name__=='__main__':
    if sys.argv[1:]==['--register']:env['register']()
    else:
        assert not sys.argv[1:]
        env['stage']()
