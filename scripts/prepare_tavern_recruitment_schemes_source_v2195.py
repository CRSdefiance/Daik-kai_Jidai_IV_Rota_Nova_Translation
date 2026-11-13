"""Exact clean/current recruitment and scheme exchanges; extraction adds no review credit."""
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import save

original = Path('scripts/prepare_tavern_exchange_source_v2182.py')
source = original.read_text()
source = source.replace('tavern_exchange_source_v2182', 'tavern_recruitment_schemes_source_v2195')
source = source.replace('IDS=list(range(820,883))', 'IDS=list(range(883,989))')
source = source.replace('==63', '==106').replace('all63_clean_current_context_catalog', 'all106_clean_current_context_catalog')
namespace = {'__name__': '__main__', '__file__': __file__}
exec(compile(source, __file__, 'exec'), namespace)
save(namespace['ROOT']/'extractor_provenance.json',dict(source=str(original),source_sha256=sha(original.read_bytes()),effective_source_sha256=sha(source.encode()),producer_sha256=sha(Path(__file__).read_bytes()),no_source_prose_or_fresh_credit=True))
