"""Check the staged Mediterranean refinements with native rendering and gameplay."""

from argparse import ArgumentParser
from inspect import getsource
from types import FunctionType, SimpleNamespace

from scripts import preflight_rafael_B161_B169_FE_20261121 as modal
from scripts import stage_rafael_mediterranean_followups_20261123 as stage
from scripts import verify_rafael_ship_lessons_20261123 as prior
from scripts.source_locked_derivation_v5118 import checked_text


base, native = stage.base, stage.native
ROOT = stage.ROOT / "focused_gameplay"
LIVE = ROOT / "verified_gameplay.json"
ROLES = stage.ROOT / "speaker_roles.json"
GLYPHS = stage.ROOT / "glyph_and_sheet_verification.json"
MODAL_SAMPLE = "DK4_MES_B166_R0237"


def sample():
    records = base.load(stage.REVIEW)["records"]
    return {0: tuple((r["block"], int(r["id"].rsplit("R", 1)[1]))
                     for r in records if r["decision"] == "revision" or r["id"] == MODAL_SAMPLE)}


def report(run):
    return scope["report_path"](int(run))


scope = prior.scope | globals()
scope["scope"] = scope
for name in ("receipt", "report_path", "run_file", "play"):
    scope[name] = FunctionType(prior.scope[name].__code__, scope)
verify = checked_text(prior.verify, {
    "rafael_recruitment_excerpt_": "rafael_mediterranean_excerpt_",
    "including recruitment and coin-game dialogue": "including the move from Claudio’s portrait to Eirene’s speakerless reply",
})
fixture = checked_text(prior.fixture, {
    "Rafael_Recruitment_And_Lessons_FOCUSED_ONLY.nds": "Rafael_Mediterranean_Followups_FOCUSED_ONLY.nds",
})
for code in (fixture, verify):
    exec(compile(code, __file__ + "::focused-dialogue", "exec"), scope)


