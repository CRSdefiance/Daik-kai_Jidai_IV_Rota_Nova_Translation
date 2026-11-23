"""Check the original Gallery, story still and legacy save display boundaries."""

from collections import defaultdict
from pathlib import Path
from struct import pack, unpack

from unicorn import UC_HOOK_CODE
from unicorn.arm_const import (
    UC_ARM_REG_LR, UC_ARM_REG_PC, UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_R2,
    UC_ARM_REG_R3, UC_ARM_REG_R5, UC_ARM_REG_R7, UC_ARM_REG_R8, UC_ARM_REG_R9,
    UC_ARM_REG_R11, UC_ARM_REG_SP,
)

from dk4tool.patch.gallery_caption_bounds import validate as validate_gallery
from scripts import checkpoint_pending_shared_native_20261115 as prior
from scripts import register_sea_hazard_dialogue_20261119 as current
from scripts.inventory_common_scene_caption_duplicates import captions as clean_gallery
from scripts.probe_button_prompt_native import BASE, STACK, VIEW, call, machine
from scripts.verify_captain_biographies_v1 import native_selector as biography_selector


base, stage = current.base, current.stage
BOOK = Path("translations/editorial_checkpoints/SharedText_20261110_v1")
OUTPUT = BOOK / "shared_display_owners_20261119_v1.json"
SCENES = Path("translations/common_scene_labels_manuscript_v2.json")
GALLERY = Path("releases/all_routes_editorial_20261111_visible_gallery_captions_candidate/verification/registered_caption_review.json")
CHOOSER = Path("releases/all_routes_editorial_20261111_captain_biographies_candidate/verification/registered_review.json")
OPENINGS = BOOK / "opening_scene_display_scope_20261119_v1.json"
CONTINUE = BOOK / "continue_legacy_calls_20261115_v1.json"
BINDINGS = current.parent.PENDING
ROUTING = Path("work/analysis/event_still_routing_v426/routing_proof.json")
GETTER, COPIER, SINK = 0x0205528C, 0x020534F4, 0x020EF068
OWNER, STREAM = VIEW + 0x8000, VIEW + 0x1000


def native_gallery(cpu, clean, current_rows, original_images):
    output = []
    for route, count in enumerate((46, 41, 39, 38)):
        cpu.mem_write(OWNER, bytes(0x80))
        cpu.reg_write(UC_ARM_REG_R11, OWNER)
        cpu.emu_start(0x02042C74, 0x02042C94, count=16)
        cpu.mem_write(OWNER + 0x1C, pack("<I", route))
        cpu.reg_write(UC_ARM_REG_R5, 0)
        cpu.emu_start(0x02042E5C, 0x02042ED4, count=32)
        assert cpu.reg_read(UC_ARM_REG_R9) == count
        for index in range(count):
            row = current_rows[(route, index)]
            cpu.reg_write(UC_ARM_REG_R7, index)
            cpu.reg_write(UC_ARM_REG_SP, STACK)
            cpu.emu_start(0x02042F58, 0x02042F6C, count=8)
            assert cpu.reg_read(UC_ARM_REG_PC) == 0x02042F6C
            assert cpu.reg_read(UC_ARM_REG_R1) == original_images[route][index]
            assert cpu.reg_read(UC_ARM_REG_R8) + index * 4 == BASE + row["field"]
            cpu.emu_start(0x02042FD0, 0x02043008, count=1024)
            assert cpu.reg_read(UC_ARM_REG_PC) == 0x02043008
            ptr = cpu.reg_read(UC_ARM_REG_R2)
            caption = bytes(cpu.mem_read(ptr, 128)).split(b"\0", 1)[0]
            expected = row["bytes"]
            x = cpu.reg_read(UC_ARM_REG_R3)
            assert ptr == row["pointer"] and caption == expected
            assert x == 128 - len(expected) * (6 if clean else 5) // 2
            if not clean:
                assert x == row["bounds"][0]
            output.append(dict(route=route, position=index, image=original_images[route][index],
                               field=row["field"], pointer=ptr, text_hex=caption.hex(), draw_x=x))
    assert len(output) == 164
    return output


