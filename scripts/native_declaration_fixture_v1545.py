"""Exact current-ROM successor of the audited40-byte location-only fixture."""
import re
from pathlib import Path
from scripts import native_retreat_transfer_fixture_v1523 as previous

source = Path(previous.__file__).read_text(encoding='utf-8')
replacements = {
    'out/all_routes_combined_v1520_candidate.nds': 'out/all_routes_combined_v1542_candidate.nds',
    'work/analysis/retreat_transfer_fixture_v1523': 'work/analysis/declaration_responses_fixture_v1545',
    'work/analysis/retreat_transfer_release_v1519/registered_release_verification.json': 'work/analysis/declaration_responses_release_v1541/registered_release_verification.json',
    'work/analysis/battle_reaction_release_v1491/registered_release_verification.json': 'work/analysis/retreat_transfer_release_v1519/registered_release_verification.json',
    'translations/retreat_transfer_editorial_release_v1.json': 'translations/declaration_responses_editorial_release_v1.json',
    'stronger_fleet_anchor_v1502_1492': 'retreat_transfer_v1524_1520',
    'V1492->V1520': 'V1520->V1542',
    'V1520 prebattle fixture': 'V1542 prebattle fixture',
}
for old in replacements:
    assert source.count(old) == 1, old
source = re.sub('|'.join(re.escape(k) for k in replacements), lambda m: replacements[m.group()], source)
exec(compile(source, __file__, 'exec'), globals())
