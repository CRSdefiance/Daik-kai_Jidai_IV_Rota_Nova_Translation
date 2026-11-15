"""Prepare one-block reference,whole-loader,entry-census and single-end proofs."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/lil_B197_research_tools_v5676')
PARENT=Path('out/all_routes_combined_v5637_candidate.nds')
ROM=Path('out/lil_B197_reference_v5677_RESEARCH_ONLY.nds')
PLAN=Path('work/analysis/lil_B197_relocation_v5671/nested_source_relocation_research.json')
if __name__=='__main__':
    assert not ROOT.exists()
    menu='work/analysis/lil_B197_stored_choices_v5673/one_final_typed_object_three_exact_references_and_both_even_alignments.json'
    shared={'B196':'B197','prepare_lil_B196_research_v5618':'prepare_lil_B197_research_v5676'}
    rows=[derive('scripts/create_lil_B196_reference_v5619.py','scripts/create_lil_B197_reference_v5677.py',{
        **shared,'V5580':'V5637','research_v5619':'research_v5677','stored_v5616':'stored_v5672','all24':'all21','targets96':'targets84',
        'verification_v5614':'verification_v5675',
        "stored['current_final_stored_macro_alignment_cases']==96":"stored['current_final_stored_macro_alignment_cases']==84",
        'current_final_stored_macro_alignment_cases=96':'current_final_stored_macro_alignment_cases=84','==[196]':'==[197]',
        'work/analysis/lil_B196_stored_choices_v5617/six_final_typed_objects_twelve_references_and_both_even_alignments.json':menu,
        "menus['all_six_stored_objects_and_twelve_actual_offsets_record_indices_labels_and_counts_exact']":"menus['source_count3_option_order_and_original_selection_cancel_results_preserved'] and len(menus['actual_target_record_references'])==3",
        "menus['fresh_count_calls']==12 and menus['fresh_label_pointer_calls']==24":"menus['fresh_count_calls']==2 and menus['fresh_label_pointer_calls']==6",
        'all6_stored_menus12_labels_bound_before_ROM_mutation':'all1_stored_menu3_labels_bound_before_ROM_mutation',
        "    assert all(Path(v['path']).resolve()!=ROM.resolve() for v in values)":"    (ROOT/'pins.before.json').write_bytes(old)\n    assert all(Path(v['path']).resolve()!=ROM.resolve() for v in values)"})]
    rows.append(derive('scripts/verify_lil_B196_loader_v5620.py','scripts/verify_lil_B197_loader_v5678.py',{
        **shared,'V5580':'V5637','loader_v5620':'loader_v5678','research_v5619':'research_v5677',
        'work/analysis/lil_B195_loader_v5565/whole_SC2_and_B195_initial_entry_proof.json':
        'work/analysis/lil_B196_loader_v5620/whole_SC2_and_B196_initial_entry_proof.json'}))
    rows.append(derive('scripts/verify_lil_B196_references_v5621.py','scripts/verify_lil_B197_references_v5679.py',{
        **shared,'119-command/52-span':'39-command/6-span','reference_census_v5621':'reference_census_v5679','loader_v5620':'loader_v5678',
        '[196]':'[197]','0x2100':'0x2200',
        "sum(len(r['mapped_commands'])for r in result)==119":"sum(len(r['mapped_commands'])for r in result)==39",
        "sum(r['typed_relative_span_count']for r in result)==52":"sum(r['typed_relative_span_count']for r in result)==6",
        "sum(r['target_native_skip_cases']for r in result)==260":"sum(r['target_native_skip_cases']for r in result)==30",
        'all119_commands52_relative_sites':'all39_commands6_relative_sites','all119_clean_current_target_commands_and52_relative_sites':'all39_clean_current_target_commands_and6_relative_sites',
        'native_commands_each=119,relative_sites=52,target_native_skip_cases=260':'native_commands_each=39,relative_sites=6,target_native_skip_cases=30'}))
    rows.append(derive('scripts/prove_lil_B196_ends_v5622.py','scripts/prove_lil_B197_ends_v5680.py',{
        **shared,'ends_v5622':'ends_v5680','all seven declared endwords per image,including six non-tail endings':'the single original common-tail endword per image',
        '(7 if n==196 else 1)':'1',
        "len(cases)==14 and sum(not c['at_logical_tail'] for c in cases)==12":"len(cases)==2 and all(c['at_logical_tail'] for c in cases)",
        'fourteen_declared_end_decodes_and_all52_in_block_relative_destinations':'two_declared_end_decodes_and_all6_in_block_relative_destinations',
        'all14_declared_end_decodes_return':'all2_declared_end_decodes_return',
        'B196_all_six_nontail_ends_precede_declared_logical_end':'B197_single_end_completes_declared_logical_payload',
        'all_seven_B196_declared_word_decoder_probes_not_actual_reachability_claim':'both_B197_declared_word_decoder_probes_not_actual_reachability_claim',
        'Fourteen declared current/target endwords':'Two declared current/target endwords','all seven words preserved':'single common end preserved'}))
    ROOT.mkdir(parents=True);save(ROOT/'prepared_tools.json',dict(tools=rows,parent=str(PARENT),research=str(ROM),plan=str(PLAN),
        source_stored_logical=[880,878],target_stored_logical=[1004,1002],source_tailzeros=2,target_tailzeros=2,
        commands=39,speeches=21,progressive=20,FE=1,FI=0,menus=1,labels=3,relative_sites=6,predicates=0,ends=1,
        stored_menu_proof=menu,parent_loader_reuse_requires_exact_whole_ROM_hash=True,
        new_emulator_runs=0,new_review_credit=0,full_goal_complete=False))
