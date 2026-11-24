"""Bind the current Genoa and Copenhagen gameplay to clean and installed text."""

import json
from collections import Counter
from hashlib import sha256
from pathlib import Path
from types import FunctionType, SimpleNamespace

from PIL import Image, ImageDraw

from dk4tool.dialogue.font_audit import GameAsciiFont
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.script.common_message_table import common_message_entries
from scripts import observe_genoa_copenhagen_town_20261123 as observed
from scripts import register_price_info_descriptions_20261123 as active
from scripts.reconcile_elegy_acceptance_20261123 import common_rows
from scripts.reconcile_town_trend_catalogue_20261123 import OUT as CATALOGUE, verification
from scripts.review_current_story_wraps_20261122 import display as story_display, layout
from scripts.seal_shared_text_source_v1 import reference as text_reference
from scripts.stage_cartridge_title_20261123 import CLEAN, GATES, REGISTRY, NdsImage, digest, read, reference, write
from scripts.verify_azores_return_20261123 import picture, shots
from scripts.verify_confirmed_name_widget_pixels_v198 import complete_mask
from scripts.verify_lisbon_seoul_trend_gameplay_20261121 import mask_check, town
from scripts.verify_moonlit_violin_20261121 import bytes_for
from scripts.verify_plaque_release_v247 import find_mask
from scripts.verify_regional_ui_v616 import glyphs


OUT = CATALOGUE.with_name("genoa_copenhagen_current_20261123.json")
STORY = "/data/SC1.DK4"
TREND = verification("20261123_hodram_late_story_wraps") / "registered_review.json"
JULIO = verification("20261122_tavern_and_proof_exchanges") / "registered_review.json"
CHOICES = verification("20261122_hodram_B161_B170") / "registered_review.json"
STORY_FRAMES = {
    181: dict(zip((6, 9, 12, 16, 20, 23, 27, 30, 34, 37), range(3800, 5601, 200), strict=True)),
    170: dict(zip(
        (5, 9, 13, 16, 21, 25, 29, 33, 37, 40, 44, 48, 51, 54, 57, 61, 65, 68, 72,
         86, 90, 94, 98, 101, 105, 109, 125, 128, 145, 149, 153, 157, 160, 164, 168, 172),
        (*range(9700, 13301, 200), *range(13700, 14901, 200), *range(15300, 16501, 200), 16800, 17100, 17350),
        strict=True,
    )),
}
CHOICE_FRAMES = {894: (13500, 830), 1314: (15100, 1194)}
GAPS = {
    (170, 90): ("I'm no connoisseur. I only know what it sells for.", ("what it sells for.",),
                "Hodram distinguishes his knowledge of liquor prices from knowing much about liquor itself. Keep that contrast without a separate short line for the trade qualification."),
    (170, 125): ("Straight to the point. I like that.", ("Straight to the point.",),
                 "Julio approves of Hodram's frank approach. Make the approving reply sound spoken and preserve the contrast with the test branch."),
    (181, 12): (None, ("It's the color of passion.", "Ah, it takes me back to my youth.", "I was madly in love."),
                "Keep the owner's dramatic reminiscence and move the interjection Ah with the recollection it introduces."),
}
COMMON = {
    341: ("", "The join notice immediately confirms the outcome without repeating the conversation."),
    51: ("Barkeep", "The short welcome gives the player the floor before the order menu."),
    53: ("Barkeep", "The drink price stays at the original five coins in the compact quote."),
    55: ("Barkeep", "The call identifies Matilda and the waiting customer in the barkeep's voice."),
    56: ("Matilda", "The brief acknowledgment answers the barkeep directly."),
    59: ("Matilda", "Matilda offers a second drink casually and leaves the choice to the player."),
    61: ("Barkeep", "The independent second-round quote preserves the original ten coins."),
    657: ("Shopkeeper", "Keep the entire short question with its tag before the advice for bulk trade."),
    658: ("Shopkeeper", "The hesitant answer and hope for a good deal keep the original tone."),
    712: ("Shopkeeper", "Preserve that the new Swedish naval fleet supports itself through both trade and privateering."),
    715: ("Shopkeeper", "The remembered trading reach and the metaphor for owning the Mediterranean both fit the rumor."),
    730: ("Shopkeeper", "The first forecast picks the Food category without naming a specific product."),
    731: ("Shopkeeper", "The second shopkeeper names the selected Tomato good as a personal prediction."),
    821: ("Barkeep", "Keep the pirate's name, home city, occupation and influence as separate facts."),
    827: ("Matilda", "Matilda repeats the player's name and makes the toast to getting acquainted."),
    858: ("Manuel Almeida", "The careful question preserves an estimated cost and asks before committing the gold."),
    865: ("Hodram Bergstrom", "The quick public instruction invites everyone present to drink."),
    872: ("Barkeep", "Announce who is paying, then invite the room to enjoy the round. The original optional gendered address stays available to the caller under the existing argument binding."),
    874: ("Patron", "The patron answers with surprise and enthusiastic gratitude."),
    880: ("Patron", "The phrasing conveys secondhand news and identifies both the commander and the destination."),
}
HOLDS = {
    "genoa": {
        6600: (730, ("Food",), ("Something in the Food market is", "sure to catch on soon.")),
        7200: (731, ("Tomato",), ("I think Tomato will sell well.",)),
        7800: (715, (), ("Back then, the Centurione Company", "traded far and wide. Their ships",
                         "sailed all over the Mediterranean,", "as if they owned it.")),
        17600: (341, ("Julio Erneco",), ("Julio Erneco joined!",)),
        17850: (51, (), ("Welcome! What will you have?",)),
        18300: (53, (), ("5 coins.",)),
        18500: (821, ("Hayreddin", "Alexandria", "pirate"), ("Hayreddin from Alexandria is", "a pirate with real pull here.")),
        18700: (55, ("Matilda",), ("Hey, Matilda! We've got a customer!",)),
        18900: (56, (), ("On it!",)),
        19100: (59, (), ("How about one more drink?",)),
        19300: (61, (), ("Ten coins.",)),
        19500: (827, ("Hodram",), ("Hodram, huh? Cheers! Glad we met.",)),
    },
    "copenhagen": {
        4300: (657, (), ("You're a sailor, aren't you?", "Try the Market for bulk trade.")),
        4900: (658, (), ("Business? Oh, it's been all right.", "I'm hoping a good deal comes along.")),
        5500: (712, (), ("They say Sweden's new naval fleet", "makes a point of paying its own way", "through trade and privateering.")),
        6600: (51, (), ("Welcome! What will you have?",)),
        7200: (858, ("236",), ("Would it be all right to spend", "about 236 gold?")),
        7400: (865, (), ("Drinks for everyone!",)),
        7600: (872, ("Bergstrom",), ("This round's on Bergstrom. Enjoy!",)),
        7800: (874, (), ("Whoa! Really? Thanks for the round!", "Mighty generous of you!")),
        8000: (880, ("Clifford", "London"), ("Word is, Clifford has a fleet", "heading to London.")),
        8400: (53, (), ("5 coins.",)),
        8800: (53, (), ("5 coins.",)),
    },
}


