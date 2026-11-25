"""Reconstruct the fuller-opening target under immutable policyv2;preserve the first target."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive,checked_text
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/lil_B225_final_reference_tools_v7213')
if __name__=='__main__':
    assert not ROOT.exists()
    jobs=[('scripts/research_lil_B225_relocation_v7197.py','scripts/research_lil_B225_relocation_v7213.py',{'relocation_v7197':'relocation_v7213','editorial_manuscript_v2.json':'editorial_manuscript_v2b.json','lil_B225_profile_v1':'lil_B225_profile_v2','lil_B225_layout_v1':'lil_B225_layout_v2','lil_B225_native_contract_v1':'lil_B225_native_contract_v2'}),('scripts/create_lil_B225_reference_v7199.py','scripts/create_lil_B225_reference_v7215.py',{'reference_v7199':'reference_v7215','relocation_v7197':'relocation_v7213','stored_v7198':'stored_v7214'})]
    for a,b,c in jobs:assert not Path(b).exists();checked_text(Path(a).read_text('utf8'),c)
    rows=[derive(a,b,c) for a,b,c in jobs];ROOT.mkdir(parents=True);save(ROOT/'source_locked_final_target_tools.json',dict(tools=rows,policyv2_manuscriptv2b_required=True,full976_inverse_andall16_commands_retained=True,no_old_target_ROM_hash_relabelled_as_new=True,all_previous_artifacts_preserved=True,new_credit=0))
