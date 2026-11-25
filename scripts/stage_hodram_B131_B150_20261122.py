"""Compile Hodram's crew lessons, introductions and discovery scenes."""

from collections import Counter
from types import SimpleNamespace

from scripts import pair_hodram_B131_B150_20261122 as paired
from scripts import register_hodram_B111_B130_20261122 as parent
from scripts import stage_hodram_B111_B130_20261122 as previous
from scripts.source_locked_derivation_v5118 import checked_text


base, native, compiler, TOKEN = previous.base, previous.native, previous.compiler, previous.TOKEN
SOURCE, ROOT = paired.PACKET, paired.ROOT / "B131_B150_staged_v2"
ROM, PROOF = ROOT / "Hodram_B131_B150_STAGED.nds", ROOT / "stored_proof.json"
OUTPUT = paired.ROOT / "B131_B150_scoped_manuscript_v3.json"
ARCHIVE, logical_end, modal = previous.ARCHIVE, previous.logical_end, previous.modal
BLOCKS = ((), tuple(paired.BLOCKS), (), ())
DRAFTS = [paired.ROOT / f"B{span}_contextual_v1.json" for span in (
    "131_B132", "133_B136", "137_B140", "141_B142", "143_B150")]
HEAD = "Girl from Abroad:"
DEFAULT_NAMES = {**parent.display.scope["DEFAULT_NAMES"]}
REFINEMENTS = {
    "131_R0054": (None, ["every tavern,", "your duty as an adventurer?"]),
    "131_R0061": ("...I'll let you call it that.", ["call it that."]),
    "135_R0028": (None, ["the crew to resupply", "they'll do the rest."]),
    "136_R0044": (None, ["the goods aboard."]),
    "137_R0010": (None, ["apologize for earlier."]),
    "137_R0014": (None, ["that brat!", "What are you doing here?!"]),
    "140_R0080": (None, ["read it that way."]),
    "142_R0159": ("You'd leave her here? The tavern's full of predators. A pretty young woman with no one to turn to... Will she be safe alone?",
                  ["You'd leave her here?", "with no one to turn to...", "Will she be safe alone?"]),
    "142_R0327": (None, ["you want to see", "in the New World?"]),
    "147_R0008": (None, ["first I've heard of it."]),
    "148_R0076": (None, ["the liquid..."]),
    "148_R0081": (None, ["the liquid..."]),
    "140_R0090": ("Let Europe keep its religious wars. I won't drag that senseless conflict to the New World. England is different!",
                  ["religious wars.", "the New World.", "England is different!"]),
}
FE_WRAPS = {
    "134_R0028": (["Relying on boarding battles?", "larger crew", "cruising range."],
                  "Keep the boarding question and range warning readable as complete phrases."),
    "135_R0039": (["decline resupply first.", "adjust the amounts."],
                  "Keep the first instruction together before the next step."),
    "136_R0031": (["use the D-pad", "then press A."],
                  "Keep the control and the confirmation step together."),
}


FE_WORDING = {
    "135_R0035": ("The crew normally buys as much as the fleet can carry. If you're short on funds, they'll buy only what you can afford.",
                  ["the fleet can carry.", "short on funds,", "what you can afford."],
                  "Separate the default resupply rule from what happens when funds are short."),
    "136_R0038": ("Choose what to buy and sell on each ship. Then press X to complete the trade.",
                  ["buy and sell", "on each ship.", "press X to complete the trade."],
                  "Keep X and its effect together after the all-ships setup."),
}