def still_filenames(cpu, images):
    filenames = []

    def hook(native, pc, _size, _user):
        if pc in (GETTER, COPIER):
            raise AssertionError(f"Still image path unexpectedly requested COMMON text at {pc:#x}")
        if pc == 0x020D4170:
            assert native.reg_read(UC_ARM_REG_R0) == OWNER
            native.reg_write(UC_ARM_REG_R0, VIEW)
        elif pc == 0x020B7158:
            assert native.reg_read(UC_ARM_REG_R0) == VIEW
            addr = native.reg_read(UC_ARM_REG_R1)
            filenames.append(bytes(native.mem_read(addr, 32)).split(b"\0", 1)[0].decode("ascii"))
        else:
            return
        native.reg_write(UC_ARM_REG_PC, native.reg_read(UC_ARM_REG_LR))

    callback = cpu.hook_add(UC_HOOK_CODE, hook)
    try:
        for index in images:
            cpu.mem_write(OWNER + 4, pack("<I", STREAM))
            cpu.mem_write(STREAM, pack("<2H", 0, 0x8000 | index))
            cpu.reg_write(UC_ARM_REG_R5, OWNER)
            cpu.reg_write(UC_ARM_REG_SP, STACK)
            cpu.emu_start(0x02029F94, 0x02029FB4, count=16)
            assert cpu.reg_read(UC_ARM_REG_PC) == 0x02029FB4
            assert cpu.reg_read(UC_ARM_REG_R1) == index
            # The canvas owner is supplied. Use the original filename formatter,
            # then intercept the allocator and file-reader boundaries.
            call(cpu, 0x28B74, (OWNER, index))
            assert filenames[-1] == f"/evstill/evstill{index:03d}.pxl"
    finally:
        cpu.hook_del(callback)
    return filenames


def legacy_sink(clean, active):
    expected = (0x020EDDAC, 0x020EDE48, 0x020EDF48, 0x020EDF84,
                0x020EDF9C, 0x020EDFD0, 0x020EE158, 0x020EF048)
    code = [(-4, 4) if pc in (0x020EDF84, 0x020EDF9C, 0x020EDFD0) else (-12, 4)
            for pc in expected]
    earlier = base.load(CONTINUE)
    for rom in (clean, active):
        matches = []
        for name, address, data in prior.components(rom.rom):
            matches.extend((name, addr, kind) for addr, _, kind in prior.branch_hits(data, address, {SINK}))
        assert matches == [("ARM9 section 0", site, "arm_bl") for site in expected]
        arm = rom.read_file(stage.ARM)
        for span in earlier["verified_code_spans"]:
            assert current.native.digest(arm[span["start"]-BASE:span["end"]-BASE]) == span["sha256"]
        assert arm[SINK-BASE:SINK-BASE+4] == bytes.fromhex("1eff2fe1")  # bx lr

    ja, en = (r.read_file(stage.ARM) for r in (clean, active))
    for site, (before, after) in zip(expected, code, strict=True):
        start, end = site-BASE+before, site-BASE+after
        assert ja[start:end] == en[start:end]
    loads = (0x020EDE44, 0x020EDF80, 0x020EDF98, 0x020EDFCC)
    assert [x[0] for x in prior.branch_hits(en[0xEDCC8:0xEE154], 0x020EDCC8, {GETTER})] == list(loads)
    assert all(site + 4 in expected for site in loads)
    assert en[0xEDE40:0xEDE44] == pack("<I", 0xE3A00070)  # mov r0, #112
    verified = earlier["controlled_offline_cases"]
    assert any(111 in row["loaded_ids"] for row in verified)
    return dict(entry=SINK, original_arm_return_opcode="1eff2fe1", executable_references=list(expected),
        common_getter_calls=dict(zip(map(hex, loads), (112, 112, 111, 112), strict=True)),
        other_inputs=["backup memory status literal", "load status literal", "end status literal",
                      "formatted memory-card or controller status"],
        complete_legacy_save_sink_reference_inventory=True,
        classification_111="Known load diagnostic fetch, followed by an immediate return without drawing.",
        known_silent_branch_evidence=str(CONTINUE))


