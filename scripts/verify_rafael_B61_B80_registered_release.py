"""Verify cumulative539 references and all eight stages,then reconstruct from clean input."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import checked_text
source=checked_text(Path('scripts/verify_rafael_B51_B60_registered_release.py').read_text(encoding='utf-8'),{
    'import argparse':'import argparse\nimport os',
    'Shared_tutorial_name_data_release_verified_20261104':'Rafael_B51_B60_release_verified_20261104',
    'Rafael_B51_B60_release_qualification_v2_20261104':'Rafael_B61_B80_release_qualification_20261104',
    "    assert config_paths[-1]==Path(prepared['field_config'])":
        "    assert config_paths==[Path(prepared['preserved_stage_configs'][key]) for key in KEYS]",
    'for k in KEYS[:-1]':'for k in KEYS',
    "parent_manifest['batches'][-7:]":"parent_manifest['batches'][-8:]",
    "parent_manifest['batches'][:-7]":"parent_manifest['batches'][:-8]",
    'len(expected_batches)==669':'len(expected_batches)==670',
    "len(qualification['semantic_rejections'])==12":"len(qualification['semantic_rejections'])==9",
    "    original_preparation=Path(prepared['prior_preparation'])\n    old_registry=load(original_preparation.parent/'release_stack_before.json')":
        "    old_registry=load(args.preparation.parent/'release_stack_before.json')",
    "    assert field_proof==qualification['positive_field_plan'] and candidate.read_file('/__arm9__.bin')==arm":
        "    assert candidate.read_file('/__arm9__.bin')==arm and qualification['unchanged_eight_final_stage_contracts_compared_exactly']",
    "assert [p for p,v in parent.iter_components() if candidate.read_file(p)!=v]==['/__arm9__.bin']":
        "assert [p for p,v in parent.iter_components() if candidate.read_file(p)!=v]==[]",
    "    inverse_arm=bytearray(arm)\n    for f in field_proof['fields']:\n        at,n=f['physical_offset'],f['owned_bytes'];assert inverse_arm[at:at+n].hex()==f['new_hex']\n        inverse_arm[at:at+n]=bytes.fromhex(f['old_hex'])\n    assert bytes(inverse_arm)==parent.read_file('/__arm9__.bin')":
        "    assert arm==parent.read_file('/__arm9__.bin')\n    inverse_arm=bytearray(arm)",
    '==list(range(51,61))':'==[n for n in range(61,81) if n!=68]',
    "(final['proposed_revisions'],final['wording_retentions'])==(102,147)":"(final['proposed_revisions'],final['wording_retentions'])==(210,329)",
    'len(final[\'records\'])==249':'len(final[\'records\'])==539',
    'all249_final_bytes_controls_source_current_andindividual_gates_bound':'all539_final_bytes_controls_source_current_andindividual_gates_bound',
    "changed_components=['/__arm9__.bin']":"changed_components=[]",
    'only_reviewed_SC0_ten_blocks_andone_owned_name_field_changed=True':
        'only_reviewed_SC0_nineteen_blocks_changed=True,all_other_files_components_graphics_names_andruntime_exact_to_parent=True',
    'complete_stack_entries=669':'complete_stack_entries=670',
    'new_contextual_records=249,dialogue_revisions=102,justified_retentions=147,wrap_fixes=38,ASCII_I_corrections=3,separate_name_field_corrections=1':
        'new_contextual_records=539,dialogue_revisions=210,justified_retentions=329,wrap_fixes=14,ASCII_I_corrections=16,ellipsis_corrections=14,separate_name_field_corrections=0',
    'actual_research_utterances=32,offline_only_utterances=213,actual_choice_captions=4':
        'actual_research_utterances=95,offline_only_utterances=444,actual_choice_captions=0',
    'all249_exact_integrated_references_bound':'all539_exact_integrated_references_bound',
    "*Path('work/f8').rglob('*.nds')":"*Path('work/r61').rglob('*.nds')",
    'Preserve registered Rafael249 eight-stage':'Preserve registered Rafael539 eight-stage',
    '    save(pins_path,pins)':
        "    temporary=pins_path.with_name('rom_retention_pins.Rafael539_verified.pending.json');assert not temporary.exists()\n    save(temporary,pins);assert pins_path.read_bytes()==pins_before;os.replace(temporary,pins_path)",
    '669 entries/114 accepted layers/eight stages/249 exact references':'670 entries/114 accepted layers/eight stages/539 exact references',
})
exec(compile(source,__file__+'::same-registered-stage-reference-inverse-andclean-patch-checks','exec'),globals())
