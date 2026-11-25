"""Derive stored B52 parity/body/control/typed-label/two-end checks with complete image inverse."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save

if __name__=='__main__':
    root=Path('work/analysis/Hodram_B52_stored_tools_v8643');assert not root.exists()
    source=Path('scripts/prove_Hodram_B51_stored_v8566.py').read_text(encoding='utf-8')
    a=source.index("    end_env = dict(end_case.__globals__)");b=source.index("    save(ROOT / 'stored_native_controls_andrefs.json'",a)
    ends="""    end_env = dict(end_case.__globals__)
    exec(compile(source['source_owned_seeded_end_adapter'], __file__ + '::original-both-full-value-carry-ends', 'exec'), end_env)
    terminals=[c for c in group['all_target_commands'] if c['word']==0];terminal=terminals[-1]
    assert len(terminals)==2 and terminal['native_extent']==4 and terminal['offset']+4==group['target_logical_end']
    assert [c['whole_command_hex'] for c in terminals]==['00000000','00000080']
    ends = [end_env['end_case'](arm, target, terminal['offset'], previous, value)
        for terminal in terminals for previous in [0, 1, 2, 3, 0xFFFFFFFF] for value in [0, 1, 2, 3, 0xFFFFFFFF]]
    assert len(rows)==3 and len(fresh)==2 and len(reused)==1 and len(dispatches)==3 and not queries and len(opaque)==4 and len(ends)==50 and not ctx.machines
    assert all(e['native_result']==([1,0,0,0,0,0] if e['flagged_terminal'] else [0,e['initial_value_word'],0,0,0,0]) for e in ends)
    assert sum(len(c['cases']) for c in group['relocated_skip_cases'])==20
    assert menu_checks is not None and len(choice_rows)==2
"""
    menu="""        elif word==0x2100:
            from scripts.prove_lil_B212_consumers_v6595 import choice_getters
            mc=group['choice_commands'][0];raw=bytes.fromhex(command['whole_command_hex'])
            menu_proof=read('work/analysis/Hodram_B52_menu_v8636/menu_provider_and_planes.json')
            assert raw.hex()==mc['target_hex'] and sha(raw)==menu_proof['compiled_choice_object_sha256'] and raw==Path(menu_proof['compiled_choice_object']).read_bytes()
            menu_checks=choice_getters(arm,command)
            assert len(menu_checks)==2 and all(c['count']==2 and [r['text'] for r in c['labels']]==[r['english'] for r in doc['typed_choice_records']] for c in menu_checks)
            for row,ref in zip(doc['typed_choice_records'],mc['label_references'],strict=True):
                assert row['id']==ref['id'] and row['option_index']==ref['option_index'] and row['source_reference']==ref['source_reference'] and row['current_reference']==ref['old_reference']
                at=ref['new_offset'];label=row['english'].encode('ascii')
                assert target[at:at+len(label)+1]==label+b'\\0' and target[:at].count(b'\\0')==ref['new_record_index'] and ref['target_hex']==label.hex()
                planes=[p for p in menu_proof['records'] if p['version']=='reviewed-stored-English' and p['option_index']==row['option_index']]
                assert len(planes)==2 and all(p['text']==row['english'] and sha(Path(p['native_plane']).read_bytes())==p['native_plane_sha256'] and p['visible_cell_center_twice']==72 for p in planes)
                choice_rows.append(dict(id=row['id'],option_index=row['option_index'],source_reference=row['source_reference'],current_reference=row['current_reference'],source_hex=row['source_hex'],current_hex=row['current_hex'],final_reference=dict(file_path='/data/SC1.DK4',block=52,offset=at,bytes=len(label),header_offset=command['offset'],command_offset=command['offset'],record_index=ref['new_record_index'],option_index=row['option_index'],target_block_sha256=sha(target)),stored_hex=label.hex(),typed_command_hex=raw.hex(),native_caption_planes_reused_exact=planes,menu_width72_andchanged_geometry_actual_test_pending=True))
        elif word not in [0, 0x4000, 0x100, 0x200, 0x300, 0x400]:
