"""Verify B60 dialogue, pagination, and both native choice objects."""

from types import FunctionType

from dk4tool.dialogue.reviewed_choice_object_v2 import labels
from scripts import check_typed_story_menu_display_20261121 as menu
from scripts import stage_rafael_spain_20261121 as stage
from scripts import verify_all_routes_next_phrase_wraps_20261118 as display


base, native = stage.base, stage.native
ROOT = stage.ROOT / "native_display"
PROOF = ROOT / "native_display.json"


def check_menu(arm, command, rows, adapters):
    assert [r["native_slots"] for r in rows] == [[0], [1]]
    raw = {side: bytes.fromhex(command[side]) for side in ("source", "current", "stored")}
    assert labels(raw["stored"]) == [r["english"].encode("ascii") for r in rows]
    vms, paint, executed = adapters
    checks = {}
    for side, obj in raw.items():
        first, second = [vms[2](arm, obj, alignment) for alignment in (0, 2)]
        assert first == second and [x["modal_selection"] for x in first["VM_cases"]] == [0, 1, -1]
        assert first["labels"] == [v.decode("cp932") for v in labels(obj)]
        checks[side] = first
    width = checks["stored"]["minimum_width_units"] * 6
    pictures, planes = [], []
    for index, (row, caption) in enumerate(zip(rows, labels(raw["stored"]), strict=True)):
        for style in (1, 15):
            pixels, audit = paint(arm, caption, style, width, (0, index * 12))
            assert audit["independent_complete_native_pixels_match"] and audit["storage_padding_all_blank"]
            assert audit["extra_flush_stays_within_physical_backing"] and audit["visible_cell_center_twice"] == width
            planes.append(dict(id=row["id"], style=style, audit=audit, plane_sha256=native.digest(pixels)))
            if style == 1:
                pictures.append((row["english"], width, pixels))
    source_at = rows[0]["source_reference"]["command_offset"]
    assert source_at == rows[1]["source_reference"]["command_offset"]
    path = ROOT / f"spain_choices_{source_at}.png"
    menu.sheet(pictures, path)
    return dict(source_command_offset=source_at, stored_command_offset=command["stored_offset"], captions=checks,
                planes=planes, native_instruction_addresses=len(executed), record_ids=[r["id"] for r in rows],
                sheet=dict(path=str(path), sha256=base.digest(path)))


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
    arm, font = ctx.arm, image.read_file("/GRP/KANJI.FNT")
    expand, paint = display.original_expander(), display.clipped_renderer(ctx)
    surname, = {c["output_hex"] for c in ctx.execute(expand, b"FA", 0)["cases"]}
    names = {"FA": bytes.fromhex(surname).decode("ascii")}
    assert names["FA"] == "Castor"
    paragraph = display.display.paragraph
    audit = FunctionType(paragraph.__code__, paragraph.__globals__ | {"build": stage})
    group, = stored["groups"]
    path = "/data/SC0.DK4"
    assert group["file_path"] == path and group["block"] == 60
    block = native.IlnkContainer.parse(image.read_file(path)).blocks[60]
    assert native.digest(block) == group["after"]
    earlier = stage.ROOT.with_name("staged_v1")
    old_proof = earlier / "native_display/native_display.json"
    previous, previous_stage = map(base.load, (old_proof, earlier / stage.PROOF.name))
    previous_rom = earlier / stage.ROM.name
    assert previous["candidate_sha256"] == previous_stage["candidate_sha256"] == base.digest(previous_rom)
    assert previous["stage_proof_sha256"] == base.digest(earlier / stage.PROOF.name)
    original_image = base.NdsImage.open(previous_rom)
    assert all(original_image.read_file(asset) == image.read_file(asset) for asset in display.ASSETS)
    assert previous["initialized_dependencies"] == ctx.receipt() and previous["default_names"] == names
    assert all(base.digest(s["path"]) == s["sha256"] for s in previous["sheets"])
    previous_rows = {r["id"]: r for r in previous["records"]}
    previous_group, = previous_stage["groups"]
    rows = {r["id"]: r for r in draft["records"]}
    records, previews, choices, refreshed = [], [], [], []
    new_pages = 0
    ROOT.mkdir()
    for command in group["commands"]:
        at = command["stored_offset"]
        old, new, clean = (bytes.fromhex(command[k]) for k in ("current", "stored", "source"))
        assert block[at:at + len(new)] == new
        owned = [rows.pop(i) for i in command["record_ids"]]
        if command["word"] == 0x2100:
            previous_menu = previous["menus"][len(choices)]
            ids = [r["id"] for r in owned]
            assert previous_menu["record_ids"] == ids and previous_menu["stored_command_offset"] == at
            earlier_command, = [c for c in previous_group["commands"] if c["record_ids"] == ids]
            assert earlier_command == command
            assert labels(new) == [r["english"].encode("ascii") for r in owned]
            choices.append(previous_menu)
        for row in owned:
            ident = row["id"]
            entry = dict(id=ident, block=60, file_path=path, decision=row["decision"],
                         stored_offset=at, stored_command_hex=new.hex())
            if command["word"] == 0x2100:
                entry.update(native_caption=True, native_pages=0)
            elif row["decision"] == "retention":
                assert new == old
            else:
                end = new.index(0, 6)
                assert new[:6] == old[:6] == clean[:6] == b"\0\x40\xff\xff\0" + bytes([row["source_selector"]])
                assert not any(new[end:]) and len(new) % 2 == 0
                plan = group["plans"][ident]
                assert plan == draft["plans"][ident]
                old_row = previous_rows[ident]
                if old_row["stored_command_hex"] == new.hex() and previous_group["plans"][ident] == plan:
                    records.append(old_row | entry | {"reused_native_render": True})
                    new_pages += old_row["native_pages"]
                    continue
                result = audit(ctx, font, paint, expand, None, names, row, new[5:end], plan)
                layouts = []
                for layout in result["layouts"]:
                    pages = []
                    for index, page in enumerate(layout["pages"], 1):
                        assert page["native_independent_plane_equal"] and page["all_bitmap_header_input_canaries_exact"]
                        pixels = bytes.fromhex(page["native_plane_hex"])
                        previews.append((f"{ident} {layout['scope']} p{index}", pixels))
                        pages.append(native.digest(pixels))
                    layouts.append(dict(scope=layout["scope"], expanded_hex=layout["expanded_hex"],
                                        pages=pages, lines=layout["lines"]))
                count = plan["expected_native_pages"]
                entry.update(native_pages=count, layouts=layouts, original_expansion=result["macro_alignment_checks"])
                new_pages += count
                refreshed.append(ident)
            records.append(entry)
    assert not rows and len(records) == 103 and [r["source_command_offset"] for r in choices] == [768, 1852]
    assert refreshed == ["DK4_MES_B60_R0486"] and len(previews) == 2 and new_pages == 56
    contact = display.display.inherited.early.contact_sheets
    sheets = FunctionType(contact.__code__, contact.__globals__ | {"ROOT": ROOT})(previews)
    base.save(PROOF, dict(candidate_sha256=candidate, stage_proof_sha256=base.digest(stage.PROOF), records=records,
                          revised_pages=new_pages, name_stress_pages=previous["name_stress_pages"],
                          refreshed_pages=2, reused_native_proof=str(old_proof), reused_native_sha256=base.digest(old_proof),
                          native_caption_count=4, menus=choices, default_names=names,
                          initialized_dependencies=ctx.receipt(), runtime_assets=list(display.ASSETS),
                          offline_native_only=True, sheets=[*previous["sheets"], *sheets]))
    print(f"Verified {new_pages} revised speech pages, including two fresh pages, six name-width cases, and four captions.")


if __name__ == "__main__":
    main()
