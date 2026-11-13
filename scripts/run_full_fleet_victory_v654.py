"""Repeat the current original encounter, then use its native automatic duel input."""

import io
import json
import sys
from pathlib import Path

from dk4tool.patch.grand_race_menu_release import sha
from scripts import headless_desmume_v193 as harness
from scripts import native_battle_fixture_v620 as dispatch
from scripts.native_full_fleet_proximity_v653 import apply_fixture
from scripts.verify_village_wrap_v608 import read

ROOT = Path('work/analysis/full_fleet_victory_v654')


class PrefixThenConsole:
    def __init__(self, commands, console):
        self.prefix = io.StringIO('\n'.join(json.dumps(c) for c in commands) + '\n')
        self.console = console

    def readline(self, *args):
        line = self.prefix.readline(*args)
        return line if line else self.console.readline(*args)


def main():
    replay = '--replay' in sys.argv
    pre = read(ROOT / ('replay_preflight.json' if replay else 'preflight.json'))
    for path, digest in pre['release_hashes'].items():
        assert sha(Path(path).read_bytes()) == digest
    assert sha(Path(pre['donor']).read_bytes()) == pre['donor_sha256']
    assert sha(Path(pre['commands']).read_bytes()) == pre['commands_sha256']
    assert sha(Path(pre['inputs']).read_bytes()) == pre['inputs_sha256']
    assert sha(Path(pre['fixture_source']).read_bytes()) == pre['fixture_source_sha256']
    dispatch.apply_fixture = apply_fixture
    sys.stdin = (io.StringIO('\n'.join(json.dumps(c) for c in read(pre['commands'])) + '\n')
                 if replay else PrefixThenConsole(read(pre['commands']), sys.stdin))
    sys.argv = ['headless_desmume_v193.py', '--rom', pre['candidate'], '--out', pre['output'],
                '--frames', '100000', '--inputs-json', pre['inputs'], '--touchscreen',
                '--capture-every', '999999', '--capture-at', '4800',
                '--battery-save', pre['donor'], '--pause-at', '4800',
                '--dump-capture-ram', '--dump-pause-ram', '--dump-native-state', '--allow-battle-fixtures']
    harness.main()


if __name__ == '__main__':
    main()
