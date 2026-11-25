"""Review Nagasaki's ordinary second recruitment and over-capacity assignment."""

import json
from struct import unpack_from
from types import FunctionType, SimpleNamespace

from PIL import Image, ImageDraw

from dk4tool.dialogue.font_audit import GameAsciiFont
from dk4tool.dialogue.review import validate_natural_dialogue_batch
from scripts import observe_nagasaki_second_recruitment_20261124 as play
from scripts import verify_riga_trade_deck_20261124 as earlier
from scripts.stage_cartridge_title_20261123 import CLEAN, GATES, NdsImage, REGISTRY, digest, read, reference, sha256, write
from scripts.verify_crew_policy_matrix_v657 import BASE, find_complete, string


OUT = earlier.OUT.with_name("nagasaki_second_recruitment_current_20261124.json")
panels = earlier.panels
ARCHIVED = {284, 318, 750, 751, 752}
TEXT = {
    893: ("Sailor", "The sailor offers to recruit for the stated amount.",
          "The volunteer's casual wording fits the tavern and names the price before Maria decides."),
    900: ("Sailor", "The sailor calls for volunteers to sail with the fleet's admiral.",
          "The open call sounds natural in a busy tavern. Admiral follows the source's form of address."),
    907: ("Patron", "A patron calls out in agreement.",
          "The one-word answer makes sense as a public response to the call for volunteers."),
    904: ("Sailor", "The sailor reports how many people have volunteered in this round.",
          "The present-tense report sounds like the sailor and accurately reports this round's turnout."),
    1045: ("Sailor", "The sailor gives the number of open berths and asks whether to keep looking.",
           "The complete question is separate from the headcount. Its wording fits both observed values."),
    71: ("Sailor", "The sailor names the unassigned crew count and asks whether Maria accepts it.",
         "The count and the sailors it describes stay together. The second line states what Maria is deciding."),
}
HOLDS = (
    (12920, 1045, ("29",), ("There's room aboard for 29 more.", "Should I keep looking?")),
    (13320, 904, ("63",), ("We've got 63 willing to join.",)),
    (14120, 71, ("120",), ("Is leaving 120 of our sailors", "unassigned all right?")),
    (16920, 893, ("1040",), ("I'll get us sailors for 1040 gold.",)),
    (17320, 900, (), ("Anyone here want to sail", "with the Admiral?")),
    (17720, 907, (), ("Aye!",)),
    (18120, 904, ("53",), ("We've got 53 willing to join.",)),
    (18520, 1045, ("33",), ("There's room aboard for 33 more.", "Should I keep looking?")),
    (18920, 904, ("53",), ("We've got 53 willing to join.",)),
    (21320, 71, ("20",), ("Is leaving 20 of our sailors", "unassigned all right?")),
    (22120, 71, ("20",), ("Is leaving 20 of our sailors", "unassigned all right?")),
)


def capture(release):
    scope = vars(panels) | dict(observed=SimpleNamespace(ROOT=play.ROOT.parent))
    frames, calls, evidence = FunctionType(panels.capture.__code__, scope)(play.ROOT.name, release)
    commands = list(map(json.loads, play.CONTROLLER.read_text("utf-8").splitlines()))
    assert commands[0] == play.OPENING and commands[-1] == {"stop": True}
    assert max(frames) == commands[-2]["until"]
    history = read(play.HISTORY)
    paired = read(play.PAIR)
    assert reference(play.HISTORY) == paired["after"]
    assert evidence["donor"]["sha256"] == history["battery_save_preloaded"]["source_sha256"]
    prefix = [row for row in history["scripted_input_schedule"] if row["start"] <= play.FIRST_PAUSE]
    run = read(evidence["capture"]["path"])
    assert run["scripted_input_schedule"][:len(prefix)] == prefix
    prior = panels.shots(history, "_cold_boot.png")[play.FIRST_PAUSE]
    assert prior["framebuffer_sha256"] == frames[play.FIRST_PAUSE]["framebuffer_sha256"]
    assert not ARCHIVED & {row["message_ID"] for row in calls}
    return frames, calls, evidence, commands


