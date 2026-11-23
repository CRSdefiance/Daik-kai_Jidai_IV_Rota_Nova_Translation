"""Bind the current Madeira target selection and allied exclusion to their actual display owners."""

from scripts import observe_attack_display_ownership_20261118 as run
from scripts import register_all_routes_final_flagged_wraps_20261118 as parent

base, native = parent.base, parent.native
ROOT = run.ROOT
OUTPUT = ROOT / "verified_display_ownership.json"
PENDING = parent.stage.ROOT / "shared_text_current_binding.json"


def main():
    release = base.load(parent.RELEASE)
    assert base.digest(parent.ROM) == release["candidate_sha256"]
    pending = base.load(PENDING)
    assert pending["candidate_sha256"] == release["candidate_sha256"]
    stored = [r for r in pending["records"] if r["message_ID"] in (300, 304)]
    assert {r["message_ID"] for r in stored} == {300, 304}
    locks = (0x0205528C, 0x020534F4)
    evidence = {str(PENDING):base.digest(PENDING)}
    cases = {}
    observed_ids = {"neutral_v2": [85, 86, 1290, 297, 65, 49, 85, 86, 2122],
                    "allied_v2": [85, 86, 1290, 297, 65, 49, 85, 86]}
    for case, ids in observed_ids.items():
        path = ROOT / case
        terminal, trace, report = (path / "terminal.json", path / "requests.json", path / "capture/capture_report.json")
        recap, cpu, video = map(base.load, (terminal, trace, report))
        assert video["ROM_sha256"] == recap["ROM_sha256"] == release["candidate_sha256"]
        assert video["cold_boot"] and not video["savestate_loaded"] and not video["callback_errors"]
        assert cpu["all_host_slots_restored_and_core_file_exact"] and not cpu["errors"] and not cpu["mismatches"]
        assert recap["preloaded_existing_save"]
        assert not recap["target_COMMON_calls"]
        assert recap["COMMON_requests"] == 2 * len(ids)
        for expected, a, b in zip(ids, cpu["source_requests"][::2], cpu["source_requests"][1::2], strict=True):
            assert (a["PC"], b["PC"]) == locks
            assert a["frame"] == b["frame"] and a["caller_LR"] == b["caller_LR"]
            assert a["message_ID"] == b["message_ID"] == expected
        fixture = recap["location_fixture"]
        assert fixture["town_ID"] == 30 and fixture["frame"] == 5000
        if case == "allied_v2":
            relation = fixture["relationship_fixture"]
            assert relation["only_relation_byte_changed"] and relation["player_company"] == 2 and relation["allied_occupant"] == 6
        else:
            assert fixture["only_own_cached_and_live_position_changed"]
            assert cpu["source_requests"][-1]["caller_LR"] == 0x02053D10
        frame, = [f for f in video["frames_captured"] if f["frame"] == 6620 and f["path"].endswith("_cold_boot.png")]
        assert base.digest(frame["path"]) == frame["PNG_sha256"]
        evidence.update({str(p):base.digest(p) for p in (terminal, trace, report, frame["path"])})
        text = "Shall we attack Madeira?" if case == "neutral_v2" else "There are no targets to attack."
        cases[case] = dict(frame=frame, visible_English=text, requests=ids, fixture=fixture)
    receipt = dict(candidate_sha256=release["candidate_sha256"], ARM9_sha256=release["target_ARM9_sha256"],
        COMMON_sha256=release["target_COMMON_sha256"], actual_emulator_cases=cases, hardware=False, evidence=evidence,
        scoped_conclusion="The Madeira paths use COMMON 2122 for confirmation and a separate no-target graphic for an allied occupant.",
        pending_records_preserved=stored, global_absence_claim=False, new_editorial_credit=0)
    if OUTPUT.exists():
        assert base.load(OUTPUT) == receipt
    else:
        base.save(OUTPUT, receipt)
    print("Bound the Madeira confirmation and allied no-target display. Stored COMMON 300 and 304 remain open elsewhere.")


if __name__ == "__main__":
    main()
