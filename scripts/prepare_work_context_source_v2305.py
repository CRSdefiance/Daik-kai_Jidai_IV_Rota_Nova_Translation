"""Next24 exact clean/current Shipwright/Doctor comments; zero review credit."""
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import save
OLD=Path('scripts/prepare_tavern_exchange_source_v2182.py')
if __name__=='__main__':
 source=OLD.read_text();changes={'town_trade_port_contextual_reference_v1':'refit_contextual_spritsail_v1','tavern_exchange_source_v2182':'work_context_source_v2305','IDS=list(range(820,883))':'IDS=list(range(1386,1410))','==63':'==24','all63_clean_current_context_catalog':'all24_clean_current_context_catalog'}
 for old,new in changes.items():assert old in source,old;source=source.replace(old,new)
 env={'__name__':'__main__','__file__':__file__};exec(compile(source,__file__,'exec'),env)
 save(env['ROOT']/'extractor_provenance.json',dict(original=str(OLD),original_sha256=sha(OLD.read_bytes()),effective_source_sha256=sha(source.encode()),current_registered_parser='dk4tool.patch.refit_contextual_spritsail_v1.current_entries',no_source_prose_or_fresh_review_credit=True,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
