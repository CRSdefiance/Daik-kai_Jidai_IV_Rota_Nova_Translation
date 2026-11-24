"""Compare both original Tavern flows with a matched one-field setup."""

from struct import unpack_from

from PIL import Image, ImageChops, ImageDraw

from dk4tool.dialogue.font_audit import GameAsciiFont
from scripts import replay_recruitment_shortfall_20261123 as playback
from scripts import stage_recruitment_shortfall_20261123 as stage
from scripts.check_tavern_round_digits_20261120 import capture_ram, wallet
from scripts.reconcile_editorial_acceptance_20261123 import OUT
from scripts.stage_cartridge_title_20261123 import NdsImage, digest, read, reference, write
from scripts.verify_azores_return_20261123 import picture, shots
from scripts.verify_confirmed_name_widget_pixels_v198 import complete_mask
from scripts.verify_lisbon_azores_voyage_20261123 import body_mask, load_exact, text_at
from scripts.verify_plaque_release_v247 import find_mask


REPORT = OUT.with_name("recruitment_shortfall_gameplay_20261123.json")
SHEET = REPORT.with_suffix(".png")
HOLD, KEY = 18080, 1041
NAME, COUNT = "Manuel Almeida", 12


def main():
    parent, proof = map(read, (stage.parent.RELEASE, stage.PROOF))
    original, candidate = parent["candidate_sha256"], proof["candidate_sha256"]
    assert digest(parent["candidate"]) == original == proof["verified_predecessor_sha256"]
    assert digest(stage.ROM) == candidate
    base, modified = map(NdsImage.open, (parent["candidate"], stage.ROM))
    arm = base.read_file(stage.ARM)
    assert arm == modified.read_file(stage.ARM)
    font = GameAsciiFont.from_arm9(arm)
    installer = stage.capacity.recruitment.catalogue
    tables = [installer(arm, image.read_file(stage.COMMON)) for image in (base, modified)]
    paths = [playback.PLAY / name / "capture/capture_report.json" for name in ("current", "revised")]
    reports = [read(path) for path in paths]
    schedule, _, end, _, donor = playback.capacity.schedule("azores")
    setup = playback.setup(parent["target_ARM9_sha256"])
    frames, evidence, panels = [], [], []
    fixture_models = []
    for record, sha, table in zip(reports, (original, candidate), tables, strict=True):
        assert record["ROM_sha256"] == sha and record["frames"] == end
        assert record["core_DLL_sha256"] == reports[0]["core_DLL_sha256"] and record["core_options"] == reports[0]["core_options"]
        assert record["cold_boot"] and not record["savestate_loaded"] and not record["callback_errors"]
        assert record["scripted_input_schedule"] == schedule
        assert record["exact_requested_capture_frames"] == list(playback.FRAMES)
        assert record["battery_save_preloaded"]["source_sha256"] == donor["source_sha256"] == digest(donor["source"])
        assert not any(value for key, value in record.items() if key.startswith("synthetic_") and key != "synthetic_condition_fixtures")
        snap, = [row for row in record["read_only_pause_RAM_snapshots"] if row["frame"] == playback.PAUSE]
        raw = load_exact(snap)
        _, fixture = setup(arm, raw, playback.REQUEST)
        assert record["synthetic_condition_fixtures"] == [fixture | dict(frame=playback.PAUSE)]
        assert fixture["crew_before"] == 39 and fixture["crew_after"] == 9 and fixture["required_crew_unchanged"] == 39
        assert len(fixture["changes"]) == 1
        fixture_models.append(fixture)
        capture = shots(record, "cold_boot.png")
        frames.append(capture)
        held = picture(capture[HOLD])
        panels.append(held)
        expected = table[KEY].text % str(COUNT).encode("ascii")
        held_ref, held_ram = capture_ram(record, HOLD)
        source, rendered = (text_at(held_ram, unpack_from("<I", arm, at)[0]) for at in (0x5444C, 0x54450))
        assert source.rstrip() == expected.rstrip() and rendered.split() == expected.split()
        lines = tuple(line.strip() for line in rendered.decode("ascii").split("\n"))
        glyphs = body_mask(font, held, lines)
        complete_mask(font, NAME, held, 16, 277, (98, 97, 98))
        end_ref, end_ram = capture_ram(record, playback.END)
        funds = [wallet(arm, data) for data in (raw, held_ram, end_ram)]
        assert funds == [39333, 38633, 38633]
        returned = find_mask(font, "Assign Sailors", picture(capture[playback.END]), (50, 0, 205, 19))
        evidence.append(dict(ROM_sha256=sha, lines=lines, rendered_hex=rendered.hex(), speaker=NAME,
                            full_glyphs=glyphs, balances=funds, transition=returned,
                            held_snapshot=held_ref, return_snapshot=end_ref))
    hashes = {"before_RAM_sha256", "after_RAM_sha256"}
    comparable = [{key: value for key, value in fixture.items() if key not in hashes} for fixture in fixture_models]
    assert comparable[0] == comparable[1]
    assert evidence[0]["lines"] == ("We're still 12 short. Shall I keep", "recruiting?")
    assert evidence[1]["lines"] == ("We're 12 short on crew. Shall I", "recruit more?")
    difference = ImageChops.difference(*panels).getbbox()
    assert difference and 16 <= difference[0] < difference[2] <= 244 and 295 <= difference[1] < difference[3] <= 360
    unchanged = [n for n in playback.FRAMES if n != HOLD]
    assert all(frames[0][n]["framebuffer_sha256"] == frames[1][n]["framebuffer_sha256"] for n in unchanged)
    view = (("Original shortfall", panels[0]), ("Revised shortfall", panels[1]),
            ("Assign Sailors after declining", picture(frames[1][playback.END])))
    sheet = Image.new("RGB", (3 * 268, 410), "#28313b")
    title = ImageDraw.Draw(sheet)
    for i, (label, panel) in enumerate(view):
        title.text((268 * i + 6, 4), label, fill="white")
        sheet.paste(panel, (268 * i + 6, 22))
    sheet.save(SHEET)
    write(REPORT, dict(candidate_sha256=candidate, previous_sha256=original, message_ID=KEY, live_shortfall=COUNT,
        fixture=fixture_models[0], revised_fixture=fixture_models[1], ordinary_actions_after_fixture=True, natural_crew_loss_observed=False,
        hardware=False, pages=evidence, changes_only_in_body=difference, unchanged_frames=unchanged,
        unvisited_revised_voice=1039, capture_reports=[reference(path) for path in paths], screenshot=reference(SHEET)))
    print("Verified the complete 12-sailor shortfall prompt, original controls and the Assign Sailors transition.")


if __name__ == "__main__":
    main()
