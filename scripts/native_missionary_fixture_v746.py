"""Reuse the V623 three-byte role fixture against the exact editorial candidates.

Keep the historical module and its hash guard intact. The reused function gets
private globals with two explicitly pinned ARM9 versions; its native getter and
whole-RAM checks execute unchanged against the current captured state.
"""

from pathlib import Path
from types import FunctionType

from scripts import native_missionary_fixture_v623 as legacy
from scripts.verify_village_wrap_v608 import read

ORIGINAL = legacy.assign


def assign(arm, raw, request):
    config = read('translations/giveaway_editorial_release_v1.json')
    assert config['format'] == 'dk4-giveaway-editorial-v1'
    allowed = (config['source_arm9_sha256'], config['target_arm9_sha256'])
    original_guards = legacy.ARMS
    scoped = FunctionType(ORIGINAL.__code__, {**ORIGINAL.__globals__, 'ARMS': allowed},
                          'assign_editorial_fixture')
    after, receipt = scoped(arm, raw, request)
    assert legacy.ARMS == original_guards
    assert len(receipt['changes']) == 3
    assert sum(a != b for a, b in zip(raw, after, strict=True)) == 3
    receipt['legacy_fixture_body_sha256'] = legacy.sha(Path(legacy.__file__).read_bytes())
    receipt['editorial_fixture_adapter_sha256'] = legacy.sha(Path(__file__).read_bytes())
    receipt['private_globals_only_historical_source_and_original_ARMS_unchanged'] = True
    receipt['accepted_current_ARM9_hashes'] = list(allowed)
    return after, receipt
