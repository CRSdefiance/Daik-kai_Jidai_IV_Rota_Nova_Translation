"""Reconcile the Monster Fish transition with the clean battle setup and actual captures."""

from pathlib import Path
from struct import unpack_from

from PIL import Image, ImageDraw

from dk4tool.dialogue.font_audit import GameAsciiFont
from dk4tool.script.common_message_table import common_message_entries

from scripts import observe_monster_fish_transition_20261123 as prior
from scripts import replay_monster_fish_trail_20261123 as replay
from scripts.stage_azores_wording_20261123 import ARM, COMMON, common_rows
from scripts.stage_cartridge_title_20261123 import CLEAN, NdsImage, REGISTRY, digest, read, reference, write
from scripts.verify_captain_biographies_v1 import captured
from scripts.verify_confirmed_name_widget_pixels_v198 import complete_mask
from scripts.verify_lisbon_azores_voyage_20261123 import body_mask
from scripts.verify_personal_gameplay_v841 import get_machine
from scripts.verify_stock_encounter_names_20261121 import read_ram

OUT = Path("translations/editorial_checkpoints/shared_display_20261123/monster_fish_transition_current_20261123.json")
BASE = 0x02000000
CODE = (
    (0x0202CFFC, 0x0202D124),          # Registration and first trail fill.
    (0x02055790, 0x020557C8),          # Repeated position writer.
    (0x0206EE90, 0x0206F0C8),          # Declare and readiness handling.
    (0x02070998, 0x02071028),          # Battle positions before combat initialization.
    (0x020692F0, 0x02069424),          # The two battle terrain conditions.
    (0x02069504, 0x020697E0),          # Position normalization and spiral search.
)


def tables(arm, ram):
    cpu, get = get_machine(arm, ram)
    results = []
    for tile in range(1024):
        a, b = (get(offset, tile) for offset in (0x693EC, 0x693B4))
        assert a in (0, 1) and b in (0, 1)
        results.append((a, b))
    assert all((a, b) != (1, 1) for a, b in results)
    return dict(terrain_values_tested=len(results),
                first_condition=[i for i, (a, _) in enumerate(results) if a],
                second_condition=[i for i, (_, b) in enumerate(results) if b],
                both_conditions=0, native_call_addresses=[0x020693EC, 0x020693B4])


def battle_state(arm, raw):
    cpu, get = get_machine(arm, raw)
    game, calendar, fleets, world = (get(n) for n in (0x3F0F8, 0xCB1B4, 0xCB1A8, 0xCB19C))
    context = unpack_from("<5I", raw, game - BASE + 8)
    state = dict(context=context, calendar_tick=unpack_from("<I", raw, calendar - BASE + 8)[0],
                 target_party=bytes(cpu.mem_read(fleets + 0x2084, 4)).hex())
    track = world + 0x234 + 0x30C
    history = bytes(cpu.mem_read(track, 780))
    state["target_position_history"] = dict(address=track, all_zero=not any(history))
    for key, n in (("own", 1), ("target", 39)):
        obj = fleets + 4 + n * 132
        mobile = get(0x36C70, obj + 12)
        state[key] = dict(fleet=n, model=int(cpu.mem_read(obj + 16, 1)[0]), mobile=mobile)
        if mobile:
            state[key].update(hull=get(0x5543C, mobile), crew=get(0x55444, mobile),
                              position=unpack_from("<2i", raw, mobile - BASE + 16))
    return state


def capture(folder, release):
    path = folder / "capture/capture_report.json"
    data = read(path)
    assert data["ROM_sha256"] == release and data["cold_boot"] and not data["savestate_loaded"] and not data["callback_errors"]
    donor = data["battery_save_preloaded"]
    assert donor["copied_byte_exact_before_cold_boot"] and digest(donor["source"]) == donor["source_sha256"]
    fixture, = data["synthetic_condition_fixtures"]
    assert fixture["frame"] == 4800 and fixture["original_existing_model_ID"] == 149 and fixture["no_message_ID_renderer_actor_identity_or_result_injected"]
    frames = {r["frame"]: r for r in data["frames_captured"] if r["path"].endswith("_navigation.png")}
    snaps = {r["frame"]: r for r in data["read_only_pause_RAM_snapshots"]}
    return path, data, fixture, frames, snaps


