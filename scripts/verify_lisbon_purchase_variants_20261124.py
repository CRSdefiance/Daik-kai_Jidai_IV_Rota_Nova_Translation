"""Verify Julio's Salt deal and direct Trade Help navigation in ordinary Lisbon play."""

import json
from pathlib import Path

from PIL import Image, ImageChops, ImageDraw
from dk4tool.dialogue.font_audit import GameAsciiFont
from dk4tool.dialogue.help_source_links import source_links
from dk4tool.dialogue.review import validate_natural_dialogue_batch
from dk4tool.formats.ilnk import IlnkContainer

from scripts import observe_lisbon_purchase_variants_20261124 as play
from scripts import reconcile_help_topic_navigation_20261124 as help_scope
from scripts import verify_riga_trade_deck_20261124 as evidence
from scripts import verify_syracuse_local_purchase_20261124 as ledger
from scripts.stage_cartridge_title_20261123 import CLEAN, GATES, NdsImage, REGISTRY, digest, read, reference, write
from scripts.verify_early_HELP23_ordinary_navigation import COLORS

OUT = evidence.OUT.with_name("lisbon_salt_and_trade_help_20261124.json")
SHEET = OUT.with_suffix(".png")
END = 46700
HOLDS = (
    (15, (40700, 41500), "Julio Erneco", "Will this do?",
     "Julio politely asks whether the pending deal is acceptable.",
     "The brief, slightly formal question fits Julio. It reads as a request for approval and leaves the same deal pending when declined."),
    (9, (41900,), "Trader", "Thanks! Come again.",
     "The trader thanks the customer and invites them to come back.",
     "The trader's friendly farewell fits after the Salt purchase is settled."),
)


def check_report(release):
    capture = play.ROOT / "capture/capture_report.json"
    journal = capture.with_name("navigation_command_journal.json")
    report, commands = map(read, (capture, journal))
    reference_capture = read(play.BOOK)["evidence"]["capture"]
    assert digest(reference_capture["path"]) == reference_capture["sha256"]
    former = read(reference_capture["path"])
    assert report["ROM_sha256"] == commands["ROM_sha256"] == release["candidate_sha256"]
    assert report["frames"] == commands["last_command_frame"] == END
    assert report["cold_boot"] and not report["savestate_loaded"] and not report["callback_errors"]
    assert not any(value for key, value in report.items() if key.startswith("synthetic_"))
    assert list(map(json.loads, play.CONTROLLER.read_text("utf-8").splitlines())) == list(play.ACTIONS)
    assert list(play.ACTIONS) == [r["command"] for r in commands["commands_received"]]
    assert all(r["validation_passed"] for r in commands["commands_received"])
    assert report["scripted_input_schedule"][:len(former["scripted_input_schedule"])] == former["scripted_input_schedule"]
    donor = report["battery_save_preloaded"]
    assert donor["copied_byte_exact_before_cold_boot"] and digest(donor["source"]) == donor["source_sha256"]
    assert donor["source_sha256"] == former["battery_save_preloaded"]["source_sha256"]
    panels = evidence.panels
    last = panels.shots(former, "_navigation.png")[play.PAUSE]
    frames = panels.shots(report, "_navigation.png")
    assert frames[play.PAUSE]["framebuffer_sha256"] == last["framebuffer_sha256"]
    return frames, list(map(reference, (capture, journal, donor["source"], play.BOOK, play.CONTROLLER)))


def exact_help(font, raw, image):
    cursor, text, links = 0, "", source_links(raw)
    for link in links:
        text += raw[cursor:link["start"]].decode("ascii") + link["label"]
        cursor = link["end"]
    text += raw[cursor:].rstrip(b"\0").decode("ascii")
    lines = text.rstrip("\n").split("\n")
    expected = set()
    for row, line in enumerate(lines):
        y = 192 if row == 0 else 216 + (row - 1) * 16
        assert len(line.rstrip()) <= 42 and y <= 344
        for col, char in enumerate(line):
            glyph = font.decode(char)
            expected.update((col * 6 + x, y + yy + 1) for yy in range(11) for x in range(6)
                            if glyph.getpixel((x, yy)))
    actual = {(x, y) for y in range(192, 356) for x in range(252) if image.getpixel((x, y)) in COLORS}
    assert actual == expected, (next(iter(expected - actual), None), next(iter(actual - expected), None))
    return dict(native_ink_pixels=len(actual), complete_lines=lines, exact_visible_pixels=True,
                stored_links=[r["topic_id"] for r in links])


