"""Prepare B199 exact relocation, stored-target, whole-loader and source-entry checks."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/lil_B199_reference_tools_v5796b')
PARENT=Path('out/all_routes_combined_v5756_candidate.nds')
ROM=Path('out/lil_B199_reference_v5800_RESEARCH_ONLY.nds')
PLAN=Path('work/analysis/lil_B199_relocation_v5797/nested_source_relocation_research.json')
if __name__=='__main__':
    assert not ROOT.exists()
    rows=[]
    assert Path('scripts/research_lil_B199_relocation_v5797.py').is_file()
    rows.append(derive('scripts/prove_lil_B195_stored_v5562.py','scripts/prove_lil_B199_stored_v5798.py',{
        'B195':'B199','stored_v5562':'stored_v5798','relocation_v5561':'relocation_v5797',
        'manuscript_v3.json':'manuscript_v5.json','voices_v5542':'voices_v5768','[92,103,119,254]':'[2,9,22,254]',
        "expanded=stored[1:]\n                assert not any(m in expanded for m in [b'FI',b'FA',b'FO'])":
        "expanded=stored[1:].replace(b'FI',b'Lil').replace(b'FA',b'Argot').replace(b'FO',b'Argot Co.')",
        'len(cases)==20':'len(cases)==31','fresh+reused==80':'fresh+reused==124','all20':'all31','targets80_macro':'targets124_macro',
        'current_final_stored_macro_alignment_cases=80':'current_final_stored_macro_alignment_cases=124',
        'actual_selected_B195_linear_A000_C200_and_end_reachability_unexecuted':'actual_English_B199_pause_two_picture_layouts_and_end_reachability_unexecuted',
        'stored_targets=20,progressive=19,FE=1,macro_cases=80':'stored_targets=31,progressive=30,FE=1,macro_cases=124'}))
    shared={'B198':'B199','prepare_lil_B198_research_v5732':'prepare_lil_B199_reference_tools_v5796'}
    rows.append(derive('scripts/create_lil_B198_reference_v5733.py','scripts/create_lil_B199_reference_v5800.py',{
        **shared,'V5692':'V5756','research_v5733':'research_v5800','stored_v5726':'stored_v5798',
        'all17':'all31','targets68':'targets124','verification_v5731':'verification_v5795',
        "stored['current_final_stored_macro_alignment_cases']==68":"stored['current_final_stored_macro_alignment_cases']==124",
        'current_final_stored_macro_alignment_cases=68':'current_final_stored_macro_alignment_cases=124','==[198]':'==[199]'}))
    rows.append(derive('scripts/verify_lil_B198_loader_v5734.py','scripts/verify_lil_B199_loader_v5801.py',{
        **shared,'V5692':'V5756','loader_v5734':'loader_v5801','research_v5733':'research_v5800',
        'work/analysis/lil_B197_loader_v5678/whole_SC2_and_B197_initial_entry_proof.json':
        'work/analysis/lil_B198_loader_v5734/whole_SC2_and_B198_initial_entry_proof.json'}))
    shared195={'B195':'B199','prepare_lil_B195_research_v5563':'prepare_lil_B199_reference_tools_v5796'}
    rows.append(derive('scripts/verify_lil_B195_references_v5566.py','scripts/verify_lil_B199_references_v5802.py',{
        **shared195,'reference_census_v5566':'reference_census_v5802','loader_v5565':'loader_v5801','[195]':'[199]',
        '23-command/no-relative-site':'47-command/no-relative-site',"sum(len(r['mapped_commands'])for r in result)==23":"sum(len(r['mapped_commands'])for r in result)==47",
        'all23':'all47','native_commands_each=23':'native_commands_each=47'}))
    rows.append(derive('scripts/prove_lil_B195_ends_v5567.py','scripts/prove_lil_B199_ends_v5803.py',{
        **shared195,'ends_v5567':'ends_v5803','n==195':'n==199'}))
    ROOT.mkdir(parents=True);save(ROOT/'source_locked_reference_tools.json',dict(tools=rows,parent=str(PARENT),research=str(ROM),plan=str(PLAN),
        source_commands=47,source_speeches=31,source_relative_sites=0,source_pause_sites=1,source_tailzeros=2,
        one_original_end_no_choices_styles_predicates_or_C200=True,source_native_constants_and_multiplicity_preserved=True,
        no_new_ROM_emulator_run_or_review_credit=True,full_goal_complete=False))
    print('Six B199 reference tools prepared;47 commands,31 speech objects,one pause,zero spans,two tailzeros. Native constants exact.')
