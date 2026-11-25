"""Check the Tavern purchase and Help history on the staged candidate."""

import io
import sys
from argparse import ArgumentParser
from inspect import getsource
from subprocess import run
from types import FunctionType

from scripts import plan_reviewed_help_navigation_v1 as help_nav
from scripts import verify_reviewed_help_navigation_v1 as help_verify
from scripts import observe_genoa_copenhagen_town_20261123 as past
from scripts import stage_tavern_buy_a_round_20261124 as build
from scripts import verify_genoa_copenhagen_town_20261123 as panels
from scripts.check_rafael_B84_training_gameplay_20261122 import MENU_HIGHLIGHT, captions
from scripts.source_locked_derivation_v5118 import checked_text
from scripts.stage_cartridge_title_20261123 import NdsImage, digest, read, reference, write


HELP_PLAY = build.ROOT / "help_ordinary_verified"
HELP_PROOF = HELP_PLAY / "verification/ordinary_gameplay_verification.json"
TAVERN_PLAY = build.ROOT / "tavern_play"
TAVERN_PROOF = TAVERN_PLAY / "ordinary_round.json"
MENU_SHEET = TAVERN_PLAY / "tavern_round_paired_1_20261123.png"
FIRST_TOWN = 3200


def invoke(module, *arguments):
    run([sys.executable, "-B", "-m", f"scripts.{module}", *map(str, arguments)], check=True)


def adapted_main(module, edits, *args, **bindings):
    code = checked_text(getsource(module.main), edits)
    scope = vars(module) | bindings
    exec(compile(code, __file__ + "::" + module.__name__, "exec"), scope)
    argv = sys.argv
    try:
        sys.argv = [module.__file__, *map(str, args)]
        scope["main"]()
    finally:
        sys.argv = argv


def help_play():
    HELP_PLAY.mkdir()
    stored = read(build.STORED)
    assert digest(build.ROM) == stored["candidate"]["sha256"] and reference(build.PLAN) == stored["help_plan"]
    _, _, baseline = panels.capture("copenhagen", read(past.current.RELEASE))
    report, terminal = [read(baseline[key]["path"]) for key in ("capture", "terminal")]
    donor = report["battery_save_preloaded"]
    assert digest(donor["source"]) == donor["source_sha256"]
    initial = past.ROOT / "copenhagen/inputs.json"
    assert digest(initial) == terminal["evidence"][str(initial)]
    entry = HELP_PLAY / "copenhagen_help_entry.json"
    write(entry, [*read(initial), dict(start=FIRST_TOWN + 1, duration=8, buttons=["SELECT"]),
        dict(start=FIRST_TOWN + 401, duration=8, buttons=["X"])])
    qualification, itinerary = (HELP_PLAY / name for name in ("qualification.json", "itinerary.json"))
    write(qualification, dict(research_ROM=str(build.ROM), research_ROM_sha256=stored["candidate"]["sha256"]))
    actions = [dict(open=11), dict(open=12), dict(remember="Tavern index"), dict(open=14), dict(remember="Buy a Round article"),
        dict(open=15), dict(remember="Recruit Crew article"), dict(open=139), dict(key="L"),
        dict(return_to="Recruit Crew article"), dict(key="L"), dict(return_to="Buy a Round article"),
        dict(key="L"), dict(return_to="Tavern index")]
    write(itinerary, dict(start_frame=FIRST_TOWN + 800, required_topics=sorted(build.ARTICLES), actions=actions))
    navigation = HELP_PLAY / "navigation"
    adapted_main(help_nav, {'dict(start=21001,duration=8,buttons=[\'X\']) and now>=21400':
        'dict(start=FIRST_TOWN+401,duration=8,buttons=[\'X\']) and now==FIRST_TOWN+800',
        'controls_only_no_fixtures_state_injection_orbattery=True': 'controls_only_no_fixtures_or_state_injection=True'},
        "--qualification", qualification, "--plan", build.PLAN, "--itinerary", itinerary, "--entry", entry,
        "--out", navigation, FIRST_TOWN=FIRST_TOWN)
    nav_path = navigation / "navigation_plan.json"
    nav = read(nav_path)
    capture = HELP_PLAY / "capture"
    frames = [nav["page_frames"][str(n)] for n in nav["observed_reviewed_topics"]]
    frames.extend(frame for pair in nav["return_pairs"] for frame in pair["frames"])
    invoke("headless_desmume_v193", "--rom", build.ROM, "--out", capture, "--frames", nav["terminal_frame"],
           "--inputs-json", navigation / "inputs.json", "--press-start", -1, "--touchscreen", "--capture-every", 999999,
           "--battery-save", donor["source"], "--dump-capture-ram", "--capture-at", *sorted(set(frames)))
    assert digest(donor["source"]) == donor["source_sha256"]
    adapted_main(help_verify, {"and not report.get('battery_save_preloaded')":
        "and report['battery_save_preloaded']['source_sha256']==DONOR and report['battery_save_preloaded']['copied_byte_exact_before_cold_boot']",
        "full_story_playthrough=False,hardware=False": "ordinary_existing_battery_save=True,full_story_playthrough=False,hardware=False"},
        "--capture", capture, "--navigation", nav_path, "--plan", build.PLAN, "--out", HELP_PROOF.parent,
        DONOR=donor["source_sha256"])


