"""Prepare preserved research images and an ordinary English-scene runner from the complete B211 target."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/lil_B211_reference_English_tools_v6566')
if __name__=='__main__':
    assert not ROOT.exists();proofs=[]
    proofs.append(derive('scripts/create_lil_B210_reference_v6515.py','scripts/create_lil_B211_reference_v6566.py',{
        'lil_B210_relocation_reference_v6513b/ten_speech_relocation_complete_preambles_A000_end_and_full_inverse_RESEARCH.json':'lil_B211_relocation_research_v6564c/twelve_speech_relocation_complete_preambles_A000_end_and_full_inverse_RESEARCH.json',
        'lil_B210_stored_v6514/all10_final_stored_targets40_alignment_cases_and10_complete_pages.json':'lil_B211_stored_v6565/all12_final_stored_targets48_alignments_and12_complete_pages.json',
        'B210':'B211','reference_v6515':'reference_v6566','all_routes_combined_v6488':'all_routes_combined_v6541','==[210]':'==[211]','all10 local-lord/reddish-sword conversation objects':'all12 swan-encounter progressive/FE conversation objects','all688 predecessor':'all640 predecessor','V6488':'V6541'}))
    proofs.append(derive('scripts/research_lil_B210_English_fixture_v6516.py','scripts/research_lil_B211_English_fixture_v6567.py',{
        'B210':'B211','reference_v6515':'reference_v6566','English_fixture_v6516':'English_fixture_v6567','English_v6516':'English_v6567','English_v6517':'English_v6568',
        'source_fixture_v6503':'source_fixture_v6555','source_v6504':'source_v6556','source_run_v6504':'source_run_v6556','English_run_v6517':'English_run_v6568','[210]':'[211]','source_block=210':'source_block=211','event210':'event211','==654':'==726','==656':'==728',
        'len(native)==12 and len(commands)==21 and len(speeches)==10':'len(native)==14 and len(commands)==23 and len(speeches)==12','all21_stored_fixture_commands':'all23_stored_fixture_commands','all12_source_commands_plus9':'all14_source_commands_plus9',
        'all10_original_static_speeches_one_A000_and_complete_end_unforced':'all12_original_speeches_nine_progressive_three_FE_one_FI_A000_and_end_unforced','all10_original_four_row_single_page_native_speech_bodies_under_test':'all12_original_single_page_native_progressive_and_FE_bodies_under_test','V6488':'V6541',
        'local-lord/reddish-sword ten-speech original-command scene':'swan-pair twelve-speech original-command scene with threeFE andoneFI','12source+9initializers,10static speeches':'14source+9initializers,9progressive/3FE objects/oneFI'}))
    ROOT.mkdir(parents=True);save(ROOT/'source_locked_tools.json',dict(proofs=proofs,all_native_constants_and_source_conditions_preserved=True,all_prior_producers_and_ROMs_retained=True,full_goal_complete=False))
