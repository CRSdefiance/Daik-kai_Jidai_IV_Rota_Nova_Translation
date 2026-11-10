"""Derive the B51 complete-object atomic stage without changing native constants."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save

ROOT=Path('work/analysis/Hodram_B51_atomic_tools_v8602')
if __name__=='__main__':
    assert not ROOT.exists()
    source=Path('dk4tool/patch/hodram_B50_editorial_v1.py').read_text(encoding='utf-8')
    a=source.index("    for key,path in [('correction'")
    b=source.index('    archive=image.read_file(PATH)',a)
    predecessors="""    for key,path in [('correction','translations/gerhard_surname_editorial_release_v2.json'),('registered_B49','translations/hodram_B49_editorial_release_v4.json'),('registered_B50','translations/hodram_B50_editorial_release_v1.json'),('compatible_B49','translations/hodram_B49_editorial_release_v5.json'),('compatible_B50','translations/hodram_B50_editorial_release_v2.json'),('compatible_outcomes','translations/hodram_outcomes_editorial_release_v7.json')]:
        require(Path(dependency[key]).resolve()==Path(path).resolve() and sha(Path(path).read_bytes())==dependency[key+'_sha256'],'exact registered/compatible predecessor configuration:'+key)
    require(data['predecessor_release']['profile']=='all-routes-unified-v8543' and data['predecessor_release']['candidate_sha256']==conf['parent_ROM_sha256'] and data['predecessor_release']['all644_manifest_batches_and114_accepted_layers_present'],'entire registered V8543 predecessor stack')
    require(data['predecessor_compatibility']['whole_registered_V8543_ROM_byte_exact'] and data['predecessor_compatibility']['current_V8543_sha256']==conf['parent_ROM_sha256'] and data['predecessor_compatibility']['all_native_semantic_production_gates_enabled'],'compatible predecessors reproduce whole V8543')
    require(data['builder_support']['all535_prior_outcomes_dependencies_retained_exact'] and data['builder_support']['all675_prior_B49_dependencies_retained_exact'] and data['builder_support']['all756_prior_B50_dependencies_retained_exact'] and data['builder_validation']['negative_count']==25 and len(data['builder_validation']['positives'])==5,'all old dependency entries andmeaningful additive-builder rejections')
"""
    result=derive('dk4tool/patch/hodram_B50_editorial_v1.py','dk4tool/patch/hodram_B51_editorial_v1.py',{
        source[a:b]:predecessors,
        'hodram_outcomes_builder_guard_v6':'hodram_outcomes_builder_guard_v7',
        'hodram_B50_profile_v2':'hodram_B51_profile_v1','hodram_B50_layout_v2':'hodram_B51_layout_v1','hodram_B50_names_v2':'hodram_B51_names_v1',
        'hodram_B50_references_v1':'hodram_B51_references_v1','hodram_B50_native_evidence_v1':'hodram_B51_native_evidence_v1',
        'hodram_B50_actual_evidence_v1':'hodram_B51_actual_evidence_v1',
        'from dk4tool.patch.hodram_B50_FE_evidence_v1 import check_FE_geometry\n':'',
        'hodram_B50_comparison_v1':'hodram_B51_comparison_v1','hodram_B50_controls_v1':'hodram_B51_controls_v1','hodram_B50_loaders_v1':'hodram_B51_loaders_v1',
        'scripts.Hodram_B50_release_paths_v8537':'scripts.Hodram_B51_release_paths_v8595',
        'dk4-Hodram-B50-editorial-release-v1':'dk4-Hodram-B51-editorial-release-v1',
        "len(policy['positive_speech_compilers'])==3 and policy['positive_editorial_units']==3 and policy['negative_count']==len(policy['negative_cases'])==182":"len(policy['positive_speech_compilers'])==5 and policy['positive_editorial_units']==5 and policy['negative_count']==len(policy['negative_cases'])==322",
        '3speech/nochoice positives and182meaningful policy rejections':'5speech/nochoice positives and322meaningful policy rejections',
        "dependency['predecessor_profile']=='all-routes-unified-v8475'":"dependency['predecessor_profile']=='all-routes-unified-v8543'",
        'explicit registered V8475/Adernkatz/B49 dependency':'explicit registered V8543/Adernkatz/B49/B50 dependency',
        'bank[50]':'bank[51]',
        'three sealed exact source/current/final references':'five sealed exact source/current/final references',
        'FE=check_FE_geometry(data,image,native,load,require);comparison=':'comparison=',
        "scope['complete_page_occurrences']==6 and scope['complete_body_name_orabsent_FE_header_holds']==50":"scope['complete_page_occurrences']==8 and scope['complete_body_name_holds']==56 and scope['actual_unique_speech_IDs']==['DK4_MES_B51_R0006','DK4_MES_B51_R0010','DK4_MES_B51_R0014','DK4_MES_B51_R0039'] and scope['unvisited_conditional_text_IDs']==['DK4_MES_B51_R0032']",
        "approval['all3_five_gates_true']":"approval['all5_five_gates_true']",
        "data['gate_metadata_approval']['manuscript_sha256']==sha(DOC.read_bytes())":"approval['manuscript_sha256']==sha(DOC.read_bytes()) and approval['names_sha256']==sha(NAMES.read_bytes())",
        'block=50,kind=':'block=51,kind=',
        'all12_commands3_preambles_zero_relative_query_choice_sites_effects_ends_andtails_preserved':'all20_commands5_preambles8_relatives2_queries_nochoices_opaque_controls_ends_andtails_preserved',
        'explicit_registered_V8475_Adernkatz_B49_dependency_preserved':'explicit_registered_V8543_Adernkatz_B49_B50_dependency_preserved',
        'original_FE=FE,':'',
        'B50 exchange':'B51 exchange','Hodram B50 atomic contract:':'Hodram B51 atomic contract:',
    })
    ROOT.mkdir(parents=True)
    save(ROOT/'derivation.json',dict(tool=result,all_native_high_integer_constants_andmultiplicity_preserved=True,all_source_runtime_compiler_QA_reference_native_actual_controls_loaders_comparison_whole_ROM_inverse_guards_preserved=True,one_complete_image_dot_rom_commit_only_after_all_gates=True,Charles_unvisited_andall_measured_limits_preserved=True,no_builder_registry_ROM_orcredit_change=True,new_credit=0,full_goal_complete=False))
