"""Verify stored text and all original fleet-dissolution portrait displays."""

import inspect
from pathlib import Path
from types import FunctionType

from dk4tool.patch import faction_aftermath_portraits_wrap_v1 as wrapper
from scripts import stage_rumor_and_cooperation_v1 as previous
from scripts.register_diplomatic_letter_portraits_v1 import RELEASE
from scripts.review_faction_aftermath_portraits_v1 import IDS, OUTPUT
from scripts.source_locked_derivation_v5118 import checked_text


ROOT = Path('out/faction_aftermath_portraits_staged_20261111_v1')
ROM = ROOT / 'faction_aftermath_portraits_RESEARCH_ONLY.nds'
PROOF = ROOT / 'stored_verification.json'
AMENDMENTS = {}
transform = wrapper.transform
relocate, reference = previous.relocate, previous.reference


def samples(row, catalog):
    assert not row['original_substitutions']
    return [()]


def check_selector(arm):
    return FunctionType(previous.check_selector.__code__, vars(previous) | vars(wrapper))(arm)


def active_rows(manuscript):
    return FunctionType(previous.active_rows.__code__, vars(previous) | {'AMENDMENTS': AMENDMENTS})(manuscript)


def main():
    source = checked_text(inspect.getsource(previous.main), {
        '    catalog = catalogue(runtime)': "    catalog = {'substitutions': 'No runtime substitutions in these three original tables.'}",
        "print(f'44 stored portraits and {len(cases)} native portrait displays passed.')":
            "print(f'{len(rows)} stored portraits and {len(cases)} native portrait displays passed.')",
        '(OUTPUT, RELEASE, Path(__file__))': '(OUTPUT, RELEASE, Path(wrapper.__file__), Path(__file__))',
    })
    env = vars(previous) | globals()
    exec(compile(source, __file__ + '::registered-common-and-native-portrait-checks', 'exec'), env)
    env['main']()


if __name__ == '__main__':
    main()

