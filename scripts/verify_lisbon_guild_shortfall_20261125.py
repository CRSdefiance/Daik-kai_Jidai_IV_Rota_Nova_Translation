"""Bind the ordinary Lisbon Guild shortfall to the original affordability branch."""

import json
from pathlib import Path
from types import FunctionType, SimpleNamespace

from capstone import CS_ARCH_ARM, CS_MODE_ARM, Cs
from PIL import Image, ImageDraw
from dk4tool.dialogue.font_audit import GameAsciiFont
from dk4tool.dialogue.review import validate_natural_dialogue_batch
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.ascii_glyph_right_bounds import assemble
from dk4tool.patch.yard_numerals_20261124 import BASE, HELPER, NUMBER
from dk4tool.script.common_message_table import common_message_entries
from scripts import observe_lisbon_guild_shortfall_20261125 as play
from scripts import verify_genoa_copenhagen_town_20261123 as panels
from scripts.stage_cartridge_title_20261123 import CLEAN, GATES, NdsImage, REGISTRY, digest, read, reference, sha256, write
from scripts.verify_all_items_gallery_v535 import glyph_pixels


OUT = panels.OUT.with_name("lisbon_guild_shortfall_current_20261125.json")
PREFLIGHT = OUT.with_name("guild_trade_numerals_preflight_20261124.json")
DECK_PACKAGE = Path("releases/all_routes_editorial_20261122_rafael_deck_tutorial_candidate")
PITCH_PACKAGE = Path("releases/all_routes_editorial_20261124_istanbul_tavern_rumor_candidate")
DECK_FRAMES = range(14521, 17162, 240)
STORY = "/data/SC0.DK4"
BRANCH = 0x0205C298
PRICE_CALL = 0x0205C3F4
END = 21241
REQUESTS = (8, 763, 747, 62, 3665, 1071, 2903, 2903, 1072, 1071, 2903, 2903, 3014, 1072, 1071, 2903, 2903)
GUILD = (
    (62, [(17881, ("Need something?",), ())],
     "The Guildmaster greets Rafael and asks what he needs.",
     "The relaxed greeting fits the Guildmaster and lets Rafael choose between buying and selling."),
    (3665, [(18601, ("It's supposed to be a twisted horn.", "Some say it came from a dragon.",
                     "Word is, you can turn it into", "medicine that cures any illness."), ())],
     "The Guildmaster repeats rumors about a twisted horn, its possible dragon origin and its use in a cure.",
     "The three hearsay cues carry the uncertainty. The full claim about the medicine stays together."),
    (1071, [(n, ("Which one would you like?",), ()) for n in (18841, 19561, 20521)],
     "The Guildmaster asks the player which item to select.",
     "The same direct invitation works when the item list first opens and when the unaffordable item is put back."),
    (1072, [(19321, ("Can you even afford 10000 coins?",), ("10000",)),
            (20281, ("Can you even afford 3000 coins?",), ("3000",))],
     "The Guildmaster names the price and doubts Rafael has enough to afford it.",
     "Even carries the Guildmaster's skeptical tone, and the whole price and question fit together on one line."),
)
CATALOG = (
    (2903, 19081, "Travels of Marco Polo", "10000", ("Completed in the 13th century, this book tells",
         "what Marco Polo saw and heard on his travels", "in the East."),
     "A book completed in the 13th century that compiles what Marco Polo saw and heard while traveling in the East.",
     "Book, date, region and first-hand sources are intact. The entry reads as a description beside the item and price."),
    (3014, 20041, "Twisted Horn Map 2", "3000", ("One of four pieces of an ancient map.",),
     "A fragment of an ancient map that forms a set with three other pieces.",
     "The one-line description makes clear that the selected item is a fragment of a four-piece map."),
)


