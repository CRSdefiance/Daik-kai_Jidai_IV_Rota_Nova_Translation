"""Verify all revised speech pages and the two source-bound lesson menus."""
from types import FunctionType

from scripts import stage_rafael_refit_sailing_lessons_20261121 as stage
from scripts import verify_parallel_ship_lessons_20261121 as earlier


base, native, display, menu = stage.base, stage.native, earlier.display, earlier.menu
ROOT = stage.ROOT / "native_display"
PROOF = ROOT / "native_display.json"


def captions(arm, record):
    block, source, current = (record[k] for k in ("block", "source", "stored"))
    assert current == record["current"]
    vms, paint, executed = menu.adapters(arm)
    results = []
    for raw in (source, current):
        first, second = [vms[2](arm, raw, align) for align in (0, 2)]
        assert first == second and [r["modal_selection"] for r in first["VM_cases"]] == [0, 1, -1]
        assert first["labels"] == [v.decode("cp932") for v in menu.labels(raw)]
        results.append(first)
    width = results[1]["minimum_width_units"] * 6
    pictures, styles = [], []
    for i, label in enumerate(menu.labels(current)):
        for style in (1, 15):
            pixels, audit = paint(arm, label, style, width, (0, i * 12))
            assert audit["independent_complete_native_pixels_match"] and audit["storage_padding_all_blank"]
            assert audit["visible_cell_center_twice"] == width and audit["extra_flush_stays_within_physical_backing"]
            styles.append(audit)
            if style == 1:
                pictures.append((label.decode("ascii"), width, pixels))
    path = ROOT / f"lesson_B{block}_choices.png"
    menu.sheet(pictures, path)
    return dict(block=block, source_and_current=results, styles=styles, executed_addresses=len(executed),
                caption_ids=record["record_ids"], sheet=dict(path=str(path), sha256=base.digest(path)))


def main():
    assert not ROOT.exists()
    stored, draft, release = map(base.load, (stage.PROOF, stage.review.OUTPUT, stage.parent.RELEASE))
    assert stored["candidate_sha256"] == base.digest(stage.ROM) and stored["whole_parent_inverse"]
    assert stored["manuscript_sha256"] == base.digest(stage.review.OUTPUT)
    assert stored["predecessor_sha256"] == release["candidate_sha256"]
    earlier_proof = base.load(stage.parent.display.PROOF)
    prior = earlier_proof["initialized_dependencies"]["0"]
    assert prior["candidate_sha256"] == release["candidate_sha256"]
    for label in ("release_proof", "startup_proof"):
        assert base.digest(prior[label]) == prior[label + "_sha256"]
    ctx = native.RegisteredRuntime(prior["release_proof"], prior["startup_proof"], captain=0)
    image = base.NdsImage.open(stage.ROM)
    assert all(ctx.image.read_file(asset) == image.read_file(asset) for asset in display.ASSETS)
    expand = display.original_expander()
    assert {x["output_hex"] for x in ctx.execute(expand, b"FI", 0)["cases"]} == {b"Rafael".hex()}
    font = image.read_file("/GRP/KANJI.FNT")
    paint = display.clipped_renderer(ctx)
    paragraph = display.display.paragraph
    audit = FunctionType(paragraph.__code__, paragraph.__globals__ | {"build": stage})
    rows = {row["id"]: row for row in draft["records"]}
    archive = native.IlnkContainer.parse(image.read_file("/data/SC0.DK4")).blocks
    ROOT.mkdir()
    records, pictures, menus = [], [], []
    for group in stored["groups"]:
        number, path = group["block"], group["file_path"]
        assert path == "/data/SC0.DK4" and native.digest(archive[number]) == group["after"]
        for command in group["commands"]:
            old, body = (bytes.fromhex(command[k]) for k in ("current", "stored"))
            at = command["stored_offset"]
            assert archive[number][at:at+len(body)] == body
            if command["word"] == 0x2100:
                menus.append(captions(ctx.arm, command | dict(block=number,
                    source=bytes.fromhex(command["source"]), current=old, stored=body)))
            for ident in command["record_ids"]:
                row = rows.pop(ident)
                proof = dict(id=ident, route=0, file_path=path, block=number, decision=row["decision"],
                             stored_offset=at, stored_command_hex=body.hex())
                if row["decision"] == "retention":
                    assert body == old
                    if command["word"] == 0x2100:
                        assert row["english"].encode("ascii") in menu.labels(body)
                        proof.update(native_caption=True, native_pages=0)
                else:
                    assert old[:6] == body[:6] == b"\0\x40\xff\xff\0" + bytes([row["source_selector"]])
                    end = body.index(0, 6)
                    assert not any(body[end:])
                    plan = group["plans"][ident]
                    assert plan["expected_native_pages"] == 1
                    result = audit(ctx, font, paint, expand, None, {"FI": "Rafael"}, row, body[5:end], plan)
                    layouts = []
                    for layout in result["layouts"]:
                        page, = layout["pages"]
                        assert page["native_independent_plane_equal"]
                        pixels = bytes.fromhex(page["native_plane_hex"])
                        pictures.append((f"{ident} {layout['scope']}", pixels))
                        layouts.append(dict(scope=layout["scope"], expanded_hex=layout["expanded_hex"],
                                            pages=[native.digest(pixels)], lines=layout["lines"]))
                    proof.update(native_pages=1, layouts=layouts, original_expansion=result["macro_alignment_checks"])
                records.append(proof)
    assert not rows and len(records) == 62 and [m["block"] for m in menus] == [179, 180]
    contact = display.display.inherited.early.contact_sheets
    sheets = FunctionType(contact.__code__, contact.__globals__ | {"ROOT": ROOT})(pictures)
    speech = sum(r["decision"] == "revision" for r in records)
    assert speech == 34 and len(pictures) == 37
    base.save(PROOF, dict(candidate_sha256=stored["candidate_sha256"], stage_proof_sha256=base.digest(stage.PROOF),
        records=records, newly_rendered_pages=speech, name_stress_pages=len(pictures)-speech,
        offline_native_only=True, native_caption_count=4, native_menu_count=2, menus=menus,
        reused_initialized_dependency=prior, sheets=[*sheets, *(m["sheet"] for m in menus)]))
    print(f"Verified {speech} revised native pages, given-name stress cases, and four retained captions.")


if __name__ == "__main__":
    main()
