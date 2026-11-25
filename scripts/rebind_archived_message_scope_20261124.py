"""Carry the archived COMMON evidence forward through the Stockholm and Tavern releases."""

from scripts import reconcile_archived_message_operands_20261123 as archive
from scripts import reconcile_shared_reference_coverage_20261124 as earlier
from scripts import register_tavern_buy_a_round_20261124 as current
from scripts import verify_copenhagen_docking_20261124 as observed
from scripts.stage_cartridge_title_20261123 import CLEAN, REGISTRY, NdsImage, digest, read, reference, sha256, write


OUT = earlier.OUT.with_name("archived_message_current_continuity_20261124.json")
STORY = "/data/SC1.DK4"


def main():
    source, latest, historical, play = map(read, (earlier.current.RELEASE, current.RELEASE, earlier.OUT, observed.OUT))
    assert digest(REGISTRY) == latest["registry_sha256"] and digest(CLEAN) == latest["clean_input_sha256"]
    assert digest(source["candidate"]) == source["candidate_sha256"] == historical["candidate_sha256"]
    assert digest(current.ROM) == latest["candidate_sha256"] == play["candidate_sha256"]
    old, new = map(NdsImage.open, (source["candidate"], current.ROM))
    before, after = map(current.parent.build.native.files, (old, new))
    assert before.keys() == after.keys()
    assert {path for path in before if before[path] != after[path]} == {current.ARM, current.HELP, STORY}
    a, b = before[current.ARM], after[current.ARM]
    assert sha256(a).hexdigest() == source["target_ARM9_sha256"] and sha256(b).hexdigest() == latest["target_ARM9_sha256"]
    slot = current.build.SLOT
    assert a == b[:slot] + a[slot:slot + 16] + b[slot + 16:]
    assert a[slot:slot+16] == b"Treat Everyone\0\0" and b[slot:slot+16] == b"Buy a Round".ljust(16, b"\0")
    rows = historical["references"]
    expected = {(r["call_site"], r["entry"], r["instruction"], r["component"]) for r in rows}
    assert len(expected) == historical["aligned_reference_count"] == 827
    assert earlier.forwarding.earlier.prior.census(current.ROM) == expected
    for group in (historical["supplementary_literal_and_table_locks"], *historical["earlier_native_locks"].values()):
        for r in group:
            lo, hi = r["start"], r["end"]
            assert all(sha256(earlier.tape(arm, lo, hi)).hexdigest() == r["sha256"] for arm in (a, b))
    for arm in (a, b):
        sections = earlier.MainCodeFile(arm, earlier.forwarding.BASE).sections
        for r in historical["exact_alias_code_spans"]:
            lo, hi = r["start"], r["end"]
            section, = [s for s in sections if s.ramAddress <= lo < hi <= s.ramAddress + len(s.data)]
            assert sha256(section.data[lo - section.ramAddress:hi - section.ramAddress]).hexdigest() == r["sha256"]
    keys = set(historical["separate_open_keys"])
    assert keys == set(archive.KEYS)
    assert all(not (set(r["possible_COMMON_ids"] or ()) & keys) for r in rows)
    old_blocks, new_blocks = (archive.IlnkContainer.parse(data[STORY]).blocks for data in (before, after))
    changed = [n for n, (a_block, b_block) in enumerate(zip(old_blocks, new_blocks, strict=True)) if a_block != b_block]
    assert changed == [134] and archive.matches(old_blocks[134]) == archive.matches(new_blocks[134]) == []
    old_rows, new_rows = [archive.common_rows(data[current.COMMON], data[current.ARM]) for data in (before, after)]
    known = []
    for key in sorted(keys):
        assert old_rows[key].text == new_rows[key].text
        known.append(dict(message_ID=key, payload_hex=new_rows[key].text.hex()))
    observed_keys = sorted({r["request"]["message_ID"] for r in play["records"]} |
                           {r["message_ID"] for r in play["unrendered_in_captured_holds_level_up_requests"]})
    assert observed_keys == [49, 65, 97] and not keys.intersection(observed_keys)
    # The odd return address is a Thumb return into the already bound level-up site.
    thumb, = [r for r in rows if r["call_site"] == 0x0207E3DE and r["entry"] == 0x0205528C]
    assert thumb["possible_COMMON_ids"] == [97]
    assert all(r["caller_LR"] == ((thumb["call_site"] + 4) | 1) for r in play["unrendered_in_captured_holds_level_up_requests"])
    write(OUT, dict(candidate_sha256=latest["candidate_sha256"], inherited_dispositions=reference(earlier.OUT),
        exact_census_count=len(expected), sole_ARM9_delta=dict(offset=slot, bytes=16),
        affected_story_blocks={STORY: changed}, no_new_archived_number_operands_in_affected_story=True,
        retained_archived_entries=known, observed_COMMON_ids=observed_keys, level_up_reference=thumb,
        five_display_owners_still_open_outside_bounded_census=True, ordinary_gameplay=reference(observed.OUT),
        sources=list(map(reference, (earlier.current.RELEASE, current.RELEASE))), new_editorial_credit=0))
    print("Carried all 827 earlier COMMON dispositions forward and confirmed the three observed Copenhagen IDs are already scoped.")


if __name__ == "__main__":
    main()