def plan_heading(row, raw, painter):
    assert row["block"] == 142 and (row["source_selector"], row["decision"]) == (254, "revision")
    prefix, text = row["english"].split(": ", 1)
    assert prefix + ":" == HEAD
    source = raw.decode("ascii")
    assert " ".join(source.split()).startswith("Foreign Girl: ")
    assert all(macro == "FI" for macro in TOKEN.findall(text))
    shape = [(0, HEAD), (0, text.replace("FI", "{MACRO:FI}"))]
    widths = ("Hodram", "I", "ABCDEFGHIJKLMNO", "ABCDEFGHIJKLMNOP")
    for body in modal.layout.candidates(row, -1, shape):
        encoded = body + b" " * ((len(body) ^ len(raw)) & 1)
        cases = []
        for name in widths if "FI" in text else widths[:1]:
            expanded = encoded.replace(b"FI", name.encode("ascii"))
            try:
                rows, raster = modal.paint(painter, expanded)
            except (ValueError, AssertionError):
                break
            expected = [(0,0,HEAD), (12,0,text.replace("FI", name))]
            if rows != expected:
                break
            cases.append(dict(name=name, rows=rows, expanded_hex=expanded.hex(), plane_sha256=native.digest(raster)))
        else:
            assert TOKEN.findall(body.decode("ascii")) == TOKEN.findall(source)
            return dict(compiled_hex=body.hex(), expected_hex=(b"\xfe"+encoded).hex(),
                        rows=cases[0]["rows"], plane_sha256=cases[0]["plane_sha256"], width_cases=cases)
    raise AssertionError((row["id"], "no exact role heading layout"))


def plan_spirit(row, raw, painter):
    assert row["english"] == "FI's Spirit increased by 1!" and row["source_selector"] == 254
    former = raw.replace(b"FI",b"ABCDEFGHIJKLMNO")
    old_rows, _ = modal.paint(painter,former)
    assert len(old_rows) == 2 and old_rows[1][2] == "y 1!"
    body = b"FI's Spirit rose by 1!"
    stored = body + b" " * ((len(body)^len(raw)) & 1)
    cases = []
    for name in ("Hodram","I","ABCDEFGHIJKLMNO","ABCDEFGHIJKLMNOP"):
        expanded = stored.replace(b"FI",name.encode("ascii"))
        rows, raster = modal.paint(painter,expanded)
        assert rows == [(0,0,f"{name}'s Spirit rose by 1!")]
        cases.append(dict(name=name,rows=rows,plane_sha256=native.digest(raster),expanded_hex=expanded.hex()))
    row.update(english=body.decode("ascii"),decision="revision",change_class="wording",
        localization_note="Match the existing Spirit notice. The old line split the gain across rows with a 15- or 16-cell captain name. The full gain now fits on one row.")
    return dict(compiled_hex=body.hex(),expected_hex=(b"\xfe"+stored).hex(),
                rows=cases[0]["rows"],plane_sha256=cases[0]["plane_sha256"],width_cases=cases)


