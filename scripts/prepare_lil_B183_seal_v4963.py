"""Derive B183 sealing from the linear contract with measured actual differences."""
from pathlib import Path
from scripts.prepare_lil_B156_layout_v3705 import derive
from scripts.verify_village_wrap_v608 import save

ROOT=Path('work/analysis/lil_B183_seal_tools_v4963')
if __name__=='__main__':
    assert not ROOT.exists()
    tool=derive('scripts/seal_lil_B181_references_v4864.py','scripts/seal_lil_B183_references_v4963.py',{
        'B181':'B183','prepare_lil_B181_research_v4851':'prepare_lil_B183_research_v4949',
        'reference_approval_v4864':'reference_approval_v4963','editorial_manuscript_v3':'editorial_manuscript_v7','editorial_manuscript_v4':'editorial_manuscript_v8',
        'reference_census_v4854':'reference_census_v4952','relocated_controls_v4856':'relocated_controls_v4954','stored_v4847':'stored_v4948',
        'ends_v4855':'ends_v4953','actual_v4861':'actual_v4960','display_fixture_v4857':'display_fixture_v4957','actual_review_v4862':'actual_review_v4961',
        'all10_final_stored_targets40':'all25_final_stored_targets100','actual_all10':'actual_all25','all2_actual_sheets10':'all5_actual_sheets25',
        'all13':'all28','all10':'all25','all115':'all149','all2_actual_sheets_viewed':'all5_actual_sheets_viewed',
        'progressive9_impersonal_FE1':'progressive23_impersonal_FE2','single_end392_actual_target376':'single_end952_actual_target1050',
        'source_end392_actual_target376':'source_end952_actual_target1050',
        "len(control['relocated_dispatch_cases'])==10":"len(control['relocated_dispatch_cases'])==25",
        "stored['current_final_stored_macro_alignment_cases']==40":"stored['current_final_stored_macro_alignment_cases']==100",
        '==(12,28)':'==(64,36)',"actual['fresh_actual_unique_speech_panels']==10":"actual['fresh_actual_unique_speech_panels']==25",
        '==[22,22]':'==[37,37]','==[5257,5257]':'==[8855,8854]','all22_stored_fixture_commands':'all37_stored_fixture_commands',
        "len(f['all22_stored_fixture_commands'])==22":"len(f['all22_stored_fixture_commands'])==37",
        "len(visual['all2_actual_sheets_viewed'])==2":"len(visual['all2_actual_sheets_viewed'])==5",
        "len(visual['paired_full_screen_views'])==3":"len(visual['paired_full_screen_views'])==4",
        "visual['nontext_equal_samples']==115":"visual['nontext_equal_samples']==149",
        'dict(total=0,speech=0,control_or_end=0)':'dict(total=11,speech=9,control_or_end=2)',
        'postscene9001':'postscene11001','[790984746,790984746]':'[1228390232,713326998]',
        'len(set(ids))==10':'len(set(ids))==25',
        'all10_panels9_progressive1_FE_A000':'all25_panels23_progressive2_FE_A000',
        'original13_commands':'original28_commands',
        'all115_upper_portrait_name_samples_equal_and_no_timing_or_postscene_RGB_differences=True':'all149_upper_portrait_name_samples_and_sampled_postscene_RGB_equal=True,measured_timing_differences=visual[\'exact_timing_difference_counts\'],fixture_return_frames=visual[\'fixture_return_frames\']',
        'five_native_state_components_whole1A04_actor_captain2_and_PRNG790984746_equal=True':'five_native_state_components_whole1A04_actor_and_captain2_equal=True,unequal_PRNG_seeds=visual[\'postscene9001_PRNG_seeds\'],PRNG_equality=False',
        'total_frames=18002':'total_frames=22002',
        "checked['block']==181":"checked['block']==183","len(block['command_map'])==13":"len(block['command_map'])==28",
        "len(block['text_records'])==10":"len(block['text_records'])==25",'==[(392,376)]':'==[(952,1050)]',
        'B181 references sealed:all10 actual panels,13 source commands':'B183 references sealed:all25 actual panels,28 source commands',
    })
    ROOT.mkdir(parents=True);save(ROOT/'prepared_tools.json',dict(tool=tool,new_review_credit=0,full_goal_complete=False))
    print('Prepared B183 reference sealing with37 actual commands,25 panels,two FE and measured unequal timing/PRNG.')
