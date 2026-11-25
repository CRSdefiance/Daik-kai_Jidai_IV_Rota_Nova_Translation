"""Verify every revised page and the four original speakerless panels."""

from inspect import getsource
from types import FunctionType, SimpleNamespace

from scripts import stage_rafael_spain_london_20261121 as stage
from scripts import verify_rafael_pereira_village_20261121 as precedent
from scripts.check_editorial_compiled_pages_v6 import check_FE_rows
from scripts.source_locked_derivation_v5118 import checked_text


base, native, display, town = stage.base, stage.native, precedent.display, precedent.town
ROOT = stage.ROOT / "native_display"
PROOF = ROOT / "native_display.json"
REFERENCE_STAGE = stage.ROOT.with_name("spanish_london_staged_v2")
REFERENCE_DISPLAY = REFERENCE_STAGE / "native_display" / PROOF.name


def previous_display(image, current):
    stored_file = REFERENCE_STAGE / stage.PROOF.name
    earlier, report = map(base.load, (stored_file, REFERENCE_DISPLAY))
    rom = REFERENCE_STAGE / stage.ROM.name
    assert earlier["candidate_sha256"] == report["candidate_sha256"] == base.digest(rom)
    assert report["stage_proof_sha256"] == base.digest(stored_file)
    assert earlier["predecessor_sha256"] == current["predecessor_sha256"]
    original = base.NdsImage.open(rom)
    assert all(original.read_file(part) == image.read_file(part) for part in display.ASSETS)
    assert all(base.digest(s["path"]) == s["sha256"] for s in report["sheets"])
    plans = {key: value for group in earlier["groups"] for key, value in group["plans"].items()}
    return report, {r["id"]: r for r in report["records"]}, plans


def name_audit():
    paragraph = display.display.paragraph
    source = checked_text(getsource(paragraph), {
        '    layouts = []': '''    if tokens == {"FI", "FA"}:
        stress += tuple(
            (f"offline FI {first} / FA {last}", {"FI": "ABCDEFGHIJKLMNOP"[:first], "FA": "ABCDEFGHIJKLMNOP"[:last]})
            for first, last in ((15, 16), (16, 15))
        )
    layouts = []''',
    })
    scope = paragraph.__globals__ | {"build": stage}
    exec(compile(source, __file__ + "::two-name-widths", "exec"), scope)
    return scope["paragraph"]


def sheet(previews, system=False):
    contact = display.display.inherited.early.contact_sheets
    context = contact.__globals__ | {"ROOT": ROOT}
    if not system:
        return FunctionType(contact.__code__, context)(previews)
    source = checked_text(getsource(contact), {
        "(888,": "(936,", "index % 2 * 444": "index % 2 * 468", "(216,64)": "(228,64)", "(432,128)": "(456,128)",
        "before_after_": "speakerless_panels_",
    })
    exec(compile(source, __file__ + "::FE-contact-sheet", "exec"), context)
    return context["contact_sheets"](previews)


def check_speakerless(fe, row, old, body, plan):
    assert bytes.fromhex(row["source_hex"])[0] == 254 and stage.review.logical(body.decode("ascii")) == row["english"]
    result = fe(body)
    assert result["complete_consumed_bytes"] == len(body)
    rows = check_FE_rows(body, result)
    if plan is not None:
        encoded = bytes.fromhex(plan["encoded_hex"])
        assert b"\xfe" + body in (encoded, encoded + b" ") and plan["expected_native_pages"] == 1
        assert rows["actual_rows"] == plan["lines"]
    else:
        assert old[6:old.index(0, 6)] == body
    plane = result["physical"]
    assert len(plane) == 228 * 64
    return plane, dict(system_FE=True, native_pages=1, expanded_hex=body.hex(),
                       panel_mask_sha256=native.digest(plane), native_rows=rows)


