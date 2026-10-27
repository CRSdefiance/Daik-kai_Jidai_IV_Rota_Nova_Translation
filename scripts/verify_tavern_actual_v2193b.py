"""Successor: include the harness's separately recorded final RAM snapshots."""
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import save

original = Path('scripts/verify_tavern_actual_v2193.py')
source = original.read_text()
source = source.replace("work/analysis/tavern_actual_verification_v2193'", "work/analysis/tavern_actual_verification_v2193b'")
marker = "        old_snapshots = {r['frame']: r for r in previous['read_only_capture_RAM_snapshots']}"
assert source.count(marker) == 1
source = source.replace(marker, marker + "\n        snapshots[report['frames']] = report['read_only_RAM_snapshot']\n        old_snapshots[previous['frames']] = previous['read_only_RAM_snapshot']")
namespace = {'__name__': '__main__', '__file__': __file__}
exec(compile(source, __file__, 'exec'), namespace)
save(namespace['ROOT']/'snapshot_scope_correction.json', dict(original_verifier=str(original), original_verifier_sha256=sha(original.read_bytes()), effective_source_sha256=sha(source.encode()), successor_sha256=sha(Path(__file__).read_bytes()), final_RAM_is_recorded_separately_from_requested_capture_RAM=True, no_ROM_capture_or_gameplay_change=True))
