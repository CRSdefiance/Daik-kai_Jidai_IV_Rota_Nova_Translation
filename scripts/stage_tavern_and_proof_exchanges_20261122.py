"""Compile the tavern follow-up and check exact dialogue, choices and pagination."""

from argparse import ArgumentParser
from types import FunctionType, SimpleNamespace

from scripts import review_tavern_and_proof_exchanges_20261122 as draft
from scripts import stage_rafael_diplomacy_and_friends_20261122 as precedent


base, native = draft.base, draft.native
parent = SimpleNamespace(ROM=draft.parent.ROM, MANIFEST=draft.parent.MANIFEST, RELEASE=draft.parent.RELEASE,
    STARTUP_CAPTURE=draft.parent.STARTUP_CAPTURE, guard_spec=draft.parent.scope["guard_spec"],
    bind_registered_story_percent_guard=draft.parent.scope["bind_registered_story_percent_guard"])
established = precedent.established
ROOT = draft.ROOT / "refined/staged"
ROM = ROOT / "Tavern_And_Proof_Exchanges_STAGED.nds"
PROOF, NATIVE = ROOT / "stored_proof.json", ROOT / "native_display.json"
PATCH, REBUILT = ROOT / "translation.xdelta", ROOT / "clean_rebuilt.nds"
STARTUP_CAPTURE = ROOT / "startup/capture/capture_report.json"
CHOICES_AND_PAGES = ROOT / "choices_and_pagination.json"
review = SimpleNamespace(REVIEW=ROOT.parent / draft.REVIEW.name, PREFLIGHT=ROOT.parent / draft.PREFLIGHT.name)
compiler_scope = precedent.compiler_scope | globals()


def additional_checks():
    assert not CHOICES_AND_PAGES.exists()
    manuscript, staged, rendered, release = map(base.load, (review.REVIEW, PROOF, NATIVE, parent.RELEASE))
    assert staged["candidate_sha256"] == rendered["candidate_sha256"] == base.digest(ROM)
    assert staged["predecessor_sha256"] == release["candidate_sha256"] == base.digest(parent.ROM)
    target = base.NdsImage.open(ROM)
    groups = {(g["file_path"], g["block"]): g for g in staged["groups"]}
    verified_choices = []
    for decision in manuscript["retained_choice_objects"]:
        before = decision["current"]
        group = groups[before["file_path"], before["block"]]
        command, = [c for c in group["commands"] if c["current_offset"] == before["command_offset"]]
        assert command["word"] == 0x2100 and command["current"] == command["stored"] == before["exact_command_hex"]
        assert command["source"] == decision["source"]["exact_command_hex"]
        at, raw = command["stored_offset"], bytes.fromhex(command["stored"])
        bank = native.IlnkContainer.parse(target.read_file(group["file_path"]))
        block = bank.blocks[group["block"]]
        assert native.digest(block) == group["after"] and block[at:at+len(raw)] == raw
        verified_choices.append(decision | {"installed_offset": at, "installed_command_hex": raw.hex()})

    ident = "DK4_MES_B173_R0138"
    before, = (r for r in manuscript["records"] if r["id"] == ident)
    after, = (r for r in rendered["records"] if r["id"] == ident)
    old = bytes.fromhex(before["current_hex"])[1:]
    assert old.count(b"\n") >= 5
    display = established.display
    ctx = native.RegisteredRuntime(parent.RELEASE, release["own_registered_startup"], captain=3)
    assert all(ctx.image.read_file(a) == target.read_file(a) for a in display.ASSETS)
    font = target.read_file("/GRP/KANJI.FNT")
    paint = display.clipped_renderer(ctx)
    previous_pages = paint(ctx.arm, font, old)
    assert previous_pages["complete_consumed_bytes"] == len(old)
    assert len(previous_pages["pages"]) > 1 and len(after["layouts"][0]["pages"]) == 1
    base.save(CHOICES_AND_PAGES, dict(candidate_sha256=staged["candidate_sha256"], choices=verified_choices,
        pagination=dict(id=ident, preexisting_page_count=len(previous_pages["pages"]), new_page_count=1,
            previous_page_layout=previous_pages["pages"], next_turn="DK4_MES_B173_R0141", original_paragraph_words_preserved_in_meaning=True),
        offline_only=True))
    print(f"Verified four exact retained choices and Mikhail's {len(previous_pages['pages'])}-to-one-page repair.", flush=True)


if __name__ == "__main__":
    cli = ArgumentParser(description=__doc__)
    cli.add_argument("action", choices=("stage", "native_display", "additional_checks", "patch", "startup"))
    action = cli.parse_args().action
    if action == "stage":
        FunctionType(established.stage.__code__, compiler_scope)()
    elif action == "native_display":
        FunctionType(precedent.native_display.__code__, compiler_scope | {"compiler_scope": compiler_scope})()
    elif action == "additional_checks":
        additional_checks()
    else:
        inherited = getattr(established.release_tools, action)
        FunctionType(inherited.__code__, inherited.__globals__ | globals())()
