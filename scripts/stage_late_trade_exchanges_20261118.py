"""Compile the late trade exchanges on the exact registered candidate."""

from inspect import getsource
from types import FunctionType

from scripts import review_late_trade_exchanges_20261118 as review
from scripts import stage_ruins_clues_and_guides_20261118 as inherited
from scripts.source_locked_derivation_v5118 import checked_text

paired = review.paired
previous = inherited.previous
base, native, stage, parent = previous.base, previous.native, previous.stage, review.parent
logical_end = stage.logical_end
ROOT = paired.ROOT / "research_v3"
ROM = ROOT / "Late_Trade_Exchanges_RESEARCH_ONLY.nds"
PROOF = ROOT / "stored_proof.json"
MAX_COMPANY_CELLS = 20
planner_scope = vars(previous) | {"MAX_COMPANY_CELLS": MAX_COMPANY_CELLS}
source = checked_text(getsource(previous.plan_progressive), {
    'return text.replace("{MACRO:FA}", "W" * 16).replace("{MACRO:FI}", "W" * 16)':
        '''return (text.replace("{MACRO:FA}", "W" * 16)
                    .replace("{MACRO:FI}", "W" * 16)
                    .replace("{MACRO:FO}", "W" * MAX_COMPANY_CELLS))''',
    'maximum_expanded_FI_FA_length=16)': 'maximum_expanded_FI_FA_length=16, maximum_expanded_FO_length=MAX_COMPANY_CELLS)',
})
exec(compile(source, __file__ + "::bounded-company-name", "exec"), planner_scope)
plan_progressive = planner_scope["plan_progressive"]


def rebuild_function():
    scope = vars(stage) | {"plan_progressive": plan_progressive, "plan_fe": inherited.plan_fe}
    for fn in (stage.changed_speech, stage.changed_styles, stage.rebuild):
        scope[fn.__name__] = FunctionType(fn.__code__, scope)
    return scope["rebuild"]


if __name__ == "__main__":
    FunctionType(previous.main.__code__, vars(previous) | globals())()
