"""Verify Valencia's ordinary investment, lodging and tavern exchanges."""

import json
from pathlib import Path
from struct import unpack_from
from types import FunctionType, SimpleNamespace

from PIL import Image, ImageDraw

from dk4tool.dialogue.font_audit import GameAsciiFont
from dk4tool.dialogue.review import validate_natural_dialogue_batch
from scripts import observe_valencia_government_20261124 as play
from scripts import preflight_ceuta_contract_refusal_20261124 as refusal
from scripts import verify_athens_palace_contract_20261124 as prior
from scripts import verify_riga_trade_deck_20261124 as review
from scripts.stage_cartridge_title_20261123 import CLEAN, GATES, NdsImage, REGISTRY, digest, read, reference, sha256, write


OUT = review.OUT.with_name("valencia_government_current_20261124.json")
panels = review.panels
END = 18800
HOLDS = ((4400, 1151), (5000, 1158), (5900, 1151), (6500, 1160), (7700, 63), (8600, 1179),
         (9800, 1180), (10100, 1179), (11000, 1180), (11300, 1181), (12500, 1177), (12800, 1178),
         (14300, 51), (15200, 858), (15500, 865), (15800, 872), (16100, 874), (16400, 870),
         (17600, 8), (18200, 761))
TEXT = {
    1151: ("Governor", ("Bergstrom",), ("Even without a trading contract,", "you offer to help defend our city.",
            "Most generous, Bergstrom."), "The governor praises Bergstrom for helping defend a city where he has no contract.",
           "The full contract phrase and courteous final address preserve both the condition and the governor's praise."),
    1158: ("Governor", (), ("Bah! Make up your mind.",), "The governor reproaches the captain's indecision.",
           "The abrupt complaint fits the cancellation before payment."),
    1160: ("Governor", (), ("Hmm. You've shown admirable spirit.", "I commend you."),
           "The governor admires the captain's spirit and commends him.",
           "The measured assent and formal commendation fit the official receiving the payment."),
    63: ("Innkeeper", (), ("Welcome! Come in.",), "The innkeeper welcomes the visitor.",
         "A warm opening gives Hodram an invitation to browse the lodging options."),
    1179: ("Innkeeper", (), ("It's 1 gold coin for each night.", "How many nights will you stay?"),
           "The innkeeper quotes one coin per night, then asks for the length of stay.",
           "The rate and complete question give the player the information needed for the next choice."),
    1180: ("Innkeeper", ("10",), ("You're staying 10 nights, then?",), "The innkeeper confirms the chosen number of nights.",
           "The conversational tag keeps the question inviting and fits on the same line as the exact length."),
    1181: ("Innkeeper", (), ("Enjoy your stay.",), "The innkeeper invites the guest to make himself comfortable.",
           "The common farewell fits the longer stay as the game advances the date."),
    1177: ("Innkeeper", (), ("That'll be 1 gold coin.",), "The innkeeper quotes one gold coin.",
           "The direct quote suits the one-night alternative and states the full price."),
    1178: ("Innkeeper", (), ("Sleep well!",), "The innkeeper wishes the guest a good night.",
           "The brief send-off is warm and suits the single night."),
    51: ("Barkeep", (), ("Welcome! What will you have?",), "The barkeep greets the guest and asks for his order.",
         "The ordinary American English greeting opens the drink menu naturally."),
    858: ("Manuel Almeida", ("218",), ("Would it be all right to spend", "about 218 gold?"),
          "Manuel estimates the expense and asks whether it is acceptable.",
          "His deferential question sounds natural and preserves the estimate."),
    865: ("Hodram Bergstrom", (), ("Drinks for everyone!",), "Hodram calls to the barkeep to serve everyone a drink.",
          "The direct call suits Hodram and carries the public invitation."),
    872: ("Barkeep", ("Bergstrom",), ("This round's on Bergstrom. Enjoy!",),
          "The barkeep names the person buying the round and invites everyone to drink.",
          "The announcement sounds like a toast and retains the sponsor through the installed surname argument."),
    874: ("Patron", (), ("Whoa! Really? Thanks for the round!", "Mighty generous of you!"),
          "The patron reacts with surprise, thanks the captain, and praises his generosity in colloquial speech.",
          "The cheerful exclamations preserve the lively response before the patron offers a tip."),
    870: ("Patron", ("Sir", "Black Rapier", "the Mediterranean"), ("Sir, a tip about a rare treasure.",
          "They say Black Rapier is stashed", "in the Mediterranean."),
          "The patron addresses the captain, then passes along a rumor that names a rare treasure and its region.",
          "The wording sounds like a friendly tip, names the treasure and location, and keeps the report hearsay."),
    8: ("Trader", (), ("Need help?",), "The trader asks what the customer needs.",
        "The short greeting suits a routine Market visit."),
    761: ("Trader", ("Governor's Office",), refusal.EXPECTED["Governor's Office"],
          "The trader apologizes and asks the customer to return after signing a contract at the named office.",
          "The current reply keeps the return instruction complete and names the office Hodram just visited."),
}


