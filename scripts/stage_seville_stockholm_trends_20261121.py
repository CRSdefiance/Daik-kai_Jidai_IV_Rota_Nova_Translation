"""Compile the Seville and Stockholm exchanges for focused validation."""

from types import FunctionType, SimpleNamespace

from scripts import review_seville_stockholm_trends_20261121 as review
from scripts import stage_hamburg_ceramics_cross_route_20261120 as precedent


base, native = precedent.base, precedent.native
parent = review.parent
ROOT = review.ROOT / "research_v3"
ROM = ROOT / "Seville_Stockholm_Trends_RESEARCH_ONLY.nds"
PROOF = ROOT / "stored_proof.json"
current_fe_painter = precedent.current_fe_painter


if __name__ == "__main__":
    workflow = precedent.workflow
    env = workflow.env | globals()
    env["paired"] = review
    catalogue_env = env | {"stage": workflow.stage}
    env["catalogue_membership"] = FunctionType(workflow.catalogue.catalogue_membership.__code__, catalogue_env)
    env["rebuild_function"] = precedent.aligned.rebuild_function
    env["stage"] = SimpleNamespace(system=SimpleNamespace(native_painter=current_fe_painter))
    FunctionType(workflow.env["main"].__code__, env)()
