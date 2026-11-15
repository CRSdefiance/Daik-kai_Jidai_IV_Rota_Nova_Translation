"""Prepare the first current-English exposure after all clean branch-specific glosses."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
if __name__=='__main__':
    root=Path('work/analysis/Rafael_B46_current_tools_v7927');assert not root.exists()
    menu="""    assert len(rows)==24 and len(groups)==1
    import struct
    from datetime import datetime,timezone
    sg=source['groups'][0];cg=groups[0];now=bytes.fromhex(cg['current_block_hex'])
    original_menu=next(c for c in sg['commands'] if c['word']==0x2100)
    paired=next(c for c in cg['all_command_reference_pairs'] if c['source_offset']==original_menu['offset'])
    at=paired['current_offset'];base=at+6
    assert original_menu==gloss['typed_menu_source'] and paired['word']==0x2100
    choice_records=[]
    for option in gloss['menu_choices']:
        row=deepcopy(option);i=row['option_index'];delta=struct.unpack_from('<H',now,at+2+2*i)[0]
        start=base+delta;end=now.index(0,start);value=now[start:end]
        assert at+6<=start<end<at+paired['current_extent']
        row.update(source_gloss_precanonical_ID=row['id'],id=f'DK4_CHOICE_B46_C256_O{i}',
            kind='typed-choice',source_kind='typed-choice',current_command_offset=at,
            current_reference=dict(block=46,command_offset=at,relative_table_field=at+2+2*i,relative_base=base,relative_offset=delta,offset=start,bytes=len(value),record_index=now[:start].count(b'\\0')),
            current_hex=value.hex(),current_raw_storage_English=value.decode('cp932'),
            raw_storage_comparison_paragraph=' '.join(value.decode('cp932').split()),
            current_English_body_unread=False,current_native_menu_getters_geometry_outcome_andactual_pending=True)
        choice_records.append(row)
    exposure=datetime.now(timezone.utc).isoformat()
    assert datetime.fromisoformat(gloss['source_first_boundary_UTC'])<datetime.fromisoformat(exposure)
"""
    row=derive('scripts/map_Rafael_B45_current_v7871.py','scripts/map_Rafael_B46_current_v7927.py',{
        'First Rafael B45 current-English exposure after twelve clean glosses,names andsource control binding.':'First Rafael B46 current-English exposure after complete branch-specific speech/choice glosses, names andsource control binding.',
        'Rafael_B45_current_v7871':'Rafael_B46_current_v7927',
        'Rafael_next_clean_v7864/complete_clean_SC0_B45_EV0_andcoverage_before_current_English.json':'Rafael_next_clean_v7918/complete_clean_SC0_B46_EV0_andcoverage_before_current_English.json',
        'Rafael_B45_clean_gloss_v7864b/twelve_fresh_clean_exchange_glosses_before_current_English.json':'Rafael_B46_branch_gloss_v7926/24_speeches2_choices_fresh_branch_context_before_current_English.json',
        'Rafael_B45_names_v7869/two_static_speakers_four_getters_clean_fields_eight_macro_alignments.json':'Rafael_B46_names_v7921/three_static_speakers_six_getters_clean_fields12_synthetic_macro_alignments.json',
        "gloss['source_packet_sha256']==sha(SOURCE.read_bytes()) and names['source_gloss_sha256']==sha(GLOSS.read_bytes())":"gloss['complete_clean_source_group']==source['groups'][0] and names['source_gloss_sha256']==gloss['previous_source_gloss_sha256']",
        "gloss['all12_complete_clean_Japanese_speeches_read_before_current_English'] and names['current_English_B45_bodies_still_unread'] and read('work/analysis/Rafael_B45_source_controls_v7870b/source_EV0_five_relative_sites_predicate_resources_structural_andnormal_end.json')['current_B45_English_bodies_still_unread']":"gloss['source_branch_context_refined_before_current_English_exposure'] and names['current_English_B46_bodies_andtwo_choices_still_unread'] and read(gloss['source_branch_proof'])['no_current_English_B46_body_orchoice_read']",
        '    assert len(rows)==12':menu.rstrip(),
        'all12_complete_source_current_refs_before_new_English_manuscript.json':'all24_speeches2_choices_source_current_refs_before_new_English_manuscript.json',
        'groups=groups,records=rows,all12_clean_whole_context_glosses_precede_current_English_exposure=True':'groups=groups,records=rows,typed_choice_records=choice_records,total_editorial_objects=26,source_first_boundary_UTC=gloss[\'source_first_boundary_UTC\'],current_English_exposure_UTC=exposure,all26_clean_whole_context_glosses_precede_current_English_exposure=True',
        'source_explicit_completion_dependencies=[]':'source_explicit_completion_dependencies=[38]',
        "        for r in g['records']:print(r['source_record_index'],repr(r['raw_storage_comparison_paragraph']))":"        for r in g['records']:print(r['source_record_index'],repr(r['raw_storage_comparison_paragraph']))\n    for r in choice_records:print(r['id'],repr(r['raw_storage_comparison_paragraph']))",
    })
    root.mkdir(parents=True);save(root/'source_locked_derivation.json',row)
