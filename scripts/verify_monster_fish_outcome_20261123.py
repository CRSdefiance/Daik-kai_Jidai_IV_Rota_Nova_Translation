"""Verify the Monster Fish outcome, Hodram's elegy and the return to sailing."""

from pathlib import Path
from struct import unpack_from

from PIL import Image, ImageDraw

from dk4tool.dialogue.font_audit import GameAsciiFont
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.script.common_message_table import common_message_entries
from scripts import replay_monster_fish_outcome_20261123 as replay
from scripts.stage_azores_wording_20261123 import ARM, COMMON, common_rows
from scripts.stage_cartridge_title_20261123 import CLEAN, REGISTRY, NdsImage, digest
from scripts.stage_cartridge_title_20261123 import read, reference, sha256, write
from scripts.verify_captain_biographies_v1 import captured
from scripts.verify_confirmed_name_widget_pixels_v198 import complete_mask
from scripts.verify_lisbon_azores_voyage_20261123 import INK, glyphs
from scripts.verify_monster_fish_transition_20261123 import battle_state
from scripts.verify_stock_encounter_names_20261121 import read_ram


OUT = Path("translations/editorial_checkpoints/shared_display_20261123/monster_fish_outcome_current_20261123.json")
SHEET = OUT.with_suffix(".png")
STORY = "/data/SC1.DK4"
STORY_REVIEW = Path("releases/all_routes_editorial_20261122_hodram_B0_B23_candidate/verification/registered_review.json")
VICTORY_REVIEW = Path("releases/all_routes_editorial_20261119_battle_dialogue_followup_candidate/verification/registered_review.json")
HOLDS = (9450, 9760, 10140, 10480, 10640, 10800, 10960, 11120, 11280, 11440,
         11600, 11760, 11920, 12080)
BASE = replay.BASE


class Capture:
    def __init__(self, label, release):
        directory = replay.ROOT / label
        self.report = directory / "capture/capture_report.json"
        self.inputs = directory / "controller.jsonl"
        self.data = read(self.report)
        assert self.data["ROM_sha256"] == release["candidate_sha256"]
        assert self.data["cold_boot"] and not self.data["savestate_loaded"] and not self.data["callback_errors"]
        donor = self.data["battery_save_preloaded"]
        assert donor["copied_byte_exact_before_cold_boot"] and digest(donor["source"]) == donor["source_sha256"]
        self.frames = {row["frame"]: row for row in self.data["frames_captured"]
                       if row["path"].endswith("_navigation.png")}
        self.ram = {row["frame"]: row for row in self.data["read_only_pause_RAM_snapshots"]}


def text_body(font, screen, lines):
    assert 1 <= len(lines) <= 4
    result, mask = [], set()
    for i, line in enumerate(lines):
        y = 297 + i * 16
        options = []
        for x in (16, 22):
            try:
                pixels, bounds = complete_mask(font, line, screen, x, y, INK)
            except ValueError:
                continue
            options.append((x, pixels, bounds))
        (x, pixels, bounds), = options
        mask.update((x + dx, y + dy) for dx, dy in glyphs(font, line))
        assert all(16 <= xx < 245 and 296 <= yy < 359 for xx, yy in mask)
        result.append(dict(line=line, origin=[x, y], ink=pixels, bounds=bounds))
    actual = {(x, y) for x in range(16, 245) for y in range(296, 359) if screen.getpixel((x, y)) == INK}
    assert actual == mask
    return result


def panel(run, frame, font, buffer, speaker, expected):
    raw = read_ram(run.ram[frame])
    actual, nul, _ = raw[buffer:buffer + 512].partition(b"\0")
    assert nul and actual == expected, (frame, actual, expected)
    lines = [line.strip().decode("ascii") for line in actual.split(b"\n")]
    assert all(lines)
    screen = captured(run.frames[frame])
    name_ink, name_bounds = complete_mask(font, speaker, screen, 16, 277, (98, 97, 98))
    check = text_body(font, screen, lines)
    return dict(frame=frame, speaker=speaker, lines=lines, formatted_hex=actual.hex(), page=1,
                nameplate=dict(ink=name_ink, bounds=name_bounds), body=check,
                snapshot=run.ram[frame], screenshot=run.frames[frame]), screen


def common_ref(entry):
    return dict(file=COMMON, block=entry.block, block_offset=entry.block_offset,
                table_offset=entry.table_offset, exact_hex=entry.text.hex())


