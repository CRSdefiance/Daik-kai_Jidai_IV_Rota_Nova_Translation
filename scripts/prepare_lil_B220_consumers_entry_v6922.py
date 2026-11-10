"""Bind this exchange's actors and original EV2 independently of B218's identities."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import checked_text,derive
from scripts.verify_village_wrap_v608 import save
if __name__=='__main__':
    root=Path('work/analysis/lil_B220_consumers_entry_tools_v6922');assert not root.exists()
    common={'B218':'B220','v6875':'v6921','thirteen_clean_current_Ares_legend_exchange_source_references':'seventeen_clean_current_empress_gown_exchange_source_references','current_V6865_native_v6874':'current_V6910_native_v6920'}
    jobs=[('scripts/prove_lil_B218_consumers_v6876.py','scripts/prove_lil_B220_consumers_v6922.py',{**common,'v6876':'v6922','all13_clean_glosses':'all17_clean_glosses','[2,21]':'[26,199]','len(cases)==26':'len(cases)==34','len(effective)==13':'len(effective)==17','all26_source_current_dispatches':'all34_source_current_dispatches','all13_current_templates':'all17_current_templates','thirteen_effective_bodies26_dispatches_two_actors_four_name_consumers':'seventeen_effective_bodies34_dispatches_two_actors_four_name_consumers','bodies=13,dispatches=26':'bodies=17,dispatches=34','Bind three actors, six distinct name consumers, eighteen effective bodies and original FI expansion.':'Bind two actors,four original name consumers and seventeen effective zero-macro bodies.',"'actor = root+4+32*ident':'actor = root+0x19E4 if ident==2 else root+4+32*ident'":"'actor = root+4+32*ident':'actor = root+4+32*ident'",'::three-actors':'::two-actors'}),
    ('scripts/prove_lil_B218_entry_v6877.py','scripts/prove_lil_B220_entry_v6923.py',{**common,'v6877':'v6923',"in [218]":"in [220]"})]
    for a,b,c in jobs:assert not Path(b).exists();checked_text(Path(a).read_text('utf8'),c)
    root.mkdir(parents=True);save(root/'source_locked_derivations.json',[derive(a,b,c) for a,b,c in jobs])
