"""Check proposed and retained speakerless panels on the registered renderer."""

from pathlib import Path
import re

from PIL import Image, ImageDraw

from scripts import check_rafael_B166_staged_FE_v7 as layout
from scripts import register_rafael_homeland_and_maps_20261121 as parent
from scripts import verify_rafael_palace_and_alliance_20261121 as prior
from scripts.source_locked_derivation_v5118 import checked_text


ROOT = Path("work/analysis/rafael_B161_B169_followup_20261121")
DRAFTS = [ROOT / f"{name}_final_candidate.json" for name in (
    "B161_contextual_decisions", "B166_contextual_decisions_v4",
)]
PAIRS = ROOT / "paired_source_final_candidate.json"
OUT = ROOT / "speakerless_panel_preflight_v2"
base, native = parent.base, prior.native
TOKEN = re.compile(rb"F[AIOU]")
WIDE_NAME = b"WWWWWWWWWWWWWWWW"


def expansions(ctx):
    library = layout.native
    adapter = checked_text(base.load(library.MACROS)["source_owned_FE_adapter"], {
        "b'Hodram'": "b'Rafael'", "b'Bergstrom'": "b'Castor'",
        "b'Bergstrom Fleet'": "b'Castor Co.'",
    })
    env = dict(library.FE_expand.__globals__)
    exec(compile(adapter, __file__ + "::original-FE-expansion", "exec"), env)

    def expand(body):
        cases = ctx.execute(env["expand"], body)["cases"]
        observed = {c["output_hex"] for c in cases}
        assert len(cases) == 4 and observed == {layout.expand(body).hex()}
        return layout.expand(body), cases

    return expand


def planned_shapes(row):
    index = row["source_record_index"]
    text = row["english"]
    if index in layout.HEADINGS:
        shapes = layout.source_shapes(index, text)
    else:
        # Reserve the full 16 cells of a customizable given name at wrap time.
        logical = text.replace("FI", WIDE_NAME.decode("ascii"))
        shapes = [[(0, line.replace(WIDE_NAME.decode("ascii"), "{MACRO:FI}")) for line in lines]
                  for lines in layout.wrap_options(logical, 4)]
    for shape in shapes:
        rows = [line.replace("{MACRO:FI}", "FI") for _, line in shape]
        assert " ".join(rows) == text
        if all(any(phrase in line for line in rows) for phrase in row["protected_phrases"]):
            yield shape


def expected_rows(shape, actor):
    return [(index * 12, x, line.replace("{MACRO:FI}", actor))
            for index, (x, line) in enumerate(shape) if line]


def paint(painter, body):
    view = painter(body)
    assert view["complete_consumed_bytes"] == len(body)
    assert len(view["physical"]) == 228 * 64
    rows = layout.actual_rows(view["events"])
    return rows, view["physical"]


def plan(row, raw, painter):
    for shape in planned_shapes(row):
        expected = expected_rows(shape, "Rafael")
        for body in layout.candidates(row, row["source_record_index"], shape):
            assert TOKEN.findall(body) == TOKEN.findall(raw)
            # Recheck the allocation-parity pad the stored speech writer adds.
            encoded = body + b" " * ((len(body) ^ len(raw)) & 1)
            try:
                actual, plane = paint(painter, layout.expand(encoded))
                if actual != expected:
                    continue
                if b"FI" in encoded:
                    stress = encoded.replace(b"FI", WIDE_NAME)
                    test, _ = paint(painter, stress)
                    if test != expected_rows(shape, WIDE_NAME.decode("ascii")):
                        continue
            except AssertionError:
                continue
            return body, encoded, actual, plane
    raise AssertionError(row["id"])


