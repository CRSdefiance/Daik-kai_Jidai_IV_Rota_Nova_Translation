"""Bind the verified Purser help proposal to the actual staged Refit screen."""

import json

from PIL import Image, ImageChops, ImageDraw

from dk4tool.dialogue.font_audit import GameAsciiFont
from scripts import replay_lisbon_purser_refit_20261124 as play
from scripts import verify_lisbon_stock_quota_20261124 as quota
from scripts.stage_cartridge_title_20261123 import NdsImage, digest, read, reference, sha256, write


OUT = quota.OUT.with_name("lisbon_purser_refit_paired_20261124.json")
HOLD = 43400
BODY = (63, 77, 233, 112)


def main():
    staged, terminal, draft = map(read, (play.STAGED, play.ROOT / "paired_terminal.json", play.draft.OUT))
    assert terminal["candidate"] == reference(play.ROM) and staged["candidate_sha256"] == digest(play.ROM)
    assert staged["exact_parent_inverse"] and staged["proposal"] == reference(play.draft.OUT)
    for key in ("original_capture", "candidate_capture", "controller", "source"):
        assert reference(terminal[key]["path"]) == terminal[key]
    prior, live = [read(terminal[key]["path"]) for key in ("original_capture", "candidate_capture")]
    for report in (prior, live):
        assert report["cold_boot"] and not report["savestate_loaded"] and not report["callback_errors"]
    assert live["frames"] == terminal["frames"] == play.STOP_AT
    assert live["ROM_sha256"] == staged["candidate_sha256"] and prior["ROM_sha256"] == draft["candidate_sha256"]
    actions = list(map(json.loads, (play.CAPTURE / "controller.jsonl").read_text("utf-8").splitlines()))
    journal = read(play.CAPTURE / "capture/navigation_command_journal.json")
    assert actions == [r["command"] for r in journal["commands_received"]] and actions[-1] == {"stop": True}
    assert all(row["validation_passed"] for row in journal["commands_received"])
    assert live["scripted_input_schedule"] == prior["scripted_input_schedule"][:len(live["scripted_input_schedule"])]
    donor, old_donor = (report["battery_save_preloaded"] for report in (live, prior))
    assert donor["source_sha256"] == old_donor["source_sha256"] == digest(donor["source"])
    a, b = (report["synthetic_market_finance_prerequisite"][0] for report in (live, prior))
    assert {k: v for k, v in a.items() if not k.startswith("full_RAM_")} == {
        k: v for k, v in b.items() if not k.startswith("full_RAM_")}
    panels = quota.panels
    old, new = [panels.shots(report, "_navigation.png") for report in (prior, live)]
    assert new.keys() == {n for n in old if n <= play.STOP_AT}
    matching = [n for n in new if n != HOLD]
    assert all(old[n]["framebuffer_sha256"] == new[n]["framebuffer_sha256"] for n in matching)
    before, after = (panels.picture(frames[HOLD]) for frames in (old, new))
    delta = ImageChops.difference(before, after)
    bounds = delta.getbbox()
    assert bounds is not None
    delta.paste((0, 0, 0), BODY)
    assert delta.getbbox() is None
    rom = NdsImage.open(play.ROM)
    current = play.play.current
    arm, raw = (rom.read_file(name) for name in (current.ARM, current.COMMON))
    assert sha256(arm).hexdigest() == staged["target_ARM9_sha256"]
    assert sha256(raw).hexdigest() == draft["proposed_COMMON_sha256"]
    font = GameAsciiFont.from_arm9(arm)
    text = quota.scope.base.common_rows(raw, arm)[play.draft.KEY]
    assert quota.scope.source_ref(text) == draft["record"]["proposed_reference"]
    lines = text.text.decode("ascii").splitlines()
    masks = [panels.find_mask(font, line, after, (60, 76 + 12 * i, 236, 94 + 12 * i)) for i, line in enumerate(lines)]
    title = panels.find_mask(font, "Purser", after, (59, 27, 236, 50))
    image = Image.new("RGB", (512, 404), "#263238")
    draw = ImageDraw.Draw(image)
    for i, (label, scene) in enumerate((("Registered Ceuta", before), ("Staged Purser help", after))):
        draw.text((i * 256 + 4, 3), label, fill="white")
        image.paste(scene, (i * 256, 20))
    path = OUT.with_suffix(".png")
    image.save(path)
    write(OUT, dict(candidate=terminal["candidate"], fixture_scope="Finance prerequisite only. Refit used normal controller inputs.",
        source_review=reference(play.draft.OUT), actual_parent_hold=old[HOLD], revised_hold=new[HOLD], lines=lines,
        exact_masks=masks, title_mask=title, difference_box=bounds, matching_navigation_frames=matching,
        sheet=reference(path), terminal=reference(play.ROOT / "paired_terminal.json"), full_goal_complete=False))
    print(f"Verified the revised Purser help hold with {len(matching)} exact companion screens.")


if __name__ == "__main__":
    main()
