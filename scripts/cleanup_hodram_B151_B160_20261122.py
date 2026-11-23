"""Remove verified duplicates after the farewell and recruitment handoff."""

from scripts import cleanup_hodram_B131_B150_20261122 as previous
from scripts import register_hodram_B151_B160_20261122 as release
from scripts.source_locked_derivation_v5118 import checked_text


base, stage = release.base, release.stage


def redundant_test_files(candidate_sha, patch_sha):
    earlier = stage.ROOT.with_name("B151_B160_staged_v2")
    staged = earlier / stage.ROM.name
    duplicate = earlier / "clean_rebuilt.nds"
    old_sha = base.digest(staged)
    assert old_sha != candidate_sha and base.digest(duplicate) == old_sha
    return {
        duplicate: old_sha,
        stage.ROOT / "clean_rebuilt.nds": candidate_sha,
        stage.ROOT / "translation.xdelta": patch_sha,
    }


source = checked_text(previous.source, {
    '"release_stack_with_hodram_B131_B150.json"': '"release_stack_with_hodram_B151_B160.json"',
})
scope = previous.scope | globals()
exec(compile(source, __file__ + "::checkpoint-cleanup", "exec"), scope)


if __name__ == "__main__":
    scope["main"]()

