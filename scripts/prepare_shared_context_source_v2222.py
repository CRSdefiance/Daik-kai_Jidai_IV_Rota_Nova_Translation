"""Next50 exact source/current shared exchanges; extraction adds zero review credit."""
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import save

original=Path('scripts/prepare_tavern_exchange_source_v2182.py')
source=original.read_text()
for old,new in(('tavern_exchange_source_v2182','shared_context_source_v2222'),('IDS=list(range(820,883))','IDS=list(range(1020,1070))'),('==63','==50'),('all63_clean_current_context_catalog','all50_clean_current_context_catalog')):
    assert old in source
    source=source.replace(old,new)
env={'__name__':'__main__','__file__':__file__}
exec(compile(source,__file__,'exec'),env)
save(env['ROOT']/'extractor_provenance.json',dict(source=str(original),source_sha256=sha(original.read_bytes()),effective_source_sha256=sha(source.encode()),producer_sha256=sha(Path(__file__).read_bytes()),no_source_prose_or_fresh_credit=True))
