"""Stage/register310 reviews while retaining the complete712-entry accepted cumulative prefix."""
from pathlib import Path
from types import SimpleNamespace
import sys
from scripts import build_registered_maria_B50_v1 as template
from scripts.prepare_maria310_registered_v1 import ARCHIVE,ARM,CLEAN,CONFIG,PARENT,QUALIFICATION,REGISTRY,FINAL,ROOT
from dk4tool.patch.maria310_release_v1 import plan_release
from dk4tool.script.format_safety_relocated_v2 import bind_registered_story_percent_guard
from scripts.source_locked_derivation_v5118 import checked_text

STORED=ROOT/'stored_v3/stored_native_verification.json'
OUT=Path('work/maria310_release_v1');PROFILE='all-routes-maria310-dialogue-v1-20261109'
CANDIDATE=OUT/'all_routes_maria310_candidate.nds'
MANIFEST=CANDIDATE.with_suffix('.manifest.json');PATCH=CANDIDATE.with_suffix('.xdelta')
INVERSE_PATCH=OUT/'clean_input_reconstruction_RESEARCH_ONLY.nds'
STAGED=OUT/'staged_successor.json';RELEASE=OUT/'registered_release_verification.json'
STARTUP=OUT/'own_registered_startup_verification.json';GETTERS=OUT/'own_registered_name_getters_v1.json'
PARENT_REGISTRY=OUT/'release_stack_before_Maria310.json'
CHECK_SC1='registered_Maria310_dialogue_FE_storage_and_complete_parent_target_inverse'
NEGATIVES=ROOT/'registered_semantic_checks_v1/qualification.json'
SOURCE25_SPEC=template.SOURCE25_SPEC
predecessor=SimpleNamespace(CHECK_SC1=template.CHECK_SC1)
stage_source=checked_text(template.stage_source,{
    "assert Path(old_manifest['batches'][-1])==prior270.FINAL\n    assert old_manifest['checks'][prior270.CHECK_SC1]":
        "assert Path(old_manifest['batches'][-1])==template.FINAL\n    assert old_manifest['checks'][template.CHECK_SC1]",
    "len(old_manifest['batches']) == 711 and len(old_manifest['checks']) == 46":
        "len(old_manifest['batches']) == 712 and len(old_manifest['checks']) == 47",
    "len(dialogue_proof['changed_records']) == 16":"len(dialogue_proof['changed_records']) == 310",
    'source_owned_FE_continuation_andfull139_character_paragraph_preserved=True,':
        'source_owned_FE_continuation_andfull139_character_paragraph_preserved=True,source_bound_FE_storage_alignment_andall318_compiled_pages_preserved=True,',
    'Staged Maria B50.':'Staged Maria310.',
})
register_source=checked_text(template.register_source,{
    'verified_Maria270_output_reused=True':'verified_Maria_B50_output_reused=True',
    "r['id']) for r in bindings}) == 16":"r['id']) for r in bindings}) == 310",
    "sum(len(r['registered_native_pages']) for r in bindings)==17":"sum(len(r['registered_native_pages']) for r in bindings)==310",
    'verified_maria270_predecessor=predecessor, maria_B50_late_dialogue':
        'verified_maria_B50_predecessor=predecessor, maria310_late_dialogue',
    'Maria B50 contextual dialogue with exact-source FE continuation, retaining every prior layer.':
        'Maria B51–B57 contextual dialogue, wrapping and exact FE storage correction, retaining every prior layer.',
    'release_stack.Maria_B50.pending.json':'release_stack.Maria310.pending.json',
    'late_editorial:maria-B50':'late_editorial:maria310','Maria_B50_registered_successor_pipeline':'Maria310_registered_successor_pipeline',
    "result['batches'][:711] == old_manifest['batches'] and len(result['batches']) == 712":
        "result['batches'][:712] == old_manifest['batches'] and len(result['batches']) == 713",
    "len(result['checks']) == 47":"len(result['checks']) == 48",
    "'complete_stack_entries': 712, 'registered_manifest_entries': 712, 'passing_release_checks': 47":
        "'complete_stack_entries': 713, 'registered_manifest_entries': 713, 'passing_release_checks': 48",
    "'new_contextual_records': 16, 'prose_revisions': 9":"'new_contextual_records': 310, 'prose_revisions': 184",
    "'justified_retentions': 7, 'physical_native_panels':17, 'additional_exact_source_FE_controls':1":
        "'justified_retentions': 126, 'physical_native_panels':310, 'additional_exact_source_FE_controls':0, 'FE_storage_padding_repairs':1",
    'Registered Maria B50 with712 entries and47 release checks.':'Registered Maria310 with713 entries and48 release checks.',
})
env={**template.env,**vars(template),**globals(),'previous':predecessor,'__file__':__file__}
exec(compile(stage_source+'\n'+register_source,__file__+'::same-complete-cumulative-contract713-with-exact-FE-storage-amendment','exec'),env)
if __name__=='__main__':
    if sys.argv[1:]==['--register']:env['register']()
    else:assert not sys.argv[1:];env['stage']()
