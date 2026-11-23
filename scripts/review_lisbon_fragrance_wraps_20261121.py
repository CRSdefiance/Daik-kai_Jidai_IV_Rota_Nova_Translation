"""Review the complete Lisbon fragrance exchange and plan two targeted repairs."""

from collections import Counter
from pathlib import Path
from types import FunctionType

from scripts import prepare_london_guild_assignments_20261118 as pairing
from scripts import stage_late_trade_exchanges_20261118 as planning
from scripts import verify_lisbon_seoul_trend_gameplay_20261121 as gameplay
from scripts.review_company_name_dialogue_20261121 import GATES, TOKEN, logical


base, native = gameplay.base, gameplay.native
parent = gameplay.runs.active
ROOT = Path("work/lisbon_fragrance_wraps_20261121")
SOURCE = ROOT / "paired_source.json"
OUTPUT = gameplay.town.events.BOOK / "lisbon_fragrance_wraps_review_20261121_v1.json"
BLOCKS = ((), (184,), (), ())
CONTEXT = ("", "Two women admire a fragrance and agree to ask the person wearing it. One worries it will catch on before they can get some. The system forecasts a fragrance trend in Lisbon.", "", "")
REVISIONS = {
    20: ("Oh, dear! Then we must get some before everyone else does.", ("before everyone else does.",),
         "Keep her polite alarm and urgency, using the same idiom as Rafael's route. The entire race to get some first stays together.", 192),
    28: ("Next time we see them, shall we work up the nerve to ask?", ("Next time we see them,", "shall we work up the nerve to ask?"),
         "Work up the nerve expresses what it costs her to ask, and the complete time clause stays together. Rafael's route already uses this wording.", 192),
}


def main():
    assert not OUTPUT.exists()
    if not SOURCE.exists():
        FunctionType(pairing.main.__code__, vars(pairing) | globals())()
    read, active, scene = map(base.load, (gameplay.OUTPUT, parent.RELEASE, SOURCE))
    assert scene["candidate_sha256"] == active["candidate_sha256"] == read["candidate_sha256"] == base.digest(parent.ROM)
    assert scene["clean_sha256"] == active["clean_input_sha256"] == base.digest(native.CLEAN)
    assert base.digest(base.REGISTRY) == active["registry_sha256"]
    prior = base.load(gameplay.town.REVIEW)["records"]
    run, = [m for m in read["town_runs"] if m["city"] == "lisbon"]
    group, = scene["groups"]
    assert group["route"] == 1 and group["block"] == 184
    scoped = {r["id"]: r for r in prior if r["file_path"] == group["file_path"] and r["block"] == group["block"]}
    assert len(scoped) == len(group["records"]) == len(run["records"]) == 11
    records, plans = [], {}
    for native_row, hold in zip(group["records"], run["records"], strict=True):
        index, selector = native_row["source_record_index"], native_row["selector"]
        ident = f"DK4_MES_B184_R{index:04}"
        original = scoped[ident]
        assert hold["id"] == ident and original["Japanese"] == native_row["Japanese"] and not native_row["slots"]
        prev = logical(native_row["current_English"])
        assert original["english"].split("}", 1)[1] == prev
        refs = {}
        for side in ("source", "current"):
            refs[side] = dict(file_path=group["file_path"], block=group["block"],
                offset=native_row[f"{side}_offset"], command_offset=native_row[f"{side}_command_offset"],
                exact_stored_hex=bytes([selector]).hex() + native_row[f"{side}_body_hex"],
                archive_sha256=group[f"{side}_archive_sha256"], block_sha256=group[f"{side}_block_sha256"])
        refs["source"]["record_index"] = index
        assert refs["source"]["exact_stored_hex"] == original["source_hex"]
        assert refs["current"]["exact_stored_hex"] == hold["registered_reference"]["raw_hex"]
        note = hold["localization_note"]
        decision, wording, phrases, approved_reference = "retention", prev, (), None
        if index in REVISIONS:
            wording, phrases, note, sibling = REVISIONS[index]
            same, = [r for r in prior if r["file_path"] == "/data/SC0.DK4" and r["block"] == sibling
                    and r["source_hex"] == original["source_hex"] and r["english"].split("}", 1)[1] == wording]
            assert wording != prev and "\n" in native_row["current_English"]
            approved_reference = {k: same[k] for k in ("file_path", "block", "id", "registered_reference")}
            decision = "revision"
        assert TOKEN.findall(wording) == TOKEN.findall(prev) == TOKEN.findall(native_row["Japanese"]) == []
        row = dict(id=ident, route=1, block=184, file_path=group["file_path"], kind="progressive",
            native_command_word=native_row["native_command_word"], native_slots=[], source_selector=selector,
            source_reference=refs["source"], current_reference=refs["current"],
            source_hex=refs["source"]["exact_stored_hex"], current_hex=refs["current"]["exact_stored_hex"],
            Japanese=native_row["Japanese"], previous_English=prev, english=wording,
            context=CONTEXT[1], speaker="System notice" if selector == 254 else "Lady",
            source_meaning=original["source_meaning"], localization_note=note, protected_phrases=list(phrases),
            matched_source_Rafael_copy=approved_reference, decision=decision, observed_existing_panel=hold["observed"],
            review=dict.fromkeys(GATES, True) | {"formatting": decision == "retention"})
        if decision == "revision":
            body, plan = planning.plan_progressive(row, selector, bytes.fromhex(native_row["current_body_hex"]),
                                                      bytes.fromhex(native_row["source_body_hex"]))
            assert all(any(phrase in line for line in plan["lines"]) for phrase in phrases)
            assert plan["expected_native_pages"] == 1 and body.isascii()
            plans[ident] = plan
        records.append(row)
    counts = Counter(r["decision"] for r in records)
    assert counts == {"revision": 2, "retention": 9}
    base.save(OUTPUT, dict(translation_policy="natural-dialogue-v2", target_locale="en-US", review_gates=GATES,
        previous_sha256=active["candidate_sha256"], previous_registry_sha256=active["registry_sha256"],
        source_packet_sha256=base.digest(SOURCE), current_gameplay_receipt_sha256=base.digest(gameplay.OUTPUT),
        source_review_sha256=base.digest(gameplay.town.REVIEW), records=records, decisions=dict(counts),
        plans=plans, other_route_copies_require_no_wrap_change=True, new_editorial_credit=0,
        status="Current game behavior verified. Proposed revisions have automatic layouts and still need stored native and gameplay validation."))
    print([(row["id"], plans[row["id"]]["lines"]) for row in records if row["id"] in plans])


if __name__ == "__main__":
    main()

