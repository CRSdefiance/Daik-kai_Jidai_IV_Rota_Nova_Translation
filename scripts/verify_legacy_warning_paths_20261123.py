"""Bind the focused disband shortfall and ordinary Quit selector to current text."""

from pathlib import Path
from struct import unpack_from

from scripts import checkpoint_exhibition_quit_warning_20261115 as exhibition
from scripts import observe_current_disband_shortfall_20261123 as replay
from scripts import verify_current_shared_encounters_20261123 as shared


base, native, current = replay.base, replay.native, replay.current
debt, check, town, visual = replay.debt, shared.check, shared.town, shared.visual
OUT = shared.OUT.with_name("legacy_warning_paths_20261123.json")
SHEET = OUT.with_suffix(".png")
SHIPYARD = Path("releases/all_routes_editorial_20261111_shipyard_fleet_setup_candidate/verification/registered_review.json")
BOOK = OUT.parent.parent / "SharedText_20261110_v1"
WAITING = SHIPYARD.parent.parent / "checksums.json"
HOLD_FRAMES = ((280, 9400), (281, 10360), (285, 10840), (285, 11560), (286, 11680))
NOTES = {
    280: "Reorganize marks the separate picker before the shipyard worker moves to the disband option.",
    281: "Use disband in both the picker and the following confirmation. The stock picker keeps its brief instruction.",
    285: "The direct confirmation suits both Yes and No and stays the same when the fixture supplies a shortfall.",
    286: "The reply tells the player what will happen to every ship only after Yes. Keep the dock as the destination.",
}


def bound_text(key, before, after):
    return dict(message_ID=key, source_reference=town.reference(before[key]),
        installed_reference=town.reference(after[key]), source_hex=before[key].text.hex(), installed_hex=after[key].text.hex(),
        clean_Japanese=before[key].text.decode("cp932"), installed_English=after[key].text.decode("cp932"))


def shortfall(candidate, arm, before, after):
    folder = replay.ROOT / replay.CASE
    terminal_path = folder / "terminal.json"
    report_path = folder / "capture/capture_report.json"
    trace_path = folder / "requests.json"
    run, report, trace = map(base.load, (terminal_path, report_path, trace_path))
    assert run["ROM_sha256"] == report["ROM_sha256"] == candidate
    assert run["focused_finance_fixture"] and not run["observation_is_ordinary_gameplay"]
    assert report["cold_boot"] and not report["savestate_loaded"] and not report["callback_errors"]
    assert all(base.digest(path) == sha for path, sha in run["evidence"].items())
    donor = report["battery_save_preloaded"]
    assert donor["copied_byte_exact_before_cold_boot"] and base.digest(donor["source"]) == donor["source_sha256"]
    assert donor["source_sha256"] == base.load(debt.FLEET_SAVE)["fixture_sha256"]
    events, _, end, _, _ = replay.SCHEDULE(replay.CASE)
    assert report["scripted_input_schedule"] == events and report["frames"] == end
    assert trace["all_host_slots_restored_and_core_file_exact"] and not trace["errors"] and not trace["mismatches"]
    calls = trace["source_requests"]
    assert calls == run["target_COMMON_calls"] and len(calls) == 12
    assert [row["message_ID"] for row in calls[::2]] == [280, 281, 285, 281, 285, 286]
    for getter, copied in zip(calls[::2], calls[1::2], strict=True):
        assert (getter["PC"], copied["PC"]) == (0x0205528C, 0x020534F4)
        assert dict(getter, PC=copied["PC"]) == copied
    proof = run["finance_fixture"]
    assert base.digest(proof["path"]) == proof["sha256"]
    fixture = base.load(proof["path"])
    owner = fixture["owner"]
    assert fixture["frame"] == 9800 and fixture["supplied_gold"] == 37 and fixture["supplied_expenses"] == 100500
    assert fixture["only_supplied_words"] == ["company cash", "regional expenses"]
    states = {}
    for row in run["available_capture_ram"]:
        assert row["read_only_export"] and base.digest(row["path"]) == row["sha256"]
        raw = Path(row["path"]).read_bytes()
        assert len(raw) == 0x400000 == row["bytes"]
        wallet = debt.field(raw, owner["wallet"])
        finances = unpack_from("<3I", raw, owner["finance"] + 0x0C - debt.BASE)
        fleet = raw[owner["fleet"]-debt.BASE:owner["fleet"]-debt.BASE+0x84]
        states[row["frame"]] = dict(gold=wallet, regional_expenses=finances[0], income=finances[1],
            invested=finances[2], fleet_record_hex=fleet.hex(), snapshot=row)
    assert [states[frame]["gold"] for frame in (9400, 10840, 11080, 11560, 11680, 11800)] == [897400, 37, 37, 37, 37, 0]
    assert all(states[frame]["regional_expenses"] == 100500 and states[frame]["income"] == states[frame]["invested"] == 0
               for frame in (10360, 10840, 11080, 11560, 11680))
    assert states[10840]["fleet_record_hex"] == states[11080]["fleet_record_hex"] == states[11560]["fleet_record_hex"]
    assert states[11560]["fleet_record_hex"] != states[11800]["fleet_record_hex"]
    assert base.digest(SHIPYARD) == base.load(WAITING)["verification/registered_review.json"]
    previous = {row["message_ID"]: row for row in base.load(SHIPYARD)["records"]}
    frames, font = check.shots(report), check.GameAsciiFont.from_arm9(arm)
    panels, pictures = [], []
    for key, frame in HOLD_FRAMES:
        row = previous[key]
        assert row["source_hex"] == before[key].text.hex() and row["source_reference"] == town.reference(before[key])
        assert row["registered_reference"]["exact_stored_hex"] == after[key].text.hex()
        text = after[key].text.decode("ascii").strip()
        assert all(row["review"].values()) and text == row["english"]
        image = check.captured(frames[frame]).convert("RGB")
        for origin in (16, 22):
            try:
                glyph_ink = debt.font_mask(image, font, text, origin, 297, debt.BODY, (0, 8, 0))
            except AssertionError:
                continue
            break
        else:
            raise AssertionError((key, frame, text))
        panels.append(bound_text(key, before, after) | dict(frame=frame, body_ink=glyph_ink, screenshot=frames[frame],
            decision="retention", localization_note=NOTES[key], context=row["context"], review=row["review"]))
        pictures.append((f"Focused shortfall / COMMON {key} / {frame}", image))
    digest_sheets = []
    for start in range(0, len(pictures), 4):
        path, digest = visual.make_sheet(SHEET.with_stem(f"{SHEET.stem}_{1+start//4}"), pictures[start:start+4])
        digest_sheets.append(dict(path=path, sha256=digest))
    return dict(held_panels=panels, selected_messages=calls, states=states, supplied_finance=fixture,
        original_inputs=True, earned_finance=False, focused_emulator_test=True, sheets=digest_sheets,
        verified_return_with_wallet_at_zero=True, requested_284=False,
        evidence={str(path):base.digest(path) for path in (terminal_path, report_path, trace_path, SHIPYARD)})


