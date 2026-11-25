"""Run frozen full native continuations against current, uniquely observed Tavern IDs."""
from pathlib import Path
import sys
from scripts.verify_village_wrap_v608 import read

mode = sys.argv[1]
assert mode in ('direct', 'price')
version = 2190 if mode == 'direct' else 2191
folder = f'tavern_{mode}_actual_v{version}_V2171'
observed = read(Path('E:/Rota Nova translations/Generated/work/emulation_v193') / folder / 'common_observer/requests.json')
ids = [row['source_request']['ID'] for row in observed['rows']]
assert len(ids) == len(set(ids))
source = Path('scripts/probe_revised_compact_font_v2147.py').read_text()
source = source.replace('square_revised_continuations_v2147', f'tavern_actual_continuations_v2192_{mode}')
source = source.replace('promoter_context_live_v2144_V2143', folder)
source = source.replace('all_routes_combined_v2143_candidate', 'all_routes_combined_v2171_candidate')
exec(compile(source, __file__, 'exec'), {'__name__': '__main__', '__file__': __file__})
