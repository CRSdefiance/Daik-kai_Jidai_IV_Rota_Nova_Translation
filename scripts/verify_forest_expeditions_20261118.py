"""Verify the stored forest dialogue and captions with the native consumers."""

from inspect import getsource
from struct import unpack_from
import sys
from types import FunctionType

from dk4tool.dialogue.reviewed_actor_style_object_v1 import unpack
from dk4tool.dialogue.reviewed_choice_object_v2 import count_and_base, labels
from scripts import check_editorial_two_choice_explicit_route_v1 as two
from scripts import check_rafael_three_choice_single_v1 as three
from scripts import reconcile_lil_B111_B119_voices_v3218 as roles
from scripts import stage_forest_expeditions_20261118 as stage
from scripts import stage_rafael_early_wraps_20261111 as early
from scripts import verify_lil_clifford_north_new_world_FE_v2980 as fe
from scripts.source_locked_derivation_v5118 import checked_text
from scripts.stage_kurushima_encounter_20261115 import visible_lines


base, native, parent = stage.base, stage.native, stage.parent
OUTPUT = stage.ROOT / "native_display_v5"
PREVIOUS = stage.ROOT.with_name("research_v1") / OUTPUT.name


def check_styles(ctx, raw):
    offsets, bodies = unpack(raw)
    cpu, get, _ = ctx.machine(ctx.arm, ctx.common, ctx.raw, ctx.plan)
    stream, owner = 0x02660000, 0x02662000
    cpu.mem_write(stream - 16, b"\xa5" * (len(raw) + 32))
    cpu.mem_write(stream, raw)
    cpu.mem_write(owner - 16, b"\xa5" * 64)
    cpu.mem_write(owner, b"\0" * 4 + stream.to_bytes(4, "little") + b"\0" * 8)
    guards = bytes(cpu.mem_read(owner - 16, 64))
    memory = bytes(cpu.mem_read(0x02000000, 0x400000))
    slots = []
    for index, offset in enumerate(offsets):
        pointer = get(0x2A154, owner, index)
        body = bodies[offset]
        assert pointer == stream + 20 + offset
        assert bytes(cpu.mem_read(pointer, len(body) + 1)) == body + b"\0"
        assert bytes(cpu.mem_read(owner - 16, 64)) == guards
        assert bytes(cpu.mem_read(0x02000000, 0x400000)) == memory
        assert bytes(cpu.mem_read(stream - 16, len(raw) + 32)) == b"\xa5" * 16 + raw + b"\xa5" * 16
        slots.append(dict(style=index, body_offset=20 + offset, body_hex=body.hex()))
    ctx.calls.clear()
    return slots, bodies


def progress_expander():
    original = early.prior.expansion
    source = checked_text(getsource(original.expand), {
        "assert identity==prefix and captain==2":
            "assert captain == 3 and (0 <= identity < 207 if 207 <= prefix < 224 else identity == prefix)",
    })
    env = vars(original).copy()
    exec(compile(source, __file__ + "::qualified-progressive-expander", "exec"), env)
    return env["expand"]


def validate_roles(ctx, proof):
    selectors = sorted({207} | {
        plan["source_selector"] for group in proof["groups"] for plan in group["plans"].values()
        if 207 <= plan.get("source_selector", 254) < 224
    })
    source = checked_text(getsource(roles.dynamic), {"==captain==2": "==captain==3"})
    env = vars(roles).copy()
    exec(compile(source, __file__ + "::qualified-role-lookup", "exec"), env)
    return ctx.execute(env["dynamic"], selectors)["rows"]


def validate_paragraph(ctx, font, paint, expand, fe_paint, row, raw, plan):
    selector, body = raw[0], raw[1:]
    planned = bytes.fromhex(plan["encoded_hex"])
    assert planned[0] == selector and raw in (planned, planned + b" ")
    assert " ".join(body.decode("ascii").split()) == row["english"]
    if selector == 254:
        expanded = ctx.execute(fe.expand, body)
        surface = fe_paint(body)
        membership = stage.system.check_FE_rows(body, surface)
        reference = fe_paint(planned[1:])
        expected = stage.system.visible_events(reference)
        pixels = surface.pop("physical")
        surface.pop("logical")
        assert pixels == reference["physical"] and stage.system.visible_events(surface) == expected
        assert surface["complete_consumed_bytes"] == len(body)
        assert len(pixels) == 228 * 64 and not any(
            any(pixels[y * 228 + 216:(y + 1) * 228]) for y in range(64)
        )
        plane = b"".join(pixels[y * 228:y * 228 + 216] for y in range(64))
        pages = [dict(page=1, native_plane_hex=plane.hex(), **membership)]
    else:
        expanded = ctx.execute(expand, body, selector)
        surface = paint(ctx.arm, font, body)
        assert surface["complete_consumed_bytes"] == len(body)
        pages = surface["pages"]
        assert pages[0]["first_visible_origin"] == [0, 0]
        assert [line for page in pages for line in visible_lines(page)] == plan["lines"]
        if raw != planned:
            reference = paint(ctx.arm, font, planned[1:])
            assert [p["native_plane_hex"] for p in pages] == [p["native_plane_hex"] for p in reference["pages"]]
    assert len(pages) == plan.get("expected_native_pages", 1) == 1
    assert len(expanded["cases"]) == 4 and all(c["output_hex"] == body.hex() for c in expanded["cases"])
    return dict(id=row["id"], file_path=row["file_path"], kind=row["kind"], target_hex=raw.hex(),
                planned_lines=plan["lines"], processor=expanded, pages=pages)