def capture(release):
    scope = vars(panels) | dict(observed=SimpleNamespace(ROOT=play.ROOT.parent))
    frames, calls, refs = FunctionType(panels.capture.__code__, scope)(play.ROOT.name, release)
    commands = list(map(json.loads, play.CONTROLLER.read_text("utf-8").splitlines()))
    assert commands[:len(play.OPENING)] == list(play.OPENING)
    assert max(frames) == commands[-2]["until"] == END
    earlier = read(play.PRIOR)["towns"]["valencia"]["evidence"]
    assert refs["donor"]["sha256"] == earlier["donor"]["sha256"]
    old = read(earlier["capture"]["path"])
    assert digest(earlier["capture"]["path"]) == earlier["capture"]["sha256"]
    start = panels.shots(old, "_navigation.png")[play.FIRST_PAUSE]
    assert frames[play.FIRST_PAUSE]["framebuffer_sha256"] == start["framebuffer_sha256"]
    assert not {284, 318, 750, 751, 752} & {row["message_ID"] for row in calls}
    return frames, calls, refs, commands


def title(source, arm, release, screens, font):
    row, = (row for row in read(prior.RULER)["records"] if row["actor_ID"] == 131)
    field, = (field for field in row["source_actor_fields"] if field["field"] == "primary")
    original, at = field["clean"], field["ARM9_pointer_field_offset"]
    pointer, = unpack_from("<I", source, at)
    assert pointer == original["pointer"] and original["text"] == "総督"
    start, length = original["offset"], original["byte_length"]
    assert source[start:start + length + 1] == bytes.fromhex(original["hex"]) + b"\0"
    startup = release["own_registered_startup"]
    assert digest(startup) == release["own_registered_startup_sha256"]
    boot = read(startup)["read_only_snapshot"]
    ram = Path(boot["path"]).read_bytes()
    assert boot["read_only_export"] and sha256(ram).hexdigest() == boot["sha256"]
    target, = unpack_from("<I", arm, at)
    assert target == unpack_from("<I", ram, at)[0]
    asserted = b"Governor\0"
    offset = target - 0x02000000
    assert ram[offset:offset + len(asserted)] == asserted
    return dict(actor_ID=131, display="Governor", rationale="Governor matches the source title and suits the port official's role.",
                source=original, installed=dict(pointer=target, field_offset=at, exact_hex=asserted.hex()),
                native_masks={f: panels.nameplate(font, "Governor", screens[f]) for f in (4400, 5000, 5900, 6500)},
                previous_role_review=reference(prior.RULER), review=dict.fromkeys(GATES, True))


def sheet(screens, titles, number):
    image = Image.new("RGB", (768, 808), "#263238")
    draw = ImageDraw.Draw(image)
    for i, (frame, label) in enumerate(titles):
        x, y = i % 3 * 256, i // 3 * 404
        draw.text((x + 4, y + 4), label, fill="white")
        image.paste(screens[frame], (x, y + 20))
    path = OUT.with_name(f"valencia_government_current_{number}_20261124.png")
    image.save(path)
    return reference(path)


def dialogue(source, installed, frames, screens, calls, font):
    assert len(calls) == 2 * len(HOLDS)
    records = {}
    for (hold, key), (getter, copier) in zip(HOLDS, zip(calls[::2], calls[1::2], strict=True), strict=True):
        assert getter["PC"] == 0x0205528C and copier == getter | {"PC": 0x020534F4}
        assert getter["message_ID"] == key and 0 < hold - getter["frame"] < 300
        ja, en = source[key], installed[key]
        speaker, arguments, lines, meaning, note = TEXT[key]
        english = " ".join(en.text.decode("ascii").split())
        assert en.text.count(b"%s") == len(arguments)
        assert ja.text.count(b"%s") == len(arguments) + (key == 872)
        assert (english % arguments).split() == " ".join(lines).split()
        stage = ("The Valencia Governor's Office defense proposal, cancellation and payment." if key in (1151, 1158, 1160)
                 else "Valencia Inn, including the longer stay and a subsequent single night." if key in (63, 1179, 1180, 1181, 1177, 1178)
                 else "Valencia Tavern, from ordering a round to a patron's treasure tip." if key not in (8, 761)
                 else "Valencia Market after defense investment, with no trading contract in place.")
        record = records.setdefault(key, dict(id=f"COMMON_MESSAGE_{key}", message_ID=key, file_path=play.current.COMMON,
            context=stage, english=english, speaker=speaker, clean_Japanese=ja.text.decode("cp932"),
            source_meaning=meaning, localization_note=note, decision="retention", review=dict.fromkeys(GATES, True),
            source_reference=review.source_ref(ja), current_reference=review.source_ref(en),
            installed_reference=review.source_ref(en), holds=[]))
        record["holds"].append(dict(capture=frames[hold], arguments=arguments, lines=lines, native_requests=[getter, copier],
            exact_body_pixels=panels.exact_body(font, lines, screens[hold]),
            exact_nameplate=panels.nameplate(font, speaker, screens[hold])))
    return list(records.values())