def dialogue(source, installed, frames, screens, calls, font):
    for getter, copier in zip(calls[::2], calls[1::2], strict=True):
        assert getter["PC"] == 0x0205528C and copier == getter | {"PC": 0x020534F4}
    records = {}
    for hold, key, arguments, lines in HOLDS:
        ja, en = source[key], installed[key]
        speaker, meaning, rationale = TEXT[key]
        english = " ".join(en.text.decode("ascii").split())
        assert en.text.count(b"%s") == ja.text.count(b"%s") == len(arguments)
        assert (english % arguments).split() == " ".join(lines).split()
        first, second = [row for row in calls if row["message_ID"] == key and 0 < hold - row["frame"] < 400]
        assert second == first | {"PC": 0x020534F4}
        record = records.setdefault(key, dict(id=f"COMMON_MESSAGE_{key}", message_ID=key, file_path=play.current.COMMON,
            context="Maria accepts the Tavern's offer to keep looking and checks the resulting crew assignment.",
            english=english, speaker=speaker, clean_Japanese=ja.text.decode("cp932"), source_meaning=meaning,
            localization_note=rationale, decision="retention", review=dict.fromkeys(GATES, True),
            source_reference=earlier.source_ref(ja), current_reference=earlier.source_ref(en),
            installed_reference=earlier.source_ref(en), holds=[]))
        record["holds"].append(dict(capture=frames[hold], arguments=arguments, lines=lines, native_requests=[first, second],
            exact_body_pixels=panels.exact_body(font, lines, screens[hold]),
            exact_nameplate=panels.nameplate(font, speaker, screens[hold])))
    return list(records.values())


def even_notice(source_arm, arm, frames, screens, font):
    pointer = unpack_from("<I", arm, 0x1E27C)[0]
    assert pointer == unpack_from("<I", source_arm, 0x1E27C)[0]
    ja, en = (string(raw, pointer) for raw in (source_arm, arm))
    assert en == b"Sailors assigned evenly."
    text = en.decode("ascii")
    return dict(ARM9_pointer_offset=0x1E27C, ARM9_text_offset=pointer - BASE,
        source_reference=dict(clean_Japanese=ja.decode("cp932"), bytes=ja.hex()), installed_reference=dict(english=text, bytes=en.hex()),
        decision="retention", rationale="The message confirms the chosen policy and the fleet table shows the resulting distribution.",
        review=dict.fromkeys(GATES, True), capture=frames[20520], body_pixels=panels.exact_body(font, (text,), screens[20520]),
        nameplate=panels.nameplate(font, "Sailor", screens[20520]))


def measures(screens, frames, font):
    counts = {
        13720: ("114", "120", "57", "57"),
        19320: ("114", "106", "57", "57"),
        20920: ("200", "20", "100", "100"),
        21720: ("200", "20", "100", "100"),
        24520: ("200", "0", "100", "100"),
    }
    boxes = ((86, 18, 127, 37), (216, 18, 255, 37), (174, 206, 198, 227), (174, 238, 198, 259))
    distributions = {frame: [find_complete(font, value, screens[frame], box) for value, box in zip(count, boxes, strict=True)]
                     for frame, count in counts.items()}
    balances = {frame: panels.find_mask(font, gold, screens[frame], (75, 348, 136, 366))
                for frame, gold in ((14920, "36195"), (22520, "34115"), (22920, "34115"), (25320, "34115"))}
    assert 57 + 63 == 120 and 53 + 53 == 106 and 114 + 106 - 200 == 20
    assert 38275 - 2 * 1040 == 36195 and 36195 - 2 * 1040 == 34115
    choices = [panels.find_mask(font, label, screens[frame], rect) for frame in (12920, 14120, 18520, 21320, 22120)
               for label, rect in (("No", (118, 360, 165, 376)), ("Yes", (188, 360, 235, 376)))]
    assert screens[20920].tobytes() == screens[21720].tobytes()
    assert screens[21320].tobytes() == screens[22120].tobytes()
    return dict(first_batches=[57, 63], second_batches=[53, 53], observed_fee_per_round=1040, wallet_balances=balances,
        distributions=distributions, choice_masks=choices, first_exit_confirmation=frames[14120],
        no_restored_exact_assignment=True, yes_returned_to_tavern=frames[22520],
        reopened_crew_setup=frames[24520], returned_to_town=frames[25320])


