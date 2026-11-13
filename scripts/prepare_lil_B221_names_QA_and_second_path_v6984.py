"""Prepare exact current name planes, unmodified QA and an ordinary Down/A source path."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import checked_text,derive
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/lil_B221_names_QA_second_path_tools_v6984')
if __name__=='__main__':
    assert not ROOT.exists()
    common={'B220':'B221','current_V6910_native_v6920':'current_V6956_native_v6966'}
    jobs=[
        ('scripts/prove_lil_B220_name_planes_v6929.py','scripts/prove_lil_B221_name_planes_v6981.py',{
            **common,'name_planes_v6929':'name_planes_v6981',
            'native_four_distinct_name_consumers':'native_six_distinct_name_consumers',
            'len(returned)==4':'len(returned)==6','[26,199]':'[2,17,85]',
            "row['actor_ID']==199 and col['column']!=0":"row['actor_ID']==85 and col['column']!=0",
            "len(strings)==4 and set(strings)=={'Julian Lopes','Julian','Lopes','Lucia'}":
            "len(strings)==9 and set(strings)=={'Lil Argot','Lil','Argot','Al Shin','Al Ferid Shin','Al','Shin','Ferid','Square Shopkeeper'}",
            'all4_complete_name':'all9_complete_name',
            'two_actors_four_getters_four_name_component_planes16_alignments':
            'three_actors_six_getters_nine_name_component_planes36_alignments',
            'name_literal_alignment_count=16':'name_literal_alignment_count=36',
            'complete_name_component_plane_count=4':'complete_name_component_plane_count=9',
            'both_actor_forms_and_Julian_components_preserved':'all_three_actor_forms_and_Lil_Al_components_preserved',
            'Two actors/four getters:4 complete name/component planes,16 literal alignments.':
            'Three actors/six getters:9 complete name/component planes,36 literal alignments.'}),
        ('scripts/probe_lil_B220_paragraph_QA_v6932b.py','scripts/probe_lil_B221_paragraph_QA_v6982.py',{
            'B220':'B221','base_QA_v6932b':'base_QA_v6982',
            'layout_v6927b/seventeen_whole_paragraph_plans_no_macros_no_prose_changes':
            'layout_v6976b/fourteen_whole_paragraph_plans_no_macros_no_prose_changes',
            'native_pages_v6928b/all17_paragraphs17_complete_native_pages136_alignments':
            'native_pages_v6980b/all14_paragraphs16_complete_native_pages112_alignments',
            '[26,199]':'[2,17,85]','all17_base_QA':'all14_base_QA'}),
        ('scripts/run_lil_B221_source_v6979.py','scripts/run_lil_B221_source_v6979b.py',{
            'source_run_v6979':'source_run_v6979b','source_v6979\'':'source_v6979b\'',
            "save(inputs,read(base_inputs)+[dict(start=f,duration=5,buttons=['A']) for f in range(2600,15501,240)])":
            "save(inputs,sorted(read(base_inputs)+[dict(start=3700,duration=5,buttons=['Down'])]+[dict(start=f,duration=5,buttons=['A']) for f in range(2600,15501,240)],key=lambda r:r['start']))"}),
    ]
    for source,target,changes in jobs:
        assert not Path(target).exists();checked_text(Path(source).read_text('utf-8'),changes)
    rows=[derive(source,target,changes) for source,target,changes in jobs]
    ROOT.mkdir(parents=True)
    save(ROOT/'source_locked_names_unmodified_QA_and_ordinary_second_choice.json',dict(derivations=rows,
        observed_first_source_menu_frame=3730,first_source_result=[2,0],
        ordinary_second_path_Down_frame3700_before_unchanged_A_frame3800=True,
        no_choice_result_roster_RNG_funds_predicate_or_emulated_RAM_forced=True,
        source_fixture_all21_original_commands_plus9_initializers_unchanged=True,
        source_actual_menu_evidence='E:/Rota Nova translations/Generated/work/emulation_v193/lil_B221_source_v6979/frame_003730_cold_boot.png',
        second_path_selection_not_claimed_until_observed=True,new_review_credit=0,full_goal_complete=False))
    print('Three exact successors prepared; ordinary second choice must still be observed.')
