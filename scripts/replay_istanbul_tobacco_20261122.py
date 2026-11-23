"""Replay Istanbul normally on Hodram and with the complete scene initialized on Lil."""

from argparse import ArgumentParser
from inspect import getsource
from pathlib import Path
from types import SimpleNamespace

from scripts import replay_seville_stockholm_trends_20261121 as lil
from scripts import stage_istanbul_tobacco_20261122 as stage
from scripts import stage_osaka_glass_20261122 as previous
from scripts import verify_seville_square_gameplay_20261121 as ordinary
from scripts.source_locked_derivation_v5118 import checked_text


base, native, parent = stage.base, stage.native, stage.parent
ROOT = stage.ROOT / "focused"
CASES = {2: (192, 22, 2600, 240)}
SPEAKERS = {k: v for k, v in stage.SPEAKERS.items() if k != 254}
PROOF, ROM, LIVE = stage.PROOF, stage.ROM, ROOT / "focused_gameplay.json"
review = SimpleNamespace(REVIEW=stage.MANUSCRIPT)
NORMAL = stage.VOYAGE / "verified_ordinary_square.json"
EXCHANGE = ordinary.Exchange(1, stage.TOWN, 196, 8, stage.PRIOR, SPEAKERS)
PROGRAM = checked_text(getsource(previous.capture), {
    'assert len(speeches) == 11': 'assert len(speeches) == 8',
    'assert [c["word"] for c in commands if c["word"] != 0x4000] == [0xA000, 0xC200, 0]':
        'assert [c["word"] for c in commands if c["word"] != 0x4000] == [0xA000, 0xC200, 0]',
    '    if route == 1:': '''    if route == 2:
        fixtures = Path("work/analysis/square_shopkeeper_scenes_v7022/four_complete_static_staged_nameplate_fixtures.json")
        original_fixture = next(row for row in base.load(fixtures)["fixtures"] if row["case"] == "static_target")
        prelude = bytes.fromhex(original_fixture["original_B22_prelude_hex"])
        initial = base.load(lil.precedent.prior.INPUTS)
    elif route == 1:''',
    'f"Osaka_Route{route}_FOCUSED_ONLY.nds"': '"Istanbul_Lil_FOCUSED_ONLY.nds"',
    'ordinary_Osaka_trigger=False': 'ordinary_Istanbul_trigger=False',
    '    folder.mkdir()': '    folder.mkdir(parents=True)',
    'first + i*interval + 220': 'first + i*interval + 190',
})
VERIFIER = checked_text(getsource(previous.verify), {
    "natural_Osaka_trigger=False": "natural_Istanbul_trigger=False",
})


def run_lil(action):
    scope = vars(previous) | globals()
    source = PROGRAM if action == "capture" else VERIFIER
    exec(compile(source, __file__ + "::native-Istanbul-scene", "exec"), scope)
    if action == "capture":
        scope["capture"](2)
    else:
        scope["verify"]()


def verify_ordinary():
    assert not NORMAL.exists()
    folder = stage.VOYAGE
    report_path = folder / "capture/capture_report.json"
    input_path = folder / "source_save.json"
    journal_path = folder / "capture/navigation_command_journal.json"
    report, launch, entered = map(base.load, (report_path, input_path, journal_path))
    assert report["ROM_sha256"] == launch["working_ROM_sha256"] == base.digest(parent.ROM)
    assert report["cold_boot"] and not report["savestate_loaded"] and not report["callback_errors"]
    assert not any(v for k, v in report.items() if k.startswith("synthetic_"))
    assert all(row["validation_passed"] for row in entered["commands_received"])
    donor = report["battery_save_preloaded"]
    assert donor["copied_byte_exact_before_cold_boot"] and donor["source"] == launch["donor"]
    assert base.digest(donor["source"]) == launch["sha256"] == donor["source_sha256"]

    image = base.NdsImage.open(parent.ROM)
    clean = base.NdsImage.open(native.CLEAN)
    arm = image.read_file(native.ARM)
    packet = base.load(stage.PROOF)
    binding = packet["original_town_entries"][1]
    event = binding["event"]
    events = image.read_file(binding["event_archive"])
    assert native.digest(events) == binding["event_sha256"] and events == clean.read_file(binding["event_archive"])
    assert event["town"] == stage.TOWN and event["facility"] == 0 and event["event_ID"] == EXCHANGE.block
    assert event["date_comparison"] == 1
    rows = ordinary.source_rows(clean, image, event, EXCHANGE)
    plan_path = folder / "ordinary_panel_frames.json"
    plan = base.load(plan_path)
    snapshots = {row["frame"]:row for row in report["read_only_pause_RAM_snapshots"]}
    moments = {k:snapshots[plan[k]] for k in ("opened_town", "before_square", "returned")}
    states = {}
    for key, moment in moments.items():
        assert moment["read_only_export"] and base.digest(moment["path"]) == moment["sha256"]
        states[key] = ordinary.navigation_state(arm, Path(moment["path"]).read_bytes(), EXCHANGE)
    assert all(r["town"] == stage.TOWN and r["captain"] == 1 for r in states.values())
    before = states["before_square"]
    assert before["calendar"][2] == before["birthday"][1] == states["returned"]["calendar"][2]
    wait = Path(moments["before_square"]["path"]).read_bytes()
    at = wait.index(events[:96])
    assert wait.find(events[:96],at+1) == -1
    cpu,get = ordinary.town.get_machine(arm,wait)
    assert get(0x23840, ordinary.town.B + at - 0x30, event["event_ID"]) == 0
    assert bytes(cpu.mem_read(ordinary.town.B, 0x400000)) == wait
    completion = ordinary.previous.event_completion(arm, report, events, event,
        dict(route=1,final_calendar=states["returned"]["calendar"][1:],birthday=before["birthday"]))
    assert plan["before_square"] < min(plan["panels"]) < max(plan["panels"]) < plan["returned"] == report["frames"]
    captures = {row["frame"]:row for row in report["frames_captured"] if row["path"].endswith("_navigation.png")}
    panels, previews = ordinary.observe(image, rows, captures, plan["panels"], SPEAKERS)
    close, img = ordinary.town.read_frame(captures, plan["returned"])
    previews.append(("Return to Istanbul Square", img))
    sheets = {}
    for i in range(0,len(previews),6):
        target = folder / f"ordinary_panels_{i//6+1}.png"
        ordinary.town.sheet(previews[i:i+6], target)
        sheets[str(target)] = base.digest(target)
    base.save(NORMAL, dict(candidate_sha256=base.digest(parent.ROM), natural_square_activation=True,
        event=event, frames=plan, exact_complete_panels=panels, exit=close, states=states, moments=moments,
        native_completion=completion, sheets=sheets, hardware=False,
        evidence={str(p):base.digest(p) for p in (report_path, input_path, journal_path, plan_path, stage.PRIOR)}))


if __name__ == "__main__":
    cli = ArgumentParser(description=__doc__)
    cli.add_argument("action",choices=("capture","verify","ordinary"))
    action = cli.parse_args().action
    if action == "ordinary":
        verify_ordinary()
    else:
        run_lil(action)