def tavern_play():
    stored = read(build.STORED)
    assert digest(build.ROM) == stored["candidate"]["sha256"]
    old, trace, evidence = panels.capture("copenhagen", read(past.current.RELEASE))
    source = past.ROOT / "copenhagen"
    report = read(evidence["capture"]["path"])
    terminal = read(evidence["terminal"]["path"])
    initial, commands = (source / name for name in ("inputs.json", "controller.jsonl"))
    assert all(digest(p) == terminal["evidence"][str(p)] for p in (initial, commands))
    donor = report["battery_save_preloaded"]
    assert digest(donor["source"]) == donor["source_sha256"]
    TAVERN_PLAY.mkdir()
    inputs = TAVERN_PLAY / "inputs.json"
    inputs.write_bytes(initial.read_bytes())
    controller = TAVERN_PLAY / "controller.jsonl"
    controller.write_bytes(commands.read_bytes())
    harness = past.replay.harness
    saved_input, argv = sys.stdin, sys.argv
    with io.TextIOWrapper(io.BytesIO(controller.read_bytes()), encoding="utf-8") as stream:
        try:
            sys.stdin = stream
            sys.argv = [harness.__file__, "--rom", str(build.ROM), "--out", str(TAVERN_PLAY / "capture"),
                "--frames", "90000", "--inputs-json", str(inputs), "--press-start", "-1", "--capture-every", "999999",
                "--battery-save", donor["source"], "--touchscreen", "--pause-at", str(past.FIRST_PAUSE)]
            harness.main()
        finally:
            sys.stdin, sys.argv = saved_input, argv
    assert digest(donor["source"]) == donor["source_sha256"]

    tavern_verify()


def tavern_verify():
    stored = read(build.STORED)
    old, trace, evidence = panels.capture("copenhagen", read(past.current.RELEASE))
    report = read(evidence["capture"]["path"])
    donor = report["battery_save_preloaded"]
    controller = TAVERN_PLAY / "controller.jsonl"
    capture, journal = [TAVERN_PLAY / "capture" / n for n in ("capture_report.json", "navigation_command_journal.json")]
    result, nav = map(read, (capture, journal))
    assert result["ROM_sha256"] == nav["ROM_sha256"] == stored["candidate"]["sha256"] and result["cold_boot"]
    assert not result["savestate_loaded"] and not result["callback_errors"]
    assert not any(v for k, v in result.items() if k.startswith("synthetic_"))
    assert result["battery_save_preloaded"]["source_sha256"] == donor["source_sha256"]
    assert result["battery_save_preloaded"]["copied_byte_exact_before_cold_boot"]
    assert result["scripted_input_schedule"] == report["scripted_input_schedule"]
    assert nav["commands_received"] == read(evidence["journal"]["path"])["commands_received"]
    assert result["frames"] == nav["last_command_frame"] == report["frames"] == 9200
    new = {r["frame"]: r for r in result["frames_captured"] if r["path"].endswith("_navigation.png")}
    stable = []
    for frame in (6600, 7200, 7400, 7600, 7800, 8000, 8400, 8800, 9200):
        assert old[frame]["framebuffer_sha256"] == new[frame]["framebuffer_sha256"], frame
        stable.append(dict(frame=frame, previous=old[frame], candidate=new[frame]))
    image = NdsImage.open(build.ROM)
    font = panels.GameAsciiFont.from_arm9(image.read_file(build.ARM))
    earlier, revised = [panels.picture(holds[7000]) for holds in (old, new)]
    old_labels = captions(font, earlier, ["Order Drink", "Treat Everyone", "Recruit Crew"])
    new_labels = captions(font, revised, ["Order Drink", build.LABEL, "Recruit Crew"])
    assert old_labels[1]["background"] == new_labels[1]["background"] == MENU_HIGHLIGHT
    assert all(r["background"] != MENU_HIGHLIGHT for r in (new_labels[0], new_labels[2]))
    funds = [panels.find_mask(font, name, panels.picture(new[f]), (74, 348, 138, 364))
             for f, name in ((7000, "43235"), (8200, "42999"))]
    sheets = FunctionType(panels.sheets_for.__code__, vars(panels) | {"OUT": TAVERN_PROOF})
    sheet, = sheets("tavern_round_paired", [("Prior selection", earlier), ("Revised selection", revised),
        ("Original 236-gold approval", panels.picture(new[7200])), ("Return to Copenhagen", panels.picture(new[9200]))], (0, 250, 256, 362))
    assert sheet == reference(MENU_SHEET)
    write(TAVERN_PROOF, dict(candidate_sha256=stored["candidate"]["sha256"], ordinary_battery_save=True,
        source=evidence, candidate_capture=reference(capture), candidate_journal=reference(journal), original_commands=reference(controller),
        original_common_requests=trace, price=236, funds_before=43235, funds_after=42999, complete_fund_glyphs=funds,
        complete_menu_captions=new_labels, menu_capture=new[7000], stable_frames=stable,
        observed_purchase_announcement_and_rumor=True, ordinary_town_return=True, sheet=sheet))
    print("Verified the complete new Tavern label, the 236-gold purchase, and the normal gossip and town return.")


if __name__ == "__main__":
    cli = ArgumentParser(description=__doc__)
    cli.add_argument("action", choices=("help_play", "tavern_play", "tavern_verify"))
    globals()[cli.parse_args().action]()
