"""Verify changes, retained commands, and all qualified name lengths for the poem."""

from types import FunctionType

from scripts import stage_manuel_poem_cross_route_20261119 as build
from scripts import verify_forest_expeditions_20261118 as native_display
from scripts import verify_london_guild_assignments_20261118 as names

base, native = build.base, build.native
ROOT = build.ROOT / "native_display"
PROOF = ROOT / "native_display.json"


def main():
    assert not ROOT.exists()
    stored, draft, release = map(base.load, (build.PROOF, build.review.OUTPUT, build.parent.RELEASE))
    assert stored["candidate_sha256"] == base.digest(build.ROM)
    assert stored["manuscript_sha256"] == base.digest(build.review.OUTPUT)
    assert stored["whole_parent_inverse"] and len(stored["groups"]) == 4
    ctx = native.RegisteredRuntime(build.parent.RELEASE, release["own_registered_startup"], captain=3)
    image = base.NdsImage.open(build.ROM)
    assets = (native.ARM, "/COMMON/MESFILE.DK4", "/GRP/KANJI.FNT")
    assert all(ctx.image.read_file(p) == image.read_file(p) for p in assets)
    font = image.read_file(assets[-1])
    _, paint = native_display.early.prior.precedent.planners(ctx.arm)
    expand, macros = names.expander(), names.current_names(ctx)
    banks = {path: native.IlnkContainer.parse(image.read_file(path)).blocks for path in stored["changed_blocks"]}
    rows = {(r["file_path"], r["id"]): r for r in draft["records"]}
    checked, retained, previews, equivalent = [], [], [], {}
    for group in stored["groups"]:
        path, number, route = (group[k] for k in ("file_path", "block", "route"))
        block = banks[path][number]
        assert native.digest(block) == group["after"]
        for cmd in group["commands"]:
            if not cmd["record_ids"]:
                continue
            ident, = cmd["record_ids"]
            row = rows[path, ident]
            at, raw = cmd["stored_offset"], bytes.fromhex(cmd["stored"])
            assert block[at:at + len(raw)] == raw and cmd["word"] == 0x4000
            value = raw[5:raw.index(0, 6)]
            assert value[0] == row["source_selector"]
            if row["decision"] == "retention":
                assert cmd["stored"] == cmd["current"] and value.hex() == row["current_hex"]
                retained.append(dict(id=ident, file_path=path, kept_complete_command=cmd))
                continue
            plan = group["plans"][ident]
            key = (value, plan["encoded_hex"], tuple(plan["lines"]))
            if key in equivalent:
                result = equivalent[key] | dict(id=ident, file_path=path, exact_layout_reuse=True)
            else:
                result = names.paragraph(ctx, font, paint, expand, None, macros, row, value, plan)
                equivalent[key] = result
            if (route, ident) == (2, "DK4_MES_B11_R0066"):
                assert build.review.TOKEN.findall(row["english"]) == ["FI"]
                body = value[1:].replace(b"FI", b"Lil")
                lines = [names.expected(line, {"FI": "Lil"}) for line in plan["lines"]]
                pages = names.raster(ctx, font, paint, body, lines, 1)
                result["layouts"].append(dict(scope="supplied Lil, to match replay", names={"FI": "Lil"},
                                              expanded_hex=body.hex(), lines=lines, pages=pages))
            main_layout = result["layouts"][-1 if (route, ident) == (2, "DK4_MES_B11_R0066") else 0]
            checked.append(result | dict(target_hex=value.hex(), pages=main_layout["pages"], planned_lines=plan["lines"]))
            for layout in result["layouts"]:
                for page in layout["pages"]:
                    label = f"SC{route} {ident} {layout['scope']}" if len(result["layouts"]) > 1 else f"SC{route} {ident}"
                    previews.append((label, bytes.fromhex(page["native_plane_hex"])))
    assert {(r["file_path"], r["id"]) for r in checked + retained} == rows.keys()
    assert len(checked) == 24 and len(retained) == 36 and len(previews) == 28
    ROOT.mkdir()
    sheets_fn = native_display.early.contact_sheets
    sheets = FunctionType(sheets_fn.__code__, vars(native_display.early) | {"ROOT": ROOT})(previews)
    base.save(PROOF, dict(candidate_sha256=stored["candidate_sha256"], stage_proof_sha256=base.digest(build.PROOF),
        revisions=checked, exact_retentions=retained, contact_sheets=sheets, distinct_layouts=len(equivalent),
        displayed_native_plans=len(previews), all_audited_offline=True, actual_gameplay=False))
    print("Checked all 24 changed records, four name-length render cases, and 36 exact retentions.")


if __name__ == "__main__":
    main()
