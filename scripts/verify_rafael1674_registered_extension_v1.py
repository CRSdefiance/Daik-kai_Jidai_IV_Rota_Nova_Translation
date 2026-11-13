"""Verify the five-block append, all 684 entries and exact clean-ROM reconstruction."""
from scripts.verify_rafael1607_registered_extension_v1 import source as previous
from scripts.source_locked_derivation_v5118 import checked_text

source = checked_text(previous, {
    "prep['expected_manifest_entries'] == 683": "prep['expected_manifest_entries'] == 684",
    'len(set(owned)) == len(owned) == 4': 'len(set(owned)) == len(owned) == 5',
    '[44,81,82,83,84,106,107,130,131,141,146,160]': '[44,81,82,83,84,106,107,130,131,141,146,160,177,178,179,180]',
    '== 183': '== 67',
    '== (133,50)': '== (51,16)',
    '== (186,8,104,115,71)': '== (68,0,55,56,12)',
    'complete_stack_entries=683': 'complete_stack_entries=684',
    'new_contextual_records=183': 'new_contextual_records=67',
    'native_andviewed_body_pages=186,typed_choice_labels=8': 'native_andviewed_body_pages=68,typed_choice_labels=0',
    'observed_actual_source_speeches=104,observed_actual_body_pages=115,observed_actual_choices=8,offline_only_source_speeches=71':
        'observed_actual_source_speeches=55,observed_actual_body_pages=56,observed_actual_choices=0,offline_only_source_speeches=12',
    'Preserve registered Rafael1607 cumulative/intermediate/clean reconstruction.':
        'Preserve registered Rafael1674 cumulative/intermediate/clean reconstruction.',
    '683 entries/183 new five-gate reviews/186 pages': '684 entries/67 new five-gate reviews/68 pages',
})
if __name__ == '__main__':
    exec(compile(source, __file__ + '::same-release-and-exact-patch-guards-for-67-records', 'exec'), globals())
