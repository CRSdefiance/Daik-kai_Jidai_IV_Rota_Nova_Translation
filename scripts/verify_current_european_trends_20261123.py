"""Check all current London and Athens story panels and natural event completion."""

from pathlib import Path
from types import SimpleNamespace

from PIL import Image, ImageDraw

from dk4tool.dialogue.font_audit import GameAsciiFont
from scripts.reconcile_town_trend_catalogue_20261123 import OUT as CATALOGUE, verification
from scripts.replay_current_european_trends_20261123 import CASES, RELEASE, ROOT, details
from scripts.stage_azores_wording_20261123 import ARM, digest_bytes
from scripts.stage_cartridge_title_20261123 import CLEAN, NdsImage, digest, read, reference, write
from scripts.verify_captain_biographies_v1 import captured
from scripts.verify_confirmed_name_widget_pixels_v198 import complete_mask
from scripts.verify_european_trends_gameplay_20261121 import CASES as PLANS, previous, town
from scripts.verify_moonlit_violin_20261121 import bytes_for
from dk4tool.formats.ilnk import IlnkContainer


OUT = CATALOGUE.with_name("european_trends_current_gameplay_20261123.json")
TEXT = verification("20261123_hodram_late_story_wraps") / "registered_review.json"
STORY, EVENT = "/data/SC1.DK4", "/data/EV1.DK4"


def images(rows):
    return {row["frame"]: row for row in rows if not row["path"].endswith("_final.png")}


def sheet(case, panels):
    versions = 2
    result = Image.new("RGB", (520 * versions, 240 * ((len(panels) + 1) // versions)), "#263238")
    draw = ImageDraw.Draw(result)
    for i, (label, frame) in enumerate(panels):
        x, y = i % versions * 520 + 4, i // versions * 240 + 4
        draw.text((x, y + 3), label, fill="white")
        crop = frame.crop((0, 269, 256, 376)).resize((512, 214), Image.Resampling.NEAREST)
        result.paste(crop, (x, y + 18))
    path = OUT.with_name(f"{case}_trend_current_20261123.png")
    result.save(path)
    return reference(path)


def check_case(city, release, ctx, clean, installed, events, pane, notice, font):
    history, earlier, controls, holds, donor = details(city)
    path = ROOT / city / "capture/capture_report.json"
    report = read(path)
    plan = PLANS[city]
    assert report["ROM_sha256"] == release["candidate_sha256"] and report["frames"] == plan["returned"]
    assert report["cold_boot"] and not report["savestate_loaded"] and not report["callback_errors"]
    assert not any(v for k, v in report.items() if k.startswith("synthetic_"))
    assert report["scripted_input_schedule"] == earlier["scripted_input_schedule"]
    assert report["battery_save_preloaded"]["source_sha256"] == donor["source_sha256"] == digest(donor["source"])
    event, = [row for row in read(CATALOGUE)["records"] if row["route"] == 1 and row["English"].lower() == city]
    assert event["original_event"]["script_block"] == plan["block"]
    completion = previous.event_completion(ctx.arm, report, events, event["original_event"], plan)
    block = installed[plan["block"]]
    source = clean[plan["block"]]
    assert digest_bytes(block) == event["installed_block_sha256"]
    assert digest_bytes(source) == event["original_event"]["prior_review"]["clean_block_sha256"]
    records = {row["id"]: row for row in read(TEXT)["records"]
               if row.get("file_path") == STORY and row["block"] == plan["block"]}
    assert records.keys() == set(holds.values())
    earlier_frames, frames = (images(r["frames_captured"]) for r in (earlier, report))
    evidence, panels = [], []
    kanji = ctx.image.read_file("/GRP/KANJI.FNT")
    for frame, ident in holds.items():
        row = records[ident]
        assert all(row["review"].values())
        ref = row["registered_reference"]
        raw, at = bytes.fromhex(ref["exact_command_hex"]), ref["command_offset"]
        assert block[at:at+len(raw)] == raw and ref["block_sha256"] == digest_bytes(block)
        body = bytes_for(raw)
        if raw[5] == 254:
            result = notice(body)
            plane, width = result["physical"], 228
        else:
            result = pane(ctx.arm, kanji, body)
            one, = result["pages"]
            assert one["native_independent_plane_equal"]
            plane, width = bytes.fromhex(one["native_plane_hex"]), 216
        assert result["complete_consumed_bytes"] == len(body)
        picture = captured(frames[frame])
        assert previous.mask_check(plane, width, picture), (city, frame, ident)
        header = None
        if raw[5] != 254:
            assert raw[5] in (166,167,168)
            header = complete_mask(font, "Lady", picture, 16, 277, town.INKS[1])
        evidence.append(dict(id=ident, frame=frames[frame], exact_installed_command=ref, source_reference=row["source_reference"],
                             English=row["english"], speaker=row["speaker"], complete_mask=digest_bytes(plane),
                             complete_nameplate=header, editorial_decision=row["decision"], review=row["review"]))
        panels.append((ident, picture))
    comparison = {}
    for kind, frame in controls.items():
        old, new = (captured(group[frame]) for group in (earlier_frames, frames))
        comparison[kind] = dict(frame=frames[frame], previous=earlier_frames[frame], exact_pixels=old.tobytes() == new.tobytes())
    assert comparison["returned"]["exact_pixels"]
    panels.append(("Return to the Square", captured(frames[controls["returned"]])))
    return dict(capture=reference(path), older_capture=reference(history), sealed_gameplay_inputs=reference(ROOT / city / "identical_inputs.json"),
                donor=reference(donor["source"]), original_event_completed=completion, same_return_to_Square=True,
                panels=evidence, original_control_frames=comparison, sheet=sheet(city, panels))


def main():
    release = read(RELEASE)
    assert digest(release["candidate"]) == release["candidate_sha256"]
    original, current = [NdsImage.open(p) for p in (CLEAN, release["candidate"])]
    clean, installed = [IlnkContainer.parse(rom.read_file(STORY)).blocks for rom in (original, current)]
    events = current.read_file(EVENT)
    assert events == original.read_file(EVENT)
    arm = current.read_file(ARM)
    assert digest_bytes(arm) == release["target_ARM9_sha256"]
    ctx = SimpleNamespace(image=current, arm=arm)
    pane, notice = town.clipped_renderer(ctx), town.current_fe_painter(ctx)
    font = GameAsciiFont.from_arm9(arm)
    outcomes = {city: check_case(city, release, ctx, clean, installed, events, pane, notice, font) for city in CASES}
    count = sum(len(run["panels"]) for run in outcomes.values())
    assert count == 18
    write(OUT, dict(registered_release=reference(RELEASE), candidate_sha256=release["candidate_sha256"],
                    exact_town_catalogue=reference(CATALOGUE), current_contextual_review=reference(TEXT), city_runs=outcomes,
                    complete_current_panels=count, fresh_ordinary_activations=2, room_fixture=False,
                    handheld=False, new_editorial_credit=0, full_goal_complete=False))
    print("Both ordinary activations, 18 current dialogue panels, and both Square returns passed.")


if __name__ == "__main__":
    main()
