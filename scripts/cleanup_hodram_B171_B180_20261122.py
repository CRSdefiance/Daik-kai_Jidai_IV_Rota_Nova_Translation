"""Remove verified duplicates after the Proofs and harbor handoff."""

from scripts import cleanup_hodram_B161_B170_20261122 as previous
from scripts import register_hodram_B171_B180_20261122 as release
from scripts.source_locked_derivation_v5118 import checked_text


base, stage = release.base, release.stage


def redundant_test_files(candidate_sha, patch_sha):
    early = stage.ROOT.with_name("B171_B180_staged_v1")
    early_sha = base.digest(early / stage.ROM.name)
    assert early_sha != candidate_sha and base.digest(early / "clean_rebuilt.nds") == early_sha
    return {early / "clean_rebuilt.nds": early_sha,
            stage.ROOT / "clean_rebuilt.nds": candidate_sha, stage.ROOT / "translation.xdelta": patch_sha}


source = checked_text(previous.source, {
    '"release_stack_with_hodram_B161_B170.json"': '"release_stack_with_hodram_B171_B180.json"',
})
scope = previous.scope | globals()
exec(compile(source,__file__+"::checkpoint-cleanup","exec"),scope)


if __name__ == "__main__":
    scope["main"]()
