"""Prefer fuller rows for the reviewed Hodram paragraphs."""

from inspect import getsource
from types import FunctionType, SimpleNamespace

from scripts import stage_hodram_opening_20261122 as opening
from scripts.source_locked_derivation_v5118 import checked_text


def bind_planner():
    layout = opening.layout
    binder = checked_text(getsource(layout.bind_planner), {
        'sparse_fragment = int(not terminal and not final and length<12)':
            'sparse_fragment = max(0, 24 - length) ** 2 * (not final)',
        'cost[2]+sparse_fragment,cost[3]+mid_sentence_page,cost[4]+1,cost[5]+weak':
            'cost[2]+mid_sentence_page,cost[3]+1,cost[4]+sparse_fragment,cost[5]+weak',
    })
    env = vars(layout).copy()
    exec(compile(binder, __file__ + "::density", "exec"), env)
    density_layout = SimpleNamespace(prior=layout.prior, bind_planner=env["bind_planner"])
    return FunctionType(opening.hodram_planner.__code__,
                        opening.hodram_planner.__globals__ | {"layout": density_layout})()


original = opening.plan_progressive
qualified_plan = FunctionType(original.__code__, original.__globals__ | {"PLANNER": bind_planner()})

