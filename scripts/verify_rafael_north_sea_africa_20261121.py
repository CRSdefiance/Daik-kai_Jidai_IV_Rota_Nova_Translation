"""Check each revised page using the native progressive dialogue renderer."""

from types import FunctionType

from scripts import stage_rafael_north_sea_africa_20261121 as stage
from scripts import verify_all_routes_next_phrase_wraps_20261118 as display
from scripts import verify_refit_sailing_parallel_routes_20261121 as prior


base, native = stage.base, stage.native
ROOT = stage.ROOT / "native_display"
PROOF = ROOT / "native_display.json"


def main():
    assert not ROOT.exists()
    stored, draft, release = map(base.load, (stage.PROOF, stage.review.OUTPUT, stage.parent.RELEASE))
    candidate = base.digest(stage.ROM)
    assert stored["candidate_sha256"] == candidate and stored["whole_parent_inverse"]
    assert stored["predecessor_sha256"] == release["candidate_sha256"] == base.digest(stage.parent.ROM)
    assert stored["manuscript_sha256"] == base.digest(stage.review.OUTPUT)
    dependency = base.load(prior.PROOF)["initialized_dependencies"]["0"]
    for key in ("release_proof", "startup_proof"):
        assert base.digest(dependency[key]) == dependency[key + "_sha256"]
    ctx = native.RegisteredRuntime(dependency["release_proof"], dependency["startup_proof"], captain=0)
    current, staged = map(base.NdsImage.open, (stage.parent.ROM, stage.ROM))
    assert all(ctx.image.read_file(path) == current.read_file(path) == staged.read_file(path)
               for path in display.ASSETS)
    first_root = stage.ROOT.with_name("staged_v1")
    first_path = first_root / "native_display/native_display.json"
    first, first_stage = map(base.load, (first_path, first_root / stage.PROOF.name))
    first_rom = first_root / stage.ROM.name
    assert first["candidate_sha256"] == first_stage["candidate_sha256"] == base.digest(first_rom)
    assert first["stage_proof_sha256"] == base.digest(first_root / stage.PROOF.name)
    assert first["initialized_dependencies"] == ctx.receipt()
    first_image = base.NdsImage.open(first_rom)
    assert all(first_image.read_file(path) == staged.read_file(path) for path in display.ASSETS)
    assert all(base.digest(sheet["path"]) == sheet["sha256"] for sheet in first["sheets"])
    first_rows = {r["id"]: r for r in first["records"]}
    first_plans = {k: v for g in first_stage["groups"] for k, v in g["plans"].items()}
    archive_path = "/data/SC0.DK4"
    before, after = [native.IlnkContainer.parse(rom.read_file(archive_path)).blocks for rom in (current, staged)]
    font = staged.read_file("/GRP/KANJI.FNT")
    paint, expand = display.clipped_renderer(ctx), display.original_expander()
    expanded, = {case["output_hex"] for case in ctx.execute(expand, b"FI FA FO", 0)["cases"]}
    names = dict(zip(("FI", "FA", "FO"), bytes.fromhex(expanded).decode("ascii").split(" ", 2), strict=True))
    assert names["FI"] == "Rafael" and names["FA"] == "Castor"
    assert names == first["default_names"]
    paragraph = display.display.paragraph
    audit = FunctionType(paragraph.__code__, paragraph.__globals__ | {"build": stage})
    rows = {row["id"]: row for row in draft["records"]}
    records, previews, refreshed = [], [], []
    for group in stored["groups"]:
        block = group["block"]
        assert group["file_path"] == archive_path
        assert native.digest(before[block]) == group["before"] and native.digest(after[block]) == group["after"]
        for command in group["commands"]:
            if not command["record_ids"]:
                continue
            ident, = command["record_ids"]
            row = rows.pop(ident)
            old, new, clean = (bytes.fromhex(command[key]) for key in ("current", "stored", "source"))
            at = command["stored_offset"]
            assert after[block][at:at + len(new)] == new
            end = new.index(0, 6)
            assert new[:6] == old[:6] == clean[:6] == b"\0\x40\xff\xff\0" + bytes([row["source_selector"]])
            assert not any(new[end:]) and len(new) % 2 == 0
            entry = dict(id=ident, block=block, file_path=archive_path, decision=row["decision"],
                         stored_offset=at, stored_command_hex=new.hex())
            if row["decision"] == "retention":
                assert new == old and new[5:end].hex() == row["current_hex"]
            else:
                assert new != old
                plan = group["plans"][ident]
                assert plan["expected_native_pages"] == 1 and plan == draft["plans"][ident]
                earlier = first_rows[ident]
                if entry["stored_command_hex"] == earlier["stored_command_hex"] and plan == first_plans[ident]:
                    records.append(earlier | entry | {"reused_native_render": True})
                    continue
                result = audit(ctx, font, paint, expand, None, names, row, new[5:end], plan)
                layouts = []
                for layout in result["layouts"]:
                    page, = layout["pages"]
                    assert page["native_independent_plane_equal"] and page["all_bitmap_header_input_canaries_exact"]
                    pixels = bytes.fromhex(page["native_plane_hex"])
                    previews.append((f"{ident} {layout['scope']}", pixels))
                    layouts.append(dict(scope=layout["scope"], expanded_hex=layout["expanded_hex"],
                                        plane_sha256=native.digest(pixels), lines=layout["lines"]))
                entry.update(native_pages=1, layouts=layouts, original_expansion=result["macro_alignment_checks"])
                refreshed.append(ident)
            records.append(entry)
    modified = sum(row["decision"] == "revision" for row in records)
    assert not rows and len(records) == 146 and modified == 38
    assert sorted(refreshed) == ["DK4_MES_B57_R0030", "DK4_MES_B57_R0135", "DK4_MES_B58_R0068", "DK4_MES_B58_R0076"]
    ROOT.mkdir()
    contact = display.display.inherited.early.contact_sheets
    sheets = FunctionType(contact.__code__, contact.__globals__ | {"ROOT": ROOT})(previews)
    base.save(PROOF, dict(candidate_sha256=candidate, stage_proof_sha256=base.digest(stage.PROOF),
                          records=records, newly_rendered_pages=modified, name_stress_pages=6,
                          refreshed_pages=refreshed, reused_render_path=str(first_path),
                          reused_render_sha256=base.digest(first_path), refreshed_sheets=sheets,
                          sheets=[*first["sheets"], *sheets], initialized_dependencies=ctx.receipt(), default_names=names,
                          runtime_assets=list(display.ASSETS), offline_native_only=True))
    print(f"Checked {modified} native pages, with {len(refreshed)} refreshed after visual review, and 108 byte-exact retentions.")


if __name__ == "__main__":
    main()
