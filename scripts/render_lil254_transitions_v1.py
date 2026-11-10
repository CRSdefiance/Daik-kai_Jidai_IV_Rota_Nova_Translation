"""Bind the Lil254 sample's intact exit to the native tutorial return."""

from scripts import render_lil382_transitions_v1 as previous
from scripts.source_locked_derivation_v5118 import checked_text


if __name__ == '__main__':
    source = checked_text(previous.source, {
        "f'display_run{choice}_v1/terminal.json'": "f'actual_run{choice}_v1/terminal.json'",
    })
    exec(compile(source, __file__, 'exec'), globals())
