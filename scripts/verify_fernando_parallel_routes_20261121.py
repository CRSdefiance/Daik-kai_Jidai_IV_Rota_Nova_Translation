"""Check all revised speech and both retained coin menus through native consumers."""
from inspect import getsource
from types import FunctionType

from scripts import register_alexandria_dialogue_20261121 as hodram_parent
from scripts import stage_fernando_parallel_routes_20261121 as stage
from scripts import verify_hodram_alexandria_tutorial_20261121 as hodram
from scripts import verify_parallel_ship_lessons_20261121 as earlier
from scripts import verify_rafael_refit_sailing_lessons_20261121 as menu_proof


base, native, display, menu = stage.base, stage.native, earlier.display, earlier.menu
ROOT = stage.ROOT / "native_display"
PROOF = ROOT / "native_display.json"
BYTE_EXACT = "DK4_MES_B127_R0096"

menu_scope = vars(menu_proof) | {"ROOT": ROOT}
exec(compile(getsource(menu_proof.captions), __file__ + "::caption-consumer", "exec"), menu_scope)


def contexts():
    prior = base.load(earlier.PROOF)["initialized_dependencies"]
    result = {}
    for route in (0, 2, 3):
        item = prior[str(route)]
        for name in ("release_proof", "startup_proof"):
            assert base.digest(item[name]) == item[name + "_sha256"]
        result[route] = native.RegisteredRuntime(item["release_proof"], item["startup_proof"], captain=route)
    boot = hodram.ROOT / "ordinary_Hodram_snapshot.json"
    result[1] = native.RegisteredRuntime(hodram_parent.RELEASE, boot, captain=1)
    return result


def main():
    assert not ROOT.exists()
    proof, draft, previous = map(base.load, (stage.PROOF, stage.review.OUTPUT, stage.parent.RELEASE))
    assert proof["candidate_sha256"] == base.digest(stage.ROM) and proof["whole_parent_inverse"]
    assert proof["predecessor_sha256"] == previous["candidate_sha256"]
    assert proof["manuscript_sha256"] == base.digest(stage.review.OUTPUT)
    rom = base.NdsImage.open(stage.ROM)
    ctx = contexts()
    assert all(c.image.read_file(asset) == rom.read_file(asset) for c in ctx.values() for asset in display.ASSETS)
    expand = display.original_expander()
    names = display.route_names(ctx, expand)
    paint = display.clipped_renderer(ctx[0])
    font = rom.read_file("/GRP/KANJI.FNT")
    paragraph = display.display.paragraph
    audit = FunctionType(paragraph.__code__, paragraph.__globals__ | {"build": stage})
    rows = {(r["file_path"], r["id"]): r for r in draft["records"]}
    records, pictures, menus = [], [], []
    ROOT.mkdir()
    for group in proof["groups"]:
        route, path, block = (group[k] for k in ("route", "file_path", "block"))
        payload = native.IlnkContainer.parse(rom.read_file(path)).blocks[block]
        assert native.digest(payload) == group["after"]
        for command in group["commands"]:
            old, new = (bytes.fromhex(command[k]) for k in ("current", "stored"))
            at = command["stored_offset"]
            assert payload[at:at+len(new)] == new
            if command["word"] == 0x2100 and command["record_ids"]:
                menus.append(menu_scope["captions"](ctx[route].arm, command | dict(block=block,
                    source=bytes.fromhex(command["source"]), current=old, stored=new)))
            for ident in command["record_ids"]:
                row = rows.pop((path, ident))
                ret = dict(id=ident, route=route, file_path=path, block=block, decision=row["decision"],
                           stored_offset=at, stored_command_hex=new.hex())
                if row["decision"] == "retention":
                    assert new == old
                    if command["word"] == 0x2100:
                        assert row["english"].encode("ascii") in menu.labels(new)
                        ret.update(native_caption=True, native_pages=0)
                    elif stage.review.TOKEN.findall(row["english"]):
                        assert route == 3 and row["source_record_index"] in (149, 163)
                        body = new[6:new.index(0, 6)]
                        got = ctx[route].execute(expand, body, row["source_selector"])
                        expected = body.replace(b"FO", names[route]["FO"].encode("ascii"))
                        assert {r["output_hex"] for r in got["cases"]} == {expected.hex()}
                        page, = paint(ctx[route].arm, font, expected)["pages"]
                        assert page["native_independent_plane_equal"]
                        ret.update(retained_original_company_resolution=got, native_pages=1)
                else:
                    assert new[:6] == old[:6] == b"\0\x40\xff\xff\0" + bytes([row["source_selector"]])
                    end = new.index(0, 6)
                    assert not any(new[end:])
                    plan = group["plans"][ident]
                    assert plan["expected_native_pages"] == 1
                    checked = audit(ctx[route], font, paint, expand, None, names[route], row, new[5:end], plan)
                    layouts = []
                    for layout in checked["layouts"]:
                        page, = layout["pages"]
                        assert page["native_independent_plane_equal"]
                        pixels = bytes.fromhex(page["native_plane_hex"])
                        pictures.append((f"SC{route} {ident} {layout['scope']}", pixels))
                        layouts.append(dict(scope=layout["scope"], expanded_hex=layout["expanded_hex"],
                                            pages=[native.digest(pixels)], lines=layout["lines"]))
                    assert (new == old) == (ident == BYTE_EXACT)
                    ret.update(native_pages=1, layouts=layouts, original_expansion=checked["macro_alignment_checks"])
                records.append(ret)
    assert not rows and len(records) == 121 and [m["block"] for m in menus] == [169, 136]
    contact = display.display.inherited.early.contact_sheets
    sheets = FunctionType(contact.__code__, contact.__globals__ | {"ROOT": ROOT})(pictures)
    default = sum(r["decision"] == "revision" for r in records)
    assert default == 63 and len(pictures) == 69
    base.save(PROOF, dict(candidate_sha256=proof["candidate_sha256"], stage_proof_sha256=base.digest(stage.PROOF),
        records=records, newly_rendered_pages=default, name_stress_pages=len(pictures)-default,
        offline_native_only=True, native_caption_count=4, native_menu_count=2, menus=menus,
        default_names=names, initialized_dependencies={str(i): c.receipt() for i, c in ctx.items()},
        sheets=[*sheets, *(m["sheet"] for m in menus)]))
    print("Verified 62 changed pages, one exact reflow, six name-length cases and both retained menus.")


if __name__ == "__main__":
    main()
