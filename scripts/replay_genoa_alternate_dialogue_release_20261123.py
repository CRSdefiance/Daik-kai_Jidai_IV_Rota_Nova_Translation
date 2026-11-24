"""Replay the staged alternate Genoa dialogue and verify the two complete returns."""

from argparse import ArgumentParser
from inspect import getsource
from types import FunctionType, SimpleNamespace

from PIL import ImageChops

from dk4tool.dialogue.font_audit import GameAsciiFont
from dk4tool.formats.ilnk import IlnkContainer
from scripts import replay_genoa_alternate_choices_20261123 as parent_runs
from scripts import stage_genoa_alternate_dialogue_20261123 as build
from scripts import verify_genoa_alternate_choices_20261123 as review
from scripts.source_locked_derivation_v5118 import checked_text
from scripts.stage_cartridge_title_20261123 import NdsImage, digest, read, reference, sha256, write
from scripts.verify_azores_return_20261123 import picture, shots
from scripts.verify_moonlit_violin_20261121 import bytes_for


ROOT = build.ROOT / "alternate_gameplay"
REPORT, SHEET = ROOT / "paired_genoa_alternates.json", ROOT / "paired_genoa_alternates_1_20261123.png"
gameplay = review.gameplay


def replay(branch):
    source = checked_text(getsource(parent_runs.replay), {
        '    assert digest(current.ROM) == release["candidate_sha256"]':
            '''    stage = read(STORED)
    assert stage["predecessor"]["sha256"] == release["candidate_sha256"]
    assert stage["staged"] == reference(current.ROM)''',
    })
    scope = vars(parent_runs) | dict(ROOT=ROOT, STORED=build.STORED,
        current=SimpleNamespace(RELEASE=build.parent.RELEASE, ROM=build.ROM))
    exec(compile(source, __file__ + "::ordinary-replay", "exec"), scope)
    scope["replay"](branch)


def verify_branch(branch, packet, stage, changes, block, ctx, kanji, renderer, font):
    old_path = parent_runs.ROOT / branch / "capture/capture_report.json"
    new_path = ROOT / branch / "capture/capture_report.json"
    before, after = map(read, (old_path, new_path))
    assert before["ROM_sha256"] == stage["predecessor"]["sha256"]
    assert after["ROM_sha256"] == stage["staged"]["sha256"]
    assert after["cold_boot"] and not after["savestate_loaded"] and not after["callback_errors"]
    assert not any(value for key, value in after.items() if key.startswith("synthetic_"))
    for field in ("frames", "scripted_input_schedule", "exact_requested_capture_frames"):
        assert before[field] == after[field]
    donor = after["battery_save_preloaded"]
    assert donor["source_sha256"] == before["battery_save_preloaded"]["source_sha256"] == digest(donor["source"])
    assert donor["copied_byte_exact_before_cold_boot"]
    old, new = (shots(run, "_cold_boot.png") for run in (before, after))
    pages, figures = {}, []
    for row in packet["story"]:
        ident = row["id"]
        if ident not in changes:
            continue
        change = changes[ident]
        offset = change["command_offset"]
        command = bytes.fromhex(change["after_hex"])
        assert block[offset:offset + len(command)] == command
        page, = renderer(ctx.arm, kanji, bytes_for(command))["pages"]
        plane = bytes.fromhex(page["native_plane_hex"])
        assert page["native_independent_plane_equal"] and sha256(plane).hexdigest() == change["page_sha256"]
        frame = row["frame"]["frame"]
        pre, post = picture(old[frame]), picture(new[frame])
        assert gameplay.mask_check(plane, 216, post), (branch, ident, frame)
        bounds = ImageChops.difference(pre, post).getbbox()
        assert bounds and 16 <= bounds[0] < bounds[2] <= 232 and 296 <= bounds[1] < bounds[3] <= 360
        name = gameplay.nameplate(font, row["speaker"], post)
        assert name == gameplay.nameplate(font, row["speaker"], pre)
        pages[frame] = dict(id=ident, frame=frame, full_native_page_sha256=change["page_sha256"], change_bounds=bounds,
            complete_nameplate=name, old_frame=old[frame], new_frame=new[frame], exact_command_hex=command.hex())
        figures.extend(((f"{ident} / Previous", pre), (f"{ident} / Revised", post)))
    controls = {}
    for frame in after["exact_requested_capture_frames"]:
        if frame not in pages:
            assert picture(old[frame]).tobytes() == picture(new[frame]).tobytes(), (branch, frame)
            controls[frame] = dict(before=old[frame], after=new[frame])
    assert len(pages) == (3 if branch == "no_liquor" else 1)
    return dict(reviewed_pages=list(pages.values()), identical_control_frames=controls,
        ordinary_selected_choice=review.OPTIONS[branch][1], retained_join_notice_and_tavern_return=True,
        donor=reference(donor["source"]), prior=reference(old_path), revised=reference(new_path)), figures


def verify():
    stage, reviewed = map(read, (build.STORED, review.OUT))
    assert stage["editorial_and_preflight"] == reference(review.OUT)
    assert stage["staged"] == reference(build.ROM)
    rom = NdsImage.open(build.ROM)
    arm, kanji = (rom.read_file(path) for path in (build.ARM, "/GRP/KANJI.FNT"))
    block = IlnkContainer.parse(rom.read_file(build.STORY)).blocks[170]
    ctx = SimpleNamespace(arm=arm, image=rom)
    font = GameAsciiFont.from_arm9(arm)
    renderer = gameplay.town.clipped_renderer(ctx)
    changes = {row["id"]: row for row in stage["changed"]}
    results, panels = {}, []
    for branch, packet in reviewed["choice_paths"].items():
        results[branch], figures = verify_branch(branch, packet, stage, changes, block, ctx, kanji, renderer, font)
        panels.extend(figures)
    count = sum(len(row["identical_control_frames"]) for row in results.values())
    assert len(panels) == 8 and count == 32
    sheets = FunctionType(gameplay.sheets_for.__code__, gameplay.sheets_for.__globals__ | {"OUT": REPORT})
    preview, = sheets("paired_genoa_alternates", panels, (0, 272, 256, 380))
    assert preview == reference(SHEET)
    write(REPORT, dict(candidate_sha256=stage["staged"]["sha256"], predecessor_sha256=stage["predecessor"]["sha256"],
        ordinary_controller_inputs=True, matched_control_frames=count, changed_page_holds=4,
        outcomes=results, visual=preview))
    print("Verified all four revised pages, both Genoa choice outcomes and 32 identical control frames.", flush=True)


if __name__ == "__main__":
    cli = ArgumentParser(description=__doc__)
    cli.add_argument("action", choices=("verify", *parent_runs.CASES))
    action = cli.parse_args().action
    verify() if action == "verify" else replay(action)
