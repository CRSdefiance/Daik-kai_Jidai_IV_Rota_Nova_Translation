"""Apply all staged completion files only after every before/planned hash matches."""
import os
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read, save

ROOT = Path('work/analysis/lil_B169_completion_v4255')
if __name__ == '__main__':
    assert not (ROOT/'native_application_receipt.json').exists()
    workspace = Path.cwd().resolve()
    plan = read(ROOT/'staged_completion.json')
    assert len(plan['files'])==6
    for entry in plan['files']:
        target,planned = Path(entry['target']),Path(entry['planned'])
        assert target.is_relative_to(workspace) and planned.is_relative_to(ROOT.resolve())
        assert sha(target.read_bytes())==entry['before_sha256']
        assert sha(planned.read_bytes())==entry['planned_sha256']
        assert planned.stat().st_size>=target.stat().st_size
    for entry in plan['files']:
        with Path(entry['target']).open('r+b') as stream:
            stream.write(Path(entry['planned']).read_bytes())
            stream.flush()
            os.fsync(stream.fileno())
        assert sha(Path(entry['target']).read_bytes())==entry['planned_sha256']
    save(ROOT/'native_application_receipt.json',dict(all6_staged_targets_hash_exact=True,
        all_before_and_planned_hashes_validated_before_any_write=True,
        staged_plan_sha256=sha((ROOT/'staged_completion.json').read_bytes()),
        producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    print('All six completion files applied byte-exactly;seal and independent audit required.')
