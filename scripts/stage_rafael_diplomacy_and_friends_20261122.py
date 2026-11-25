"""Compile the reviewed Rafael scenes through the registered story workflow."""

from argparse import ArgumentParser
from inspect import getsource
from types import FunctionType, SimpleNamespace

from scripts import review_rafael_diplomacy_and_friends_20261122 as draft
from scripts import stage_current_story_wraps_20261122 as established
from scripts.source_locked_derivation_v5118 import checked_text


base, native, parent = draft.base, draft.native, draft.parent
ROOT = draft.ROOT / "release/staged"
ROM = ROOT / "Rafael_Diplomacy_And_Friends_STAGED.nds"
PROOF, NATIVE = ROOT / "stored_proof.json", ROOT / "native_display.json"
PATCH, REBUILT = ROOT / "translation.xdelta", ROOT / "clean_rebuilt.nds"
STARTUP_CAPTURE = ROOT / "startup/capture/capture_report.json"
review = SimpleNamespace(REVIEW=ROOT.parent / draft.REVIEW.name, PREFLIGHT=ROOT.parent / draft.PREFLIGHT.name)
compiler_scope = vars(established) | globals()


def native_display():
    # The batch changes no runtime name substitutions. The compiler and renderer
    # still compare tokens and exact bytes for every installed line.
    source = checked_text(getsource(established.native_display), {
        '    hodram = display.contexts.hodram_context()\n    routes = {1: hodram, 3: current}': '    routes = {}',
        '            if tokens:\n': '            assert not tokens\n            if tokens:\n',
    })
    namespace = compiler_scope.copy()
    exec(compile(source, __file__ + "::no_changed_name_substitutions", "exec"), namespace)
    namespace["native_display"]()


if __name__ == "__main__":
    cli = ArgumentParser(description=__doc__)
    cli.add_argument("action", choices=("stage", "native_display", "patch", "startup"))
    action = cli.parse_args().action
    if action == "native_display":
        native_display()
    elif action == "stage":
        FunctionType(established.stage.__code__, compiler_scope)()
    else:
        inherited = getattr(established.release_tools, action)
        FunctionType(inherited.__code__, inherited.__globals__ | globals())()
