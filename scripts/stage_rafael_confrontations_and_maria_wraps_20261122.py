"""Compile the reviewed Rafael scenes and observed Maria wrap repairs."""

from argparse import ArgumentParser
from types import FunctionType, SimpleNamespace

from scripts import review_rafael_confrontations_and_maria_wraps_20261122 as draft
from scripts import stage_camille_and_maria_reveals_20261122 as template


base, native = draft.base, draft.native
parent = SimpleNamespace(
    ROM=draft.parent.ROM, MANIFEST=draft.parent.MANIFEST, RELEASE=draft.parent.RELEASE,
    STARTUP_CAPTURE=draft.parent.STARTUP_CAPTURE, guard_spec=draft.parent.scope["guard_spec"],
    bind_registered_story_percent_guard=draft.parent.scope["bind_registered_story_percent_guard"],
)
established = template.established
ROOT = draft.ROOT / "staged"
ROM = ROOT / "Rafael_Confrontations_And_Maria_Wraps_STAGED.nds"
PROOF, NATIVE = ROOT / "stored_proof.json", ROOT / "native_display.json"
PATCH, REBUILT = ROOT / "translation.xdelta", ROOT / "clean_rebuilt.nds"
STARTUP_CAPTURE = ROOT / "startup/capture/capture_report.json"
review = SimpleNamespace(REVIEW=draft.REVIEW, PREFLIGHT=draft.PREFLIGHT)
compiler_scope = template.compiler_scope | globals()


if __name__ == "__main__":
    cli = ArgumentParser(description=__doc__)
    cli.add_argument("action", choices=("stage", "native_display", "patch", "startup"))
    action = cli.parse_args().action
    if action == "stage":
        FunctionType(established.stage.__code__, compiler_scope)()
    elif action == "native_display":
        renderer = template.template.precedent.native_display
        FunctionType(renderer.__code__, renderer.__globals__ | globals())()
    else:
        inherited = getattr(established.release_tools, action)
        FunctionType(inherited.__code__, inherited.__globals__ | globals())()
