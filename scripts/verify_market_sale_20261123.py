"""Review ordinary sale settlement, backtracking and the handoff to Rafael's lesson."""

import json
from pathlib import Path

from PIL import Image, ImageChops, ImageDraw
from dk4tool.dialogue.font_audit import GameAsciiFont
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.script.common_message_table import common_message_entries
from scripts import observe_market_sale_20261123 as run
from scripts import verify_genoa_copenhagen_town_20261123 as genoa
from scripts.reconcile_archived_message_selectors_20261123 import KEYS, OUT as SELECTORS
from scripts.reconcile_elegy_acceptance_20261123 import common_rows
from scripts.stage_cartridge_title_20261123 import CLEAN, GATES, REGISTRY, NdsImage, digest, read, reference, write


OUT = SELECTORS.with_name("market_sale_current_20261123.json")
SHEET = OUT.with_suffix(".png")
DECK_REVIEW = Path("releases/all_routes_editorial_20261122_rafael_deck_tutorial_candidate/verification/registered_review.json")
FRAMES = {
    13081: "Purchased Olive Oil in Cargo",
    13481: "Sale staged for 211 gold",
    13881: "Finish confirmation",
    14281: "No keeps the pending sale",
    15081: "Yes completes the sale",
    15481: "Market with proceeds",
    16281: "New purchase staged",
    16681: "Back discards the purchase",
    17081: "Julio opens the Deck lesson",
}
PANELS = {
    14: ("Sailor", "All set, then?", (13881, 14681),
         "The sailor's short check invites a decision about the pending deal and works for both buying and selling."),
    9: ("Trader", "Thanks! Come again.", (15081,),
        "The trader acknowledges the completed sale and invites the sailor to return."),
}


def checked_capture(release):
    paths = [run.ROOT / name for name in ("capture/capture_report.json", "trace/requests.json",
             "capture/navigation_command_journal.json", "terminal.json")]
    capture, trace, journal, terminal = map(read, paths)
    assert release["candidate_sha256"] == capture["ROM_sha256"] == journal["ROM_sha256"] == terminal["candidate_sha256"]
    assert terminal["ordinary_controller_inputs"] and capture["cold_boot"] and not capture["savestate_loaded"]
    assert not capture["callback_errors"] and not any(v for k, v in capture.items() if k.startswith("synthetic_"))
    donor = capture["battery_save_preloaded"]
    assert donor["copied_byte_exact_before_cold_boot"]
    assert digest(donor["source"]) == donor["source_sha256"] == terminal["copied_save_sha256"]
    commands = [json.loads(line) for line in run.CONTROLLER.read_text("utf-8").splitlines()]
    assert commands == [r["command"] for r in journal["commands_received"]] and commands[-1] == {"stop": True}
    assert all(row["validation_passed"] for row in journal["commands_received"])
    assert capture["frames"] == terminal["total_frames"] == journal["last_command_frame"] == 17081
    assert all(digest(path) == h for path, h in terminal["evidence"].items())
    assert trace["all_host_slots_restored_and_core_file_exact"] and not trace["errors"] and not trace["mismatches"]
    calls = trace["source_requests"]
    assert calls == terminal["common_requests"]
    assert [r["message_ID"] for r in calls[::2]] == [8, 14, 9, 14, 14, 9]
    assert not any(r["message_ID"] in KEYS for r in calls)
    for got, copied in zip(calls[::2], calls[1::2], strict=True):
        assert got["PC"] == 0x0205528C and copied == got | {"PC": 0x020534F4}
    return genoa.shots(capture, "_navigation.png"), calls, [reference(path) for path in paths]


def reviewed_panels(source, installed, font, calls, frames, screens):
    rows = []
    for key, (speaker, text, holds, reason) in PANELS.items():
        japanese, english = source[key], installed[key]
        assert english.text.decode("ascii").strip() == text
        evidence = []
        for frame in holds:
            got, copied = [r for r in calls if r["message_ID"] == key and 0 < frame - r["frame"] < 400]
            assert got["caller_LR"] == (0x02053D10 if key == 14 else 0x02053FF8)
            evidence.append(dict(frame=frame, requests=[got, copied], capture=frames[frame],
                body_pixels=genoa.exact_body(font, (text,), screens[frame]),
                nameplate=genoa.nameplate(font, speaker, screens[frame])))
        rows.append(dict(message_ID=key, speaker=speaker, decision="retention", localization_note=reason,
            clean_Japanese=japanese.text.decode("cp932"), source_hex=japanese.text.hex(),
            source_reference=genoa.text_reference(japanese), installed_hex=english.text.hex(),
            installed_reference=genoa.text_reference(english), review=dict.fromkeys(GATES, True), holds=evidence))
    return rows


