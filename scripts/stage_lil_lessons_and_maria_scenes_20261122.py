"""Compile the Lil and Maria edits and prove the retained menus and system text."""

from argparse import ArgumentParser
from inspect import getsource
from types import FunctionType, SimpleNamespace

from scripts import review_lil_lessons_and_maria_scenes_20261122 as draft
from scripts import stage_tavern_and_proof_exchanges_20261122 as precedent
from scripts.source_locked_derivation_v5118 import checked_text


base, native = draft.base, draft.native
parent = SimpleNamespace(ROM=draft.parent.ROM, MANIFEST=draft.parent.MANIFEST, RELEASE=draft.parent.RELEASE,
    STARTUP_CAPTURE=draft.parent.STARTUP_CAPTURE, guard_spec=draft.parent.scope["guard_spec"],
    bind_registered_story_percent_guard=draft.parent.scope["bind_registered_story_percent_guard"])
established = precedent.established
ROOT = draft.ROOT / "release/staged"
ROM = ROOT / "Lil_Lessons_And_Maria_Scenes_STAGED.nds"
PROOF, NATIVE = ROOT / "stored_proof.json", ROOT / "native_display.json"
PATCH, REBUILT = ROOT / "translation.xdelta", ROOT / "clean_rebuilt.nds"
STARTUP_CAPTURE = ROOT / "startup/capture/capture_report.json"
CHOICES_AND_FE = ROOT / "choices_and_system_notices.json"
review = SimpleNamespace(REVIEW=ROOT.parent / draft.REVIEW.name, PREFLIGHT=ROOT.parent / draft.PREFLIGHT.name)
compiler_scope = precedent.compiler_scope | globals()

renderer_source = checked_text(getsource(established.native_display), {
    '    hodram = display.contexts.hodram_context()\n    routes = {1: hodram, 3: current}':
        '    lil = display.contexts.routes.lil_context()\n    routes = {2: lil}',
    '{1: "Hodram", 3: "Maria"}[route]': '"Lil"',
    'captain in (1,3)': 'captain == 2',
    '                if route == 1:\n': '                if route == 2:\n',
})
exec(compile(renderer_source, __file__ + "::Lil-native-context", "exec"), compiler_scope)


def additional_checks():
    assert not CHOICES_AND_FE.exists()
    manuscript, staged, report = map(base.load, (review.REVIEW, PROOF, NATIVE))
    candidate = base.digest(ROM)
    assert candidate == staged["candidate_sha256"] == report["candidate_sha256"]
    assert staged["predecessor_sha256"] == base.digest(parent.ROM)
    target = base.NdsImage.open(ROM)
    banks = {p: native.IlnkContainer.parse(target.read_file(p)).blocks for p in staged["archive_hashes"]}
    groups = {(g["file_path"], g["block"]): g for g in staged["groups"]}
    verified_choices = []
    for decision in manuscript["retained_choice_objects"]:
        before = decision["current"]
        path, number = before["file_path"], before["block"]
        group = groups[path, number]
        command, = (c for c in group["commands"] if c["current_offset"] == before["command_offset"])
        assert command["word"] == 0x2100 and command["current"] == command["stored"] == before["exact_command_hex"]
        assert command["source"] == decision["source"]["exact_command_hex"]
        at, raw = command["stored_offset"], bytes.fromhex(command["stored"])
        block = banks[path][number]
        assert native.digest(block) == group["after"] and block[at:at+len(raw)] == raw
        verified_choices.append(decision | {"installed_offset": at, "installed_command_hex": raw.hex()})
    checked = {(r["file_path"], r["id"]): r for r in report["records"]}
    controls = []
    for row in (r for r in manuscript["records"] if r["source_selector"] == 254):
        path, ident, number = (row[k] for k in ("file_path", "id", "block"))
        original = row["current_reference"]
        entry = checked.get((path, ident), original)
        raw = bytes.fromhex(entry["exact_command_hex"])
        at = entry["command_offset"]
        assert raw[5] == 254 and raw.hex() == original["exact_command_hex"]
        assert row["decision"] == "retention" and banks[path][number][at:at+len(raw)] == raw
        controls.append(dict(id=ident, file_path=path, block=number, offset=at, installed_command_hex=raw.hex()))
    assert len(verified_choices) == len(controls) == 3
    base.save(CHOICES_AND_FE, dict(candidate_sha256=candidate, choices=verified_choices, retained_FE=controls,
        original_controls_and_payloads_exact=True, offline_only=True))
    print("Verified three exact choice objects and three retained FE panels.", flush=True)


if __name__ == "__main__":
    cli = ArgumentParser(description=__doc__)
    cli.add_argument("action", choices=("stage", "native_display", "additional_checks", "patch", "startup"))
    action = cli.parse_args().action
    if action == "stage":
        FunctionType(established.stage.__code__, compiler_scope)()
    elif action == "native_display":
        compiler_scope["native_display"]()
    elif action == "additional_checks":
        additional_checks()
    else:
        inherited = getattr(established.release_tools, action)
        FunctionType(inherited.__code__, inherited.__globals__ | globals())()
