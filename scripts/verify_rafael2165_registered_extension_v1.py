"""Verify all 190 exact registered bindings and reconstruct the clean-input patch."""
from scripts.verify_rafael1975_registered_extension_v1 import source as previous
from scripts.source_locked_derivation_v5118 import checked_text


source = checked_text(previous, {
    "prep['expected_manifest_entries'] == 686": "prep['expected_manifest_entries'] == 687",
    'len(set(owned)) == len(owned) == 2': 'len(set(owned)) == len(owned) == 7',
    '[44,81,82,83,84,106,107,130,131,141,146,160,161,162,163,164,165,166,167,170,171,172,173,174,175,176,177,178,179,180]':
        '[44,81,82,83,84,106,107,130,131,141,146,160,161,162,163,164,165,166,167,168,169,177,178,179,180,181,182,183,184,185,186]',
    '== 115': '== 190',
    '== (90,25)': '== (152,38)',
    '== (117,0,58,60,57)': '== (190,0,72,72,118)',
    'complete_stack_entries=686': 'complete_stack_entries=687',
    'new_contextual_records=115': 'new_contextual_records=190',
    'native_andviewed_body_pages=117': 'native_andviewed_body_pages=190',
    'observed_actual_source_speeches=58,observed_actual_body_pages=60,observed_actual_choices=0,offline_only_source_speeches=57':
        'observed_actual_source_speeches=72,observed_actual_body_pages=72,observed_actual_choices=0,offline_only_source_speeches=118',
    'Preserve registered Rafael1975 cumulative/intermediate/clean reconstruction.':
        'Preserve registered Rafael2165 cumulative/intermediate/clean reconstruction.',
    '686 entries/115 new five-gate reviews/117 pages': '687 entries/190 new five-gate reviews/190 pages',
})
if __name__ == '__main__':
    exec(compile(source, __file__+'::same-registered-release-and-clean-input-verification', 'exec'), globals())
