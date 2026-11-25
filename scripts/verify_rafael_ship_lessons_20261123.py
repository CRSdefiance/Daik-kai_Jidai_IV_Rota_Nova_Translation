"""Verify the full recruitment and ship lesson stage and qualify earlier gameplay."""

from argparse import ArgumentParser
from inspect import getsource
from pathlib import Path
from types import FunctionType, SimpleNamespace

from scripts import replay_rafael_ship_lessons_20261123 as prototype
from scripts import stage_rafael_ship_lessons_20261123 as stage
from scripts.source_locked_derivation_v5118 import checked_text


base, native = stage.base, stage.native
ROOT = stage.ROOT / "focused_gameplay"
EXCERPTS = ROOT / "fresh_excerpts.json"
LIVE = ROOT / "verified_gameplay.json"
GLYPHS = stage.ROOT / "glyph_and_sheet_verification.json"
CHOICES = stage.ROOT / "original_choice_tables.json"
ROLES = stage.ROOT / "speaker_roles.json"
OLD = prototype.stage
ARCHIVE = "/data/SC0.DK4"
CONTEXT = {(176, 13), (176, 114), (176, 148), (178, 24), (178, 151), (178, 231), (178, 234)}
NOTES = {
    0: "Keep Rafael Castor in the header and the original first-name substitution in Clau's and Janus's direct addresses.",
    4: "Keep Janus Pasar as Cesare's equally curious listener and the crew member who explains the coin game's pattern.",
    5: "Keep Claudio Manaus in his header and Clau in Rafael's and Janus's familiar address.",
    11: "Keep Jam Ludwyan for the public nameplate. Preserve Jam Jack Ludwyan in the spoken introduction and J-A-M in his boast.",
    13: "Keep Cesare Tony as stated when he introduces himself. Recognizing his old ship gives him no military rank.",
    20: "Keep Fernando Dias, as he says after the successful toss. His comments about insight and luck are part of the conversation.",
    23: "Keep Manuel Almeida in the nameplate. Preserve the source's first-name-only introduction.",
    109: "Keep Shipwright for the unnamed instructor. His lesson shows the knowledge of his trade without a personal title.",
    116: "Keep Port Worker for the unnamed person who calls out that the ship has returned.",
    164: "Keep Man for the unnamed person who agrees to end the relationship. Fernando's description establishes the two as a couple.",
    165: "Keep Woman for the unnamed person who says they should stop seeing each other. The exchange gives her no formal relationship title.",
}


def sample():
    pairs = []
    for row in base.load(stage.REVIEW)["records"]:
        key = row["block"], int(row["id"].rsplit("R", 1)[1])
        if key in CONTEXT or (row["decision"] == "revision" and (
            row["block"] in (176, 178) or row["id"] == stage.LATEEN_ID
        )):
            pairs.append(key)
    return {0: tuple(pairs)}


def report(run):
    return scope["report_path"](int(run))


scope = prototype.excerpt_scope | globals() | {"LIVE": EXCERPTS}
scope["scope"] = scope
for name in ("receipt", "report_path", "run_file", "play"):
    scope[name] = FunctionType(prototype.excerpt_scope[name].__code__, scope)
fixture = checked_text(prototype.fixture_source, {
    "Rafael_Ship_Lessons_FOCUSED_ONLY.nds": "Rafael_Recruitment_And_Lessons_FOCUSED_ONLY.nds",
})
verify = checked_text(prototype.excerpt_verify, {
    '    assert {r["id"] for r in by_id.values() if r["layouts"]} <= {r["id"] for r in observations}':
        '    assert {record_id(*pair) for pair in SAMPLE[0]} == {r["id"] for r in observations}',
    "rafael_ship_lessons_excerpt_": "rafael_recruitment_excerpt_",
    "including the original armor notice": "including recruitment and coin-game dialogue",
})
for code in (fixture, verify):
    exec(compile(code, __file__ + "::focused-dialogue", "exec"), scope)


def formatting():
    code = checked_text(getsource(prototype.formatting), {
        '"len(choices) == 5": "len(choices) == 6"': '"len(choices) == 5": "len(choices) == 8"',
        "Verified all six original captions": "Verified all eight original captions",
    })
    context = vars(prototype) | globals()
    exec(compile(code, __file__ + "::complete-glyphs-and-original-controls", "exec"), context)
    context["formatting"]()


