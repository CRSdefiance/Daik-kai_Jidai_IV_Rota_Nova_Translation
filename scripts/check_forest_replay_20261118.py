"""Match both initialized forest menus and their controller transitions to native pixels."""

from PIL import Image, ImageDraw

from scripts import replay_forest_expeditions_20261118 as replay
from scripts import verify_forest_expeditions_20261118 as display
from scripts.analyze_maria301_display_v1 import verified_existing_unlock
from scripts.check_hodram_B91_B110_actual_pixels import mask, match


stage, base, native = replay.stage, replay.base, replay.native
OUTPUT = replay.ROOT / "verified.json"


def selected_option(image, proof, expected):
    versions = proof.get("versions") or proof["menus"][0]["versions"]
    vm = versions[-1]["cases"][0]["native_VM"]
    width = vm["minimum_width_units"] * 6
    left, top, _, _ = vm["native_menu_rectangle"]
    x = left + 16
    for index, label in enumerate(vm["labels"]):
        plane = next(p for p in proof["records"]
                     if p["version"] == "reviewed-English" and p["option"] == index and p["style"] == 1)
        ink = mask(plane["path"], plane["sha256"], width)
        y = 192 + top + 16 + 20 * index
        assert match(image, ink, (8, 8, 8), [x], [y]) == [x, y]
        blank = {(xx, yy) for yy in range(y - 4, y + 16) for xx in range(x, x + width)}
        blank -= {(x + xx, y + yy) for xx, yy in ink}
        highlight = {point for point in blank if image.getpixel(point) == (0, 165, 172)}
        if index == expected:
            assert highlight, (label, index, expected)
            lo, hi = min(p[1] for p in highlight), max(p[1] for p in highlight)
            assert highlight == {p for p in blank if lo <= p[1] <= hi}
        else:
            assert not highlight, (label, index, expected)
        assert all(image.getpixel(p) == (205, 198, 180) for p in blank - highlight)
    return vm["labels"][expected]


def assets(image):
    return [image.read_file(p) for p in (native.ARM, "/COMMON/MESFILE.DK4", "/GRP/KANJI.FNT")]


