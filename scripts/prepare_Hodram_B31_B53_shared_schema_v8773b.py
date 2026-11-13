"""Reuse completed shared positive; qualify literal receipt key and finish the late failure."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
if __name__=='__main__':
    root=Path('work/analysis/Hodram_B31_B53_shared_schema_v8773b');assert not root.exists()
    source=Path('scripts/validate_Hodram_B31_B53_shared_v8773.py').read_text('utf-8')
    a=source.index('    image=WatchedImage(');z=source.index('    prior_path=',a)
    reuse="""    old_positive=Path('work/analysis/Hodram_B31_B53_shared_extension_v8773/positive.json')
    positive=read(old_positive)
    assert positive['spec']==spec and positive['one_final_whole_NDS_commit'] and positive['original_object_identity_files_components_andserialized_bytes_exact_until_commit']
    assert positive['whole_output_equals_reviewed_reference'] and positive['canonical_source_full_current_memory'] and positive['all_frozen_native_editorial_andproduction_guards_active']
    assert len(positive['reports'])==1 and len(positive['reports'][0]['changed_records'])==3 and positive['reports'][0]['target_ROM_sha256']==sha(ROM.read_bytes())
    save(ROOT/'positive.json',positive)
    print('REUSE exact completed shared positive;no planner orpositive case replay',flush=True)
"""
    receipt=derive('scripts/validate_Hodram_B31_B53_shared_v8773.py','scripts/validate_Hodram_B31_B53_shared_v8773b.py',{
        source[a:z]:reuse,
        'Hodram_B31_B53_shared_extension_v8773':'Hodram_B31_B53_shared_extension_v8773b',
        "prior['evidence'][str(shared)]":"prior['evidence'][shared.as_posix()]",
        'positive_lifecycles=1,negative_count=1':'positive_lifecycles=1,negative_count=1,completed_positive_reused_without_reexecution=True,positive_source=str(old_positive),positive_source_sha256=sha(old_positive.read_bytes()),',
    })
    root.mkdir(parents=True);save(root/'derivation.json',dict(tool=receipt,stopped_reader_andcompleted_positive_preserved=True,
        existing_generic_framework_receipt_uses_forward_slash_literal_key_not_platform_Path_string=True,
        no_guard_orsemantics_change_no_completed_positive_replay=True,new_credit=0,full_goal_complete=False))