def make_sheets(pictures):
    sheets = []
    for start in range(0, len(pictures), 8):
        part = pictures[start:start + 8]
        sheet = Image.new("RGB", (920, 154 * ((len(part) + 1) // 2)), "#263238")
        draw = ImageDraw.Draw(sheet)
        for i, (label, plane) in enumerate(part):
            x, y = (i % 2) * 460, (i // 2) * 154
            draw.text((x + 4, y + 3), label, fill="white")
            panel = Image.new("RGB", (228, 64))
            panel.putdata([(0, 8, 0) if ink else (239, 232, 201) for ink in plane])
            sheet.paste(panel.resize((456, 128), Image.Resampling.NEAREST), (x, y + 20))
        path = OUT / f"panels_{start // 8 + 1}.png"
        sheet.save(path)
        sheets.append(dict(path=str(path), sha256=base.digest(path), panels=[label for label, _ in part]))
    return sheets


def main():
    assert not OUT.exists()
    release = base.load(parent.RELEASE)
    pair = base.load(PAIRS)
    assert base.digest(parent.ROM) == release["candidate_sha256"] == pair["candidate_sha256"]
    deps = base.load(parent.display.PROOF)["initialized_dependencies"]
    assert all(base.digest(deps[key]) == deps[key + "_sha256"] for key in ("release_proof", "startup_proof"))
    ctx = native.RegisteredRuntime(deps["release_proof"], deps["startup_proof"], captain=0)
    image = base.NdsImage.open(parent.ROM)
    assets = {path: native.digest(image.read_file(path)) for path in prior.display.ASSETS}
    assert assets == {path: native.digest(ctx.image.read_file(path)) for path in assets}
    picker = prior.town.current_fe_painter(ctx)
    expand = expansions(ctx)
    anchors = {r["id"]: r for r in base.load(layout.SOURCE_ANCHORS)["staged"]}
    previous = {r["id"]: r for r in base.load(layout.OUT / "staged_display.json")["records"]}
    assert set(previous) == set(anchors) and len(anchors) == 22
    bank = native.IlnkContainer.parse(image.read_file(prior.PATH)).blocks
    clean = base.NdsImage.open(Path("work/clean.nds"))
    assert base.digest(Path("work/clean.nds")) == pair["clean_sha256"]
    clean_bank = native.IlnkContainer.parse(clean.read_file(prior.PATH)).blocks
    proofs, pictures = [], []
    for draft_path in DRAFTS:
        draft = base.load(draft_path)
        assert draft["candidate_sha256"] == pair["candidate_sha256"]
        for row in draft["records"]:
            if row["source_selector"] != 254:
                continue
            ident, block = row["id"], row["block"]
            references = [row[key + "_reference"] for key in ("source", "current")]
            source, current = (bytes.fromhex(ref["exact_body_hex"]) for ref in references)
            for ref, archive, body in zip(references, (clean_bank, bank), (source, current), strict=True):
                assert native.digest(archive[block]) == ref["block_sha256"]
                assert ref["offset"] == ref["command_offset"] + 5
                assert archive[block][ref["command_offset"]:ref["offset"] + 1 + len(body)] == b"\x00\x40\xff\xff\x00\xfe" + body
            origin, _ = paint(picker, expand(current)[0])
            special = anchors.get(ident)
            if special:
                assert [int(ident[-4:]), special["id"]] == [row["source_record_index"], ident]
                assert special["source_reference"]["offset"] == references[0]["offset"]
                assert special["source_reference"]["header_offset"] == references[0]["command_offset"]
                assert special["source_reference"]["length"] == len(source) + 1
                retained_rows = [tuple(line) for line in previous[ident]["planned_visible_rows"]]
                if row["decision"] == "retention":
                    assert origin == retained_rows, (ident, origin, retained_rows)
            if row["decision"] == "revision":
                body, stored, rows, plane = plan(row, current, picker)
            else:
                assert row["decision"] == "retention"
                body = stored = current
                rows, plane = paint(picker, layout.expand(stored))
            if b"FI" in stored:
                stress, _ = paint(picker, stored.replace(b"FI", WIDE_NAME))
                assert stress == [(y, x, text.replace("Rafael", WIDE_NAME.decode("ascii")))
                                  for y, x, text in rows]
            expanded, cases = expand(stored)
            proofs.append(dict(id=ident, decision=row["decision"], source_reference=references[0],
                current_reference=references[1], source_anchor=special and special["observations"]["source"],
                previous_rows=origin, rows=rows, english=row["english"],
                compiled_hex=(b"\xfe" + body).hex(), expected_stored_hex=(b"\xfe" + stored).hex(),
                expanded_hex=expanded.hex(), macro_alignment_cases=cases,
                longest_given_name_rendered=b"FI" in stored, plane_sha256=native.digest(plane)))
            pictures.append((ident + "  " + row["decision"], plane))
    assert len(proofs) == 30 and sum(r["decision"] == "revision" for r in proofs) == 3
    OUT.mkdir()
    evidence = [PAIRS, *DRAFTS, layout.SOURCE_ANCHORS, layout.OUT / "staged_display.json",
                parent.RELEASE, parent.display.PROOF, Path(__file__)]
    base.save(OUT / "native_speakerless_preflight.json", dict(
        parent_sha256=pair["candidate_sha256"], initialized_dependencies=deps, exact_runtime_assets=assets,
        evidence={str(path): base.digest(path) for path in evidence}, records=proofs,
        sheets=make_sheets(pictures), offline_preflight=True, candidate_storage_and_gameplay_pending=True,
    ))
    print("30 speakerless panels passed native preflight, including 3 revisions.")


if __name__ == "__main__":
    main()
