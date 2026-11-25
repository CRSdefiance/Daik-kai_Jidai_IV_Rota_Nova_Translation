"""Verify Supply Ratio after ordinary sailing, redocking and choosing Resupply."""

from pathlib import Path
from struct import unpack, unpack_from

from PIL import Image, ImageDraw

from dk4tool.dialogue.font_audit import GameAsciiFont
from dk4tool.script.common_message_table import common_message_entries
from scripts.check_tavern_round_digits_20261120 import wallet
from scripts.inventory_native_common_calls import direct_bl_target
from scripts.reconcile_editorial_acceptance_20261123 import ARM, BASE, COMMON, OUT
from scripts.reconcile_elegy_acceptance_20261123 import common_rows
from scripts.register_recruitment_shortfall_20261123 import RELEASE
from scripts.stage_cartridge_title_20261123 import CLEAN, REGISTRY, NdsImage, digest, read, reference, write
from scripts.stage_supply_ratio_hint_20261123 import ENGLISH, SLOT, SOURCE
from scripts.verify_azores_return_20261123 import picture, shots
from scripts.verify_confirmed_name_widget_pixels_v198 import complete_mask
from scripts.verify_lisbon_azores_voyage_20261123 import body_mask, load_exact, text_at, town
from scripts.verify_personal_gameplay_v841 import get_machine
from scripts.verify_plaque_release_v247 import find_mask


ROOT = Path(".codex-release-work/shared_display_20261123/ordinary_supply_mix")
CAPTURE = ROOT / "capture/capture_report.json"
REPORT = OUT.with_name("ordinary_supply_mix_20261123.json")
SHEET = REPORT.with_suffix(".png")
MIX_REVIEW = Path("releases/all_routes_editorial_20261123_supply_ratio_hint_candidate/verification/registered_review.json")
SCRATCH = 0x02450000
STOCKS = {13000: (150, 150), 13900: (150, 150), 14025: (146, 146), 14175: (139, 138),
          14540: (128, 127), 15140: (128, 127), 16540: (128, 127), 17420: (128, 127), 17650: (147, 153)}
PANELS = {14540: (65, ("Istanbul",), "Charles Rochefort", "The direct question preserves the selected town and the choice to dock."),
          15140: (49, ("46",), "Port Worker", "The direct refill offer keeps the exact price in ordinary digits."),
          15400: (817, (), "Port Worker", "The concise question connects the food and water mix to the offered controls."),
          16540: (49, ("46",), "Port Worker", "Cancelling returns to the original quote with the same amount."),
          16760: (817, (), "Port Worker", "The worker offers the same adjustment when the player declines the quote again."),
          17420: (49, ("52",), "Port Worker", "The updated original price uses the same clear offer after accepting the new ratio.")}
SLIDER = {15660: (50, 50), 15880: (49, 51), 16100: (50, 50), 16320: (49, 51),
          16980: (50, 50), 17200: (49, 51)}


def archived_arm(arm):
    assert arm[SLOT:SLOT + len(ENGLISH)] == ENGLISH
    dismount, adjust = 0x020609EC, 0x02060500
    assert direct_bl_target(unpack_from("<I", arm, dismount - BASE)[0], dismount) == 0x020604D0
    assert direct_bl_target(unpack_from("<I", arm, adjust - BASE)[0], adjust) == 0x02086354
    assert unpack_from("<I", arm, 0x60510)[0] == 817
    assert unpack_from("<I", arm, 0x11980C)[0] == BASE + SLOT


def fleet_state(arm, after):
    cpu, get = get_machine(arm, after)
    fleet = get(0xCB1A8) + 4 + 132 * get(0x2E58C)
    get(0x34EB0, fleet, SCRATCH)
    supplies = unpack("<2I", cpu.mem_read(SCRATCH, 8))
    assert bytes(cpu.mem_read(BASE, len(after))) == after
    return dict(water_food=list(supplies), gold=wallet(arm, after), native_fleet=fleet)


