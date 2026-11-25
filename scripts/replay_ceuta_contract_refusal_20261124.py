"""Stage the exact previewed Market refusal and replay Ceuta up through dismissal."""

from argparse import ArgumentParser
from pathlib import Path
import sys

from PIL import Image, ImageChops, ImageDraw

from dk4tool.dialogue.font_audit import GameAsciiFont
from scripts import headless_desmume_v193 as harness
from scripts import observe_ceuta_town_20261124 as ordinary
from scripts import preflight_ceuta_contract_refusal_20261124 as draft
from scripts.stage_cartridge_title_20261123 import NdsImage, digest, read, reference, sha256, write


ROOT = draft.ROOT
ROM = ROOT / "Ceuta_Contract_Refusal_STAGED.nds"
STORED = ROOT / "stored_proof.json"
OUT = draft.OUT.with_name("ceuta_contract_refusal_paired_20261124.json")
OLD = ordinary.ROOT / "capture/capture_report.json"
CAPTURE = ROOT / "paired/capture_report.json"
HOLD = 4650
HOLDS = (3400, 3700, 4050, 4350, HOLD, 4950, 5250)
panels = draft.evidence.panels


def stage(visual_sha):
    preflight = read(draft.OUT)
    startup = read(ordinary.current.RELEASE)
    assert preflight["parent_candidate_sha256"] == startup["candidate_sha256"] == digest(ordinary.current.ROM)
    view = preflight["native_preview"]
    assert digest(view["path"]) == view["sha256"] == visual_sha and preflight["offline_only"]
    image = NdsImage.open(ordinary.current.ROM)
    arm, common = [image.read_file(path) for path in (ordinary.current.ARM, ordinary.current.COMMON)]
    records = draft.native.owned_entries(common, arm, draft.digest_range(arm))
    body = b" " + draft.DRAFT.encode("ascii")
    target, _, slots = draft.native.owned_deployment(common, arm, records, {draft.KEY: body})
    assert slots[draft.KEY] == preflight["one_owned_allocation"]
    assert sha256(target).hexdigest() == preflight["proposed_COMMON_sha256"]
    old_files = draft.native.files(image)
    image.replace_file(ordinary.current.COMMON, target)
    new_files = draft.native.files(image)
    assert old_files.keys() == new_files.keys()
    assert {key for key in old_files if old_files[key] != new_files[key]} == {ordinary.current.COMMON}
    result = bytes(image.rom.save())
    image.replace_file(ordinary.current.COMMON, common)
    assert sha256(image.rom.save()).hexdigest() == startup["candidate_sha256"]
    with ROM.open("xb") as stream:
        stream.write(result)
    write(STORED, dict(candidate=reference(ROM), previous=reference(ordinary.current.ROM), reviewed_preview=view,
                       target_COMMON_sha256=preflight["proposed_COMMON_sha256"], only_message=draft.KEY,
                       exact_complete_parent_inverse=True, registered=False))


def replay():
    staged = read(STORED)
    assert digest(ROM) == staged["candidate"]["sha256"]
    report = read(OLD)
    assert report["cold_boot"] and not report["savestate_loaded"]
    assert report["ROM_sha256"] == staged["previous"]["sha256"]
    donor = report["battery_save_preloaded"]
    assert digest(donor["source"]) == donor["source_sha256"]
    plan = ROOT / "paired_inputs.json"
    write(plan, [row for row in report["scripted_input_schedule"] if row["start"] <= HOLDS[-1]])
    original = sys.argv
    try:
        sys.argv = [__file__, "--rom", str(ROM), "--out", str(CAPTURE.parent), "--frames", str(HOLDS[-1]),
                    "--inputs-json", str(plan), "--press-start", "-1", "--touchscreen", "--battery-save", donor["source"],
                    "--capture-every", "999999", "--capture-at", *map(str, HOLDS)]
        harness.main()
    finally:
        sys.argv = original
    assert digest(donor["source"]) == donor["source_sha256"]


def verify():
    parent, changed, stored = map(read, (OLD, CAPTURE, STORED))
    assert changed["ROM_sha256"] == stored["candidate"]["sha256"] == digest(ROM)
    assert parent["ROM_sha256"] == stored["previous"]["sha256"]
    assert changed["cold_boot"] and not changed["savestate_loaded"] and not changed["callback_errors"]
    assert not any(value for key, value in changed.items() if key.startswith("synthetic_"))
    old_save, new_save = (report["battery_save_preloaded"] for report in (parent, changed))
    assert new_save["copied_byte_exact_before_cold_boot"]
    assert digest(old_save["source"]) == old_save["source_sha256"] == new_save["source_sha256"]
    assert [row for row in parent["scripted_input_schedule"] if row["start"] <= HOLDS[-1]] == changed["scripted_input_schedule"]
    before = panels.shots(parent, "_navigation.png")
    after = panels.shots(changed, "_cold_boot.png")
    companion = [frame for frame in HOLDS if frame != HOLD]
    assert all(before[f]["framebuffer_sha256"] == after[f]["framebuffer_sha256"] for f in companion)
    old, new = (panels.picture(row[HOLD]) for row in (before, after))
    diff = ImageChops.difference(old, new).getbbox()
    assert diff and 16 <= diff[0] < diff[2] <= 245 and 296 <= diff[1] < diff[3] <= 360
    font = GameAsciiFont.from_arm9(NdsImage.open(ROM).read_file(ordinary.current.ARM))
    body = panels.exact_body(font, draft.EXPECTED["Governor's Office"], new)
    nameplate = panels.nameplate(font, "Trader", new)
    paper = Image.new("RGB", (512, 404), "#263238")
    titles = ImageDraw.Draw(paper)
    for i, (screen, label) in enumerate(((old, "Registered Ceuta refusal"), (new, "Proposed Ceuta refusal"))):
        x = i * 256
        titles.text((x + 4, 4), label, fill="white")
        paper.paste(screen, (x, 20))
    sheet = OUT.with_suffix(".png")
    paper.save(sheet)
    write(OUT, dict(candidate=stored["candidate"], installed_predecessor=stored["previous"],
        ordinary_gameplay=True, revised_frame=after[HOLD], former_frame=before[HOLD],
        revised_message=draft.KEY, full_body_pixels=body, full_nameplate=nameplate, difference_box=diff,
        matching_companion_frames=companion, exact_complete_parent_inverse=True, contact_sheet=reference(sheet),
        reviewed_native_preflight=reference(draft.OUT), stored_proof=reference(STORED), captures=list(map(reference, (OLD, CAPTURE))),
        registered=False, hardware_tested=False))
    print("Verified the complete staged Governor's Office refusal, nameplate and six exact companion frames.")


if __name__ == "__main__":
    cli = ArgumentParser(description=__doc__)
    cli.add_argument("--visual-sha", required=True)
    stage(cli.parse_args().visual_sha)
    replay()
    verify()
