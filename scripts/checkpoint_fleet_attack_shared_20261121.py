"""Bind the observed fleet encounter to the current shared text and coverage ledger."""

from scripts import observe_fleet_attack_shared_20261121 as replay
from scripts import reconcile_shared_display_20261121 as shared


base = replay.base
ROOT = replay.ROOT / "attack"
OUTPUT = shared.worklist.BOOK / "fleet_attack_shared_20261121_v1.json"
FRAMES = {
    1905: (6010, "Gerhard Adernkatz", "The cautious question asks for assent after reporting that the faction is unidentified."),
    2205: (6120, "James Clifford", "Disbelief, a scoff, then a personal boast carry the original response. Preserve the words and improve the break before 'they can beat me?'."),
    1958: (6950, "James Clifford", "The pause and emphatic claim sound like a quick reaction during the duel."),
    2086: (8200, "Sailor", "The crew identifies the captured enemy vessel using the actual ship-model name, War Galleon."),
    2011: (8400, "Gerhard Adernkatz", "The report identifies both the defeated enemy flagship crew and the capture of its ship."),
    2131: (8600, "Gerhard Adernkatz", "The address and short victory report suit an officer immediately after the fight."),
    303: (8800, None, "A single reward notice clearly attributes 109 barrels to food and 103 to water."),
    301: (9200, None, "The notice reports 6055 gold recovered from captured ships and preserves where the gold came from."),
}
EXPECTED = [
    (3609, 85), (4423, 86), (5244, 97), (5569, 2217), (5674, 308), (5929, 1905),
    (6037, 2205), (6381, 1932), (6381, 1931), (6508, 1943), (6508, 1931),
    (6902, 1958), (6902, 1931), (7146, 1990), (7146, 1931), (7958, 1947),
    (7958, 1931), (8161, 2086), (8261, 2011), (8463, 2131), (8661, 303), (8860, 301),
]


def main():
    assert not OUTPUT.exists()
    release, pending = map(base.load, (replay.current.RELEASE, shared.OUTPUT))
    terminal_file = ROOT / "terminal.json"
    terminal = base.load(terminal_file)
    candidate = release["candidate_sha256"]
    assert base.digest(base.REGISTRY) == release["registry_sha256"]
    assert base.digest(replay.current.ROM) == candidate == terminal["ROM_sha256"]
    assert base.digest(shared.CLEAN) == release["clean_input_sha256"]
    assert terminal["COMMON_requests"] == 44 and not terminal["target_COMMON_calls"]
    for path, digest in terminal["evidence"].items():
        assert base.digest(path) == digest, path
    capture = base.load(ROOT / "capture/capture_report.json")
    original = base.load(replay.HISTORICAL)
    assert capture["scripted_input_schedule"] == original["scripted_input_schedule"]
    assert capture["frames"] == terminal["completed_frames"] == 9200
    assert capture["ROM_sha256"] == candidate and capture["cold_boot"] and not capture["savestate_loaded"]
    assert not capture["callback_errors"] and not capture["hardware_device_verification"]
    copied = capture["battery_save_preloaded"]
    assert copied["copied_byte_exact_before_cold_boot"] and base.digest(copied["source"]) == copied["source_sha256"]
    fixture, = capture["synthetic_battle_recovery_proximity_fixtures"]
    assert fixture["frame"] == replay.PAUSE and fixture["original_existing_enemy_fleet"] == 4
    assert len(fixture["owned_bytes"]) == 40
    assert fixture["all_other4MiB_enemy_health_crew_equipment_actors_IDs_RNG_eligibility_and_results_exact"]
    assert not any(value for key, value in capture.items() if key.startswith("synthetic_")
                   and key != "synthetic_battle_recovery_proximity_fixtures")

    clean, active = map(base.NdsImage.open, (shared.CLEAN, replay.current.ROM))
    workflow = shared.workflow
    source = workflow.common_message_entries(clean.read_file(shared.COMMON), clean.read_file(shared.ARM))
    current = shared.entries(active)
    changed_pending_references = []
    for stored in pending["records"]:
        n = stored["message_ID"]
        assert source[n].text.hex() == stored["source_hex"]
        assert workflow.reference(source[n]) == stored["source_reference"]
        assert current[n].text.hex() == stored["current_hex"], n
        if workflow.reference(current[n]) != stored["current_reference"]:
            changed_pending_references.append(n)
    requests = base.load(ROOT / "requests.json")["source_requests"]
    records = {}
    for (getter, copier), (frame, n) in zip(zip(requests[::2], requests[1::2], strict=True), EXPECTED, strict=True):
        assert (getter["PC"], copier["PC"]) == (0x0205528C, 0x020534F4)
        assert getter["frame"] == copier["frame"] == frame and getter["message_ID"] == copier["message_ID"] == n
        assert getter["caller_LR"] == copier["caller_LR"]
        jp, en = source[n], current[n]
        row = records.setdefault(n, dict(message_ID=n, requests=[], source_reference=workflow.reference(jp),
            source_hex=jp.text.hex(), clean_Japanese=jp.text.decode("cp932"),
            current_reference=workflow.reference(en), current_hex=en.text.hex(), current_template=en.text.decode("cp932")))
        row["requests"].append(dict(frame=frame, caller_LR=getter["caller_LR"]))
    assert len(records) == 18 and len(pending["records"]) == 276
    assert not (records.keys() & {r["message_ID"] for r in pending["records"]})
    assert replay.FOCUS <= {r["message_ID"] for r in pending["records"]}

    captures = {r["frame"]: r for r in capture["frames_captured"] if r["path"].endswith("_cold_boot.png")}
    for n, (frame, speaker, reason) in FRAMES.items():
        still = captures[frame]
        assert max(call["frame"] for call in records[n]["requests"]) < frame
        assert base.digest(still["path"]) == still["PNG_sha256"]
        records[n].update(observed_frame=still, speaker=speaker, localization_note=reason,
                          decision="retain_words_review_wrap" if n == 2205 else "gameplay_retention")
    for frame in (5355, 5918):
        assert base.digest(captures[frame]["path"]) == captures[frame]["PNG_sha256"]
    base.save(OUTPUT, dict(candidate_sha256=candidate, release=str(replay.current.RELEASE),
        clean_sha256=release["clean_input_sha256"], terminal_sha256=base.digest(terminal_file),
        capture_report=str(ROOT / "capture/capture_report.json"), complete_requested_pairs=len(EXPECTED),
        pending_shared_records=276, archived_focus=sorted(replay.FOCUS), observed_pending_records=[],
        previous_worklist_sha256=base.digest(shared.OUTPUT), pending_bytes_unchanged=True,
        pending_reference_changes=changed_pending_references,
        search_mode=captures[5355], declare_war_mode=captures[5918], original_controls=True,
        fixture_description="Copied Copenhagen save with a 40-byte adjustment to the player's fleet position before the encounter.",
        earlier_outcome="defeat and transfer", observed_outcome="victory, including the food and water and recovered gold notices",
        gold_notice_dismissal_verified=False, hardware_verified=False, new_editorial_credit=0,
        records=list(records.values())))
    print("Bound 22 original shared requests across 18 records and eight visually checked dialogue or reward holds.")


if __name__ == "__main__":
    main()