def main():
    assert not ROOT.exists()
    stored, draft, release = map(base.load, (stage.PROOF, stage.OUTPUT, stage.parent.RELEASE))
    candidate = base.digest(stage.ROM)
    assert stored["candidate_sha256"] == candidate and stored["whole_parent_inverse"]
    assert stored["predecessor_sha256"] == release["candidate_sha256"] == base.digest(stage.parent.ROM)
    assert stored["manuscript_sha256"] == base.digest(stage.OUTPUT)
    dependency = base.load(stage.parent.display.PROOF)["initialized_dependencies"]
    for key in ("release_proof", "startup_proof"):
        assert base.digest(dependency[key]) == dependency[key + "_sha256"]
    ctx = native.RegisteredRuntime(dependency["release_proof"], dependency["startup_proof"], captain=0)
    image = base.NdsImage.open(stage.ROM)
    assert all(ctx.image.read_file(path) == image.read_file(path) for path in display.ASSETS)
    reference, older, older_plans = previous_display(image, stored)
    paint, expand = display.clipped_renderer(ctx), display.original_expander()
    font = image.read_file("/GRP/KANJI.FNT")
    expanded, = {case["output_hex"] for case in ctx.execute(expand, b"FI FA FO", 0)["cases"]}
    names = dict(zip(("FI", "FA", "FO"), bytes.fromhex(expanded).decode("ascii").split(" ", 2), strict=True))
    assert names["FI"] == "Rafael" and names["FA"] == "Castor"
    audit = name_audit()
    fe = town.current_fe_painter(SimpleNamespace(arm=ctx.arm, image=image))
    path = "/data/SC0.DK4"
    bank = native.IlnkContainer.parse(image.read_file(path)).blocks
    rows = {r["id"]: r for r in draft["records"]}
    records, ordinary, system, reused, refreshed = [], [], [], [], []
    revised_pages = stress_pages = 0
    for group in stored["groups"]:
        block = group["block"]
        assert group["file_path"] == path and native.digest(bank[block]) == group["after"]
        for command in group["commands"]:
            at = command["stored_offset"]
            old, new, source = (bytes.fromhex(command[k]) for k in ("current", "stored", "source"))
            assert bank[block][at:at + len(new)] == new
            if not command["record_ids"]:
                continue
            ident, = command["record_ids"]
            row = rows.pop(ident)
            selector, ending = row["source_selector"], new.index(0, 6)
            assert new[:6] == old[:6] == source[:6] == b"\0\x40\xff\xff\0" + bytes([selector])
            assert len(new) % 2 == 0 and not any(new[ending:])
            body = new[6:ending]
            plan = group["plans"].get(ident)
            if row["decision"] == "retention":
                assert old == new and new[5:ending].hex() == row["current_hex"] and plan is None
            else:
                assert old != new and plan is not None
                if selector != 254:
                    assert plan == draft["plans"][ident]
            entry = dict(id=ident, block=block, file_path=path, decision=row["decision"],
                         stored_offset=at, stored_command_hex=new.hex())
            records.append(entry)
            if plan and older[ident]["stored_command_hex"] == new.hex() and older_plans.get(ident) == plan:
                prior = older[ident]
                assert prior["decision"] == row["decision"] == "revision"
                entry.update(prior | {"stored_offset": at})
                count = prior["native_pages"]
                revised_pages += count
                stress_pages += (len(prior.get("layouts", [None])) - 1) * count
                reused.append(ident)
                continue
            if plan:
                refreshed.append(ident)
            if selector == 254:
                plane, result = check_speakerless(fe, row, old, body, plan)
                entry.update(result)
                system.append((ident, plane))
                revised_pages += row["decision"] == "revision"
                continue
            if not plan:
                continue
            count = plan["expected_native_pages"]
            if stage.review.TOKEN.findall(row["english"]):
                validated = audit(ctx, font, paint, expand, None, names, row, new[5:ending], plan)
                layouts = validated["layouts"]
                entry["original_expansion"] = validated["macro_alignment_checks"]
            else:
                compiled = bytes.fromhex(plan["encoded_hex"])
                assert new[5:ending] in (compiled, compiled + b" ")
                assert stage.review.logical(body.decode("ascii")) == row["english"]
                pages = display.display.raster(ctx, font, paint, body, plan["lines"], count)
                layouts = [dict(scope="registered default", expanded_hex=body.hex(), pages=pages, lines=plan["lines"])]
            shapes = []
            for layout in layouts:
                pages = layout["pages"]
                assert len(pages) == count
                hashes = []
                for number, page in enumerate(pages, 1):
                    assert page["native_independent_plane_equal"] and page["all_bitmap_header_input_canaries_exact"]
                    pixels = bytes.fromhex(page["native_plane_hex"])
                    title = f"{ident} {layout['scope']}" + (f" {number}/{count}" if count > 1 else "")
                    ordinary.append((title, pixels))
                    hashes.append(native.digest(pixels))
                shapes.append(dict(scope=layout["scope"], expanded_hex=layout["expanded_hex"],
                                   page_sha256=hashes, lines=layout["lines"]))
            entry.update(native_pages=count, layouts=shapes)
            revised_pages += count
            stress_pages += (len(layouts) - 1) * count

    assert len(records) == 199 and not rows
    assert sum(bool(row.get("system_FE")) for row in records) == 4
    assert len(refreshed) + len(reused) == draft["decisions"]["revision"]
    ROOT.mkdir()
    sheets = reference["sheets"] + sheet(ordinary)
    if system:
        sheets += sheet(system, system=True)
    base.save(PROOF, dict(candidate_sha256=candidate, stage_proof_sha256=base.digest(stage.PROOF),
        records=records, revised_pages=revised_pages, name_stress_pages=stress_pages, speakerless_panels=4,
        sheets=sheets, initialized_dependencies=ctx.receipt(), default_names=names,
        runtime_assets=list(display.ASSETS), offline_native_only=True, refreshed_ids=refreshed,
        reused_exact_revision_ids=reused, reference_path=str(REFERENCE_DISPLAY), reference_sha256=base.digest(REFERENCE_DISPLAY)))
    print(f"Verified {revised_pages} revised pages and {stress_pages} alternate name-width pages, including all four FE panels.")


if __name__ == "__main__":
    main()
