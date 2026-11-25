"""Verify the Cabin warning, Square confirmation and both dismissal paths."""

from inspect import getsource
from types import FunctionType

from dk4tool.dialogue.font_audit import GameAsciiFont
from scripts import replay_cabin_warning_wrap_20261123 as cabin
from scripts import stage_cabin_square_wrap_20261123 as stage
from scripts import verify_square_and_market_reward_wraps_20261123 as earlier
from scripts.record_navigation_v327 import dark_text
from scripts.source_locked_derivation_v5118 import checked_text


base = stage.base
LIVE = stage.ROOT / "focused_dialogue.json"


def cabin_holds(stored, displays, evidence, scope, font):
    runs = []
    for side, sha in (("old", stored["predecessor_sha256"]), ("new", stored["candidate_sha256"])):
        folder = stage.ROOT / f"{side}_cabin"
        terminal = folder / "terminal.json"
        report_file = folder / "capture/capture_report.json"
        t, report = map(base.load, (terminal, report_file))
        assert t["candidate_sha256"] == report["ROM_sha256"] == sha
        assert t["only_fixture_fields_restored"] and not t["natural_activation"]
        assert t["report_sha256"] == base.digest(report_file)
        donor = report["battery_save_preloaded"]
        assert donor["copied_byte_exact_before_cold_boot"]
        assert base.digest(donor["source"]) == t["donor_sha256"] == donor["source_sha256"] == cabin.DONOR
        assert report["cold_boot"] and not report["savestate_loaded"] and not report["callback_errors"]
        fixtures = report["synthetic_condition_fixtures"]
        assert [row["frame"] for row in fixtures] == [7200, 7500]
        assert [row["source_selected_warning"] for row in fixtures] == [649, 646]
        assert all(row["original_compiled_code_unmodified"] and len(row["changes"]) == 2 for row in fixtures)
        evidence.update({str(path): base.digest(path) for path in (terminal, report_file, folder / "inputs.json")})
        runs.append((report, earlier.market.shots(report)))
    (older_report, older), (newer_report, newer) = runs
    for key in ("core_DLL_sha256", "core_options", "scripted_input_schedule", "synthetic_condition_fixtures"):
        assert older_report[key] == newer_report[key]
    _, _, old_plane, new_plane = displays[649]
    verified, photos = scope["display_hold"](649, 7500, older[7500], newer[7500], old_plane, new_plane, evidence)
    panels = [("Captain's Cabin warning", photos)]
    for frame in (7200, 7800):
        assert older[frame]["PNG_sha256"] == newer[frame]["PNG_sha256"]
        for shot in (older[frame], newer[frame]):
            evidence[shot["path"]] = shot["PNG_sha256"]
    before, after = map(earlier.market.captured, (older[7200], older[7800]))
    assert before.crop((0, 0, 256, 192)).tobytes() == after.crop((0, 0, 256, 192)).tobytes()
    verified["confirmation_caption_masks"] = [
        dark_text(font, "Auto Move", screen, (88, 270, 170, 308)) for screen in (before, after)]
    panels.append(("Auto Move confirmation after dismissal",
        tuple(map(earlier.market.captured, (older[7800], newer[7800])))))
    return [verified], [7800], scope["render_sheet"]("captains_cabin", panels)


def main():
    assert not LIVE.exists()
    stored, previous = map(base.load, (stage.PROOF, stage.parent.RELEASE))
    assert base.digest(stage.ROM) == stored["candidate_sha256"]
    assert base.digest(stage.parent.ROM) == previous["candidate_sha256"] == stored["predecessor_sha256"]
    ctx = stage.town.RegisteredRuntime(stage.parent.RELEASE, previous["own_registered_startup"], captain=3)
    cpu, _, _ = ctx.machine(ctx.arm, ctx.common, ctx.raw, ctx.plan)
    rom = base.NdsImage.open(stage.ROM)
    arm, kanji = (rom.read_file(path) for path in (stage.ARM, "/GRP/KANJI.FNT"))
    assert arm == ctx.arm
    raster, _, _ = stage.town.font_tools(rom)
    group, = [row for row in stored["auto_move_owners"] if row["first_ID"] <= 649 <= row["last_ID"]]
    displays = {}
    for row in stored["records"]:
        key = row["message_ID"]
        if key not in {649, 664, 672, 674}:
            continue
        old, _, _ = stage.display(ctx, key, bytes.fromhex(row["current_hex"]), group, cpu)
        new = bytes.fromhex(row["display_hex"])
        old_plane, new_plane = (stage.town.render_portrait(raster, arm, kanji, body)[0] for body in (old, new))
        assert stage.native.digest(new_plane) == row["native_plane_sha256"]
        displays[key] = (old.hex(), new.hex(), old_plane, new_plane)
    scope = vars(earlier) | {"stage": stage}
    for name in ("display_hold", "render_sheet"):
        scope[name] = FunctionType(scope[name].__code__, scope)
    code = checked_text(getsource(earlier.square_holds), {
        'fixture["supplied_voice_style"] == 5': 'fixture["supplied_voice_style"] == 6',
        'fixture["original_confirmation"] == 663 and fixture["original_announcement"] == 671':
            'fixture["original_confirmation"] == 664 and fixture["original_announcement"] == 672',
        '((4800, 663), (5200, 663), (6800, 671), (7200, 674))':
            '((4800, 664), (5200, 664), (6800, 672), (7200, 674))',
        'render_sheet("square_sample", panels)': 'render_sheet("square_confirmation", panels)',
    })
    exec(compile(code, __file__ + "::sample_confirmation", "exec"), scope)
    evidence = {str(stage.PROOF): base.digest(stage.PROOF)}
    square, square_return, square_sheet = scope["square_holds"](stored, displays, evidence, arm)
    warning, cabin_return, cabin_sheet = cabin_holds(stored, displays, evidence, scope, GameAsciiFont.from_arm9(arm))
    base.save(LIVE, dict(candidate_sha256=stored["candidate_sha256"], predecessor_sha256=stored["predecessor_sha256"],
        observed=dict(cabin=warning, square=square), revised_holds=3, retained_holds=2, menu_transitions=2,
        revised_offline_only_records=[], ordinary_gameplay=False, focused_fixtures=True, hardware=False,
        returns=dict(cabin=cabin_return, square=square_return), evidence=evidence, sheets=cabin_sheet | square_sheet))
    print("Verified three revised holds, two retained holds and both original return screens.")


if __name__ == "__main__":
    main()
