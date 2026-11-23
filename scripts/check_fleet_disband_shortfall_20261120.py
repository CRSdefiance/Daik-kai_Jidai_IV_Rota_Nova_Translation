"""Bind the live fleet shortfall branch to modal glyphs and the original wallet state."""

from pathlib import Path
from struct import unpack_from

from PIL import Image, ImageDraw

from dk4tool.dialogue.font_audit import GameAsciiFont
from scripts import checkpoint_fleet_debt_disband_20261115 as prior
from scripts import checkpoint_shared_display_worklist_20261120 as worklist
from scripts import register_market_bargaining_20261120 as current
from scripts import replay_fleet_disband_shortfall_20261120 as replay
from scripts.checkpoint_market_shared_consumers_20261114 import font_mask
from scripts.verify_captain_biographies_v1 import captured, shots
from scripts.verify_personal_gameplay_v841 import get_machine


base = current.base
OUTPUT = worklist.BOOK / "fleet_disband_shortfall_20261120_v1.json"
SHEET = replay.ROOT / "disband_shortfall_comparison.png"
STATES = (10000, 10840, 11080, 11560, 11680, 11800)
DIALOGUE = (
    (281, 10360, "Choose a fleet to disband."),
    (285, 10840, "Disband this fleet?"),
    (285, 11560, "Disband this fleet?"),
    (286, 11680, "We'll put all the ships in the dock."),
)


def wallet_states(report, arm, evidence):
    snapshots = {r["frame"]: r for r in report["read_only_capture_RAM_snapshots"]}
    result = []
    for frame in STATES:
        shot = snapshots[frame]
        path = Path(shot["path"])
        assert shot["read_only_export"] and base.digest(path) == shot["sha256"]
        evidence[str(path)] = shot["sha256"]
        raw = path.read_bytes()
        _, field = prior.setup(raw, arm, replay.FLEET_ID)
        _, get = get_machine(arm, raw)
        fleet = field["fleet"]
        ships = [get(0x36C94, fleet + 0xC + 8 * i) for i in range(5)]
        result.append(dict(frame=frame, company_gold=prior.field(raw, field["wallet"]),
            fleet_active=get(0x36914, fleet), occupied_slots=sum(bool(obj) for obj in ships),
            expenses_income_invested=unpack_from("<3I", raw, field["finance"] + 0xC - replay.BASE)))
    return result


def exact_hold(board, font, text, frame):
    for x in (16, 22):
        try:
            return font_mask(board, font, text, x, 297, prior.BODY, (0, 8, 0))
        except AssertionError:
            continue
    raise AssertionError(f"Complete original mask did not match frame {frame}")


def main():
    assert not OUTPUT.exists() and not SHEET.exists()
    release = base.load(current.RELEASE)
    assert base.digest(current.ROM) == release["candidate_sha256"]
    arm = base.NdsImage.open(current.ROM).read_file(prior.ARM)
    paths = [replay.ROOT / side / "capture/capture_report.json" for side in ("control", "shortfall_isolated")]
    recipe_path = paths[-1].parent.parent / "scoped_runtime_inputs.json"
    inputs, _, terminal, _, donor = prior.playback.schedule("fleet")
    receipt = base.load(recipe_path)
    evidence = {str(path): base.digest(path) for path in (*paths, recipe_path, prior.PROOF, worklist.OUTPUT)}
    reports = [base.load(path) for path in paths]
    for report in reports:
        assert report["ROM_sha256"] == release["candidate_sha256"] and report["frames"] == terminal
        assert report["cold_boot"] and not report["savestate_loaded"] and not report["callback_errors"]
        assert report["scripted_input_schedule"] == inputs
        assert report["battery_save_preloaded"]["copied_byte_exact_before_cold_boot"]
        assert report["battery_save_preloaded"]["source_sha256"] == donor["source_sha256"] == base.digest(donor["source"])
    assert reports[0]["core_DLL_sha256"] == reports[1]["core_DLL_sha256"]
    assert reports[0]["core_options"] == reports[1]["core_options"]
    assert not any(v for k, v in reports[0].items() if k.startswith("synthetic_"))
    assert all(k == "synthetic_condition_fixtures" for k, v in reports[1].items() if k.startswith("synthetic_") and v)
    assert reports[1]["synthetic_condition_fixtures"] == [receipt["receipt"] | {"frame": replay.INIT_FRAME}]

    full_control, shortfall = [wallet_states(report, arm, evidence) for report in reports]
    assert [r["company_gold"] for r in full_control] == [897_400] * 5 + [997_400]
    assert [r["company_gold"] for r in shortfall] == [897_400] + [replay.WALLET] * 4 + [0]
    for states, expenses in ((full_control, 0), (shortfall, replay.EXPENSES)):
        assert [r["fleet_active"] for r in states] == [1] * 5 + [0]
        assert [r["occupied_slots"] for r in states] == [1] * 5 + [0]
        assert all(r["expenses_income_invested"] == (expenses, 0, 0) for r in states[1:])

    font = GameAsciiFont.from_arm9(arm)
    plane = Image.new("RGB", (1040, 458), "#273034")
    labels = ImageDraw.Draw(plane)
    masks = []
    for side, report in enumerate(reports):
        by_frame = shots(report)
        for i, (message_id, frame, text) in enumerate(DIALOGUE):
            shot = by_frame[frame]
            evidence[shot["path"]] = shot["PNG_sha256"]
            screen = captured(shot)
            masks.append(dict(run=("control", "shortfall")[side], frame=frame, complete_rendered_text=text,
                expected_original_message_ID=message_id, complete_ink_pixels=exact_hold(screen, font, text, frame)))
            x, y = 520 * (i % 2), 114 * (side * 2 + i // 2)
            labels.text((x + 4, y + 3), f"{('Control', 'Shortfall')[side]} | {frame}", fill="white")
            plane.paste(screen.crop((0, 292, 256, 384)).resize((512, 92), Image.Resampling.NEAREST), (x + 4, y + 16))
    plane.save(SHEET)

    previous = base.load(prior.PROOF)
    current_record, = [r for r in base.load(worklist.OUTPUT)["records"] if r["message_ID"] == 284]
    assert current_record["source_reference"] == previous["debt_warning"]["source_reference"]
    assert bytes.fromhex(current_record["current_hex"]).decode("cp932") == previous["debt_warning"]["current"]
    base.save(OUTPUT, dict(candidate_sha256=release["candidate_sha256"], current_shared_reference=current_record,
        original_native_arithmetic_proof=str(prior.PROOF), unchanged_original_code_ranges=replay.DEPENDENCIES,
        prior_gameplay_and_native_evidence_reused=True, new_gameplay_runs=2, panel_checks=masks,
        control_state=full_control, shortfall_state=shortfall, supplied_shortfall=receipt["receipt"],
        unexpected_debt_warning_seen_in_held_panels=False, new_live_COMMON_lookup_trace=False,
        remaining_other_display_paths_open=True, hardware=False, new_dialogue_credit=0,
        sheet=dict(path=str(SHEET), sha256=base.digest(SHEET)), evidence=evidence))
    print("Eight complete panel masks passed. Cancel kept 37 gold and one ship; accepting reduced gold to zero and disbanded the fleet.")


if __name__ == "__main__":
    main()
