"""Verify the B84 text renderers, original menu indices and installed page boundaries."""

from inspect import getsource
from types import FunctionType, SimpleNamespace

from dk4tool.dialogue.reviewed_choice_object_v2 import labels
from scripts import check_typed_story_menu_display_20261121 as menu
from scripts import stage_rafael_gerhard_tutorial_20261121 as stage
from scripts import verify_rafael_spain_london_20261121 as precedent
from scripts.check_editorial_compiled_pages_v6 import check_FE_rows
from scripts.source_locked_derivation_v5118 import checked_text


base, native, display, town = stage.base, stage.native, precedent.display, precedent.town
ROOT = stage.ROOT / "native_display"
PROOF = ROOT / "native_display.json"


def verify_menu(arm, originals, command, rows, adapters):
    vms, paint, executed = adapters
    count = len(rows)
    assert [row["native_slots"] for row in rows] == [[i] for i in range(count)]
    source = originals[command["source_offset"]]
    objects = [bytes.fromhex(raw) for raw in (source["whole_command_hex"], command["current"], command["stored"])]
    result = []
    for raw in objects:
        value, shifted = [vms[count](arm, raw, alignment) for alignment in (0, 2)]
        assert value == shifted and value["labels"] == [caption.decode("cp932") for caption in labels(raw)]
        assert [case["modal_selection"] for case in value["VM_cases"]] == [*range(count), -1]
        result.append(value)
    compiled = labels(objects[-1])
    assert compiled == [row["english"].encode("ascii") for row in rows]
    width = result[-1]["minimum_width_units"] * 6
    pictures, planes = [], []
    for index, (row, caption) in enumerate(zip(rows, compiled, strict=True)):
        for style in (1, 15):
            pixels, audit = paint(arm, caption, style, width, (0, index * 12))
            assert audit["independent_complete_native_pixels_match"] and audit["storage_padding_all_blank"]
            assert audit["extra_flush_stays_within_physical_backing"] and audit["visible_cell_center_twice"] == width
            planes.append(dict(id=row["id"], slot=index, style=style, audit=audit, plane_sha256=native.digest(pixels)))
            if style == 1:
                pictures.append((row["english"], width, pixels))
    path = ROOT / f"choice_{command['source_offset']}.png"
    menu.sheet(pictures, path)
    assert executed
    return dict(stored_command_offset=command["stored_offset"], source_command_offset=source["offset"], count=count,
                record_ids=command["record_ids"], native_vm_cases=result, planes=planes,
                native_instruction_addresses=len(executed), sheet=dict(path=str(path), sha256=base.digest(path)))


