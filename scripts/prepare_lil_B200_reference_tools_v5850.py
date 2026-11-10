"""Prepare exact B200 relocation,stored-target,whole-loader and source-entry checks."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/lil_B200_reference_tools_v5850')
PARENT=Path('out/all_routes_combined_v5816_candidate.nds')
ROM=Path('out/lil_B200_reference_v5853_RESEARCH_ONLY.nds')
PLAN=Path('work/analysis/lil_B200_relocation_v5851/nested_source_relocation_research.json')
if __name__=='__main__':
    assert not ROOT.exists()
    tools=[derive('scripts/research_lil_B199_relocation_v5797.py','scripts/research_lil_B200_relocation_v5851.py',{
        'B199':'B200','relocation_v5797':'relocation_v5851','manuscript_v5.json':'manuscript_v4.json','v5756_candidate':'v5816_candidate',
        'number==199':'number==200',"end_maps[0]['source_offset']==1162":"end_maps[0]['source_offset']==926",
        "sum(len(r['text_records']) for r in results)==31":"sum(len(r['text_records']) for r in results)==19",
        "sum(len(r['command_map']) for r in results)==47":"sum(len(r['command_map']) for r in results)==31",
        "sum(len(r['original2000_pause_and_resume_maps']) for r in results)==1":"sum(len(r['original2000_pause_and_resume_maps']) for r in results)==0",
        '[199]':'[200]','all31speech':'all19speech','one_source2000_pause_and_resume_preserved=True':'no_source2000_pause_or_resume_maps=True',
        'source_FE_system_objects=1':'source_FE_system_objects=2',
        '47commands/31speech/no menu/no spans/one pause,one common end,all1168':'31commands/19speech/no menu/no spans/no2000 pause,one common end,all932'})]
    tools.append(derive('scripts/prove_lil_B199_stored_v5798.py','scripts/prove_lil_B200_stored_v5852.py',{
        'B199':'B200','stored_v5798':'stored_v5852','relocation_v5797':'relocation_v5851','manuscript_v5.json':'manuscript_v4.json',
        'voices_v5768':'voices_v5827','[2,9,22,254]':'[19,172,254]','len(cases)==31':'len(cases)==19','fresh+reused==124':'fresh+reused==76',
        "sum(c['consumer']=='FE-paper' for c in cases)==1":"sum(c['consumer']=='FE-paper' for c in cases)==2",
        'all31':'all19','targets124_macro':'targets76_macro','current_final_stored_macro_alignment_cases=124':'current_final_stored_macro_alignment_cases=76',
        'actual_English_B199_pause_two_picture_layouts_and_end_reachability_unexecuted':'actual_English_B200_inn_picture_gift_stat_and_end_reachability_unexecuted',
        'stored_targets=31,progressive=30,FE=1,macro_cases=124':'stored_targets=19,progressive=17,FE=2,macro_cases=76'}))
    shared={'B199':'B200','prepare_lil_B199_reference_tools_v5796':'prepare_lil_B200_reference_tools_v5850'}
    tools.append(derive('scripts/create_lil_B199_reference_v5800.py','scripts/create_lil_B200_reference_v5853.py',{
        **shared,'V5756':'V5816','research_v5800':'research_v5853','stored_v5798':'stored_v5852','all31':'all19','targets124':'targets76',
        'verification_v5795':'verification_v5842',"stored['current_final_stored_macro_alignment_cases']==124":"stored['current_final_stored_macro_alignment_cases']==76",
        'current_final_stored_macro_alignment_cases=124':'current_final_stored_macro_alignment_cases=76','==[199]':'==[200]'}))
    tools.append(derive('scripts/verify_lil_B199_loader_v5801.py','scripts/verify_lil_B200_loader_v5854.py',{
        **shared,'V5756':'V5816','loader_v5801':'loader_v5854','research_v5800':'research_v5853',
        'work/analysis/lil_B198_loader_v5734/whole_SC2_and_B198_initial_entry_proof.json':
        'work/analysis/lil_B199_loader_v5801/whole_SC2_and_B199_initial_entry_proof.json'}))
    tools.append(derive('scripts/verify_lil_B199_references_v5802.py','scripts/verify_lil_B200_references_v5855.py',{
        **shared,'reference_census_v5802':'reference_census_v5855','loader_v5801':'loader_v5854','[199]':'[200]',
        '47-command/no-relative-site':'31-command/no-relative-site',"sum(len(r['mapped_commands'])for r in result)==47":"sum(len(r['mapped_commands'])for r in result)==31",
        'all47':'all31','native_commands_each=47':'native_commands_each=31'}))
    tools.append(derive('scripts/prove_lil_B199_ends_v5803.py','scripts/prove_lil_B200_ends_v5856.py',{
        **shared,'ends_v5803':'ends_v5856','n==199':'n==200'}))
    ROOT.mkdir(parents=True);save(ROOT/'source_locked_reference_tools.json',dict(tools=tools,parent=str(PARENT),research=str(ROM),plan=str(PLAN),
        source_commands=31,source_speeches=19,source_relative_sites=0,source_pause_sites=0,source_tailzeros=2,
        one_original_end_two_FE_no_choices_styles_predicates_or_C200=True,source_native_constants_and_multiplicity_preserved=True,
        no_new_ROM_emulator_run_or_review_credit=True,full_goal_complete=False))
    print('Six B200 reference tools prepared;31 commands/19 speech objects/two FE/zero spans and pauses/two tailzeros. Native constants exact.')
