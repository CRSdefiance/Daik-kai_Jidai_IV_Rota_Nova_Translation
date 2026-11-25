"""Clear duplicate and disposable files after publishing the Hodram candidate."""

from gzip import open as open_gzip
from hashlib import file_digest

from scripts import cleanup_rafael_B306_B309_20261122 as previous
from scripts import register_hodram_opening_20261122 as release
from scripts.source_locked_derivation_v5118 import checked_text


base, stage = release.base, release.stage
PARKED = tuple(root.with_name(root.name + "_unregistered_ledger_aliases")
               for root in (release.ROOT, release.PACKAGE))


def redundant_test_files(candidate_sha, patch_sha):
    discarded = {stage.ROOT / "clean_rebuilt.nds": candidate_sha,
                 stage.ROOT / "translation.xdelta": patch_sha}
    for old_root, kept_root in zip(PARKED, (release.ROOT, release.PACKAGE), strict=True):
        if not old_root.exists():
            continue
        assert not old_root.is_symlink() and not old_root.is_junction()
        for old in old_root.rglob("*"):
            if old.is_symlink() or old.is_junction() or not old.is_file():
                continue
            assert old.resolve().is_relative_to(old_root.resolve())
            relative = old.relative_to(old_root)
            kept = kept_root / relative
            if not kept.is_file():
                continue
            if old.stat().st_size == kept.stat().st_size and base.digest(old) == base.digest(kept):
                discarded[old] = base.digest(old)
            elif relative.name == "editorial_ledger_before.json.gz":
                with open_gzip(old, "rb") as source, open_gzip(kept, "rb") as target:
                    assert file_digest(source, "sha256").hexdigest() == file_digest(target, "sha256").hexdigest()
                discarded[old] = base.digest(old)
    return discarded


source = checked_text(previous.source, {
    '"release_stack_with_rafael_B306_B309.json"': '"release_stack_with_hodram_B24_B53.json"',
    '(stage.ROOT.parent, release.ROOT)': '(stage.ROOT.parent, release.ROOT, *PARKED)',
    '".nds", ".xdelta"}': '".nds", ".xdelta", ".gz", ".xml"}',
})
scope = previous.scope | globals()
exec(compile(source, __file__ + "::verified-Hodram-checkpoint-cleanup", "exec"), scope)


if __name__ == "__main__":
    scope["main"]()