def menu_checker(ctx, release, command, rows, folder):
    raw = bytes.fromhex(command["stored"])
    count, header = count_and_base(raw)
    assert len(rows) == count
    prepared = []
    for i, (row, caption) in enumerate(zip(rows, labels(raw), strict=True)):
        assert caption == row["english"].encode("ascii")
        target = command["stored_offset"] + header + unpack_from("<H", raw, 2 + 2 * i)[0]
        prepared.append(row | dict(source_index=i, source_command_offset=command["source_offset"],
            source_choice_object_hex=command["source"], current_choice_object_hex=command["current"],
            target_reference=dict(offset=target, command_offset=command["stored_offset"], index=i),
            source_reference=row["source_reference"] | {"file_path": row["file_path"]},
            current_reference=row["current_reference"] | {"file_path": row["file_path"]}))
    metadata = folder.with_suffix(".json")
    base.save(metadata, dict(records=prepared, typed_choice_objects=count, file_path=rows[0]["file_path"],
                              current_ROM_sha256=ctx.release["candidate_sha256"]))
    arguments = ["--manuscript", str(metadata), "--release", str(parent.RELEASE),
                 "--startup", release["own_registered_startup"], "--out", str(folder)]
    if count == 3:
        source = checked_text(three.source, {
            "ctx=RegisteredRuntime(args.release,args.startup,captain=0)":
                "ctx=RegisteredRuntime(args.release,args.startup,captain=3)",
        })
        scope = {**vars(three), "__name__": three.__name__}
        exec(compile(source, __file__ + "::same-three-choice-contract-with-registered-snapshot", "exec"), scope)
        run = scope["main"]
    else:
        arguments += ["--captain", "3"]
        run = two.main
    argv = sys.argv
    try:
        sys.argv = [__file__, *arguments]
        run()
    finally:
        sys.argv = argv
    path = folder / "menu_provider_and_planes.json"
    proof = base.load(path)
    target_hex = (proof["menus"][0]["target_object_hex"] if count == 3
                  else proof["native_choice_object_hex"])
    assert target_hex == raw.hex() and proof["complete_caption_glyphs_centering_bounds_guards_andconsumption_pass"]
    return dict(menu_path=str(path), proof_sha256=base.digest(path), option_ids=command["record_ids"],
                planes=proof["complete_English_caption_style_planes"])