def source_path(clean, arm):
    spans = []
    for start, end in ((0x0205C204, 0x0205C20C), (0x0205C290, 0x0205C29C),
                       (0x0205C3F0, PRICE_CALL), (PRICE_CALL + 4, 0x0205C408)):
        source = clean[start - BASE:end - BASE]
        assert source and source == arm[start - BASE:end - BASE]
        spans.append(dict(start=start, end=end, exact_hex=source.hex()))
    inst = {i.address: f"{i.mnemonic} {i.op_str}" for span in spans
            for i in Cs(CS_ARCH_ARM, CS_MODE_ARM).disasm(bytes.fromhex(span["exact_hex"]), span["start"])}
    assert inst[0x0205C204] == "mov r0, #0x430" and inst[0x0205C208] == "str r0, [sp, #0x1c]"
    assert inst[0x0205C294] == "cmp r0, r8" and inst[BRANCH] == "blo #0x205c3f0"
    assert inst[0x0205C3FC] == "ldr r1, [sp, #0x1c]" and inst[0x0205C404] == "bl #0x2053fe4"
    installed = arm[PRICE_CALL - BASE:PRICE_CALL - BASE + 4]
    before = clean[PRICE_CALL - BASE:PRICE_CALL - BASE + 4]
    assert before == assemble(f"bl {NUMBER}", PRICE_CALL) and installed == assemble(f"bl {HELPER}", PRICE_CALL)
    old, = [row for row in read(PREFLIGHT)["exact_ARM9_edits"] if row["message_ID"] == 1072]
    assert old["address"] == PRICE_CALL and old["installed_hex"] == installed.hex()
    return dict(original_and_installed_spans=spans, original_code=inst,
                registered_numeral_call=dict(address=PRICE_CALL, clean_hex=before.hex(), installed_hex=installed.hex()))


def read_run():
    active = play.current
    release = read(active.RELEASE)
    assert digest(CLEAN) == release["clean_input_sha256"] and digest(REGISTRY) == release["registry_sha256"]
    assert digest(active.ROM) == release["candidate_sha256"]
    scope = vars(panels) | dict(observed=SimpleNamespace(ROOT=play.ROOT.parent))
    frames, calls, refs = FunctionType(panels.capture.__code__, scope)(play.ROOT.name, release)
    commands = [json.loads(line) for line in play.CONTROLLER.read_text("utf-8").splitlines()]
    assert commands[0] == play.OPENING
    historical = read(play.HISTORY)
    replay = read(refs["capture"]["path"])
    prefix = [row for row in historical["scripted_input_schedule"] if row["start"] <= play.FIRST_PAUSE]
    assert replay["scripted_input_schedule"][:len(prefix)] == prefix
    assert refs["donor"]["sha256"] == historical["battery_save_preloaded"]["source_sha256"]
    original, current = map(NdsImage.open, (CLEAN, active.ROM))
    clean_arm, arm = (image.read_file(active.ARM) for image in (original, current))
    assert sha256(arm).hexdigest() == release["target_ARM9_sha256"]
    source = common_message_entries(original.read_file(active.COMMON), clean_arm)
    installed = panels.common_rows(current.read_file(active.COMMON), arm)
    assert all(a["PC"] == 0x0205528C and b == a | {"PC": 0x020534F4}
               for a, b in zip(calls[::2], calls[1::2], strict=True))
    return release, frames, calls, refs, commands, original, current, clean_arm, arm, source, installed


def line(font, source, installed, key, holds, meaning, reason, frames, calls, screens):
    ja, en = source[key], installed[key]
    observed = []
    for frame, rows, args in holds:
        assert ja.text.count(b"%s") == en.text.count(b"%s") == len(args)
        assert (en.text % tuple(arg.encode("ascii") for arg in args)).decode("ascii").split() == " ".join(rows).split()
        first, second = [r for r in calls if r["message_ID"] == key and 0 < frame - r["frame"] <= 240]
        assert second == first | {"PC": 0x020534F4}
        observed.append(dict(frame=frame, lines=rows, arguments=args, capture=frames[frame], requests=[first, second],
            glyphs=panels.exact_body(font, rows, screens[frame]),
            nameplate=panels.nameplate(font, "Guildmaster", screens[frame])))
    exact = panels.text_reference(en) | {"exact_hex": en.text.hex()}
    return dict(id=f"COMMON_MESSAGE_{key}", message_ID=key, speaker="Guildmaster",
        context="Lisbon Guild. Rafael checks the available merchandise and selects an item after a 27,000-gold investment.",
        english=en.text.decode("ascii").strip(), clean_Japanese=ja.text.decode("cp932"), source_meaning=meaning,
        localization_note=reason, decision="retention", observations=observed,
        source_reference=panels.text_reference(ja) | {"exact_hex": ja.text.hex()},
        current_reference=exact, installed_reference=exact, review=dict.fromkeys(GATES, True))


