"""Verify reformatted Deck lesson pages and replay them in the initialized Rafael route."""

from argparse import ArgumentParser
from inspect import getsource
from types import FunctionType

from scripts import replay_rafael_early_phrase_wraps_20261118 as rehearsal
from scripts import replay_sea_event_dialogue_followup_20261118 as startup_driver
from scripts import stage_rafael_deck_lesson_20261119 as build
from scripts import verify_london_guild_assignments_20261118 as display
from scripts import verify_sea_event_dialogue_followup_20261118 as startup_verifier
from scripts.source_locked_derivation_v5118 import checked_text

base, native = build.base, build.native
ROOT = build.ROOT / "native_display_v1"
PROOF = ROOT / "native_display.json"
R_ROOT = build.ROOT / "initialized_replay"
ROM = R_ROOT / "Rafael_Deck_Lesson_Excerpt_RESEARCH_ONLY.nds"
SETUP, LIVE = R_ROOT / "rafael_fixture.json", R_ROOT / "verified.json"
RAFAEL = ((43, (11, 14, 17, 20, 23, 30, 33, 37, 40)),)
STARTUP_DIR = build.ROOT / "startup_fixture"
STARTUP = build.ROOT / "own_startup_verification.json"


def offline():
    assert not ROOT.exists()
    stored, draft = map(base.load, (build.PROOF, build.review.OUTPUT))
    assert stored["candidate_sha256"] == base.digest(build.ROM)
    assert stored["manuscript_sha256"] == base.digest(build.review.OUTPUT) and stored["whole_parent_inverse"]
    target, before = map(base.NdsImage.open, (build.ROM, build.parent.ROM))
    assets = (native.ARM, "/COMMON/MESFILE.DK4", "/GRP/KANJI.FNT")
    assert all(target.read_file(p) == before.read_file(p) for p in assets)
    arm, _, font = (target.read_file(p) for p in assets)
    _, paint = display.inherited.early.prior.precedent.planners(arm)
    group, = stored["groups"]
    archive = native.IlnkContainer.parse(target.read_file(group["file_path"]))
    block = archive.blocks[43]
    assert native.digest(block) == group["after"]
    commands = {ident: c for c in group["commands"] for ident in c["record_ids"]}
    pictures, records = [], []
    for row in draft["records"]:
        ident = row["id"]
        command = commands[ident]
        offset = command["stored_offset"]
        raw = bytes.fromhex(command["stored"])
        current = bytes.fromhex(command["current"])
        assert block[offset:offset+len(raw)] == raw
        assert raw[:6] == current[:6] and raw[5] == row["source_selector"]
        data = raw[5:raw.index(0, 6)]
        entry = dict(id=ident, file_path=group["file_path"], exact_stored_hex=data.hex(),
                     current_reference=command, decision=row["decision"])
        if row["decision"] == "retention":
            assert command["stored"] == command["current"] and data.hex() == row["current_hex"]
        else:
            plan = group["plans"][ident]
            assert data in (bytes.fromhex(plan["encoded_hex"]), bytes.fromhex(plan["encoded_hex"]) + b" ")
            assert not build.review.TOKEN.findall(row["english"]) and data[1:].isascii()
            issues = plan["diagnostics"]
            assert all(i["severity"] == "warning" and i["code"] == "line-break-count" for i in issues)
            rendered = paint(arm, font, data[1:])
            assert rendered["complete_consumed_bytes"] == len(data) - 1
            page, = rendered["pages"]
            assert page["native_independent_plane_equal"] and page["first_visible_origin"] == [0, 0]
            assert display.inherited.visible_lines(page) == plan["lines"]
            old = paint(arm, font, current[6:current.index(0, 6)])
            entry.update(page=page, lines=plan["lines"], source_row_count_notes=issues,
                         pagination=[len(old["pages"]), 1], stored_command_allocation=len(raw))
            pictures.append((ident, bytes.fromhex(page["native_plane_hex"])))
        records.append(entry)
    assert len(records) == len(commands) == 12 and len(pictures) == 7
    ROOT.mkdir()
    contact = display.inherited.early.contact_sheets
    sheets = FunctionType(contact.__code__, contact.__globals__ | {"ROOT": ROOT})(pictures)
    base.save(PROOF, dict(candidate_sha256=stored["candidate_sha256"], stage_proof_sha256=base.digest(build.PROOF),
                         records=records, contact_sheets=sheets, offline_only=True))
    print("Seven revised pages match the native font and bounds; five exact retentions carry forward.")


def run_rehearsal(action):
    scope = vars(rehearsal.excerpt) | globals() | {"stage": build}
    if action == "prepare":
        FunctionType(rehearsal.excerpt.prepare.__code__, scope)("rafael")
    elif action == "capture":
        FunctionType(rehearsal.excerpt.capture.__code__, scope)("rafael")
    else:
        result = FunctionType(rehearsal.masks.verify_one.__code__, vars(rehearsal.masks) | {"stage": build})(
            R_ROOT, ROM, SETUP, "Rafael", "Castor", 9)
        assert result["candidate_sha256"] == base.digest(build.ROM)
        assert [h["page"] for h in result["holds"]] == [1] * 9
        assert b"Rafael" in bytes.fromhex(result["holds"][2]["body_hex"])
        assert result["exact_native_panel_masks"] and result["hardware"] is False


def startup():
    FunctionType(startup_driver.startup.__code__, vars(startup_driver) | {"stage": build, "STARTUP": STARTUP_DIR})()
    source = checked_text(getsource(startup_verifier.startup), {
        '"proof[\'parent_sha256\']"': '"proof[\'predecessor_sha256\']"',
    })
    bindings = vars(startup_verifier) | {
        "stage": build, "replay": type("Capture", (), {"STARTUP": STARTUP_DIR}), "STARTUP": STARTUP,
        "__file__": __file__,
    }
    exec(compile(source, __file__ + "::fresh-startup", "exec"), bindings)
    bindings["startup"]()


if __name__ == "__main__":
    parser = ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=("offline", "prepare", "capture", "verify", "startup"))
    action = parser.parse_args().action
    if action == "offline":
        offline()
    elif action == "startup":
        startup()
    else:
        run_rehearsal(action)