def validate(release, frames, refs):
    clean, image = map(NdsImage.open, (CLEAN, play.current.ROM))
    a, b = (rom.read_file(play.current.ARM) for rom in (clean, image))
    path = play.current.COMMON
    clean_rows = evidence.base.common_message_entries(clean.read_file(path), a)
    new_rows = evidence.base.common_rows(image.read_file(path), b)
    font = GameAsciiFont.from_arm9(b)
    panels = evidence.panels
    screens = {frame: panels.picture(shot) for frame, shot in frames.items()}
    records = []
    for key, sample, speaker, text, gloss, rationale in HOLDS:
        source, installed = clean_rows[key], new_rows[key]
        assert installed.text.decode("ascii").strip() == text
        assert b"%" not in source.text and b"%" not in installed.text
        checks = [dict(frame=frames[frame], body=panels.exact_body(font, (text,), screens[frame]),
                      nameplate=panels.nameplate(font, speaker, screens[frame])) for frame in sample]
        records.append(dict(id=f"COMMON_MESSAGE_{key}", message_ID=key, file_path=path, speaker=speaker,
            english=text, clean_Japanese=source.text.decode("cp932"), source_meaning=gloss,
            context="Julio and the Trader handle a 577-gold Salt purchase after an earlier Olive Oil concession.",
            localization_note=rationale, decision="retention", review=dict.fromkeys(GATES, True),
            source_reference=evidence.source_ref(source), installed_reference=evidence.source_ref(installed),
            current_reference=evidence.source_ref(installed), holds=checks))

    assert screens[40300].tobytes() == screens[41100].tobytes()
    confirmation_difference = ImageChops.difference(screens[40700], screens[41500]).getbbox()
    assert confirmation_difference == (146, 284, 174, 288)
    assert screens[42700].tobytes() == screens[END].tobytes()
    values = {37700: (26995, 0, 0, 26995), 40300: (26995, 0, 577, 26418),
              41100: (26995, 0, 577, 26418), END: (26418, 0, 0, 26418)}
    balances = {f: ledger.exact_ledger(font, screens[f], row) for f, row in values.items()}
    assert 26995 - 577 == 26418
    choices = {frame: [panels.find_mask(font, label, screens[frame], rect) for label, rect in (
                  ("No", (118, 360, 165, 376)), ("Yes", (188, 360, 235, 376)))]
               for frame in (40700, 41500)}
    help_archive = image.read_file(help_scope.HELP)
    pages = IlnkContainer.parse(help_archive).blocks
    page_inventory = read(help_scope.OUT)
    assert page_inventory["candidate_sha256"] == release["candidate_sha256"]
    page_frames = {43100: 22, 44700: 22, 45100: 212, 45500: 22, 45900: 212, 46300: 22}
    help_result = []
    for frame, key in page_frames.items():
        result = exact_help(font, pages[key], screens[frame])
        exact = page_inventory["records"][key]
        assert exact["source_article"] == 22 and exact["installed"]["exact_hex"] == pages[key].hex()
        assert result["stored_links"] == exact["outgoing_links"]
        help_result.append(dict(page=key, capture=frames[frame], review_binding=exact, **result))
    assert screens[45100].tobytes() == screens[45900].tobytes()
    assert screens[45500].tobytes() == screens[46300].tobytes()
    assert screens[43100].crop((0,192,256,356)).tobytes() == screens[45500].crop((0,192,256,356)).tobytes()

    labels = ((38500, "Salt purchase staged"), (40700, "Julio asks for approval"), (41900, "Trader acknowledges payment"),
              (43100, "Select opens Trade Help"), (45100, "Trade continuation"), (END, "Help returns to the same Trade screen"))
    sheet = Image.new("RGB", (768, 808), "#263238")
    titles = ImageDraw.Draw(sheet)
    for i, (frame, title) in enumerate(labels):
        x, y = i % 3 * 256, i // 3 * 404
        titles.text((x + 3, y + 4), title, fill="white")
        sheet.paste(screens[frame], (x, y + 20))
    sheet.save(SHEET)
    result = dict(translation_policy="natural-dialogue-v2", encoder="dialogue-relocatable-v1", target_locale="en-US",
        review_gates=list(GATES), records=records, clean_rom_sha256=release["clean_input_sha256"],
        candidate_sha256=release["candidate_sha256"], ordinary_gameplay=True, fixture_or_state_load=False,
        original_lisbon_checkpoint_matches=True, settled_salt_cost=577, decline_kept_same_pending_deal=True,
        affirmative_choice_settled_quoted_price=True, balances=balances, choices=choices,
        confirmation_difference_in_background=confirmation_difference,
        Help_direct_trade_article=22, Help_linked_continuation=212, Help_holds=help_result,
        Help_article_body_after_history_matches=True, Help_exit_returns_exact_trade_frame=True,
        evidence=refs + [reference(play.current.RELEASE), reference(help_scope.OUT)], contact_sheet=reference(SHEET),
        unvisited=["Double-price stock offer", "Other native request IDs outside displayed text",
                   "Help slot 205 through other direct opens", "Physical hardware"],
        ROM_changed=False, new_editorial_credit=0)
    validate_natural_dialogue_batch(result)
    return result


def main():
    release = read(play.current.RELEASE)
    assert digest(REGISTRY) == release["registry_sha256"] and digest(CLEAN) == release["clean_input_sha256"]
    assert digest(play.current.ROM) == release["candidate_sha256"]
    frames, refs = check_report(release)
    write(OUT, validate(release, frames, refs))
    print("Verified both Salt purchase choices, the 577-gold settlement and six direct Trade Help holds.")


if __name__ == "__main__":
    main()
