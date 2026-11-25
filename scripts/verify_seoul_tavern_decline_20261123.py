"""Verify Reika's original No branch, its complete glyphs, and the town return."""

from pathlib import Path
from struct import unpack_from

from PIL import Image, ImageDraw

from dk4tool.dialogue.font_audit import GameAsciiFont
from dk4tool.script.common_message_table import common_message_entries
from scripts.observe_seoul_tavern_decline_20261123 import HISTORY, RELEASE, ROOT
from scripts.stage_azores_wording_20261123 import ARM, COMMON, common_rows, digest_bytes
from scripts.stage_cartridge_title_20261123 import CLEAN, NdsImage, digest, read, reference, write
from scripts.verify_captain_biographies_v1 import captured
from scripts.verify_confirmed_name_widget_pixels_v198 import complete_mask
from scripts.verify_lisbon_azores_voyage_20261123 import body_mask, text_at
from scripts.verify_personal_gameplay_v841 import get_machine
from scripts.verify_special_target_battle_20261123 import message_reference
from scripts.verify_stock_encounter_names_20261121 import read_ram


OUT = Path("translations/editorial_checkpoints/shared_display_20261123/seoul_tavern_decline_20261123.json")
SHEET = OUT.with_suffix(".png")
HOLD = {15130: (59, "How about one more drink?", "The friendly invitation opens the original Yes and No choices."),
        15350: (826, "Oh, can't handle another drink?", "The teasing question keeps Reika's mild surprise at the refusal.")}
CONTROLS = (9230, 9530, 14330, 15130, 15560, 15770, 15980)


def frame_map(report):
    return {r["frame"]: r for r in report["frames_captured"] if not r["path"].endswith("_final.png")}


def cash_state(arm, snapshot):
    raw = read_ram(snapshot)
    _, get = get_machine(arm, raw)
    companies = get(0xCB160)
    current_company = get(0x397D8, companies)
    return get(0x7F244), current_company, get(0x3CCC8, companies + 4 + current_company * 76)


def main():
    baseline, release = map(read, (HISTORY, RELEASE))
    path, terminal = ROOT / "capture/capture_report.json", ROOT / "terminal.json"
    run, end = map(read, (path, terminal))
    assert run["ROM_sha256"] == end["candidate_sha256"] == release["candidate_sha256"] == digest(release["candidate"])
    assert run["frames"] == end["total_frames"] == 15980 and run["cold_boot"] and not run["savestate_loaded"]
    assert not run["callback_errors"] and not any(v for k, v in run.items() if k.startswith("synthetic_"))
    assert end["ordinary_controller_inputs"] and all(digest(p) == h for p, h in end["evidence"].items() if not p.endswith(".py"))
    donor = run["battery_save_preloaded"]
    assert donor["copied_byte_exact_before_cold_boot"] and digest(donor["source"]) == end["copied_save_sha256"]
    assert baseline["battery_save_preloaded"]["source_sha256"] == donor["source_sha256"]
    assert run["scripted_input_schedule"][:len(baseline["scripted_input_schedule"])] == baseline["scripted_input_schedule"]
    frames, earlier_frames = map(frame_map, (run, baseline))
    for n in CONTROLS[:4]:
        assert captured(frames[n]).tobytes() == captured(earlier_frames[n]).tobytes()
    original, current = map(NdsImage.open, (CLEAN, release["candidate"]))
    assert digest(CLEAN) == release["clean_input_sha256"]
    arm = current.read_file(ARM)
    assert digest_bytes(arm) == release["target_ARM9_sha256"]
    source = common_message_entries(original.read_file(COMMON), original.read_file(ARM))
    installed = common_rows(current.read_file(COMMON), arm)
    assert source[826].text.decode("cp932") == "あら、意外と弱いのね"
    assert source[59].text.decode("cp932") == "さあ、もう１杯召し上がって"
    font = GameAsciiFont.from_arm9(arm)
    snapshots = {s["frame"]: s for s in run["read_only_pause_RAM_snapshots"]}
    samples = {}
    before = cash_state(arm, snapshots[15130])
    for n in (15350, *CONTROLS[-3:]):
        assert cash_state(arm, snapshots[n]) == before
    assert before[0] == 3 and before[2] == 38781
    for frame, (key, line, note) in HOLD.items():
        jp, en = source[key], installed[key]
        assert b"%" not in jp.text and en.text.decode("ascii").strip() == line
        raw = read_ram(snapshots[frame])
        rendered = text_at(raw, unpack_from("<I", raw, 0x54450)[0])
        assert rendered.decode("ascii").strip() == line and b"\n" not in rendered
        rgb = captured(frames[frame])
        ink, bounds = complete_mask(font, "Reika", rgb, 16, 277, (98, 97, 98))
        proof = body_mask(font, rgb, (line,))
        assert not any(c == (0, 8, 0) for c in rgb.crop((16, 345, 245, 360)).get_flattened_data())
        a, b = [call for call in end["common_requests"] if call["message_ID"] == key and frame - 200 <= call["frame"] < frame]
        assert (a["PC"], b["PC"]) == (0x0205528C, 0x020534F4) and dict(a, PC=b["PC"]) == b
        samples[key] = dict(clean=message_reference(jp), installed=message_reference(en), English=line,
            Japanese=jp.text.decode("cp932"), speaker="Reika", capture=frames[frame], read_only_state=snapshots[frame],
            original_COMMON_calls=[a, b], complete_body=proof, complete_nameplate=dict(pixels=ink, bounds=bounds),
            decision="retain", reason=note, review=dict(source=True, context=True, localization=True, naturalness=True, formatting=True))
    commands = read(ROOT / "capture/navigation_command_journal.json")["commands_received"]
    assert commands[0]["frame"] == 15130 and commands[0]["command"]["buttons"] == ["B"]
    assert all(command["validation_passed"] for command in commands)
    assert all(call["message_ID"] == 826 for call in end["common_requests"] if call["frame"] > 15130)
    image = Image.new("RGB", (1040, 782), "#263238")
    draw = ImageDraw.Draw(image)
    for i, (frame, caption) in enumerate(((15130, "Another drink?"), (15350, "Reika after No"),
                                         (15560, "Tavern menu"), (15770, "Seoul town return"))):
        x, y = 5 + i % 2 * 520, i // 2 * 390
        draw.text((x, y + 5), caption, fill="white")
        crop = captured(frames[frame]).crop((0, 192, 256, 384))
        image.paste(crop.resize((480, 360), Image.Resampling.NEAREST), (x, y + 22))
    image.save(SHEET)
    write(OUT, dict(candidate_sha256=release["candidate_sha256"], release=reference(RELEASE),
                    capture=reference(path), terminal=reference(terminal), donor=reference(donor["source"]),
                    witnessed_on_current_registered_ROM=True, ordinary_gameplay=True, exact_previous_control_frames=CONTROLS[:4],
                    transition_frames={n: frames[n] for n in CONTROLS[-3:]}, no_extra_drink_purchased=True,
                    gold_unchanged=before[2], records=samples, sheet=reference(SHEET),
                    new_editorial_credit=0, full_goal_complete=False))


if __name__ == "__main__":
    main()