def transitions(screens, frames, font):
    # Wallet balances and dates use the existing interface's digits and were read on the captured screens.
    amounts = ((3800, "2/10", 39144), (5300, "2/10", 39144), (6800, "2/11", 37694),
               (11900, "2/21", 37684), (13400, "2/22", 37683), (17000, "2/22", 37465), (END, "2/22", 37465))
    assert 39144 - 1450 == 37694 and 37694 - 10 - 1 - 218 == 37465
    charge = {
        text: panels.find_mask(font, text, screens[4700], bounds)
        for text, bounds in (("1450", (148, 329, 198, 347)), ("37694", (148, 346, 198, 366)))
    }
    repeats = ((3800, 5300), (4700, 6200), (8600, 10100), (9800, 11000))
    assert all(screens[before].tobytes() == screens[after].tobytes() for before, after in repeats)
    choices = {frame: [panels.find_mask(font, label, screens[frame], rect) for label, rect in
        (("No", (118, 360, 165, 376)), ("Yes", (188, 360, 235, 376)))] for frame in (9800, 11000, 15200)}
    return dict(wallet_and_calendar_visual_reads=[dict(capture=frames[frame], date=date, gold=gold)
        for frame, date, gold in amounts], payment=1450, lodging_gold=[10, 1], drinks_gold=218, projected_gold_masks=charge,
        exact_repeat_frames=repeats, choice_masks=choices, refused_after_payment=frames[18200],
        returned_to_market=frames[18500], returned_to_town=frames[END])


def main():
    release = read(play.current.RELEASE)
    assert digest(play.current.ROM) == release["candidate_sha256"]
    assert digest(CLEAN) == release["clean_input_sha256"] and digest(REGISTRY) == release["registry_sha256"]
    frames, calls, refs, commands = capture(release)
    clean, rom = map(NdsImage.open, (CLEAN, play.current.ROM))
    old_arm, arm = (image.read_file(play.current.ARM) for image in (clean, rom))
    archive = rom.read_file(play.current.COMMON)
    assert sha256(arm).hexdigest() == release["target_ARM9_sha256"]
    assert sha256(archive).hexdigest() == release["target_COMMON_sha256"]
    source = review.base.common_message_entries(clean.read_file(play.current.COMMON), old_arm)
    installed = review.base.common_rows(archive, arm)
    screens = {frame: panels.picture(shot) for frame, shot in frames.items()}
    font = GameAsciiFont.from_arm9(arm)
    rows = dialogue(source, installed, frames, screens, calls, font)
    registered, = (row for row in read(play.current.REVIEW)["records"] if row["message_ID"] == refusal.KEY)
    assert review.source_ref(source[refusal.KEY]) == registered["source_reference"]
    assert review.source_ref(installed[refusal.KEY]) == registered["installed_reference"]
    notes = dict(translation_policy="natural-dialogue-v2", encoder="dialogue-relocatable-v1", target_locale="en-US",
        review_gates=list(GATES), candidate_sha256=release["candidate_sha256"], clean_input_sha256=release["clean_input_sha256"],
        ordinary_gameplay=True, records=rows, role_title=title(old_arm, arm, release, screens, font),
        transitions=transitions(screens, frames, font), controller_commands=commands, evidence=refs,
        registered_market_refusal=reference(play.current.REVIEW), ROM_changed=False, new_editorial_credit=0,
        unvisited=["Other defense amounts and longer stay lengths", "Other patrons and rumors", "Physical hardware"])
    validate_natural_dialogue_batch(notes)
    groups = (
        ((3800, "Government menu"), (4400, "Defense offer"), (4700, "Proposed payment"),
         (5000, "Cancelled payment"), (6500, "Governor's thanks"), (6800, "Paid 1,450 gold")),
        ((7700, "Innkeeper greeting"), (8600, "Nightly rate"), (9800, "Ten-night choice"),
         (11300, "Long-stay farewell"), (12500, "One-night price"), (12800, "One-night farewell")),
        ((11900, "Ten nights complete"), (13400, "Single night complete"), (14300, "Barkeep greeting"),
         (15200, "Manuel's estimate"), (15500, "A round for everyone"), (15800, "Barkeep's toast")),
        ((16100, "Patron's thanks"), (16400, "Patron's tip"), (17000, "After the round"),
         (17600, "Trader greeting"), (18200, "Trading contract required"), (END, "Back in Valencia")),
    )
    notes["review_sheets"] = [sheet(screens, group, index) for index, group in enumerate(groups, 1)]
    write(OUT, notes)
    print(f"Verified {len(rows)} distinct Valencia records across {len(HOLDS)} ordinary gameplay holds.")


if __name__ == "__main__":
    main()