def main():
    assert not PROOF.exists()
    stored, draft, release = map(base.load, (stage.PROOF, stage.OUTPUT, stage.parent.RELEASE))
    candidate = base.digest(stage.ROM)
    assert stored["candidate_sha256"] == candidate and stored["whole_parent_inverse"]
    assert stored["predecessor_sha256"] == release["candidate_sha256"] == base.digest(stage.parent.ROM)
    assert stored["manuscript_sha256"] == base.digest(stage.OUTPUT)
    dependency = base.load(stage.parent.display.PROOF)["initialized_dependencies"]
    for key in ("release_proof", "startup_proof"):
        assert base.digest(dependency[key]) == dependency[key + "_sha256"]
    ctx = native.RegisteredRuntime(dependency["release_proof"], dependency["startup_proof"], captain=0)
    image, clean = map(base.NdsImage.open, (stage.ROM, native.CLEAN))
    assert all(ctx.image.read_file(path) == image.read_file(path) for path in display.ASSETS)
    arm, font = (image.read_file(path) for path in (native.ARM, "/GRP/KANJI.FNT"))
    paint, expand = display.clipped_renderer(ctx), display.original_expander()
    paragraph = display.display.paragraph
    source = checked_text(getsource(paragraph), {
        '{macro: example for macro in tokens}':
            '{macro: example + " Co." if macro == "FO" and n == 16 else example for macro in tokens}'
    })
    scope = paragraph.__globals__ | {"build": stage}
    exec(compile(source, __file__ + "::full-company-width", "exec"), scope)
    audit = scope["paragraph"]
    fe = town.current_fe_painter(SimpleNamespace(arm=arm, image=image))
    expanded, = {case["output_hex"] for case in ctx.execute(expand, b"FI FA FO", 0)["cases"]}
    names = dict(zip(("FI", "FA", "FO"), bytes.fromhex(expanded).decode("ascii").split(" ", 2), strict=True))
    assert (names["FI"], names["FA"], names["FO"]) == ("Rafael", "Castor", "Castor Co.")
    inventory, _, _ = native.scoped_inventory()
    clean_block, block = [native.IlnkContainer.parse(item.read_file(stage.PATH)).blocks[84] for item in (clean, image)]
    originals = {item["offset"]: item for item in inventory(clean.read_file(native.ARM), clean_block)[0]}
    group, = stored["groups"]
    assert native.digest(block) == group["after"]
    rows = {r["id"]: r for r in draft["records"]}
    entries, ordinary, system, menus, reclaimed = {}, [], [], [], []
    revisions = stress = 0
    ROOT.mkdir(exist_ok=True)
    predecessors = menu.adapters(arm)
    for command in group["commands"]:
        stored_raw = bytes.fromhex(command["stored"])
        at = command["stored_offset"]
        assert block[at:at + len(stored_raw)] == stored_raw
        if not command["record_ids"]:
            continue
        members = [rows[ident] for ident in command["record_ids"]]
        if command["word"] in stage.compiler.MENU:
            checked = verify_menu(arm, originals, command, members, predecessors)
            menus.append(checked)
            for row in members:
                entries[row["id"]] = dict(id=row["id"], kind=row["kind"], decision=row["decision"], stored_pages=[command])
            continue
        row, = members
        ident, selector, number = row["id"], row["source_selector"], command["page"]
        current = bytes.fromhex(command["current"])
        assert stored_raw[:6] == current[:6] == bytes.fromhex("0040ffff00") + bytes([selector])
        end = stored_raw.index(0, 6)
        assert len(stored_raw) % 2 == 0 and not any(stored_raw[end:])
        if row["decision"] == "retention":
            assert stored_raw == current
        entry = entries.setdefault(ident, dict(id=ident, kind=row["kind"], decision=row["decision"], stored_pages=[]))
        entry["stored_pages"].append(command)
        if selector == 254:
            body = stored_raw[6:end]
            expected = row["editable_FE_pages"][number - 1]
            assert stage.review.logical(body.decode("ascii")) == expected
            tokens = stage.review.TOKEN.findall(expected)
            if tokens:
                assert tokens == ["FI"]
                value = ctx.execute(expand, body, 0)["cases"]
                assert {case["output_hex"] for case in value} == {body.replace(b"FI", b"Rafael").hex()}
                body = body.replace(b"FI", b"Rafael")
            result = fe(body)
            assert result["complete_consumed_bytes"] == len(body)
            rows_fit = check_FE_rows(body, result)
            plan = command["plan"]
            if plan:
                assert rows_fit["actual_rows"] == plan["lines"]
            plane = result["physical"]
            assert len(plane) == 228 * 64
            system.append((f"{ident} panel {number}", plane))
            entry.setdefault("system", []).append(dict(expanded_hex=body.hex(), row_proof=rows_fit, plane_sha256=native.digest(plane)))
            revisions += row["decision"] == "revision"
            continue
        plan = command["plan"]
        if not plan:
            continue
        count = plan["expected_native_pages"]
        if stage.review.TOKEN.findall(row["english"]):
            checked = audit(ctx, font, paint, expand, None, names, row, stored_raw[5:end], plan)
            layouts = checked["layouts"]
            entry["original_expansion"] = checked["macro_alignment_checks"]
        else:
            assert stored_raw[5:end] in (bytes.fromhex(plan["encoded_hex"]), bytes.fromhex(plan["encoded_hex"]) + b" ")
            assert stage.review.logical(stored_raw[6:end].decode("ascii")) == row["english"]
            pages = display.display.raster(ctx, font, paint, stored_raw[6:end], plan["lines"], count)
            layouts = [dict(scope="registered default", expanded_hex=stored_raw[6:end].hex(), pages=pages, lines=plan["lines"])]
            previous_body = current[6:current.index(0, 6)]
            if previous_body.count(10) >= 4 or count > 1:
                old_count = len(paint(arm, font, previous_body)["pages"])
                if old_count != count:
                    reclaimed.append(dict(id=ident, previous_pages=old_count, current_pages=count))
        validations = []
        for layout in layouts:
            hashes = []
            assert len(layout["pages"]) == count
            for num, page in enumerate(layout["pages"], 1):
                assert page["native_independent_plane_equal"] and page["all_bitmap_header_input_canaries_exact"]
                pixels = bytes.fromhex(page["native_plane_hex"])
                ordinary.append((f"{ident} {layout['scope']} {num}/{count}", pixels))
                hashes.append(native.digest(pixels))
            validations.append(dict(scope=layout["scope"], expanded_hex=layout["expanded_hex"], lines=layout["lines"], page_sha256=hashes))
        entry["layouts"] = validations
        revisions += count
        stress += (len(layouts) - 1) * count
    assert len(entries) == len(rows) == 131 and len(menus) == 2
    assert sorted(item["count"] for item in menus) == [2, 3]
    assert sum(len(row["stored_pages"]) == 2 for row in entries.values()) == 2
    make_sheets = FunctionType(precedent.sheet.__code__, precedent.sheet.__globals__ | {"ROOT": ROOT},
                               argdefs=precedent.sheet.__defaults__)
    sheets = make_sheets(ordinary) + make_sheets(system, system=True)
    sheets += [obj["sheet"] for obj in menus]
    base.save(PROOF, dict(candidate_sha256=candidate, stage_proof_sha256=base.digest(stage.PROOF), records=list(entries.values()),
        revised_speech_pages=revisions, alternate_name_width_pages=stress, FE_panels=len(system), menus=menus,
        sheets=sheets, pagination_changes=reclaimed, default_names=names, initialized_dependencies=ctx.receipt(),
        runtime_assets=list(display.ASSETS), offline_native_only=True))
    print(f"Verified {revisions} revised speech pages, {len(system)} FE panels and all five typed captions.")


if __name__ == "__main__":
    main()