def deck_opening(clean, image, font, frame, screen):
    assert digest(DECK_REVIEW) == read(DECK_REVIEW.parents[1] / "checksums.json")["verification/registered_review.json"]
    row, = [entry for entry in read(DECK_REVIEW)["records"] if entry["id"] == "DK4_MES_B43_R0007"]
    original, installed = [IlnkContainer.parse(rom.read_file(row["file_path"])).blocks[row["block"]] for rom in (clean, image)]
    for block, field in ((original, "source_reference"), (installed, "registered_reference")):
        entry = row[field]
        expected = bytes.fromhex(entry["complete_command_hex"])
        offset = entry["command_offset"]
        assert block[offset:offset + len(expected)] == expected and expected[:6].hex() == entry["complete_preamble_hex"]
    assert set(row["review"]) == set(GATES) and all(row["review"].values())
    lines = ("Still with me? Now let me show you", "what the crew does aboard ship.")
    assert " ".join(lines) == row["english"]
    return dict(id=row["id"], source=row["source_reference"], installed=row["registered_reference"],
        complete_native_pixels=genoa.exact_body(font, lines, screen), capture=frame,
        nameplate=genoa.nameplate(font, row["speaker"], screen), decision="retention",
        localization_note=row["localization_note"], review=row["review"], whole_exchange_evidence=reference(DECK_REVIEW))


def wallet_checks(font, screens):
    def mask(frame, text, region):
        return genoa.find_mask(font, str(text), screens[frame], region)

    checks = {}
    for frame, (funds, income, spent, net) in {
        13081: (26982, 0, 0, 26982), 13481: (26982, 211, 0, 27193),
        14281: (26982, 211, 0, 27193), 15881: (27193, 0, 0, 27193),
        16281: (27193, 0, 572, 26621),
    }.items():
        checks[frame] = dict(zip(("funds", "income", "spent", "net"),
            (mask(frame, n, (72, 38 + i * 16, 123, 53 + i * 16)) for i, n in enumerate((funds,income,spent,net))), strict=True))
    for frame in (15481, 16681):
        checks[frame] = dict(funds=mask(frame, 27193, (77, 348, 134, 364)))
    return checks


def main():
    release = read(run.current.RELEASE)
    assert digest(run.current.ROM) == release["candidate_sha256"] and digest(REGISTRY) == release["registry_sha256"]
    assert digest(CLEAN) == release["clean_input_sha256"]
    frames, calls, evidence = checked_capture(release)
    screens = {frame: genoa.picture(shot) for frame, shot in frames.items()}
    clean, rom = map(NdsImage.open, (CLEAN, release["candidate"]))
    arm = rom.read_file(run.current.ARM)
    font = GameAsciiFont.from_arm9(arm)
    source = common_message_entries(clean.read_file(run.current.COMMON), clean.read_file(run.current.ARM))
    current = common_rows(rom.read_file(run.current.COMMON), arm)
    panels = reviewed_panels(source, current, font, calls, frames, screens)
    lesson = deck_opening(clean, rom, font, frames[17081], screens[17081])
    wallet = wallet_checks(font, screens)
    no_diff = ImageChops.difference(screens[13481], screens[14281]).getbbox()
    assert no_diff is None or (no_diff[1] >= 268 and no_diff[3] <= 330), no_diff
    sheet = Image.new("RGB", (768, 1212), "#263238")
    draw = ImageDraw.Draw(sheet)
    for i, (frame, label) in enumerate(FRAMES.items()):
        x, y = i % 3 * 256, i // 3 * 404
        draw.text((x + 4, y + 3), label, fill="white")
        sheet.paste(screens[frame], (x, y + 20))
    sheet.save(SHEET)
    write(OUT, dict(candidate_sha256=release["candidate_sha256"], ordinary_controls_using_existing_save=True,
        paid_purchase=418, confirmed_sale=211, restored_after_discarding_pending_purchase=27193,
        exact_wallet_masks=wallet, returned_to_pending_sale_image_difference=no_diff, reviewed_panels=panels,
        following_deck_opening=lesson, upstream_requests=calls, watched_legacy_ids=list(KEYS),
        watched_legacy_ids_requested=[], contact_sheet=reference(SHEET), evidence=evidence,
        unvisited=["Other Market models and alternate voices", "Direct callers for the five archived records"],
        changed_ROM=False, editorial_credit_added=0))
    print("Verified the full sale, decline, settlement, cancellation and Rafael's ensuing lesson opening.")


if __name__ == "__main__":
    main()
