"""Unstubbed native font continuations from observed ordinary recruitment."""
from pathlib import Path
from scripts.verify_village_wrap_v608 import read

folder = 'recruitment_actual_v2202_V2171'
observed = read(Path('E:/Rota Nova translations/Generated/work/emulation_v193') / folder / 'common_observer/requests.json')
ids = [row['source_request']['ID'] for row in observed['rows']]
assert len(ids) == len(set(ids))
source = Path('scripts/probe_revised_compact_font_v2147.py').read_text()
for old, new in (
    ('square_revised_continuations_v2147', 'recruitment_actual_continuations_v2206'),
    ('promoter_context_live_v2144_V2143', folder),
    ('all_routes_combined_v2143_candidate', 'all_routes_combined_v2171_candidate'),
):
    assert old in source
    source = source.replace(old, new)
exec(compile(source, __file__, 'exec'), {'__name__': '__main__', '__file__': __file__})
