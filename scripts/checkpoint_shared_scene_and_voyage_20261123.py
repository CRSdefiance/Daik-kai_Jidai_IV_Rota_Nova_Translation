"""Record the current COMMON encoding scope and dependency-checked duplicate cleanup."""

from collections import Counter
from pathlib import Path

from scripts import reconcile_shared_movie_labels_20261123 as movies
from scripts import verify_additional_voyages_20261123 as voyages


base, native, current = movies.base, movies.native, movies.current
OUT = movies.OUT.with_name("scene_and_voyage_checkpoint_20261123.json")


def main():
    assert not OUT.exists()
    release, scenes, played = map(base.load, (current.RELEASE, movies.OUT, voyages.OUTPUT))
    candidate = base.digest(current.ROM)
    assert candidate == release["candidate_sha256"] == scenes["candidate_sha256"] == played["candidate_sha256"]
    assert base.digest(base.REGISTRY) == release["registry_sha256"]
    image = base.NdsImage.open(current.ROM)
    assert native.digest(image.read_file(current.COMMON)) == release["target_COMMON_sha256"]
    rows = movies.current.stage.observed.prior.shared.paired.prior.entries(image)
    assert {row.message_id for row in rows} == set(range(3668))
    shared = base.load(current.REVIEW)["shared_consumer_binding"]["records"]
    pending = {row["message_ID"] for row in shared}
    proven = [row for row in rows if row.message_id not in pending]
    assert len(pending) == 276 and len(proven) == 3392
    mapped, value, field = (current.scope[name] for name in ("mapped", "value", "field"))
    with mapped(base.LEDGER) as data:
        assert value(data, "current_integrated_candidate", 1)["sha256"] == candidate
        assert value(data, "records_editorially_completed", 1) == 27700
        _, start, end, _ = field(data, base.CONTEXT, 1)
        credit = value(data, "integrated_record_keys", 2, start, end)
        credited_COMMON = {int(row["id"].split("_")[-1]) for row in credit if row["file_path"] == current.COMMON}
        assert credited_COMMON == {row.message_id for row in proven}
    non_ascii = [row for row in rows if not row.text.isascii()]
    assert not any(row.message_id not in pending for row in non_ascii)
    outstanding = Counter()
    affected = []
    for row in non_ascii:
        text = row.text.decode("cp932")
        grouping = "scene_or_opening_label" if 3393 <= row.message_id <= 3606 else (
            "online_and_extras_copy" if 3289 <= row.message_id <= 3319 else "other")
        if grouping == "other":
            assert row.message_id == 318 and "Ｉf" in text
        outstanding[grouping] += 1
        affected.append(dict(message_ID=row.message_id, full_width_I_lead=row.message_id == 318,
            grouping=grouping, characters="".join(sorted({char for char in text if ord(char) > 127})),
            reference=current.stage.town.reference(row), exact_stored_hex=row.text.hex()))
    assert outstanding == {"scene_or_opening_label": 214, "online_and_extras_copy": 31, "other": 1}
    assert played["exact_gameplay_holds"] == 11 and played["distinct_reviewed_messages"] == 6
    for case in played["cases"].values():
        assert not case["pending_requests"] and case["ordinary_input_only_saved_gameplay"]
        for sheet in case["sheets"]:
            assert base.digest(Path(sheet["path"])) == sheet["sha256"]
    originals = base.load(movies.atlas.ROOT / "texture_inventory.json")["movie_archives"]
    retained = scenes["visual_comparison_of_57_texture_pairs"]
    assert originals.keys() == retained.keys()
    removed = []
    root = movies.atlas.ROOT.resolve()
    for name, item in originals.items():
        source, keep = item["sheet"], retained[name]["sheet"]
        old, current_copy = Path(source["path"]), Path(keep["path"])
        assert old.parent.resolve() == root and old.resolve() != current_copy.resolve()
        assert not old.is_symlink() and not current_copy.is_symlink()
        sha = base.digest(current_copy)
        assert sha == source["sha256"] == keep["sha256"]
        if old.is_file():
            assert base.digest(old) == sha
            length = old.stat().st_size
            old.unlink()
            removed.append(dict(path=str(old), kept=str(current_copy), sha256=sha, bytes=length))
    base.save(OUT, dict(candidate_sha256=candidate, clean_sha256=release["clean_input_sha256"],
        editorial_credits=27700, ASCII_credited_COMMON_entries=len(proven), pending_stored_COMMON_entries=len(pending),
        non_ASCII_stored_count=len(non_ascii), pending_encoding_breakdown=dict(outstanding),
        pending_non_ASCII_stored_references=affected,
        encoded_scope="COMMON getter's stored table. External text assets, intentional full-width UI, runtime names and substitutions have separate proofs.",
        visual_review=dict(voyage_sheets=4, texture_sheets=10),
        evidence={str(path):base.digest(path) for path in (movies.OUT, voyages.OUTPUT, current.RELEASE)},
        cleanup=dict(removed=removed, reclaimed_duplicate_bytes=sum(row["bytes"] for row in removed)),
        new_editorial_credit=0, full_goal_complete=False))
    print(f"Confirmed 3,392 credited COMMON entries in ASCII and removed {len(removed)} exact duplicate contact sheets.")


if __name__ == "__main__":
    main()
