"""Prepare B211's complete source fixture and its own leaves/event checks; retain native constants."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/lil_B211_source_tools_v6555')
if __name__=='__main__':
    assert not ROOT.exists();proofs=[]
    packet='lil_B211_source_v6550c/twelve_clean_current_complete_exchange_source_references.json'
    proofs.append(derive('scripts/research_lil_B210_source_fixture_v6503.py','scripts/research_lil_B211_source_fixture_v6555.py',{
        'lil_B210_source_v6498/ten_clean_current_complete_exchange_source_references.json':packet,'B210':'B211','source_fixture_v6503':'source_fixture_v6555','_source_v6503_':'_source_v6555_',
        'blocks[210]':'blocks[211]','source_block=210':'source_block=211','source_event210':'source_event211','len(jp)==688 and end==686 and jp[end:]==bytes(2)':'len(jp)==640 and end==640 and jp[end:]==bytes(0)',
        'len(commands)==21 and len(speeches)==10':'len(commands)==23 and len(speeches)==12','all21_stored_fixture_commands':'all23_stored_fixture_commands','all12_source_commands_plus9':'all14_source_commands_plus9',
        'local-lord-reddish-sword-rumor-ten-original-speeches-and-one-original-A000':'swan-pair-twelve-original-speeches-three-FE-animal-panels-one-FI-and-one-original-A000',
        '12 original+9 initializer commands,10 progressive speeches,one original A000,no FE/typed objects/choices/relatives/predicates/macros':'14 original+9 initializer commands,9 progressive/3 FE animal panels,one FI andone original A000,no typed objects/choices/relatives/predicates'}))
    proofs.append(derive('scripts/run_lil_B210_source_v6504.py','scripts/run_lil_B211_source_v6556.py',{'B210':'B211','source_fixture_v6503':'source_fixture_v6555','source_run_v6504':'source_run_v6556','_source_v6504':'_source_v6556',"selected['source_block']==210":"selected['source_block']==211",'source_event210':'source_event211',"'displayed_original_source_block':210":"'displayed_original_source_block':211",'all12_source_commands_retained':'all14_source_commands_retained'}))
    proofs.append(derive('scripts/prove_lil_B210_controls_v6505.py','scripts/prove_lil_B211_controls_v6557.py',{
        'B210':'B211','controls_v6505':'controls_v6557','lil_B210_source_v6498/ten_clean_current_complete_exchange_source_references.json':packet,'blocks[210]':'blocks[211]','==12':'==14',
        "[(674,'00a0ffff24000110'),(682,'00000000')]":"[(628,'00a0ffff1a000110'),(636,'00000000')]",'(688,686)':'(640,640)','b[logical:]==bytes(2) and b[682:686]':'b[logical:]==bytes(0) and b[636:640]',
        'stored_bytes=688,logical_end=686,tailzeros=2':'stored_bytes=640,logical_end=640,tailzeros=0',',b,682,previous)':',b,636,previous)',
        'source_stored688_logical686_tail2_complete_end682':'source_stored640_logical640_tail0_complete_end636','source10_static_progressive_speeches_no_FE_or_macro_preserved':'source9_progressive_three_null_actor_FE_one_FI_macro_preserved'}))
    proofs.append(derive('scripts/prove_lil_B210_entry_v6506.py','scripts/prove_lil_B211_entry_v6558.py',{
        'B210':'B211','entry_v6506':'entry_v6558','lil_B210_source_v6498/ten_clean_current_complete_exchange_source_references.json':packet,'current_V6488_native_v6497':'current_V6541_native_v6549','current_build_native_context_v6261b':'Al_Ferid_exact_native_context_v6520','[210]':'[211]'}))
    ROOT.mkdir(parents=True);save(ROOT/'prepared_tools.json',dict(proofs=proofs,source_commands=14,source_objects=12,source640_logical640_tail0=True,nine_progressive_three_FE_one_FI_bound=True,no_forced_role_roster_condition_funds_RNG_result_RAM_or_progress=True,all_native_constants_preserved=True,full_goal_complete=False))