def main():
    release, capture, terminal = map(read, (RELEASE, CAPTURE, ROOT / "terminal.json"))
    assert release["registry_sha256"] == digest(REGISTRY)
    assert capture["ROM_sha256"] == release["candidate_sha256"] == digest(release["candidate"])
    assert terminal["candidate_sha256"] == release["candidate_sha256"]
    assert capture["cold_boot"] and not capture["savestate_loaded"] and not capture["callback_errors"]
    assert not any(value for key, value in capture.items() if key.startswith("synthetic_"))
    assert terminal["ordinary_controller_inputs"] and capture["frames"] == terminal["total_frames"] == 17650
    donor = capture["battery_save_preloaded"]
    assert donor["copied_byte_exact_before_cold_boot"] and digest(donor["source"]) == donor["source_sha256"]
    assert all(digest(path) == sha for path, sha in terminal["evidence"].items())
    assert digest(CLEAN) == release["clean_input_sha256"]
    current, clean = map(NdsImage.open, (release["candidate"], CLEAN))
    arm, original = current.read_file(ARM), clean.read_file(ARM)
    assert original[SLOT:SLOT + len(SOURCE)] == SOURCE
    archived_arm(arm)
    font = GameAsciiFont.from_arm9(arm)
    previous, installed = common_message_entries(clean.read_file(COMMON), original), common_rows(current.read_file(COMMON), arm)
    frames = shots(capture, "navigation.png")
    rams = {r["frame"]: r for r in capture["read_only_pause_RAM_snapshots"]}
    states, dialogues, sliders = [], [], []
    for frame, expected in STOCKS.items():
        state = fleet_state(arm, load_exact(rams[frame]))
        assert tuple(state["water_food"]) == expected
        assert state["gold"] == (8089 if frame == 17650 else 8141)
        states.append(state | dict(frame=frame, snapshot=rams[frame]))
    assert len({s["native_fleet"] for s in states}) == 1
    requests = terminal["common_requests"]
    prior = 14470
    for frame, (key, arguments, speaker, reason) in PANELS.items():
        row = installed[key]
        calls = [r for r in requests if r["message_ID"] == key and prior < r["frame"] < frame]
        assert [r["PC"] for r in calls] == [0x0205528C, 0x020534F4] and dict(calls[0], PC=calls[1]["PC"]) == calls[1]
        assert calls[0]["caller_LR"] == (0x02053D10 if key == 65 else 0x02053FB0)
        prior = frame
        expected = (row.text.rstrip() % tuple(arg.encode("ascii") for arg in arguments)).strip()
        snapshot = load_exact(rams[frame])
        rendered = text_at(snapshot, unpack_from("<I", arm, 0x54450)[0])
        assert rendered.split() == expected.split()
        panel = picture(frames[frame])
        lines = tuple(line.strip() for line in rendered.decode("ascii").split("\n"))
        ink = body_mask(font, panel, lines)
        complete_mask(font, speaker, panel, 16, 277, (98, 97, 98))
        src = previous[key]
        assert src.text.count(b"%s") == row.text.count(b"%s") == len(arguments)
        dialogues.append(dict(message_ID=key, frame=frame, lines=lines, substitutions=arguments, speaker=speaker,
            source_Japanese=src.text.decode("cp932"), source_reference=town.reference(src), exact_source_hex=src.text.hex(),
            installed_reference=town.reference(row), exact_installed_hex=row.text.hex(), full_glyphs=ink,
            calls=calls, decision="retention", reason=reason, review=dict(source=True, context=True,
                localization=True, naturalness=True, formatting=True)))
    panel_crops = {}
    for frame, shares in SLIDER.items():
        panel = picture(frames[frame])
        mix = find_mask(font, "Mix", panel, (87, 366, 151, 384))
        assert mix["bounds"] == [131, 371, 149, 382] and mix["ink_pixels"] == 49
        back = find_mask(font, "Back", panel, (149, 367, 204, 384))
        select = find_mask(font, "Select", panel, (198, 367, 256, 384))
        heading = find_mask(font, "Supply Ratio", panel, (50, 264, 133, 286))
        panel_crops[frame] = panel.crop((30, 284, 153, 322)).tobytes()
        sliders.append(dict(frame=frame, water_food_percent=shares, exact_labels=[heading, mix, back, select]))
    assert panel_crops[15660] == panel_crops[16100] == panel_crops[16980]
    assert panel_crops[15880] == panel_crops[16320] == panel_crops[17200] != panel_crops[15660]

    holds = ((13900, "Depart Istanbul full"), (14540, "Redock after using supplies"), (15140, "Original refill quote"),
             (15400, "Decline to open the mix question"), (15660, "First opening at 50/50"), (15880, "L selects 49/51"),
             (16980, "Cancel and reopen at 50/50"), (17420, "Apply and see the new quote"), (17650, "Refill and Port return"))
    contact = Image.new("RGB", (3 * 268, 3 * 218), "#28313b")
    labels = ImageDraw.Draw(contact)
    for i, (frame, label) in enumerate(holds):
        x, y = 268 * (i % 3) + 6, 218 * (i // 3)
        labels.text((x, y + 6), label, fill="white")
        contact.paste(picture(frames[frame]).crop((0, 192, 256, 384)), (x, y + 22))
    contact.save(SHEET)
    write(REPORT, dict(candidate_sha256=release["candidate_sha256"], registered_release=reference(RELEASE),
        full_ordinary_voyage_and_consumption=True, started_from_existing_battery_save=True, fixture=False,
        records=dialogues, slider_frames=sliders, state_timeline=states, source_amounts_and_settlement_exact=True,
        source_hint_review=reference(MIX_REVIEW), hint_reference=dict(file=ARM, offset=SLOT, clean_hex=SOURCE.hex(),
        installed_hex=ENGLISH.hex(), decision="retention", reason="Mix describes the adjustment and matches the worker's question."),
        evidence=[reference(p) for p in (CAPTURE, ROOT / "terminal.json", SHEET)],
        selected_screens=[frames[frame] for frame, _ in holds], hardware=False, new_editorial_credit=0))
    print("Verified ordinary consumption, both ratio exits, every label and the exact refill and settlement.")


if __name__ == "__main__":
    main()
