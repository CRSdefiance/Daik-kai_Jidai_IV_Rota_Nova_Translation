"""Check the complete stored text and native pages for the four Hamburg scenes."""

from types import FunctionType

from scripts import stage_hamburg_ceramics_cross_route_20261120 as build
from scripts import verify_forest_expeditions_20261118 as display


base, native = build.base, build.native
ROOT = build.ROOT / "native_display"
PROOF = ROOT / "native_display.json"


def main():
    assert not ROOT.exists()
    staged, review, release = map(base.load, (build.PROOF, build.review.OUTPUT, build.parent.RELEASE))
    assert base.digest(build.ROM) == staged["candidate_sha256"] and staged["whole_parent_inverse"]
    assert base.digest(build.review.OUTPUT) == staged["manuscript_sha256"]
    assert staged["predecessor_sha256"] == release["candidate_sha256"] == base.digest(build.parent.ROM)
    ctx = native.RegisteredRuntime(build.parent.RELEASE, release["own_registered_startup"], captain=3)
    image = base.NdsImage.open(build.ROM)
    for path in (native.ARM, "/COMMON/MESFILE.DK4", "/GRP/KANJI.FNT"):
        assert ctx.image.read_file(path) == image.read_file(path)
    font = image.read_file("/GRP/KANJI.FNT")
    _, paint = display.early.prior.precedent.planners(ctx.arm)
    expand = display.progress_expander()
    fe_paint = build.current_fe_painter(ctx)
    lookup = {(r["file_path"], r["id"]): r for r in review["records"]}
    receipts, previews, cached = [], [], {}
    for group in staged["groups"]:
        path, number, route = (group[k] for k in ("file_path", "block", "route"))
        block = native.IlnkContainer.parse(image.read_file(path)).blocks[number]
        assert native.digest(block) == group["after"]
        for cmd in group["commands"]:
            if not cmd["record_ids"]:
                continue
            ident, = cmd["record_ids"]
            row = lookup[path, ident]
            offset, raw = cmd["stored_offset"], bytes.fromhex(cmd["stored"])
            assert block[offset:offset + len(raw)] == raw and cmd["word"] == 0x4000
            value = raw[5:raw.index(0, 6)]
            assert value[0] == row["source_selector"]
            if row["decision"] == "retention":
                assert cmd["stored"] == cmd["current"] and value.hex() == row["current_hex"]
                receipts.append(dict(id=ident, file_path=path, kept_complete_command=cmd))
                continue
            plan = group["plans"][ident]
            key = (value, plan["encoded_hex"], tuple(plan["lines"]))
            if key not in cached:
                cached[key] = display.validate_paragraph(ctx, font, paint, expand, fe_paint, row, value, plan)
            result = cached[key] | dict(id=ident, file_path=path, target_command_offset=offset)
            receipts.append(result)
            for page in result["pages"]:
                previews.append((f"SC{route} / R{row['source_reference']['record_index']:04d}", bytes.fromhex(page["native_plane_hex"])))
    assert len(receipts) == len(lookup) == 68
    assert {(r["file_path"], r["id"]) for r in receipts} == lookup.keys()
    assert len(previews) == len([r for r in receipts if "pages" in r]) == len(lookup) - review["counts"]["retention"]
    ROOT.mkdir()
    sheet_builder = display.early.contact_sheets
    sheets = FunctionType(sheet_builder.__code__, vars(display.early) | {"ROOT": ROOT})(previews)
    base.save(PROOF, dict(candidate_sha256=staged["candidate_sha256"], stage_proof_sha256=base.digest(build.PROOF),
        receipts=receipts, contact_sheets=sheets, distinct_checked_byte_layouts=len(cached),
        displayed_native_plans=len(previews), exact_retentions=len(receipts) - len(previews),
        offline_only=True, hardware=False))
    print(f"Checked {len(previews)} complete native pages and {len(receipts) - len(previews)} exact retentions.")


if __name__ == "__main__":
    main()
