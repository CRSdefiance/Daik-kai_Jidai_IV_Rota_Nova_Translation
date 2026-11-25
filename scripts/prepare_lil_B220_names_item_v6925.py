"""Preserve both personal-name forms and bind the source gown without global changes."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
if __name__=='__main__':
    root=Path('work/analysis/lil_B220_names_item_tools_v6925');assert not root.exists();root.mkdir(parents=True)
    p=derive('scripts/bind_lil_B218_names_item_v6879.py','scripts/bind_lil_B220_names_item_v6925.py',{'B218':'B220','v6879':'v6925','v6875':'v6921','v6876':'v6922','thirteen_clean_current_Ares_legend_exchange_source_references':'seventeen_clean_current_empress_gown_exchange_source_references','thirteen_effective_bodies26_dispatches_two_actors_four_name_consumers':'seventeen_effective_bodies34_dispatches_two_actors_four_name_consumers',"{(2,'progressive-nameplate'):'Lil Argot',(2,'full-catalogue'):'Lil Argot',(21,'progressive-nameplate'):'Ian Dukov',(21,'full-catalogue'):'Ian Dukov'}":"{(26,'progressive-nameplate'):'Julian Lopes',(26,'full-catalogue'):'Julian Lopes',(199,'progressive-nameplate'):'Lucia',(199,'full-catalogue'):'Lucia'}",'[2,21]':'[26,199]','アレスの聖槍':'女帝のガウン','two_personal_names_and_exact_clean_current_Ares_spear_pointer':'two_personal_names_and_exact_clean_current_empress_gown_pointer','source_named_spear_is_not':'source_named_gown_is_not','source-named spear':'source-named gown'})
    save(root/'source_locked_derivation.json',p)
