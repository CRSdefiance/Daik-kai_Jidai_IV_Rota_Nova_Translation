"""Replay Rafael's revised panels and all five original midroute menu paths."""

from argparse import ArgumentParser
from inspect import getsource
from pathlib import Path
from struct import pack_into
from types import FunctionType
import sys

from scripts import replay_hodram_and_lil_followups_20261122 as branch_fixture
from scripts import replay_rafael_athens_and_maria_crew_20261122 as fixture
from scripts import replay_rafael_fleet_and_crew_exchanges_20261122 as precedent
from scripts import stage_rafael_midroute_exchanges_20261122 as stage
from scripts import verify_rafael_midroute_exchanges_20261122 as checked
from scripts.source_locked_derivation_v5118 import checked_text

base, native, gameplay = stage.base, stage.native, fixture.gameplay
ROOT = stage.ROOT / "focused_gameplay"
LIVE = ROOT / "verified_gameplay.json"
EXCERPTS = ROOT / "verified_excerpts.json"
PROMPTS = {118: 26, 136: 102}
RESULTS = {
    118: ((46, 50, 55, 58, 62), (78, 82, 87, 90, 94), (111, 116, 120, 125)),
    136: ((116,), (189,)),
}
RUNS = {f"b{block}_{slot}": (block, slot) for block, options in RESULTS.items() for slot in range(len(options))}
MODAL_SAMPLE = {(128, 42), (128, 56), (128, 89)}
BOOT = fixture.rafael_boot.BOOT.INPUTS


def record_id(block, ordinal):
    return f"DK4_MES_B{block}_R{ordinal:04d}"


def sample():
    draft = base.load(stage.REVIEW)
    return {0: tuple(
        (r["block"], int(r["id"].rsplit("R", 1)[1]))
        for r in draft["records"]
        if r["block"] != 118 and (
            r["decision"] == "revision"
            or (r["block"], int(r["id"].rsplit("R", 1)[1])) in MODAL_SAMPLE
        )
    )}


def report(run):
    if run == "0":
        return ROOT / "route0/capture/capture_report.json"
    return ROOT / run / "capture/capture_report.json"


def choice_paths(block):
    root = ROOT / f"b{block}_choice"
    return root, root / f"Rafael_B{block}_FOCUSED_ONLY.nds", root / "fixture.json"


def route_config(route):
    assert route == 0
    return {"opening": 44, "prefix": 40}


prepare_source = checked_text(getsource(branch_fixture.prepare_choice), {
    "def prepare_choice():": "def prepare_choice(block):\n    CHOICE_ROOT, CHOICE_ROM, CHOICE_RECEIPT = choice_paths(block)",
    '(row["route"], row["block"]) == (2, 133)': '(row["route"], row["block"]) == (0, block)',
    'route_config(2)': 'route_config(0)',
    'archive.blocks[133]': 'archive.blocks[block]',
    'record_id(133, 145)': 'record_id(block, PROMPTS[block])',
    'c["word"] == 0x2100': 'c["word"] == (0x2200 if block == 118 else 0x2100)',
    'exact_contiguous_suffix_source_block=133': 'exact_contiguous_suffix_source_block=block',
})
branch_scope = vars(branch_fixture) | globals()
exec(compile(prepare_source, __file__ + "::exact-menu-suffix", "exec"), branch_scope)

excerpt_source = checked_text(precedent.fixture_source, {
    "Rafael_Fleet_And_Crew_FOCUSED_ONLY.nds": "Rafael_Midroute_Exchanges_FOCUSED_ONLY.nds",
})
excerpt_verify = checked_text(precedent.verify_source, {
    'assert len(observations) == len(SAMPLE[0]) and system.keys() <= {r["id"] for r in observations}':
        'assert len(observations) == len(SAMPLE[0])',
    'assert {r["id"] for r in by_id.values() if r["layouts"]} <= {r["id"] for r in observations}':
        'assert {r["id"] for r in by_id.values() if r["layouts"] and r["block"] != 118} <= {r["id"] for r in observations}',
    'rafael_fleet_and_crew_gameplay_': 'rafael_midroute_excerpt_',
})
excerpt_scope = precedent.scope | globals() | dict(LIVE=EXCERPTS, RUNTIME_VALUES={})
excerpt_scope["scope"] = excerpt_scope
for function in ("receipt", "report_path", "run_file", "play"):
    inherited = precedent.scope[function]
    excerpt_scope[function] = FunctionType(inherited.__code__, excerpt_scope)
for source in (excerpt_source, excerpt_verify):
    exec(compile(source, __file__ + "::revised-panel-excerpts", "exec"), excerpt_scope)


def replay():
    excerpt_scope["SAMPLE"] = sample()
    excerpt_scope["fixture"](0)
    excerpt_scope["play"](0)


def branch_frames(run):
    block, selected = RUNS[run]
    responses = RESULTS[block][selected]
    buttons = [(4000, "A"), *[(4600 + i * 160, "DOWN") for i in range(selected)]]
    buttons.extend((5050 + i * 400, "A") for i in range(len(responses)))
    holds = [3900, 4300, 4970, *(5350 + i * 400 for i in range(len(responses)))]
    return buttons, holds


