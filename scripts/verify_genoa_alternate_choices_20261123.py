"""Verify the two remaining Genoa choices, their full exchanges, and the Tavern return."""

from collections import Counter
from types import FunctionType, SimpleNamespace

from dk4tool.dialogue.font_audit import GameAsciiFont
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.script.common_message_table import common_message_entries
from scripts import replay_genoa_alternate_choices_20261123 as replay
from scripts import verify_genoa_copenhagen_town_20261123 as gameplay
from scripts.reconcile_elegy_acceptance_20261123 import common_rows
from scripts.review_current_story_wraps_20261122 import display as story_display, layout
from scripts.seal_shared_text_source_v1 import reference as text_reference
from scripts.stage_cartridge_title_20261123 import CLEAN, GATES, REGISTRY, NdsImage, digest, read, reference, sha256, write
from scripts.verify_azores_return_20261123 import picture, shots
from scripts.verify_moonlit_violin_20261121 import bytes_for


OUT = gameplay.OUT.with_name("genoa_alternate_choices_20261123.json")
PAGES = {
    "no_liquor": (181, 184, 188, 192, 196, 200, 203, 207, 211),
    "test_julio": (133, 136, 139, 145, 149, 153, 157, 160, 164, 168, 172),
}
OPTIONS = {"no_liquor": ("Yes...", "No."), "test_julio": ("Ask what you don't know", "Test him on what you know.")}
PROPOSALS = {
    136: ("A contrary fellow like you needs a proper education. First, how to spot a good drink.",
          ("A contrary fellow like you", "needs a proper education.", "First, how to spot a good drink."),
          "Julio takes charge after he recognizes the test. Give his first lesson a complete line and keep the comic promise to educate Hodram."),
    181: (None, ("on account of my age.", "Come on, out with it!"),
          "Keep Julio's suspicion and his increasingly impatient demand. Put the entire final demand together."),
    184: ("Well... I thought I'd look for some on our voyage.", ("on our voyage.",),
          "Hodram hesitantly says he plans to look for better liquor during the voyage. His mention of sailing still prompts Julio's excitement."),
    211: (None, ("I look forward to sailing with you!",),
          "Give Julio's full name room as its own introduction. Keep his greeting about sailing together intact."),
}
TAVERN_RETURN = {
    341: ("", ("Julio Erneco",), ("Julio Erneco joined!",),
          "The notice uses the complete name and confirms the result after Hodram agrees."),
    51: ("Barkeep", (), ("Welcome! What will you have?",),
         "The short greeting hands control back to the player at the ordinary Tavern."),
}


def capture(branch, release):
    folder = replay.ROOT / branch
    path = folder / "capture/capture_report.json"
    plan_file = folder / "replay_plan.json"
    run, plan = read(path), read(plan_file)
    assert plan == replay.plan(branch, release)
    assert run["ROM_sha256"] == release["candidate_sha256"]
    assert run["cold_boot"] and not run["savestate_loaded"] and not run["callback_errors"]
    assert not any(value for key, value in run.items() if key.startswith("synthetic_"))
    assert run["frames"] == plan["captures"][-1] and run["exact_requested_capture_frames"] == plan["captures"]
    assert run["scripted_input_schedule"] == plan["controls"]
    assert run["battery_save_preloaded"]["copied_byte_exact_before_cold_boot"]
    assert run["battery_save_preloaded"]["source_sha256"] == plan["donor"]["sha256"]
    return plan, shots(run, "_cold_boot.png"), [reference(item) for item in (path, plan_file, folder / "inputs.json")]