def encounter_notices(current, stock, arm, clean, replay_data):
    native_source = common_message_entries(stock.read_file(COMMON), clean)
    installed = common_rows(current.read_file(COMMON), arm)
    font = GameAsciiFont.from_arm9(arm)
    owner, wrapper = (unpack_from("<I", arm, at)[0] - BASE for at in (0x552A0, 0x54450))
    cases = (
        (9920, 2054, "Sailor", ("The gunpowder's caught fire", "in the battery!"),
         "The contraction matches the familiar gunner's voice and preserves the ignition and its location."),
        (10700, 597, "Sailor", ("We put out the fire on Latina!",),
         "The first-person crew report preserves the completed action and names the affected ship."),
        (11000, 2059, "Gerhard Adernkatz", ("Admiral, Latina is going under...",),
         "Gerhard uses the original rank and reports a ship sinking. The hesitation fits the warning."),
    )
    results = []
    for frame, message, speaker, lines, reason in cases:
        raw = read_ram(replay_data[4][frame])
        template = raw[owner + 0x2030:owner + 0x2230].split(b"\0")[0]
        selected, = [row for row in installed if row.text == template]
        assert selected.message_id == message
        visible = raw[wrapper:wrapper + 512].split(b"\0")[0]
        assert tuple(row.strip().decode("ascii") for row in visible.split(b"\n")) == lines
        source = native_source[message]
        assert source.text.count(b"%s") == selected.text.count(b"%s") == int(message != 2054)
        screen = captured(replay_data[3][frame])
        ink, bounds = complete_mask(font, speaker, screen, 16, 277, (98, 97, 98))
        body = body_mask(font, screen, lines)
        results.append(dict(frame=frame, retained=True, reason=reason, speaker=speaker, source=dict(message_ID=message,
            file=COMMON, block=source.block, offset=source.block_offset, table_offset=source.table_offset,
            exact_hex=source.text.hex(), Japanese=source.text.decode("cp932")),
            installed=dict(file=COMMON, block=selected.block, offset=selected.block_offset,
                table_offset=selected.table_offset, exact_hex=selected.text.hex()),
            lines=lines, native_formatted_hex=visible.hex(), font_mask=body, nameplate_ink=ink,
            nameplate_bounds=bounds, on_screen_capture=replay_data[3][frame],
            review=dict(source=True, context=True, localization=True, naturalness=True, formatting=True)))
    flags = {}
    for frame in (9920, 10040, 10700, 10830, 11000):
        raw = read_ram(replay_data[4][frame])
        cpu, get = get_machine(arm, raw)
        fleet = get(0xCB1A8) + 4 + 132
        mobile = get(0x36C70, fleet + 12 + 4 * 8)
        model = get(0x36C94, fleet + 12 + 4 * 8)
        assert bytes(cpu.mem_read(model + 8, 7)) == b"Latina\0"
        flags[frame] = dict(mobile=mobile, original_flag=int(cpu.mem_read(mobile + 14, 1)[0]),
                            hull=get(0x5543C, mobile), confirmed_source_ship_name="Latina")
    assert [flags[n]["original_flag"] & 1 for n in flags] == [1, 1, 1, 0, 0]
    assert flags[11000]["hull"] == 0 < flags[10830]["hull"]
    return results, flags

