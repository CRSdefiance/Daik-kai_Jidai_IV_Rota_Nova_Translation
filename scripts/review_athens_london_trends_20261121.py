"""Review the full Athens and London exchanges after ordinary gameplay."""
from collections import Counter
from pathlib import Path
from types import FunctionType

from scripts import prepare_london_guild_assignments_20261118 as pairing
from scripts import stage_late_trade_exchanges_20261118 as planning
from scripts import verify_european_trends_gameplay_20261121 as gameplay
from scripts.review_company_name_dialogue_20261121 import GATES, TOKEN, logical


base, native, parent = gameplay.base, gameplay.native, gameplay.runs.active
ROOT = Path("work/athens_london_trend_repairs_20261121")
SOURCE = ROOT / "paired_source.json"
OUTPUT = gameplay.town.events.BOOK / "athens_london_trend_repairs_20261121_v1.json"
BLOCKS = ((193, 194), (185, 186), (181, 182), (154, 155))
CONTEXT = tuple("The two complete Athens and London trends." for _ in BLOCKS)
CONTEXT_BY_TOWN = {
    19: "Three women admire the ruby in a lady's necklace. One wishes for a similar gift. All three sigh before the ruby forecast.",
    0: "Two women discuss the princess's engagement, the duke's son, and the size and cost of the ring. They want to identify the gem before it catches on.",
}
MOUNTAIN = "I hear her engagement ring could buy a whole mountain."
REVISIONS = {
    (1, 185, 23): ("Just once in my life, I'd love a gentleman to give me something like that.",
                   ("Just once in my life,", "a gentleman", "something like that."),
                   "Use Maria's already reviewed wording for the polite wish. Keep the once-in-a-lifetime thought and the reference to the gift intact.", "prose and phrase wrapping"),
    (1, 186, 11): (MOUNTAIN, ("engagement ring", "buy a whole mountain."),
                   "Keep the hearsay and the price exaggerated to the value of an entire mountain. The whole comparison stays together.", "prose and phrase wrapping"),
    (1, 186, 17): (None, ("Once she wears it,", "how many ladies will want one!"),
                   "Keep her confident timing and anticipation. Put the entire phrase about the other ladies together.", "phrase wrapping"),
    (3, 155, 10): (MOUNTAIN, ("engagement ring", "buy a whole mountain."),
                   "Keep the hearsay and the price exaggerated to the value of an entire mountain. Match the fix in Hodram's scene.", "prose and phrase wrapping"),
}
for route, block, first, second, last in ((1, 185, 27, 31, 35), (3, 154, 26, 30, 34)):
    REVISIONS[route, block, first] = (
        "It would be lovely. (Sighs)", (), "Keep the polite agreement and mark the first audible sigh as an action.", "action cue")
    for index in (second, last):
        REVISIONS[route, block, index] = (
            "(Sighs)", (), "Repeat the same brief action cue to carry the comic rhythm of the three sighs.", "action cue")


def main():
    assert not OUTPUT.exists()
    if not SOURCE.exists():
        FunctionType(pairing.main.__code__, vars(pairing) | globals())()
    release, packet, live = map(base.load, (parent.RELEASE, SOURCE, gameplay.OUTPUT))
    assert packet["candidate_sha256"] == release["candidate_sha256"] == live["candidate_sha256"] == base.digest(parent.ROM)
    assert packet["clean_sha256"] == release["clean_input_sha256"] == base.digest(native.CLEAN)
    assert base.digest(base.REGISTRY) == release["registry_sha256"]
    event_map = base.load(gameplay.town.events.OUTPUT)
    cases = {(route["route"], row["script_block"]): row for route in event_map["routes"]
             for row in route["entries"] if row["town"] in CONTEXT_BY_TOWN}
    prior = base.load(gameplay.town.REVIEW)["records"]
    past = {(row["file_path"],row["id"]):row for row in prior}
    holds = {line["id"]:line["observed"] for case in live["scene_runs"] for line in case["panels"]}
    decisions, plans = [], {}
    selected = set()
    for group in packet["groups"]:
        route, block, path = (group[k] for k in ("route","block","file_path"))
        event = cases[route,block]
        assert group["source_block_sha256"] == event["prior_review"]["clean_block_sha256"]
        assert group["current_block_sha256"] == event["prior_review"]["current_block_sha256"]
        for row in group["records"]:
            index, selector = (row[k] for k in ("source_record_index","selector"))
            ident = f"DK4_MES_B{block}_R{index:04}"
            history = past[path,ident]
            refs={}
            for side in ("source","current"):
                refs[side] = dict(file_path=path,block=block,offset=row[f"{side}_offset"],
                    command_offset=row[f"{side}_command_offset"],archive_sha256=group[f"{side}_archive_sha256"],
                    block_sha256=group[f"{side}_block_sha256"],
                    exact_stored_hex=bytes([selector]).hex()+row[f"{side}_body_hex"])
            refs["source"]["record_index"] = index
            assert refs["source"]["exact_stored_hex"] == history["source_hex"]
            assert refs["current"]["exact_stored_hex"] == history["registered_reference"]["raw_hex"]
            assert history["Japanese"] == row["Japanese"] and all(history["review"].values())
            previous = logical(row["current_English"])
            assert previous == history["english"].split("}",1)[1]
            key = route,block,index
            revise = key in REVISIONS
            if revise:
                wording, phrases, note, finding = REVISIONS[key]
                wording = previous if wording is None else wording
                selected.add(key)
            else:
                wording,phrases,note,finding = previous,(),history["localization_note"],"retention"
            assert not TOKEN.findall(wording) and not TOKEN.findall(row["Japanese"]) and not row["slots"]
            entry = dict(id=ident,route=route,block=block,file_path=path,kind="progressive",
                native_command_word=row["native_command_word"],native_slots=[],source_selector=selector,
                source_reference=refs["source"],current_reference=refs["current"],
                source_hex=refs["source"]["exact_stored_hex"],current_hex=refs["current"]["exact_stored_hex"],
                Japanese=row["Japanese"],previous_English=previous,english=wording,
                context=CONTEXT_BY_TOWN[event["town"]],speaker="System notice" if selector==254 else "Lady",
                source_meaning=history["source_meaning"],localization_note=note,protected_phrases=list(phrases),
                decision="revision" if revise else "retention",finding=finding,
                observed_previous_panel=holds.get(ident) if route==1 else None,
                review=dict.fromkeys(GATES,True)|{"formatting":not revise})
            if revise:
                body,plan=planning.plan_progressive(entry,selector,bytes.fromhex(row["current_body_hex"]),
                                                       bytes.fromhex(row["source_body_hex"]))
                assert plan["expected_native_pages"]==1 and body.isascii()
                plans[f"{path}:{ident}"] = plan
                assert body.rstrip(b" ") != bytes.fromhex(row["current_body_hex"]).rstrip(b" ")
            decisions.append(entry)
    assert selected == set(REVISIONS) and len(decisions)==72
    base.save(OUTPUT,dict(translation_policy="natural-dialogue-v2",target_locale="en-US",review_gates=GATES,
        previous_sha256=release["candidate_sha256"],previous_registry_sha256=release["registry_sha256"],
        source_packet=str(SOURCE),source_packet_sha256=base.digest(SOURCE),decisions=dict(Counter(r["decision"] for r in decisions)),
        current_gameplay_sha256=base.digest(gameplay.OUTPUT),records=decisions,plans=plans,
        status="Protected layouts planned for 10 revisions. Staged native and gameplay verification are separate.",new_editorial_credit=0))
    for name,plan in plans.items():
        print(name,plan["lines"])


if __name__ == "__main__":
    main()

