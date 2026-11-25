"""Verify all Lil ceramics panels and the original return in paired emulator runs."""

from PIL import Image, ImageChops, ImageDraw

from scripts import replay_hamburg_ceramics_cross_route_20261120 as replay
from scripts import verify_hamburg_ceramics_cross_route_20261120 as offline
from scripts.replay_lil_ceramics_wrap_20261111 import body_masks, masks, photos


base, build, ROOT = replay.base, replay.build, replay.ROOT
PROOF, SHEET = ROOT / "gameplay.json", ROOT / "comparison.png"


def main():
    assert not PROOF.exists() and not SHEET.exists()
    setup, display, draft = map(base.load, (replay.SETUP, offline.PROOF, build.review.OUTPUT))
    paths = [build.ROOT.with_name("research") / "emulator/before/capture_report.json",
             ROOT / "after/capture_report.json"]
    reports = [base.load(path) for path in paths]
    prior_setup = base.load(paths[0].parents[1] / "fixture_receipt.json")
    assert prior_setup["fixture_ROMs"]["before"]["sha256"] == setup["fixture_ROMs"]["before"]["sha256"]
    schedule = base.load(ROOT / "inputs.json")
    for side, report in zip(("before", "after"), reports, strict=True):
        receipt = setup["fixture_ROMs"][side]
        assert report["ROM_sha256"] == receipt["sha256"] == base.digest(receipt["path"])
        assert report["cold_boot"] and report["frames"] == setup["end"] and not report["savestate_loaded"]
        assert not report.get("battery_save_preloaded") and not report["callback_errors"]
        assert not any(value for key, value in report.items() if key.startswith("synthetic_"))
        assert report["scripted_input_schedule"] == schedule
    assert reports[0]["core_DLL_sha256"] == reports[1]["core_DLL_sha256"]
    assert reports[0]["core_options"] == reports[1]["core_options"]

    prior, current = map(photos, reports)
    route_path = "/data/SC2.DK4"
    rows = [r for r in draft["records"] if r["file_path"] == route_path]
    receipts = {r["id"]: r for r in display["receipts"] if r["file_path"] == route_path}
    output = []
    for row, frame in zip(rows, setup["representative_frames"], strict=True):
        before, old = prior[frame]
        after, new = current[frame]
        ident = row["id"]
        difference = ImageChops.difference(old, new)
        change = difference.crop((0, 0, 256, 360)).getbbox()
        advance = difference.crop((0, 360, 256, 384)).getbbox()
        assert advance is None or advance == (224, 0, 240, 16), (ident, advance)
        if row["decision"] == "revision":
            assert change and 16 <= change[0] < change[2] <= 232 and 296 <= change[1] < change[3] <= 360, (ident, change)
            page, = receipts[ident]["pages"]
            assert body_masks(new) == masks(bytes.fromhex(page["native_plane_hex"])), (ident, frame)
        else:
            assert change is None, (ident, frame, change)
        output.append(dict(id=ident, frame=frame, before=before, after=after, change=change,
                           advance_prompt_phase_differs=advance is not None))
    matches = (2100, 7030, 7270, 7520)
    assert all(ImageChops.difference(prior[f][1], current[f][1]).getbbox() is None for f in matches)
    panels = (0, 3, 6, 11, 12, 16)
    width, height = 472, 153
    contact = Image.new("RGB", (width * 2, height * len(panels)), "#242932")
    draw = ImageDraw.Draw(contact)
    for line, index in enumerate(panels):
        frame = output[index]["frame"]
        for column, (status, source) in enumerate((("Before", prior), ("After", current))):
            x, y = width * column + 6, height * line
            draw.text((x, y + 4), f"{status} / line {index + 1}", fill="white")
            crop = source[frame][1].crop((12, 294, 244, 360))
            contact.paste(crop.resize((464, 132), Image.Resampling.NEAREST), (x, y + 17))
    contact.save(SHEET)
    hashes = {str(p): base.digest(p) for p in (replay.SETUP, offline.PROOF, *paths)}
    base.save(PROOF, dict(candidate_sha256=setup["candidate_sha256"], parent_sha256=setup["parent_sha256"],
        matched=output, observed_revisions=sum(row["change"] is not None for row in output),
        exact_early_and_return_frames=list(matches), initialized_scene=True, natural_Hamburg_activation=False,
        hardware=False, sheet={str(SHEET): base.digest(SHEET)}, evidence=hashes))
    print("All 17 Lil ceramics panels and the original return passed.")


if __name__ == "__main__":
    main()