def ordinary_quit(release, clean, source_arm, arm, before, after):
    earlier = base.load(exhibition.OUTPUT)
    proof = earlier["normal_quit"]
    lo, hi = exhibition.HELPER - exhibition.BASE, exhibition.SELECTOR_END - exhibition.BASE
    assert source_arm[lo:hi] == arm[lo:hi]
    ctx = town.RegisteredRuntime(current.RELEASE, release["own_registered_startup"], captain=3)
    routes = exhibition.sites(ctx.image)
    assert routes == exhibition.sites(clean)
    assert base.load(exhibition.OUTPUT)["normal_quit"]["source"] == town.reference(before[319])
    field = proof["stock_flag_address"]
    assert exhibition.flags_on_source(arm, field) == proof["paired_selector_cases"]
    active = exhibition.current_template(ctx, field, after[319])
    assert active["complete_template_hex"] == proof["exact_active_template"]["complete_template_hex"]
    assert active["native_lookup"] == [319]
    observed = proof["reused_actual_quit_evidence"]
    for key in ("confirmation", "cancelled"):
        shot = observed[key]
        assert base.digest(shot["path"]) == shot["PNG_sha256"]
    return dict(native_selector_cases=proof["paired_selector_cases"], direct_callers=routes, native_template=active,
        prior_ordinary_quit_and_cancel=observed, current_new_quit_gameplay=False,
        retained=bound_text(319, before, after) | dict(decision="retention", review=proof["review"],
            localization_note="The active-session prompt stays brief and lets the player confirm or cancel."),
        warning_draft=earlier["exhibition_warning"]["english"],
        evidence=dict(path=str(exhibition.OUTPUT), sha256=base.digest(exhibition.OUTPUT)))


def main():
    assert not OUT.exists()
    release = base.load(current.RELEASE)
    candidate = base.digest(current.ROM)
    assert candidate == release["candidate_sha256"] and base.digest(base.REGISTRY) == release["registry_sha256"]
    assert base.digest(native.CLEAN) == release["clean_input_sha256"]
    clean, image = map(base.NdsImage.open, (native.CLEAN, current.ROM))
    source_arm, arm = (rom.read_file(current.ARM) for rom in (clean, image))
    assert native.digest(arm) == release["target_ARM9_sha256"]
    original = town.common_message_entries(clean.read_file(current.COMMON), source_arm)
    installed = current.stage.observed.prior.shared.paired.prior.entries(image)
    evidence = base.load(shared.OUT.with_name("current_shared_display_evidence_20261123.json"))["records"]
    prior = {row["message_ID"]: row for row in evidence}
    pending = []
    for key in (284, 318):
        row = bound_text(key, original, installed)
        assert prior[key]["source_hex"] == row["source_hex"] and prior[key]["installed_hex"] == row["installed_hex"]
        assert prior[key]["source_reference"] == row["source_reference"] and prior[key]["installed_reference"] == row["installed_reference"]
        pending.append(row | dict(display_caller_open=True, draft=prior[key]["earlier_draft"]))
    base.save(OUT, dict(candidate_sha256=candidate, clean_sha256=release["clean_input_sha256"],
        disband_shortfall=shortfall(candidate, arm, original, installed),
        quit_path=ordinary_quit(release, clean, source_arm, arm, original, installed),
        stored_warning_leads=pending, shared_records_open=276, new_editorial_credit=0, hardware=False))
    print("Verified current low-funds Disband and the stock Quit selector. Both legacy warnings remain outside those tested paths.")


if __name__ == "__main__":
    main()
