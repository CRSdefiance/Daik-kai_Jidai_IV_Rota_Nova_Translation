"""Source-lock one whole-image B50 atomic stage to every approved native and actual guard."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save

if __name__=='__main__':
    root=Path('work/analysis/Hodram_B50_atomic_tools_v8537');assert not root.exists()
    path=Path('dk4tool/patch/hodram_B49_editorial_v2.py');source=path.read_text(encoding='utf-8')
    a=source.index("    dependency=conf['required_registered_Gerhard_dependency']");b=source.index('    archive=image.read_file(PATH)',a)
    dependency="""    dependency=conf['required_registered_stack_dependency'];slot=data['Gerhard_reference']['only_changed_name_span'];arm=image.read_file('/__arm9__.bin');at=slot['offset']
    require(dependency==seal['required_registered_stack_dependency'] and dependency['predecessor_profile']=='all-routes-unified-v8475' and dependency['predecessor_ROM_sha256']==conf['parent_ROM_sha256'] and dependency['name_span']==slot,'explicit registered V8475/Adernkatz/B49 dependency')
    require(slot['bytes']==12 and arm[at:at+12].hex()==slot['target_hex'] and arm[at+12:at+20]==b'Blades\\0\\0' and sha(arm)==data['Gerhard_release']['ARM9_sha256']==data['predecessor_release']['ARM9_sha256'],'complete12byte registered surname andfollowing8byte name preserved')
    for key,path in [('correction','translations/gerhard_surname_editorial_release_v2.json'),('registered_B49','translations/hodram_B49_editorial_release_v3.json'),('compatible_B49','translations/hodram_B49_editorial_release_v4.json'),('compatible_outcomes','translations/hodram_outcomes_editorial_release_v6.json')]:
        require(Path(dependency[key]).resolve()==Path(path).resolve() and sha(Path(path).read_bytes())==dependency[key+'_sha256'],'exact registered/compatible predecessor configuration:'+key)
    require(data['predecessor_release']['profile']=='all-routes-unified-v8475' and data['predecessor_release']['candidate_sha256']==conf['parent_ROM_sha256'] and data['predecessor_release']['all643_manifest_batches_and114_accepted_layers_present'],'entire registered V8475 predecessor stack')
    require(data['predecessor_compatibility']['whole_registered_V8475_ROM_byte_exact'] and data['predecessor_compatibility']['current_V8475_sha256']==conf['parent_ROM_sha256'] and data['predecessor_compatibility']['all_native_semantic_production_gates_enabled'],'compatible predecessors reproduce whole V8475')
    require(data['builder_support']['all524_prior_outcomes_dependencies_retained_exact'] and data['builder_support']['all663_prior_B49_dependencies_retained_exact'] and data['builder_validation']['negative_count']==16,'all old dependency entries andmeaningful additive-builder rejections')
"""
    result=derive(str(path),'dk4tool/patch/hodram_B50_editorial_v1.py',{
        'hodram_outcomes_builder_guard_v5':'hodram_outcomes_builder_guard_v6',
        'hodram_B49_profile_v2':'hodram_B50_profile_v2','hodram_B49_layout_v2':'hodram_B50_layout_v2','hodram_B49_names_v2':'hodram_B50_names_v2',
        'from dk4tool.dialogue.hodram_B49_choices_v2 import compile_choices\n':'',
        'hodram_B49_references_v1':'hodram_B50_references_v1','hodram_B49_native_evidence_v1':'hodram_B50_native_evidence_v1','hodram_B49_actual_evidence_v2':'hodram_B50_actual_evidence_v1',
        'from dk4tool.patch.hodram_B49_menu_evidence_v1 import check_menu_actual\n':'',
        'hodram_B49_FE_evidence_v1':'hodram_B50_FE_evidence_v1','hodram_B49_comparison_v1':'hodram_B50_comparison_v1','hodram_B49_controls_v3':'hodram_B50_controls_v1','hodram_B49_loaders_v1':'hodram_B50_loaders_v1',
        'scripts.Hodram_B49_release_paths_v8450':'scripts.Hodram_B50_release_paths_v8537',
        'dk4-Hodram-B49-editorial-release-v1':'dk4-Hodram-B50-editorial-release-v1',
        "len(policy['positive_speech_compilers'])==14 and policy['positive_editorial_units']==16 and policy['negative_count']==len(policy['negative_cases'])==838":"len(policy['positive_speech_compilers'])==3 and policy['positive_editorial_units']==3 and policy['negative_count']==len(policy['negative_cases'])==182",
        '14speech/twochoice positives and838meaningful policy rejections':'3speech/nochoice positives and182meaningful policy rejections',
        source[a:b]:dependency,
        'bank[49]':'bank[50]',
        "    require(compile_choices(doc['typed_choice_records']).hex()==frozen['choice_object_hex'],'exact original-count two-choice native menu')\n":'',
        "doc['records']+doc['typed_choice_records']":"doc['records']",
        'sixteen sealed exact source/current/final references':'three sealed exact source/current/final references',
        'menu=check_menu_actual(data,doc,image,clean,load,require);FE=':'FE=',
        "scope['complete_page_occurrences']==34 and scope['complete_body_name_orabsent_FE_header_holds']==200":"scope['complete_page_occurrences']==6 and scope['complete_body_name_orabsent_FE_header_holds']==50",
        "approval['all16_five_gates_true'] and approval['all14_sheets_directly_viewed'] and doc['total_actual_frames']==scope['total_actual_frames']==69868":"approval['all3_five_gates_true'] and approval['measured_limits']['all_three_sheets_directly_viewed'] and doc['total_actual_frames']==scope['total_actual_frames']==20002 and data['gate_metadata_approval']['manuscript_sha256']==sha(DOC.read_bytes())",
        "approval['directly_viewed_sheets']":"approval['measured_limits']['directly_viewed_sheets']",
        "block=49,kind='typed-choice' if r in doc['typed_choice_records'] else frozen['record_bindings'][r['id']]['consumer']":"block=50,kind=frozen['record_bindings'][r['id']]['consumer']",
        'all36_commands14_preambles8_relatives2_choices_query_effects_ends_andtails_preserved':'all12_commands3_preambles_zero_relative_query_choice_sites_effects_ends_andtails_preserved',
        'explicit_registered_V8377_Adernkatz_dependency_preserved':'explicit_registered_V8475_Adernkatz_B49_dependency_preserved',
        'actual_summary=actual[\'summary\'],menu=menu,original_FE=FE':"actual_summary=actual['summary'],original_FE=FE",
        'B49 exchange':'B50 exchange','Hodram B49 atomic contract:':'Hodram B50 atomic contract:',
    })
    root.mkdir(parents=True);save(root/'derivation.json',dict(tool=result,all_native_high_integer_constants_andmultiplicity_preserved=True,all_source_runtime_compiler_QA_reference_native_actual_FE_controls_loaders_comparison_whole_ROM_inverse_guards_preserved=True,one_complete_image_dot_rom_commit_only_after_all_gates=True,no_builder_registry_ROM_orcredit_change=True,new_credit=0,full_goal_complete=False))
