"""Stage the reviewed village sighting and compare the position-only replay."""

from argparse import ArgumentParser
from inspect import getsource
from pathlib import Path
from shutil import copyfile
from types import FunctionType, SimpleNamespace

from PIL import ImageChops
from scripts import observe_narvik_focused_visit_20261124 as focused
from scripts import review_copenhagen_narvik_20261124 as review
from scripts import stage_tunis_shop_advice_20261124 as shared
from scripts.source_locked_derivation_v5118 import checked_text
from scripts.stage_cartridge_title_20261123 import NdsImage, digest, read, reference, write


KEY, trend, panels = review.KEY, shared.trend, review.panels
played = SimpleNamespace(RELEASE=review.RELEASE)
ROOT = Path("E:/Rota Nova translations/Generated/work/editorial_20261124_narvik_lookout")
ROM, STORED, PAIRED = (ROOT / name for name in ("Narvik_Lookout_STAGED.nds", "stored_proof.json", "paired_gameplay.json"))
PATCH, REBUILT, PATCH_PROOF = (ROOT / name for name in ("translation.xdelta", "clean_rebuilt.nds", "clean_patch_proof.json"))
STARTUP_CAPTURE = ROOT / "startup/capture/capture_report.json"
REPLAY = ROOT / "replay"
CONTROLLER = REPLAY / "controller.jsonl"
CHANGED = 5400


def stage():
    source = checked_text(getsource(shared.stage), {
        'sum(len(sheet["messages"]) for sheet in proof["proposed_sheets"]) == 124':
            'sum(len(sheet["messages"]) for sheet in proof["proposed_sheets"]) == 2',
    })
    scope = vars(shared) | globals()
    exec(compile(source, __file__ + "::fixed-allocation", "exec"), scope)
    scope["stage"]()


def candidate_release(stored):
    parent = read(played.RELEASE)
    assert stored["predecessor_sha256"] == parent["candidate_sha256"]
    assert stored["candidate_sha256"] == digest(ROM)
    assert stored["target_ARM9_sha256"] == parent["target_ARM9_sha256"]
    return parent | dict(candidate=str(ROM), candidate_sha256=stored["candidate_sha256"],
                         target_COMMON_sha256=stored["target_COMMON_sha256"])


def replay(stored):
    proof = read(review.OUT)
    assert proof["location_only_narvik"]["controller"] == reference(focused.CONTROLLER)
    REPLAY.mkdir()
    copyfile(focused.CONTROLLER, CONTROLLER)
    source = Path(focused.__file__).read_text(encoding="utf-8")
    main = source[source.index('if __name__ == "__main__":'):]
    command = checked_text(main, {
        'release = replay.base.load(active.RELEASE)': 'release = staged_receipt',
        'driver = checked_text(getsource(replay.main), {':
            'driver = checked_text(getsource(replay.main), {\n'
            '        "release = base.load(current.RELEASE)": "release = staged_receipt",',
        '__file__=__file__)': '__file__=__file__, staged_receipt=staged_receipt)',
    })
    scope = vars(focused) | dict(ROOT=REPLAY, CONTROLLER=CONTROLLER, __name__="__main__",
        __file__=__file__, staged_receipt=candidate_release(stored))
    exec(compile(command, __file__ + "::source-locked-replay", "exec"), scope)


def verify(stored):
    parent, current = read(played.RELEASE), candidate_release(stored)
    before, old_calls, source = review.capture(focused, parent, location_only=True)
    runner = SimpleNamespace(ROOT=REPLAY, CONTROLLER=CONTROLLER, NARVIK=focused.NARVIK)
    after, calls, test = review.capture(runner, current, location_only=True)
    assert old_calls == calls and before.keys() == after.keys() and max(after) == 13800
    assert test["controller"]["sha256"] == source["controller"]["sha256"]
    assert test["donor"] == source["donor"]
    assert test["location_fixture"] == source["location_fixture"]
    font = panels.GameAsciiFont.from_arm9(NdsImage.open(ROM).read_file(trend.ARM))
    unchanged, changed, figures = [], None, []
    for frame in sorted(after):
        old, new = (panels.picture(group[frame]) for group in (before, after))
        bounds = ImageChops.difference(old, new).getbbox()
        if frame == CHANGED:
            assert bounds and 16 <= bounds[0] < bounds[2] <= 244 and 296 <= bounds[1] < bounds[3] <= 360
            plate = panels.nameplate(font, review.LOOKOUT, new)
            assert plate == panels.nameplate(font, review.LOOKOUT, old)
            ink = panels.exact_body(font, (review.PROPOSED,), new)
            changed = dict(frame=frame, bounds=bounds, full_native_ink_pixels=ink, nameplate=plate, capture=after[frame])
            figures.extend([("Narvik / before", old), ("Narvik / revised", new)])
        else:
            assert bounds is None, (frame, bounds)
            unchanged.append(frame)
    assert changed is not None
    for frame in (5800, 6200, 7000, 7700, 13000, 13400):
        figures.append((f"Retained / {frame}", panels.picture(after[frame])))
    draw = FunctionType(panels.sheets_for.__code__, vars(panels) | dict(OUT=PAIRED),
                        argdefs=panels.sheets_for.__defaults__)
    sheets = draw("paired_narvik_lookout_20261124", figures)
    write(PAIRED, dict(candidate_sha256=current["candidate_sha256"], predecessor_sha256=parent["candidate_sha256"],
        before=source, after=test, stored=reference(STORED), changed=changed, unchanged_frames=unchanged,
        same_trace_message_requests=True, position_only_focused_gameplay=True, sheets=sheets))
    print(f"Verified the complete revised line and {len(unchanged)} unchanged focused gameplay frames.")


if __name__ == "__main__":
    cli = ArgumentParser(description=__doc__)
    cli.add_argument("action", choices=("stage", "replay", "verify", "patch", "startup"))
    action = cli.parse_args().action
    if action == "stage":
        stage()
    elif action in ("replay", "verify"):
        globals()[action](read(STORED))
    else:
        FunctionType(shared.release_check.__code__, vars(shared) | globals())(read(STORED), action)