def sheets(screens):
    groups = (
        ((12920, "Accept another round"), (13320, "63 additional volunteers"), (13720, "120 unassigned"),
         (14120, "Confirm leaving them unassigned"), (14920, "Two recruiting fees paid"), (16920, "Begin a fresh round")),
        ((18120, "First batch of 53"), (18520, "33 places remain"), (18920, "Another 53 volunteers"),
         (19320, "106 new unassigned"), (20520, "Even fills both ships"), (21320, "20 remain unassigned")),
        ((21720, "No keeps the assignment"), (22120, "Warning repeats"), (22520, "After the two recruiting fees"),
         (24120, "Reopen Crew Setup"), (24520, "200 assigned, none left over"), (25320, "Back in Nagasaki")),
    )
    entries = []
    for n, group in enumerate(groups, 1):
        sheet = Image.new("RGB", (768, 808), "#263238")
        draw = ImageDraw.Draw(sheet)
        for i, (frame, label) in enumerate(group):
            x, y = i % 3 * 256, i // 3 * 404
            sheet.paste(screens[frame], (x, y + 20))
            draw.text((x + 4, y + 4), label, fill="white")
        path = OUT.with_name(f"nagasaki_second_recruitment_current_{n}_20261124.png")
        sheet.save(path)
        entries.append(reference(path))
    return entries


def main():
    current = play.current
    release = read(current.RELEASE)
    assert digest(REGISTRY) == release["registry_sha256"] and digest(CLEAN) == release["clean_input_sha256"]
    assert digest(current.ROM) == release["candidate_sha256"]
    frames, calls, evidence, commands = capture(release)
    clean, image = map(NdsImage.open, (CLEAN, current.ROM))
    source_arm, arm = (rom.read_file(current.ARM) for rom in (clean, image))
    archive = image.read_file(current.COMMON)
    assert sha256(arm).hexdigest() == release["target_ARM9_sha256"] and sha256(archive).hexdigest() == release["target_COMMON_sha256"]
    source = earlier.base.common_message_entries(clean.read_file(current.COMMON), source_arm)
    installed = earlier.base.common_rows(archive, arm)
    font = GameAsciiFont.from_arm9(arm)
    screens = {frame: panels.picture(shot) for frame, shot in frames.items()}
    completed = dialogue(source, installed, frames, screens, calls, font)
    native = even_notice(source_arm, arm, frames, screens, font)
    packet = dict(translation_policy="natural-dialogue-v2", encoder="dialogue-relocatable-v1", target_locale="en-US",
        review_gates=list(GATES), candidate_sha256=release["candidate_sha256"], clean_input_sha256=release["clean_input_sha256"],
        ordinary_gameplay=True, records=completed, ARM9_even_notice=native, changes=measures(screens, frames, font),
        earlier_paired_replay=reference(play.PAIR), earlier_decline_review=reference(play.earlier.tavern.OUT),
        controller_commands=commands, evidence=evidence,
        observed_COMMON_ids=sorted({row["message_ID"] for row in calls}), archived_ids_seen=[],
        unvisited=["Other recruit amounts, policy orders, and voice variants", "Physical hardware"],
        ROM_changed=False, new_editorial_credit=0)
    validate_natural_dialogue_batch(packet)
    packet["contact_sheets"] = sheets(screens)
    write(OUT, packet)
    print(f"Verified the second recruitment branch with {len(completed)} COMMON retentions and the Even notice.")


if __name__ == "__main__":
    main()