def capture(city, release):
    root = observed.ROOT / city
    run_path, journal_path, trace_path, terminal_path = [root / path for path in (
        "capture/capture_report.json", "capture/navigation_command_journal.json", "trace/requests.json", "terminal.json")]
    report, journal, trace, terminal = map(read, (run_path, journal_path, trace_path, terminal_path))
    assert report["ROM_sha256"] == terminal["candidate_sha256"] == journal["ROM_sha256"] == release["candidate_sha256"]
    assert terminal["ordinary_controller_inputs"] and report["cold_boot"] and not report["savestate_loaded"]
    assert not report["callback_errors"] and not any(v for k, v in report.items() if k.startswith("synthetic_"))
    commands = [json.loads(line) for line in (root / "controller.jsonl").read_text("utf-8").splitlines()]
    assert [r["command"] for r in journal["commands_received"]] == commands and commands[-1] == {"stop": True}
    assert all(r["validation_passed"] for r in journal["commands_received"])
    assert journal["last_command_frame"] == terminal["total_frames"] == report["frames"]
    assert all(digest(path) == sha for path, sha in terminal["evidence"].items())
    donor = report["battery_save_preloaded"]
    assert donor["copied_byte_exact_before_cold_boot"]
    assert digest(donor["source"]) == donor["source_sha256"] == terminal["copied_save_sha256"]
    assert trace["all_host_slots_restored_and_core_file_exact"] and not trace["errors"] and not trace["mismatches"]
    assert trace["source_requests"] == terminal["common_requests"]
    return shots(report, "_navigation.png"), trace["source_requests"], dict(
        donor=reference(donor["source"]), capture=reference(run_path), trace=reference(trace_path),
        terminal=reference(terminal_path), journal=reference(journal_path))


