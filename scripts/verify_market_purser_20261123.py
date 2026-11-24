"""Bind the focused Lisbon concession to clean source, full glyphs and settlement."""

from pathlib import Path
from struct import unpack_from

from PIL import Image, ImageDraw

from dk4tool.dialogue.font_audit import GameAsciiFont
from dk4tool.script.common_message_table import common_message_entries
from scripts import observe_market_purser_20261123 as replay
from scripts.check_tavern_round_digits_20261120 import wallet
from scripts.reconcile_elegy_acceptance_20261123 import common_rows
from scripts.reconcile_editorial_acceptance_20261123 import ARM, COMMON, OUT
from scripts.stage_cartridge_title_20261123 import CLEAN, REGISTRY, NdsImage, digest, read, reference, write
from scripts.verify_azores_return_20261123 import picture, shots
from scripts.verify_confirmed_name_widget_pixels_v198 import complete_mask
from scripts.verify_lisbon_azores_voyage_20261123 import body_mask, load_exact, town


REPORT = OUT.with_name("market_purser_current_20261123.json")
EARLIER = OUT.with_name("market_exit_current_20261123.json")
SHEET = REPORT.with_suffix(".png")
PRIOR = Path("releases/all_routes_editorial_20261120_market_bargaining_candidate/verification/registered_review.json")
PANELS = {
    11881: (15, "Julio Erneco", "The slightly formal question suits Julio and leaves the purchase decision with Rafael."),
    12281: (24, "Julio Erneco", "The polite opening suits Julio. The price already on screen makes the object of his request clear."),
    12681: (10, "Trader", "The trader relents and grants a small concession, which the original settlement actually applies."),
}


