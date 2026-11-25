"""Prepare B196 whole-image loading, entry census and seven-end guards."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save

ROOT=Path('work/analysis/lil_B196_research_tools_v5618')
PARENT=Path('out/all_routes_combined_v5580_candidate.nds')
ROM=Path('out/lil_B196_reference_v5619_RESEARCH_ONLY.nds')
PLAN=Path('work/analysis/lil_B196_relocation_v5615/nested_source_relocation_research.json')
if __name__=='__main__':
    assert not ROOT.exists()
    shared={'B195':'B196','prepare_lil_B195_research_v5563':'prepare_lil_B196_research_v5618'}
    menu="work/analysis/lil_B196_stored_choices_v5617/six_final_typed_objects_twelve_references_and_both_even_alignments.json"
    rows=[derive('scripts/create_lil_B195_reference_v5564.py','scripts/create_lil_B196_reference_v5619.py',{
        **shared,'V5531':'V5580','research_v5564':'research_v5619','stored_v5562':'stored_v5616',
        'all20':'all24','targets80':'targets96','verification_v5560':'verification_v5614',
        "stored['current_final_stored_macro_alignment_cases']==80":"stored['current_final_stored_macro_alignment_cases']==96",
        'current_final_stored_macro_alignment_cases=80':'current_final_stored_macro_alignment_cases=96','==[195]':'==[196]',
        '    parent,image=NdsImage.open(PARENT),NdsImage.open(PARENT)':
        "    menus=read('"+menu+"')\n    assert menus['candidate_sha256']==digest and menus['relocation_plan_sha256']==sha(PLAN.read_bytes())\n    assert menus['all_six_stored_objects_and_twelve_actual_offsets_record_indices_labels_and_counts_exact']\n    assert menus['fresh_count_calls']==12 and menus['fresh_label_pointer_calls']==24\n    parent,image=NdsImage.open(PARENT),NdsImage.open(PARENT)",
        'registered_candidate=False,':"stored_menu_proof='"+menu+"',stored_menu_proof_sha256=sha(Path('"+menu+"').read_bytes()),all6_stored_menus12_labels_bound_before_ROM_mutation=True,registered_candidate=False,"})]
    rows.append(derive('scripts/verify_lil_B195_loader_v5565.py','scripts/verify_lil_B196_loader_v5620.py',{
        **shared,'V5531':'V5580','loader_v5565':'loader_v5620','research_v5564':'research_v5619',
        'work/analysis/lil_B194_loader_v5510/whole_SC2_and_B194_initial_entry_proof.json':
        'work/analysis/lil_B195_loader_v5565/whole_SC2_and_B195_initial_entry_proof.json'}))
    typed={'B164':'B196','prepare_lil_B164_research_v3988':'prepare_lil_B196_research_v5618'}
    rows.append(derive('scripts/verify_lil_B164_references_v3990.py','scripts/verify_lil_B196_references_v5621.py',{
        **typed,'61-command/4-span':'119-command/52-span','reference_census_v3990':'reference_census_v5621',
        'loader_v3989':'loader_v5620','[164]':'[196]',
        "sum(len(r['mapped_commands'])for r in result)==61":"sum(len(r['mapped_commands'])for r in result)==119",
        "sum(r['typed_relative_span_count']for r in result)==4":"sum(r['typed_relative_span_count']for r in result)==52",
        "sum(r['target_native_skip_cases']for r in result)==20":"sum(r['target_native_skip_cases']for r in result)==260",
        'all61_commands4_relative_sites':'all119_commands52_relative_sites','all61_clean_current_target_commands_and4_relative_sites':'all119_clean_current_target_commands_and52_relative_sites',
        'native_commands_each=61,relative_sites=4,target_native_skip_cases=20':'native_commands_each=119,relative_sites=52,target_native_skip_cases=260'}))
    rows.append(derive('scripts/prove_lil_B164_ends_v3991.py','scripts/prove_lil_B196_ends_v5622.py',{
        **typed,'ends_v3991':'ends_v5622','both declared endwords per image,including both separated advice endwords':'all seven declared endwords per image,including six non-tail endings',
        '(2 if n==164 else 1)':'(7 if n==196 else 1)',
        "len(cases)==4 and sum(not c['at_logical_tail'] for c in cases)==2":"len(cases)==14 and sum(not c['at_logical_tail'] for c in cases)==12",
        'four_declared_end_decodes_and_all4_in_block_relative_destinations':'fourteen_declared_end_decodes_and_all52_in_block_relative_destinations',
        'all4_declared_end_decodes_return':'all14_declared_end_decodes_return',
        'B164_first_end_precedes_second_end_and_declared_logical_end':'B196_all_six_nontail_ends_precede_declared_logical_end',
        'second_B164_declared_word_decoder_probe_not_actual_reachability_claim':'all_seven_B196_declared_word_decoder_probes_not_actual_reachability_claim',
        'Four declared current/target endwords':'Fourteen declared current/target endwords','bothwords preserved':'all seven words preserved'}))
    ROOT.mkdir(parents=True);save(ROOT/'prepared_tools.json',dict(tools=rows,parent=str(PARENT),research=str(ROM),plan=str(PLAN),
        source_stored_logical=[1816,1814],target_stored_logical=[1668,1668],source_tailzeros=2,target_tailzeros=0,
        commands=119,speeches=24,progressive=23,FE=1,FI=1,menus=6,labels=12,relative_sites=52,predicates=7,ends=7,
        stored_menu_proof=menu,parent_loader_reuse_requires_exact_whole_ROM_hash=True,
        new_emulator_runs=0,new_review_credit=0,full_goal_complete=False))
