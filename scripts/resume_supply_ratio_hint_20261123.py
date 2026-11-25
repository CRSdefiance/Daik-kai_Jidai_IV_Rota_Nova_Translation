"""Finish the verified Supply Ratio transaction after interrupted ledger storage."""

from gzip import open as open_gzip
from hashlib import file_digest
from pathlib import Path

from dk4tool.dialogue.review import validate_natural_dialogue_batch
from scripts import register_supply_ratio_hint_20261123 as r


def append_verified_suffix(data, path, edits):
    """Verify the partial prefix against the requested snapshot before completing it."""
    def chunks(start, stop):
        for at in range(start, stop, 1 << 20):
            yield data[at:min(at + (1 << 20), stop)]

    def payloads():
        old = 0
        for start, stop, replacement in sorted(edits):
            assert old <= start <= stop <= len(data)
            yield from chunks(old, start)
            yield replacement
            old = stop
        yield from chunks(old, len(data))

    with path.open("r+b") as stream:
        prefix_size = path.stat().st_size
        assert 0 < prefix_size < len(data)
        consumed = 0
        for payload in payloads():
            count = min(len(payload), max(0, prefix_size - consumed))
            assert stream.read(count) == payload[:count]
            if count < len(payload):
                assert stream.write(payload[count:]) == len(payload) - count
            consumed += len(payload)
        assert consumed > prefix_size


def main():
    previous, stored, draft, release = map(r.base.load, (r.parent.RELEASE, r.stage.PROOF, r.REVIEW, r.RELEASE))
    stored["changed_files"] = [stored["changed_file"]]
    candidate = stored["candidate_sha256"]
    assert candidate == release["candidate_sha256"] == draft["candidate_sha256"] == r.base.digest(r.ROM)
    assert r.ROM.samefile(r.REBUILT) and r.ROM.samefile(r.stage.ROM)
    assert r.base.digest(r.PATCH) == release["patch_sha256"] == r.base.digest(r.RESEARCH_PATCH)
    assert r.base.digest(r.MANIFEST) == release["manifest_sha256"]
    assert r.base.digest(release["own_registered_startup"]) == release["own_registered_startup_sha256"]
    snapshot = dict(registry_before=r.base.digest(r.base.REGISTRY), ledger_before=r.base.digest(r.base.LEDGER),
                    main_sha256=r.base.digest(r.base.PROMOTED))
    registry_backup, ledger_backup = r.REGISTRY_BACKUP, r.LEDGER_BACKUP
    assert r.base.digest(registry_backup) == snapshot["registry_before"] == previous["registry_sha256"]
    assert r.base.digest(ledger_backup) == snapshot["ledger_before"] == r.storage["ledger_sha256"]
    registry_next, ledger_next = (r.WORK / name for name in ("release_stack_with_supply_ratio_hint.json", "ledger_after.json"))
    registry_sha = r.base.digest(registry_next)
    assert registry_sha == release["registry_sha256"]
    with r.scope["mapped"](registry_next) as data:
        assert r.scope["value"](data, r.PROFILE, 4)["verified_sound_play_stop_predecessor"] == release["predecessor"]
    with r.scope["mapped"](r.MANIFEST) as data:
        assert r.scope["value"](data, "candidate_sha256", 2) == candidate
        assert len(r.scope["value"](data, "batches", 2)) == 1101
    for path, expected in ((r.PACKAGE / "build_manifest.json.gz", release["manifest_sha256"]),
                           (r.PACKAGE / "build_release_stack.json.gz", registry_sha),
                           (r.ROOT / "editorial_ledger_before.json.gz", snapshot["ledger_before"])):
        with open_gzip(path, "rb") as stream:
            assert file_digest(stream, "sha256").hexdigest() == expected
    validate_natural_dialogue_batch(draft)
    assert all(r.base.digest(path) == sha for path, sha in (draft["visual_review"] | draft["evidence"]).items())
    assert not any(p.exists() for p in (r.VERIFY / "registration_mutation_plan.json", r.DOC))
    r.base.save(r.VERIFY / "snapshot_resume.json", dict(verified_partial_ledger_bytes=ledger_next.stat().st_size,
        verified_partial_ledger_sha256=r.base.digest(ledger_next), preserved_predecessor_registry_sha256=snapshot["registry_before"],
        preserved_predecessor_ledger_sha256=snapshot["ledger_before"], driver_sha256=r.base.digest(Path(__file__))))
    archives = {r.ARM: release["target_ARM9_sha256"], r.COMMON: release["target_COMMON_sha256"]}
    start = r.build.index("    with mapped(base.LEDGER) as data:")
    names = ("snapshot", "previous", "stored", "draft", "candidate", "archives", "registry_sha",
             "registry_backup", "registry_next", "ledger_backup", "ledger_next", "release")
    environment, prepared = r.scope | {"write_update": append_verified_suffix}, locals()
    header = "def finish(" + ", ".join(names) + "):\n"
    exec(compile(header + r.build[start:], __file__ + "::finish-prepared-package", "exec"), environment)
    environment["finish"](*(prepared[name] for name in names))


if __name__ == "__main__":
    main()
