"""Continue the focused ship-menu replay using the observed current-game pacing."""

import inspect

from scripts import run_ship_command_replay_v1 as previous
from scripts.run_battle_cooking_livestock_live_v911 import GrowingCommands
from scripts.source_locked_derivation_v5118 import checked_text


RUN = previous.WORK / 'actual_menu_live_v2'
CAP = RUN / 'capture'


def main():
    source = checked_text(inspect.getsource(previous.main), {
        "    commands = [row for row in commands if row.get('until', 999999) <= 14100]\n"
        "    assert commands[-2]['until'] == 13900 and commands[-1] == dict(until=14100, buttons=['B'], duration=8)\n"
        "    commands.extend([dict(until=14300, duration=1), dict(stop=True)])":
        "    commands = [row for row in commands if row.get('until', 999999) <= 12900]\n"
        "    assert commands[-1] == dict(until=12900, buttons=['A'], duration=8)",
        "'--frames', '14500'": "'--frames', '24000'",
        "'--capture-at', '13700', '13900', '14100', '14300', '--dump-capture-ram'":
            "'--capture-at', '12900', '--dump-capture-ram', '--dump-ram'",
        'terminal_frame=14300': 'interactive_navigation_starts_at_frame=12900',
        '        with new_journal.open(encoding=\'utf-8\') as stream:\n'
        '            sys.stdin = stream\n'
        '            adapter.main()':
        '        stream = GrowingCommands(new_journal)\n'
        '        try:\n'
        '            sys.stdin = stream\n'
        '            adapter.main()\n'
        '        finally:\n'
        '            stream.close()',
        'original_donor_hash_preserved=True, visual_and_transition_approval_pending=True,':
        'original_donor_hash_preserved=True, final_navigation_sha256=digest(new_journal), visual_and_transition_approval_pending=True,',
    })
    env = {**vars(previous), **globals()}
    exec(compile(source, __file__, 'exec'), env)
    env['main']()


if __name__ == '__main__':
    main()
