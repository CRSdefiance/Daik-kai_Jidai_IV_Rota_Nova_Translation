"""Bind native personal-name fields and the exact source-named shield pointer."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import checked_text,derive
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/lil_B224_names_item_tools_v7138')
if __name__=='__main__':
    assert not ROOT.exists()
    a='scripts/bind_lil_B220_names_item_v6925.py';b='scripts/bind_lil_B224_names_item_v7138.py'
    c={'B220':'B224','name_item_v6925':'name_item_v7138','source_v6921/seventeen_clean_current_empress_gown_exchange_source_references':'source_v7130/fifteen_clean_current_Medusa_flirtation_exchange_source_references','consumers_v6922/seventeen_effective_bodies34_dispatches_two_actors_four_name_consumers':'consumers_v7131/fifteen_effective_bodies30_dispatches_two_actors_four_name_consumers',
      "(199,'progressive-nameplate'):'Lucia'":"(197,'progressive-nameplate'):'Safia'","(199,'full-catalogue'):'Lucia'":"(197,'full-catalogue'):'Safia'",'[26,199]':'[26,197]','女帝のガウン':'メデューサの盾','empress_gown':'Medusa_shield','source_named_gown_is_not_a_runtime_FI_substitution':'source_named_shield_is_not_a_runtime_FI_substitution','source-named gown':'source-named shield'}
    assert not Path(b).exists();checked_text(Path(a).read_text('utf8'),c);row=derive(a,b,c)
    ROOT.mkdir(parents=True);save(ROOT/'source_locked_names_item_binding.json',dict(tool=row,no_global_name_or_item_asset_changes=True,source_named_shield_pointer_not_inferred_from_A000_operand=True,new_credit=0,full_goal_complete=False))
