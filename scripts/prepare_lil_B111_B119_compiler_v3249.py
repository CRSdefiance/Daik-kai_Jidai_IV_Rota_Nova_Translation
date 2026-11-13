"""Prepare a guarded cumulative compiler without changing earlier release stages."""
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import save

OLD=Path('dk4tool/patch/lil_shrines_temples_editorial.py')
NEW=Path('dk4tool/patch/lil_B111_B119_editorial.py')
ROOT=Path('work/analysis/lil_B111_B119_compiler_tools_v3249')
if __name__=='__main__':
    assert not NEW.exists() and not ROOT.exists();t=OLD.read_text(encoding='utf-8')
    # Delete unsupported player-choice behavior, retaining an explicit empty census.
    a=t.index("    menu_native=load(doc['native_choice_proof'])");z=t.index("    refs={r['id']",a)
    t=t[:a]+t[z:]
    a=t.index("        for ref in spec['choice_commands']:");z=t.index('        patches.sort(',a)
    t=t[:a]+"        _require(spec['choice_commands']==[],'unexpected player-choice object')\n"+t[z:]
    swaps={
        'lil_shrines_temples_layout_v2':'lil_B111_B119_layout_v2',
        'lil_shrines_temples_profile':'lil_B111_B119_profile',
        'lil_shrines_temples_editorial_release_v1.json':'lil_B111_B119_editorial_release_v1.json',
        'Lil Shrines/Temples ':'Lil B111-B119 ',
        'range(101,111)':'range(111,120)',
        'dk4-lil-shrines-temples-editorial-release-v1':'dk4-lil-B111-B119-editorial-release-v1',
        'dk4-lil-shrines-temples-source-relocation-map-v1':'dk4-lil-B111-B119-source-relocation-map-v1',
        "doc,voice,menu=[load(config[k]) for k in ['manuscript','actor_styles','choices']]":"doc,voice=[load(config[k]) for k in ['manuscript','actor_styles']]",
        'for d in [doc,voice,menu]:':'for d in [doc,voice]:',
        'all421_nested_command_boundaries_and114_relative_sites_verified':'all305_physical_nested_command_boundaries_and64_relative_sites_verified',
        'all570_relocated_relative_skip_cases_preserve_original_targets':'all320_relocated_relative_skip_cases_preserve_original_targets',
        'all21_relocated_predicate_pairs_preserve_source_operands_and_results':'all15_relocated_predicate_pairs_and_one_event319_query_preserve_source_operands_results_and_mapped_cursor',
        'all8_actor_style_objects64_slots56_strings_aliases_and_virtual_D0_storage_verified':'all6_actor_style_objects48_slots34_strings_aliases_and_actual5_virtual_prefixes_verified',
        'all5_three_option_menu_objects15_labels_preserve_source_indices012_and_cancel':'unowned1886byte_copy_preserved_and_original_VM_return_before_copy_verified',
        "_require(mapping['original_event_queries']==[],'unexpected event-query contract')":"_require(len(mapping['original_event_queries'])==1 and mapping['original_event_queries'][0]['event']==319,'event319 query contract required')\n    _require(mapping.get('no_player_choice_objects') is True and mapping.get('all116_active_speech_targets_and148_physical_speeches_preserved') is True and mapping.get('canonical_Maria_SC3_B97_32_targets_still_pending_uncredited') is True,'active/physical/canonical scope contract differs')",
        'individual_selected_Shrines_Temples_visits_not_required_for_reusable_rules':'individual_selected_B111_B119_visits_not_required_for_reusable_rules',
        'current4100_original_D0_roles_all56_bodies_all64_aliases_and_all207_catalog_styles_bound':'current4100_actual5_prefixes_all34_bodies_all48_aliases_and_all207_catalog_styles_bound',
        "        and len(representative.get('three_option_distinct_count_geometry_and_result_tests',[]))==5\n":"",
        "        and representative.get('actual_three_option_menu_gameplay_coverage')==[]\n":"",
        'actual_selected_Shrines_Temples_IDs':'actual_selected_B111_B119_IDs',
        "doc['native_formatter_module']=='dk4tool/dialogue/lil_B111_B119_layout_v2.py'":"Path(doc['native_formatter_module'])==Path('dk4tool/dialogue/lil_B111_B119_layout_v2.py')",
        "len(FE['cases'])==30":"len(FE['cases'])==1",
        'all30_one_native_page_consumes_complete_target':'all1_one_native_page_consumes_complete_target',
        'all30_complete_native_independent_planes_all_glyphs_and_canaries_equal':'all1_complete_native_independent_planes_all_glyphs_and_canaries_equal',
        'all30_source_unlabeled_panels_preserved_without_invented_names_or_macros':'one_source_unlabeled24000_gold_notice_preserved_without_invented_names_or_macros',
        'all21_current_relocated_predicate_results_and_source_operands_equal':'all15_predicate_and_one_query_current_relocated_results_and_source_operands_equal',
        'all3312_pointer_cases_and_all_source_alias_groups_preserved':'all2484_pointer_cases_and_all_source_alias_groups_preserved',
        'all220_final_stored_paragraphs_reach_expected_original_consumer_and_exact_macro_text':'all150_final_stored_paragraphs_reach_expected_original_consumer_and_exact_macro_text',
        "len(doc['records'])==len(refs)==164":"len(doc['records'])==len(refs)==116",
        '164speech coverage differs':'116speech coverage differs',
        "len(voice['records'])==len(style_refs)==56":"len(voice['records'])==len(style_refs)==34",
        '56style coverage differs':'34style coverage differs',
        'len(fonts)==220':'len(fonts)==150',
        '220complete native cases required':'150complete native cases required',
        "    _require(len(menu['records'])==len({r['id'] for r in menu['records']})==15,'15choice labels required')\n":"",
        'ten exact blocks required':'nine exact blocks required',
        'sum(expected_commands.values())==421':'sum(expected_commands.values())==305',
        'used_styles=set();used_choices=set()':'used_styles=set()',
        'raw[0] in {2,9,16,20,139,151,160,177,178,191,207,208,254}':'raw[0] in {2,4,9,14,19,20,104,137,163,170,179,198,207,208,209,214,215,220,254}',
        "old[18:20]==original[at+18:at+20]==b'\\0\\xd0'":"old[18:20]==original[at+18:at+20] and old[18]==0 and old[19] in {208,209,214,215,220}",
        "row['source_selector']==208":"row['source_selector']==old[19] and row['virtual_formatter_prefix_hex']==format(old[19],'02x')",
        "_compile(b'\\xd0'+raw,row,profile,fonts[ident])":"_compile(bytes([old[19]])+raw,row,profile,fonts[ident])",
        "value[:1]==b'\\xd0'":"value[:1]==bytes([old[19]])",
        'virtual_D0_excluded_from_stored_body':'actual_virtual_prefix_excluded_from_stored_body',
        " and used_choices=={r['id'] for r in menu['records']}":'',
        "len(changes)==len({r['id'] for r in changes})==235":"len(changes)==len({r['id'] for r in changes})==150",
        "actor_styles=config['actor_styles'],choices=config['choices'],reference_map=config['reference_map']":"actor_styles=config['actor_styles'],reference_map=config['reference_map']",
        'only_SC2_selected_ten_blocks_changed':'only_SC2_selected_nine_blocks_changed',
        'all326_other_SC2_blocks_unchanged':'all327_other_SC2_blocks_unchanged',
        'all164_speeches56_style_alternatives15_choice_labels114_relative_operands_verified':'all116_speeches34_style_alternatives_no_choices64_relative_operands_verified',
        'all64_style_slots_aliases_and_virtual_D0_storage_verified':'all48_style_slots_aliases_and_actual5_virtual_prefix_storage_verified',
        'all5_three_option_menu_counts_indices012_and_cancel_verified':'unowned1886byte_copy_preserved_and_canonicalMaria32_uncredited'}
    for a,b in swaps.items():assert a in t,a;t=t.replace(a,b)
    anchor="    refs={r['id']:r for b in mapping['blocks'] for r in b['text_records']}"
    assert t.count(anchor)==1
    t=t.replace(anchor,"""    copy=load(doc['unowned_copy_proof'])
    _require(sha(Path(doc['unowned_copy_proof']).read_bytes())==doc['unowned_copy_proof_sha256']==mapping['unowned_copy_proof_sha256']
        and copy.get('all32_unowned_copy_speeches_byte_exact_and_unreachable_from_ordinary_Lil_entry') is True
        and len(copy['original_VM_return_cases'])==2,'moved original return/copy proof required')
    _require(controls.get('original_query_r0_r1_r2_and_mapped_incidental_r3_cursor_exact') is True,'mapped query cursor approval required')
"""+anchor)
    anchor="        _require(sha(target)==spec['target_block_sha256'],'complete target block differs')"
    assert t.count(anchor)==1
    t=t.replace(anchor,"""        if n==115:
            unowned=spec['unowned_appended_copy'];a=unowned['old_offset'];z=unowned['new_offset'];size=unowned['bytes']
            _require(a==440 and size==1886 and z==_mapped(patches,a) and end-a==size
                and block[a:end]==target[z:z+size] and sha(target[z:z+size])==unowned['sha256']
                and target[z-4:z]==bytes(4) and copy['unowned_copy']==unowned
                and copy['conservative_relocated_prefix_graph']['reachable_return0_commands']==[z-4]
                and not any(p>=z for p in copy['conservative_relocated_prefix_graph']['reachable_commands']),
                'unowned copy or mapped original return changed')
"""+anchor)
    # No player-choice patch can be created by this compiler.
    a=t.index("            else:\n                a=_mapped(patches,r['choice_command_offset'])")
    z=t.index('        restored=bytearray(logical)',a)
    t=t[:a]+"            else:raise ValueError('Unexpected ownership kind')\n"+t[z:]
    compile(t,str(NEW),'exec');NEW.write_text(t,encoding='utf-8');ROOT.mkdir(parents=True)
    save(ROOT/'guarded_compiler_provenance.json',dict(previous=str(OLD),previous_sha256=sha(OLD.read_bytes()),successor=str(NEW),successor_sha256=sha(NEW.read_bytes()),no_previous_release_stage_or_global_helper_modified=True,all_actual_variable_prefixes_unowned_copy_query_and_physical_source_scope_guarded=True,compiler_registration_negatives_and_release_pending=True,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    print('Guarded150-target compiler prepared;registration/negative controls/registered build still required.')
