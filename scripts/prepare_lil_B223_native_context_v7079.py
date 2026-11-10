"""Prepare source-owned B223 consumers,entry and relative controls under exact2b6."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive,checked_text
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/lil_B223_context_tools_v7079')
if __name__=='__main__':
    assert not ROOT.exists()
    common={'B214':'B223','source_v6697':'source_v7078','current_V6686_native_v6696':'current_V7067_native_v7077','Al_Ferid_exact_native_context_v6520':'square_shopkeeper_exact_native_context_v7020'}
    jobs=[('scripts/prove_lil_B214_consumers_v6698.py','scripts/prove_lil_B223_consumers_v7079.py',{**common,'consumers_v6698':'consumers_v7079','V6686':'V7067','aa5a7ed159f33fb8ca5dafdfc068ebc69cf9de0469ffe8eba388d3b954e20d05':'2b6aaaa499d634be9afc255d1c39b64ef0f578283c9768c525b31e34499abd0a','[2,4,23]':'[2,13,21]','[2,4,23,d0':'[2,13,21,d0','blocks[214]':'blocks[223]','block=214':'block=223','related_Judas_sword_item_consumers_pending':'related_Timur_mail_item_title_and_consumers_pending'}),
    ('scripts/prove_lil_B214_entry_v6704.py','scripts/prove_lil_B223_entry_v7080.py',{**common,'entry_v6704':'entry_v7080','in [214]':'in [223]'}),
    ('scripts/prove_lil_B214_branches_v6701.py','scripts/prove_lil_B223_branches_v7081.py',{'B214':'B223','branches_v6701':'branches_v7081','source_v6697':'source_v7078'})]
    for a,b,c in jobs:assert not Path(b).exists();checked_text(Path(a).read_text('utf8'),c)
    rows=[derive(a,b,c) for a,b,c in jobs];ROOT.mkdir(parents=True);save(ROOT/'source_locked_context_checks.json',dict(tools=rows,all_native_addresses_and_ownership_checks_preserved=True,exact_current_runtime_not_relaxed_AA5=True,new_credit=0,full_goal_complete=False))