def choice(branch, font, frames, plan, choices, clean, block):
    default, selected = (picture(frames[plan[key]]) for key in ("menu", "selected"))
    records = [next(row for row in choices if row["english"] == label) for label in OPTIONS[branch]]
    evidence = []
    for idx, row in enumerate(records):
        label, ref = row["english"], row["registered_reference"]
        command = gameplay.exact_command(block, ref)
        assert command[:4] == b"\x00\x21\x00\x00"
        assert block[ref["offset"]:ref["offset"]+len(label)+1] == label.encode("ascii") + b"\0"
        source = row["source_reference"]
        start, body = source["offset"], bytes.fromhex(source["exact_body_hex"])
        assert clean[start:start + len(body)] == body and sha256(clean).hexdigest() == source["block_sha256"]
        screens = []
        for screen in (default, selected):
            mask = gameplay.find_line(font, label, screen, range(37, 128),
                                      range(269+20*idx, 277+20*idx), (8, 8, 8))
            ink = Counter(screen.crop(tuple(mask[1])).get_flattened_data())
            highlighted = ink[(0, 165, 172)] > 0
            screens.append(dict(complete_native_label_mask=mask, highlighted=highlighted))
        assert screens[0]["highlighted"] == (idx == 0) and screens[1]["highlighted"] == (idx == 1)
        evidence.append(dict(id=row["id"], english=label, Japanese=row["Japanese"], slot=idx,
            source_reference=row["source_reference"], registered_reference=ref, selected=idx == 1,
            before_direction_input=screens[0], after_direction_input=screens[1],
            rationale=row["localization_note"], review=row["review"]))
    return dict(labels=evidence, default_frame=frames[plan["menu"]], selected_frame=frames[plan["selected"]]), selected


def story_panel(row, frame, before, after, arm, kanji, renderer, font):
    source, registered = (gameplay.exact_command(block, row[key]) for block, key in (
        (before, "source_reference"), (after, "registered_reference")))
    assert source[:6] == registered[:6]
    assert set(row["review"]) == set(GATES) and all(row["review"].values())
    raw = bytes_for(registered)
    rendered = renderer(arm, kanji, raw)
    page, = rendered["pages"]
    assert rendered["complete_consumed_bytes"] == len(raw) and page["native_independent_plane_equal"]
    plane = bytes.fromhex(page["native_plane_hex"])
    screen = picture(frame)
    assert gameplay.mask_check(plane, 216, screen), (row["id"], frame["frame"])
    number = int(row["id"].rsplit("_R", 1)[1])
    proposal = PROPOSALS.get(number)
    result = dict(id=row["id"], block=170, speaker=row["speaker"], clean_Japanese=row["Japanese"],
        source_reference=row["source_reference"], installed_reference=row["registered_reference"],
        installed_English=raw.decode("ascii"), source_meaning=row["source_meaning"], context=row["context"],
        decision="revision proposed" if proposal else "retention",
        rationale=proposal[2] if proposal else row["localization_note"], frame=frame,
        full_page_sha256=sha256(plane).hexdigest(), full_nameplate=gameplay.nameplate(font, row["speaker"], screen),
        review=row["review"] | ({"formatting": False} if proposal else {}))
    return result, raw, bytes_for(source), registered[5], screen


def preflight(row, raw, source, selector, ctx, kanji, renderer):
    number = int(row["id"].rsplit("_R", 1)[1])
    wording, phrases, _ = PROPOSALS[number]
    draft = wording or " ".join(raw.decode("ascii").split())
    body, plan = layout.plan_progressive(dict(id=row["id"], english=draft, protected_phrases=phrases),
                                         selector, raw, source)
    assert plan["expected_native_pages"] == 1
    page, = story_display.display.raster(ctx, kanji, renderer, body, plan["lines"], 1)
    assert page["native_independent_plane_equal"]
    plane = bytes.fromhex(page["native_plane_hex"])
    row.update(proposed_English=draft, protected_phrases=phrases, offline_preflight=dict(
        formatter_plan=plan, native_plane_sha256=sha256(plane).hexdigest(), physical_source_and_installed_selectors=selector,
        fits_current_text_bytes=len(body) <= len(raw), stored_and_gameplay_checks_pending=True))
    return row["id"], plane