"""
    result=derive('scripts/prove_Hodram_B51_stored_v8566.py','scripts/prove_Hodram_B52_stored_v8643.py',{
        source[a:b]:ends,
        'scripts.Hodram_B50_registered_route_context_v8546':'scripts.Hodram_B51_registered_route_context_v8612',
        'Hodram_B51_stored_v8566':'Hodram_B52_stored_v8643','Hodram_B51_relocation_v8565':'Hodram_B52_relocation_v8642','Hodram_B51_pages_v8563':'Hodram_B52_pages_v8635',
        'work/analysis/Hodram_B51_native_review_v8564/native_body_review.json':'work/analysis/Hodram_B52_native_note_v8638/qualified_native_review.json',
        'hodram_B51_editorial_manuscript_v2':'hodram_B52_editorial_manuscript_v3','current_V8543_Hodram_native_v8546':'current_V8609_Hodram_native_v8612','Hodram_B51_source_controls_v8555':'Hodram_B52_source_controls_v8620','Hodram_B51_source_display_v8556':'Hodram_B52_source_display_v8626','Hodram_B51_current_v8559':'Hodram_B52_current_v8631',
        "native['manuscript_sha256'] == sha(Path(doc['predecessor_manuscript']).read_bytes())":"sha(NATIVE.read_bytes())==doc['native_body_pages_sha256'] and native['manuscript_sha256']==read(doc['predecessor_manuscript'])['predecessor_manuscript_sha256']",
        "view['all_five_complete_bodies_visually_read'] and view['directly_viewed_sheet'] == native['review_sheet']":"view['all_words_compiled_bytes_source_current_refs_individual_review_gates_native_planes_choice_geometry_andactual_scope_unchanged'] and read(view['prior_native_review'])['directly_viewed_speech_sheet']==native['review_sheet']",
        '.blocks[51]':'.blocks[52]','block=51':'block=52',
        'rows, fresh, reused, dispatches, queries, opaque = [], [], [], [], [], []':'rows, fresh, reused, dispatches, queries, opaque = [], [], [], [], [], []\n    choice_rows=[];menu_checks=None',
        '{1: 1, 16: 1, 18: 0, 113: 0}[stored[0]]':'{113:0}[stored[0]]',
        '        elif word not in [0, 0x4000, 0x100, 0x200, 0x300, 0x400]:\n':menu,
        'fresh_native_alignment_cases=4, exact_reused_native_alignment_cases=16':'fresh_native_alignment_cases=8, exact_reused_native_alignment_cases=4',
        'all5_full_first_internal_final_glyphs_bounds_consumption_single_page_andviewed_ink_checks_pass':'all3_speech_full_first_internal_final_glyphs_bounds_consumption_single_page_andviewed_ink_checks_pass',
        'four_opaque_structural_decodes=opaque, normal_seeded_ends=ends':'four_opaque_structural_decodes=opaque, distinct_seeded_ends=ends, typed_choice_records=choice_rows,stored_menu_getters=menu_checks',
        'all20_commands5_preambles8_relative_sites2_queries4_opaque_controls_andwhole_source_current_inverses_bound':'all14_commands3_preambles4_relative_sites_zeroqueries_twochoices4_opaque_controls_bothendwords_andwhole_source_current_inverses_bound',
        'actual_B51_branch_name_header_transition_effect_semantics_loaders_policy_atomic_andregistered_release_pending':'actual_B52_changed_menu_branch_name_header_both_end_transition_effect_semantics_loaders_policy_atomic_andregistered_release_pending',
        'Stored B51 parity':'Stored B52 parity',
        'the single changed parity tail is freshly exercised':'the two changed parity tails are freshly exercised',
        'B51 stored: one parity tail/four fresh alignments, four exact bodies/sixteen reused alignments; five dispatches, two queries, forty reused branch cases, twenty-five complete value-carry ends.':'B52 stored: two parity tails/eight fresh alignments, one exact body/four reused alignments; three dispatches,two typed labels,zeroqueries,twenty reused branch cases,fifty distinct end cases.',
    })
    root.mkdir(parents=True);save(root/'derivation.json',dict(tool=result,all_native_high_integer_constants_andmultiplicity_preserved=True,all_original_native_body_macro_scratch_unowned4MiB_output_ink_bounds_andwholeROM_inverse_guards_preserved=True,two_distinct_original_end_words_andall_six_result_fields_checked=True,exact32byte_menu_getters_label_refs_andtwo_styles_reused_by_whole_object_binding=True,no_emulator_ROM_registry_orcredit_change=True,new_credit=0,full_goal_complete=False))
