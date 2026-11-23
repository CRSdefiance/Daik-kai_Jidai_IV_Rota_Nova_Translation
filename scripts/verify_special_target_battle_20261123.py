"""Bind the focused declaration stall to the captured frames and original text."""

from pathlib import Path
from struct import unpack_from

from PIL import Image, ImageDraw

from dk4tool.dialogue.font_audit import GameAsciiFont
from dk4tool.script.common_message_table import common_message_entries
from scripts.play_special_target_battle_20261123 import CLEAN, PREDECESSOR, RELEASE, ROOT
from scripts.stage_azores_wording_20261123 import ARM, BASE, COMMON, common_rows, digest_bytes
from scripts.stage_cartridge_title_20261123 import NdsImage, REGISTRY, digest, read, reference, write
from scripts.verify_captain_biographies_v1 import captured
from scripts.verify_confirmed_name_widget_pixels_v198 import complete_mask
from scripts.verify_lisbon_azores_voyage_20261123 import body_mask
from scripts.verify_personal_gameplay_v841 import get_machine
from scripts.verify_stock_encounter_names_20261121 import read_ram


OUT = Path("translations/editorial_checkpoints/shared_display_20261123")
SPEAKER = "Gerhard Adernkatz"
LINES = ("All hands to battle stations...", "Let's go!")
RUNS = {
    "fish_approach": (7110, 7250, 7400, 8770, 10100),
    "fish_close": (6810, 6950, 7150, 8050, 8750),
    "predecessor_fish_approach": (7110, 7250, 7400, 8770, 10100),
    "clean_fish_approach": (6750, 7110, 7250, 10100),
}


def message_reference(row):
    return dict(file=COMMON, message_ID=row.message_id, block=row.block, offset=row.block_offset,
                table_offset=row.table_offset, exact_hex=row.text.hex())


def state(arm, snapshot, table):
    raw = read_ram(snapshot)
    cpu, get = get_machine(arm, raw)
    battle, fleet, actors = (get(offset) for offset in (0x3F0F8, 0xCB1A8, 0xCB184))
    actor = get(0x82478, fleet + 0x2090, 1)
    assert actor == 16
    message = get(0x53F4C, actors + 4 + actor * 32, table)
    assert message == 1890
    return dict(battle_context_address=battle, context_words=unpack_from("<5I", raw, battle - BASE + 8),
                party_hex=bytes(cpu.mem_read(fleet + 0x2084, 4)).hex(),
                first_mate_actor=actor, selected_COMMON_ID=message)


def verify_run(label, numbers, expected_rom, arm, font, table):
    run = ROOT / label
    path = run / "capture/capture_report.json"
    report = read(path)
    assert report["ROM_sha256"] == expected_rom and report["frames"] == numbers[-1]
    assert report["cold_boot"] and not report["savestate_loaded"] and not report["callback_errors"]
    donor = report["battery_save_preloaded"]
    assert donor["copied_byte_exact_before_cold_boot"] and digest(donor["source"]) == donor["source_sha256"]
    fixture, = report["synthetic_condition_fixtures"]
    assert fixture["frame"] == 4800 and fixture["original_existing_model_ID"] == 149
    assert fixture["all_other4MiB_bytes_exact"] and fixture["no_message_ID_renderer_actor_identity_or_result_injected"]
    assert not report["natural_condition_event_verified"]
    frames = {r["frame"]: r for r in report["frames_captured"] if r["path"].endswith("_navigation.png")}
    images = {n: captured(frames[n]) for n in numbers}
    evidence = dict(capture=reference(path), commands=reference(run / "controller.jsonl"),
                    rom_sha256=expected_rom, source_battery=reference(donor["source"]),
                    fixture_frame=4800, fixture_sha256=fixture["fixture_sha256"],
                    frames={n: frames[n] for n in numbers})
    if label == "clean_fish_approach":
        evidence["observation"] = "Japanese controller timing reached the Speyer story prelude instead."
        return evidence, images
    declare, reply, stall, *later = numbers
    assert all(images[n].tobytes() == images[stall].tobytes() for n in later)
    assert images[reply].crop((0, 192, 256, 384)).tobytes() == images[stall].crop((0, 192, 256, 384)).tobytes()
    assert len({images[n].crop((0, 0, 256, 192)).tobytes() for n in (declare, reply, stall)}) == 3
    ink, bounds = complete_mask(font, SPEAKER, images[reply], 16, 277, (98, 97, 98))
    evidence["reply"] = dict(frame=reply, lines=body_mask(font, images[reply], LINES),
                             speaker=SPEAKER, nameplate_pixels=ink, nameplate_bounds=bounds)
    snapshots = {r["frame"]: r for r in report["read_only_pause_RAM_snapshots"]}
    states = {n: state(arm, snapshots[n], table) for n in (declare, reply, stall, numbers[-1])}
    for n in (declare, reply):
        assert states[n]["context_words"][:3] == (0, 0, 0)
        assert states[n]["party_hex"] == "27010102"
    for n in (stall, numbers[-1]):
        assert states[n]["context_words"] == (0, 1, 39, 181, 21)
        assert states[n]["party_hex"] == "27020102"
    evidence["read_only_state"] = {n: dict(snapshot=snapshots[n], **value) for n, value in states.items()}
    evidence["observed"] = dict(declaration=declare, battle_stations=reply,
                                instruction_overlay_persists_from=stall, last_checked_frame=numbers[-1],
                                combat_and_result_screen_observed=False)
    return evidence, images