def formatting():
    if not GLYPHS.exists():
        glyphs = prior.prototype.prior.display.verification.glyphs
        FunctionType(glyphs.verify.__code__, vars(glyphs) | dict(stage=stage, OUTPUT=GLYPHS))()
    staged, draft, release = map(base.load, (stage.PROOF, stage.REVIEW, stage.parent.RELEASE))
    candidate = base.digest(stage.ROM)
    assert staged["candidate_sha256"] == candidate and staged["draft_sha256"] == base.digest(stage.REVIEW)
    assert staged["predecessor_sha256"] == release["candidate_sha256"]
    ctx = native.RegisteredRuntime(stage.parent.RELEASE, release["own_registered_startup"], captain=3)
    image = base.NdsImage.open(stage.ROM)
    assert all(ctx.image.read_file(p) == image.read_file(p) for p in stage.established.display.ASSETS)
    bank = native.IlnkContainer.parse(image.read_file(stage.ARCHIVE)).blocks
    paint = modal.prior.town.current_fe_painter(ctx)
    # The saved registered startup belongs to Maria. Check its actual macro
    # output, then compare Rafael's projected rows to their registered proof.
    expansion_source = checked_text(getsource(modal.expansions), {
        '"b\'Hodram\'": "b\'Rafael\'", "b\'Bergstrom\'": "b\'Castor\'",':
            '"b\'Hodram\'": "b\'Maria\'", "b\'Bergstrom\'": "b\'Li\'",',
        '"b\'Bergstrom Fleet\'": "b\'Castor Co.\'",': '"b\'Bergstrom Fleet\'": "b\'Li Fleet\'",',
        "layout.expand(body)": 'body.replace(b"FI", b"Maria")',
    })
    expansion_context = vars(modal).copy()
    exec(compile(expansion_source, __file__ + "::registered-Maria-FE-ABI", "exec"), expansion_context)
    expand = expansion_context["expansions"](ctx)

    witnesses, sources = {}, {}
    for package, blocks in stage.PACKETS.items():
        if not {166, 170}.intersection(blocks):
            continue
        folder = stage.parent.PACKAGE.with_name(package)
        path = folder / "verification/refreshed_native_display.json"
        sha = base.load(folder / "checksums.json")["verification/refreshed_native_display.json"]
        assert base.digest(path) == sha
        sources[str(path)] = sha
        for row in base.load(path)["records"]:
            if row["block"] in blocks and row.get("system"):
                witnesses[row["id"]] = row

    records, pictures = [], []
    owners = {r["id"]: r for r in draft["records"] if r["source_selector"] == 254}
    for group in staged["groups"]:
        block = group["block"]
        payload = bank[block]
        assert native.digest(payload) == group["after"]
        for command in group["commands"]:
            raw = bytes.fromhex(command["stored"])
            if command["word"] != 0x4000 or raw[5] != 254:
                continue
            ident, = command["record_ids"]
            row = owners.pop(ident)
            earlier = witnesses.pop(ident)
            (historical,), (system,) = earlier["stored_pages"], earlier["system"]
            at = command["stored_offset"]
            assert row["decision"] == "retention" and raw[:6] == bytes.fromhex("0040ffff00fe")
            assert payload[at:at + len(raw)] == raw == bytes.fromhex(command["current"])
            assert raw == bytes.fromhex(historical["stored"])
            stored = raw[6:raw.index(0, 6)]
            assert b"\xfe" + stored == bytes.fromhex(earlier["body_hex"])
            assert set(modal.TOKEN.findall(stored)) <= {b"FI"}
            actual, cases = expand(stored)
            assert actual == stored.replace(b"FI", b"Maria")
            expanded = modal.layout.expand(stored)
            rows, plane = modal.paint(paint, expanded)
            assert expanded.hex() == system["expanded_hex"]
            assert [list(line) for line in rows] == system["row_proof"]
            assert native.digest(plane) == system["plane_sha256"]
            if b"FI" in stored:
                wide_rows, _ = modal.paint(paint, stored.replace(b"FI", modal.WIDE_NAME))
                assert wide_rows == [(y, x, text.replace("Rafael", modal.WIDE_NAME.decode("ascii")))
                                     for y, x, text in rows]
            pictures.append((ident, plane))
            records.append(dict(route=0, block=block, id=ident, second_page=False, stored_offset=at,
                exact_command_hex=raw.hex(), visual_rows=rows, expanded_hex=expanded.hex(), macro_cases=cases,
                macro_test_protagonist="Maria", projected_protagonist="Rafael",
                physical_plane_hex=plane.hex(), physical_plane_sha256=native.digest(plane),
                prior_owner_plane_equal=True))
    assert len(records) == 31 and not owners and not witnesses
    directory = stage.ROOT / "retained_FE"
    directory.mkdir(exist_ok=True)
    make_sheets = FunctionType(modal.make_sheets.__code__, modal.make_sheets.__globals__ | {"OUT": directory})
    sheets = make_sheets(pictures)
    base.save(stage.FE_PROOF, dict(candidate_sha256=candidate, records=records, sheets=sheets,
        prior_registered_layouts=sources, original_modal_consumer=True, complete_stored_page_count=len(records)))
    print("Verified the 31 original speakerless panels against their exact owner-specific 228-pixel layouts.")


def names():
    selected = {r["source_selector"]: r["speaker"] for r in base.load(stage.REVIEW)["records"]
                if r["source_selector"] != 254}
    notes, references = {}, {}
    for package in stage.PACKETS:
        folder = stage.parent.PACKAGE.with_name(package)
        name = "speaker_roles.json" if package == stage.parent.PACKAGE.name else "speaker_labels.json"
        path = folder / "verification" / name
        checksum = base.load(folder / "checksums.json")[f"verification/{name}"]
        assert base.digest(path) == checksum
        references[str(path)] = checksum
        for row in base.load(path)["records"]:
            actor = row["actor_ID"]
            if actor in selected:
                progressive, catalogue = row["native_getters"]
                assert progressive["text"] == selected[actor]
                assert catalogue["text"]
                notes.setdefault(actor, row["localization_note"])
    assert len(notes) == 29 and selected.keys() == notes.keys()
    labels = prior.prototype.prior.names
    context = labels.scope | dict(PROOF=ROLES, NOTES=notes, parent=stage.parent, prior_role_receipts=references,
        stage=SimpleNamespace(OUTPUT=stage.REVIEW, PROOF=stage.PROOF, ROM=stage.ROM),
        display=SimpleNamespace(PROOF=stage.NATIVE), live_receipt=LIVE)
    code = checked_text(labels.source, {
        "offline_native_getters_only=True, new_editorial_credit=0":
            "offline_native_getters_only=True, new_editorial_credit=0, prior_role_receipts=prior_role_receipts",
    })
    exec(compile(code, __file__ + "::speaker-and-catalogue-names", "exec"), context)
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
            scope["verify"]()
    else:
        globals()[action]()