def main():
    proof = base.load(stage.PROOF)
    release = base.load(parent.RELEASE)
    assert proof["candidate_sha256"] == base.digest(stage.ROM) and proof["whole_parent_inverse"]
    assert proof["manuscript_sha256"] == base.digest(stage.review.MANUSCRIPT)
    previous = base.load(PREVIOUS / "native_display.json")
    previous_stage_path = PREVIOUS.parent / "stored_proof.json"
    assert previous["stage_proof_sha256"] == base.digest(previous_stage_path)
    previous_stage = base.load(previous_stage_path)
    for key in ("manuscript_sha256", "predecessor_sha256", "preserved_ARM9_sha256", "source_sha256"):
        assert proof[key] == previous_stage[key]
    prior_commands = {(group["file_path"], cmd["source_offset"]): cmd
                      for group in previous_stage["groups"] for cmd in group["commands"]}
    prior_paragraphs = {(row["file_path"], row["id"]): row for row in previous["checked_paragraphs"]}
    prior_menus = {tuple(item["option_ids"]): item for item in previous["menus"]}
    prior_styles = {(group["file_path"], item["source_offset"]): receipt
                    for group in previous_stage["groups"]
                    for item in group["commands"] if item["word"] == stage.STYLE
                    for receipt in previous["styles"]
                    if receipt["file_path"] == group["file_path"] and receipt["offset"] == item["stored_offset"]}
    assert not OUTPUT.exists()
    OUTPUT.mkdir()
    manuscript = base.load(stage.review.MANUSCRIPT)
    rows = {(row["file_path"], row["id"]): row for row in manuscript["records"]}
    ctx = native.RegisteredRuntime(parent.RELEASE, release["own_registered_startup"], captain=3)
    image = base.NdsImage.open(stage.ROM)
    assert image.read_file(native.ARM) == ctx.arm
    font = ctx.image.read_file("/GRP/KANJI.FNT")
    assert image.read_file("/GRP/KANJI.FNT") == font
    _, paint = early.prior.precedent.planners(ctx.arm)
    expand, fe_paint = progress_expander(), stage.system.native_painter(ctx)
    dynamic = validate_roles(ctx, proof)
    checked, styles, menus, pictures, reused = [], [], [], [], []
    for group in proof["groups"]:
        file, n = group["file_path"], group["block"]
        block = native.IlnkContainer.parse(image.read_file(file)).blocks[n]
        assert native.digest(block) == group["after"]
        for command in group["commands"]:
            if command["current"] == command["stored"] or not command["record_ids"]:
                continue
            records = [rows[file, key] for key in command["record_ids"]]
            word, offset = command["word"], command["stored_offset"]
            raw = bytes.fromhex(command["stored"])
            assert block[offset:offset + len(raw)] == raw
            key = file, command["source_offset"]
            same_object = command["stored"] == prior_commands[key]["stored"]
            if word in stage.MENU:
                assert same_object
                prior_menu = prior_menus[tuple(command["record_ids"])]
                assert base.digest(prior_menu["menu_path"]) == prior_menu["proof_sha256"]
                menus.append(prior_menu | {"candidate_menu_offset": offset, "identical_native_object_reused": True})
                continue
            if word == stage.STYLE:
                if same_object:
                    slots = prior_styles[key]["slots"]
                    _, bodies = unpack(raw)
                else:
                    slots, bodies = check_styles(ctx, raw)
                source_slots, _ = unpack(bytes.fromhex(command["source"]))
                stored_slots, _ = unpack(raw)
                assert [(a == b) for a in source_slots for b in source_slots] == [
                    (a == b) for a in stored_slots for b in stored_slots
                ]
                styles.append(dict(file_path=file, block=n, offset=offset, slots=slots,
                                   identical_native_object_reused=same_object))
                assert len(records) == len(bodies)
                typed = [(raw[19:20] + bodies[i], row) for i, row in zip(sorted(bodies), records, strict=True)]
            else:
                assert word == stage.SPEECH
                row, = records
                typed = [(raw[5:raw.index(0, 6)], row)]
            for text, row in typed:
                if row["decision"] == "retention":
                    assert text[1 if word == stage.STYLE else 0:].hex() == row["current_hex"]
                    continue
                identity = file, row["id"]
                plan = group["plans"][row["id"]]
                prior = prior_paragraphs[identity]
                if prior["target_hex"] == text.hex() and prior["planned_lines"] == plan["lines"]:
                    checked.append(prior)
                    reused.append(identity)
                    continue
                try:
                    record = validate_paragraph(ctx, font, paint, expand, fe_paint, row, text, plan)
                except AssertionError as error:
                    raise AssertionError((file, row["id"], text)) from error
                checked.append(record)
                for page in record["pages"]:
                    pictures.append((f"SC{group['route']} {row['id']} / {page['page']}",
                                     bytes.fromhex(page["native_plane_hex"])))
        print(f"SC{group['route']} complete", flush=True)
        base.save(OUTPUT / f"route_{group['route']}_checkpoint.json", dict(
            paragraphs=[r for r in checked if r["file_path"] == file],
            styles=[r for r in styles if r["file_path"] == file],
            reviewed_candidate_sha256=proof["candidate_sha256"],
        ))
    edited = {(r["file_path"], r["id"]) for r in rows.values() if r["decision"] == "revision"}
    rendered = {(r["file_path"], r["id"]) for r in checked}
    for menu in menus:
        checker = base.load(menu["menu_path"])
        metadata = base.load(checker["manuscript"])
        rendered.update((r["file_path"], r["id"]) for r in metadata["records"] if r["decision"] == "revision")
    assert rendered == edited and len(checked) == 78 and len(styles) == 30 and len(menus) == 6
    assert len(reused) + len(pictures) == 78 and 1 <= len(pictures) <= 12
    make_sheets = FunctionType(early.contact_sheets.__code__, vars(early) | {"ROOT": OUTPUT})
    sheets = make_sheets(pictures)
    base.save(OUTPUT / "native_display.json", dict(compiled_candidate_sha256=proof["candidate_sha256"],
        stage_proof_sha256=base.digest(stage.PROOF), exact_revised_record_count=len(rendered),
        checked_paragraphs=checked, styles=styles, menus=menus, current_startup_roles=dynamic,
        reused_paragraphs=reused, fresh_paragraphs=len(pictures),
        identical_proof=dict(path=str(PREVIOUS / "native_display.json"),
                            sha256=base.digest(PREVIOUS / "native_display.json")),
        previous_sheets=previous["sheets"], sheets=sheets, actual_gameplay=False,
        manual_visual_review_pending=True))
    print("All 87 revised records passed native display checks.", flush=True)


if __name__ == "__main__":
    main()