def main():
    assert not OUTPUT.exists()
    release = base.load(current.RELEASE)
    ledger = base.load(base.LEDGER)
    assert base.digest(current.ROM) == release["candidate_sha256"] == ledger["current_integrated_candidate"]["sha256"]
    assert base.digest(base.REGISTRY) == release["registry_sha256"]
    assert base.digest(stage.CLEAN) == release["clean_input_sha256"]
    clean, active = map(base.NdsImage.open, (stage.CLEAN, current.ROM))
    ja, en = (r.read_file(stage.ARM) for r in (clean, active))
    common = active.read_file(stage.COMMON)
    assert current.native.digest(common) == release["target_COMMON_sha256"]
    assert current.native.digest(en) == release["target_ARM9_sha256"]
    workflow = stage.workflow
    source = workflow.common_message_entries(clean.read_file(stage.COMMON), ja)
    installed = workflow.owned_entries(common, en, current.native.digest(en[workflow.DIRECTORY_OFFSET:workflow.TABLE_OFFSET]))
    rows = base.load(BINDINGS)["records"]
    assert len(rows) == 276
    for row in rows:
        number = row["message_ID"]
        for entry, reference, raw in ((source[number], "source_reference", "source_hex"),
                                      (installed[number], "current_reference", "current_hex")):
            assert workflow.reference(entry) == row[reference]
            assert entry.text.hex() == row[raw]

    for start, end in ((0x28B74, 0x28BAC), (0x29F94, 0x29FB8), (0x42C74, 0x42C94),
                       (0x42E5C, 0x42ED4), (0x42F58, 0x42F70),
                       (0x432DC, 0x432FC), (0xCED28, 0xCED50)):
        assert ja[start:end] == en[start:end]
    normalized = bytearray(en[0x42FD0:0x4300C])
    for at, original, accepted in ((0x42FDC, "06c0a0e3", "05c0a0e3"),
                                    (0x42FF0, "04608de5", "04508de5")):
        index = at - 0x42FD0
        assert normalized[index:index+4] == bytes.fromhex(accepted)
        normalized[index:index+4] = bytes.fromhex(original)
    assert bytes(normalized) == ja[0x42FD0:0x4300C]
    previously = base.load(GALLERY)["records"]
    modern = validate_gallery(en)
    modern_rows = {(r["route"], r["position"]): r | {"bytes": r["English"].encode("ascii")}
                   for r in modern}
    old = {(r["route_index"], r["index"]): dict(field=r["pointer_field"], pointer=BASE+r["offset"],
              bytes=bytes.fromhex(r["source_hex"])) for r in clean_gallery(ja)}
    assert len(modern_rows) == len(old) == len(previously) == 164
    for row in previously:
        key = row["route"], row["position"]
        assert all(row["review"].values()) and row["english"] == modern_rows[key]["English"]
        assert row["source_Japanese"] == old[key]["bytes"].decode("cp932")

    opening = base.load(OPENINGS)
    for path, digest in opening["original_visible_asset_sha256"].items():
        assert current.native.digest(active.read_file(path)) == digest
    runtime = workflow.RegisteredRuntime(current.RELEASE, release["own_registered_startup"], captain=3)
    translated_cpu, _, _ = runtime.machine(runtime.arm, runtime.common, runtime.raw, runtime.plan)
    before_cpu = machine(ja)
    gallery_images = [r["image_indices"] for r in base.load(ROUTING)["Gallery_tables"][0]["routes"]]
    before = native_gallery(before_cpu, True, old, gallery_images)
    after = native_gallery(translated_cpu, False, modern_rows, gallery_images)
    gallery_sources = defaultdict(list)
    for original, translated in zip(before, after, strict=True):
        assert all(original[k] == translated[k] for k in ("route", "position", "image", "field"))
        gallery_sources[original["text_hex"]].append(dict(clean=original, current=translated))

    scene_rows = {r["message_ID"]: r for r in base.load(SCENES)["records"]}
    art = {n: row["artwork"] for n, row in scene_rows.items() if row["artwork"]}
    indices = sorted({r["image_index"] for r in art.values()})
    assert indices == list(range(168))
    assert still_filenames(before_cpu, indices) == still_filenames(translated_cpu, indices) == [
        f"/evstill/evstill{n:03d}.pxl" for n in indices]
    for item in art.values():
        path = item["path"]
        assert current.native.digest(clean.read_file(path)) == item["sha256"] == current.native.digest(active.read_file(path))
    sink = legacy_sink(clean, active)
    online = prior.exact_online_dependencies(clean, active)
    openings = {r["message_ID"]: r["artwork_association"] for r in opening["records"]}

    chooser = base.load(CHOOSER)
    chooser_controls = []
    for index, r in enumerate(chooser["records"]):
        assert all(r["review"].values()) and r["chooser_index"] == index
        ref = r["registered_reference"]
        field = ref["pointer_field"] - BASE
        assert unpack("<I", en[field:field+4]) == (ref["runtime_address"],)
        start, length = ref["ARM9_offset"], ref["byte_count"]
        assert en[start:start+length].hex() == ref["exact_hex"]
        chooser_controls.append(biography_selector(en, runtime.raw, r))
    chooser_ids = dict(zip(range(104, 108), chooser["records"], strict=True))
    for r in rows:
        number = r["message_ID"]
        gallery = gallery_sources.get(r["source_hex"], []) if number in scene_rows else []
        r["independent_gallery_draw_sources"] = gallery
        if number in art:
            r["story_still_filename"] = art[number]["path"]
        if number in openings:
            r["observed_title_and_route_intros_use_separate_assets"] = True
            r["opening_artwork_association"] = openings[number]
        if 3289 <= number <= 3319:
            r["tested_Online_and_About_Extras_use_separate_ARM9_text"] = True
        if number in chooser_ids:
            r["separate_chooser_biography_review"] = chooser_ids[number]["id"]
        if number == 111:
            r["known_load_behavior"] = sink["classification_111"]
        r["other_COMMON_display_paths"] = "unverified"

    matches = sum(bool(r["independent_gallery_draw_sources"]) for r in rows)
    assert matches == 123 and len(art) == 168 and len(openings) == 37
    proofs = [BINDINGS, GALLERY, CHOOSER, SCENES, ROUTING, OPENINGS, CONTINUE,
              prior.ONLINE, current.RELEASE, Path(__file__)]
    base.save(OUTPUT, dict(candidate_sha256=release["candidate_sha256"], clean_sha256=release["clean_input_sha256"],
        records=rows, exact_clean_and_current_gallery_draw_inputs=328, exact_Gallery_duplicate_labels=matches,
        native_story_still_filename_cases=336, exact_still_assets=len(art), independent_Online_and_Extras=online,
        current_chooser_biography_selections=chooser_controls,
        legacy_save_diagnostic_sink=sink, prior_gameplay_reused=True, new_gameplay_runs=0, hardware=False,
        pending_display_keys=len(rows), new_editorial_credit=0, full_goal_complete=False,
        evidence={str(p): base.digest(p) for p in proofs}))
    print("Verified 328 Gallery draw inputs, 336 story still filenames, and all 8 legacy diagnostic sink calls.")


if __name__ == "__main__":
    main()
