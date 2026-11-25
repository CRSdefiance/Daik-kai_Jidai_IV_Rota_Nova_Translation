"""Select forty complete residual exchanges from the verified current SC2 census."""
import inspect
from pathlib import Path
from scripts import prepare_lil391_source_intake_v1 as previous
from scripts.source_locked_derivation_v5118 import checked_text

source=checked_text(inspect.getsource(previous.main), {
    '1805':'1423','4915':'5297','391':'269',
    'len(selected) == 30':'len(selected) == 40',
    'complete_exchanges=30':'complete_exchanges=40',
    "    for path, expected in census['source_packets'].items():\n        assert digest(path) == expected, path":
        "    for path in [census['prior_census']]:\n        assert digest(path)==census['prior_census_sha256']",
})
env={**previous.main.__globals__,'ROOT':Path('work/Lil269_B243_B282_clean_20261110'),
    'CENSUS':Path('work/story_source_coverage_20261110_SC2_v3/coverage.json'),
    'PACKET':Path('work/story_source_coverage_20261110_SC2_v3/residual_clean_source_packet.json'),
    'RELEASE':Path('work/lil382_residual_A_release_v1/registered_release_verification.json'),
    'BLOCKS':list(range(243,283)),'__file__':__file__}
exec(compile(source,__file__+'::same-clean-source-anddisjoint-credit-selection-guards','exec'),env)
if __name__=='__main__':env['main']()
