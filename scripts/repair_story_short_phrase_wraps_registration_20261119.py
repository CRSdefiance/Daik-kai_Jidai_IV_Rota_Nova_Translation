"""Restore inherited manifest entries alongside the new phrase-wrap checks."""

from copy import deepcopy

from scripts import register_story_short_phrase_wraps_20261119 as registered


base = registered.base
workflow, windows = registered.env["workflow"], registered.env["windows"]
BACKUP = registered.stage.ROOT / "registration_metadata_correction"


def main():
    r = registered
    registry_draft = r.ROOT / "release_stack_with_story_phrase_wraps.json"
    receipt = r.VERIFY / "registration_mutation_plan.json"
    package_receipt = r.PACKAGE / "release_manifest.json"
    manifest_gz = r.PACKAGE / "build_manifest.json.gz"
    registry_gz = r.PACKAGE / "build_release_stack.json.gz"
    checksum_path = r.PACKAGE / "checksums.json"
    ledger_raw = base.LEDGER.read_bytes()
    previous, current, stack, release, plan, ledger, checksums = map(base.load, (
        r.parent.MANIFEST, r.MANIFEST, base.REGISTRY, r.RELEASE, receipt, base.LEDGER, checksum_path))
    assert base.digest(r.ROM) == release["candidate_sha256"] and base.digest(r.PATCH) == release["patch_sha256"]
    assert base.digest(r.MANIFEST) == release["manifest_sha256"]
    assert base.digest(base.REGISTRY) == base.digest(registry_draft) == plan["registry_after"]
    assert r.native.digest(ledger_raw) == plan["ledger_after"] and base.digest(base.PROMOTED) == plan["main_sha256"]
    assert checksums == workflow.package_checksums(r.PACKAGE)
    assert current["checks"] == previous["checks"] and len(current["checks"]) == 233
    profile = stack["profiles"][r.PROFILE]
    old_profile = stack["profiles"][r.parent.PROFILE]
    assert profile["story_phrase_wraps_release"] == str(r.REVIEW)
    profile["story_short_phrase_wraps_release"] = profile["story_phrase_wraps_release"]
    profile["story_phrase_wraps_release"] = old_profile["story_phrase_wraps_release"]
    assert all(profile[k] == v for k, v in old_profile.items())
    pipeline = current["story_phrase_wraps_pipeline"]
    assert pipeline["registered_review"] == str(r.REVIEW)
    current["story_phrase_wraps_pipeline"] = deepcopy(previous["story_phrase_wraps_pipeline"])
    current["story_short_phrase_wraps_pipeline"] = pipeline | {"registration_driver_sha256": base.digest(r.__file__)}
    current["checks"]["registered_story_short_phrase_wraps_and_complete_parent_inverse"] = True

    BACKUP.mkdir()
    targets = (base.REGISTRY, registry_draft, r.MANIFEST, manifest_gz, registry_gz, r.RELEASE, package_receipt,
        receipt, checksum_path)
    before = {p: p.read_bytes() for p in targets}
    for i, (path, data) in enumerate(before.items()):
        workflow.archive_file(data, BACKUP / f"before_{i}_{path.name}.gz")
    workflow.archive_file(ledger_raw, BACKUP / "before_ledger.json.gz")

    def item(name, value):
        path = BACKUP / name
        base.save(path, value)
        return path.read_bytes()

    stack_raw = item("stack.json", stack)
    stack_sha = r.native.digest(stack_raw)
    current["release_stack_sha256"] = stack_sha
    manifest_raw = item("manifest.json", current)
    manifest_sha = r.native.digest(manifest_raw)
    release.update(registry_sha256=stack_sha, manifest_sha256=manifest_sha, passing_release_checks=len(current["checks"]))
    ledger["current_integrated_candidate"]["manifest_sha256"] = manifest_sha
    ledger_new = workflow.encode_ledger(ledger)
    plan.update(registry_after=stack_sha, ledger_after=r.native.digest(ledger_new))
    staged = {base.REGISTRY: stack_raw, registry_draft: stack_raw, r.MANIFEST: manifest_raw,
        r.RELEASE: item("verification.json", release), package_receipt: item("package.json", release | {"user_acceptance_pending": True}),
        receipt: item("plan.json", plan)}
    for raw, path in ((manifest_raw, manifest_gz), (stack_raw, registry_gz)):
        archived = BACKUP / path.name
        workflow.archive_file(raw, archived)
        staged[path] = archived.read_bytes()
    for path, data in staged.items():
        if path.is_relative_to(r.PACKAGE):
            checksums[path.relative_to(r.PACKAGE).as_posix()] = r.native.digest(data)
    staged[checksum_path] = item("checksums.json", checksums)
    assert staged.keys() == before.keys()
    assert all(p.read_bytes() == data for p, data in before.items()) and base.LEDGER.read_bytes() == ledger_raw
    updated = []
    try:
        for path, data in staged.items():
            base.replace_checked(path, data)
            updated.append(path)
        assert workflow.package_checksums(r.PACKAGE) == checksums
        windows.update_ledger_in_place(ledger_raw, ledger_new)
    except (AssertionError, OSError):
        for path in reversed(updated):
            base.replace_checked(path, before[path])
        raise
    assert base.digest(base.PROMOTED) == plan["main_sha256"]
    assert base.digest(r.ROM) == release["candidate_sha256"] and base.digest(r.PATCH) == release["patch_sha256"]
    print("Verified 234 passing checks with all inherited release references preserved.")


if __name__ == "__main__":
    main()
