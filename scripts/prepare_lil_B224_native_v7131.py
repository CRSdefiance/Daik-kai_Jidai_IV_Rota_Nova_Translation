"""Prepare strict2b6 names, dispatches, event binding and A000/C200/end checks."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import checked_text,derive
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/lil_B224_native_tools_v7131')
if __name__=='__main__':
    assert not ROOT.exists()
    common={'B222':'B224','source_v7037/sixteen_clean_current_sunset_Noritsune_exchange_source_references':'source_v7130/fifteen_clean_current_Medusa_flirtation_exchange_source_references','current_V7029_native_v7033':'current_V7118_native_v7123'}
    consumers={**common,'v7038':'v7131','all16_clean_speeches_glossed_together_before_old_English':'all15_clean_glosses_precede_old_English','[2,16]':'[26,197]',"len(cases)==32":"len(cases)==30","len(effective)==16":"len(effective)==15",'all32_source_current_dispatches':'all30_source_current_dispatches','all16_current_templates':'all15_current_templates','sixteen_effective_bodies32_dispatches':'fifteen_effective_bodies30_dispatches','sixteen effective zero-macro':'fifteen effective zero-macro','bodies=16,dispatches=32':'bodies=15,dispatches=30'}
    entry={**common,'v7039':'v7132','in [222]':'in [224]'}
    controls={'B220':'B224','controls_v6924':'controls_v7133','source_v6921/seventeen_clean_current_empress_gown_exchange_source_references':'source_v7130/fifteen_clean_current_Medusa_flirtation_exchange_source_references','current_V6910_native_v6920':'current_V7118_native_v7123','Al_Ferid_exact_native_context_v6520':'square_shopkeeper_exact_native_context_v7020','[26,199]':'[26,197]','blocks[220]':'blocks[224]',
      'len(block)==1280 and 8+struct.unpack_from(\'<H\',block,4)[0]==1280 and block[1276:]==bytes(4)':'len(block)==960 and 8+struct.unpack_from(\'<H\',block,4)[0]==958 and block[954:]==bytes(6)',
      'len(commands)==20':'len(commands)==18','1266':'944','1274':'952','1276':'954','00a0ffff43000110':'00a0ffff46000110',
      'original_end1276_full4bytes_and_no_tail_preserved':'original_end954_full4bytes_and_tail2_preserved',
      'C200_original_two_byte_request_at1274':'C200_original_two_byte_request_at952'}
    jobs=[('scripts/prove_lil_B222_consumers_v7038.py','scripts/prove_lil_B224_consumers_v7131.py',consumers),('scripts/prove_lil_B222_entry_v7039.py','scripts/prove_lil_B224_entry_v7132.py',entry),('scripts/prove_lil_B220_controls_v6924.py','scripts/prove_lil_B224_controls_v7133.py',controls)]
    for a,b,c in jobs:assert not Path(b).exists();checked_text(Path(a).read_text('utf8'),c)
    rows=[derive(a,b,c) for a,b,c in jobs];ROOT.mkdir(parents=True);save(ROOT/'source_locked_native_tools.json',dict(tools=rows,strict2b6_and_own_current_input_required=True,all_native_high_integer_constants_and_multiplicity_preserved=True,actual_names_roles_voices_and_outer_event_conditions_not_assumed=True,new_credit=0,full_goal_complete=False))