def check_capture(case, root, approved, menu_inputs, speech_inputs):
    fixture_path = root / "fixture.json"
    report_path = root / case / "capture/capture_report.json"
    report, fixture = base.load(report_path), base.load(fixture_path)
    assert base.digest(report["ROM"]) == report["ROM_sha256"] == fixture["fixture_sha256"]
    assert fixture["original_scene_commands_exact"] and fixture["whole_source_ROM_inverse"]
    assert report["cold_boot"] and not report["savestate_loaded"] and not report["callback_errors"]
    assert verified_existing_unlock(report)
    proof_path = root.parent / stage.PROOF.name
    stage_proof = base.load(proof_path)
    assert stage_proof["candidate_sha256"] == fixture["reference_ROM_sha256"]
    assert stage_proof["preserved_ARM9_sha256"] == approved["preserved_ARM9_sha256"]
    group = stage_proof["groups"][3]
    final = approved["groups"][3]
    assert group["after"] == fixture["forest_sha256"]
    assert len(group["commands"]) == len(final["commands"])
    for before, now in zip(group["commands"], final["commands"], strict=True):
        assert before["source_offset"] == now["source_offset"]
        assert before["word"] == now["word"]
        assert before.get("target_command_index") == now.get("target_command_index")
        if before["word"] in stage.MENU:
            assert before["stored"] == now["stored"]
    image = base.NdsImage.open(report["ROM"])
    assert assets(image) == assets(base.NdsImage.open(stage.ROM))
    menu_proofs = base.load(display.OUTPUT / "native_display.json")["menus"]
    receipts = {}
    for cmd in final["commands"]:
        if cmd["word"] in stage.MENU:
            receipt = next(m for m in menu_proofs if m["option_ids"] == cmd["record_ids"])
            assert base.digest(receipt["menu_path"]) == receipt["proof_sha256"]
            receipts[cmd["source_offset"]] = base.load(receipt["menu_path"])
    frames = {row["frame"]: row for row in report["frames_captured"]}

    def read_frame(n):
        meta = frames[n]
        assert base.digest(meta["path"]) == meta["PNG_sha256"]
        return meta, Image.open(meta["path"]).convert("RGB")

    displays, pictures = [], []
    for frame, offset, index in menu_inputs:
        meta, captured = read_frame(frame)
        label = selected_option(captured, receipts[offset], index)
        displays.append(dict(frame=frame, source_command_offset=offset, index=index, label=label, capture=meta))
        pictures.append((f"{label}  [{frame}]", captured))
    _, paint = display.early.prior.precedent.planners(assets(image)[0])
    fe_ctx = native.RegisteredRuntime(stage.parent.RELEASE,
        base.load(stage.parent.RELEASE)["own_registered_startup"], captain=3)
    paint_fe = stage.system.native_painter(fe_ctx)
    holds = []
    for frame, offset, row_id, printed in speech_inputs:
        here, there = (next(c for c in bank["commands"] if c["source_offset"] == offset)
                       for bank in (group, final))
        assert row_id in here["record_ids"] and row_id in there["record_ids"]
        index = here["record_ids"].index(row_id)
        current, target = [bytes.fromhex(cmd["stored"]) for cmd in (here, there)]
        assert here["word"] in (stage.SPEECH, stage.STYLE)
        if here["word"] == stage.STYLE:
            text, final_text = (list(unpack_bytes(raw).values())[index] for raw in (current, target))
            selector = target[19]
        else:
            text, final_text = (raw[6:raw.index(0, 6)] for raw in (current, target))
            selector = target[5]
        assert text == final_text and " ".join(text.decode("ascii").split()) == printed
        arm, _, font = assets(image)
        if selector == 254:
            plane = paint_fe(text)["physical"]
            width = 228
        else:
            result = paint(arm, font, text)
            only, = result["pages"]
            plane, width = bytes.fromhex(only["native_plane_hex"]), 216
        ink = {(i % width, i // width) for i, pixel in enumerate(plane) if pixel and i % width < 216}
        meta, captured = read_frame(frame)
        origin = match(captured, ink, (0, 8, 0), range(12, 24), range(294, 310))
        holds.append(dict(frame=frame, source_command_offset=offset, id=row_id, text=printed,
                          origin=origin, capture=meta, complete_native_ink=True, FE=selector == 254))
        pictures.append((f"{row_id}  [{frame}]", captured))
    order = report["scripted_input_schedule"]
    if case in ("other_run", "other_scare"):
        assert [r["start"] for r in order if r["buttons"] == ["A"] and 6275 < r["start"] < 6325] == [6300]
        assert [r["start"] for r in order if r["buttons"] == ["A"] and 6525 < r["start"] < speech_inputs[0][0]] == [6600]
    sheet = Image.new("RGB", (888, ((len(pictures) + 1) // 2) * 206), "#263238")
    draw = ImageDraw.Draw(sheet)
    for i, (title, captured) in enumerate(pictures):
        x, y = i % 2 * 444, i // 2 * 206
        draw.text((x + 4, y + 2), title, fill="white")
        sheet.paste(captured.crop((0, 192, 256, 384)), (x + 4, y + 14))
    path = replay.ROOT / f"live_{case}.png"
    sheet.save(path)
    return dict(case=case, menu_displays=displays, body_holds=holds,
                exact_final_candidate_fixture=stage_proof["candidate_sha256"] == approved["candidate_sha256"],
                fixture=str(fixture_path), fixture_sha256=base.digest(fixture_path),
                report=str(report_path), report_sha256=base.digest(report_path),
                review_sheet=dict(path=str(path), sha256=base.digest(path)))


def unpack_bytes(raw):
    offsets, bodies = display.unpack(raw)
    return {offset: bodies[offset] for offset in sorted(set(offsets))}


def main():
    assert not OUTPUT.exists()
    final = base.load(stage.PROOF)
    preliminary = replay.ROOT.parent.with_name("research_v1") / replay.ROOT.name
    discovery = ((6150, 882, 0),)
    others = ((6075, 882, 0), (6175, 882, 1), (6275, 882, 2), (6325, 1876, 0))
    fight = ((7200, 1124, "DK4_MES_B252_R0147", "Some sailors seem to have suffered minor injuries."),)
    run = ((6775, 3014, "DK4_MES_B252_R0312", "Run!!"),
           (7125, 3046, "SC3_B252_STYLE_3046_120", "Whew... Did we lose it?"))
    scare = ((6775, 1924, "SC3_B252_STYLE_1924_136", "This bear's got guts. It won't run!"),
             (7125, 2398, "SC3_B252_STYLE_2398_314", "Look out! Damn, did some of us get hurt? We'd better run!"),
             (7475, 2936, "DK4_MES_B252_R0304", "The sailors are much more fatigued. Some appear to be injured."),
             (7825, 3046, "SC3_B252_STYLE_3046_120", "Whew... Did we lose it?"),
             (8175, 3306, "SC3_B252_STYLE_3306_186", "Hey, Admiral! We're out of the woods! Yep, those are the ruins!"))
    scenes = [
        check_capture("discovery", preliminary, final, discovery, fight),
        check_capture("other_run", preliminary, final, (*others, (6525, 1876, 1)), run),
        check_capture("other_scare", replay.ROOT, final, (*others, (6525, 1876, 0)), scare),
    ]
    base.save(OUTPUT, dict(candidate_sha256=final["candidate_sha256"], cases=scenes,
        initialized_emulator=True, natural_activation=False, hardware=False,
        source_controls_rebased_by_native_command_boundary=True, no_guide_photos=True))


if __name__ == "__main__":
    main()
