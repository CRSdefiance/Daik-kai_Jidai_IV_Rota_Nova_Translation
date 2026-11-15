"""Verify the exact 115-record registered append and clean-input patch."""
from scripts.verify_rafael1860_registered_extension_v1 import source as previous
from scripts.source_locked_derivation_v5118 import checked_text


source = checked_text(previous, {
    "prep['expected_manifest_entries'] == 685": "prep['expected_manifest_entries'] == 686",
    '[44,81,82,83,84,106,107,130,131,141,146,160,161,162,163,164,165,168,177,178,179,180]':
        '[44,81,82,83,84,106,107,130,131,141,146,160,161,162,163,164,165,166,167,170,171,172,173,174,175,176,177,178,179,180]',
    '== 186': '== 115',
    '== (146,40)': '== (90,25)',
    '== (187,0,101,102,85)': '== (117,0,58,60,57)',
    'complete_stack_entries=685': 'complete_stack_entries=686',
    'new_contextual_records=186': 'new_contextual_records=115',
    'native_andviewed_body_pages=187': 'native_andviewed_body_pages=117',
    'observed_actual_source_speeches=101,observed_actual_body_pages=102,observed_actual_choices=0,offline_only_source_speeches=85':
        'observed_actual_source_speeches=58,observed_actual_body_pages=60,observed_actual_choices=0,offline_only_source_speeches=57',
    'Preserve registered Rafael1860 cumulative/intermediate/clean reconstruction.':
        'Preserve registered Rafael1975 cumulative/intermediate/clean reconstruction.',
    '685 entries/186 new five-gate reviews/187 pages': '686 entries/115 new five-gate reviews/117 pages',
})
if __name__ == '__main__':
    exec(compile(source, __file__+'::same-complete-release-and-clean-input-guards', 'exec'), globals())
