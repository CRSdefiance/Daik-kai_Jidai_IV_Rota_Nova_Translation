"""Bind the Amsterdam round, price substitution and patron rumor to original text."""

from pathlib import Path
from struct import unpack_from

from PIL import ImageChops

from scripts import observe_amsterdam_tavern_followup_20261120 as replay
from scripts.replay_lil_ceramics_wrap_20261111 import photos
from scripts.stage_ruin_discovery_display_20261120 import batch, target


base, parent = replay.base, replay.current
ROOT = Path("work/amsterdam_tavern_followup_20261120_v4")
OUTPUT = Path("translations/editorial_checkpoints/SharedText_20261110_v1/amsterdam_tavern_round_20261120_v1.json")
HOLDS = {25630: 855, 26500: 855, 26900: 866, 27230: 872, 27560: 874, 27890: 880}
DECISIONS = {
    855: ("The sailor estimates the gold cost and asks the player to approve it.",
          "Keep the relaxed yes-or-no question and the single price substitution. Use regular-width digits in the existing original number path."),
    866: ("Lil asks the barkeep to serve drinks to everyone.",
          "The friendly request follows approval of the round and keeps the entire tavern as the recipient."),
    872: ("The barkeep announces who's buying today's round and encourages the patrons to enjoy themselves.",
          "The familiar announcement identifies the payer by the established dynamic surname and invites the patrons to enjoy the drinks."),
    874: ("The patron is surprised, thanks the payer, and calls the gesture generous.",
          "The excited thanks and praise follow the barkeep's announcement and set up the confidential tip."),
    880: ("The patron heard that a faction's fleet is headed for the named city.",
          "Keep the hearsay, the faction and city substitutions, and the fleet's destination. The patron has heard about a voyage in progress."),
}


def main():
    assert not OUTPUT.exists()
    release = base.load(parent.RELEASE)
    capture_path = ROOT / "capture/capture_report.json"
    trace_path = ROOT / "observer/requests.json"
    capture, trace = map(base.load, (capture_path, trace_path))
    assert capture["ROM_sha256"] == base.digest(parent.ROM) == release["candidate_sha256"]
    assert capture["cold_boot"] and not capture["savestate_loaded"] and not capture.get("battery_save_preloaded")
    assert not capture["callback_errors"] and not any(v for k, v in capture.items() if k.startswith("synthetic_"))
    appended = replay.verified_schedule(ROOT, base.load(replay.REPLAY / "capture_report.json")["scripted_input_schedule"], capture)
    assert len(appended) == 15 and capture["frames"] == 29210
    assert trace["all_host_slots_restored_and_core_file_exact"] and not trace["errors"] and not trace["mismatches"]
    requests = [r for r in trace["source_requests"] if replay.START < r["frame"] <= 28220]
    assert [r["message_ID"] for r in requests] == [n for n in HOLDS.values() for _ in range(2)]
    assert all({a["PC"], b["PC"]} == set(replay.trace.REQUESTS) and a["frame"] == b["frame"]
               for a, b in zip(requests[::2], requests[1::2], strict=True))
    for (held, n), row in zip(HOLDS.items(), requests[::2], strict=True):
        assert held - 400 <= row["frame"] < held and row["message_ID"] == n
    clean, active = map(base.NdsImage.open, (parent.stage.CLEAN, parent.ROM))
    ja, en = [im.read_file(parent.stage.ARM) for im in (clean, active)]
    assert ja[0x58374:0x583A8] == en[0x58374:0x583A8]
    assert target(en, 0x58388) == 0x020ABF50 and target(en, 0x58398) == 0x02053CB0
    assert unpack_from("<8i", en, 0x118400) == (852, -1, 853, 854, 855, 856, 857, 858)
    source = batch.common_message_entries(clean.read_file(parent.stage.COMMON), ja)
    current = batch.owned_entries(active.read_file(parent.stage.COMMON), en,
                                  batch.digest(en[batch.DIRECTORY_OFFSET:batch.TABLE_OFFSET]))
    frames = photos(capture)
    # The same prompt and price are visible before either response. The two
    # menu holds show the original wallet before and after the successful round.
    assert ImageChops.difference(frames[25630][1], frames[26500][1]).getbbox() is None
    assert ImageChops.difference(frames[24550][1], frames[25960][1]).getbbox() is None
    debit = ImageChops.difference(frames[25960][1], frames[28220][1]).getbbox()
    assert debit and 77 <= debit[0] < debit[2] <= 137 and 345 <= debit[1] < debit[3] <= 364
    records = []
    for n, (meaning, note) in DECISIONS.items():
        original, installed = (r[n].text for r in (source, current))
        records.append(dict(message_ID=n, source_reference=batch.reference(source[n]),
            current_reference=batch.reference(current[n]), source_hex=original.hex(), current_hex=installed.hex(),
            japanese=original.decode("cp932"), english=installed.decode("cp932").strip(),
            source_meaning=meaning, localization_note=note, wording_decision="retention",
            display_finding="wide runtime price numerals" if n == 855 else "none in the observed panel",
            held_frames=[frame for frame, message in HOLDS.items() if message == n],
            review=dict.fromkeys(batch.GATES, True) | {"formatting": n != 855}))
    evidence = {str(p): base.digest(p) for p in (capture_path, trace_path, ROOT / "navigation.jsonl",
        ROOT / "capture/navigation_command_journal.json", ROOT / "observer/source_contract.json")}
    base.save(OUTPUT, dict(candidate_sha256=capture["ROM_sha256"], records=records, requests=requests,
        observed_actual_controller_inputs=True, new_dialogue_credit=0, hardware=False,
        price_call=0x02058388, original_number_formatter=0x020ABF50, dialogue_wrapper=0x02053CB0,
        observed_price=268, wallet_after_cancel=34980, wallet_after_accept=34712,
        rumor_actual_substitutions=["Clifford", "Bristol"], held_images=[frames[f][0] for f in HOLDS], evidence=evidence))
    print("Verified both Tavern responses, the 268-gold debit, and Clifford's Bristol rumor.")


if __name__ == "__main__":
    main()
