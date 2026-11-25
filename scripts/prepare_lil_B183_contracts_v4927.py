"""Prepare source-owned B183 dispatch,entry and three linear control leaves."""
from pathlib import Path
from scripts.prepare_lil_B156_layout_v3705 import derive
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/lil_B183_contract_tools_v4927')
OLD='lil_B181_source_v4832/all10_clean_current_complete_context'
NEW='lil_B183_source_v4925/all25_clean_current_complete_context'
if __name__=='__main__':
    assert not ROOT.exists();tools=[]
    tools.append(derive('scripts/prove_lil_B181_dispatches_v4834.py','scripts/prove_lil_B183_dispatches_v4927.py',{
        OLD:NEW,'B181':'B183','dispatches_v4834':'dispatches_v4927','voices_v4833':'voices_v4926',
        'len(cases)==20':'len(cases)==50',"sum(c['source_selector']==254 for c in cases)==2":"sum(c['source_selector']==254 for c in cases)==4",
        'all10_source_current_dispatches':'all25_source_current_dispatches','all3_static_actors':'all5_static_actors',
        'one_FE_source_object_uses_original_null_actor_path':'both_FE_source_objects_use_original_null_actor_path',
        'Bind20':'Bind50','20 source/current dispatches pass:three static actors,one FE/null-actor notice':'50 source/current dispatches pass:five static actors,two FE/null-actor objects'}))
    tools.append(derive('scripts/prove_lil_B181_entry_v4835.py','scripts/prove_lil_B183_entry_v4928.py',{
        OLD:NEW,'B181':'B183','entry_v4835':'entry_v4928','voices_v4833':'voices_v4926','in [181]':'in [183]'}))
    tools.append(derive('scripts/prove_lil_B181_controls_v4836.py','scripts/prove_lil_B183_controls_v4929.py',{
        OLD:NEW,'B181':'B183','controls_v4836':'controls_v4929','voices_v4833':'voices_v4926',
        'blocks[181]':'blocks[183]','block=181':'block=183',
        "[(8,'00a0ffff014913a1'),(390,'00c2'),(392,'00000000')]":"[(8,'00a0ffff013926a1'),(950,'00c2'),(952,'00000000')]",
        'len(commands)==13 and len(blocks[0])==len(blocks[1])==396':'len(commands)==28 and len(blocks[0])==len(blocks[1])==956',
        'source_offset=390':'source_offset=950','source_declared_end_offsets=[392]':'source_declared_end_offsets=[952]'}))
    ROOT.mkdir(parents=True);save(ROOT/'prepared_contracts.json',dict(tools=tools,source_speeches=25,source_commands=28,
        progressive=23,FE=2,static_selectors=[85,110,132,148,153],relative_sites=0,predicates=0,
        no_new_ROM_emulator_or_review_credit=True,full_goal_complete=False))
    print('Prepared B183 50 dispatches,current entry and A000/C200/end gates.')