def play_choice(run):
    block, _ = RUNS[run]
    _, rom, receipt = choice_paths(block)
    proof = base.load(receipt)
    assert proof["rom_sha256"] == base.digest(rom)
    out = report(run).parent
    out.parent.mkdir(exist_ok=True)
    steps, holds = branch_frames(run)
    inputs = out.parent / "inputs.json"
    base.save(inputs, base.load(BOOT) + [dict(start=f, duration=8, buttons=[button]) for f, button in steps])
    harness = fixture.harness
    sys.argv = [harness.__file__, "--rom", str(rom), "--out", str(out), "--frames", str(holds[-1] + 120),
                "--inputs-json", str(inputs), "--press-start", "-1", "--capture-every", "999999",
                "--capture-at", *map(str, holds)]
    harness.main()


def verify_branches():
    proof, draft, layout, modal, choice_tables = map(base.load, (
        stage.PROOF, stage.REVIEW, stage.NATIVE, stage.FE_PROOF, checked.CHOICES))
    candidate = base.digest(stage.ROM)
    assert all(d["candidate_sha256"] == candidate for d in (proof, layout, modal, choice_tables))
    runtime = base.load(stage.parent.RELEASE)
    ctx = native.RegisteredRuntime(stage.parent.RELEASE, runtime["own_registered_startup"], captain=3)
    font = ctx.image.read_file("/GRP/KANJI.FNT")
    paint = stage.established.display.clipped_renderer(ctx)
    names = gameplay.GameAsciiFont.from_arm9(ctx.arm)
    bodies = {(0, r["id"]): r for r in layout["records"]}
    modals = {(0, r["id"]): r for r in modal["records"]}
    source = {r["id"]: r for r in draft["records"]}
    observations, choices, reports, pictures = [], [], {}, []
    for run, (block, selection) in RUNS.items():
        _, rom, receipt = choice_paths(block)
        saved = base.load(receipt)
        assert saved["candidate_sha256"] == candidate and saved["exact_inverse"] and not saved["natural_activation"]
        path = report(run)
        data = base.load(path)
        branch_fixture.verify_capture(data, rom, saved["rom_sha256"], path.parent.parent / "inputs.json")
        reports[run] = base.digest(path)
        texts = [r["caption"] for r in choice_tables["choices"] if r["block"] == block]
        menu_views = []
        for frame, expected in ((4300, 0), (4970, selection)):
            hold, screen = gameplay.screen(data, frame)
            labels = gameplay.captions(names, screen, texts)
            selected = [i for i, r in enumerate(labels) if r["background"] == gameplay.MENU_HIGHLIGHT]
            assert selected == [expected], (run, frame, selected)
            menu_views.append(dict(capture=hold, labels=labels))
            if frame == 4970:
                pictures.append((f"SC0 B{block} / {texts[selection]}", screen))
        responses = RESULTS[block][selection]
        for ordinal, frame in zip((PROMPTS[block], *responses), (3900, *branch_frames(run)[1][3:]), strict=True):
            row = source[record_id(block, ordinal)]
            width, plane = branch_fixture.panel_mask(row, bodies, modals, ctx, paint, font)
            hold, screen = gameplay.screen(data, frame)
            assert gameplay.mask_check(plane, width, screen), (run, row["id"], frame)
            if width == 216:
                gameplay.glyphs(names, screen, row["speaker"], (16, 277), gameplay.LABEL_COLOR, 226)
            else:
                assert not any(pixel == gameplay.LABEL_COLOR for pixel in screen.crop((16, 277, 226, 288)).get_flattened_data())
            observations.append(branch_fixture.observation(row, run, hold, bodies[0, row["id"]]["command_offset"]))
            pictures.append((f"{run} / {row['id']} / {row['speaker']}", screen))
        choices.append(dict(run=run, block=block, slot=selection, caption=texts[selection],
                            observations=menu_views, original_branch_executed=True,
                            fixture_sha256=saved["rom_sha256"], response_ids=[record_id(block, v) for v in responses]))
    sheets = []
    for offset in range(0, len(pictures), 6):
        path, digest = gameplay.make_sheet(ROOT / f"rafael_midroute_menus_{1 + offset//6}.png", pictures[offset:offset+6])
        sheets.append(dict(path=path, sha256=digest))
    return observations, choices, reports, sheets


def verify():
    excerpt_scope["SAMPLE"] = sample()
    if not EXCERPTS.exists():
        excerpt_scope["verify"]()
    clips = base.load(EXCERPTS)
    assert clips["candidate_sha256"] == base.digest(stage.ROM)
    observations, choices, reports, sheets = verify_branches()
    all_holds = clips["observations"] + observations
    revised = {r["id"] for r in base.load(stage.REVIEW)["records"] if r["decision"] == "revision"}
    assert revised <= {r["id"] for r in all_holds} and len(choices) == 5
    base.save(LIVE, clips | dict(observed_speech_pages=len(all_holds), observations=all_holds,
        original_menu_choices=choices, report_sha256=clips["report_sha256"] | reports,
        sheets=clips["sheets"] + sheets, natural_story_triggers_claimed=False, hardware=False))
    print(f"Verified {len(all_holds)} focused display holds and all five original menu outcomes.", flush=True)


if __name__ == "__main__":
    parser = ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=("replay", "prepare_choices", "verify", *RUNS))
    action = parser.parse_args().action
    if action == "prepare_choices":
        for block in PROMPTS:
            branch_scope["prepare_choice"](block)
    elif action in RUNS:
        play_choice(action)
    else:
        globals()[action]()
