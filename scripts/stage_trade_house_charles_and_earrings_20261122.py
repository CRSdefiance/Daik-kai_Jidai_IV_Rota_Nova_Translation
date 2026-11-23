"""Stage the editorial changes and verify their stored controls and native display."""

from argparse import ArgumentParser
from inspect import getsource
from pathlib import Path
from types import FunctionType, SimpleNamespace

from scripts import review_trade_house_charles_and_earrings_20261122 as draft
from scripts import stage_rafael_confrontations_and_maria_wraps_20261122 as template
from scripts.source_locked_derivation_v5118 import checked_text


base, native, established = draft.base, draft.native, template.established
parent = SimpleNamespace(
    ROM=draft.parent.ROM, MANIFEST=draft.parent.MANIFEST, RELEASE=draft.parent.RELEASE,
    STARTUP_CAPTURE=draft.parent.STARTUP_CAPTURE, guard_spec=draft.parent.scope["guard_spec"],
    bind_registered_story_percent_guard=draft.parent.scope["bind_registered_story_percent_guard"],
)
ROOT = draft.ROOT / "staged"
ROM = ROOT / "Trade_House_Charles_And_Earrings_STAGED.nds"
PROOF, NATIVE = ROOT / "stored_proof.json", ROOT / "native_display.json"
PATCH, REBUILT = ROOT / "translation.xdelta", ROOT / "clean_rebuilt.nds"
STARTUP_CAPTURE = ROOT / "startup/capture/capture_report.json"
CHOICE_PROOF = ROOT / "unchanged_choice_proof.json"
review = SimpleNamespace(REVIEW=draft.REVIEW, PREFLIGHT=draft.PREFLIGHT)
compiler_scope = template.compiler_scope | globals()
renderer_source = checked_text(getsource(established.native_display), {
    '    hodram = display.contexts.hodram_context()\n    routes = {1: hodram, 3: current}':
        '''    context = base.load(display.build.parent.display.PROOF)["previous_initialized_rafael_context"]
    boot, identity = map(Path, (context["path"], context["identity"]))
    assert base.digest(boot) == context["sha256"] and base.digest(identity) == context["identity_sha256"]
    routes = {0: native.RegisteredRuntime(identity, boot, captain=0)}''',
    '{1: "Hodram", 3: "Maria"}[route]': '"Rafael"',
    'captain in (1,3)': 'captain == 0',
    '                if route == 1:': '                if route == 0:',
})
exec(compile(renderer_source, __file__ + "::Rafael-substitutions", "exec"), compiler_scope)


def verify_choices():
    manuscript, stored = map(base.load, (review.REVIEW, PROOF))
    assert base.digest(ROM) == stored["candidate_sha256"]
    path = "/data/SC1.DK4"
    group, = (g for g in stored["groups"] if g["file_path"] == path)
    block = native.IlnkContainer.parse(base.NdsImage.open(ROM).read_file(path)).blocks[group["block"]]
    assert native.digest(block) == group["after"]
    choices = []
    for row in manuscript["retained_choice_objects"]:
        old = row["current"]
        command, = (c for c in group["commands"] if c["current_offset"] == old["command_offset"])
        assert command["word"] == 0x2100
        assert command["source"] == row["source"]["exact_command_hex"]
        assert command["current"] == command["stored"] == old["exact_command_hex"]
        at, raw = command["stored_offset"], bytes.fromhex(command["stored"])
        assert block[at:at+len(raw)] == raw
        choices.append(row | dict(installed_offset=at, installed_command_hex=raw.hex(),
                                  installed_block_sha256=group["after"]))
    assert len(choices) == 2
    base.save(CHOICE_PROOF, dict(candidate_sha256=stored["candidate_sha256"], offline_exact=True, choices=choices))


if __name__ == "__main__":
    cli = ArgumentParser(description=__doc__)
    cli.add_argument("action", choices=("stage", "native_display", "patch", "startup", "choices"))
    action = cli.parse_args().action
    if action == "stage":
        FunctionType(established.stage.__code__, compiler_scope)()
    elif action == "native_display":
        compiler_scope["native_display"]()
    elif action == "choices":
        verify_choices()
    else:
        inherited = getattr(established.release_tools, action)
        FunctionType(inherited.__code__, inherited.__globals__ | globals())()
