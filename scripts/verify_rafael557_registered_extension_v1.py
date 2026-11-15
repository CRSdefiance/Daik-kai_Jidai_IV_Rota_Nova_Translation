"""Verify the complete 557 append, 682 entries and byte-exact clean-input patch."""
from scripts.verify_rafael351_registered_extension_v3 import source as previous
from scripts.source_locked_derivation_v5118 import checked_text

source=checked_text(previous,{
    'scripts.registered_canonical_extension_resume_v3 import qualify,stage_source,STAGES':
        'scripts.registered_canonical_extension_resume_v6 import qualify,stage_source,STAGES,derive_tail',
    "    assert sha(tail.encode('utf-8'))==resume['executed_original_final_contract_source_sha256']":
        """    assert sha(tail.encode('utf-8'))==resume['original_final_contract_source_sha256']
    assert sha(derive_tail(tail).encode('utf-8'))==resume['executed_final_contract_source_sha256']
    assert resume['source_bound_story_percent_guard']==resume_config['percent_relocation_guard']
    assert m['story_percent_contract']['exact_source_bound_relocated_leading25_count']==5
    assert m['story_percent_contract']['all_four_final_story_archives_checked']""",
    "prep['expected_manifest_entries'] == 681":"prep['expected_manifest_entries'] == 682",
    'len(set(owned)) == len(owned) == 18':'len(set(owned)) == len(owned) == 20',
    "== 351":"== 557",
    "== (201,150)":"== (235,322)",
    "== (344,10,132,134,209)":"== (558,8,188,193,361)",
    "complete_stack_entries=681":"complete_stack_entries=682",
    "new_contextual_records=351":"new_contextual_records=557",
    "native_andviewed_body_pages=344,typed_choice_labels=10":"native_andviewed_body_pages=558,typed_choice_labels=8",
    "observed_actual_source_speeches=132,observed_actual_body_pages=134,observed_actual_choices=10,offline_only_source_speeches=209":
        "observed_actual_source_speeches=188,observed_actual_body_pages=193,observed_actual_choices=8,offline_only_source_speeches=361",
    'Preserve registered867 cumulative/intermediate/clean reconstruction.':'Preserve registered Rafael1424 cumulative/intermediate/clean reconstruction.',
    '681 entries/351 new five-gate reviews/344 pages':'682 entries/557 new five-gate reviews/558 pages',
})
if __name__=='__main__':exec(compile(source,__file__+'::same-release-andpatch-guards-557-records','exec'),globals())