def collect():
    packet, carry, release = map(base.load, (SOURCE, paired.CARRY, parent.RELEASE))
    assert base.digest(parent.ROM) == packet["candidate_sha256"] == release["candidate_sha256"] == carry["candidate_sha256"]
    assert release["registry_sha256"] == base.digest(base.REGISTRY)
    assert not carry["reused_records"] and carry["source_packet_sha256"] == base.digest(SOURCE)
    drafts = list(map(base.load, DRAFTS))
    assert all(d["source_packet_sha256"] == base.digest(SOURCE) for d in drafts)
    by_id = {r["id"]: r for d in drafts for r in d["records"]}
    assert len(by_id) == sum(len(d["records"]) for d in drafts) == 350
    image = base.NdsImage.open(parent.ROM)
    painter = modal.prior.town.current_fe_painter(SimpleNamespace(image=image,arm=image.read_file(native.ARM)))
    rows, fe = [], {}
    for group in packet["groups"]:
        for original in group["records"]:
            row = by_id.pop(original["id"])
            assert all(row[k] == v for k,v in original.items())
            ident = row["id"]
            short = ident.partition("_B")[2]
            if short in REFINEMENTS:
                wording, row["protected_phrases"] = REFINEMENTS[short]
                row["english"] = wording or row["english"]
                assert row["change_class"] == "wording"
            if row["source_selector"] == 254:
                raw = bytes.fromhex(row["current_hex"])[1:]
                if short == "132_R0145":
                    fe[ident] = plan_spirit(row,raw,painter)
                elif row["english"].startswith(HEAD):
                    assert row["kind"] == "system-FE"
                    fe[ident] = plan_heading(row, raw, painter)
                elif short in FE_WRAPS or short in FE_WORDING:
                    wording, phrases, note = FE_WORDING[short] if short in FE_WORDING else (None,*FE_WRAPS[short])
                    assert row["decision"] == "retention"
                    ask = row | {"source_record_index": -1, "protected_phrases": phrases,
                                 "english": wording or row["english"]}
                    body, expected, cells, raster = modal.plan(ask, raw, painter)
                    old_rows, _ = modal.paint(painter,raw)
                    if cells != old_rows:
                        assert expected != raw
                        row.update(decision="revision",change_class="wording" if wording else "wrap-only",
                                   english=ask["english"],protected_phrases=phrases,
                                   prior_retention_note=row["localization_note"],localization_note=note)
                        fe[ident] = dict(compiled_hex=body.hex(),expected_hex=(b"\xfe"+expected).hex(),
                                         rows=cells,plane_sha256=native.digest(raster),width_cases=[])
            if ident == "DK4_MES_B143_R0033":
                assert row["decision"] == "retention" and row["current_English"].count("\n") == 2
                row["formatting_retention_reason"] = ("The clean Japanese separates three silent beats while the captain waits. "
                                                      "The existing three rows reproduce that timing.")
            rows.append(row | {"route":1})
    assert not by_id and sum(r["english"].startswith(HEAD) for r in rows) == 12
    findings = dict(Counter(r["change_class"] for r in rows))
    assert findings["wording"] == 110 and findings["glyph"] == 3 and findings.get("wrap-only",0) == len(fe)-15
    doc = dict(translation_policy="natural-dialogue-v2",encoder="dialogue-relocatable-v1",target_locale="en-US",
               review_gates=drafts[0]["review_gates"],previous_sha256=release["candidate_sha256"],
               previous_registry_sha256=release["registry_sha256"],source_packet=str(SOURCE),
               source_packet_sha256=base.digest(SOURCE),records=rows,findings=findings,planned_FE=fe,
               source_and_draft_evidence={str(p):base.digest(p) for p in DRAFTS},contextual_records_revisited=350,
               contextual_decisions_reused=0,new_editorial_credit=0,status="Prose reviewed. Native and gameplay checks pending.")
    if OUTPUT.exists():
        assert base.load(OUTPUT) == doc
    else:
        base.save(OUTPUT,doc)
    return doc


program = checked_text(previous.compiler.source, {
    '    painter = stage.system.native_painter(ctx)': '    painter = None',
    '    rebuild = rebuild_function()': '    rebuild = assemble(draft["planned_FE"])',
    'for g in packet["groups"]}': 'for g in packet["groups"] if g["block"] in paired.BLOCKS[1]}',
})
assemble = previous.assemble


def main():
    assert not PROOF.exists()
    draft = collect()
    print(draft["findings"], flush=True)
    scope = compiler.env | globals() | dict(review=SimpleNamespace(OUTPUT=OUTPUT,SOURCE=SOURCE),
                                           paired=SimpleNamespace(BLOCKS=BLOCKS),draft=draft)
    exec(compile(program,__file__+"::stored-script-and-inverse","exec"),scope)
    scope["main"]()
    stored = base.load(PROOF)
    assert stored["whole_parent_inverse"] and len(stored["groups"]) == len(BLOCKS[1])
    assert stored["changed_blocks"] == {ARCHIVE:sorted({r["block"] for r in draft["records"] if r["decision"]=="revision"})}


if __name__ == "__main__":
    main()

