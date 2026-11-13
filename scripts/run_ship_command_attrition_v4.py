"""Keep the ship-menu attrition replay and all captures on the project output drive."""

import inspect
from pathlib import Path

from scripts import run_ship_command_attrition_v3 as previous
from scripts.source_locked_derivation_v5118 import checked_text


RUN = Path('out/ship_command_menu_capture_20261110_v4')


def main():
    assert RUN.resolve().drive.upper() == 'E:'
    commands = previous.RUN / 'navigation_inputs.jsonl'
    assert commands.exists()
    source = checked_text(inspect.getsource(previous.main), {
        "    journal.write_text(json.dumps(dict(until=7000, buttons=['A'], duration=8))+'\\n', encoding='utf-8')":
            "    journal.write_bytes(replay_inputs.read_bytes())",
    })
    env = {**vars(previous), **globals(), 'replay_inputs': commands}
    exec(compile(source, __file__, 'exec'), env)
    env['main']()


if __name__ == '__main__':
    main()
