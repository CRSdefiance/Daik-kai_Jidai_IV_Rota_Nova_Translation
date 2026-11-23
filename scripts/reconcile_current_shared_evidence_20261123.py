"""Rebind shared-text counterparts and check the 35 unassociated source records."""

from collections import Counter
from pathlib import Path

from scripts import bind_shared_display_after_hodram_20261123 as paired
from scripts import checkpoint_shared_display_worklist_20261120 as prior
from scripts import register_regional_rumor_wrap_followups_20261123 as current


base, native = current.base, current.native
OUT = paired.OUTPUT.with_name("current_shared_display_evidence_20261123.json")
PREVIOUS = paired.paired.prior.OUTPUT
OWNERS = prior.previous.OUTPUT


def literal_matches(files, text):
    for path, data in files.items():
        offset = data.find(text)
        while offset != -1:
            yield dict(file_path=path, offset=offset)
            offset = data.find(text, offset + 1)


def main():
    assert not OUT.exists()
    release, review, list_before, ownership = map(base.load, (current.RELEASE, current.REVIEW, PREVIOUS, OWNERS))
    candidate = release["candidate_sha256"]
    assert candidate == review["candidate_sha256"] == base.digest(current.ROM)
    assert release["registry_sha256"] == base.digest(base.REGISTRY)
    assert release["clean_input_sha256"] == list_before["clean_sha256"] == base.digest(native.CLEAN)
    earlier = prior.previous.current
    previous = base.load(earlier.RELEASE)
    assert ownership["candidate_sha256"] == previous["candidate_sha256"] == base.digest(earlier.ROM)
    clean, installed, historical = map(base.NdsImage.open, (native.CLEAN, current.ROM, earlier.ROM))
    active_captions = prior.revalidate_displays(clean, installed, historical, ownership)
    assert len(active_captions) == 164
    clean_files = native.files(clean)
    bound = {row["message_ID"]: row for row in review["shared_consumer_binding"]["records"]}
    priorities = set(base.load(paired.OUTPUT)["legacy_and_unassociated_first_pass"])
    raw = []
    totals = Counter()
    for row in list_before["records"]:
        key = row["message_ID"]
        installed_ref = bound.pop(key)["installed"]
        disposition = row["established_display_scope"]
        record = dict(message_ID=key, source_reference=row["source_reference"], source_hex=row["source_hex"],
            installed_reference=installed_ref, installed_hex=row["current_hex"], earlier_draft=row["draft"],
            established_use=disposition, other_stored_COMMON_display_paths="unverified")
        if key in priorities:
            hits = list(literal_matches(clean_files, bytes.fromhex(row["source_hex"])))
            assert len(hits) == 1 and hits[0]["file_path"] == current.COMMON
            record["exact_clean_stored_byte_locations"] = hits
        else:
            for item in row["independent_gallery_draw_sources"]:
                a, b = item["clean"], item["current"]
                caption = active_captions[b["route"], b["position"]]
                assert a["text_hex"] == row["source_hex"] and caption["English"].encode("ascii").hex() == b["text_hex"]
                assert caption["pointer"] == b["pointer"] and caption["bounds"][0] == b["draw_x"]
            for name in ("independent_gallery_draw_sources", "story_still_filename", "story_image_request",
                         "opening_artwork_association", "tested_Online_and_About_Extras_use_separate_ARM9_text",
                         "separate_chooser_biography_review"):
                if row.get(name):
                    record[name] = row[name]
        raw.append(record)
        totals[disposition] += 1
    assert not bound and len(raw) == 276 and len(priorities) == 35
    result = dict(candidate_sha256=candidate, clean_sha256=release["clean_input_sha256"],
        source_worklist=dict(path=str(PREVIOUS), sha256=base.digest(PREVIOUS)),
        installed_shared_binding=dict(path=str(current.REVIEW), sha256=base.digest(current.REVIEW)),
        reused_independent_evidence=dict(path=str(OWNERS), sha256=base.digest(OWNERS)),
        counts_by_established_use=dict(totals), independent_evidence_rebound=241, literal_scan_keys=sorted(priorities),
        literal_scan_scope="Stored file bytes from the clean ROM, with no inference about runtime-generated, compressed or alternate displays.",
        records=raw, new_gameplay_runs=0, new_editorial_credit=0)
    base.save(OUT, result)
    print("Revalidated 241 independent associations. For each of the other 35 records, the only exact stored clean copy is in COMMON.")


if __name__ == "__main__":
    main()
