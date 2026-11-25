"""Verify the stored script against the engine's progressive and FE consumers."""

from inspect import getsource
from pathlib import Path
from types import FunctionType, SimpleNamespace

from scripts import stage_rafael_B161_B169_20261121 as stage
from scripts import verify_rafael_palace_and_alliance_20261121 as prior
from scripts.source_locked_derivation_v5118 import checked_text


base, native, parent = stage.base, stage.native, stage.parent
display, PATH = prior.display, prior.PATH
ROOT = stage.ROOT / "native_display"
PROOF, NAMES = ROOT / "native_display.json", stage.ROOT / "speaker_labels.json"
DEFAULT_NAMES = {"FI": "Rafael", "FA": "Castor", "FO": "Castor Co.", "FU": "Rafael Castor"}


def audit_macro_widths():
    audit = display.display.paragraph
    source = checked_text(getsource(audit), {
        '{macro: example for macro in tokens}':
            '{macro: (FULL_NAMES[n] if macro == "FU" else example + (" Co." if macro == "FO" else "")) for macro in tokens}',
        'for n, example in ((1, "I"), (15, "ABCDEFGHIJKLMNO"), (16, "ABCDEFGHIJKLMNOP"))) if tokens else ()':
            'for n, example in ((1, "I"), (15, "ABCDEFGHIJKLMNO"), (16, "ABCDEFGHIJKLMNOP"), (32, "ABCDEFGHIJKLMNOP"))\n'
            '                   if n != 32 or "FU" in tokens) if tokens else ()',
    })
    env = audit.__globals__ | {"FULL_NAMES": {1: "A B", 15: "ABCDEFGHIJKLMNO ABCDEFGHIJKLMNO",
        16: "ABCDEFGHIJKLMNOP ABCDEFGHIJKLMNOP", 32: "ABCDEFGHIJKLMNOP ABCDEFGHIJKLMNO"}}
    exec(compile(source, __file__ + "::registered-name-widths", "exec"), env)
    return env["paragraph"]


def current_runtime(image):
    dependencies = base.load(parent.display.PROOF)["initialized_dependencies"]
    assert all(base.digest(dependencies[k]) == dependencies[k + "_sha256"] for k in ("release_proof", "startup_proof"))
    ctx = native.RegisteredRuntime(dependencies["release_proof"], dependencies["startup_proof"], captain=0)
    assert all(ctx.image.read_file(path) == image.read_file(path) for path in display.ASSETS)
    return ctx


def check_progressive(ctx, font, paint, expand, audit, row, body, plan):
    assert " ".join(body.decode("ascii").split()) == row["english"]
    compiled = bytes.fromhex(plan["encoded_hex"])
    prefix = bytes([row["source_selector"]])
    assert prefix + body in (compiled, compiled + b" ")
    if stage.TOKEN.search(row["english"]):
        result = audit(ctx, font, paint, expand, None, DEFAULT_NAMES, row, prefix + body, plan)
        return result["layouts"], result["macro_alignment_checks"]
    cases = ctx.execute(expand, body, prefix[0])["cases"]
    assert len(cases) == 4 and {case["output_hex"] for case in cases} == {body.hex()}
    count, lines = plan["expected_native_pages"], plan["lines"]
    pages = display.display.raster(ctx, font, paint, body, lines, count)
    if prefix + body != compiled:
        unpadded = display.display.raster(ctx, font, paint, compiled[1:], lines, count)
        assert [page["native_plane_hex"] for page in pages] == [page["native_plane_hex"] for page in unpadded]
    return [dict(scope="registered default", expanded_hex=body.hex(), lines=lines, pages=pages)], cases


