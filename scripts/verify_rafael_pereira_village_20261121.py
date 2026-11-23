"""Check final stored controls, complete native glyphs and name substitutions."""

from types import FunctionType, SimpleNamespace

from scripts import stage_rafael_pereira_village_20261121 as stage
from scripts import verify_all_routes_next_phrase_wraps_20261118 as display
from scripts import verify_seville_square_gameplay_20261121 as seville


base, native, town = stage.base, stage.native, seville.town
ROOT = stage.ROOT / "native_display"
PROOF = ROOT / "native_display.json"


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
    paint, expand = display.clipped_renderer(ctx), display.original_expander()
    font = image.read_file("/GRP/KANJI.FNT")
    expanded, = {case["output_hex"] for case in ctx.execute(expand, b"FI FA FO", 0)["cases"]}
    names = dict(zip(("FI", "FA", "FO"), bytes.fromhex(expanded).decode("ascii").split(" ", 2), strict=True))
    assert names["FI"] == "Rafael" and names["FA"] == "Castor"
    paragraph = display.display.paragraph
    audit = FunctionType(paragraph.__code__, paragraph.__globals__ | {"build": stage})
    fe = town.current_fe_painter(SimpleNamespace(arm=ctx.arm, image=image))
    path = "/data/SC0.DK4"
    bank = native.IlnkContainer.parse(image.read_file(path)).blocks
    rows = {r["id"]: r for r in draft["records"]}
    records, previews = [], []
    revised_pages = 0
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
            selector = row["source_selector"]
            end = new.index(0, 6)
            assert new[:6] == old[:6] == source[:6] == b"\0\x40\xff\xff\0" + bytes([selector])
            assert len(new) % 2 == 0 and not any(new[end:])
            body = new[6:end]
            entry = dict(id=ident, block=block, file_path=path, decision=row["decision"],
                         stored_offset=at, stored_command_hex=new.hex())
            if row["decision"] == "retention":
                assert old == new and new[5:end].hex() == row["current_hex"]
                if selector == 254:
                    result = fe(body)
                    assert result["complete_consumed_bytes"] == len(body)
                    entry.update(retained_system_panel=True, native_pages=1,
                                 panel_mask_sha256=native.digest(result["physical"]))
            else:
                plan = group["plans"][ident]
                assert selector != 254 and old != new and plan == draft["plans"][ident]
                assert plan["expected_native_pages"] == 1
                if stage.review.TOKEN.findall(row["english"]):
                    validated = audit(ctx, font, paint, expand, None, names, row, new[5:end], plan)
                    layouts = validated["layouts"]
                    entry["original_expansion"] = validated["macro_alignment_checks"]
                else:
                    compiled = bytes.fromhex(plan["encoded_hex"])
                    assert new[5:end] in (compiled, compiled + b" ")
                    assert not any(token in body for token in (b"FA", b"FI", b"FO"))
                    assert stage.review.logical(body.decode("ascii")) == row["english"]
                    pages = display.display.raster(ctx, font, paint, body, plan["lines"], 1)
                    layouts = [dict(scope="registered default", expanded_hex=body.hex(), pages=pages, lines=plan["lines"])]
                screens = []
                for layout in layouts:
                    page, = layout["pages"]
                    assert page["native_independent_plane_equal"] and page["all_bitmap_header_input_canaries_exact"]
                    pixels = bytes.fromhex(page["native_plane_hex"])
                    previews.append((f"{ident} {layout['scope']}", pixels))
                    screens.append(dict(scope=layout["scope"], expanded_hex=layout["expanded_hex"],
                                        plane_sha256=native.digest(pixels), lines=layout["lines"]))
                entry.update(native_pages=1, layouts=screens)
                revised_pages += 1
            records.append(entry)
    assert len(records) == 197 and not rows and revised_pages == 110
    assert sum(bool(r.get("retained_system_panel")) for r in records) == 1
    contact = display.display.inherited.early.contact_sheets
    ROOT.mkdir()
    sheets = FunctionType(contact.__code__, contact.__globals__ | {"ROOT": ROOT})(previews)
    base.save(PROOF, dict(candidate_sha256=candidate, stage_proof_sha256=base.digest(stage.PROOF), records=records,
                          revised_pages=revised_pages, name_stress_pages=len(previews) - revised_pages, sheets=sheets,
                          initialized_dependencies=ctx.receipt(), default_names=names,
                          runtime_assets=list(display.ASSETS), offline_native_only=True))
    print(f"Verified {revised_pages} native pages, {len(previews) - revised_pages} name-width cases, and the retained FE notice.")


if __name__ == "__main__":
    main()
