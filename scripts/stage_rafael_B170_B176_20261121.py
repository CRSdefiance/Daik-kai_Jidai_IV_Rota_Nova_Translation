"""Stage reviewed dialogue and verify the source-authored patron headings."""

from types import FunctionType, SimpleNamespace

from scripts import preflight_rafael_B161_B169_FE_20261121 as modal
from scripts import review_rafael_B170_B176_20261121 as review
from scripts import stage_rafael_B161_B169_20261121 as previous
from scripts import verify_rafael_B161_B169_20261121 as verifier
from scripts.source_locked_derivation_v5118 import checked_text


base, native, parent = review.base, review.paired.native, review.paired.parent
OWNER = review.paired.ROOT
ROOT = OWNER / "staged_B170_B176_v3"
ROM, PROOF = ROOT / "Rafael_B170_B176_STAGED.nds", ROOT / "stored_proof.json"
MANUSCRIPT, SOURCE = review.OUTPUT, review.PACKET
FE_ROOT = OWNER / "speakerless_panel_preflight_v2"
FE_PROOF = FE_ROOT / "native_speakerless_preflight.json"
BLOCKS = (tuple(range(170, 177)), (), (), ())
TOKEN = review.TOKEN


def padding(line_bytes, old):
    return line_bytes + b" " * ((len(line_bytes) ^ len(old)) & 1)


def reflow_panel(row, old, painter):
    heading = row.get("english_heading")
    prefix = (heading,) if heading else ()
    body = row["english"][len(heading) + 1:] if heading else row["english"]
    for rows in modal.layout.wrap_options(body, 4 - len(prefix)):
        if not all(any(phrase in line for line in rows) for phrase in row["protected_phrases"]):
            continue
        shape = [(0, text) for text in (*prefix, *rows)]
        expected = modal.expected_rows(shape, "Rafael")
        for raw in modal.layout.candidates(row, row["source_record_index"], shape):
            try:
                actual, plane = modal.paint(painter, padding(raw, old))
            except AssertionError:
                continue
            if actual == expected:
                return raw, padding(raw, old), actual, plane
    raise AssertionError(f"No complete speakerless panel render for {row['id']}")


def qualified_panels():
    if FE_PROOF.exists():
        proof = base.load(FE_PROOF)
        assert proof["parent_sha256"] == base.digest(parent.ROM)
        assert all(base.digest(path) == h for path, h in proof["evidence"].items())
        assert all(base.digest(sheet["path"]) == sheet["sha256"] for sheet in proof["sheets"])
        if str(MANUSCRIPT) not in proof["evidence"]:
            earlier = OWNER / "contextual_decisions_B170_B176_v3.json"
            assert proof["evidence"][str(earlier)] == base.digest(earlier)
            old, current = [[r for r in base.load(path)["records"] if r["source_selector"] == 254]
                            for path in (earlier, MANUSCRIPT)]
            assert old == current
        return {r["id"]: r for r in proof["records"]}
    draft = base.load(MANUSCRIPT)
    parent_hash = base.digest(parent.ROM)
    assert parent_hash == draft["previous_sha256"]
    image = base.NdsImage.open(parent.ROM)
    ctx = verifier.current_runtime(image)
    painter = modal.prior.town.current_fe_painter(ctx)
    expand = modal.expansions(ctx)
    records, pictures = [], []
    for row in draft["records"]:
        if row["source_selector"] != 254:
            continue
        ja, old = [bytes.fromhex(row[k])[1:] for k in ("source_hex", "current_hex")]
        baseline, _ = modal.paint(painter, old)
        original = None
        if row["decision"] == "revision":
            if row.get("source_heading"):
                original, _ = modal.paint(painter, ja)
                assert original[0] == (0, 0, row["source_heading"]) and len(original) >= 2
                assert baseline[0][2].startswith(row["english_heading"] + " ")
            raw, stored, actual, plane = reflow_panel(row, old, painter)
        else:
            assert row["decision"] == "retention"
            raw = stored = old
            actual, plane = modal.paint(painter, stored)
        expanded, cases = expand(stored)
        assert expanded == stored and len(cases) == 4
        assert (stored != old) == (row["decision"] == "revision")
        ident = row["id"]
        records.append(dict(id=ident, source_reference=row["source_reference"], current_reference=row["current_reference"],
            source_rows=original, previous_rows=baseline, rows=actual, compiled_hex=(b"\xfe" + raw).hex(),
            expected_stored_hex=(b"\xfe" + stored).hex(), expanded_hex=expanded.hex(),
            plane_sha256=native.digest(plane), macro_alignment_cases=cases))
        pictures.append((ident + "  " + row["decision"], plane))
    assert len(records) == 6 and sum(r["source_rows"] is not None for r in records) == 3
    FE_ROOT.mkdir()
    make_sheets = FunctionType(modal.make_sheets.__code__, modal.make_sheets.__globals__ | {"OUT": FE_ROOT})
    proof = dict(parent_sha256=parent_hash, initialized_dependencies=ctx.receipt(), records=records,
        sheets=make_sheets(pictures), evidence={str(p): base.digest(p) for p in (MANUSCRIPT, SOURCE, parent.RELEASE)},
        offline_preflight=True)
    base.save(FE_PROOF, proof)
    return {r["id"]: r for r in records}


def rebuild_function(fe):
    rebuild = previous.compiler.rebuild_function()
    env = rebuild.__globals__ | {"plan_progressive": previous.plan_progressive}

    def plan_fe(row, _):
        proof = fe[row["id"]]
        assert (row["source_reference"], row["current_reference"]) == (proof["source_reference"], proof["current_reference"])
        raw = bytes.fromhex(proof["compiled_hex"])
        assert raw[0] == 254
        return raw[1:], dict(encoded_hex=raw.hex(), expected_native_pages=1,
            planned_visible_rows=proof["rows"], expected_stored_hex=proof["expected_stored_hex"])

    env["plan_fe"] = plan_fe
    env["changed_speech"] = FunctionType(env["changed_speech"].__code__, env)
    return FunctionType(rebuild.__code__, env)


def main():
    fe = qualified_panels()
    source = checked_text(previous.compiler.source, {
        "    painter = stage.system.native_painter(ctx)": "    painter = None",
        "    rebuild = rebuild_function()": "    rebuild = rebuild_function(fe)",
    })
    review_input = SimpleNamespace(OUTPUT=MANUSCRIPT, SOURCE=SOURCE)
    scope = previous.compiler.env | globals() | dict(review=review_input, paired=SimpleNamespace(BLOCKS=BLOCKS), fe=fe)
    exec(compile(source, __file__ + "::registered-story-writer", "exec"), scope)
    scope["main"]()


if __name__ == "__main__":
    main()
