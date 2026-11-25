"""Preserve compiler v1 and bind all four original name-consumer outputs explicitly."""
from pathlib import Path
from scripts.prepare_lil_B156_layout_v3705 import derive
from scripts.verify_village_wrap_v608 import save
from dk4tool.patch.grand_race_menu_release import sha
if __name__=='__main__':
    row=derive('dk4tool/patch/lil_B159_editorial_v1.py','dk4tool/patch/lil_B159_editorial_v2.py',{"require(len(nc)==4 and all(c['all_actor_models_and_unowned4MiB_exact']":"require(len(nc)==4 and {(c['actor_ID'],c['consumer']):c['text'] for c in nc}=={(9,'progressive-nameplate'):'Camille Overijssel',(9,'full-catalogue'):'Camille Marinus Overijssel',(22,'progressive-nameplate'):'Samwell Khan',(22,'full-catalogue'):'Samwell ダ Khan'} and all(c['all_actor_models_and_unowned4MiB_exact']"})
    root=Path('work/analysis/lil_B159_compiler_name_contract_v3861');assert not root.exists();root.mkdir(parents=True);save(root/'source_derivation.json',dict(tool=row,no_source_English_ROM_orledger_change=True,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
