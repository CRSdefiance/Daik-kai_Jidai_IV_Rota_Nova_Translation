"""Carry the exact four-route census through later registered story batches."""

from collections import Counter
from pathlib import Path
import re

from scripts import bind_shared_display_after_hodram_20261123 as shared
from scripts import reconcile_route_coverage_at_hodram_B324_20261122 as baseline
from scripts import register_hodram_b261_b310_wrap_fixes_20261123 as current


base, native = current.base, current.native
OUT = shared.OUTPUT.parent / "current_route_coverage_20261123.json"
ROUTES = tuple(f"/data/SC{i}.DK4" for i in range(4))
STORY_ID = re.compile(r"(?:DK4_MES_|SC[0-3]_)B(\d+)_")
GATES = ("source", "context", "localization", "naturalness", "formatting")


def story_blocks(image):
    return {path: native.IlnkContainer.parse(image.read_file(path)).blocks for path in ROUTES}


def reviewed_blocks(review):
    assigned = Counter()
    for row in review["records"]:
        path = row["file_path"]
        if path not in ROUTES:
            continue
        ident = STORY_ID.match(row["id"])
        if ident is None and not isinstance(row.get("block"), int):
            continue
        block = row.get("block", int(ident[1]) if ident else None)
        assert all(row["review"][k] for k in GATES), (path, row["id"])
        assigned[path, block] += 1
    return assigned


def main():
    old, latest, starting = map(base.load, (baseline.build.RELEASE, current.RELEASE, baseline.OUT))
    assert not OUT.exists()
    assert old["candidate_sha256"] == starting["candidate_sha256"] == base.digest(baseline.build.ROM)
    assert current.ROM.is_file() and latest["candidate_sha256"] == base.digest(current.ROM)
    assert latest["registry_sha256"] == base.digest(base.REGISTRY)
    assert old["clean_input_sha256"] == latest["clean_input_sha256"] == base.digest(native.CLEAN)
    assert old["manifest_sha256"] == base.digest(baseline.build.MANIFEST)
    assert latest["manifest_sha256"] == base.digest(current.MANIFEST)
    mapped, value = (current.scope[name] for name in ("mapped", "value"))
    with mapped(baseline.build.MANIFEST) as manifest:
        former = value(manifest, "batches", 2)
    with mapped(current.MANIFEST) as manifest:
        total = value(manifest, "batches", 2)
    assert total[:len(former)] == former

    archive = base.NdsImage.open(baseline.build.ROM)
    before = story_blocks(archive)
    last = {path: {} for path in ROUTES}
    evidence = []
    predecessor = old["candidate_sha256"]
    for review_path in map(Path, total[len(former):]):
        receipt = review_path.with_name("registered_release_verification.json")
        package = review_path.parent.parent
        release, review, checksums = map(base.load, (receipt, review_path, package / "checksums.json"))
        for p in (receipt, review_path):
            assert base.digest(p) == checksums[p.relative_to(package).as_posix()], p
        digest = release["candidate_sha256"]
        assert release["predecessor"]["candidate_sha256"] == predecessor
        assert digest == base.digest(Path(release["candidate"]))
        assert review["candidate_sha256"] == digest
        image = base.NdsImage.open(Path(release["candidate"]))
        after = story_blocks(image)
        owners = reviewed_blocks(review)
        proof_path = review_path.with_name("stored_proof.json")
        group_proofs = {}
        if proof_path.is_file():
            assert base.digest(proof_path) == checksums[proof_path.relative_to(package).as_posix()]
            for g in base.load(proof_path).get("groups", ()):
                if g.get("file_path") in ROUTES and "after" in g:
                    group_proofs[g["file_path"], g["block"]] = g["after"]
        changes = {}
        for i, path in enumerate(ROUTES):
            data = image.read_file(path)
            assert native.digest(data) == release[f"target_SC{i}_sha256"], (receipt, path)
            touched = [j for j, (a, b) in enumerate(zip(before[path], after[path], strict=True)) if a != b]
            for block in touched:
                key = (path, block)
                assert owners[key] > 0 or key in group_proofs, (receipt, key)
                if key in group_proofs:
                    assert group_proofs[key] == native.digest(after[path][block]), (receipt, key)
                last[path][block] = str(review_path)
            if touched:
                changes[path] = touched
        evidence.append(dict(candidate_sha256=digest, review=str(review_path), review_sha256=base.digest(review_path),
            release_sha256=base.digest(receipt), previous_sha256=predecessor, changed_story_blocks=changes))
        predecessor, before = digest, after
    assert predecessor == latest["candidate_sha256"] and before == story_blocks(base.NdsImage.open(current.ROM))
    routes = {}
    for i, path in enumerate(ROUTES):
        row = starting["routes"][path]
        assert base.digest(Path(row["census"])) == row["census_sha256"]
        assert row["exact_credited_clean_positions"] == (6887, 5356, 6720, 5129)[i]
        routes[path] = dict(exact_credited_clean_positions=row["exact_credited_clean_positions"],
            source_census=dict(path=row["census"], sha256=row["census_sha256"]),
            installed_archive_sha256=latest[f"target_SC{i}_sha256"], later_reviewed_blocks=last[path])
    result = dict(candidate_sha256=latest["candidate_sha256"], registry_sha256=latest["registry_sha256"],
        starting_coverage=dict(path=str(baseline.OUT), sha256=base.digest(baseline.OUT)),
        manifest_prefix_exact=True, registration_successors=evidence, routes=routes,
        exact_credited_clean_positions=sum(r["exact_credited_clean_positions"] for r in routes.values()),
        bounded_to_existing_census=True, independent_gameplay_added=False, new_editorial_credit=0)
    base.save(OUT, result)
    print("Bound", result["exact_credited_clean_positions"], "story positions through",
          len(evidence), "registered updates. Later reviewed blocks:", {p: len(v) for p, v in last.items()})


if __name__ == "__main__":
    main()
