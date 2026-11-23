"""Stage the reviewed story blocks and qualify Aziza's speakerless panels."""

from types import FunctionType, SimpleNamespace

from scripts import preflight_rafael_B161_B169_FE_20261121 as modal
from scripts import review_rafael_B181_B187_20261121 as review
from scripts import stage_rafael_B161_B169_20261121 as previous
from scripts import verify_rafael_B161_B169_20261121 as verifier
from scripts.source_locked_derivation_v5118 import checked_text


base, native, parent = review.base, review.paired.pairing.native, review.paired.parent
ROOT = review.paired.ROOT / "staged_B181_B187_v2"
ROM, PROOF = ROOT / "Rafael_B181_B187_STAGED.nds", ROOT / "stored_proof.json"
MANUSCRIPT, SOURCE = review.OUTPUT, review.paired.PAIRED
FE_ROOT = review.paired.ROOT / "Aziza_speakerless_preflight_v2"
FE_PROOF = FE_ROOT / "native_speakerless_preflight.json"
BLOCKS = (review.BLOCKS, (), (), ())
TOKEN = review.TOKEN
DEFAULT_COMPANY = "Castor Co."
WIDE_COMPANY = "W" * previous.width.company_scope["MAX_COMPANY_CELLS"]


def expand_default(ctx):
    historic = modal.layout.native
    adapter = checked_text(base.load(historic.MACROS)["source_owned_FE_adapter"], {
        "b'Hodram'": "b'Rafael'", "b'Bergstrom'": "b'Castor'",
        "b'Bergstrom Fleet'": "b'Castor Co.'",
    })
    env = dict(historic.FE_expand.__globals__)
    exec(compile(adapter, __file__ + "::native-FE-macros", "exec"), env)
    return lambda body: ctx.execute(env["expand"], body)["cases"]


def plan_panel(row, old, painter):
    record_index = int(row["id"][-4:])
    for strings in modal.layout.wrap_options(row["english"].replace("FO", WIDE_COMPANY), 4):
        normalized = [text.replace(WIDE_COMPANY, "FO") for text in strings]
        assert " ".join(normalized) == row["english"]
        if not all(any(phrase.casefold() in line.casefold() for line in normalized) for phrase in row["protected_phrases"]):
            continue
        shape = [(0, text) for text in normalized]
        for raw in modal.layout.candidates(row, record_index, shape):
            stored = raw + b" " * ((len(raw) ^ len(old)) & 1)
            try:
                measured, plane = modal.paint(painter, stored.replace(b"FO", DEFAULT_COMPANY.encode("ascii")))
                expected = [(12 * i, 0, line.replace("FO", DEFAULT_COMPANY)) for i, line in enumerate(normalized)]
                if measured != expected:
                    continue
                if b"FO" in stored:
                    stress, _ = modal.paint(painter, stored.replace(b"FO", WIDE_COMPANY.encode("ascii")))
                    assert stress == [(12 * i, 0, text) for i, text in enumerate(strings)]
            except AssertionError:
                continue
            return raw, stored, measured, plane
    raise AssertionError(f"No complete FE wrap for {row['id']}")


def qualified_panels():
    parent_hash = base.digest(parent.ROM)
    if FE_PROOF.exists():
        doc = base.load(FE_PROOF)
        assert doc["parent_sha256"] == parent_hash
        assert all(base.digest(path) == digest for path, digest in doc["evidence"].items())
        assert all(base.digest(s["path"]) == s["sha256"] for s in doc["sheets"])
        return {r["id"]: r for r in doc["records"]}
    draft = base.load(MANUSCRIPT)
    assert parent_hash == draft["previous_sha256"]
    image = base.NdsImage.open(parent.ROM)
    ctx = verifier.current_runtime(image)
    painter = modal.prior.town.current_fe_painter(ctx)
    expand = expand_default(ctx)
    records, pictures = [], []
    company = DEFAULT_COMPANY.encode("ascii")
    for row in draft["records"]:
        if row["source_selector"] != 254:
            continue
        ident = row["id"]
        old = bytes.fromhex(row["current_hex"])[1:]
        baseline, _ = modal.paint(painter, old.replace(b"FO", company))
        if row["decision"] == "revision":
            raw, stored, measured, plane = plan_panel(row, old, painter)
        else:
            assert row["decision"] == "retention"
            raw = stored = old
            measured, plane = modal.paint(painter, stored.replace(b"FO", company))
        expected = row["english"].replace("FO", DEFAULT_COMPANY)
        assert " ".join(line for _, _, line in measured) == expected
        assert (stored != old) == (row["decision"] == "revision")
        assert TOKEN.findall(stored.decode("ascii")) == TOKEN.findall(old.decode("ascii"))
        expanded = stored.replace(b"FO", company)
        if b"FO" in stored:
            assert company + b"." not in expanded
        cases = expand(stored)
        assert len(cases) == 4 and {c["output_hex"] for c in cases} == {expanded.hex()}
        records.append(dict(id=ident, source_reference=row["source_reference"], current_reference=row["current_reference"],
            previous_rows=baseline, rows=measured, compiled_hex=(b"\xfe" + raw).hex(),
            expected_stored_hex=(b"\xfe" + stored).hex(), expanded_hex=expanded.hex(),
            plane_sha256=native.digest(plane), macro_alignment_cases=cases, full_company_width_tested=b"FO" in stored))
        pictures.append((ident + " " + row["decision"], plane))
    assert len(records) == 13 and sum(r["full_company_width_tested"] for r in records) == 1
    FE_ROOT.mkdir(exist_ok=True)
    make_sheets = FunctionType(modal.make_sheets.__code__, modal.make_sheets.__globals__ | {"OUT": FE_ROOT})
    base.save(FE_PROOF, dict(parent_sha256=parent_hash, initialized_dependencies=ctx.receipt(), records=records,
        sheets=make_sheets(pictures), evidence={str(path): base.digest(path) for path in (MANUSCRIPT, SOURCE, parent.RELEASE)},
        offline_preflight=True))
    return {r["id"]: r for r in records}


def rebuild_function(fe):
    rebuild = previous.compiler.rebuild_function()
    env = rebuild.__globals__ | {"plan_progressive": previous.plan_progressive}

    def plan_fe(row, _):
        proof = fe[row["id"]]
        assert (row["source_reference"], row["current_reference"]) == (proof["source_reference"], proof["current_reference"])
        encoded = bytes.fromhex(proof["compiled_hex"])
        assert encoded[0] == 254
        return encoded[1:], dict(encoded_hex=encoded.hex(), expected_native_pages=1,
            planned_visible_rows=proof["rows"], expected_stored_hex=proof["expected_stored_hex"])

    env["plan_fe"] = plan_fe
    env["changed_speech"] = FunctionType(env["changed_speech"].__code__, env)
    return FunctionType(rebuild.__code__, env)


def main():
    fe = qualified_panels()
    source = checked_text(previous.compiler.source, {
        "    painter = stage.system.native_painter(ctx)": "    painter = None",
        "    rebuild = rebuild_function()": "    rebuild = rebuild_function(fe)",
        'g for g in packet["groups"]}': 'g for g in packet["groups"] if g["block"] in BLOCKS[0]}',
    })
    scope = previous.compiler.env | globals() | dict(
        review=SimpleNamespace(OUTPUT=MANUSCRIPT, SOURCE=SOURCE), paired=SimpleNamespace(BLOCKS=BLOCKS), fe=fe,
    )
    exec(compile(source, __file__ + "::registered-story-objects", "exec"), scope)
    scope["main"]()


if __name__ == "__main__":
    main()