def verify_victory(run, arm, clean, rom, stock, font, buffer):
    source = common_message_entries(stock.read_file(COMMON), clean)
    installed = common_rows(rom.read_file(COMMON), arm)
    row = next(r for r in read(VICTORY_REVIEW)["records"] if r["message_ID"] == 2188)
    source_entry, installed_entry = source[2188], installed[2188]
    assert source_entry.text.hex() == row["source_hex"]
    assert installed_entry.text.hex() == row["staged_hex"] and installed_entry.text.count(b"%s") == 1
    owner = unpack_from("<I", arm, 0x552A0)[0] - BASE
    raw = read_ram(run.ram[9180])
    assert raw[owner + 0x2030:owner + 0x2230].split(b"\0")[0] == installed_entry.text
    record, screen = panel(run, 9180, font, buffer, "Gerhard Adernkatz", b" Monster Fish down!")
    record.update(message_ID=2188, source=common_ref(source_entry), installed=common_ref(installed_entry),
                  Japanese=source_entry.text.decode("cp932"), native_argument="Monster Fish",
                  editorial_decision="retention", reason="Gerhard's clipped report preserves the original victory and names the defeated encounter without adding a claim about the creature's fate.",
                  review=row["review"])
    assert all(record["review"].values())
    return record, screen


def verify_story(run, rom, stock, font, buffer):
    archive = rom.read_file(STORY)
    source = stock.read_file(STORY)
    current_block = IlnkContainer.parse(archive).blocks[16]
    source_block = IlnkContainer.parse(source).blocks[16]
    rows = [row for row in read(STORY_REVIEW)["records"] if row["block"] == 16]
    assert len(rows) == len(HOLDS) == 14
    records, images = [], []
    for row, frame in zip(rows, HOLDS, strict=True):
        original = row["source_reference"]
        earlier = row["registered_reference"]
        assert sha256(source_block).hexdigest() == original["block_sha256"]
        assert sha256(current_block).hexdigest() == earlier["block_sha256"]
        assert sha256(source).hexdigest() == original["archive_sha256"]
        raw_source = bytes.fromhex(row["source_hex"])
        assert source_block[original["offset"]:original["offset"] + len(raw_source)] == raw_source
        command = bytes.fromhex(earlier["exact_command_hex"])
        offset = earlier["command_offset"]
        assert current_block[offset:offset + len(command)] == command
        stored = bytes.fromhex(earlier["exact_stored_hex"])
        assert raw_source[0] == stored[0]  # Native story speaker byte.
        assert " ".join(stored[1:].decode("ascii").split()) == row["english"]
        record, screen = panel(run, frame, font, buffer, row["speaker"], stored[1:])
        installed = dict(earlier, candidate_sha256=run.data["ROM_sha256"],
                         archive_sha256=sha256(archive).hexdigest())
        record.update(id=row["id"], source=original | dict(exact_stored_hex=row["source_hex"]),
                      installed=installed, Japanese=row["Japanese"], reason=row["localization_note"],
                      prior_editorial_decision=row["decision"], review=row["review"])
        assert all(record["review"].values())
        records.append(record)
        images.append(screen)
    return records, images


