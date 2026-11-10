"""Verify registered Rafael3222, its exact integrated references and clean-input patch."""
from scripts.verify_rafael2952_registered_extension_v1 import source as previous
from scripts.source_locked_derivation_v5118 import checked_text

source = checked_text(previous, {
    "prep['expected_manifest_entries'] == 689": "prep['expected_manifest_entries'] == 690",
    'len(set(owned)) == len(owned) == 20': 'len(set(owned)) == len(owned) == 19',
    '*range(161,201)]': '*range(161,221),231]',
    "        for row in doc['records']:\n            ref = deepcopy(row['planned_integrated_reference']);":
        """        stored_styles = {row['id']:row for row in load(conf['stored_native'])['style_records']}
        for row in doc['records']:
            ref = deepcopy(row['planned_integrated_reference']);""",
    "                header = bytes.fromhex(ref['exact_command_header_hex']); offset = ref['command_offset']":
        """                stored_style = stored_styles[row['id']]
                offset = ref['command_offset']
                assert stored_style['final_command_offset'] == offset and stored_style['source_style_indices'] == row['source_style_indices']
                ref['exact_command_header_hex'] = stored_style['final_header_hex']
                header = bytes.fromhex(ref['exact_command_header_hex'])""",
    '== 403': '== 270',
    '(299,104)': '(221,49)',
    '(383,21,173,174,209)': '(279,7,86,94,177)',
    'complete_stack_entries=689': 'complete_stack_entries=690',
    'new_contextual_records=403': 'new_contextual_records=270',
    'native_andviewed_body_pages=383,typed_choice_labels=21': 'native_andviewed_body_pages=279,typed_choice_labels=7',
    'observed_actual_source_speeches=173,observed_actual_body_pages=174,observed_actual_choices=13,observed_actual_menu_instances=6,offline_only_source_speeches=209':
        'observed_actual_source_speeches=86,observed_actual_body_pages=94,observed_actual_choices=7,observed_actual_menu_instances=3,offline_only_source_speeches=177',
    'Preserve registered Rafael2952 cumulative/intermediate/clean reconstruction.':
        'Preserve registered Rafael3222 cumulative/intermediate/clean reconstruction.',
    '689 entries/403 new five-gate reviews/383 pages': '690 entries/270 new five-gate reviews/279 pages',
})
if __name__ == '__main__':
    exec(compile(source, __file__+'::same-cumulative-inverse-and-clean-input-verification', 'exec'), globals())

