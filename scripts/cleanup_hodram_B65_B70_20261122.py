"""Remove verified duplicate rebuilds and disposable playback artifacts."""

from scripts import cleanup_hodram_B61_B64_20261122 as previous
from scripts import register_hodram_B65_B70_20261122 as release
from scripts.source_locked_derivation_v5118 import checked_text


base, stage = release.base, release.stage


def redundant_test_files(candidate_sha, patch_sha):
    return {
        stage.ROOT / "clean_rebuilt.nds": candidate_sha,
        stage.ROOT / "translation.xdelta": patch_sha,
    }


source = checked_text(previous.source, {
    '"release_stack_with_hodram_B61_B64.json"': '"release_stack_with_hodram_B65_B70.json"',
})
scope = previous.scope | globals()
exec(compile(source, __file__ + "::checkpoint-cleanup", "exec"), scope)


if __name__ == "__main__":
    scope["main"]()
