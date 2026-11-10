"""Verify the 183 tutorial append, 683 entries, and byte-exact clean-input patch."""
from scripts.verify_rafael557_registered_extension_v1 import source as previous
from scripts.source_locked_derivation_v5118 import checked_text

source=checked_text(previous,{
    "prep['expected_manifest_entries'] == 682":"prep['expected_manifest_entries'] == 683",
    'len(set(owned)) == len(owned) == 20':'len(set(owned)) == len(owned) == 4',
    "[44,81,82,83,84,106,107,130,131]":"[44,81,82,83,84,106,107,130,131,141,146,160]",
    "== 557":"== 183",
    "== (235,322)":"== (133,50)",
    "== (558,8,188,193,361)":"== (186,8,104,115,71)",
    "complete_stack_entries=682":"complete_stack_entries=683",
    "new_contextual_records=557":"new_contextual_records=183",
    "native_andviewed_body_pages=558,typed_choice_labels=8":"native_andviewed_body_pages=186,typed_choice_labels=8",
    "observed_actual_source_speeches=188,observed_actual_body_pages=193,observed_actual_choices=8,offline_only_source_speeches=361":
        "observed_actual_source_speeches=104,observed_actual_body_pages=115,observed_actual_choices=8,offline_only_source_speeches=71",
    'Preserve registered Rafael1424 cumulative/intermediate/clean reconstruction.':'Preserve registered Rafael1607 cumulative/intermediate/clean reconstruction.',
    '682 entries/557 new five-gate reviews/558 pages':'683 entries/183 new five-gate reviews/186 pages',
})
if __name__=='__main__':
    exec(compile(source,__file__+'::same-release-and-exact-patch-guards-for-183-records','exec'),globals())
