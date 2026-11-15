"""Prepare full988-byte inverse and measured stored/reference proofs for B230."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive,checked_text
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/lil_B230_relocation_tools_v7447')
if __name__=='__main__':
    assert not ROOT.exists();common={'B229':'B230','relocation_v7399':'relocation_v7447','stored_v7400':'stored_v7448','reference_v7401':'reference_v7449','native_pages_v7394':'native_pages_v7442b','current_V7371_native_v7376':'current_V7418_native_v7423','v7371':'v7418','V7371':'V7418','944':'988','932':'976','940':'984','936':'980','00a0ffff35000110':'00a0ffff34000110','blocks[229]':'blocks[230]','block=229':'block=230','[229]':'[230]','block229_RESEARCH':'block230_RESEARCH'};jobs=[]
    for a,b in [('research_lil_B229_relocation_v7399','research_lil_B230_relocation_v7447'),('prove_lil_B229_stored_v7400','prove_lil_B230_stored_v7448'),('create_lil_B229_reference_v7401','create_lil_B230_reference_v7449')]:
        src=Path('scripts/'+a+'.py').read_text('utf8');changes={k:v for k,v in common.items() if k in src};checked_text(src,changes);assert not Path('scripts/'+b+'.py').exists();jobs.append(('scripts/'+a+'.py','scripts/'+b+'.py',changes))
    rows=[derive(*j) for j in jobs];ROOT.mkdir(parents=True);save(ROOT/'source_locked_full_inverse_andstored_reference.json',dict(tools=rows,source988_logical988_tail0_A000976_end984_exact=True,all17_speeches19_commands_andfull_inverse_required=True,target_sizes_andtails_measured_not_inherited=True,all_native_high_integer_constants_preserved=True,new_credit=0,full_goal_complete=False))