def verify():
    assert not ROOT.exists()
    staged, draft = map(base.load, (stage.PROOF, stage.MANUSCRIPT))
    candidate = base.digest(stage.ROM)
    assert staged["candidate_sha256"] == candidate and staged["whole_parent_inverse"]
    assert staged["predecessor_sha256"] == base.digest(parent.ROM)
    assert staged["manuscript_sha256"] == base.digest(stage.MANUSCRIPT)
    image = base.NdsImage.open(stage.ROM)
    ctx = current_runtime(image)
    font = image.read_file("/GRP/KANJI.FNT")
    paint, expand = display.clipped_renderer(ctx), display.original_expander()
    default = ctx.execute(expand, b"FI FA FO FU", 0)["cases"]
    assert {bytes.fromhex(r["output_hex"]).decode("ascii") for r in default} == {" ".join(DEFAULT_NAMES.values())}
    audit = audit_macro_widths()
    qualified = stage.qualified_panels()
    rows = {r["id"]: r for r in draft["records"]}
    bank = native.IlnkContainer.parse(image.read_file(PATH)).blocks
    entries, pictures, pagination = [], [], []
    revised_pages, alternate_pages, fe_count = 0, 0, 0
    for group in staged["groups"]:
        n = group["block"]
        assert native.digest(bank[n]) == group["after"]
        for cmd in group["commands"]:
            at = cmd["stored_offset"]
            raw, old, source = [bytes.fromhex(cmd[k]) for k in ("stored", "current", "source")]
            assert bank[n][at:at + len(raw)] == raw
            if not cmd["record_ids"]:
                continue
            ident, = cmd["record_ids"]
            row = rows.pop(ident)
            selector = row["source_selector"]
            assert cmd["word"] == 0x4000 and raw[:6] == old[:6] == source[:6] == b"\x00\x40\xff\xff\x00" + bytes([selector])
            planned = group["plans"].get(ident)
            assert (raw != old) == bool(planned) == (row["decision"] == "revision")
            before = old[5:old.index(0, 6)]
            assert before.hex() == row["current_hex"] and source[5:source.index(0, 6)].hex() == row["source_hex"]
            body = raw[5:raw.index(0, 6)]
            assert not any(raw[5 + len(body):])
            entry = dict(id=ident, block=n, stored_pages=[cmd], body_offset=at + 5, body_hex=body.hex(), style_slots=[])
            entries.append(entry)
            if selector == 254:
                panel = qualified.pop(ident)
                assert body.hex() == panel["expected_stored_hex"]
                entry["system"] = [{"expanded_hex": panel["expanded_hex"], "plane_sha256": panel["plane_sha256"],
                                    "row_proof": panel["rows"], "proven_by_exact_preflight_binding": True}]
                revised_pages += bool(planned)
                fe_count += 1
            elif planned:
                try:
                    layouts, checks = check_progressive(ctx, font, paint, expand, audit, row, body[1:], planned)
                except (ValueError, AssertionError) as error:
                    raise AssertionError((ident, planned["lines"], body)) from error
                entry["layouts"] = []
                entry["original_expansion"] = checks
                count = planned["expected_native_pages"]
                if before.count(b"\n") >= 4:
                    old_default = stage.TOKEN.sub(lambda m: DEFAULT_NAMES[m[0]], before[1:].decode("ascii")).encode("ascii")
                    old_count = len(paint(ctx.arm, font, old_default)["pages"])
                    if old_count != count:
                        pagination.append(dict(id=ident, previous_pages=old_count, current_pages=count))
                for layout in layouts:
                    hashes = []
                    assert len(layout["pages"]) == count
                    for page_number, page in enumerate(layout["pages"], 1):
                        assert page["native_independent_plane_equal"] and page["all_bitmap_header_input_canaries_exact"]
                        plane = bytes.fromhex(page["native_plane_hex"])
                        pictures.append((f"{ident} {layout['scope']} {page_number}/{count}", plane))
                        hashes.append(native.digest(plane))
                    entry["layouts"].append(dict(scope=layout["scope"], expanded_hex=layout["expanded_hex"],
                                                 lines=layout["lines"], page_sha256=hashes))
                revised_pages += count
                alternate_pages += (len(layouts) - 1) * count
        print(f"B{n}: exact stored controls and changed pages verified", flush=True)
    assert not rows and not qualified and len(entries) == 368 and fe_count == 30
    ROOT.mkdir()
    sheet = prior.precedent.prior.sheet
    make_sheets = FunctionType(sheet.__code__, sheet.__globals__ | {"ROOT": ROOT})
    fresh = make_sheets(pictures, "rafael_B161_B169_progressive", 216)
    panels = base.load(stage.FE_PROOF)["sheets"]
    base.save(PROOF, dict(candidate_sha256=candidate, stage_proof_sha256=base.digest(stage.PROOF),
        records=entries, default_names=DEFAULT_NAMES, revised_speech_pages=revised_pages,
        alternate_name_width_pages=alternate_pages, pagination_changes=pagination, FE_panels=fe_count,
        menus=[], style_objects=[], sheets=fresh + panels, fresh_sheets=fresh,
        initialized_dependencies=ctx.receipt(), runtime_assets=list(display.ASSETS), offline_native_only=True))
    print(f"Verified {revised_pages} revised pages plus {alternate_pages} name-width pages.", flush=True)


def verify_names():
    selectors = {r["source_selector"] for r in base.load(stage.MANUSCRIPT)["records"] if r["kind"] == "progressive"}
    notes = {}
    for span in ("B161_B165", "B166_B167", "B168_B169"):
        old = base.load(Path(f"translations/rafael_{span}_scoped_names_final_v1.json"))
        notes.update({r["actor_ID"]: r["localization_note"] for r in old["records"]})
    notes[132] = "Officiant matches the registered generic ceremonial role. This speaker formally confers the item, and the exchange gives no specific rank."
    assert set(notes) == selectors
    names = prior.precedent.prior.labels
    source = checked_text(getsource(names.main), {
        'selectors = {r["source_selector"] for r in review["records"]}':
            'selectors = {r["source_selector"] for r in review["records"] if r["kind"] == "progressive"}',
    })
    scope = vars(names) | {"stage": SimpleNamespace(ROM=stage.ROM, PROOF=stage.PROOF, OUTPUT=stage.MANUSCRIPT),
        "display": SimpleNamespace(PROOF=PROOF, display=display), "NOTES": notes, "PROOF": NAMES}
    exec(compile(source, __file__ + "::contextual-native-nameplates", "exec"), scope)
    scope["main"]()


if __name__ == "__main__":
    verify()
    verify_names()
