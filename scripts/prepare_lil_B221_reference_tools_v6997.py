"""Prepare the pinned reference and fresh resized-archive/caller checks with exact current reuse."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import checked_text,derive
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/lil_B221_reference_tools_v6997')
if __name__=='__main__':
    assert not ROOT.exists()
    jobs=[
        ('scripts/create_lil_B220_reference_v6942.py','scripts/create_lil_B221_reference_v6997.py',{
            'B220':'B221','reference_v6942':'reference_v6997','reference_v6942_RESEARCH_ONLY':'reference_v6997_RESEARCH_ONLY',
            'relocation_v6940/all17_objects20_commands_full1280_inverse_RESEARCH':
            'relocation_v6994/all16_objects21_commands_four_relatives_full1208_inverse_RESEARCH',
            'stored_v6941/all17_final_stored_targets68_alignments17_complete_pages':
            'stored_v6995/all14_final_stored_targets56_alignments16_complete_pages',
            'v6910':'v6956','V6910':'V6956','[220]':'[221]',
            '    parent,image=NdsImage.open(PARENT),NdsImage.open(PARENT);data=':
            "    menus=read('work/analysis/lil_B221_stored_choices_v6996/one_final_typed_object_two_references_and_both_even_alignments.json');assert menus['relocation_plan_sha256']==sha(PLAN.read_bytes()) and menus['candidate_sha256']==digest and menus['one_stored_object_and_two_actual_offsets_record_indices_labels_and_counts_exact'] and menus['fresh_count_calls']==2 and menus['fresh_label_pointer_calls']==4\n    assert stored['complete_native_pages']==sum(len(r['complete_pages']['pages']) for r in stored['records'])==16\n    parent,image=NdsImage.open(PARENT),NdsImage.open(PARENT);data=",
            'seventeen whole-exchange speeches,seventeen native pages,zero macros,no relatives/predicates/typed controls,original A000,C200 and normal end;all1280 predecessor bytes reversible':
            'fourteen whole-exchange speeches/two response labels,sixteen native pages,zero macros,four relatives/one typed menu,original A000 and normal end;all1208 predecessor bytes reversible'}),
        ('scripts/verify_lil_B220_loader_v6943.py','scripts/verify_lil_B221_loader_v6998.py',{
            'B220':'B221','loader_v6943':'loader_v6998','reference_v6942':'reference_v6997',
            'lil_B218_loader_v6897/whole_SC2_and_B218_initial_entry_proof':
            'lil_B220_loader_v6943/whole_SC2_and_B220_initial_entry_proof',
            'V6910':'V6956','1276_bytes':'1224_bytes'}),
        ('scripts/verify_lil_B220_references_v6944.py','scripts/verify_lil_B221_references_v6999.py',{
            'B220':'B221','reference_v6942':'reference_v6997','reference_census_v6944':'reference_census_v6999',
            'loader_v6943':'loader_v6998',
            'lil_B218_reference_census_v6898/all15_commands_no_relative_or_typed_sites_and_shipped_census':
            'lil_B220_reference_census_v6944/all20_commands_no_relative_or_typed_sites_and_shipped_census',
            '[220]':'[221]','block=220':'block=221','len(w)==20':'len(w)==21',
            "len(spec['relative_skip_fixups'])==0":"len(spec['relative_skip_fixups'])==4",
            "len(spec['target_native_skip_cases'])==0":"len(spec['target_native_skip_cases'])==20",
            "len(spec['choice_commands'])==0":"len(spec['choice_commands'])==1",
            "len(spec['text_records'])==17":"len(spec['text_records'])==14",
            'all20_commands_no_relative_or_typed_sites_and_shipped_census':'all21_commands_four_relatives_one_menu_and_shipped_census',
            'all20_clean_current_target_commands_bound':'all21_clean_current_target_commands_bound',
            'typed_choice_count=0':'typed_choice_count=1','typed_relative_span_count=0':'typed_relative_span_count=4',
            'target_native_skip_cases=0':'target_native_skip_cases=20',
            'All20 commands/no relatives,predicates or typed styles/A000/C200/normal end':
            'All21 commands/four relatives/one typed menu/A000/normal end',
            'Bind all20 mapped commands':'Bind all21 mapped commands'}),
    ]
    for source,target,changes in jobs:
        assert not Path(target).exists();checked_text(Path(source).read_text('utf-8'),changes)
    rows=[derive(source,target,changes) for source,target,changes in jobs]
    stored_path=Path('work/analysis/lil_B221_stored_v6995/all14_final_stored_targets56_alignments16_complete_pages.json')
    stored=read(stored_path);actual_pages=sum(len(r['complete_pages']['pages']) for r in stored['records'])
    assert actual_pages==stored['complete_native_pages']==16
    ROOT.mkdir(parents=True)
    save(ROOT/'exact_reference_loader_caller_successors_and_stored_console_count_erratum.json',dict(derivations=rows,
        stored_proof=str(stored_path),stored_proof_sha256=sha(stored_path.read_bytes()),
        authoritative_stored_native_page_count=actual_pages,
        inherited_console_only_complete_pages17_is_superseded_by_bound_proof_count16=True,
        stored_proof_was_already_correct_no_native_checks_repeated_for_reporting_typo=True,
        current_V6956_whole_ROM_matches_prior_B220_reference_and_loader_proof=True,
        fresh_target_archive_and_caller_checks_required=True,
        no_new_ROM_or_credit_from_preparation=True,full_goal_complete=False))
    print('Reference/loader/caller tools prepared. Stored proof has16 pages; inherited console17 was reporting only.')