def exact_command(block, ref):
    at = ref["command_offset"]
    command = bytes.fromhex(ref["exact_command_hex"])
    assert sha256(block).hexdigest() == ref["block_sha256"] and block[at:at + len(command)] == command
    return command


def nameplate(font, name, screen):
    return complete_mask(font, name, screen, 16, 277, town.INKS[1]) if name else None


def story_panels(clean, image, font, frames, release):
    jp, en = [rom.read_file(STORY) for rom in (clean, image)]
    before, after = [IlnkContainer.parse(raw).blocks for raw in (jp, en)]
    ctx = SimpleNamespace(image=image, arm=image.read_file(active.ARM))
    paint, fe = town.clipped_renderer(ctx), town.current_fe_painter(ctx)
    kanji = image.read_file("/GRP/KANJI.FNT")
    rows, sheets, previews = [], {}, []
    for block, ledger in ((181, TREND), (170, JULIO)):
        assert digest(ledger) == read(ledger.parent.parent / "checksums.json")["verification/registered_review.json"]
        source_rows = [r for r in read(ledger)["records"] if r.get("file_path") == STORY and r["block"] == block]
        assert len(source_rows) == (10 if block == 181 else 48)
        figures = []
        for row in source_rows:
            number = int(row["id"].rsplit("_R", 1)[1])
            src, dst = row["source_reference"], row["registered_reference"]
            a, b = exact_command(before[block], src), exact_command(after[block], dst)
            assert a[:6] == b[:6] and set(row["review"]) == set(GATES) and all(row["review"].values())
            raw = bytes_for(b)
            assert raw.isascii() and " ".join(raw.decode("ascii").split()) == row["english"]
            frame = STORY_FRAMES[block].get(number)
            evidence = {}
            if frame:
                screen = picture(frames[frame])
                if b[5] == 254:
                    display = fe(raw)
                    plane, width = display["physical"], 228
                else:
                    display = paint(ctx.arm, kanji, raw)
                    page, = display["pages"]
                    assert page["native_independent_plane_equal"]
                    plane, width = bytes.fromhex(page["native_plane_hex"]), 216
                assert display["complete_consumed_bytes"] == len(raw)
                assert mask_check(plane, width, screen), (block, row["id"], frame)
                plate = nameplate(font, row["speaker"], screen) if b[5] != 254 else None
                evidence.update(capture=frames[frame], native_plane_sha256=sha256(plane).hexdigest(), complete_nameplate=plate)
                figures.append((row["id"], screen))
            finding = GAPS.get((block, number))
            planned = None
            if finding:
                draft = finding[0] or row["english"]
                proposal = dict(id=row["id"], english=draft, protected_phrases=finding[1])
                body, plan = layout.plan_progressive(proposal, b[5], raw, bytes_for(a))
                assert plan["expected_native_pages"] == 1 and len(body) <= len(raw)
                page, = story_display.display.raster(ctx, kanji, paint, body, plan["lines"], 1)
                assert page["native_independent_plane_equal"]
                plane = bytes.fromhex(page["native_plane_hex"])
                previews.append((row["id"], plane))
                planned = dict(formatter_plan=plan, native_plane_sha256=sha256(plane).hexdigest(),
                               physical_source_and_installed_selectors=b[5], fits_current_text_bytes=True,
                               stored_and_gameplay_checks_pending=True)
            rows.append(dict(id=row["id"], block=block, context=row["context"], speaker=row["speaker"],
                clean_Japanese=row["Japanese"], source_gloss=row["source_meaning"], source_reference=src,
                installed_reference=dst | dict(candidate_sha256=release["candidate_sha256"], archive_sha256=sha256(en).hexdigest()),
                installed_English=raw.decode("ascii"), gameplay_observed=bool(frame), display=evidence,
                decision="revision proposed" if finding else "retention",
                rationale=finding[2] if finding else row["localization_note"],
                proposed_English=(finding[0] or row["english"]) if finding else None,
                offline_preflight=planned,
                review=row["review"] | ({"formatting": False} if finding else {})))
        sheets[block] = sheets_for(f"genoa_story_B{block}", figures)
    contact = story_display.display.inherited.early.contact_sheets
    preview_directory = OUT.parent / "genoa_proposed_text_20261123"
    preview_directory.mkdir(exist_ok=True)
    proposed_sheets = FunctionType(contact.__code__, contact.__globals__ | {"ROOT": preview_directory})(previews)
    event, = [row for row in read(CATALOGUE)["records"] if row["route"] == 1 and row["English"] == "Genoa"]
    event_bytes = image.read_file(event["event_archive"])
    assert clean.read_file(event["event_archive"]) == event_bytes and event["original_event"]["script_block"] == 181
    original = event["original_event"]
    at = original["event_record_offset"]
    raw = bytes.fromhex(original["record_hex"])
    assert event_bytes[at:at + len(raw)] == raw and event["installed_block_sha256"] == sha256(after[181]).hexdigest()
    return rows, sheets, proposed_sheets, event, before[170], after[170], sha256(en).hexdigest()


