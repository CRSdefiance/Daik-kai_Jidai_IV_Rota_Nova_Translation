"""Replay the stored elegy and validate both changes in the complete scene."""

from argparse import ArgumentParser
from inspect import getsource
from json import loads
from struct import unpack_from

from PIL import Image, ImageDraw

from dk4tool.dialogue.font_audit import GameAsciiFont
from scripts import replay_monster_fish_outcome_20261123 as outcome
from scripts import stage_hodram_B16_elegy_20261123 as stage
from scripts import verify_monster_fish_outcome_20261123 as prior
from scripts.source_locked_derivation_v5118 import checked_text
from scripts.stage_cartridge_title_20261123 import digest, read, reference, sha256, write


LABEL = "elegy_replay"
RUN = stage.ROOT / LABEL
INPUT = stage.ROOT / "candidate_playback_input.json"
PLAY = stage.ROOT / "elegy_paired_gameplay.json"
SHEET = stage.ROOT / "elegy_paired_gameplay.png"


def replay():
    stored = read(stage.STORED)
    release = read(stage.parent.RELEASE)
    actual = prior.Capture("outcome_verified", release)
    assert stored["staged"] == reference(stage.ROM) and stored["predecessor"] == reference(release["candidate"])
    assert stored["whole_parent_inverse"] and not RUN.exists()
    assert digest(actual.inputs) == read(prior.OUT)["controlled_runs"][-1]["inputs"]["sha256"]
    derived = release | dict(candidate=str(stage.ROM), candidate_sha256=stored["staged"]["sha256"])
    write(INPUT, derived)
    play = checked_text(getsource(outcome.trail.previous.play), {
        'lambda arm, raw, request: env["special_target"](':
            'lambda arm, raw, request: setup(env["special_target"], ',
        "fixture, = report[fixtures[0]]": "fixture, activation = report[fixtures[0]]",
    })

    def setup(starter, rom, arm_sha, model, arm, raw, request):
        if request == outcome.OUTCOME_REQUEST:
            return outcome.activate_after_played_damage(arm, raw)
        return outcome.shortened_encounter(starter, rom, arm_sha, model, arm, raw, request, activate=False)

    context = vars(outcome.trail.previous) | dict(ROOT=stage.ROOT, RELEASE=INPUT, setup=setup, __file__=__file__)
    exec(compile(play, __file__ + "::staged-elegy", "exec"), context)
    context["play"]("fish", LABEL, actual.inputs)


def verify():
    stored = read(stage.STORED)
    release = read(stage.parent.RELEASE)
    paired = read(prior.OUT)
    candidate = stored["staged"]["sha256"]
    assert candidate == digest(stage.ROM)
    old, new = prior.Capture("outcome_verified", release), prior.Capture(str(RUN), {"candidate_sha256":candidate})
    original_commands, repeated_commands = (
        [loads(line) for line in run.inputs.read_text(encoding="utf-8").splitlines()] for run in (old, new)
    )
    assert original_commands == repeated_commands and old.data["frames"] == new.data["frames"] == 12400
    assert old.data["scripted_input_schedule"] == new.data["scripted_input_schedule"]
    a, b = (run.data["synthetic_condition_fixtures"] for run in (old, new))
    assert [p["frame"] for p in a] == [p["frame"] for p in b] == [4800, 9030]
    assert b[0]["added_fixture"]["supplied_hull"] == 3
    assert a[1]["changes"] == b[1]["changes"]
    assert all(f["no_outcome_or_text_supply"] for f in b)
    image = stage.NdsImage.open(stage.ROM)
    arm = image.read_file(stage.ARM)
    assert sha256(arm).hexdigest() == stored["target_ARM9_sha256"] == release["target_ARM9_sha256"]
    glyphs = GameAsciiFont.from_arm9(arm)
    buffer = unpack_from("<I", arm, 0x54450)[0] - outcome.BASE
    commands = {c["record_ids"][0]: c for c in stored["commands"] if c["record_ids"]}
    intact, changed, comparisons = [], [], []
    for r in paired["story"]:
        frame = r["frame"]
        key = r["id"]
        command = bytes.fromhex(commands[key]["stored"])
        expected = command[6:command.index(0, 6)]
        verified, screen = prior.panel(new, frame, glyphs, buffer, r["speaker"], expected)
        old_screen = prior.captured(old.frames[frame])
        assert old_screen.crop((0, 192, 256, 295)).tobytes() == screen.crop((0, 192, 256, 295)).tobytes()
        if key in stored["plans"]:
            assert verified["lines"] == stored["plans"][key]["lines"] != r["lines"]
            changed.append(verified | dict(id=key, old_lines=r["lines"]))
            comparisons.append((key, old_screen, screen))
        else:
            assert old.frames[frame]["framebuffer_sha256"] == new.frames[frame]["framebuffer_sha256"]
            intact.append(frame)
    assert len(intact) == 12 and len(changed) == 2
    assert changed[0]["lines"][1] == "The waves lap in a familiar rhythm,"
    assert changed[1]["lines"][0] == "The sea is like a mother." and changed[1]["lines"][1].startswith("Both hold us")
    for frame in (4800, 7250, 8870, 9030, 9180, 12240, 12400):
        assert old.frames[frame]["framebuffer_sha256"] == new.frames[frame]["framebuffer_sha256"]
    for frame in (12240, 12400):
        state = prior.battle_state(arm, prior.read_ram(new.ram[frame]))
        assert list(state["context"]) == paired["source_states"][str(frame)]["context"] and not state["target"]["mobile"]
    sheet = Image.new("RGB", (1056, 460), (24, 26, 29))
    for index, (key, old_screen, screen) in enumerate(comparisons):
        y = index * 230
        ImageDraw.Draw(sheet).text((12, y + 8), f"{key} / Control and revised", fill="white")
        for x, capture in ((8, old_screen), (536, screen)):
            body = capture.crop((0, 269, 256, 369)).resize((512, 200), Image.Resampling.NEAREST)
            sheet.paste(body, (x, y + 25))
    sheet.save(SHEET)
    write(PLAY, dict(candidate_sha256=candidate, predecessor_sha256=release["candidate_sha256"],
                     gameplay_fixtures_disclosed=True, original_input_journal=reference(old.inputs),
                     captures=dict(parent=reference(old.report), candidate=reference(new.report)),
                     changed_pages=changed, unchanged_story_frames=intact, unchanged_victory_and_return=True,
                     all_14_story_pages_checked=True, one_page_per_command=True, visual=reference(SHEET)))
    print("Both revised pages and all 12 retained pages passed the paired complete-scene replay.")


if __name__ == "__main__":
    cli = ArgumentParser(description=__doc__)
    cli.add_argument("--verify-only", action="store_true")
    if not cli.parse_args().verify_only:
        replay()
    verify()
