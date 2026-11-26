"""Bind the ordinary Tunis recruitment exchange and flagship preview to clean Japanese."""

from struct import unpack_from
from types import FunctionType, SimpleNamespace

from PIL import ImageChops

from dk4tool.dialogue.font_audit import GameAsciiFont
from dk4tool.dialogue.review import validate_natural_dialogue_batch
from dk4tool.script.common_message_table import common_message_entries
from scripts import observe_tunis_recruitment_20261125 as play
from scripts import verify_genoa_copenhagen_town_20261123 as panels
from scripts.stage_cartridge_title_20261123 import CLEAN, GATES, NdsImage, digest, read, reference, write


OUT = panels.OUT.with_name("tunis_recruitment_current_20261125.json")
TAVERN = "Tunis Tavern. Hodram declines the first quote, accepts the same quote when he returns, then declines to look for more sailors."
ASSIGN = "Assign Sailors. Hodram previews Flagship auto-assignment and declines the prompt to confirm the proposed allocation."
HOLDS = {
    51: ((4820,), "Barkeep", (), ("Welcome! What will you have?",), TAVERN,
         "The barkeep greets the customer and asks what he wants.",
         "The brief welcome introduces the menu, which includes recruiting as well as ordering a drink."),
    890: ((5640, 6460), "Charles Rochefort", ("1363",), ("I'll recruit crew for 1363 gold.",), TAVERN,
          "Charles offers to recruit sailors for the specified cost.",
          "The concise offer preserves Charles's first-person commitment and matches Recruit Crew. The whole price fits with its currency."),
    897: ((6680,), "Charles Rochefort", (), ("Who wants to sail with the Admiral?",), TAVERN,
          "Charles asks which patrons want to sail with the admiral.",
          "An open call fits the room. Admiral preserves his established address for Hodram."),
    907: ((6900,), "Patron", (), ("Aye!",), TAVERN,
          "The Tavern answers the recruiting call with assent.",
          "The brisk assent suits the seafaring setting and leads directly to the count of volunteers."),
    904: ((7120,), "Charles Rochefort", ("29",), ("We've got 29 willing to join.",), TAVERN,
          "Charles reports how many people volunteered to join.",
          "The spoken count makes the result clear after the response. The complete two-digit count fits inside the sentence."),
    1042: ((7340,), "Charles Rochefort", ("56",), ("There's room aboard for 56 more.", "Shall I keep looking?"), TAVERN,
           "Charles reports how many places remain and asks whether to keep recruiting.",
           "The spare capacity and the question have separate complete lines, and the polite question suits Charles."),
    11: ((8440,), "Charles Rochefort", (), ("Will this be all right?",), ASSIGN,
         "The prompt asks whether the proposed crew assignment is acceptable.",
         "The courteous check fits Charles's delivery and asks for approval after the player sees the proposed distribution."),
}


def review_common_holds(holds_by_message, source, installed, font, frames, screens, calls):
    records, figures = [], []
    for key, (holds, speaker, args, lines, context, meaning, reason) in holds_by_message.items():
        ja, text = source[key], installed[key]
        assert ja.text.count(b"%s") == text.text.count(b"%s") == len(args)
        formatted = (text.text % tuple(v.encode("ascii") for v in args)).decode("ascii")
        assert formatted.split() == " ".join(lines).split()
        observed = []
        for frame in holds:
            request = [r for r in calls if r["message_ID"] == key and 0 < frame - r["frame"] <= 220]
            assert len(request) == 2
            screen = screens[frame]
            observed.append(dict(capture=frames[frame], requests=request, body_ink=panels.exact_body(font, lines, screen),
                                 nameplate=panels.nameplate(font, speaker, screen)))
        src, target = (panels.text_reference(entry) | dict(exact_hex=entry.text.hex()) for entry in (ja, text))
        records.append(dict(id=f"COMMON_MESSAGE_{key}", message_ID=key, speaker=speaker, context=context, source_meaning=meaning,
            clean_Japanese=ja.text.decode("cp932"), english=text.text.decode("ascii").strip(),
            source_reference=src, current_reference=target, installed_reference=target, observations=observed,
            arguments=args, lines=lines, decision="retention", localization_note=reason, review=dict.fromkeys(GATES, True)))
        figures.append((f"{holds[0]} / COMMON {key}", screens[holds[0]]))
    return records, figures


