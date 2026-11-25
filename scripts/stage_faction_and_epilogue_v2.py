"""Refine the attack alert and historical narration after visual review."""

import inspect
from pathlib import Path

from scripts import stage_faction_and_epilogue_v1 as previous


ROOT = Path('out/faction_and_epilogue_staged_20261111_v2')
ROM = ROOT / 'faction_and_epilogue_RESEARCH_ONLY.nds'
PROOF = ROOT / 'stored_verification.json'
RETAIN_STORED = {343}
AMENDMENTS = {
    334: dict(english='%s is under naval attack by %s!', decision='revision',
        localization_note='The native roster includes Bergstrom Fleet. “Under naval attack” preserves the fleet attack, the town and the attacking faction while avoiding “Bergstrom Fleet’s fleet.”'),
    344: dict(english='The Age of Discovery transformed the world from the Middle Ages into the early modern era.',
        localization_note='Complete the historical thought on this panel and keep “the early modern era” together at the end. The next panel still refers to the Age of Discovery.'),
}


def active_rows(manuscript):
    return {row['message_ID']: row | AMENDMENTS.get(row['message_ID'], {}) for row in manuscript['records']}


def stage():
    from types import FunctionType

    env = {**vars(previous), **globals(), 'previous': previous.previous}
    for operation in ('storage_text', 'render_cases'):
        env[operation] = FunctionType(getattr(previous, operation).__code__, env)
    exec(compile(inspect.getsource(previous.stage), __file__ + '::same-stored-checks-after-visual-review', 'exec'), env)
    env['stage']()


if __name__ == '__main__':
    stage()