def shared_holds(plan, frames, font, source, installed, count):
    labels, pictures = [], []
    for key, hold in zip(TAVERN_RETURN, plan["holds"][count:count + 2], strict=True):
        name, substitutions, lines, reason = TAVERN_RETURN[key]
        original, current = source[key], installed[key]
        assert original.text.count(b"%s") == current.text.count(b"%s") == len(substitutions)
        text = current.text % tuple(value.encode("ascii") for value in substitutions)
        assert text.decode("ascii").split() == " ".join(lines).split()
        screen = picture(frames[hold])
        labels.append(dict(message_ID=key, source_reference=text_reference(original), installed_reference=text_reference(current),
            Japanese=original.text.decode("cp932"), installed_English=current.text.decode("ascii"),
            runtime_substitutions=substitutions, full_body_ink=gameplay.exact_body(font, lines, screen),
            full_nameplate=gameplay.nameplate(font, name, screen), frame=frames[hold],
            rationale=reason, review=dict.fromkeys(GATES, True)))
        pictures.append((f"COMMON {key}", screen))
    return labels, pictures


def main():
    current = replay.current
    release = read(current.RELEASE)
    assert digest(current.ROM) == release["candidate_sha256"] and digest(REGISTRY) == release["registry_sha256"]
    assert digest(CLEAN) == release["clean_input_sha256"]
    review = read(current.REVIEW)
    assert review["candidate_sha256"] == release["candidate_sha256"]
    package = read(current.PACKAGE / "checksums.json")
    assert digest(current.REVIEW) == package["verification/registered_review.json"]
    clean, rom = map(NdsImage.open, (CLEAN, current.ROM))
    arm, kanji = (rom.read_file(path) for path in (current.ARM, "/GRP/KANJI.FNT"))
    ctx = SimpleNamespace(arm=arm, image=rom)
    font = GameAsciiFont.from_arm9(arm)
    renderer = gameplay.town.clipped_renderer(ctx)
    before, after = [IlnkContainer.parse(image.read_file(current.STORY)).blocks[170] for image in (clean, rom)]
    source = common_message_entries(clean.read_file(current.COMMON), clean.read_file(current.ARM))
    installed = common_rows(rom.read_file(current.COMMON), arm)
    old = shots(read(replay.previous.CAPTURE), "_cold_boot.png")
    choices = [row for row in review["records"] if row["block"] == 170 and row["id"].startswith("SC1_B170_CHOICE_")]
    rows = {int(row["id"].rsplit("_R", 1)[1]): row for row in review["records"]
            if row["block"] == 170 and "_R" in row["id"]}
    results, previews = {}, []
    for branch, numbers in PAGES.items():
        plan, frames, evidence = capture(branch, release)
        controls = (3500, 5800, 9700, plan["menu"])
        assert all(picture(frames[hold]).tobytes() == picture(old[hold]).tobytes() for hold in controls)
        selection, menu = choice(branch, font, frames, plan, choices, before, after)
        records, figures = [], [(f"{branch} / lower entry selected", menu)]
        for number, hold in zip(numbers, plan["holds"][:len(numbers)], strict=True):
            result, raw, jp, selector, screen = story_panel(rows[number], frames[hold], before, after,
                                                           arm, kanji, renderer, font)
            if number in PROPOSALS:
                previews.append(preflight(result, raw, jp, selector, ctx, kanji, renderer))
            records.append(result)
            figures.append((result["id"], screen))
        shared, pair = shared_holds(plan, frames, font, source, installed, len(numbers))
        figures.extend(pair)
        results[branch] = dict(evidence=evidence, unchanged_control_frames=list(controls), choice=selection, story=records,
            shared=shared, ordinary_tavern_return=True, gameplay_sheets=gameplay.sheets_for(f"genoa_{branch}", figures))
    directory = OUT.with_name("genoa_alternate_choice_previews_20261123")
    directory.mkdir(exist_ok=True)
    contact = story_display.display.inherited.early.contact_sheets
    sheets = FunctionType(contact.__code__, contact.__globals__ | {"ROOT": directory})(previews)
    assert len(previews) == len(PROPOSALS) and len(sheets) == 1
    proof = dict(candidate_sha256=release["candidate_sha256"], release=reference(current.RELEASE),
                 fresh_ordinary_input_runs=2, verified_story_holds=sum(map(len, PAGES.values())),
                 new_editorial_credit=0, changed_ROM=False, choice_paths=results, offline_proposed_pages=sheets)
    write(OUT, proof)
    print(f"Verified both alternate recruitment outcomes, {proof['verified_story_holds']} story holds and {len(previews)} offline drafts.")


if __name__ == "__main__":
    main()
