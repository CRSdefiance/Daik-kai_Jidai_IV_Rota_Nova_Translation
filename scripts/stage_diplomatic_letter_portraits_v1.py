"""Check native lookup, faction and surname expansion, and every letter portrait."""

import inspect
from pathlib import Path
from types import FunctionType

from dk4tool.patch import diplomatic_letter_portraits_wrap_v1 as wrapper
from scripts import stage_rumor_and_cooperation_v1 as previous
from scripts.register_rumor_and_cooperation_v1 import RELEASE
from scripts.review_diplomatic_letter_portraits_v1 import IDS
from scripts.review_diplomatic_letter_portraits_v2 import OUTPUT, surnames
from scripts.source_locked_derivation_v5118 import checked_text


ROOT = Path('out/diplomatic_letter_portraits_staged_20261111_v1')
ROM = ROOT / 'diplomatic_letter_portraits_RESEARCH_ONLY.nds'
PROOF = ROOT / 'stored_verification.json'
AMENDMENTS = {}


def catalogue(runtime):
    return previous.catalogue(runtime) | {'captain_surnames': surnames(runtime)}


def samples(row, catalog):
    args = tuple(row['original_substitutions'])
    if args == ('sending captain surname',):
        return [(name,) for name in catalog['captain_surnames'].values()]
    if row.get('unused_native_arguments'):
        assert row['message_ID'] == 2755 and not args
        args = tuple(row['unused_native_arguments'])
    if args:
        assert len(args) == 1 and args[0] in ('sending faction', 'target faction', 'declaring faction', 'demanding faction')
        return previous.samples(row | {'original_substitutions': ['faction']}, catalog) + [('Clifford',)]
    return [()]


def renderer():
    source = checked_text(inspect.getsource(previous.renderer), {
        "expanded = stored % tuple(substitutions)": "expanded = stored % tuple(substitutions[:stored.count(b'%s')])",
    })
    env = vars(previous).copy()
    exec(compile(source, __file__ + '::native-expansion-with-unused-argument', 'exec'), env)
    return env['renderer']()


def check_selector(arm):
    env = vars(previous) | vars(wrapper)
    return FunctionType(previous.check_selector.__code__, env)(arm)


def active_rows(manuscript):
    return FunctionType(previous.active_rows.__code__, vars(previous) | {'AMENDMENTS': AMENDMENTS})(manuscript)


def main():
    source = checked_text(inspect.getsource(previous.main), {
        "print(f'44 stored portraits and {len(cases)} native portrait displays passed.')":
            "print(f'{len(rows)} stored portraits and {len(cases)} native portrait displays passed.')",
        "raw % encoded": "raw % encoded[:raw.count(b'%s')]",
        '(OUTPUT, RELEASE, Path(__file__))': '(OUTPUT, RELEASE, Path(wrapper.__file__), Path(__file__))',
    })
    env = vars(previous) | globals() | {'transform': wrapper.transform}
    exec(compile(source, __file__ + '::registered-common-and-native-portrait-checks', 'exec'), env)
    env['main']()


if __name__ == '__main__':
    main()

