"""Seal the revised layouts and the original monthly payout for the Lisbon candidate."""

import argparse
from inspect import getsource
from types import FunctionType, SimpleNamespace

from scripts import replay_golden_route_exchanges_v2 as replay
from scripts import verify_golden_route_exchanges_v1 as prior
from scripts.source_locked_derivation_v5118 import checked_text


stage, base = replay.stage, replay.base
ROOT, ROM, PROOF = stage.ROOT, stage.ROM, stage.PROOF
BIOGRAPHIES = replay.prior.PREVIOUS.parent
BOOT, VISUAL = ROOT / prior.BOOT.name, ROOT / prior.VISUAL.name
LIVE, CHECKPOINT = ROOT / prior.LIVE.name, ROOT / prior.CHECKPOINT.name
QA = prior.QA
payout = SimpleNamespace(OUTPUT=ROOT / prior.payout.OUTPUT.name)


def verify_payout():
    environment = vars(prior.payout) | {'stage': stage, 'OUTPUT': payout.OUTPUT}
    FunctionType(prior.payout.main.__code__, environment)()


def approve_layout(viewed):
    source = checked_text(getsource(prior.approve_layout), {
        "assert sum(len(row['messages']) for row in proof['sheets']) == 117":
            "assert sum(len(row['messages']) for row in proof['sheets']) == 121\n"
            "    assert proof['superseded_page_IDs'] == sorted(stage.ADJUSTED)\n"
            "    assert proof['fresh_native_pages'] == 4 and proof['reused_native_pages'] == 113\n"
            "    assert proof['reused_renderer_and_selector_byte_exact']",
        'sheet_sha256=viewed, payout_amount_last_row=':
            "sheet_sha256=viewed, superseded_page_IDs=proof['superseded_page_IDs'], payout_amount_last_row=",
    })
    environment = vars(prior) | globals()
    exec(compile(source, __file__ + '::final-layout', 'exec'), environment)
    environment['approve_layout'](viewed)


def verify_startup():
    FunctionType(prior.verify_startup.__code__, vars(prior) | globals())()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('action', choices=('payout', 'layout', 'startup'))
    parser.add_argument('--viewed-sheets', nargs='+')
    args = parser.parse_args()
    if args.action == 'layout':
        approve_layout(args.viewed_sheets)
    else:
        {'payout': verify_payout, 'startup': verify_startup}[args.action]()