def main():
    active = play.current
    release = read(active.RELEASE)
    assert digest(CLEAN) == release["clean_input_sha256"] and digest(active.ROM) == release["candidate_sha256"]
    scope = vars(panels) | dict(observed=SimpleNamespace(ROOT=play.ROOT.parent))
    frames, calls, evidence = FunctionType(panels.capture.__code__, scope)(play.ROOT.name, release)
    assert max(frames) == 8660
    assert [r["message_ID"] for r in calls[::2]] == [0, 51, 890, 890, 897, 907, 904, 1042, 11]
    for first, second in zip(calls[::2], calls[1::2], strict=True):
        assert first["PC"] == 0x0205528C and second == first | {"PC": 0x020534F4}

    original, current = map(NdsImage.open, (CLEAN, active.ROM))
    source_arm, arm = (image.read_file(active.ARM) for image in (original, current))
    jp = common_message_entries(original.read_file(active.COMMON), source_arm)
    en = panels.common_rows(current.read_file(active.COMMON), arm)
    font = GameAsciiFont.from_arm9(arm)
    screens = {frame: panels.picture(shot) for frame, shot in frames.items()}
    records, figures = review_common_holds(HOLDS, jp, en, font, frames, screens, calls)

    pointer = unpack_from("<I", arm, 0x1E278)[0]
    assert pointer == unpack_from("<I", source_arm, 0x1E278)[0]
    offset = pointer - 0x02000000
    ja, en_flagship = (data[offset:offset + 128].split(b"\0")[0] for data in (source_arm, arm))
    notice = "Assigned to flagship first."
    assert en_flagship.decode("ascii").strip() == notice
    src = dict(offset=offset, exact_hex=ja.hex())
    installed = dict(offset=offset, exact_hex=en_flagship.hex())
    records.append(dict(id="ARM9_ASSIGN_SAILORS_FLAGSHIP_NOTICE", context=ASSIGN, speaker="Charles Rochefort",
        clean_Japanese=ja.decode("cp932"), english=notice,
        source_meaning="The notice says that assigning sailors gives the flagship priority.",
        source_reference=src, current_reference=installed, installed_reference=installed, pointer_offset=0x1E278,
        observations=[dict(capture=frames[8000], nameplate=panels.nameplate(font, "Charles Rochefort", screens[8000]),
                           body_ink=panels.exact_body(font, (notice,), screens[8000]))],
        decision="retention", localization_note="Flagship first succinctly reports the selected policy. The preview gives the flagship all 29 recruits.",
        review=dict.fromkeys(GATES, True)))
    figures.append(("8000 / Flagship assignment notice", screens[8000]))
    choices = {frame: [
        panels.find_mask(font, label, screens[frame], bounds) for label, bounds in (
            ("No", (126, 359, 172, 377)), ("Yes", (196, 359, 237, 377)))]
        for frame in (5640, 6460, 7340, 8440)}
    assert all(all(result) for result in choices.values())
    assert all(panels.find_mask(font, "7056", screens[frame], (78, 349, 136, 367)) for frame in (4200, 5860))
    blink = ImageChops.difference(screens[8220], screens[8660]).getbbox()
    assert blink == (32, 208, 256, 240)
    batch = dict(translation_policy="natural-dialogue-v2", target_locale="en-US", encoder="dialogue-relocatable-v1",
        review_gates=list(GATES), records=records, candidate_sha256=release["candidate_sha256"], ordinary_gameplay=True,
        evidence=evidence, choices=choices, quote_decline_wallet=7056,
        assignment_return=dict(frames=[8220, 8660], changing_selection_highlight_bounds=blink),
        controller_commands=[r["command"] for r in read(evidence["journal"]["path"])["commands_received"]],
        assignment_preview=dict(before=frames[7560], after=frames[8220], fleet_crew=[39, 68], unassigned=[29, 0]),
        unvisited=["Second recruitment in Tunis", "Accepting this final assignment", "Strategist options", "Physical hardware"],
        ROM_changed=False, new_editorial_credit=0)
    validate_natural_dialogue_batch(batch)
    sheets = panels.sheets_for("tunis_recruitment_current_20261125", figures)
    sheets += panels.sheets_for("tunis_recruitment_assignment_20261125", [
        ("Before Flagship / 39 aboard, 29 unassigned", screens[7560]),
        ("Flagship preview / 68 aboard, 0 unassigned", screens[8660]),
    ], crop=(0, 192, 256, 384))
    write(OUT, batch | {"figures": sheets})
    print("Verified eight Tunis recruiting and assignment retentions through ordinary play.")


if __name__ == "__main__":
    main()