def main():
    folder = replay.ROOT / replay.CASE
    cap_path = folder / "capture/capture_report.json"
    fixture_path, trace_path, terminal_path = (folder / p for p in ("purser_fixture.json", "requests.json", "terminal.json"))
    capture, fixture, trace, terminal = map(read, (cap_path, fixture_path, trace_path, terminal_path))
    release = read(replay.RELEASE)
    assert release["registry_sha256"] == digest(REGISTRY) and release["clean_input_sha256"] == digest(CLEAN)
    assert capture["ROM_sha256"] == terminal["ROM_sha256"] == release["candidate_sha256"] == digest(release["candidate"])
    assert capture["cold_boot"] and not capture["savestate_loaded"] and not capture["callback_errors"]
    assert not any(value for key, value in capture.items() if key.startswith("synthetic_"))
    events, frames, end, _, donor = replay.schedule(replay.CASE)
    assert capture["scripted_input_schedule"] == events and capture["exact_requested_capture_frames"] == list(frames)
    assert capture["frames"] == terminal["completed_frames"] == end
    save = capture["battery_save_preloaded"]
    assert save["copied_byte_exact_before_cold_boot"] and save["source_sha256"] == donor["source_sha256"] == digest(donor["source"])
    assert all(digest(path) == sha for path, sha in terminal["evidence"].items())
    assert trace["all_host_slots_restored_and_core_file_exact"] and not trace["errors"] and not trace["mismatches"]
    assert [state["PC"] for state in trace["rows"]] == [replay.DISCOUNT_CALL, replay.ROLL_CHECK, replay.PRICE_RETURN]
    started, roll, price = [state["registers"] for state in trace["rows"]]
    assert started[3:5] == [replay.ACTOR, 418] and roll[0] == 3 < roll[6] == 27 and price[0] == 1
    assert [state["frame"] for state in trace["rows"]] == [12024] * 3

    calls = trace["source_requests"]
    assert calls == terminal["target_COMMON_calls"] and len(calls) == 8
    assert [got["message_ID"] for got in calls[::2]] == [8, 15, 24, 10]
    for got, copied in zip(calls[::2], calls[1::2], strict=True):
        assert got["PC"] == 0x0205528C and copied == got | {"PC": 0x020534F4}
    assert [got["caller_LR"] for got in calls[::2]] == [0x02053FF8, 0x02053D10, 0x02053DA4, 0x02053FF8]

    clean, current = map(NdsImage.open, (CLEAN, release["candidate"]))
    ja, arm = clean.read_file(ARM), current.read_file(ARM)
    source = common_message_entries(clean.read_file(COMMON), ja)
    installed = common_rows(current.read_file(COMMON), arm)
    reviewed = {row["message_ID"]: row for row in read(PRIOR)["records"]}
    assert all(arm[lo:hi] == ja[lo:hi] for lo, hi in replay.SPANS if (lo, hi) != (0xBB3C4, 0xBC3A4))
    assert unpack_from("<8I", arm, 0x118A80) == tuple(range(19, 27))
    assert unpack_from("<8I", arm, 0x118AA0) == (11, 0xFFFFFFFF, 12, 13, 14, 15, 16, 17)

    font = GameAsciiFont.from_arm9(arm)
    held = shots(capture, "_cold_boot.png")
    snapshots = {r["frame"]: r for r in capture["read_only_capture_RAM_snapshots"]}
    assert fixture["frame"] == replay.BEFORE_FINISH and [(r["before"], r["after"]) for r in fixture["changes"]] == [(24, 20), (208, 6)]
    assert snapshots[replay.BEFORE_FINISH]["sha256"] == fixture["before_sha256"]
    expected_wallets = {frame: (27400 if frame < 12281 else 26995) for frame in frames}
    wallets = {}
    for frame, expected in expected_wallets.items():
        actual = wallet(arm, load_exact(snapshots[frame]))
        assert actual == expected, (frame, actual)
        wallets[frame] = actual

    displayed, records = {}, []
    for frame, (key, speaker, reason) in PANELS.items():
        row, old, decision = installed[key], source[key], reviewed[key]
        assert decision["source_hex"] == old.text.hex() and decision["source_reference"] == town.reference(old)
        assert all(decision["review"].values())
        lines = [line.strip() for line in row.text.decode("ascii").splitlines()]
        assert " ".join(lines) == decision["english"] and 1 <= len(lines) <= 3
        displayed[frame] = panel = picture(held[frame])
        ink = body_mask(font, panel, lines)
        name = complete_mask(font, speaker, panel, 16, 277, (98, 97, 98))
        records.append(dict(message_ID=key, source_reference=town.reference(old), installed_reference=town.reference(row),
            source_Japanese=old.text.decode("cp932"), source_hex=old.text.hex(), installed_hex=row.text.hex(),
            lines=lines, speaker=speaker, speaker_complete_ink=name[0], frame=frame, full_body_glyphs=ink,
            decision="retention", reason=reason, review=decision["review"], screenshot=held[frame]))
    assert records[1]["lines"] == ["Sorry to trouble you, but could you", "do a bit better?"]
    returned = picture(held[13081])
    menu = []
    for label, x, y in (("Trade", 113, 263), ("Invest", 110, 283), ("Market Info", 95, 303)):
        ink, bounds = complete_mask(font, label, returned, x, y, (8, 8, 8))
        menu.append(dict(text=label, bounds=bounds, ink_pixels=ink))
    sheet = Image.new("RGB", (4 * 268, 226), "#273034")
    draw = ImageDraw.Draw(sheet)
    for i, (frame, title) in enumerate(zip((*PANELS, 13081), ("Confirm trade", "Julio bargains", "Trader concedes", "Return to Market"), strict=True)):
        draw.text((i * 268 + 6, 4), title, fill="white")
        panel = displayed.get(frame, returned)
        sheet.paste(panel.crop((0, 192, 256, 384)), (i * 268 + 6, 26))
    sheet.save(SHEET)

    archived = read(EARLIER)["reviewed_entries"]
    for row in archived:
        key = row["message_ID"]
        assert key in (750, 751, 752) and key not in [call["message_ID"] for call in calls]
        assert row["source_reference"] == town.reference(source[key]) and row["source_hex"] == source[key].text.hex()
        assert row["installed_reference"] == town.reference(installed[key]) and row["installed_hex"] == installed[key].text.hex()

    write(REPORT, dict(candidate_sha256=release["candidate_sha256"], focused_emulator_gameplay=True,
        fixture_scope="Two bytes equip one existing empty room as a Purser's Office and assign Julio before Finish.",
        original_inputs=True, original_random_roll=3, success_threshold=27, quote_gold=418, paid_gold=405,
        wallet_timeline=wallets, original_market_return_labels=menu, records=records,
        archived_keys_with_exact_prior_source_and_installed_bindings=[r["message_ID"] for r in archived],
        archived_keys_direct_caller_still_open=True, native_request_pairs=calls, native_discount_trace=trace["rows"],
        replay_fixture=fixture, hardware=False, new_editorial_credit=0,
        evidence=[reference(path) for path in (replay.RELEASE, PRIOR, EARLIER, cap_path, fixture_path, trace_path, terminal_path, SHEET)]))
    print("Verified Julio's complete confirmation, bargaining request, concession, exact charge and Market return.")


if __name__ == "__main__":
    main()