def contact_sheet(records, images):
    assert len(records) == len(images)
    sheet = Image.new("RGB", (3 * 512, ((len(images) + 2) // 3) * 412), (20, 23, 27))
    draw = ImageDraw.Draw(sheet)
    for index, (row, screen) in enumerate(zip(records, images, strict=True)):
        x, y = (index % 3) * 512, (index // 3) * 412
        label = "COMMON 2188" if index == 0 else row["id"].replace("DK4_MES_", "")
        draw.text((x + 12, y + 7), f"{label} / Frame {row['frame']}", fill=(250, 250, 250))
        sheet.paste(screen.crop((0, 192, 256, 384)).resize((512, 384), Image.Resampling.NEAREST), (x, y + 24))
    sheet.save(SHEET)


def main():
    release = read(replay.RELEASE)
    assert digest(release["candidate"]) == release["candidate_sha256"]
    assert digest(CLEAN) == release["clean_input_sha256"] and digest(REGISTRY) == release["registry_sha256"]
    inactive, early, outcome = (Capture(case, release) for case in ("hull_3", "active_hull_3", "outcome_verified"))
    assert len({c.data["battery_save_preloaded"]["source_sha256"] for c in (inactive, early, outcome)}) == 1
    assert inactive.data["frames"] == 9850 and early.data["frames"] == 11260 and outcome.data["frames"] == 12400
    prep, activation = outcome.data["synthetic_condition_fixtures"]
    assert prep["frame"] == 4800 and prep["added_fixture"]["supplied_hull"] == 3
    assert prep["after_RAM_sha256"] == inactive.data["synthetic_condition_fixtures"][0]["after_RAM_sha256"]
    early_activation = early.data["synthetic_condition_fixtures"][0]["original_activation_tail"]
    late_activation = activation["original_activation_tail"]
    for field in ("address", "original_start", "original_end", "original_hex", "original_predicate"):
        assert early_activation[field] == late_activation[field]
    assert early_activation["before"] ^ early_activation["after"] == 1
    assert activation["no_outcome_or_text_supply"] and activation["frame"] == 9030
    assert activation["changes"] == [{"address": activation["owned_bytes"][0], "before": 13, "after": 12}]
    assert inactive.ram[9030]["sha256"] == outcome.ram[9030]["sha256"] == activation["before_RAM_sha256"]

    rom, stock = map(NdsImage.open, (release["candidate"], CLEAN))
    arm, clean = (image.read_file(ARM) for image in (rom, stock))
    assert sha256(arm).hexdigest() == release["target_ARM9_sha256"]
    spans = [(0x0202E9AC, 0x0202E9BC), (0x0202BDD8, 0x0202BDEC), (0x0207270C, 0x020727EC)]
    verified = []
    for lo, hi in spans:
        data = arm[lo - BASE:hi - BASE]
        assert data == clean[lo - BASE:hi - BASE]
        verified.append(dict(start=lo, end=hi, exact_hex=data.hex(), sha256=sha256(data).hexdigest()))

    frames = (6750, 8640, 8870, 9030, 9180, 9450, 12240, 12400)
    states = {n: battle_state(arm, read_ram(outcome.ram[n])) for n in frames}
    assert [states[n]["target"]["hull"] for n in (6750, 8640, 8870, 9030)] == [3, 3, 1, 0]
    assert states[9180]["target"]["mobile"] and not states[9450]["target"]["mobile"]
    assert not states[12240]["target"]["mobile"] and not states[12400]["target"]["mobile"]
    assert all(states[n]["context"][:3] == (0, 0, 0) for n in (12240, 12400))
    assert states[12400]["calendar_tick"] > states[12240]["calendar_tick"] > states[9450]["calendar_tick"]
    assert states[12400]["own"]["position"] != states[12240]["own"]["position"]
    hold = battle_state(arm, read_ram(inactive.ram[9850]))
    assert hold["target"]["hull"] == 0 and hold["target"]["mobile"] and hold["context"] == states[9030]["context"]
    font = GameAsciiFont.from_arm9(arm)
    buffer = unpack_from("<I", arm, 0x54450)[0] - BASE
    victory, screen = verify_victory(outcome, arm, clean, rom, stock, font, buffer)
    story, images = verify_story(outcome, rom, stock, font, buffer)
    contact_sheet([victory, *story], [screen, *images])
    first, second, final = story[7:10]
    assert first["id"].endswith("R0032") and first["lines"][1] == "The waves lap"
    first["wrap_finding"] = "A 13-character line splits the verb from its familiar rhythm while the body fills four lines."
    second["retention_reason"] = "The attribution gives the speaker a natural pause before he reports what he has heard about the two words."
    assert final["id"].endswith("R0039") and final["lines"][0].endswith(" Both")
    final["wrap_finding"] = "Both lands alone after the completed refrain, separated from its verb."
    return_captures = [outcome.frames[n] for n in (12240, 12400)]
    for row in return_captures:
        captured(row)
    write(OUT, dict(registered_release=reference(replay.RELEASE), candidate_sha256=release["candidate_sha256"],
                   reused_story_review=reference(STORY_REVIEW), reused_special_victory_review=reference(VICTORY_REVIEW),
                   controlled_runs=[dict(report=reference(c.report), inputs=reference(c.inputs))
                                    for c in (inactive, early, outcome)],
                   paired_same_pre_activation_snapshot=outcome.ram[9030], exact_native_code=verified,
                   initial_hull_fixture=prep["added_fixture"], in_battle_activation_fixture=activation,
                   source_states=states, inactive_control_at_9850=hold, victory=victory, story=story,
                   actual_return_to_Sea_View=return_captures, contact_sheet=reference(SHEET),
                   ordinary_in_game_inputs_after_fixtures=True, natural_spawn_or_unmodified_battle_unverified=True,
                   newly_identified_wraps=[first["id"], final["id"]], new_edit_or_ROM_change=False, new_editorial_credit=0))
    print("Verified Monster Fish victory, 14 Hodram story pages, and the return to sailing.")


if __name__ == "__main__":
    main()
