"""Run the exact-position clean-source census for SC1 at the registered 18,767 checkpoint.

Missing exact bindings are leads for reconciliation, not automatic permission to
repeat a historical review. This makes no editorial credit or ROM changes.
"""
import inspect
from pathlib import Path

from scripts import reconcile_rafael_source_coverage_v1 as previous
from scripts.source_locked_derivation_v5118 import checked_text

ROOT = Path('work/Hodram_source_coverage_20261107_v1')
RELEASE = Path('work/hodram_B311_B324_release_v1/registered_release_verification.json')
ARCHIVE = '/data/SC1.DK4'

source = checked_text(inspect.getsource(previous.main), {
    "== 16748": "== 18767",
    "['integrated_record_keys']": "['integrated_record_keys']",
    "Path('work').glob('Rafael_*/clean_source_packet.json')":
        "Path('work').glob('*/clean_source_packet.json')",
    "Path('work/analysis').glob('Rafael_*/clean_source_packet.json')":
        "Path('work/analysis').glob('*/clean_source_packet.json')",
    "f'SC0_B{n}_STYLE_": "f'SC1_B{n}_STYLE_",
    "f'SC0_B{n}_CHOICE_": "f'SC1_B{n}_CHOICE_",
    "f'SC0 {n}/": "f'SC1 {n}/",
    "dict(route=0, file_path=ARCHIVE": "dict(route=1, file_path=ARCHIVE",
})

env = {**vars(previous), **globals(), '__file__': __file__}
exec(compile(source, __file__+'::same-clean-native-inventory-and-exact-source-binding-contract', 'exec'), env)

if __name__ == '__main__':
    env['main']()
