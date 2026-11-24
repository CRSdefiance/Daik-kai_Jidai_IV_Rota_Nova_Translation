"""Replay the Narvik Promised Words acceptance on the staged village-clue build."""

from argparse import ArgumentParser
from inspect import getsource
from pathlib import Path
from shutil import copyfile
from types import FunctionType, SimpleNamespace

from PIL import ImageChops

from scripts import stage_narvik_lookout_20261124 as baseline
from scripts import stage_village_clue_punctuation_20261124 as build
from scripts.source_locked_derivation_v5118 import checked_text
from scripts.stage_cartridge_title_20261123 import NdsImage, digest, read, reference, write
from scripts.verify_narvik_lookout_replay_20261124 import coordinate_proof


focused, panels = baseline.focused, baseline.panels
ROOT = build.ROOT / "replay"
CONTROLLER, OUT = ROOT / "controller.jsonl", build.ROOT / "paired_gameplay.json"
RESULT = 13000


def candidate_release():
    old, proof = map(read, (build.RELEASE, build.STORED))
    assert old["candidate_sha256"] == proof["predecessor_sha256"]
    assert digest(proof["candidate"]) == proof["candidate_sha256"]
    assert proof["target_COMMON_sha256"] == old["target_COMMON_sha256"] and proof["whole_parent_inverse"]
    return old | {key: proof[key] for key in ("candidate", "candidate_sha256", "target_ARM9_sha256")}


def replay():
    receipt = candidate_release()
    approved = read(build.RELEASE)
    assert digest(approved["candidate"]) == approved["candidate_sha256"]
    original, current = [NdsImage.open(case["candidate"]).read_file(build.ARM) for case in (approved, receipt)]
    # The dock fixture is identical. Rebind its whole ARM9 assertion only after
    # independently recovering the approved bytes from the exact owned pool edits.
    old_code = build.MainCodeFile(original, build.BASE)
    new_code = build.MainCodeFile(current, build.BASE)
    for edit in read(build.STORED)["changed_pool_spans"]:
        offset, size = edit["pool_offset"], edit["extent"]
        assert new_code.sections[3].data[offset:offset + size].hex() == edit["after_hex"]
        new_code.sections[3].data[offset:offset + size] = bytes.fromhex(edit["before_hex"])
    assert bytes(new_code.save()) == original == bytes(old_code.save())
    relocator = checked_text(getsource(focused.visit_position), {
        "release = replay.base.load(active.RELEASE)": "release = staged_release",
    })
    scope = vars(focused) | dict(staged_release=receipt)
    exec(compile(relocator, __file__ + "::same-Narvik-coordinates", "exec"), scope)

    active = Path(focused.__file__).read_text(encoding="utf-8")
    driver = checked_text(active[active.index('if __name__ == "__main__":'):], {
        "release = replay.base.load(active.RELEASE)": "release = staged_release",
        "driver = checked_text(getsource(replay.main), {":
            'driver = checked_text(getsource(replay.main), {\n'
            '        "release = base.load(current.RELEASE)": "release = staged_release",',
        "__file__=__file__)": "__file__=__file__, staged_release=staged_release)",
    })
    scope.update(ROOT=ROOT, CONTROLLER=CONTROLLER, __file__=__file__, __name__="__main__")
    paired = read(baseline.PAIRED)
    assert paired["candidate_sha256"] == approved["candidate_sha256"]
    assert reference(baseline.CONTROLLER) == paired["after"]["controller"]
    ROOT.mkdir()
    copyfile(baseline.CONTROLLER, CONTROLLER)
    exec(compile(driver, __file__ + "::source-locked-Narvik-replay", "exec"), scope)


def verify():
    source = read(build.RELEASE)
    installed = candidate_release()
    a = SimpleNamespace(ROOT=baseline.REPLAY, CONTROLLER=baseline.CONTROLLER, NARVIK=focused.NARVIK)
    b = SimpleNamespace(ROOT=ROOT, CONTROLLER=CONTROLLER, NARVIK=focused.NARVIK)
    before, old_calls, old_scope = baseline.review.capture(a, source, location_only=True)
    after, new_calls, new_scope = baseline.review.capture(b, installed, location_only=True)
    assert old_calls == new_calls and before.keys() == after.keys()
    assert old_scope["controller"]["sha256"] == new_scope["controller"]["sha256"]
    assert old_scope["donor"] == new_scope["donor"]
    assert coordinate_proof(old_scope) == coordinate_proof(new_scope)
    arm = NdsImage.open(installed["candidate"]).read_file(build.ARM)
    font = panels.GameAsciiFont.from_arm9(arm)
    clue, = [item for item in read(build.OUT)["native_cases"] if item["index"] == focused.NARVIK]
    expected = tuple(line.strip() for line in clue["proposed"].splitlines())
    changed, unchanged, figures = None, [], []
    for frame in sorted(before):
        old, new = (panels.picture(shot[frame]) for shot in (before, after))
        bounds = ImageChops.difference(old, new).getbbox()
        if frame == RESULT:
            assert bounds and 16 <= bounds[0] < bounds[2] <= 244 and 296 <= bounds[1] < bounds[3] <= 360
            plate = panels.nameplate(font, baseline.review.MATE, new)
            assert plate == panels.nameplate(font, baseline.review.MATE, old)
            assert panels.exact_body(font, tuple(line.strip() for line in clue["previous"].splitlines()), old)
            changed = dict(frame=frame, nameplate=plate, complete_body_ink=panels.exact_body(font, expected, new),
                           native_expected_rows=expected, capture=after[frame], difference_bounds=bounds)
            figures.extend([("Narvik clue / before", old), ("Narvik clue / revised", new)])
        else:
            assert bounds is None, (frame, bounds)
            unchanged.append(frame)
    assert changed is not None and {12600, 13400, 13800} <= set(unchanged)
    draw = FunctionType(panels.sheets_for.__code__, vars(panels) | dict(OUT=OUT),
                        argdefs=panels.sheets_for.__defaults__)
    sheets = draw("paired_village_clue_replay", figures)
    write(OUT, dict(candidate_sha256=installed["candidate_sha256"], predecessor_sha256=source["candidate_sha256"],
        old=old_scope, new=new_scope, changed=changed, unchanged_frames=unchanged, sheets=sheets,
        same_message_requests=True, same_ship_writes=True, position_only_focused_gameplay=True))
    print(f"Narvik clue and its whole nameplate passed. {len(unchanged)} surrounding frames matched.")


if __name__ == "__main__":
    cli = ArgumentParser(description=__doc__)
    cli.add_argument("action", choices=("replay", "verify"))
    globals()[cli.parse_args().action]()