def deck_lesson(clean, current, frames, screens, font, candidate):
    block, registered = (IlnkContainer.parse(image.read_file(STORY)).blocks[43] for image in (clean, current))
    paths = [DECK_PACKAGE / "verification" / name for name in ("stored_proof.json", "registered_review.json", "verified_gameplay.json")]
    checksums = read(DECK_PACKAGE / "checksums.json")
    assert all(digest(path) == checksums[path.relative_to(DECK_PACKAGE).as_posix()] for path in paths)
    stored, review, earlier = map(read, paths)
    assert sha256(block).hexdigest() == stored["clean_block_sha256"]
    assert sha256(registered).hexdigest() == stored["compiled_block_sha256"]
    rows = {row["id"]: row for row in review["records"]}
    observed = []
    for hold, number in zip(earlier["twelve_complete_panels"], DECK_FRAMES, strict=True):
        row = rows[hold["id"]]
        assert all(row["review"][gate] for gate in GATES)
        src, dst = (row[name] for name in ("source_reference", "registered_reference"))
        a, b = (bytes.fromhex(ref["complete_command_hex"]) for ref in (src, dst))
        assert a[:6] == b[:6]
        assert all(raw[ref["command_offset"]:ref["command_offset"] + len(command)] == command
                   for raw, ref, command in ((block, src, a), (registered, dst, b)))
        body = bytes.fromhex(hold["body_hex"])
        assert body.rstrip() == panels.bytes_for(b).replace(b"FI", b"Rafael").rstrip()
        rows_displayed = [row.strip() for row in body.decode("ascii").splitlines()]
        speaker = hold["hold"]["speaker"]
        mask = panels.nameplate(font, speaker["text"], screens[number]) if speaker else None
        assert (speaker is None) == (b[5] == 254)
        observed.append(dict(id=row["id"], capture=frames[number], speaker=mask, lines=rows_displayed,
            glyphs=panels.exact_body(font, rows_displayed, screens[number]), source_reference=src,
            installed_reference=dst | {"observed_ROM_sha256": candidate},
            review=row["review"]))
    captain = observed[3]
    assert captain["id"].endswith("R0017")
    assert captain["lines"][:2] == ["First up is the captain.", "That's you, Rafael."]
    assert observed[-1]["speaker"] is None and "Deck View" in observed[-1]["lines"][0]
    return dict(archive=STORY, block=43, compiled_block_sha256=stored["compiled_block_sha256"],
                evidence=list(map(reference, paths)), complete_panels=observed)


def catalogue_mask(font, screen, text, x, y, left, right):
    assert text.isascii()
    ink = glyph_pixels(font, b"", (), text, x, y)
    actual = {(xx, yy) for yy in range(y, y + 11) for xx in range(left, right)
              if screen.getpixel((xx, yy)) == (230, 230, 230)}
    assert actual == ink, (text, len(actual ^ ink))
    return dict(text=text, origin=[x, y], complete_ink_pixels=len(ink), checked_row=[left, y, right, y + 11])


def catalogue(font, source, installed, frames, calls, screens):
    rows = []
    for key, frame, name, price, lines, meaning, reason in CATALOG:
        ja, en = source[key], installed[key]
        assert en.text.decode("ascii").split() == " ".join(lines).split() and b"%" not in ja.text + en.text
        screen = screens[frame]
        selection = [r for r in calls if r["message_ID"] == key and 0 < frame - r["frame"] <= 240]
        assert selection
        text_masks = [catalogue_mask(font, screen, value, 8, 113 + 16 * i, 8, 248) for i, value in enumerate(lines)]
        title = catalogue_mask(font, screen, name, 56, 25, 56, 248)
        cost = catalogue_mask(font, screen, price, 126 - len(price) * 5, 81, 94, 139)
        exact = panels.text_reference(en) | {"exact_hex": en.text.hex()}
        rows.append(dict(id=f"COMMON_MESSAGE_{key}", message_ID=key, speaker="Item catalogue",
            context=f"The Lisbon Guild Buy Items list describes {name} before Rafael chooses whether to buy.",
            english=en.text.decode("ascii").strip(), clean_Japanese=ja.text.decode("cp932"), source_meaning=meaning,
            localization_note=reason, decision="retention", title=title, price=cost, body=text_masks,
            capture=frames[frame], requests=selection, source_reference=panels.text_reference(ja) | {"exact_hex": ja.text.hex()},
            current_reference=exact, installed_reference=exact, review=dict.fromkeys(GATES, True)))
    return rows


