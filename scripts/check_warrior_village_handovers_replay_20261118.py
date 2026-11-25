"""Check Hodram's menus and branch alongside Rafael's training replay."""

from argparse import ArgumentParser
from types import FunctionType

from scripts import check_caves_offshore_monk_replay_20261118 as prior
from scripts import replay_warrior_village_handovers_20261118 as game
from scripts import verify_forest_expeditions_20261118 as display

stage, base, native, parent = game.stage, game.base, game.native, game.stage.parent
EARLIER = stage.ROOT.with_name("research_v1")
TRIAL_ROOT = EARLIER / game.ROOT.name
TRIAL_ROM, TRIAL_SETUP = TRIAL_ROOT / game.ROM.name, TRIAL_ROOT / game.SETUP.name
TRIAL_REPORT = TRIAL_ROOT / game.LIVE.name
MENU_ROOT = EARLIER / "menu"
LIVE = stage.ROOT / "verified_replays.json"
PICKS = ((674, 4100, 4150, "Keep going"), (934, 5150, 5200, "Push on anyway"))
FOG_REFS = (520, 718, 754, 976, 1010, 1244, 1916)


def menus():
    release = base.load(parent.RELEASE)
    staged = base.load(stage.PROOF)
    group = prior.scene(staged, 1, 316)
    rows = {r["id"]: r for r in base.load(stage.review.OUTPUT)["records"] if r["route"] == 1}
    check = FunctionType(display.menu_checker.__code__, vars(display) | {"parent": parent})
    ctx = native.RegisteredRuntime(parent.RELEASE, release["own_registered_startup"], captain=3)
    MENU_ROOT.mkdir()
    receipts = []
    for offset, _, _, label in PICKS:
        cmd = next(c for c in group["commands"] if c["source_offset"] == offset)
        receipt = check(ctx, release, cmd, [rows[i] for i in cmd["record_ids"]], MENU_ROOT / str(offset))
        output = base.load(receipt["menu_path"])
        assert output["versions"][-1]["cases"][0]["native_VM"]["labels"][0] == label
        receipts.append(receipt | {"source_offset": offset})
    base.save(MENU_ROOT / "menus.json", receipts)


def verify():
    assert not LIVE.exists()
    stage_proof, release, trial = map(base.load, (stage.PROOF, parent.RELEASE, TRIAL_REPORT))
    report_path = game.HODRAM_ROOT / "capture/capture_report.json"
    report, setup = map(base.load, (report_path, game.HODRAM_SETUP))
    assert setup["initialized_Hodram"] and setup["whole_ROM_inverse"] and setup["original_fog_commands_exact"]
    assert report["cold_boot"] and not report["savestate_loaded"] and not report["callback_errors"]
    assert not report.get("battery_save_preloaded") and not setup["natural_activation"]
    assert report["ROM_sha256"] == setup["fixture_sha256"] == base.digest(game.HODRAM_ROM)
    assert setup["candidate_sha256"] == stage_proof["candidate_sha256"] == base.digest(stage.ROM)
    assert trial["initialized_Rafael"] and trial["actual_Rafael_macro_and_speakerless_FE"]
    assert len(trial["holds"]) == 30
    assert all(base.digest(p) == v for p, v in trial["evidence"].items())
    first = EARLIER / stage.ROM.name
    original = base.NdsImage.open(first)
    image = base.NdsImage.open(stage.ROM)
    exact_trial = base.load(TRIAL_SETUP)
    assert exact_trial["candidate_sha256"] == trial["candidate_sha256"] == base.digest(first)
    assert exact_trial["fixture_sha256"] == trial["fixture_sha256"] == base.digest(TRIAL_ROM)
    assert prior.pixels.assets(image) == prior.pixels.assets(original)
    archives = [native.IlnkContainer.parse(rom.read_file("/data/SC0.DK4")).blocks for rom in (original, image)]
    assert all(archives[0][b] == archives[1][b] for b in (44, 336, 337, 338))
    assert report["scripted_input_schedule"] == base.load(setup["inputs"])
    group = prior.scene(stage_proof, 1, 316)
    commands = {c["source_offset"]: c for c in group["commands"]}
    assert set(FOG_REFS) <= set(setup["included_source_offsets"])
    assert prior.pixels.assets(image) == prior.pixels.assets(base.NdsImage.open(game.HODRAM_ROM))
    arm, font = [image.read_file(p) for p in (native.ARM, "/GRP/KANJI.FNT")]
    ctx = native.RegisteredRuntime(parent.RELEASE, release["own_registered_startup"], captain=3)
    assert ctx.arm == arm
    _, paint = stage.stage.progressive.layout.prior.precedent.planners(arm)
    fe_paint = stage.stage.system.native_painter(ctx)
    tool = game.rafael.scope["quest"].prior.TOOL
    photos = tool.photos(report)
    masks = [(n, tuple(map(frozenset, tool.body_masks(img)))) for n, (_, img) in sorted(photos.items())]

    def raster(body, selector):
        if selector == 254:
            physical = fe_paint(body)["physical"]
            return bytes(int(bool(v)) for y in range(64) for v in physical[y * 228:y * 228 + 216])
        page, = paint(arm, font, body)["pages"]
        return bytes.fromhex(page["native_plane_hex"])

    fog = prior.match_bodies(commands, FOG_REFS, masks, raster, b"Hodram", tool, photos, 3650)
    evidence = trial["evidence"] | {str(p): base.digest(p) for p in (TRIAL_REPORT, report_path, game.HODRAM_SETUP)}
    contacts, choices = [], []
    for (offset, frame, confirm, label), receipt in zip(PICKS, base.load(MENU_ROOT / "menus.json"), strict=True):
        proof_path = receipt["menu_path"]
        layout = base.load(proof_path)
        assert offset == receipt["source_offset"] and layout["native_choice_object_hex"] == commands[offset]["stored"]
        assert base.digest(proof_path) == receipt["proof_sha256"]
        capture, shot = photos[frame]
        assert prior.pixels.selected_option(shot, layout, 0) == label
        assert [i["start"] for i in report["scripted_input_schedule"]
                if i["buttons"] == ["A"] and frame < i["start"] <= confirm] == [confirm]
        assert any(h["frame"] < frame for h in fog) and any(h["frame"] > confirm for h in fog)
        choices.append(dict(source_offset=offset, capture=capture, selected=label, confirmation=confirm,
                            native_receipt=receipt))
        contacts.append(layout["review_sheet"])
        evidence[proof_path] = receipt["proof_sha256"]
    timeline = [(h["id"] or "Crew reply", h["frame"]) for h in fog]
    timeline.extend((m["selected"], m["capture"]["frame"]) for m in choices)
    timeline.sort(key=lambda r: r[1])
    contacts += prior.sheets(stage.ROOT, timeline, photos, "hodram_live")
    assert len(fog) == 7 and len(choices) == 2
    base.save(LIVE, trial | dict(candidate_sha256=stage_proof["candidate_sha256"],
        initialized_Hodram=True, both_fog_choices_confirmed=True,
        Rafael_replay_reused_from=trial["candidate_sha256"], exact_Rafael_blocks=[44, 336, 337, 338],
        holds=trial["holds"] + fog, menus=choices, sheets=trial["sheets"] + contacts, evidence=evidence))
    print("Matched Rafael's 30 trial holds and Hodram's two fog menus and seven dialogue holds.", flush=True)


if __name__ == "__main__":
    parser = ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=("menus", "verify"))
    globals()[parser.parse_args().action]()