def main():
    release = read(prior.RELEASE)
    candidate = release["candidate_sha256"]
    assert digest(release["candidate"]) == candidate and digest(REGISTRY) == release["registry_sha256"]
    assert digest(CLEAN) == release["clean_input_sha256"]
    current, stock = [NdsImage.open(p) for p in (release["candidate"], CLEAN)]
    arm, clean = current.read_file(ARM), stock.read_file(ARM)
    spans = []
    for lo, hi in CODE:
        code = arm[lo-BASE:hi-BASE]
        assert code == clean[lo-BASE:hi-BASE]
        spans.append(dict(start=lo, end=hi, same_clean_and_registered_bytes=True))
    bad, better = (capture(prior.ROOT / key, candidate) for key in ("current", "position_history"))
    assert bad[1]["battery_save_preloaded"]["source_sha256"] == better[1]["battery_save_preloaded"]["source_sha256"]
    assert bad[2]["target_point"] == better[2]["target_point"]
    assert bad[2]["after_RAM_sha256"] == better[2]["before_trail_fixture"]["after_RAM_sha256"]
    assert better[2]["exact_wrapper_call_chain"] == [replay.ENTRY, replay.FILL, replay.HISTORY_WRITER]
    assert better[2]["all_other_bytes_equal_to_previous_inspection_fixture"]
    assert len(better[2]["changes"]) > len(bad[2]["changes"])

    cert = []
    for n, radius in ((7400, 386), (10100, 809)):
        state_path = bad[0].parent / f"native_state_{n:06}" / "native_state.json"
        state = read(state_path)
        cpu = state["ARM9_registers"]
        assert state["serialized_RAM_matches_same_frame_direct_export"] and state["read_only_export"] and not state["state_loaded"]
        raw = read_ram(bad[4][n])
        words = unpack_from("<112I", raw, cpu[13]-BASE)
        returns = (0x020695E4, 0x02069798, 0x02070BD4, 0x02070FD8)
        assert all(x in words for x in returns)
        native = battle_state(arm, raw)
        assert native["context"] == (0, 1, 39, 181, 21) and native["target_position_history"]["all_zero"]
        assert cpu[8] == radius
        cert.append(dict(frame=n, processor=reference(state_path), PC=state["ARM9_instruction_address"],
                         raw_snapshot=bad[4][n], stack_returns=returns,
                         radius_register=radius, battle=native))
    assert cert[0]["battle"]["calendar_tick"] == cert[1]["battle"]["calendar_tick"]
    initial = read_ram(bad[4][4800])
    # Load the clean ARM9 program with the same captured data for offline pure
    # predicates. Those routines and their tables are byte-exact on both ROMs.
    def with_clean_codes():
        clean_bytes = bytearray(initial)
        for lo, hi in CODE:
            clean_bytes[lo-BASE:hi-BASE] = clean[lo-BASE:hi-BASE]
        return bytes(clean_bytes)
    test = tables(arm, initial)
    assert test == tables(clean, with_clean_codes()) and test["first_condition"] == [0, 1, 16, 17]
    assert unpack_from("<I", arm, 0x69664)[0] == 1250

    controls = (4800, 6750, 7000, 7050, 7110, 7250)
    # New trails are read in battle setup and are allowed to influence an earlier
    # sailing frame. The matched held declaration demonstrates the same target
    # and input at the ordinary confirmation point.
    assert bad[3][4800]["PNG_sha256"] == better[3][4800]["PNG_sha256"]
    cutoff = [n for n in controls if bad[3][n]["PNG_sha256"] == better[3][n]["PNG_sha256"]]
    assert set((4800, 7110, 7250)) <= set(cutoff)
    inspected = (7250, 7400, 7600, 8000, 9030, 9360, 9700)
    states = {n: battle_state(arm, read_ram(better[4][n])) for n in inspected}
    assert states[7250]["context"] == (0, 0, 0, 0, 0)
    assert all(states[n]["context"] == (0, 1, 39, 181, 21) for n in inspected[1:])
    assert not any(s["target_position_history"]["all_zero"] for s in states.values())
    assert states[7400]["calendar_tick"] < states[7600]["calendar_tick"] < states[8000]["calendar_tick"]
    assert len({states[n]["own"]["position"] for n in (7400, 7600, 8000)}) == 3
    assert [states[n]["target"]["hull"] for n in (7250, 9030, 9360, 9700)] == [800, 796, 794, 794]
    assert states[7250]["own"]["hull"] == 60 and states[9700]["own"]["hull"] == 56
    assert all(states[n]["target"]["model"] == 149 and states[n]["target"]["crew"] == 60 for n in inspected)

    notices, fire_flags = encounter_notices(current, stock, arm, clean, better)
    assert better[1]["frames"] == 11320
    return_frames = (10040, 10830, 11320)
    resumed = {}
    for frame, notice in zip(return_frames, notices, strict=True):
        assert frame > notice["frame"]
        resumed[frame] = dict(frame=better[3][frame], battle=battle_state(arm, read_ram(better[4][frame])))
        assert resumed[frame]["battle"]["context"] == (0, 1, 39, 181, 21)
        assert captured(better[3][frame]).tobytes() != captured(notice["on_screen_capture"]).tobytes()
    sheet = Image.new("RGB", (1048, 808), "#263238")
    labels = ImageDraw.Draw(sheet)
    for i, (title, frame) in enumerate((("Inspection-only setup", bad[3][7400]),
                                         ("Original registration with position history", better[3][7400]))):
        x = 4 + i * 522
        labels.text((x, 8), title, fill="white")
        sheet.paste(captured(frame).resize((512, 768), Image.Resampling.NEAREST), (x, 27))
    evidence_sheet = Image.new("RGB", (3 * 516, 256), "#263238")
    ink = ImageDraw.Draw(evidence_sheet)
    for i, record in enumerate(notices):
        x = i * 516 + 2
        ink.text((x, 5), f"COMMON {record['source']['message_ID']}", fill="white")
        panel = captured(record["on_screen_capture"]).crop((0, 271, 256, 384))
        evidence_sheet.paste(panel.resize((512, 226), Image.Resampling.NEAREST), (x, 23))
    notices_png = OUT.with_name("monster_fish_battle_notices_current_20261123.png")
    evidence_sheet.save(notices_png)
    png = OUT.with_suffix(".png")
    sheet.save(png)

    write(OUT, dict(registered_release=reference(prior.RELEASE), candidate_sha256=candidate,
        clean_source_sha256=release["clean_input_sha256"], phase_code=spans,
        earlier_battle_text=reference("translations/editorial_checkpoints/shared_display_20261123/special_target_battle_20261123.json"),
        inspection_only_run=reference(bad[0]), original_position_history_run=reference(better[0]),
        same_controller_frames=cutoff, exact_read_only_stall_states=cert, original_terrain_predicates=test,
        source_radius_limit=1250, source_position_history={
            key: better[2][key] for key in ("complete_stock_registration_wrapper", "exact_wrapper_call_chain",
                "position_history_address", "position_history_size", "position_history_records", "each_record_hex",
                "source_exact_spans", "all_other_bytes_equal_to_previous_inspection_fixture")},
        initialized_battle_states=states, played_hull_changes_observed=True,
        comparison_sheet=reference(png), verified_random_battle_notices=notices, notice_sheet=reference(notices_png),
        verified_Latina_fire_and_sinking_flags=fire_flags, observed_battle_returns=resumed,
        ordinary_controller_input_on_prepared_encounter=True,
        original_combat_setup_and_phase_resume=True, natural_spawn=False, runtime_outcome_fixture=False,
        new_editorial_credit=0, full_goal_complete=False, ROM_changed=False))
    print("Verified that the original position-history initialization clears the observed battle setup stall.")


if __name__ == "__main__":
    main()