def stock_pitch(clean_arm, arm, frames, screens, font):
    path = PITCH_PACKAGE / "verification/registered_review.json"
    assert digest(path) == read(PITCH_PACKAGE / "checksums.json")["verification/registered_review.json"]
    row, = [row for row in read(path)["records"] if row["id"] == "ARM9_GUILD_TREASURE_PITCH"]
    src, dst = (row[name] for name in ("source_reference", "registered_reference"))
    for data, ref in ((clean_arm, src), (arm, dst)):
        raw = bytes.fromhex(ref["exact_hex"])
        assert data[ref["offset"]:ref["offset"] + len(raw) + 1] == raw + b"\0"
    lines = [line.strip() for line in bytes.fromhex(dst["exact_hex"]).decode("ascii").splitlines()]
    frame = 18361
    assert " ".join(lines) == row["english"]
    return row | dict(decision="retention", current_reference=dst, installed_reference=dst,
        context="The Lisbon Guildmaster presents a rumored treasure map before Rafael opens the stock list.",
        localization_note="I have keeps the Guildmaster's sales pitch concrete, and said to lead presents the treasure as hearsay.",
        capture=frames[frame], lines=lines, glyphs=panels.exact_body(font, lines, screens[frame]),
        nameplate=panels.nameplate(font, "Guildmaster", screens[frame]), earlier_review=reference(path))


def sheet(name, shots, screens):
    img = Image.new("RGB", (1056, 214 * ((len(shots) + 3) // 4)), "#263238")
    labels = ImageDraw.Draw(img)
    for i, (frame, label, upper) in enumerate(shots):
        x, y = (i % 4) * 264 + 4, (i // 4) * 214
        labels.text((x, y + 2), label, fill="white")
        top = 0 if upper else 192
        img.paste(screens[frame].crop((0, top, 256, top + 192)), (x, y + 18))
    path = OUT.with_name(f"lisbon_guild_shortfall_{name}_20261125.png")
    img.save(path)
    return reference(path)


def main():
    release, frames, calls, refs, commands, clean, rom, clean_arm, arm, source, installed = read_run()
    assert max(frames) == END and tuple(row["message_ID"] for row in calls[::2]) == REQUESTS
    screens = {frame: panels.picture(shot) for frame, shot in frames.items()}
    font = GameAsciiFont.from_arm9(arm)
    assert screens[19081].tobytes() == screens[19801].tobytes() == screens[20761].tobytes()
    cash = {n: panels.find_mask(font, "400", screens[n], (77, 348, 137, 368))
            for n in (play.FIRST_PAUSE, 17401, 18121, 21001, END)}
    title = panels.find_mask(font, "Lisbon", screens[END], (51, 13, 108, 34))
    story = deck_lesson(clean, rom, frames, screens, font, release["candidate_sha256"])
    records = [line(font, source, installed, *setup, frames, calls, screens) for setup in GUILD]
    records.extend(catalogue(font, source, installed, frames, calls, screens))
    records.append(stock_pitch(clean_arm, arm, frames, screens, font))
    stock_native = source_path(clean_arm, arm)
    batch = dict(candidate_sha256=release["candidate_sha256"], translation_policy="natural-dialogue-v2",
        target_locale="en-US", encoder="dialogue-relocatable-v1", review_gates=list(GATES), records=records,
        rafael_deck_tutorial=story, native_affordability_branch=stock_native, ordinary_gameplay=True,
        original_save_and_replay=refs, commands=commands, source_requests=calls, verified_wallet=cash,
        refused_prices=[10000, 3000], stock_unchanged_frames=[19081, 19801, 20761], returned_to_Lisbon=title,
        earlier_guild_preflight=reference(PREFLIGHT), archived_display_ids_requested=sorted(set(REQUESTS) & {284, 318, 750, 751, 752}),
        unvisited=["Guild buy bargaining", "Guild sale bargaining"], ROM_changed=False, new_editorial_credit=0)
    validate_natural_dialogue_batch(batch)
    deck_sheet = sheet("deck", [(n, row["id"], False)
                                for n, row in zip(DECK_FRAMES, story["complete_panels"], strict=True)], screens)
    guild_sheet = sheet("guild", [(17881, "Guild greeting", False), (18361, "Map pitch", False),
        (18601, "Twisted Horn rumor", False), (18841, "Item prompt", False), (19081, "Travels of Marco Polo", True),
        (19321, "Shortfall at 10000 coins", False), (20041, "Twisted Horn Map 2", True),
        (20281, "Shortfall at 3000 coins", False), (21001, "Guild menu", False), (END, "Returned to Lisbon", False)], screens)
    write(OUT, batch | {"review_sheets": [deck_sheet, guild_sheet]})
    print("Verified all 12 Deck pages, two ordinary Guild shortfalls and the unchanged 400-gold wallet.")


if __name__ == "__main__":
    main()
