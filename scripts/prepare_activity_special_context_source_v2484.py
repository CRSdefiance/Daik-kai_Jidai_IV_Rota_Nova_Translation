"""Next24 exact clean/current battle Activity2_Chapel_Refusal_Special comments;extraction only."""
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import save
OLD=Path('scripts/prepare_tavern_exchange_source_v2182.py')
if __name__=='__main__':
 source=OLD.read_text();changes={'town_trade_port_contextual_reference_v1':'refit_contextual_spritsail_v1','tavern_exchange_source_v2182':'activity_special_context_source_v2484','IDS=list(range(820,883))':'IDS=list(range(1872,1889))','==63':'==17','all63_clean_current_context_catalog':'all17_clean_current_context_catalog'}
 for old,new in changes.items():assert old in source,old;source=source.replace(old,new)
 env={'__name__':'__main__','__file__':__file__};exec(compile(source,__file__,'exec'),env)
 save(env['ROOT']/'extractor_provenance.json',dict(original=str(OLD),original_sha256=sha(OLD.read_bytes()),effective_source_sha256=sha(source.encode()),no_new_editorial_credit=True,full_goal_complete=False))