def choice_panels(font, frames, source, installed, archive):
    assert digest(CHOICES) == read(CHOICES.parent.parent / "checksums.json")["verification/registered_review.json"]
    records = [r for r in read(CHOICES)["records"] if r["id"].startswith("SC1_B170_CHOICE_")]
    assert len(records) == 4
    rows, figures = [], []
    for group, (frame, command_at) in CHOICE_FRAMES.items():
        labels = [r for r in records if r["source_reference"]["command_offset"] == group]
        assert len(labels) == 2 and all(all(r["review"].values()) for r in labels)
        a = exact_command(installed, labels[0]["registered_reference"] | {
            "command_offset": command_at, "block_sha256": sha256(installed).hexdigest()})
        assert a[:4] == source[group:group + 4] == b"\x00\x21\x00\x00"
        screen = picture(frames[frame])
        for index, row in enumerate(labels):
            ref = row["source_reference"]
            source_body = bytes.fromhex(ref["exact_body_hex"])
            assert source[ref["offset"]:ref["offset"] + len(source_body)] == source_body
            at = command_at + 6 + (int.from_bytes(a[4:6], "little") if index else 0)
            assert installed[at:at + len(row["english"]) + 1] == row["english"].encode("ascii") + b"\0"
            mask = find_line(font, row["english"], screen, range(37, 128),
                             range(269 + 20 * index, 277 + 20 * index), (8, 8, 8))
            rows.append(dict(id=row["id"], clean_Japanese=row["Japanese"], source_reference=ref,
                installed_reference=dict(path=STORY, archive_sha256=archive, block=170,
                    block_sha256=sha256(installed).hexdigest(), offset=at, command_offset=command_at,
                    exact_command_hex=a.hex()), installed_English=row["english"], capture=frames[frame],
                complete_label=mask, observed_selected=index == 0, choice_index=index,
                decision="retention", rationale=row["localization_note"], review=row["review"]))
        figures.append((f"Choice {group} / top option selected", screen))
    return rows, sheets_for("genoa_choices", figures, crop=(0, 244, 256, 378))


def find_line(font, text, screen, xs, ys, color):
    matches = []
    for y in ys:
        for x in xs:
            if x + 6 * len(text) <= 256 and y + 11 <= 384:
                try:
                    matches.append(complete_mask(font, text, screen, x, y, color))
                except ValueError:
                    pass
    result, = matches
    return result


def exact_body(font, lines, screen):
    glyph_points = set()
    for i, line in enumerate(lines):
        _, (x, y, _, _) = find_line(font, line, screen, (16, 20, 22), (297 + 16 * i,), town.INKS[0])
        glyph_points.update((x + dx, y + dy) for dx, dy in glyphs(font, line))
    actual = {(x, y) for x in range(16, 245) for y in range(296, 360) if screen.getpixel((x, y)) == town.INKS[0]}
    assert actual == glyph_points
    return len(actual)


def common_panels(city, frames, calls, source, installed, font):
    rows, figures = [], []
    for frame, (key, args, lines) in HOLDS[city].items():
        requests = [row for row in calls if row["message_ID"] == key and 0 <= frame - row["frame"] < 400]
        first, second = requests
        assert first["PC"] == 0x0205528C and second == first | {"PC": 0x020534F4}
        ja, en = source[key], installed[key]
        assert ja.text.count(b"%s") == len(args) + (key == 872)
        assert en.text.count(b"%s") == len(args)
        text = en.text % tuple(arg.encode("ascii") for arg in args)
        assert text.decode("ascii").split() == " ".join(lines).split()
        speaker, reason = COMMON[key]
        screen = picture(frames[frame])
        try:
            ink = exact_body(font, lines, screen)
        except (AssertionError, ValueError) as error:
            raise ValueError((city, frame, key, lines)) from error
        figures.append((f"{frame} / COMMON {key}", screen))
        rows.append(dict(message_ID=key, clean_Japanese=ja.text.decode("cp932"),
            source_reference=text_reference(ja), installed_reference=text_reference(en),
            source_hex=ja.text.hex(), installed_hex=en.text.hex(), speaker=speaker, arguments=args,
            lines=lines, capture=frames[frame], body_ink_pixels=ink, complete_nameplate=nameplate(font, speaker, screen),
            requests=requests, decision="retention", rationale=reason, review=dict.fromkeys(GATES, True)))
    return rows, sheets_for(f"{city}_shops_and_tavern", figures)


