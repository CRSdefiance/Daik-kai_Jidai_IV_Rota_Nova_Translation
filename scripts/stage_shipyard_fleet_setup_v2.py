"""Retain the compact captain prompt and keep the admiral question together."""

from types import FunctionType

from dk4tool.patch.shipyard_fleet_setup_wrap_v2 import transform
from scripts import stage_shipyard_fleet_setup_v1 as first


ROOT = first.ROOT.with_name('shipyard_fleet_setup_staged_20261111_v2')
ROM = ROOT / first.ROM.name
PROOF = ROOT / first.PROOF.name
MANUSCRIPT, PREFLIGHT = first.MANUSCRIPT, first.PREFLIGHT
RETAIN_STORED = first.RETAIN_STORED | {271}
AMENDMENTS = first.AMENDMENTS | {
    271: {
        'english': 'Choose a crew member as captain.',
        'decision': 'retention',
        'localization_note': 'The current invitation is clear and identifies both the eligible crew and the intended role. It stays together in one native row.',
    },
}
PHRASE_STARTS = {n: phrase for n, phrase in first.PHRASE_STARTS.items() if n not in (269, 271)}


def stage():
    env = {**vars(first), **globals(), '__file__': __file__, '__name__': 'shipyard_fleet_setup_v2'}
    for method in (first.active_rows, first.choose_storage):
        env[method.__name__] = FunctionType(method.__code__, env)
    FunctionType(first.stage.__code__, env)()


if __name__ == '__main__':
    stage()
