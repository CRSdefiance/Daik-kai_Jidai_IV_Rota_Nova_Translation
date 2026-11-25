"""Stage and pair the source-reviewed Tunis Palace refusal."""

from argparse import ArgumentParser
from inspect import getsource
from pathlib import Path
from types import FunctionType

from PIL import ImageChops

from scripts import preflight_tunis_palace_refusal_20261124 as review
from scripts import stage_tunis_shop_advice_20261124 as previous
from scripts.source_locked_derivation_v5118 import checked_text
from scripts.stage_cartridge_title_20261123 import NdsImage, digest, read, reference, write


trend, panels, played, KEY, END = review.trend, review.panels, review.played, review.KEY, review.END
ROOT = Path("E:/Rota Nova translations/Generated/work/editorial_20261124_tunis_palace_refusal")
ROM, STORED = ROOT / "Tunis_Palace_Refusal_STAGED.nds", ROOT / "stored_proof.json"
BEFORE = played.ROOT / "capture/capture_report.json"
AFTER = ROOT / "replay/capture/capture_report.json"
PATCH, REBUILT, PATCH_PROOF = (ROOT / name for name in ("translation.xdelta", "clean_rebuilt.nds", "clean_patch_proof.json"))
STARTUP_CAPTURE = ROOT / "startup/capture/capture_report.json"
PAIRED = ROOT / "paired_gameplay.json"
SHEET = ROOT / "paired_tunis_palace_refusal_1_20261123.png"


def stage():
    assert ROOT.parent.exists()
    source = checked_text(getsource(previous.stage), {
        '== 124': '== 2',
    })
    scope = vars(previous) | globals()
    exec(compile(source, __file__ + "::source-locked-COMMON-stage", "exec"), scope)
    scope["stage"]()


def verify(stored):
    old, new, preflight = map(read, (BEFORE, AFTER, review.OUT))
    assert digest(ROM) == stored["candidate_sha256"] == new["ROM_sha256"]
    assert old["ROM_sha256"] == stored["predecessor_sha256"] == preflight["candidate_sha256"]
    assert new["cold_boot"] and not new["savestate_loaded"] and not new["callback_errors"]
    assert not any(value for label, value in new.items() if label.startswith("synthetic_"))
    assert new["frames"] == END and new["scripted_input_schedule"] == old["scripted_input_schedule"]
    assert new["battery_save_preloaded"]["source_sha256"] == old["battery_save_preloaded"]["source_sha256"]
    previous_frames = panels.shots(old, "_navigation.png")
    revised_frames = {row["frame"]: row for row in new["frames_captured"] if row["frame"] in previous_frames}
    assert previous_frames.keys() == revised_frames.keys()
    font = review.GameAsciiFont.from_arm9(NdsImage.open(ROM).read_file(trend.ARM))
    native, = [row for row in preflight["native_cases"] if row["label"] == "Proposed"]
    unchanged, changed, figures = [], [], []
    for frame in sorted(previous_frames):
        a, b = (panels.picture(group[frame]) for group in (previous_frames, revised_frames))
        bounds = ImageChops.difference(a, b).getbbox()
        if frame not in review.REVISED_HOLDS:
            assert bounds is None, (frame, bounds)
            unchanged.append(frame)
            continue
        assert bounds and 16 <= bounds[0] < bounds[2] <= 250 and 296 <= bounds[1] < bounds[3] <= 360
        name = panels.nameplate(font, "Guard", b)
        assert name == panels.nameplate(font, "Guard", a)
        ink = panels.exact_body(font, native["layout"]["lines"], b)
        changed.append(dict(frame=frame, capture=revised_frames[frame], complete_body_ink=ink, nameplate=name, bounds=bounds))
        figures.extend(((f"Previous / {frame}", a), (f"Revised / {frame}", b)))
    assert len(changed) == 2 and {8600, 9400, 14600, 15400, 15800, END} <= set(unchanged)
    sheets = FunctionType(panels.sheets_for.__code__, vars(panels) | {"OUT": PAIRED},
                          argdefs=panels.sheets_for.__defaults__)
    sheet, = sheets("paired_tunis_palace_refusal", figures)
    assert sheet == reference(SHEET)
    write(PAIRED, dict(candidate_sha256=stored["candidate_sha256"], predecessor_sha256=stored["predecessor_sha256"],
        before=reference(BEFORE), after=reference(AFTER), stored=reference(STORED), dialogue_holds=changed,
        unchanged_frames=unchanged, ordinary_saved_game=True, sheets=[sheet]))
    print(f"Verified both revised Guard holds and {len(unchanged)} pixel-identical gameplay holds.")


if __name__ == "__main__":
    cli = ArgumentParser(description=__doc__)
    cli.add_argument("action", choices=("stage", "replay", "verify", "patch", "startup"))
    action = cli.parse_args().action
    if action == "stage":
        stage()
    elif action == "verify":
        verify(read(STORED))
    else:
        dependent = (previous.replay if action == "replay" else previous.release_check).__code__
        args = [read(STORED)] if action == "replay" else [read(STORED), action]
        FunctionType(dependent, vars(previous) | globals())(*args)