def carry_forward_gameplay():
    old, new = map(native.files, map(base.NdsImage.open, (OLD.ROM, stage.ROM)))
    assert old.keys() == new.keys() and {path for path in old if old[path] != new[path]} == {ARCHIVE}
    before, after = (native.IlnkContainer.parse(image[ARCHIVE]).blocks for image in (old, new))
    assert {i for i, (a, b) in enumerate(zip(before, after, strict=True)) if a != b} == {176, 178, 180}
    assert before[44] == after[44]
    fixture_receipt = base.load(prototype.choice_paths(180)[2])
    assert fixture_receipt["exact_inverse"] and not fixture_receipt["natural_activation"]
    assert base.digest(fixture_receipt["rom"]) == fixture_receipt["rom_sha256"]

    previous, final = map(base.load, (OLD.PROOF, stage.PROOF))
    candidate = base.digest(stage.ROM)
    assert final["candidate_sha256"] == candidate
    assert previous["candidate_sha256"] == fixture_receipt["candidate_sha256"] == base.digest(OLD.ROM)
    early = []
    for proof in (previous, final):
        commands = next(group["commands"] for group in proof["groups"] if group["block"] == 180)
        last, = [i for i, row in enumerate(commands) if "DK4_MES_B180_R0063" in row["record_ids"]]
        early.append(commands[:last+1])
    assert early[0] == early[1]
    for command in early[1]:
        at, raw = command["stored_offset"], bytes.fromhex(command["stored"])
        assert before[180][at:at+len(raw)] == after[180][at:at+len(raw)] == raw

    old_display, final_display = map(base.load, (OLD.NATIVE, stage.NATIVE))
    p, q = ({r["id"]: r for r in display["records"]} for display in (old_display, final_display))
    prior_game = base.load(prototype.LIVE)
    earlier = prior_game["excerpts"]
    assert earlier["candidate_sha256"] == old_display["candidate_sha256"] == previous["candidate_sha256"]
    assert earlier["report_sha256"]["0"] == base.digest(prototype.report("0"))
    assert prior_game["choice_reports"] == {run: base.digest(prototype.report(run)) for run in prototype.RUNS}
    retained = []
    for hold in earlier["observations"] + prior_game["choice_holds"]:
        ident = hold["id"]
        if ident == stage.LATEEN_ID:
            continue
        a, b = p[ident], q[ident]
        assert all(a[key] == b[key] for key in ("file_path", "block", "body_hex", "exact_command_hex", "layouts"))
        capture = hold["capture"]
        assert base.digest(capture["path"]) == capture["PNG_sha256"] and hold["exact_complete_body_mask"]
        retained.append(hold | dict(
            original_candidate_sha256=previous["candidate_sha256"], original_stored_offset=hold["stored_offset"],
            stored_offset=b["command_offset"], reused_exact_stored_command_and_runtime=True,
        ))
    assert len(retained) == 17
    for outcome in prior_game["choices"]:
        assert outcome["original_branch_executed"] and outcome["fixture_sha256"] == fixture_receipt["rom_sha256"]
        for menu in outcome["observations"]:
            capture = menu["capture"]
            assert base.digest(capture["path"]) == capture["PNG_sha256"]

    fresh = base.load(EXCERPTS)
    assert fresh["candidate_sha256"] == final_display["candidate_sha256"] == candidate
    assert fresh["report_sha256"]["0"] == base.digest(scope["report_path"](0))
    assert not {hold["id"] for hold in retained} & {hold["id"] for hold in fresh["observations"]}
    old_sheets = earlier["sheets"] + prior_game["choice_sheets"]
    sheets = fresh["sheets"] + old_sheets
    assert all(base.digest(row["path"]) == row["sha256"] for row in sheets)
    base.save(LIVE, fresh | dict(
        observations=fresh["observations"] + retained, sheets=sheets, reused_count=len(retained),
        original_menu_choices=prior_game["choices"], carried_gameplay={str(prototype.LIVE):base.digest(prototype.LIVE)},
        carried_report_sha256=earlier["report_sha256"] | prior_game["choice_reports"],
        original_sailing_menu_prefix_byte_exact=True, initialization_block_byte_exact=True,
        prior_and_current_runtime_components_equal=True,
    ))
    print(f"Verified {len(fresh['observations'])} fresh holds, {len(retained)} exact prior holds and both sailing outcomes.")


def names():
    labels = prototype.prior.names
    context = labels.scope | dict(PROOF=ROLES, NOTES=NOTES, parent=stage.parent,
        stage=SimpleNamespace(OUTPUT=stage.REVIEW, PROOF=stage.PROOF, ROM=stage.ROM),
        display=SimpleNamespace(PROOF=stage.NATIVE), live_receipt=LIVE)
    exec(compile(labels.source, __file__ + "::original-name-consumers", "exec"), context)
    context["main"]()


if __name__ == "__main__":
    cli = ArgumentParser(description=__doc__)
    cli.add_argument("action", choices=("formatting", "replay", "verify", "names"))
    action = cli.parse_args().action
    if action in ("replay", "verify"):
        scope["SAMPLE"] = sample()
        if action == "replay":
            scope["fixture"](0)
            scope["play"](0)
        else:
            if not EXCERPTS.exists():
                scope["verify"]()
            carry_forward_gameplay()
    else:
        globals()[action]()
