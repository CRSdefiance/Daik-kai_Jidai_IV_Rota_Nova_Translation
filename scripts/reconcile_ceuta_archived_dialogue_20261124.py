"""Check the archived dialogue leads against the registered Ceuta build and runtime requests."""

from collections import Counter

from scripts import reconcile_common_observed_callers_20261124 as callers
from scripts import register_ceuta_contract_refusal_20261124 as release
from scripts import verify_archived_message_storage_20261124 as archive
from scripts import verify_athens_palace_contract_20261124 as athens
from scripts import verify_valencia_government_20261124 as valencia
from scripts.stage_cartridge_title_20261123 import CLEAN, NdsImage, REGISTRY, digest, read, reference, sha256, write


OUT = valencia.OUT.with_name("ceuta_archived_dialogue_current_20261124.json")
SOURCE_TERMS = {
    "艦隊の借金": 284,
    "フェアデータ": 318,
    "本当にやり直す": 750,
    "面倒だねえ": 751,
    "冗談は勘弁": 752,
    "フェア用": None,
    "体験版": None,
    "展示会": None,
}


def source_terms(clean, originals):
    terms = {term: term.encode("cp932") for term in SOURCE_TERMS}
    hits = {term: [] for term in terms}
    for identity, payload in archive.payloads(clean):
        for term, encoded in terms.items():
            hits[term].extend(identity | {"archive_offset": offset} for offset in archive.offsets(payload, encoded))
    for term, key in SOURCE_TERMS.items():
        assert len(hits[term]) == (0 if key is None else 1)
        if key is not None:
            assert terms[term] in originals[key].text
            assert hits[term][0]["path"] == archive.COMMON
    return hits


def observed_requests(manifest):
    census, bounds = map(read, (callers.CENSUS, callers.BOUNDS))
    assert bounds["inherited_dispositions"] == reference(callers.CENSUS)
    domains = {(row["call_site"], row["entry"]): row["possible_COMMON_ids"] for row in census["references"]}
    assert len(domains) == bounds["fully_bounded_census_sites"] == 827
    for row in bounds["completed_bindings"]:
        site = (row["call_site"], row["target"])
        assert domains[site] is None
        domains[site] = row["ids"]

    visits = {}
    for city, proof in (("Athens", athens.OUT), ("Valencia", valencia.OUT)):
        packet = read(proof)
        assert packet["ordinary_gameplay"] and packet["candidate_sha256"] == manifest["candidate_sha256"]
        receipt = packet["evidence"]["trace"]
        assert digest(receipt["path"]) == receipt["sha256"]
        trace = read(receipt["path"])
        assert trace["all_host_slots_restored_and_core_file_exact"] and not trace["errors"] and not trace["mismatches"]
        rows = trace["source_requests"]
        counted = Counter()
        for opened, copied in zip(rows[::2], rows[1::2], strict=True):
            assert opened["PC"] == callers.GETTER and copied == opened | {"PC": callers.COPIER}
            key = opened["message_ID"]
            site = (opened["caller_LR"] & ~1) - 4
            assert key in domains[site, callers.GETTER] and key not in archive.KEYS
            counted[site, key] += 1
        assert sum(count for (_, key), count in counted.items() if key == 761) == (3 if city == "Athens" else 1)
        visits[city] = dict(ordinary_gameplay=reference(proof), trace=receipt, requests=[
            dict(call_site=site, message_ID=key, count=count) for (site, key), count in sorted(counted.items())])
    return visits


def main():
    manifest = read(release.RELEASE)
    previous = read(release.parent.RELEASE)
    assert digest(REGISTRY) == manifest["registry_sha256"] and digest(CLEAN) == manifest["clean_input_sha256"]
    assert digest(release.ROM) == manifest["candidate_sha256"] and digest(previous["candidate"]) == previous["candidate_sha256"]
    clean, prior, current = map(NdsImage.open, (CLEAN, previous["candidate"], release.ROM))
    old_files, new_files = map(release.draft.native.files, (prior, current))
    assert old_files.keys() == new_files.keys()
    assert [path for path in old_files if old_files[path] != new_files[path]] == [archive.COMMON]
    arm = new_files[archive.ARM]
    assert sha256(arm).hexdigest() == manifest["target_ARM9_sha256"] == previous["target_ARM9_sha256"]
    assert sha256(new_files[archive.COMMON]).hexdigest() == manifest["target_COMMON_sha256"]
    originals = archive.common_message_entries(clean.read_file(archive.COMMON), clean.read_file(archive.ARM))
    before, after = (archive.common_rows(parts[archive.COMMON], arm) for parts in (old_files, new_files))
    assert [a.message_id for a, b in zip(before, after, strict=True) if a.text != b.text] == [761]
    stored = {}
    for key in archive.KEYS:
        a, b = map(valencia.review.source_ref, (before[key], after[key]))
        assert a == b
        stored[key] = dict(clean_Japanese=originals[key].text.decode("cp932"),
            clean_reference=valencia.review.source_ref(originals[key]), installed_reference=b,
            display_owner="unverified outside the checked callers")
    proof = dict(candidate_sha256=manifest["candidate_sha256"], registered_release=reference(release.RELEASE),
        prior_release=reference(release.parent.RELEASE), archived_records=stored,
        source_term_search=source_terms(clean, originals), observed_requests=observed_requests(manifest),
        offline_scope="Exact CP932 byte sequences, including decompressed overlays. Absence does not establish runtime unreachability.",
        caller_census=reference(callers.CENSUS), caller_argument_bounds=reference(callers.BOUNDS),
        five_display_owners_still_open=True, ROM_changed=False, new_editorial_credit=0)
    write(OUT, proof)
    print("Verified five archived payloads on Ceuta and reconciled the ordinary Athens and Valencia COMMON requests.")


if __name__ == "__main__":
    main()
