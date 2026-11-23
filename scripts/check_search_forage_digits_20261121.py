"""Check the distinct water and food amounts in the extended Search replay."""

from pathlib import Path

from PIL import Image, ImageChops, ImageDraw

from scripts import replay_search_supply_and_fatigue_digits_20261121 as replay
from scripts.verify_crew_and_shore_reports_v1 import fleet_state


stage, base, shared = replay.stage, replay.base, replay.shared
ROOT = stage.ROOT
PROOF, SHEET = ROOT / "verified_forage.json", ROOT / "search_forage_live.png"
HOLD, RETURN, EXPECTED_ID = 11198, 11378, 2229
QUANTITIES = (175, 140)


def main():
    dirs = [ROOT / f"{v}_extra" / "capture" for v in ("before", "after")]
    reports = [directory / "capture_report.json" for directory in dirs]
    before, after = capture = list(map(base.load, reports))
    proof = base.load(stage.PROOF)
    assert [r["ROM_sha256"] for r in capture] == [proof["parent_sha256"], proof["candidate_sha256"]]
    assert all(r["cold_boot"] and not r["savestate_loaded"] and not r["callback_errors"] for r in capture)
    for key in ("frames", "core_options", "core_DLL_sha256", "scripted_input_schedule"):
        assert before[key] == after[key]
    for key in ("source_sha256", "copied_byte_exact_before_cold_boot"):
        assert before["battery_save_preloaded"][key] == after["battery_save_preloaded"][key]
    commands = [folder / "navigation_command_journal.json" for folder in dirs]
    assert base.load(commands[0])["commands_received"] == base.load(commands[1])["commands_received"]
    fixture_key = "synthetic_battle_recovery_proximity_fixtures"
    pairs = [(r["frame"], r["owned_bytes"], r["changes"]) for r in before[fixture_key]]
    assert pairs == [(r["frame"], r["owned_bytes"], r["changes"]) for r in after[fixture_key]]
    assert len(pairs) == 8 and all(len(owned) == 48 for _, owned, _ in pairs)
    frames = [{r["frame"]: r for r in report["frames_captured"] if r["path"].endswith("_navigation.png")}
              for report in capture]
    assert frames[0][RETURN]["framebuffer_sha256"] == frames[1][RETURN]["framebuffer_sha256"]

    previous = base.load(stage.parent.RELEASE)
    ctx = stage.common.RegisteredRuntime(stage.parent.RELEASE, previous["own_registered_startup"], captain=3)
    image = base.NdsImage.open(stage.ROM)
    arm = image.read_file(shared.ARM)
    revised = stage.common.discovery.with_components(ctx, arm, ctx.common)
    row = shared.entries(ctx.image)[EXPECTED_ID]
    group = dict(consumer=0x02053D44, table=stage.TABLE, original_role_argument=stage.ROLE)
    native = stage.with_arguments()
    outputs = []
    palette_ink = (0, 8, 0)
    kanji = image.read_file("/GRP/KANJI.FNT")
    for context, f, encoding in zip((ctx, revised), frames, ("cp932", "ascii"), strict=True):
        args = tuple(str(value).encode("ascii") for value in QUANTITIES)
        if encoding == "cp932":
            args = tuple("".join(chr(0xFF10 + int(c)) for c in str(value)).encode("cp932") for value in QUANTITIES)
        result = native(context, {"message_ID": EXPECTED_ID}, group, row.text, 18, args)
        text = result["display"]
        raster, _, _ = stage.common.discovery.mixed.font_tools(context.image)
        plane, glyphs = stage.render_portrait(raster, context.arm, kanji, text)
        assert glyphs[0]["code"] == ord("T") and glyphs[-1]["code"] == ord(".")
        hold = f[HOLD]
        assert base.digest(hold["path"]) == hold["PNG_sha256"]
        panel = Image.open(hold["path"]).convert("RGB")
        reference = bytes(p == 1 for p in plane)
        # The original portrait painter anchors the English font at this box
        # and offsets wide glyph shadows within the same canvas.
        assert bytes(c == palette_ink for c in panel.crop((16, 296, 244, 360)).get_flattened_data()) == reference, encoding
        outputs.append((panel, text))
    delta = ImageChops.difference(outputs[0][0], outputs[1][0]).getbbox()
    assert delta and 16 <= delta[0] < delta[2] <= 244 and 296 <= delta[1] < delta[3] <= 361
    states = []
    for context, result in zip((ctx, revised), capture, strict=True):
        snapshot = result["read_only_RAM_snapshot"]
        assert snapshot["read_only_export"] and base.digest(snapshot["path"]) == snapshot["sha256"]
        states.append(fleet_state(context.arm, Path(snapshot["path"]).read_bytes()))
    assert states[0] == states[1] and states[0]["original_mode"] == [0, 0, 0]
    sheet = Image.new("RGB", (1024, 338), "#263238")
    labels = ImageDraw.Draw(sheet)
    for i, (panel, _) in enumerate(outputs):
        left = i * 512
        labels.text((left + 6, 6), ("Original wide digits", "Regular English digits")[i], fill="white")
        sheet.paste(panel.crop((0, 226, 256, 384)).resize((512, 316), Image.Resampling.NEAREST), (left, 22))
    sheet.save(SHEET)
    base.save(PROOF, dict(candidate_sha256=proof["candidate_sha256"], parent_sha256=proof["parent_sha256"],
        message_ID=EXPECTED_ID, speaker="Charles Rochefort", original_voice_actor=18, held_frame=HOLD,
        source_water_and_food=list(QUANTITIES), rows=[b.decode("ascii").strip() for b in outputs[1][1].splitlines()],
        same_original_commands=True, captured_return_frame=RETURN, final_fleet_state=states[1],
        full_foreground_glyph_masks=True, hardware_verified=False, sheet=dict(path=str(SHEET), sha256=base.digest(SHEET)),
        changed_rectangle=delta, evidence={str(p): base.digest(p) for p in (*reports, *commands)}))
    print("The original foraging replay shows 175 barrels of water and 140 of food in regular English digits.")


if __name__ == "__main__":
    main()
