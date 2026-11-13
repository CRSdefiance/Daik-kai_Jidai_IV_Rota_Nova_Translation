"""Compare the actual matching recorded RAM frames; older runs have no final RAM dump."""
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import save

original = Path('scripts/verify_tavern_actual_v2193.py')
source = original.read_text()
changes = {
    "work/analysis/tavern_actual_verification_v2193'": "work/analysis/tavern_actual_verification_v2193c'",
    '(3200, 5000, 7000, 8200, 9201)': '(3200, 5000, 7000, 8200, 9200)',
    '(3200, 5000, 6001)': '(3200, 5000, 6000)',
}
for before, after in changes.items():
    assert source.count(before) == 1
    source = source.replace(before, after)
namespace = {'__name__': '__main__', '__file__': __file__}
exec(compile(source, __file__, 'exec'), namespace)
save(namespace['ROOT']/'snapshot_scope_correction.json', dict(original_verifier=str(original), original_verifier_sha256=sha(original.read_bytes()), effective_source_sha256=sha(source.encode()), successor_sha256=sha(Path(__file__).read_bytes()), paired_direct_state_frames=[3200,5000,7000,8200,9200], paired_price_state_frames=[3200,5000,6000], old_final_RAM_snapshots_absent=True, new_final_RAM_dumps_preserved_without_invented_old_reference=True, prior_failed_2193_and2193b_preserved=True, no_ROM_capture_or_gameplay_change=True))
