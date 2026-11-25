"""Verify the exact cumulative B181–B200 release and clean-input patch."""
from scripts.verify_rafael2165_registered_extension_v1 import source as previous
from scripts.source_locked_derivation_v5118 import checked_text

source = checked_text(previous, {
    "prep['expected_manifest_entries'] == 687": "prep['expected_manifest_entries'] == 688",
    'len(set(owned)) == len(owned) == 7': 'len(set(owned)) == len(owned) == 20',
    '[44,81,82,83,84,106,107,130,131,141,146,160,161,162,163,164,165,166,167,168,169,177,178,179,180,181,182,183,184,185,186]':
        '[44,81,82,83,84,106,107,130,131,141,146,160,*range(161,181)]',
    '== 190': '== 384',
    '== (152,38)': '== (317,67)',
    '== (190,0,72,72,118)': '== (384,0,148,148,236)',
    'complete_stack_entries=687': 'complete_stack_entries=688',
    'new_contextual_records=190': 'new_contextual_records=384',
    'native_andviewed_body_pages=190': 'native_andviewed_body_pages=384',
    'observed_actual_source_speeches=72,observed_actual_body_pages=72,observed_actual_choices=0,offline_only_source_speeches=118':
        'observed_actual_source_speeches=148,observed_actual_body_pages=148,observed_actual_choices=0,offline_only_source_speeches=236',
    'Preserve registered Rafael2165 cumulative/intermediate/clean reconstruction.':
        'Preserve registered Rafael2549 cumulative/intermediate/clean reconstruction.',
    '687 entries/190 new five-gate reviews/190 pages': '688 entries/384 new five-gate reviews/384 pages',
})
if __name__ == '__main__':
    exec(compile(source, __file__+'::same-registered-release-and-clean-input-verification', 'exec'), globals())