def main():
    out = OUT / "special_target_battle_20261123.json"
    release, parent = read(RELEASE), read(PREDECESSOR)
    assert digest(REGISTRY) == release["registry_sha256"]
    for build in (release, parent):
        assert digest(build["candidate"]) == build["candidate_sha256"]
    assert digest(CLEAN) == release["clean_input_sha256"]
    assert release["predecessor"]["candidate_sha256"] == parent["candidate_sha256"]
    current, predecessor, clean = [NdsImage.open(p) for p in (release["candidate"], parent["candidate"], CLEAN)]
    arm, original = current.read_file(ARM), clean.read_file(ARM)
    assert arm == predecessor.read_file(ARM) and digest_bytes(arm) == release["target_ARM9_sha256"]
    table, = unpack_from("<I", arm, 0x6F0B8)
    assert table == 0x02117440 and arm[0x6F0B8:0x6F0BC] == original[0x6F0B8:0x6F0BC]
    table_offset = table - BASE
    assert arm[table_offset:table_offset + 32] == original[table_offset:table_offset + 32]
    assert unpack_from("<8I", arm, table_offset) == tuple(range(1889, 1897))
    jp = common_message_entries(clean.read_file(COMMON), original)[1890]
    installed = common_rows(current.read_file(COMMON), arm)[1890]
    assert installed == common_rows(predecessor.read_file(COMMON), arm)[1890]
    assert installed.text.decode("ascii").strip() == " ".join(LINES)
    assert jp.text.decode("cp932") == "総員戦闘態勢…、行くぞ！"
    font = GameAsciiFont.from_arm9(arm)
    expected = (release["candidate_sha256"], release["candidate_sha256"], parent["candidate_sha256"],
                release["clean_input_sha256"])
    runs, images = {}, {}
    for (label, frames), rom in zip(RUNS.items(), expected, strict=True):
        runs[label], images[label] = verify_run(label, frames, rom, arm, font, table)
    current_frames, parent_frames = (runs[k]["frames"] for k in ("fish_approach", "predecessor_fish_approach"))
    assert all(current_frames[n]["PNG_sha256"] == parent_frames[n]["PNG_sha256"] for n in current_frames)
    assert runs["fish_approach"]["commands"]["sha256"] == runs["predecessor_fish_approach"]["commands"]["sha256"]
    assert runs["fish_approach"]["commands"]["sha256"] == runs["clean_fish_approach"]["commands"]["sha256"]
    sheet = Image.new("RGB", (1560, 804), "#263238")
    draw = ImageDraw.Draw(sheet)
    for i, (frame, caption) in enumerate(((7110, "Declare War Mode"), (7250, "Gerhard's battle order"),
                                         (7400, "The instructions return over Sea View"))):
        x = 4 + 520 * i
        draw.text((x, 8), caption, fill="white")
        sheet.paste(images["fish_approach"][frame].resize((512, 768), Image.Resampling.NEAREST), (x, 27))
    sheet.save(out.with_suffix(".png"))
    write(out, dict(release=reference(RELEASE), predecessor=reference(PREDECESSOR), runs=runs,
          paired_identical_frame_numbers=list(current_frames), contact_sheet=reference(out.with_suffix(".png")),
          readiness=dict(source=message_reference(jp), installed=message_reference(installed),
                         Japanese=jp.text.decode("cp932"), current=" ".join(LINES),
                         caller_address=0x0206EF44, table=table, decision="retain",
                         reason="The idiomatic all-hands order and determined follow-up retain the Japanese pace and intent.",
                         gates=dict(source=True, context=True, localization=True, naturalness=True, formatting=True)),
          coverage="Focused emulator with a stock encounter initialized by a disclosed fixture.",
          original_cause_established=False, natural_spawn=False, natural_victory=False,
          new_review_credits=0, ROM_changed=False, full_goal_complete=False))


if __name__ == "__main__":
    main()
