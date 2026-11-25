"""Run the existing cumulative Maria cold-boot schedule on the staged ship-label ROM."""

import sys
from pathlib import Path

from scripts.audit_story_glyph_consistency import load
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest
from scripts.prepare_lil361_own_startup_v1 import source as previous
from scripts.source_locked_derivation_v5118 import checked_text
from scripts.stage_ship_command_release_v1 import OUT


def main():
    if sys.argv[1:] == ['prepare']:
        source = checked_text(previous, {
            'scripts.build_registered_lil361_v1': 'scripts.stage_ship_command_release_v1',
            'Own cumulative Lil361 B283-B298 candidate': 'Own cumulative ship command label candidate',
        })
        exec(compile(source, __file__, 'exec'), {'__name__': '__main__', '__file__': __file__})
        return
    assert sys.argv[1:] == ['run']
    from scripts import headless_desmume_v193 as harness

    root = OUT / 'own_startup_run_v1'
    plan, worker = map(load, (root / 'run_plan.json', root / 'worker_argv.json'))
    assert digest(plan['candidate']) == plan['candidate_sha256'] == worker['candidate_sha256']
    assert not (root / 'capture').exists()
    sys.argv = [sys.argv[0], *worker['argv']]
    harness.main()


if __name__ == '__main__':
    main()
