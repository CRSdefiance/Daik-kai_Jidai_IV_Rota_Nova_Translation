"""Verify the exact 186-speech append and its clean-ROM reconstruction."""
from scripts.verify_rafael1674_registered_extension_v1 import source as previous
from scripts.source_locked_derivation_v5118 import checked_text

source=checked_text(previous,{
    "prep['expected_manifest_entries'] == 684":"prep['expected_manifest_entries'] == 685",
    'len(set(owned)) == len(owned) == 5':'len(set(owned)) == len(owned) == 2',
    '[44,81,82,83,84,106,107,130,131,141,146,160,177,178,179,180]':
        '[44,81,82,83,84,106,107,130,131,141,146,160,161,162,163,164,165,168,177,178,179,180]',
    '== 67':'== 186',
    '== (51,16)':'== (146,40)',
    '== (68,0,55,56,12)':'== (187,0,101,102,85)',
    'complete_stack_entries=684':'complete_stack_entries=685',
    'new_contextual_records=67':'new_contextual_records=186',
    'native_andviewed_body_pages=68,typed_choice_labels=0':'native_andviewed_body_pages=187,typed_choice_labels=0',
    'observed_actual_source_speeches=55,observed_actual_body_pages=56,observed_actual_choices=0,offline_only_source_speeches=12':
        'observed_actual_source_speeches=101,observed_actual_body_pages=102,observed_actual_choices=0,offline_only_source_speeches=85',
    'Preserve registered Rafael1674 cumulative/intermediate/clean reconstruction.':
        'Preserve registered Rafael1860 cumulative/intermediate/clean reconstruction.',
    '684 entries/67 new five-gate reviews/68 pages':'685 entries/186 new five-gate reviews/187 pages',
})
if __name__=='__main__':
    exec(compile(source,__file__+'::same-release-and-exact-patch-guards-for-186-records','exec'),globals())