def sheets_for(name, figures, crop=(0, 272, 256, 380)):
    sheets = []
    for start in range(0, len(figures), 8):
        batch = figures[start:start + 8]
        box = Image.new("RGB", (1040, 242 * ((len(batch) + 1) // 2)), "#263238")
        draw = ImageDraw.Draw(box)
        for i, (label, screen) in enumerate(batch):
            x, y = i % 2 * 520 + 4, i // 2 * 242
            draw.text((x, y + 2), label, fill="white")
            view = screen.crop(crop)
            if view.height <= 112:
                view = view.resize((512, view.height * 2), Image.Resampling.NEAREST)
            box.paste(view, (x, y + 20))
        path = OUT.with_name(f"{name}_{1 + start // 8}_20261123.png")
        box.save(path)
        sheets.append(reference(path))
    return sheets


def main():
    release = read(active.RELEASE)
    assert digest(REGISTRY) == release["registry_sha256"] and digest(CLEAN) == release["clean_input_sha256"]
    assert digest(active.ROM) == release["candidate_sha256"]
    clean, image = map(NdsImage.open, (CLEAN, active.ROM))
    arm = image.read_file(active.ARM)
    clean_arm = clean.read_file(active.ARM)
    round_caller = arm[0x584CC:0x584E8]
    assert round_caller == clean_arm[0x584CC:0x584E8]
    source = common_message_entries(clean.read_file(active.COMMON), clean_arm)
    installed = common_rows(image.read_file(active.COMMON), arm)
    font = GameAsciiFont.from_arm9(arm)
    game = {}
    for city in observed.HISTORIES:
        frames, calls, evidence = capture(city, release)
        shared, sheets = common_panels(city, frames, calls, source, installed, font)
        changes = (3200, 5800, 9200, 18100, 19700, 19900) if city == "genoa" else (3200, 6100, 6800, 8200, 9200)
        game[city] = dict(evidence=evidence, shared=shared, shared_sheets=sheets,
                          transitions=[frames[frame] for frame in changes])
        if city == "genoa":
            story, figures, proposed, trend, old, new, archive = story_panels(clean, image, font, frames, release)
            choices, menus = choice_panels(font, frames, old, new, archive)
            game[city].update(story=story, story_sheets=figures, proposed_native_sheets=proposed,
                              original_Genoa_event=trend, choices=choices, choice_sheets=menus)
        else:
            amounts = {3200: 43235, 8200: 42999, 9200: 42989}
            balances = {frame: find_mask(font, str(amount), picture(frames[frame]), (78, 350, 133, 365))
                        for frame, amount in amounts.items()}
            assert amounts[3200] - amounts[8200] == 236 and amounts[8200] - amounts[9200] == 10
            game[city].update(wallet_masks=balances, tavern_round_cost=236,
                              two_individual_drinks_total=10, round_caller_unchanged=dict(
                                  start=0x020584CC, end_exclusive=0x020584E8,
                                  sha256=sha256(round_caller).hexdigest(), surname_argument_observed="Bergstrom"))
    counts = Counter("story" for row in story if row["gameplay_observed"])
    counts.update(dict(shared=sum(len(r["shared"]) for r in game.values()), choice_labels=len(choices)))
    assert counts == {"story": 46, "shared": 23, "choice_labels": 4}
    write(OUT, dict(release=reference(active.RELEASE), candidate_sha256=release["candidate_sha256"],
        counts=dict(counts), draft_findings=len(GAPS), ordinary_gameplay=game,
        alternate_Julio_outcomes_observed=False, new_editorial_credit=0, changed_ROM=False))
    print(f"Verified {dict(counts)} with ordinary controller input on the registered ROM.")


if __name__ == "__main__":
    main()
