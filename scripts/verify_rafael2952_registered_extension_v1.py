"""Verify the exact B201–B220 cumulative release and clean-input patch."""
from scripts.verify_rafael2549_registered_extension_v1 import source as previous
from scripts.source_locked_derivation_v5118 import checked_text


source=checked_text(previous,{
    "prep['expected_manifest_entries'] == 688":"prep['expected_manifest_entries'] == 689",
    '*range(161,181)]':'*range(161,201)]',
    "            ref['target_archive_sha256'] = sha(resource)":
        """            if row['kind']=='typed-choice-label':
                command=ref['command_offset']
                assert int.from_bytes(block[command:command+2],'little')==row['source_word']
                assert ref['source_index']==row['source_index']
            ref['target_archive_sha256'] = sha(resource)""",
    '== 384':'== 403',
    '(317,67)':'(299,104)',
    '(384,0,148,148,236)':'(383,21,173,174,209)',
    'complete_stack_entries=688':'complete_stack_entries=689',
    'new_contextual_records=384':'new_contextual_records=403',
    'native_andviewed_body_pages=384,typed_choice_labels=0':'native_andviewed_body_pages=383,typed_choice_labels=21',
    'observed_actual_source_speeches=148,observed_actual_body_pages=148,observed_actual_choices=0,offline_only_source_speeches=236':
        'observed_actual_source_speeches=173,observed_actual_body_pages=174,observed_actual_choices=13,observed_actual_menu_instances=6,offline_only_source_speeches=209',
    'Preserve registered Rafael2549 cumulative/intermediate/clean reconstruction.':
        'Preserve registered Rafael2952 cumulative/intermediate/clean reconstruction.',
    '688 entries/384 new five-gate reviews/384 pages':'689 entries/403 new five-gate reviews/383 pages',
})
if __name__=='__main__':
    exec(compile(source,__file__+'::same-registered-cumulative-and-exact-clean-input-verification','exec'),globals())

