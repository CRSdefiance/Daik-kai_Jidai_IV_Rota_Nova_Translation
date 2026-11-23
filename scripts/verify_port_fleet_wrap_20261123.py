"""Compare the Gerhard veto and fleet picker transitions across both emulator runs."""

from types import FunctionType

from scripts import replay_port_fleet_refusals_20261123 as replay
from scripts import stage_port_fleet_wrap_20261123 as stage
from scripts import verify_square_and_market_reward_wraps_20261123 as comparison


base = stage.base
LIVE = stage.ROOT / "focused_dialogue.json"


def read_run(case, sha, evidence):
    folder = replay.ROOT / case
    terminal_path = folder / "terminal.json"
    report_path = folder / "capture/capture_report.json"
    input_path = folder / "inputs.json"
    terminal, report = map(base.load, (terminal_path, report_path))
    assert terminal["rom_sha256"] == report["ROM_sha256"] == sha
    assert terminal["report_sha256"] == base.digest(report_path)
    assert terminal["inputs_sha256"] == base.digest(input_path)
    assert terminal["history_sha256"] == base.digest(replay.HISTORY)
    assert terminal["focused_fixture"] and not terminal["earned_regional_fleet"]
    assert report["cold_boot"] and not report["savestate_loaded"] and not report["callback_errors"]
    assert report["battery_save_preloaded"]["source_sha256"] == terminal["donor_sha256"] == replay.SAVED_GAME_SHA
    for path in (terminal_path, report_path, input_path):
        evidence[str(path)] = base.digest(path)
    return report, comparison.market.shots(report)


def main():
    assert not LIVE.exists()
    stored, previous = map(base.load, (stage.PROOF, stage.parent.RELEASE))
    assert base.digest(stage.ROM) == stored["candidate_sha256"]
    assert base.digest(stage.parent.ROM) == previous["candidate_sha256"] == stored["predecessor_sha256"]
    evidence = {str(stage.PROOF): base.digest(stage.PROOF)}
    old, a = read_run("current", previous["candidate_sha256"], evidence)
    new, b = read_run("revised", stored["candidate_sha256"], evidence)
    for key in ("frames", "scripted_input_schedule", "core_DLL_sha256", "core_options"):
        assert old[key] == new[key], key
    fixture_ram_hashes = {"before_RAM_sha256", "after_RAM_sha256"}
    for key in ("synthetic_finance_fixtures", "synthetic_crew_ability_fixtures"):
        old_fixture, = old[key]
        new_fixture, = new[key]
        assert ({name: value for name, value in old_fixture.items() if name not in fixture_ram_hashes}
                == {name: value for name, value in new_fixture.items() if name not in fixture_ram_hashes}), key

    ctx = stage.town.RegisteredRuntime(stage.parent.RELEASE, previous["own_registered_startup"], captain=3)
    cpu, _, _ = ctx.machine(ctx.arm, ctx.common, ctx.raw, ctx.plan)
    rom = base.NdsImage.open(stage.ROM)
    arm, kanji = (rom.read_file(path) for path in (stage.ARM, "/GRP/KANJI.FNT"))
    assert arm == ctx.arm
    raster, _, _ = stage.town.font_tools(rom)
    row, = [row for row in stored["records"] if row["message_ID"] == 809]
    old_display, _ = stage.display(ctx, bytes.fromhex(row["current_hex"]), 809, cpu)
    new_display = bytes.fromhex(row["display_hex"])
    old_plane, new_plane = (stage.town.render_portrait(raster, arm, kanji, body)[0]
                            for body in (old_display, new_display))
    assert stage.native.digest(new_plane) == row["native_plane_sha256"]
    scope = vars(comparison) | {"stage": stage}
    hold = FunctionType(comparison.display_hold.__code__, scope)
    render = FunctionType(comparison.render_sheet.__code__, scope)
    verified, pictures = hold(809, 17000, a[17000], b[17000], old_plane, new_plane, evidence)
    holds = [("Gerhard's refusal", pictures)]
    transitions = [16200, 16600, 17400]
    for frame, name in zip(transitions, ("Choose a fleet admiral", "Gerhard in the picker",
                                         "Fleet admiral prompt after dismissal"), strict=True):
        assert a[frame]["PNG_sha256"] == b[frame]["PNG_sha256"]
        for shot in (a[frame], b[frame]):
            evidence[shot["path"]] = shot["PNG_sha256"]
        if frame != 16600:
            holds.append((name, tuple(map(comparison.market.captured, (a[frame], b[frame])))))
    sheets = render("port_fleet", holds)
    base.save(LIVE, dict(candidate_sha256=stored["candidate_sha256"], predecessor_sha256=stored["predecessor_sha256"],
        observed={"port_fleet": [verified]}, revised_holds=1, retained_holds=0, menu_transitions=len(transitions),
        revised_offline_only_records=[805], focused_fixtures=True, ordinary_gameplay=False,
        menu_transition_frames=transitions, hardware=False, evidence=evidence, sheets=sheets))
    print("Verified the complete Gerhard panel and three unchanged picker transitions.")


if __name__ == "__main__":
    main()
